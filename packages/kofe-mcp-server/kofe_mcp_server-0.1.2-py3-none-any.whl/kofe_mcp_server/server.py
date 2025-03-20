import asyncio
import json
import os
from abc import ABC

import mcp.server.stdio
import mcp.types as types
import requests
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import os

agent_key = os.getenv('agent_key')
server = Server("kofe_app")

kofe_config= {
    "kofe_url": "https://www.iagent.cc/gateway/kofe/v1",
    "kofe_app_sks": [
        {
            "name": "翻译",
            "description": "实时翻译服务、自动文档翻译、支持工单翻译、产品描述翻译等，确保跨语言无缝沟通。",
            "app_name":"translation-copilot",
            "app_param": {
                "input_text": {
                    "string": {
                        "variable": "input_text",
                        "label": "Input Text",
                        "required": True
                    }
                },
                "target_language": {
                    "string": {
                        "variable": "target_language",
                        "label": "Target Language",
                        "required": True
                    }
                }
            }
        },  {
            "name": "简历生成",
            "description": "告诉我您的学术和职业历史，一个优秀的简历将立即生成！",
            "app_name":"resume-creator-agent",
            "app_param": {
                "Work_experience": {
                    "string": {
                        "variable": "Work_experience",
                        "label": "Input Text",
                        "required": True
                    }
                },
                "Output_language": {
                    "string": {
                        "variable": "Output_language",
                        "label": "Target Language",
                        "required": True
                    }
                }
            }
        }
    ]
}
class KofeAPI(ABC):
    def __init__(self, config_path, user="default_user"):


        if agent_key is None:
            raise ValueError("Agent key not found.")
        self.kofe_url = kofe_config.get("kofe_url")
        self.kofe_info = kofe_config.get("kofe_app_sks")

    def chat_message(
            self,
            api_key,
            app_name,
            inputs={},
            response_mode="streaming",
            conversation_id=None,
            user="default_user",
            files=None,):
        url = f"{self.kofe_url}/workflows/run"
        headers = {
            # "Authorization": f"Bearer {api_key}",
            "app_key": agent_key,
            "app_name": app_name,
            "Content-Type": "application/json"
        }
        data = {
            "inputs": inputs,
            "response_mode": response_mode,
            "user": user,
        }
        if conversation_id:
            data["conversation_id"] = conversation_id
        if files:
            files_data = []
            for file_info in files:
                file_path = file_info.get('path')
                transfer_method = file_info.get('transfer_method')
                if transfer_method == 'local_file':
                    files_data.append(('file', open(file_path, 'rb')))
                elif transfer_method == 'remote_url':
                    pass
            response = requests.post(
                url, headers=headers, data=data, files=files_data, stream=response_mode == "streaming")
        else:
            response = requests.post(
                url, headers=headers, json=data, stream=response_mode == "streaming")
        response.raise_for_status()
        if response_mode == "streaming":
            for line in response.iter_lines():
                if line:
                    if line.startswith(b'data:'):
                        try:
                            json_data = json.loads(line[5:].decode('utf-8'))
                            yield json_data
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON: {line}")
        else:
            return response.json()

    def upload_file(
            self,
            api_key,
            file_path,
            user="default_user"):

        url = f"{self.kofe_url}/files/upload"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        files = {
            "file": open(file_path, "rb")
        }
        data = {
            "user": user
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()

    def stop_response(
            self,
            api_key,
            task_id,
            user="default_user"):

        url = f"{self.kofe_url}/chat-messages/{task_id}/stop"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "user": user
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

kofe_api = KofeAPI( "")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    tools = [] 
    for app_info in kofe_api.kofe_info : 
        inputSchema = dict(
            type="object",
            properties={},
            required=[],
        ) 
        input_params = app_info.get("app_param", {})
        for j in input_params:
            param = input_params[j]
            param_type = list(param.keys())[0]
            param_info = param[param_type]
            property_name = param_info['variable']

            inputSchema["properties"][property_name] = dict(
                type=param_type,
                description=param_info['label'],
            )

            if param_info['required']:
                inputSchema['required'].append(property_name)
        tools.append(
            types.Tool(
                name=app_info['name'],
                description=app_info['description'],
                inputSchema=inputSchema,
            )
        )
    return tools


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    for app_info in kofe_api.kofe_info : 
        if app_info['name'] == name :  
            responses = kofe_api.chat_message(
                agent_key ,
                app_info.get('app_name'),
                arguments,
            )
            for res in responses:
                if res['event'] == 'workflow_finished':
                    outputs = res['data']['outputs']
            mcp_out = []
            for _, v in outputs.items():
                mcp_out.append(
                    types.TextContent(
                        type='text',
                        text=v
                    )
                )
            return mcp_out
    else:
        raise ValueError(f"Unknown tool: {name}")



async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Kofe_mcp_server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
