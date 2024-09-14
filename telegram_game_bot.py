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

# Start command handler
async def start(update, context):
    logging.info("Start command received")
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
    # Use await to properly call the async method
    await update.message.reply_text('Click a memecoin to move it forward!', reply_markup=reply_markup)

# Generate the progress chart
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

# Callback query handler for button clicks
async def button_click(update, context):
    query = update.callback_query
    await query.answer()  # Await the asynchronous callback query answer
    meme = query.data  # Get the meme coin that was clicked

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
def main():
    # Create application with bot token
    application = Application.builder().token('7062758539:AAGeUAMUPlR6yU4Gg9fMrcplTDA01RbGiX0').build()

    # Add command handlers directly to the application
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))

    # Start polling to handle commands and callbacks
    application.run_polling()

# Run the main function
if __name__ == '__main__':
    main()

# Run the main function depending on whether an event loop is already running
if __name__ == '__main__':
    try:
        # If an event loop is already running, we directly await the main function
        asyncio.get_running_loop().run_until_complete(main())
    except RuntimeError:  # No event loop is running
        asyncio.run(main())
