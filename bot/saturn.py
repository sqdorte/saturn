#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
import re
import json
import asyncio
import os

if not 'TOKEN' in os.environ:
  print('Token not found, exiting...')
  raise SystemExit
  
if not 'LOG' in os.environ:
  print('Log channel id missing, exiting...')
  raise SystemExit

token = os.environ.get('TOKEN')
log = os.environ.get('LOG')

invite_pattern = re.compile(r'(?:discord\.gg/|discordapp\.com/invite/)([^\s|^\W+$]+)')
last = None

client = discord.Client()

@client.event
async def on_ready():
  print(f'\n\nLogged in as {client.user.name} [{client.user.id}]\n\n')

@client.event
async def on_message(e):
  global last
  if e.author.id == client.user.id:
    return

  if client.get_member(client.user.id) in e.mentions:
    client.send_file(e.channel, '../media/sanic.png')

  if e.type == 7:
    last = e

@client.event
async def on_member_join(member):
  global last
  if invite_pattern.match(member.name) is not None:
    
    while last == None:
      await asyncio.sleep(0.5)

    await client.delete_message(last)
    await client.ban(member)

    em = discord.Embed(
      color = 0x36393F,
      title = 'Blocked invite and banned user.'
    )
    em.add_field(
      name = 'Member',
      value = f'<@{member.id}>'
    )
    em.add_field(
      name = 'Invite',  
      value = ''.join(invite_pattern.findall(member.name))
    )

    await client.send_message(client.get_channel(log), embed=em)

    last = None

client.run(token)
