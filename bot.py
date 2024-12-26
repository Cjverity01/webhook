import discord
from discord.ext import tasks
from multiprocessing import Queue
from sanic_server import get_application_queue
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord Bot Settings
DISCORD_BOT_TOKEN = os.getenv(TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Queue to receive applications from the Sanic server
application_queue = get_application_queue()

# Initialize Discord bot
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

# Function to Process Application Queue
async def process_applications():
    await bot.wait_until_ready()
    channel = bot.get_channel(DISCORD_CHANNEL_ID)

    while True:
        if not application_queue.empty():
            application = application_queue.get()

            # Create an embed for the application
            embed = discord.Embed(
                title="New Application Received",
                color=discord.Color.blue()
            )
            embed.add_field(name="Applicant", value=application["name"], inline=False)
            embed.add_field(name="Application", value=application["details"], inline=False)
            embed.add_field(name="Submitted At", value=application["timestamp"], inline=False)
            embed.set_footer(text="Review this application below:")

            # Create buttons for Accept/Deny
            view = ApplicationButtons(application["name"])
            await channel.send(embed=embed, view=view)

        await asyncio.sleep(1)  # Check the queue every second

# Button Response Functionality
class ApplicationButtons(discord.ui.View):
    def __init__(self, applicant_name):
        super().__init__()
        self.applicant_name = applicant_name

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {self.applicant_name}! Your application has been accepted! Please join https://discord.gg/7hqZmHSjKd.")
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {self.applicant_name}! You will not be able to apply again this wave. Try again next time!")
        self.stop()

# Run the Discord Bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(process_applications())
    bot.run(DISCORD_BOT_TOKEN)
