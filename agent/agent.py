import os
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, noise_cancellation

# Load environment variables from .env file
load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:  # ✅ fixed __init__
        super().__init__(instructions="You are a helpful voice AI assistant for ConversX.")


async def entrypoint(ctx: agents.JobContext):
    # ✅ load credentials from .env
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_project_id = os.getenv("OPENAI_PROJECT_ID")

    # ✅ initialize session with credentials
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            
            voice="coral",
            api_key=openai_api_key,
            base_url=f"https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview&project={openai_project_id}"

    )
)


    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
