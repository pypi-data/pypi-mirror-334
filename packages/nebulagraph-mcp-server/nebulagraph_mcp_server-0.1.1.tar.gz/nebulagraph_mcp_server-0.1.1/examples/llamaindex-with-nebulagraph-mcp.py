import asyncio
import os

from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent, ReActChatFormatter
from llama_index.core.agent.react.prompts import REACT_CHAT_SYSTEM_HEADER
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai_like import OpenAILike
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

load_dotenv()


# MCP Server Connection Parameters
MCP_HOST = os.getenv("MCP_HOST")
MCP_PORT = os.getenv("MCP_PORT")

SYSTEM_PROMPT = """\
You are an agricultural research assistant.\

We have a NebulaGraph database with a knowledge graph of people relationships.

Please use tools to answer the question:

- You can list all spaces with `list_spaces` tool, and get schema from space with `get_space_schema` tool.
- You can choose to query NebulaGraph directly with `execute_query` tool and nGQL/OpenCypher.
- Or, you can get information from NebulaGraph with `find_path` and `find_neighbors` tools.
"""


async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    agent = ReActAgent.from_tools(
        llm=OpenAILike(
            model=os.getenv("OPENAI_MODEL"),
            api_base=os.getenv("OPENAI_ENDPOINT"),
            api_key=os.getenv("OPENAI_API_KEY"),
            is_chat_model=True,
        ),
        tools=list(tools),
        react_chat_formatter=ReActChatFormatter(
            system_header=SYSTEM_PROMPT + "\n" + REACT_CHAT_SYSTEM_HEADER,
        ),
        max_iterations=20,
        verbose=True,
    )
    return agent


async def handle_user_message(message_content: str, agent: ReActAgent):
    user_message = ChatMessage.from_str(role="user", content=message_content)
    response = await agent.achat(message=user_message.content)
    print(response.response)


async def main():
    mcp_tool = McpToolSpec(client=BasicMCPClient(f"http://{MCP_HOST}:{MCP_PORT}/sse"))

    agent = await get_agent(mcp_tool)
    try:
        await handle_user_message(
            "Find the shortest path between 'person1' and 'person5'.", agent
        )
    except Exception as e:
        print(f"Unexpected error: {type(e)}, {e}")


if __name__ == "__main__":
    asyncio.run(main())
