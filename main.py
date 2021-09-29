import os
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import ffmpeg
import random
import datetime

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'worstaudio/worst',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        try:
            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]
        except:
            pass
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data),filename

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  

rd=[] #request_data
@client.event
async def on_message(message: discord.Message):
    # メッセージの送信者がbotだった場合は無視する
    if message.author.bot:
        return

    if message.content == (".music"):
        await message.delete()
        print('music')
        text = '`.p <検索キーワード>`: 音楽再生\n`.n`: 次の曲\n`.loop`: ループon/off\n`.q`: キュー表示\n`.dis`: bot切断'
        msg = discord.Embed(title='音楽機能',description=text,color=0x0caee4)
        await message.channel.send(embed=msg)

    if message.content.startswith(".p"):
        
        if message.author.voice is None:
            return

        # ボイスチャンネルに接続する
        if message.guild.voice_client is None:
            await message.author.voice.channel.connect()
            
        url = message.content[3:]
        await message.delete()
        if url!='':
            await(await message.channel.send('Loading...')).delete(delay=3)
            files = os.listdir()
            if len(files)>1000:
                for f in files:
                    if 'youtube' in f:
                        os.remove(f)
            # youtubeから音楽をダウンロードする
            player,filename = await YTDLSource.from_url(url, loop=client.loop)
            print(player.title)
            # 再生する

            try:
                with open('userdata.txt', mode='a', encoding='shift_jis') as f:
                    text = f'{datetime.datetime.now()} | {player.title} | {message.guild.name}\n'
                    f.write(text)
            except:
                pass

            def play_next(filename):
                #通話に誰もいなかったらストップ
                try:
                    if len(message.guild.voice_client.channel.members)==1:
                        message.guild.voice_client.stop()
                        return
                except:
                    pass

                ok=0
                n=0
                for d in rd:
                    if d[0] == message.guild.id:
                        ok=d[1]
                        break
                    else:
                        n+=1
                #loop onなら同じ曲
                if ok == 1:
                    try:
                        message.guild.voice_client.play(discord.FFmpegPCMAudio(filename),after=lambda e:play_next(filename))
                    except:
                        pass
                else:
                #loop offなら次の曲
                    if n<len(rd):
                        if len(rd[n])>2:
                            filename = d[2]
                            title = d[3]
                            rd[n].pop(2)
                            rd[n].pop(2)
                            try:
                                message.guild.voice_client.play(discord.FFmpegPCMAudio(filename),after=lambda e:play_next(filename))
                            except:
                                pass
                    #次の曲が無かったらストップ
                    else:
                        message.guild.voice_client.stop()
                        
            # 再生中の場合はキューに追加
            if message.guild.voice_client.is_playing():
                ok=0
                n=0
                for d in rd:
                    if d[0] == message.guild.id:
                        ok=1
                        break
                    else:
                        n+=1
                if ok==0:
                    rd.append([message.guild.id,0])
                rd[n].append(filename)
                rd[n].append(player.title)
                queue = ''
                for i in range((len(rd[n])-2)//2):
                    queue += f'{i+1}: {rd[n][3+2*i]}\n'
                text = discord.Embed(title='キューに追加しました' ,description=f'{player.title}\n--------------\n{queue}',color=0xa60ced)
                await(await message.channel.send(embed=text)).delete(delay=10)
                
            else:
                text = discord.Embed(title='再生中' ,description=f'{player.title}')
                await(await message.channel.send(embed=text)).delete(delay=10)
                #message.guild.voice_client.play(discord.FFmpegPCMAudio(filename))
                message.guild.voice_client.play(discord.FFmpegPCMAudio(filename),after=lambda e:play_next(filename))
    
    elif message.content == ".dis":
        await message.delete()
        if message.author.voice is None:
            return
        if message.guild.voice_client is None:
            return

        # 切断する
        await message.guild.voice_client.disconnect()
        await(await message.channel.send("切断しました。")).delete(delay=3)

    elif message.content == ".q" or message.content == ".queue":
        await message.delete()
        if message.author.voice is None:
            return
        if message.guild.voice_client is None:
            return

        ok=0
        n=0
        for d in rd:
            if d[0] == message.guild.id:
                ok=1
                break
            else:
                n+=1
        if ok==0:
            await(await message.channel.send('`全曲再生済み`')).delete(delay=10)
            return
        if len(rd[n])<3:
            await(await message.channel.send('`全曲再生済み`')).delete(delay=10)
            return

        queue = ''
        for i in range((len(d)-2)//2):
            queue += f'{i+1}: {rd[n][3+2*i]}\n'
        text = discord.Embed(title='キュー' ,description=f'{queue}',color=0xa60ced)
        await(await message.channel.send(embed=text)).delete(delay=10)
        

    elif message.content == ".loop":
        await message.delete()
        if message.author.voice is None:
            return
        if message.guild.voice_client is None:
            return
        ok=0
        n=0
        for d in rd:
            if d[0] == message.guild.id:
                ok=1
                break
            else:
                n+=1
        if ok==0:
            rd.append([message.guild.id,0])
            d=rd[len(rd)-1]

        ok=1-rd[n][1]
        rd[n][1]=ok
        if ok == 1:
            text = '`loop on`'
        else:
            text = '`loop off`'
        await(await message.channel.send(text)).delete(delay=5)

    elif message.content == ".n":
        await message.delete()
        if message.guild.voice_client is None:
            return

        # 再生中ではない場合は実行しない
        if not message.guild.voice_client.is_playing():
            return

        message.guild.voice_client.stop()
        await(await message.channel.send("スキップしました。")).delete(delay=3)

token = os.environ['DISCORD_BOT_TOKEN']
client.run(token)
