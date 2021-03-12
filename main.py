import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix='g!', intents=intents)

@client.event
async def on_ready():
	print("hello world!")


with open("tokenfile", "r") as tokenfile:
        token=tokenfile.read()

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency*1000)} ms')

@client.event
async def on_member_join(member):
	welcome = discord.utils.get(member.guild.channels, id=766848918499360809)

	await welcome.send(f"{member.mention} has joined the server\n\nwe now have {len(member.guild.members)} members")

@client.event
async def on_member_remove(member):
        welcome = discord.utils.get(member.guild.channels, id=766848918499360809)

        await welcome.send(f"{member.mention} has left the server\n\nwe now have {len(member.guild.members)} members")

pog = ["pog","poj","poog","pooog","pooj","poooj", "po𝑔"]

@client.event
async def on_message(message):
	for x in pog:
		if x in message.content:
			try:
				await message.guild.kick(message.author, reason="said p*g")
				print(f"{message.author} said p*g")
			except discord.errors.Forbidden:
				print(f"{message.author} said p*g but i cant kick them")
			break

client.run(token)
