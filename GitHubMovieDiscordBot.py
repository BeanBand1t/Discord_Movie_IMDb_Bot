import discord
from discord.ext import commands
from discord import app_commands
import requests

#This Discord Bot was made by BeanBand1t 
#For more random Bs visit https://github.com/BeanBand1t
TOKEN = "Your_Bot_Token"

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        try:
            guild = discord.Object(id="Your_Guild_Id remove_qoutes")
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')


    async def on_message(self, message):
        if message.author == self.user:
            return
        
        
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id="Your_Guild_Id remove_qoutes")

class MyView(discord.ui.View):
    def __init__(self, url):
        super().__init__()
        # Add a link button that opens the URL
        self.add_item(
            discord.ui.Button(label="View on IMDb", style=discord.ButtonStyle.blurple, url=url)
        )

@client.tree.command(name="showinfo", description="info from OMDb", guild=GUILD_ID)
@app_commands.describe(query = "Show Title")
async def movieInfo(interaction: discord.interactions, query: str):
    await interaction.response.defer()
    
    #https://www.omdbapi.com/
    appId = "Your_API_Key" 

    try:
        url = f'https://www.omdbapi.com/?t={query}&apikey={appId}'
        response = requests.get(url)
        data = response.json()
        print(data)

        if data.get("Response") == "False":
            await interaction.followup.send(f'Movie not found: {query}')
            return
        
        name = data["Title"]
        year = data["Year"]
        rating = data["imdbRating"]
        plot = data["Plot"]
        poster = data.get("Poster", "")
        imdbID = data["imdbID"]

        imdbUrl = f'https://www.imdb.com/title/{imdbID}'

        embed = discord.Embed(
            title=f'{name}, ({year})',
            description=plot,
            color=discord.Color.red()
        )
        embed.add_field(name="IMDb Rating", value=rating, inline=True)
        if poster and poster != "N/A":
            embed.set_thumbnail(url=poster)

        view = MyView(imdbUrl)

        await interaction.followup.send(embed=embed, view=view)

    except Exception as e:
        await interaction.followup.send(f'Error fetching movie: {e}')

client.run(TOKEN)