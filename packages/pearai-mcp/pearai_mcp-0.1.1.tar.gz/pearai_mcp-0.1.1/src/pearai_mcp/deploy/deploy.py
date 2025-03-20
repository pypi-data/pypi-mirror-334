#!/usr/bin/env python3
import os
import aiohttp
import mcp.types as types

class DeploymentService:
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url
        self.auth_token = auth_token

    def get_tools(self) -> list[types.Tool]:
        """List available deployment tools."""
        return [
            types.Tool(
                name="deploy-webapp-from-path",
                description="Deploy a website application from a zip file path of the distribution folder",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "zip_file_path": {
                            "type": "string",
                            "description": "Absolute path to the zip file of the distribution folder to deploy"
                        },
                    },
                    "required": ["zip_file_path"],
                },
            )
        ]

    async def deploy_from_path(self, zip_file_path: str) -> list[types.TextContent]:
        """Deploy a website from a zip file path."""
        if not os.path.isabs(zip_file_path):
            raise ValueError("zip_file_path must be an absolute path")

        try:
            # Read zip file content
            with open(zip_file_path, 'rb') as f:
                zip_content = f.read()

            # Prepare form data
            form = aiohttp.FormData()
            form.add_field('zip_file',
                          zip_content,
                          filename='dist.zip',
                          content_type='application/zip')

            # Make POST request to deployment endpoint
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.server_url}/deploy-netlify',
                    headers={
                        "Authorization": f"Bearer {self.auth_token}"
                    },
                    data=form
                ) as response:
                    result = await response.text()
                    return [
                        types.TextContent(
                            type="text",
                            text=result
                        )
                    ]

        except FileNotFoundError:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": f"Zip file not found at path: {zip_file_path}"})
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": str(e)})
                )
            ]