#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Kabilan Tamilmani
# E-mail: kavikabilan37@gmail.com
# Github: Kabilan-T

''' Manage cog for the bot'''

#-------------------------------------------------------------------------------

import os
import io
import yaml
import zipfile
import asyncio
import subprocess
import discord
from discord.ext import commands
from discord.ext.commands import Context

tmp = "tmp"

class Manage(commands.Cog, name="Manage"):
    def __init__(self, bot):
        '''Initializes the bot management cog'''
        self.bot = bot

    @commands.command( name="reload", description="Reload the bot cogs.")
    @commands.has_permissions(administrator=True)
    async def reload(self, context: Context):
        '''Reload the bot cogs'''
        (succeeded_reloads, failed_reloads, unloaded) = await self.bot.reload_extensions()
        embed = discord.Embed(
            title="Cogs Reloaded :gear:",
            color=self.bot.default_color,
            )
        if len(succeeded_reloads) > 0:
            embed.add_field(
                name="Succeeded",
                value=f"\n".join([f":thumbsup: `{cog}`" for cog in succeeded_reloads]),
                inline=False,
                )
        if len(failed_reloads) > 0:
            embed.add_field(
                name="Failed",
                value=f"\n".join([f":thumbsdown: `{cog}`" for cog in failed_reloads]),
                inline=False,
                )
        if len(unloaded) > 0:
            embed.add_field(
                name="Unloaded",
                value=f"\n".join([f":x: `{cog}`" for cog in unloaded]),
                inline=False,
                )
        await context.send(embed=embed)

    @commands.command( name="set_log_channel", description="Set the log channel for the bot.")
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, context: Context, channel: discord.TextChannel):
        '''Set the log channel for the bot'''
        self.bot.log.set_log_channel(context.guild.id, channel)
        if os.path.exists(os.path.join(self.bot.data_dir, str(context.guild.id), 'custom_settings.yml')):
            with open(os.path.join(self.bot.data_dir, str(context.guild.id), 'custom_settings.yml'), 'r') as file:
                guild_settings = yaml.safe_load(file)
                guild_settings['log_channel'] = channel.id
        else:
            guild_settings = {'log_channel': channel.id}
        with open(os.path.join(self.bot.data_dir, str(context.guild.id), 'custom_settings.yml'), 'w+') as file:
            yaml.dump(guild_settings, file)
        embed = discord.Embed(
            title="Log Channel",
            description=f"Log channel has been set to {channel.mention}",
            color=self.bot.default_color,
            )
        await context.send(embed=embed)
        self.bot.log.info(f"Log channel set to {channel.mention}", context.guild)

    @commands.command( name="get_data", description="Send the data of the bot as zip file.")
    @commands.has_permissions(administrator=True)
    async def getdata(self, context: Context):
        '''Get the data of the bot'''
        if os.path.exists(os.path.join(self.bot.data_dir, str(context.guild.id))):
            dir_path = os.path.join(self.bot.data_dir, str(context.guild.id))
            zip_file_path = os.path.join(self.bot.data_dir, f"{context.guild.id}.zip")
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dir_path))
            file = discord.File(filename=f"{self.bot.name}_{context.guild.id}.zip",  
                                fp=zip_file_path)
            embed = discord.Embed(
                title="Data :file_folder:",
                description="Here is the data of the bot.",
                color=self.bot.default_color,
                )
            await context.reply(embed=embed, file=file)
            self.bot.log.info(f"Data sent to {context.author.name}", context.guild)
            os.remove(zip_file_path)
        else:
            embed = discord.Embed(
                title="Data",
                description="No data found.",
                color=self.bot.default_color,
                )
            await context.send(embed=embed)
    
    @commands.command( name="clear_data", description="Clear the data of the bot including custom settings.")
    @commands.has_permissions(administrator=True)
    async def cleardata(self, context: Context):
        '''Clear the data of the bot'''
        if os.path.exists(os.path.join(self.bot.data_dir, str(context.guild.id))):
            for file in os.listdir(os.path.join(self.bot.data_dir, str(context.guild.id))):
                os.remove(os.path.join(self.bot.data_dir, str(context.guild.id), file))
        self.bot.log.info(f"Data cleared", context.guild)
        self.bot.log.remove_log_channel(context.guild.id)
        embed = discord.Embed(
            title="Data Cleared :wastebasket:",
            description="The data of the bot has been cleared. Cogs will be reloaded to apply changes.",
            color=self.bot.default_color,
            )
        await context.send(embed=embed)
        await self.reload(context)
    
async def setup(bot):
    await bot.add_cog(Manage(bot))     