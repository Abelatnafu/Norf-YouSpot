import discord
from discord.ext import commands
import os
import shutil
from dotenv import load_dotenv
import mp3 as m3

load_dotenv()

client = discord.Client()
client = commands.Bot(command_prefix="+")
client.remove_command("help")

@client.event
async def on_ready():
    print("Im on.")

# Function that downloads a song from youtube and stores it in my spotify local files path
@client.command(pass_context=True, aliases=["downyou", "youtube", "spotify", "download"])
async def youspot(ctx, url: str):
    # delete already existing .mp3 files in the main directory
    directory = "."
    m3.clean_all_mp3(directory)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # download data and extract information about the video
    infor = m3.download_mp3(ydl_opts, url)

    # rename the existing dowloaded .mp3 file into the current dowloaded file
    m3.rename_mp3(directory, infor)

    # Try sending file to the discord chat if less that 8MB(Discord size limit)


    # source path
    source = f"{directory}/{infor['title']}.mp3"
    #  destination path
    destination = [f"{directory}/musics",
                   f"/Users/abelatnafu/Desktop/spotify"]
    # copy all songs to one folder named music to store them
    shutil.copy(source, destination[0])
    print("Music copied to storage.")
    # move all the songs to my spotify local path
    shutil.move(source, destination[1])
    print("Muisc moved to spotify local path.")
    try:

        await ctx.send(file=discord.File(f"{destination[0]}/{infor['title']}.mp3"))
    except discord.errors.HTTPException:
        embedding = discord.Embed(color=0x7289da, title="Invalid file size")
        embedding.add_field(name="File size limit: 8MB", value="", inline=False)
        await ctx.send(embed=embedding)


@client.command()
async def help(ctx):
    embedding = discord.Embed(color=0xe74c3c, title="Nner")
    # image_addy = "https://www.iconsdb.com/icons/preview/red/wolfram-alpha-xxl.png"
    embedding.set_footer(text="© 2021 Norf INC")
    # embedding.set_image(url=image_addy)
    embedding.add_field(name="+youspot 'youtube song link to download'",
                        value="To download a youtube song into your spotify local file path", inline=False)
    # embedding.set_thumbnail(url=image_addy)
    await ctx.send(embed=embedding)

# Bot API Key
client.run(os.environ.get('BOT_ID'))
