#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Kabilan Tamilmani
# E-mail: kavikabilan37@gmail.com
# Github: Kabilan-T

''' Nanban bot execution script '''

#-------------------------------------------------------------------------------

import os
import discord
from bots.base import BaseBot
import hosting

class NanbanBot(BaseBot):
    ''' Nanban bot class definition '''

    def __init__(self):
        ''' Initialize the bot '''
        super().__init__('nanban')
    
if __name__ == '__main__':
    # Launch the bot
    TOKEN = os.getenv('NANBAN_BOT_TOKEN', None)
    nanban_bot = NanbanBot()
    hosting.keep_alive()
    nanban_bot.run(TOKEN)