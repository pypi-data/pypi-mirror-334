import csp
from csp import ts

from csp_adapter_discord import DiscordAdapterConfig, DiscordAdapterManager, DiscordMessage

config = DiscordAdapterConfig(
    token=".token",  # Your Discord bot token or file containing the token
)


@csp.node
def add_reaction_when_mentioned(msg: ts[DiscordMessage]) -> ts[DiscordMessage]:
    """Add a reaction to every message that starts with hello."""
    if msg.msg.lower().startswith("hello"):
        return DiscordMessage(
            channel=msg.channel,
            thread=msg.thread,
            reaction="👋",
        )


def graph():
    # Create a DiscordAdapter object
    adapter = DiscordAdapterManager(config)

    # Subscribe and unroll the messages
    msgs = csp.unroll(adapter.subscribe())

    # Print it out locally for debugging
    csp.print("msgs", msgs)

    # Add the reaction node
    reactions = add_reaction_when_mentioned(msgs)

    # Print it out locally for debugging
    csp.print("reactions", reactions)

    # Publish the reactions
    adapter.publish(reactions)


if __name__ == "__main__":
    csp.run(graph, realtime=True)
