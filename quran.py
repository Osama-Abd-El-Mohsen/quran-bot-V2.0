from nextcord import Interaction, SlashOption,FFmpegPCMAudio
from nextcord.ext import commands, tasks
from itertools import cycle
import nextcord
import pyquran as q
import datetime
import asyncio
from Database import QB_DataBase,audio,verse2,aya_Num

intents = nextcord.Intents.default()
intents.message_content = True
intents.members=True


guild = [972498788235223040]
token = 'OTcyNDk4NjQ1NjE2Mjk1OTY2.GmvcEc.Fp-DKrSxFmiifFmL0lJuktefbExvwow_SktxK4'
statu = cycle(["/help", "Quran 🌜"])
bot = commands.Bot(command_prefix='/',status=nextcord.Status.idle, help_command=None,intents=intents)
so = 0
global st, wait_time
wait_time = 0


@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=next(statu)))




@bot.event
async def on_ready():
    change_status.start()
    print(f"Quran Bot Connected 🌜")
    
    
@bot.slash_command(name="leave", description="يتم استخدام هذا الامر لخروج البوت من ال voice channel", guild_ids=guild)
async def leave(ctx: Interaction):
    if ctx.user.id != 716301044514029619:
        embed2 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed2.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed2.add_field(name="\u200b ❓",value=f"ليس لديك الاذن لاستخدام هذا الامر `/stop`", inline=True)
        await ctx.send(embed=embed2)

    else :
        channel = bot.get_channel(1050770039181156422)
        await channel.guild.voice_client.disconnect()
        await ctx.send("Bot Left voice channel 🤖") 


@bot.slash_command(name="play", description="يتم استخدام هذا الامر لتشغيل التلاوه فى ال voice channel", guild_ids=guild)
async def play(ctx: Interaction, start_from: int = SlashOption(description="ادخل رقم السوره من 1 <= 114", min_value=1, max_value=114)):
    if ctx.user.id != 716301044514029619:
        embed2 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed2.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed2.add_field(name="\u200b ❓",value=f"ليس لديك الاذن لاستخدام هذا الامر `/stop`", inline=True)
        await ctx.send(embed=embed2)
        
    else:
        await ctx.response.defer()
        channel2 = bot.get_channel(1049085171254689823)
        sura_Name = q.quran.get_sura_name(start_from)
        await ctx.send("Bot joined voice channel 🤖") 

        x=(start_from-1)
        channel = bot.get_channel(1050770039181156422)
        voice = await channel.connect()
        play= FFmpegPCMAudio(f"https://server8.mp3quran.net/afs/{audio[x]}.mp3",options = "-loglevel panic")
        voice.play(play)
        voice = nextcord.utils.get(bot.voice_clients,guild=channel.guild)
        message = await channel2.send("Playing...Rn") 
        await channel.send(f" 🌛  تتم تلاوه سوره ( **{sura_Name}** ) الان ")
        while 1 :
            
            if  voice.is_playing():
                await message.add_reaction("🌜")

            else :
                try :
                    await ctx.response.defer()
                    y=1
                except : 
                    y=0
                await message.add_reaction("🌛")
                x=x+1
                if x == 114 :
                    x=0
                y =x+1
                play= FFmpegPCMAudio(f"https://server8.mp3quran.net/afs/{audio[x]}.mp3",options = "-loglevel panic")
                sura_Name = q.quran.get_sura_name(y)
                voice.play(play)
                await channel.send(f" 🌛  تتم تلاوه سوره ( **{sura_Name}** ) الان ")




        
@bot.slash_command(name="help", description="يمكن استخدام هذا الامر لمعرفه اوامر البوت", guild_ids=guild)
async def help(ctx: Interaction):
    
    embed = nextcord.Embed(
        title="قائمه المساعده ❓",
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
    )
    
    url = ctx.user.avatar
    if url == None:
        url = "https://velog.velcdn.com/cloudflare/amelieluke/0c7c0d87-7903-4ae5-b33e-e73b650439fd/Discord%20Brand.jpg"
    else:
        url = url
    embed.set_footer(
        text=f"Requested by - {ctx.user}", icon_url=url)
    embed.add_field(name="أوامر خاصه بالأدمن 👑",value="""`/start` , `/stop` , `/play` , `/leave` """, inline=True)
    embed.add_field(name="أوامر عامه ⚙️",value="`/get_sura_name` , `/get_sura_num`,`/get_verse`\n", inline=True)

    embed.add_field(name="طريقه إستخدام هذه الأوامر ⬇️", value="`/get_sura_name` , `/get_sura_num`,`/get_verse`",inline=False)

    embed.add_field(name="`/get_sura_name`",value="""```ادخل رقم السوره التى تريد ان تعرف اسمها ``` ```fix
Ex :
/get_sura_name 11   (النتيجه : هود)
``` """, inline=True)

    embed.add_field(name="`/get_sura_num`", value="""```ادخل رقم السوره التى تريد معرفه رقمها ``` ```fix
Ex :
/get_sura_num هود   
(النتيجه : 11)``` """, inline=True)

    embed.add_field(name="`/get_verse`",value="""```ادخل رقم السوره ورقم الايه التى تريدها ``` ```fix
Ex :
/get_verse 2 1 (النتيجه : الم) 
``` """, inline=True)



    embed.add_field(name="للدعم والاقتراحات 👨🏼‍💻",value="[```By : Osama Abd El Mohsen  اضغط هنا```](https://discordapp.com/users/716301044514029619)", inline=True)

    embed.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")


    await ctx.send(embed=embed)


@bot.slash_command(name="stop", description="Use it to stop delay loop only owner 👑 allowed to use this command )", guild_ids=guild)
async def restart(ctx: Interaction):
    global so

    if ctx.user.id != 716301044514029619:
        embed2 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed2.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed2.add_field(name="\u200b ❓",value=f"ليس لديك الاذن لاستخدام هذا الامر `/stop`", inline=True)
        await ctx.send(embed=embed2)
    else:
        global st
        st = False
        if so != 0:

            embed2 = nextcord.Embed(
            colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
            )
            embed2.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
            embed2.add_field(name=" Delay Status ❓",value=f"```Delay stopped```", inline=True)
            await ctx.send(embed=embed2)
            so = 0
        else:

            embed2 = nextcord.Embed(
            colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
            )
            embed2.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
            embed2.add_field(name=" Delay Status ❓",value=f"```No delay found```", inline=True)
            await ctx.send(embed=embed2)


@bot.slash_command(name="start", description="Use it to start delay loop only owner 👑 allowed to use this command )", guild_ids=guild)
async def sendMessage(ctx: Interaction, sura_num: int = SlashOption(description="ادخل رقم السوره من 1 <= 114", min_value=1, max_value=114), verse_num: int = SlashOption(description="ادخل رقم الايه", min_value=1, max_value=286), loop_time: float = SlashOption(description="ادخل الوقت المطلوب")):
    global st, so
    if ctx.user.id != 716301044514029619:
        embed2 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed2.add_field(name="\u200b ❓",value=f"ليس لديك الاذن لاستخدام هذا الامر `/start`", inline=True)
        await ctx.send(embed=embed2)
    
    else:
        sura_Name = q.quran.get_sura_name(sura_num)
        verse = QB_DataBase[sura_num-1][verse_num-2]
        if loop_time != 0 and verse_num-1 != 0 :
            embed2 = nextcord.Embed(
            colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
            )
            embed2.add_field(name="Delay Time 💤 :",value=f"""```md
[{loop_time}][دقيقه]
```""", inline=False)
            embed2.add_field(name="سيبدأ البوت بسوره ⬇️",value=f"""```ini
[{sura_Name}]
```""", inline=False)

            embed2.add_field(name="بعد هذه الايه ⬇️",value=f"\u200b", inline=False)
            embed2.set_image(url=f"{verse}")

            await ctx.send(embed=embed2)
        

        else:
            sura_Name = q.quran.get_sura_name(sura_num)
            embed2 = nextcord.Embed(
            colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
            )
            embed2.add_field(name="Delay Time 💤 :",value=f"""```md
[{loop_time}][دقيقه]
```""", inline=False)
            embed2.add_field(name="سيبدأ البوت بسوره ⬇️",value=f"""```ini
[{sura_Name}]
```""", inline=False)

            await ctx.send(embed=embed2)
        st = True
        

        while st:
            #111 #1
            if verse_num in range(len(QB_DataBase[sura_num-1])+1) :
                verse =QB_DataBase[sura_num-1][verse_num-1]

                suranum=sura_num-1
                versenum=verse_num
                if suranum == 1 :
                    res = 7
                elif suranum == 0 :
                    res = 0
                else :
                    res=0
                    for y in range(suranum):
                        x=aya_Num[y]
                        res=x+res

                verse_text=verse2[(versenum)+(res-1)]

                embed1 = nextcord.Embed(
                colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
                )
                now = datetime.datetime.now()
                then = now + datetime.timedelta(minutes=loop_time)
                global wait_time
                wait_time = (then-now).total_seconds()
                await asyncio.sleep(wait_time)
                embed1.add_field(name="\u200b",value=f"{verse_text}", inline=True)
                embed1.set_image(url=f"{verse}")
                await ctx.channel.send(embed=embed1)
                verse_num=verse_num+1

            else :
                sura_num=sura_num+1
                if sura_num == 115 :
                    sura_num = 1
                verse_num=1
            so =1


@bot.slash_command(name="get_verse", description="استخدم هذا الامر لايجاد ايه بإستخدام رقم السوره ورقم الايه ", guild_ids=guild)
async def sendMessage(ctx: Interaction, sura_number: int = SlashOption(description="ادخل رقم السوره من  1 <= 114", min_value=1, max_value=114), *, verse_number: int = SlashOption(description="ادخل رقم الايه", min_value=1, max_value=286)):
    user = q.quran.get_sura(sura_number)
    if 1 <= sura_number <= 114 and 0 < verse_number < len(user)+1:
        verse =QB_DataBase[sura_number-1][verse_number-1]
        embed1 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed1.set_image(url=f"{verse}")
        await ctx.send(embed=embed1)


    else:
        embed1 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed1.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed1.add_field(name="خطأ ❌",value=f"""```diff
تأكد من رقم الايه
```""", inline=True)
        await ctx.send(embed=embed1)


@bot.slash_command(name="get_sura_num", description="استخدم هذا الامر لايجاد رقم سوره بإستخدام اسم السوره", guild_ids=guild)
async def sendMessage(ctx: Interaction, sura_name: str = SlashOption(description="ادخل اسم السوره",)):
    sura_num = q.quran.get_sura_number(sura_name)
    if sura_num == None:
        embed1 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed1.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed1.add_field(name="خطأ ❌",value=f"""```diff
تأكد من رقم السوره
```""", inline=True)

        await ctx.send(embed=embed1)

    else:
        embed1 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed1.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed1.add_field(name="رقم السوره ⬇️",value=f"""```ini
[ {sura_num} ]
```""", inline=True)
        await ctx.send(embed=embed1)

@bot.slash_command(name='get_sura_name', description="استخدم هذا الامر لايجاد اسم السوره من خلال رقمها", guild_ids=guild)
async def sendMessage(ctx: Interaction, sura_number: int = SlashOption(description="ادخل رقم السوره من 1 <= 114", min_value=1, max_value=114)):
    if 1 <= sura_number <= 114:
        sura_Name = q.quran.get_sura_name(sura_number)
        embed1 = nextcord.Embed(
        colour=nextcord.colour.Color.from_rgb(r=82,g=117,b=185)
        )
        embed1.set_author(name="Quran Bot", url="https://discord.gg/vCzRrN9AHS",icon_url="https://i.postimg.cc/q7xRd1bC/quran-bot-01.jpg")
        embed1.add_field(name="اسم السوره ⬇",value=f"""```ini
[ {sura_Name} ]
```""", inline=True)

        await ctx.send(embed=embed1)

    else:
        pass


bot.run(token)