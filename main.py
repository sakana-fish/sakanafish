import discord
import datetime
import os

#list = []
#apre = 'おさかなのサーバー'

from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  

@client.command()
async def cal(ctx2):
  i = 0
  a1 = 0
  a2 = 0
  b1 = 0
  b2 = 0
  c1 = ""
  c2 = str(a2)+" - "+str(b2)
  cal = discord.Embed(title="🐟即時集計🐟",color=0xe74c3c,description="{} @{}\n{}".format(c2,12-i,c1))
  result = await ctx2.send(embed=cal)
  await ctx2.send("結果を入力してください")

  for k in range(12):
    i += 1
    check = 0
    while check == 0:
      rank = await client.wait_for('message')
      rank = rank.content
      await ctx2.channel.purge(limit=1)
      
      #print(rank)
      if len(rank) == 6:        
        check = 1
        #print("OK")
      else:
        await ctx2.send("try again")
    
    ranklist = ''
    a1 = 0
    for j in range(6):
      ranklist += str(int(rank[j],16))+" "
      point = int(rank[j],16)
      if point == 1:
        point = 15
      elif point == 2:
        point = 12
      else:
        point = 13-point
      a1 += point
      #print(a1)

    b1 = 82-a1
    a2 += a1
    b2 += b1
    c1 += "race"+str(i)+"\t"+str(a1)+" - "+str(b1)+"\t点差 "+str(a1-b1)+"\t順位 "+ranklist+"\n"
    c2 = str(a2)+" - "+str(b2)+"\t点差 "+str(a2-b2)
    cal = discord.Embed(title="🐟即時集計🐟",color=0xe74c3c,description="{} @{}\n順位 {}\n--------------------------\n{}".format(c2,12-i,ranklist,c1))
    await result.edit(embed=cal)
    #print(a1,a2,b1,b2,c1,c2)    
    
@client.command()
async def s(ctx, about = "交流戦募集 {}".format(datetime.date.today()), cnt = 6, settime = 43200):
    cnt, settime = int(cnt), float(settime)
    #a = ctx.channel.name
    #print(a)
    #list.append(0)
    #b = len(list)
    #print(b)
  
    list1 = [">"]
    list2 = [">"]
    list3 = [">"]
    list4 = [">"]
    mem1 = []
    mem2 = []
    mem3 = []
    mem4 = []
    cnt2 = 6
    cnt3 = 6
    cnt4 = 6
    check1 = 0
    check2 = 0
    check3 = 0
    check4 = 0

    test = discord.Embed(title=about,colour=0x1e90ff)
    #test.add_field(name=f"交流戦\n", value=None, inline=True)
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"21@{cnt} ", value=' '.join(list1), inline=True)
    test.add_field(name=f"22@{cnt2} ", value=' '.join(list2), inline=True)
    test.add_field(name=f"23@{cnt3} ", value=' '.join(list3), inline=True)
    test.add_field(name=f"24@{cnt4} ", value=' '.join(list4), inline=True)
    msg = await ctx.send(embed=test)
    a = ctx.message.id
    print(a)
    a = ctx.message.content
    print(a)
    #投票の欄

    await msg.add_reaction('🇦')
    await msg.add_reaction('🇧')
    await msg.add_reaction('🇨')
    await msg.add_reaction('🇩')
    await msg.add_reaction('✖')
    #print(msg.id)

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji

    while len(list1)-1 <= 10:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            #await ctx.send('残念、人が足りなかったようだ...')
            break
        else:
            #if len(list) != b:
            #  break
            #else:
            if msg.id == reaction.message.id:
                print(str(reaction.emoji))
                print(reaction.message.id)
                print(reaction.message.content)
                if str(reaction.emoji) == '🇦':
                    list1.append(user.name)
                    mem1.append(user.mention)
                    cnt -= 1
                    #test = discord.Embed(title=about,colour=0x1e90ff)
                    #test.add_field(name=f"21@{cnt} ", value=' '.join(list1), inline=True)
                    #test.add_field(name=f"22@{cnt2} ", value=' '.join(list2), inline=True)
                    #await msg.edit(embed=test)
                    if cnt == 0:
                      if check1 == 0:
                        member1 = ' '.join(mem1)
                        await ctx.send("21〆 {}".format(member1))
                        check1 +=1
                    """if cnt == 0:
                        test = discord.Embed(title=about,colour=0x1e90ff)
                        test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(list1), inline=True)
                        await msg.edit(embed=test)
                        finish = discord.Embed(title=about,colour=0x1e90ff)
                        finish.add_field(name="おっと、メンバーがきまったようだ",value='\n'.join(list1), inline=True)
                        await ctx.send(embed=finish)
                    """    
                if str(reaction.emoji) == '🇧':
                    list2.append(user.name)
                    mem2.append(user.mention)
                    cnt2 -= 1
                    if cnt2 == 0:
                      if check2 == 0:
                        member2 = ' '.join(mem2)
                        await ctx.send("22〆 {}".format(member2))
                        check2 +=1

                if str(reaction.emoji) == '🇨':
                    list3.append(user.name)
                    mem3.append(user.mention)
                    cnt3 -= 1
                    if cnt3 == 0:
                      if check3 == 0:
                        member3 = ' '.join(mem3)
                        await ctx.send("23〆 {}".format(member3))
                        check3 +=1

                if str(reaction.emoji) == '🇩':
                    list4.append(user.name)
                    mem4.append(user.mention)
                    cnt4 -= 1
                    if cnt4 == 0:
                      if check4 == 0:
                        member4 = ' '.join(mem4)
                        await ctx.send("24〆 {}".format(member4))
                        check4 +=1
      
                elif str(reaction.emoji) == '✖':
                    if user.name in list1:
                        list1.remove(user.name)
                        mem1.remove(user.mention)
                        cnt += 1
                        #test = discord.Embed(title=about,colour=0x1e90ff)
                        #test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(list1), inline=True)
                        #await msg.edit(embed=test)
                    if user.name in list2:
                        list2.remove(user.name)
                        mem2.remove(user.mention)
                        cnt2 += 1
                    if user.name in list3:
                        list3.remove(user.name)
                        mem3.remove(user.mention)
                        cnt3 += 1
                    if user.name in list4:
                        list4.remove(user.name)
                        mem4.remove(user.mention)
                        cnt4 += 1        
                    else:
                        pass

        test = discord.Embed(title=about,colour=0x1e90ff)
        test.add_field(name=f"21@{cnt} ", value=' '.join(list1), inline=True)
        test.add_field(name=f"22@{cnt2} ", value=' '.join(list2), inline=True)
        test.add_field(name=f"23@{cnt3} ", value=' '.join(list3), inline=True)
        test.add_field(name=f"24@{cnt4} ", value=' '.join(list4), inline=True)
        await msg.edit(embed=test)
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)

  

token = os.environ['DISCORD_BOT_TOKEN']
client.run('token')
