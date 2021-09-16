import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, ComponentContext, create_select_option, create_select
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import ButtonStyle, SlashCommandPermissionType

import json
import random
import sys
import traceback

intents = discord.Intents.all()
client = commands.Bot(command_prefix='g!', intents=intents)
slash = SlashCommand(client, sync_commands=True,debug_guild=766848554899079218)

@client.event
async def on_ready():
	print("hello world!")
	gamerzone = client.get_guild(766848554899079218)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with your mom"))

with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

# VVVVVV commands VVVVVV'

@slash.slash()
async def membercount(ctx):
	await ctx.send(f"{len(ctx.guild.members)} members", hidden=hidden)

@slash.slash()
async def owo(ctx, owo, hidden:bool = False):
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
	await ctx.send(owo, hidden=hidden)

@slash.slash(default_permission=False, permissions={766848554899079218: [create_permission(312292633978339329, SlashCommandPermissionType.USER, True)]})
async def purge(ctx, messageid, hidden:bool = False):
	messageid = int(messageid)

	purge = None
	async for x in ctx.channel.history():
		try:
			if x.id == messageid:
				purge = x
		except AttributeError:
			embed = discord.Embed(title="you need to give a message id", colour=discord.Colour.red())
			await ctx.send(embed=embed, hidden=hidden)
			return
	print(purge.content)
	
	async for x in ctx.channel.history(limit=1):
		message = x
	print(message.content)

	amount = 2
	async for x in ctx.channel.history(after=purge, before=message):
		amount += 1

	await ctx.channel.purge(after=purge, before=message)
	await message.delete()
	await purge.delete()
	embed = discord.Embed(title=f"{amount} messages purged", colour=discord.Colour.green())
	await ctx.send(embed=embed, hidden=hidden)

@slash.slash()
async def ping(ctx, hidden:bool = False):
	await ctx.send(f'Pong! {round(client.latency*1000)} ms', hidden=hidden)

@slash.slash(default_permission=False, permissions={766848554899079218: [create_permission(766849548277645313, SlashCommandPermissionType.ROLE, True)]})
async def wii(ctx, game:str, hidden:bool = False):
	rhozeta = client.get_user(312292633978339329)
	await rhozeta.send(f'wii game from **{ctx.author}** ```{game}```')
	print(f'wii game from {ctx.author}, {game}')
	await ctx.send(f'suggestion taken ```{game}```', hidden=hidden)

@slash.slash(default_permission=False, permissions={766848554899079218: [create_permission(766849548277645313, SlashCommandPermissionType.ROLE, True)]})
async def kick(ctx, user:discord.Member, reason:str, hidden:bool = False):

	if ctx.channel.permissions_for(ctx.author).kick_members:
		try:
			await user.send(f"kicked by {ctx.author} for `{reason}`")
			await ctx.guild.kick(user, reason=f"kicked by {ctx.author} for {reason}")
			await ctx.send(f"kicked {user.name} for `{reason}`", hidden=hidden)
		except discord.errors.HTTPException:
			await ctx.guild.kick(user, reason=f"kicked by {ctx.author} for {reason}")
			await ctx.send(f"kicked {user.name} for `{reason}`", hidden=hidden)
	else:
		embed = discord.Embed(title="you dont have permission to do this command", colour=discord.Colour.red(), description="become a mod nerd")

		await ctx.send(embed=embed, hidden=hidden)

@slash.slash(default_permission=False, permissions={766848554899079218: [create_permission(766849548277645313, SlashCommandPermissionType.ROLE, True)]})
async def ban(ctx, user:discord.Member, reason:str, hidden:bool = False):
	try:
		await user.send(f"banned by {ctx.author} for `{reason}`")
		await ctx.guild.ban(user, reason=f"banned by {ctx.author} for {reason}", delete_message_days=0)
		await ctx.send(f"banned {user.name} for `{reason}`", hidden=hidden)
	except discord.errors.HTTPException:
		await ctx.guild.ban(user, reason=f"banned by {ctx.author} for {reason}", delete_message_days=0)
		await ctx.send(f"banned {user.name} for `{reason}`", hidden=hidden)

@slash.slash(default_permission=False, permissions={766848554899079218: [create_permission(766849548277645313, SlashCommandPermissionType.ROLE, True)]})
async def mute(ctx, user:discord.Member, reason:str, hidden:bool = False):
	muted = ctx.guild.get_role(774294917299830824)
	try:
		await user.send(f"you were **muted** for {reason}")
		await ctx.send(f"muted {user.display_name} for {reason}", hidden=hidden)
	except discord.errors.Forbidden:
		await ctx.send(f"muted {user.display_name} for {reason} but i couldnt message them", hidden=hidden)
	await user.add_roles(muted)

@slash.slash(default_permission=False, permissions={766848554899079218: [create_permission(766849548277645313, SlashCommandPermissionType.ROLE, True)]})
async def unmute(ctx, user:discord.Member, reason:str, hidden:bool = False):
	muted = ctx.guild.get_role(774294917299830824)
	try:
		await user.send(f"you were **unmuted** for {reason}")
		await ctx.send(f"unmuted `{user.display_name}` for {reason}", hidden=hidden)
	except discord.errors.Forbidden:
		await ctx.send(f"unmuted `{user.display_name}` for `{reason}` but i couldnt message them", hidden=hidden)
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

client.run(token)