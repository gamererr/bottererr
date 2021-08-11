import discord
from discord.ext import commands
import json
import random
import sys
import traceback

intents = discord.Intents.all()
client = commands.Bot(command_prefix='g!', intents=intents)

@client.event
async def on_ready():
	print("hello world!")
	gamerzone = client.get_guild(766848554899079218)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with your mom"))

with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

# VVVVVV commands VVVVVV'

@client.command(aliases=['mc'])
async def membercount(ctx):
	await ctx.send(f"{len(ctx.guild.members)} members")

@client.command()
async def owo(ctx, *owo):
	owo = ' '.join(owo)
	if owo == '':
		await ctx.send('you need to give me something to owoify')
		return
	owo = owo.replace('rr','🇷')
	owo = owo.replace('RR','🇷 🇷')
	owo = owo.replace('r','w')
	owo = owo.replace('R','W')
	owo = owo.replace('🇷','rr')
	owo = owo.replace('🇷 🇷','RR')
	owo = owo.replace('ll','w')
	owo = owo.replace('LL','W')
	if random.randrange(0, 100) in range(50):
		owo += '~'
	await ctx.send(owo)

@client.command()
async def purge(ctx):
	if not await client.is_owner(ctx.author):
		embed = discord.Embed(title="you dont have permission to do this command", colour=discord.Colour.red(), description="become the owner of the bot nerd")
		await ctx.send(embed=embed)
		return

	async for x in ctx.channel.history():
		try:
			if x.id == ctx.message.reference.message_id:
				purge = x
		except AttributeError:
			embed = discord.Embed(title="you need to reply to a message", colour=discord.Colour.red())
			await ctx.send(embed=embed)
			return

	amount = 1
	async for x in ctx.channel.history(after=purge, before=ctx.message):
		amount += 1

	await ctx.channel.purge(after=purge, before=ctx.message)
	await purge.delete()
	embed = discord.Embed(title=f"{amount} messages purged", colour=discord.Colour.green())
	await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency*1000)} ms')

@client.command()
async def wii(ctx, *game):
	game = " ".join(game)
	gamererr = client.get_user(312292633978339329)
	await gamererr.send(f'wii game from **{ctx.author}** ```{game}```')
	print(f'wii game from {ctx.author}, {game}')
	await ctx.send(f'suggestion taken ```{game}```')

@client.command()
async def kick(ctx, user, *reason):

	reason = " ".join(reason)

	if reason == "":
		reason = "no reason given"

	if ctx.message.mentions != []:
		user = ctx.message.mentions
	else:
		user = client.get_user(int(user))
		if not user:
			await("you need to ping someone or give a user id")
			return

	if ctx.channel.permissions_for(ctx.author).kick_members:
		try:
			await user.send(f"kicked by {ctx.message.author} for `{reason}`")
			await ctx.guild.kick(user, reason=f"kicked by {ctx.message.author} for {reason}")
			await ctx.send(f"kicked {user.name} for `{reason}`")
		except discord.errors.HTTPException:
			await ctx.guild.kick(user, reason=f"kicked by {ctx.message.author} for {reason}")
			await ctx.send(f"kicked {user.name} for `{reason}`")
	else:
		embed = discord.Embed(title="you dont have permission to do this command", colour=discord.Colour.red(), description="become a mod nerd")

		await ctx.send(embed=embed)

@client.command()
async def ban(ctx, user, *reason):

	if reason == []:
		reason = "no reason"
	else:
		reason = " ".join(reason)

	if ctx.message.mentions != []:
		user = ctx.message.mentions
	else:
		user = client.get_user(int(user))
		if not user:
			await("you need to ping someone or give a user id")
			return

	if ctx.channel.permissions_for(ctx.author).ban_members:
		try:
			await user.send(f"banned by {ctx.message.author} for `{reason}`")
			await ctx.guild.ban(user, reason=f"banned by {ctx.message.author} for {reason}", delete_message_days=0)
			await ctx.send(f"banned {user.name} for `{reason}`")
		except discord.errors.HTTPException:
			await ctx.guild.ban(user, reason=f"banned by {ctx.message.author} for {reason}", delete_message_days=0)
			await ctx.send(f"banned {user.name} for `{reason}`")
	else:
		embed = discord.Embed(title="you dont have permission to do this command", colour=discord.Colour.red(), description="become a mod nerd")

		await ctx.send(embed=embed)

@client.command()
async def mute(ctx, user, *reason):

	if reason == []:
		reason = "no reason"
	else:
		reason = " ".join(reason)

	if ctx.message.mentions != []:
		user = ctx.message.mentions
	else:
		user = client.get_user(int(user))
		if not user:
			await("you need to ping someone or give a user id")
			return

	muted = client.get_role(774294917299830824)

	await user.send(f"you were **muted** for {reason}")
	await user.add_roles(muted)

@client.command()
async def unmute(ctx, user, *reason):

	if reason == []:
		reason = "no reason"
	else:
		reason = " ".join(reason)

	if ctx.message.mentions != []:
		user = ctx.message.mentions
	else:
		user = client.get_user(int(user))
		if not user:
			await("you need to ping someone or give a user id")
			return

	muted = client.get_role(774294917299830824)

	await user.send(f"you were **unmuted** for {reason}")
	await user.remove_roles(muted)

# VVVVVV events VVVVVV

@client.event
async def on_member_join(member):
	welcome = client.get_channel(766848918499360809)

	await welcome.send(f"{member.mention} has joined the server\n\nwe now have {len(member.guild.members)} members")
	await member.send(f"welcome to **{member.guild.name}**")

@client.event
async def on_member_remove(member):
	welcome = client.get_channel(766848918499360809)

	await welcome.send(f"{member.mention} has left the server\n\nwe now have {len(member.guild.members)} members")
	await member.send(f"thanks for joining **{member.guild.name}**, we hope to see you again")

@client.event
async def on_command_error(ctx:commands.Context, exception):
	embed = discord.Embed(color=discord.Color.red())
	if type(exception) is commands.errors.MissingRequiredArgument:
		embed.title = "You forgot an argument"
		embed.description = f"The syntax to `{client.command_prefix}{ctx.command.name}` is `{client.command_prefix}{ctx.command.name} {ctx.command.signature}`."
		await ctx.send(embed=embed)
	elif type(exception) is commands.CommandNotFound:
		embed.title = "Invalid command"
		embed.description = f"The command you just tried to use is invalid. Use `{client.command_prefix}help` to see all commands."
		await ctx.send(embed=embed)
	else:
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

client.run(token)