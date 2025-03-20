from setuptools import setup, find_packages

setup(
    name="gcp-mcp-server",
    version="0.1.0",
    description="An MCP server providing tools for GCP Cloud Functions logs",
    author="Lee",
    packages=find_packages(),
    install_requires=[
        "anyio>=4.5",
        "click>=8.1.0",
        "mcp",
        "google-cloud-logging>=3.9.0",
        "google-cloud-functions>=1.15.0"
    ],
    entry_points={
        'console_scripts': [
            'gcp-mcp-server=gcp_mcp_server.server:main',
        ],
    },
    python_requires=">=3.10",
)
