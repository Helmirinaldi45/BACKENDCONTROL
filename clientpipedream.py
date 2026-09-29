import os
import asyncio
from datetime import datetime
from fastmcp import Client
from google import genai
from pipedream import Pipedream


async def run_gemini_with_mcp(inputs: str):
    CONTROLINPUTS: list[str] = [
        inputs + " " + "" if "" in inputs else inputs + " " + "",
        inputs + " " + "" if "" in inputs else inputs + " " + "",
    ]
    TOOLAUTOMATIONS: dict[str, bool] = {
        inputs + "" if "" in inputs else inputs + " " + "": True if "" in inputs else False,

    }
    # Initialize Pipedream client and get access token
    pd = Pipedream(
        project_id=os.environ.get('PIPEDREAM_PROJECT_ID'),
        project_environment=os.environ.get('PIPEDREAM_ENVIRONMENT'),
        client_id=os.environ.get('PIPEDREAM_CLIENT_ID'),
        client_secret=os.environ.get('PIPEDREAM_CLIENT_SECRET'),
    )
    FILTERAPPS: list[str] = [
        apps for apps in pd.apps.list()
        if apps.name_slug in [
            "",
            "",
            "",
            ""
        ]
    ]
    OLAHQUERYPROMPT: list[str] = [
        prompts for prompts in FILTERAPPS
        if prompts in inputs
    ]
    access_token = await pd.raw_access_token

    # Initialize Gemini client
    client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))

    # Initialize MCP client with Pipedream
    mcp_client = Client({
        "mcpServers": {
            "pipedream": {
                "transport": "http",
                "url": "https://remote.mcp.pipedream.net/v3",
                "headers": {
                    "Authorization": f"Bearer {access_token}",
                    "x-pd-project-id": os.environ.get('PIPEDREAM_PROJECT_ID'),
                    "x-pd-environment": os.environ.get('PIPEDREAM_ENVIRONMENT'),
                    "x-pd-external-user-id": "user-123",  # Your user's unique ID
                    "x-pd-app-slug": "gmail, google_calendar",  # Apps to use
                },
            }
        }
    })

    async with mcp_client:
        # Configure Gemini with MCP tools and system instructions
        config = genai.types.GenerateContentConfig(
            temperature=0,
            tools=[mcp_client.session],
            system_instructions="",
        )

        # Create chat session
        chat = client.aio.chats.create(model="gemini-2.0-flash-exp", config=config)

        # Send user message
        user_message = "Check my recent emails and summarize the important ones"

        print(f"User: {user_message}")

        # Generate response with automatic tool calling
        response = await chat.send_message(user_message)

        print(f"Gemini: {response.text}")

        # Continue conversation if needed
        follow_up = "Can you schedule a meeting based on the most important email?"
        print(f"User: {follow_up}")

        response = await chat.send_message(follow_up)
        print(f"Gemini: {response.text}")


if __name__ == "__main__":
    asyncio.run(run_gemini_with_mcp())