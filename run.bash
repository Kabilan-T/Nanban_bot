#!/bin/bash

# Check if script is run from Nanban_bot directory
if [[ ! $(basename "$(pwd)") == "Nanban_bot" ]]; then
    echo "Please run this script from the Nanban_bot directory."
    exit 1
fi


# Check if tokens.sh file exists
if [ ! -f "tokens.sh" ]; then
    echo "tokens.sh not found. Creating a template..."
    # Create tokens.sh file with template
    cat << EOF > tokens.sh
#!/bin/bash

# Please fill in your bot tokens below

export NANBAN_BOT_TOKEN="<Enter bot token here>"

EOF
    echo "Template created in tokens.sh. Please fill in your bot tokens and then rerun the script."
    exit 0
fi

# Activate the virtual environment
eval "$(conda shell.bash hook)"
conda activate nanban_bot_env

# Check if the Conda environment is activated
if [[ -z "$CONDA_PREFIX" ]]; then
    echo "Failed to activate Conda environment 'nanban_bot_env'. Exiting."
    exit 1
fi

echo "Virtual environment 'nanban_bot_env' activated."

# Source token file
source tokens.sh

# Run the Nanban bot
python src/nanban.py

exit 0
