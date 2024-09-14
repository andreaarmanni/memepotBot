from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, Application
import logging

# Initialize logging
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

total_steps = 1000000

# Game Start command handler
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

    # Show the current progress to the player
    await query.answer(text=f"{meme.upper()} has gained {steps} votes.")

# Leaderboard command handler
async def leaderboard(update, context):
    """Displays the leaderboard showing the total steps for each memecoin."""
    leaderboard_text = "🏆 Meme Coin Leaderboard 🏆\n\n"
    
    # Iterate through each memecoin and display the progress
    for meme, steps in meme_counters.items():
        leaderboard_text += f"{meme.upper()}: {steps}/{total_steps} votes\n"

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
