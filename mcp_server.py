import contextlib
import datetime

import uvicorn
from mcp.server.fastmcp import FastMCP
from sqlite_utils import Database
from fastapi import FastAPI

mcp = FastMCP("Message Board", stateless_http=True)
db = Database("message_board.db")
messages = db["messages"]


@mcp.tool()
async def leave_message(message: str) -> bool:
    """Leaves a message on the message board.
    """
    messages.insert({
        "message": message,
        "time": datetime.datetime.now().isoformat(),
    }, pk="id")  # This will create an auto-incrementing integer primary key
    return True


@mcp.tool()
async def last_messages() -> list[dict]:
    """Gets the last 5 messages that have been left on the message board.

    Most recent messages are returned first
    """
    recent_messages = messages.rows_where(
        order_by="id desc",
        limit=5
    )

    return [recent_message["message"] for recent_message in recent_messages]


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/message_board", mcp.streamable_http_app())


@app.get("/up")
def up():
    return {"message": "Hello world"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8222)
