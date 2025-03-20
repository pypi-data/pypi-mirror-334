import discord
from discord import app_commands
from typing import Callable, List, Tuple

# Global variables for server ID and token
server_id_client = None
token_client = None
commands_list = []  # Stores (name, description, response, options)

__all__ = ["preset_bot", "send_message", "add_command", "run_client", "testAppPrints"]

# Set bot credentials
def preset_bot(server_id: int, token: str):
    global server_id_client, token_client
    server_id_client = server_id
    token_client = token


# Send plain text as a response
async def send_message(interaction: discord.Interaction, text: str, ephemeral: bool = False):
    await interaction.response.send_message(content=text, ephemeral=ephemeral)


# Add a new command with optional parameters
def add_command(
    name: str,
    description: str,
    response: Callable[[discord.Interaction, str], None],  # <-- Explicit parameter
    options: List[Tuple[str, str, type]] = [],
):
    commands_list.append((name, description, response, options))


# Print stored server ID and token for debugging
def testAppPrints():
    if server_id_client and token_client:
        print(f"Server ID: {server_id_client}")
        print(f"Token: {token_client}")
    else:
        print("Server ID and Token are not defined. Use preset_bot to set them.")


def run_client():
    if not server_id_client or not token_client:
        raise ValueError("Server ID and Token must be set using preset_bot before running the client.")

    class AClient(discord.Client):
        def __init__(self):
            super().__init__(intents=discord.Intents.default())
            self.synced = False
            self.tree = app_commands.CommandTree(self)

        async def setup_hook(self):
            for name, description, response, options in commands_list:
                if options:
                    param_name, param_desc, param_type = options[0]

                    # Define a command function with explicit parameters
                    async def command_func(interaction: discord.Interaction, param: str):
                        await response(interaction, param)

                    # Register command with explicit parameter
                    cmd = app_commands.Command(
                        name=name,
                        description=description,
                        callback=command_func
                    )
                    self.tree.add_command(cmd, guild=discord.Object(id=server_id_client))
                else:
                    async def command_func(interaction: discord.Interaction):
                        await response(interaction, "")

                    # Register command with NO parameters
                    cmd = app_commands.Command(
                        name=name,
                        description=description,
                        callback=command_func
                    )
                    self.tree.add_command(cmd, guild=discord.Object(id=server_id_client))

            if not self.synced:
                await self.tree.sync(guild=discord.Object(id=server_id_client))
                self.synced = True

    client = AClient()

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}.")

    try:
        client.run(token_client)
    except discord.LoginFailure:
        print("Invalid token. Check your bot token and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
