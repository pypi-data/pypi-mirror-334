import anyio
import click
import json
from datetime import datetime, timedelta
import mcp.types as types
from mcp.server.lowlevel import Server
from google.cloud import logging
from google.oauth2 import service_account
from google.auth.credentials import Credentials
import google.auth
from typing import Optional
from pathlib import Path


def get_credentials(service_account_path: Optional[str] = None) -> Credentials:
    """Get GCP credentials either from service account JSON or application default credentials."""
    if service_account_path:
        path = Path(service_account_path).expanduser().resolve()
        if not path.exists():
            raise ValueError(f"Service account file not found: {path}")
        return service_account.Credentials.from_service_account_file(str(path))
    
    # Try to get application default credentials (interactive auth)
    credentials, project = google.auth.default()
    return credentials


async def get_cloud_function_logs(
    project_id: str,
    function_name: str,
    minutes: int = 10,
    filter_str: Optional[str] = None,
    credentials: Optional[Credentials] = None,
) -> list[types.TextContent]:
    # Create client with specific credentials if provided
    if credentials:
        client = logging.Client(project=project_id, credentials=credentials)
    else:
        client = logging.Client(project=project_id)
    
    # Calculate the time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)
    
    # Build the filter
    base_filter = f'resource.type="cloud_function" resource.labels.function_name="{function_name}" '
    time_filter = f'timestamp >= "{start_time.isoformat()}Z" timestamp <= "{end_time.isoformat()}Z"'
    
    if filter_str:
        full_filter = f"{base_filter} AND {time_filter} AND {filter_str}"
    else:
        full_filter = f"{base_filter} AND {time_filter}"
    
    # Get logs
    logs = []
    for entry in client.list_entries(filter_=full_filter, order_by="timestamp asc"):
        timestamp = entry.timestamp.isoformat()
        severity = entry.severity
        message = entry.payload
        
        log_entry = f"[{timestamp}] {severity}: {message}"
        logs.append(log_entry)
    
    if not logs:
        return [types.TextContent(type="text", text="No logs found for the specified criteria.")]
    
    return [types.TextContent(type="text", text="\n".join(logs))]


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
@click.option(
    "--service-account",
    type=str,
    help="Path to service account JSON file. If not provided, will use application default credentials.",
    envvar="GCP_SERVICE_ACCOUNT_PATH",
)
def main(port: int, transport: str, service_account: Optional[str]) -> int:
    # Get credentials early to fail fast if auth issues
    try:
        credentials = get_credentials(service_account)
    except Exception as e:
        click.echo(f"Error setting up GCP authentication: {e}", err=True)
        return 1

    app = Server("gcp-function-logs")

    @app.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent]:
        if name != "get_function_logs":
            raise ValueError(f"Unknown tool: {name}")
            
        required_args = ["project_id", "function_name"]
        for arg in required_args:
            if arg not in arguments:
                raise ValueError(f"Missing required argument '{arg}'")
        
        minutes = arguments.get("minutes", 10)
        filter_str = arguments.get("filter", None)
        
        return await get_cloud_function_logs(
            project_id=arguments["project_id"],
            function_name=arguments["function_name"],
            minutes=minutes,
            filter_str=filter_str,
            credentials=credentials
        )

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="get_function_logs",
                description="Retrieves logs from a GCP Cloud Function",
                inputSchema={
                    "type": "object",
                    "required": ["project_id", "function_name"],
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "The GCP project ID",
                        },
                        "function_name": {
                            "type": "string",
                            "description": "The name of the Cloud Function",
                        },
                        "minutes": {
                            "type": "integer",
                            "description": "Number of minutes of logs to retrieve",
                            "default": 10,
                        },
                        "filter": {
                            "type": "string",
                            "description": "Additional filter for the logs",
                        },
                    },
                },
            )
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn
        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0

if __name__ == "__main__":
    main()
