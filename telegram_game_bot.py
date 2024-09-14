from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, Application
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set your bot token
bot_token = '7062758539:AAGeUAMUPlR6yU4Gg9fMrcplTDA01RbGiX0'

# Create the Bot instance
bot = Bot(token=bot_token)

# Game data
meme_counters = {
    'bonk': 0,
    'buddha': 0,
    'wif': 0,
    'wolf': 0
}

total_steps = 1000  # Define the total number of steps for a memecoin to win

# Dictionary to store player contributions (player handle -> total steps made)
player_contributions = {}

# Progress bar settings
bar_length = 20  # Number of characters in the progress bar

def create_progress_bar(current_steps, total_steps, bar_length=20):
    """Creates a progress bar based on the current steps and total steps."""
    progress = int((current_steps / total_steps) * bar_length)  # Calculate progress as a percentage of the bar
    bar = '█' * progress + '-' * (bar_length - progress)  # Create the progress bar string
    return f"{bar} {current_steps}/{total_steps} steps"

# Start command handler
async def start_game(update, context):
    """Starts the game and shows the interactive buttons."""
    chat_id = update.message.chat_id

    # Create game buttons for players to interact
    keyboard = [
        [InlineKeyboardButton("BONK", callback_data='bonk')],
        [InlineKeyboardButton("BUDDHA", callback_data='buddha')],
        [InlineKeyboardButton("WIF", callback_data='wif')],
        [InlineKeyboardButton("WOLF", callback_data='wolf')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the game interface to the player
    await update.message.reply_text('Vote your favorite project. Win the race to get a $50,000 buyback and be the first to launch on memepot!🔥', reply_markup=reply_markup)

# Callback query handler for memecoin clicks
async def button_click(update: Update, context):
    """Handles the memecoin button clicks to update progress."""
    query = update.callback_query
    meme = query.data  # The memecoin clicked
    user = query.from_user  # The user who clicked

    meme_counters[meme] += 1  # Increment memecoin progress

    # Track player contributions
    username = user.username if user.username else user.first_name  # Use username or first name if no handle
    if username in player_contributions:
        player_contributions[username] += 1  # Increment the player's total steps
    else:
        player_contributions[username] = 1  # Add the player with 1 step

    # Show the current progress to the player with the progress bar
    progress_bar = create_progress_bar(meme_counters[meme], total_steps)
    await query.answer(text=f"{meme.upper()} has gained {meme_counters[meme]} votes.\n{progress_bar}")

# Leaderboard command handler with progress bar
async def leaderboard(update, context):
    """Displays the leaderboard showing the total steps and progress bar for each memecoin."""
    leaderboard_text = "🏆 MEMES LEADERBOARD 🏆\n\n"
    
    # Iterate through each memecoin and display the progress with a progress bar
    for meme, steps in meme_counters.items():
        progress_bar = create_progress_bar(steps, total_steps)  # Generate progress bar for each memecoin
        leaderboard_text += f"{meme.upper()}: {progress_bar}\n"

    # Send the leaderboard as a message
    await update.message.reply_text(leaderboard_text)

# Players command handler to show player contributions with trophy emojis for top 3
async def players(update, context):
    """Displays the total steps made by each player, with trophies for the top 3 players."""
    players_text = "🚀 TOP PLAYERS 🚀\n\n"

    # Check if there are any contributions yet
    if not player_contributions:
        players_text += "There haven't been any players yet!"
    else:
        # Sort players by total steps in descending order
        sorted_players = sorted(player_contributions.items(), key=lambda x: x[1], reverse=True)

        # Add top 3 players with trophy emojis
        for index, (player, steps) in enumerate(sorted_players):
            if index == 0:
                players_text += f"🥇 {player}: {steps} votes\n"  # Gold trophy
            elif index == 1:
                players_text += f"🥈 {player}: {steps} votes\n"  # Silver trophy
            elif index == 2:
                players_text += f"🥉 {player}: {steps} votes\n"  # Bronze trophy
            else:
                players_text += f"{player}: {steps} votes\n"  # No trophy for other players

    # Send the player contributions as a message
    await update.message.reply_text(players_text)

# Main function to run the bot
def main():
    # Initialize bot application
    application = Application.builder().token(bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start_game))
    application.add_handler(CommandHandler('leaderboard', leaderboard))  # Add the leaderboard command
    application.add_handler(CommandHandler('players', players))  # Add the players command
    application.add_handler(CallbackQueryHandler(button_click))

    # Start polling to listen for incoming commands and game events
    application.run_polling()

if __name__ == '__main__':
    main()
