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

total_steps = 100  # Define the total number of steps for a memecoin to win

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
    meme_counters[meme] += 1  # Increment memecoin progress
    steps = meme_counters[meme]

    # Show the current progress to the player with the progress bar
    progress_bar = create_progress_bar(steps, total_steps)
    await query.answer(text=f"{meme.upper()} has gained {steps} votes.\n{progress_bar}")

# Leaderboard command handler with progress bar
async def leaderboard(update, context):
    """Displays the leaderboard showing the total steps and progress bar for each memecoin."""
    leaderboard_text = "🏆 Meme Coin Leaderboard 🏆\n\n"
    
    # Iterate through each memecoin and display the progress with a progress bar
    for meme, steps in meme_counters.items():
        progress_bar = create_progress_bar(steps, total_steps)  # Generate progress bar for each memecoin
        leaderboard_text += f"{meme.upper()}: {progress_bar}\n"

    # Send the leaderboard as a message
    await update.message.reply_text(leaderboard_text)

# Main function to run the bot
def main():
    # Initialize bot application
    application = Application.builder().token(bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start_game))
    application.add_handler(CommandHandler('leaderboard', leaderboard))  # Add the leaderboard command
    application.add_handler(CallbackQueryHandler(button_click))

    # Start polling to listen for incoming commands and game events
    application.run_polling()

if __name__ == '__main__':
    main()
