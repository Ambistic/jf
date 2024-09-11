import discord
import asyncio
import os

class DiscordBot:
    def __init__(self, message, token=None, user_id=None):
        if token:
            self.token = token
        else:
            self.token = os.environ["DISCORD_TOKEN"]
        if user_id:
            self.user_id = user_id
        else:
            self.user_id = os.environ["DISCORD_USER_ID"]
        self.message = message
        
        intents = discord.Intents.default()
        intents.messages = True
        
        self.client = discord.Client(intents=intents)

        # Bind the event handlers to the bot client
        self.client.event(self.on_ready)

    async def send_private_message(self, message):
        """Sends a private message (DM) to the specified user."""
        await self.client.wait_until_ready()
        user = await self.client.fetch_user(self.user_id)  # Fetch the user object
        if user:
            await user.send(message)
        else:
            print(f"User with ID {self.user_id} not found.")

    async def on_ready(self):
        print(f'{self.client.user} has connected to Discord!')
        
        # Send private message when the bot is ready
        await self.send_private_message(self.message)

        # Optionally close the bot after sending the message
        await self.client.close()
        pass

    def run(self):
        """Starts the bot and runs the event loop."""
        self.client.run(self.token)
        
        
def send_discord_msg(msg):
    # Initialize the bot with the token, channel ID, user ID, and message
    bot = DiscordBot(msg)
    
    # Run the bot
    bot.run()


if __name__ == "__main__":
    send_discord_msg("Hello World")
