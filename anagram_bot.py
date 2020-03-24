#!/home/kev/dispy/venv/bin/python
import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
from anagram import anagram
import connector
import math
conn = connector.create_connection("/home/kev/dispy/scores.db")

f = open("/home/kev/dispy/words.txt","r")
py_list = f.readlines()
new_list = []
for word in py_list:
    if len(word) > 5:
        new_list.append(word)
random.shuffle(new_list)
py_act = cycle(new_list)

current_word = ""
description = '''
An Anagram bot that tracks your scores.

Use ?guess {your guess} to guess the anagram in the status
'''
bot = commands.Bot(command_prefix='?', description=description)
"""
async def change_word():
    global current_word
    r = requests.get('https://random-word-api.herokuapp.com/word?number=10')
    words = r.json()
    current_word = words[0]
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=anagram(words[0])))
"""


async def change_word():
    global current_word
    current_word = next(py_act).replace("\n", "")
    print(current_word)
    anag = anagram(current_word)
    anag = anag.replace("\n","")
    print(anag)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=anag))


@tasks.loop(minutes=5)
async def change_loop():
    global current_word
    await change_word()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Learning Python"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    change_loop.start()

@bot.command()
async def score(ctx):
    global current_word
    author = str(ctx.author)
    score = connector.get_score(conn,author)
    await ctx.send(score)


@bot.command()
async def guess(ctx,args):
    global current_word
    old = current_word
    print(ctx.author)
    if current_word.upper() == str(args).upper():
        score = connector.update_score(conn,str(ctx.author))
        await change_word()
        await ctx.send('Well Done You Guessed it!\nIt was '+old+'\nNew Score:'+str(score))
    else:
        await ctx.send('Good Guess but wrong')

@bot.command()
async def change(ctx):
    global current_word
    temp = current_word
    await ctx.send('Aww you give up\nThe word was '+temp)
    await change_word()

@bot.command()
async def rank(ctx):
    scores = connector.get_scores(conn)
    sstr = ""
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
    for index,scored in enumerate(scores,start=1):
        sstr = sstr + ordinal(index)+" : "+scored[1] + " : "+str(scored[2])+"\n"
    await ctx.send(sstr)

bot.run('addyourbottokenhere')

