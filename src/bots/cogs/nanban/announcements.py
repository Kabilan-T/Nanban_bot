#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Kabilan Tamilmani
# E-mail: kavikabilan37@gmail.com
# Github: Kabilan-T

''' Announcements messages for server and DMs '''

#-------------------------------------------------------------------------------

import os
import yaml
import discord
import typing
import datetime
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import Context

class Announcements(commands.Cog, name="Announcements"):
    def __init__(self, bot):
        self.bot = bot
        if self.broadcast_daily_highlights.is_running():
            self.bot.log.info("broadcast_daily_highlights task is already running")
            self.broadcast_daily_highlights.stop()
            self.bot.log.info("broadcast_daily_highlights task stopped")
        self.broadcast_daily_highlights.start()
    
    @tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=datetime.timezone.utc))
    async def broadcast_daily_highlights(self):
        ''' Broadcast daily highlights to all servers '''
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        holiday_data = self.load_holiday_data()
        if holiday_data is None: return
        todays_events = holiday_data.get(today, None)
        if todays_events is None:
            self.bot.log.info(f"No special events found for {today}")
            return
        embed = discord.Embed(
            title="Today's Highlights :calendar_spiral:",
            color=self.bot.default_color,
            )
        for event in todays_events:
            event_name = event['name']
            event_description = event['description']
            event_type = event['types']
            embed.add_field(name=f"**{event_name}**",
                            value=f"_{event_description}_\ncategory: _{event_type}_\n",
                            inline=False)
        for guild in self.bot.guilds:
            general_channel = discord.utils.find( lambda c: "general" in c.name.lower(), guild.text_channels)
            if general_channel is not None:
                embed.set_author(name=self.bot.name+", Your Friend", icon_url=self.bot.user.avatar.url)
                embed.set_footer(text=f"Earth Date: {today} \t\t\t\tStar Date: {(discord.utils.utcnow() - guild.created_at).days} days")
                await general_channel.send(embed=embed)
                self.bot.log.info(f"Sending today's highlights to {guild.name} in {general_channel.name}", guild)
            else:
                self.bot.log.warning(f"No general channel found in {guild.name}", guild)
    
    @broadcast_daily_highlights.before_loop
    async def before_broadcast(self):
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.broadcast_daily_highlights.cancel()
        
    def load_holiday_data(self):
        ''' Load holidays data from file '''
        data_fpath = os.path.join(self.bot.data_dir, "holidays_2026.yml")
        if not os.path.exists(data_fpath):
            self.bot.log.warning(f"Holidays file not found in {data_fpath}")
            return None
        try:
            with open(data_fpath, "r") as file:
                holidays = yaml.load(file, Loader=yaml.FullLoader) or None
            self.bot.log.info(f"Loaded {len(holidays)} holidays from {data_fpath}")
            return holidays
        except Exception as e:
            self.bot.log.warning(f"Error loading holidays: {e}")
            return None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        ''' Send welcome message when a new member joins the server '''
        if member.bot: return
        guild = member.guild
        self.bot.log.info(f"New member {member.display_name} joined {guild.name}", guild)
        if guild.system_channel is not None:
            embed = await self.get_welcome_message(guild, member)
            await guild.system_channel.send(embed=embed)
            self.bot.log.info(f"Sending greeting message to {member.display_name} in {guild.system_channel.name}", guild)
        try:
            embed = await self.get_welcome_dm_message(guild, member)
            await member.send(embed=embed)
            self.bot.log.info(f"Sending greeting message to {member.display_name} in DM", guild)
        except discord.Forbidden:
            self.bot.log.warning(f"Failed to send greeting message to {member.display_name} in DM", guild)
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        ''' Send goodbye message when a member leaves the server '''
        if member.bot: return
        guild = member.guild
        self.bot.log.info(f"Member {member.display_name} left {guild.name}", guild)
        if guild.system_channel is not None:
            embed = await self.get_goodbye_message(guild, member)
            await guild.system_channel.send(embed=embed)
            self.bot.log.info(f"Sending goodbye message to {member.display_name} in {guild.system_channel.name}", guild)
        try:
            embed = await self.get_goodbye_dm_message(guild, member)
            await member.send(embed=embed)
            self.bot.log.info(f"Sending goodbye message to {member.display_name} in DM", guild)
        except discord.Forbidden:
            self.bot.log.warning(f"Failed to send goodbye message to {member.display_name} in DM", guild)
            pass

    async def get_welcome_message(self, guild: discord.Guild,  member: discord.Member):
        ''' Get welcome message for a member '''
        embed = discord.Embed()
        embed.set_author(name=self.bot.name+", Your Friend",
                         icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.title = f"A new nanban (friend) has joined!"
        embed.description = f"Welcome to **{guild.name}**, {member.mention}! The more the merrier! :tada:\n\n"
        embed.description += f" :handshake: Say hi and make yourself at home!"
        embed.color = discord.Color.green()
        embed.add_field(name=":busts_in_silhouette: Member count:",
                        value=f"{guild.member_count}",
                        inline=True)
        embed.add_field(name=":calendar: Server age:",
                        value=f"{(discord.utils.utcnow() - guild.created_at).days} days",
                        inline=True)
        embed.set_footer(text=f"Glad to have you here, @{member.name}!")
        return embed

    async def get_goodbye_message(self, guild: discord.Guild,  member: discord.Member):
        ''' Get goodbye message for a member '''
        embed = discord.Embed()
        embed.set_author(name=self.bot.name+", Your Friend",
                            icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.title = f"Our nanban {member.display_name} has left."
        embed.description = f":wave: {member.mention} has left **{guild.name}**.\n"
        embed.description += f"We'll miss you — come back soon!"
        embed.color = discord.Color.red()
        embed.add_field(name=":busts_in_silhouette: Member count:",
                        value=f"{guild.member_count}",
                        inline=True)
        embed.add_field(name=":stopwatch: Time with us:",
                        value=f"{(discord.utils.utcnow() - member.joined_at).days} days",
                        inline=True)
        embed.set_footer(text=f"You'll always be a nanban, @{member.name}")
        return embed

    async def get_welcome_dm_message(self, guild: discord.Guild,  member: discord.Member):
        ''' Get welcome DM message for a member '''
        embed = discord.Embed()
        embed.set_author(name=self.bot.name+", Your Friend",
                         icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.title = f"Hey {member.display_name}, welcome to {guild.name}!"
        embed.description = f"I'm **Nanban**, your friendly server companion. :wave:\n\n"
        embed.description += f"There are **{guild.member_count}** members in **{guild.name}** — and now you're one of us!\n\n"
        embed.description += f":speech_balloon: Jump into the conversations, have fun, and don't hesitate to reach out if you need anything."
        embed.color = discord.Color.green()
        embed.set_footer(text="Nanban means 'friend' in Tamil — and that's exactly what we are!")
        return embed

    async def get_goodbye_dm_message(self, guild: discord.Guild,  member: discord.Member):
        ''' Get goodbye DM message for a member '''
        embed = discord.Embed()
        embed.set_author(name=self.bot.name+", Your Friend",
                            icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.title = f"Goodbye {member.display_name}, take care!"
        embed.description = f"You've left **{guild.name}**, but you'll always be a nanban to us. :heart:\n\n"
        embed.description += f"Hope you had a great time — the door is always open if you want to come back!"
        embed.color = discord.Color.red()
        embed.set_footer(text="Until we meet again!")
        return embed


async def setup(bot):
    await bot.add_cog(Announcements(bot))