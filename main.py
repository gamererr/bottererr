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


with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

# VVVVVV commands VVVVVV'

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency*1000)} ms')

@client.command()
async def kick(ctx, user, reason):

	if ctx.channel.permissions_for(ctx.author).kick_members:
		try:
			await ctx.message.mentions[0].send(f"kicked by {ctx.message.author} for `{reason}`")
			await ctx.guild.kick(ctx.message.mentions[0], reason=f"kicked by ctx.message.author for {reason}")
			await ctx.send(f"kicked {ctx.message.mentions[0].name} for `{reason}`")
		except discord.errors.HTTPException:
			await ctx.guild.kick(ctx.message.mentions[0], reason=f"kicked by ctx.message.author for {reason}")
			await ctx.send(f"kicked {ctx.message.mentions[0].name} for `{reason}`")
	else:
		embed = discord.Embed(title="you dont have permission to do this command", colour=discord.Colour.red(), description="become a mod nerd")

		await ctx.send(embed=embed)


@client.command()
async def ban(ctx, user, reason):

	if ctx.channel.permissions_for(ctx.author).ban_members:
		try:
			await ctx.message.mentions[0].send(f"banned by {ctx.message.author} for `{reason}`")
			await ctx.guild.ban(ctx.message.mentions[0], reason=f"banned by ctx.message.author for {reason}", delete_message_days=0)
			await ctx.send(f"banned {ctx.message.mentions[0].name} for `{reason}`")
		except discord.errors.HTTPException:
			await ctx.guild.ban(ctx.message.mentions[0], reason=f"banned by ctx.message.author for {reason}", delete_message_days=0)
			await ctx.send(f"banned {ctx.message.mentions[0].name} for `{reason}`")
	else:
		embed = discord.Embed(title="you dont have permission to do this command", colour=discord.Colour.red(), description="become a mod nerd")

		await ctx.send(embed=embed)


# VVVVVV events VVVVVV

@client.event
async def on_member_join(member):
	welcome = discord.utils.get(member.guild.channels, id=766848918499360809)

	await member.send(f"welcome to **{member.guild.name}**")
	await welcome.send(f"{member.mention} has joined the server\n\nwe now have {len(member.guild.members)} members")

@client.event
async def on_member_remove(member):
	welcome = discord.utils.get(member.guild.channels, id=766848918499360809)

	await welcome.send(f"{member.mention} has left the server\n\nwe now have {len(member.guild.members)} members")

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
