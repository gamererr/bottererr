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
	guild = client.get_guild(766848554899079218)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with your mom"))

with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

# VVVVVV commands VVVVVV'

@slash.slash()
async def membercount(ctx, hidden:bool=True):
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

pronounslist = [
	create_button(style=ButtonStyle.blue, label="he/him", custom_id="874814745482502195"),
	create_button(style=ButtonStyle.blue, label="she/her", custom_id="874814779598995516"),
	create_button(style=ButtonStyle.blue, label="they/them", custom_id="874814813803544587"),
	create_button(style=ButtonStyle.blue, label="other", custom_id="874814852990906430"),
	create_button(style=ButtonStyle.red, label="remove pronoun", custom_id="rp")
]
colorlist1 = [
	create_button(style=ButtonStyle.grey, label="Red", custom_id="874816935186026536"),
	create_button(style=ButtonStyle.grey, label="Orange ", custom_id="874816865925472296"),
	create_button(style=ButtonStyle.grey, label="Yellow", custom_id="874817014424813619"),
	create_button(style=ButtonStyle.grey, label="Green", custom_id="874817043180970014")
]
colorlist2 = [
	create_button(style=ButtonStyle.grey, label="Blue", custom_id="874816828080283679"),
	create_button(style=ButtonStyle.grey, label="Purple", custom_id="874816896497770527"),
	create_button(style=ButtonStyle.grey, label="White", custom_id="874816975514251266"),
	create_button(style=ButtonStyle.red, label="remove color", custom_id="rc")
]
pridelist1 = [
	create_button(style=ButtonStyle.green, label="gay/lesbian", custom_id="874815859930038292"),
	create_button(style=ButtonStyle.green, label="bi/pan", custom_id="874815900342157362"),
	create_button(style=ButtonStyle.green, label="asexual", custom_id="874815999210311754")
]
pridelist2 = [
	create_button(style=ButtonStyle.green, label="trans", custom_id="874816036761923614"),
	create_button(style=ButtonStyle.green, label="straight", custom_id="892410652973494332"),
	create_button(style=ButtonStyle.green, label="other", custom_id="892420004119715930"),
	create_button(style=ButtonStyle.red, label="remove pride", custom_id="rpr")
]

pronouns = create_actionrow(*pronounslist)
color1 = create_actionrow(*colorlist1)
color2 = create_actionrow(*colorlist2)
pride1 = create_actionrow(*pridelist1)
pride2 = create_actionrow(*pridelist2)

@slash.slash()
async def role(ctx):
	embed = discord.Embed(title=f"pronouns", colour=discord.Colour.blue(), description=f"select your pronouns")
	await ctx.channel.send(embed=embed, components=[pronouns])
	embed = discord.Embed(title=f"color", colour=discord.Colour.dark_gray(), description=f"select your color")
	await ctx.channel.send(embed=embed, components=[color1])
	await ctx.channel.send("** **", components=[color2])
	embed = discord.Embed(title=f"sexuality", colour=discord.Colour.green(), description=f"select your sexuality")
	await ctx.channel.send(embed=embed, components=[pride1])
	await ctx.channel.send("** **", components=[pride2])

# VVVVVV callbacks VVVVVV

@slash.component_callback(components=["874814745482502195","874814779598995516","874814813803544587","874814852990906430","rp","874816935186026536","874816865925472296","874817014424813619","874817043180970014","874816828080283679","874816896497770527","874816975514251266","rc","874815859930038292","874815900342157362","874815999210311754","874816036761923614","892410652973494332","892420004119715930","rpr"])
async def rolecallback(ctx): # called for when a user presses a self assign role button
	if ctx.custom_id == "rp":
		roles = [ctx.guild.get_role(874814745482502195),ctx.guild.get_role(874814779598995516),ctx.guild.get_role(874814813803544587),ctx.guild.get_role(874814852990906430)]

		for x in roles:
			await ctx.author.remove_roles(x)
		await ctx.send("removed all the pronoun roles you had", hidden=True)
	elif ctx.custom_id == "rc":
		roles = [ctx.guild.get_role(874816935186026536),ctx.guild.get_role(874816865925472296),ctx.guild.get_role(874817014424813619),ctx.guild.get_role(874817043180970014),ctx.guild.get_role(874816828080283679),ctx.guild.get_role(874816896497770527),ctx.guild.get_role(874816975514251266)]

		for x in roles:
			await ctx.author.remove_roles(x)
		await ctx.send("removed the color role you had", hidden=True)
	elif ctx.custom_id == "rpr":
		roles = [ctx.guild.get_role(874815859930038292),ctx.guild.get_role(874815900342157362),ctx.guild.get_role(874815999210311754),ctx.guild.get_role(874816036761923614),ctx.guild.get_role(892410652973494332),ctx.guild.get_role(892420004119715930)]

		for x in roles:
			await ctx.author.remove_roles(x)
		await ctx.send("removed the sexuality role role you had", hidden=True)
	else:
		id = int(ctx.custom_id)

		if ctx.custom_id in ["874814745482502195","874814779598995516","874814813803544587","874814852990906430"]:
			group = "pronouns"
		elif ctx.custom_id in ["874816935186026536","874816865925472296","874817014424813619","874817043180970014","874816828080283679","874816896497770527","874816975514251266"]:
			group = "colors"
		elif ctx.custom_id in ["874815859930038292","874815900342157362","874815999210311754","874816036761923614","892410652973494332","892420004119715930"]:
			group = "sexuality"

		role = ctx.guild.get_role(id)
		await ctx.author.add_roles(role)
		await ctx.send(f"gave you {role} role from {group}", hidden=True)


# VVVVVV events VVVVVV

@client.event
async def on_member_join(member):
	welcome = client.get_channel(766848918499360809)
	if not member.bot:
		role1 = member.guild.get_role(874814677295714366)
		role2 = member.guild.get_role(874815019282464810)
		await member.add_roles(role1)
		await member.add_roles(role2)

	await welcome.send(f"{member.mention} has joined the server\n\nwe now have {len(member.guild.members)} members")

@client.event
async def on_member_remove(member):
	welcome = client.get_channel(766848918499360809)

	await welcome.send(f"{member.mention} has left the server\n\nwe now have {len(member.guild.members)} members")

client.run(token)