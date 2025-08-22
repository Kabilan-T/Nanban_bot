# Nanban Bot

Nanban is a standalone Discord bot written in Python using the `discord.py` library. It is designed to enhance community interactions and provides a mix of utility, moderation, entertainment, and cultural features.

This bot is originally derived from my other [discord_bot](https://github.com/Kabilan-T/discord_bots) project, which contained multiple custom bots for the "Axiom" server (inspired by the movie WALL-E). Nanban takes that foundation and simplifies it into a single reusable bot that can be easily set up in any Discord server. For more information on the original project, you can visit the [discord_bots](https://github.com/Kabilan-T/discord_bots) repository.


The main functionalities include:
- General utilities: Commands for everyday server usage and convenience.
- Moderation tools: Role management, message cleanup, and moderation commands.
- Voice features: Voice channel greetings, text-to-speech, and interactions.
- Radio streaming: Play and manage online radio streams in voice channels.
- Thirukkural module: Daily Thirukkural posts with access in Tamil and English.
- CosmicCon commands: Fun, pop-culture–inspired interactions.


## Usage

To use the bots in your own server, you need to create a Discord bot and get the token. The following link provides the instructions to create a Discord bot and get the token: [Discord Bot](https://discordpy.readthedocs.io/en/stable/discord.html)

The tokens are secret and should not be shared with anyone. The tokens are sourced as environment variables and are used in the code to authenticate the bot with the Discord server. 

Create a `tokens.sh` file in the root directory of the project and add the following lines to the file.

```
export NANBAN_BOT_TOKEN="<Enter bot token here>"
```

Follow the instructions in the [Installation](#installation) section to create the virtual environment and install the required packages.

To start the bot's execution, a `run.bash` script is provided in the repository. The script will activate the virtual environment, source the token file, and run the Python script of the bot. The command to run the script is as follows.
```
bash run.bash
```
or make the script executable and run the script.
```
chmod +x run.bash
./run.bash
```
The bot will start executing and you can see the logs in the terminal.

To stop a bot execution, press `Ctrl + C` in the terminal where the bot is running.

Note: If you don't have `tokens.sh` file in the root directory, `run.bash` script will create a template file for you. You need to enter the bot tokens in the file and run the `run.bash` script again.

## Installation

1. Clone the repository to your local machine.

```
git clone https://github.com/Kabilan-T/discord_bots.git
```

2. Install miniconda or anaconda to create a virtual environment. Use the following link for installation instructions: [Miniconda](https://conda.io/projects/conda/en/latest/index.html) or use the following command to install Miniconda.

```
sudo apt-get update
sudo apt-get install wget
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

3. Create the virtual environment and install the required packages. To ease the installation process, a `setup.bash` script is provided in the repository. Run the following command.
    
```
bash setup.bash
```
optional: `--with-auto-update` flag to enable automatic updates (cron job to run `update.bash` every 6 hours, which fetches the latest changes from the repository and applies them).

```
bash setup.bash --with-auto-update
```


Credits: [Vijhay Anandd](https://github.com/vijayanandrp)  for [Thirukkural Dataset](https://github.com/vijayanandrp/Thirukkural-Tamil-Dataset)