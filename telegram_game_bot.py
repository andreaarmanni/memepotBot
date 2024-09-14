import matplotlib.pyplot as plt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import logging
import asyncio

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize counters for meme coins
meme_counters = {
    'bonk': 0,
    'wen': 0,
    'maneki': 0,
    'popcat': 0,
    'mumu': 0,
    'wolf': 0
}

total_steps = 1000000

# Start command handler to initiate the game
async def start(update, context):
    logging.info(f"Start command received from {update.effective_user.username}")
    # Create buttons for each memecoin
    keyboard = [
        [InlineKeyboardButton("$BONK 🐕", callback_data='bonk')],
        [InlineKeyboardButton("$WEN ⏰", callback_data='wen')],
        [InlineKeyboardButton("$MANEKI 🐱", callback_data='maneki')],
        [InlineKeyboardButton("$POPCAT 😺", callback_data='popcat')],
        [InlineKeyboardButton("$MUMU 🐮", callback_data='mumu')],
        [InlineKeyboardButton("$WOLF 🐺", callback_data='wolf')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Click a memecoin to move it forward!', reply_markup=reply_markup)

# Function to generate the progress chart
def plot_curve():
    labels = list(meme_counters.keys())
    values = list(meme_counters.values())

    plt.figure(figsize=(10, 5))
    plt.plot(labels, values, marker='o', color='green')
    plt.fill_between(labels, values, color='green', alpha=0.2)
    plt.xlabel('Memecoins')
    plt.ylabel('Clicks')
    plt.title('Memecoin Race Progress')
    plt.savefig('meme_race.png')
    plt.close()

# Callback query handler for button clicks (game action)
async def button_click(update, context):
    query = update.callback_query
    logging.info(f"Button clicked: {query.data} by {query.from_user.username}")
    await query.answer()  # Acknowledge the button click
    meme = query.data  # Get the memecoin clicked by the user

    # Increment the counter for the selected memecoin
    meme_counters[meme] += 1
    steps = (meme_counters[meme] / total_steps) * 100  # Calculate percentage progress

    # Generate the updated graph showing progress for all memecoins
    plot_curve()

    # Send the updated graph as a photo to the user
    await query.message.reply_photo(photo=open('meme_race.png', 'rb'))

    # Optionally, show how much the clicked memecoin has progressed
    await query.edit_message_text(f'{meme.upper()} clicked! It has moved {steps:.2f}% on the curve.')

# Main bot function
async def main():
    # Create application with bot token
    application = Application.builder().token('7062758539:AAGeUAMUPlR6yU4Gg9fMrcplTDA01RbGiX0').build()

    # Add command handlers for game interaction
    application.add_handler(CommandHandler('start', start))  # To start the game
    application.add_handler(CallbackQueryHandler(button_click))  # To handle button clicks

    # Start polling to handle commands and callbacks
    await application.run_polling()

# Run the game bot
if __name__ == '__main__':
    try:
        # If an event loop is already running
        asyncio.get_running_loop().run_until_complete(main())
    except RuntimeError:
        # No event loop is running
        asyncio.run(main())
