import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    filters
)

# Placeholder for your TON wallet address and support username
TON_WALLET_ADDRESS = "YOUR_TON_WALLET_ADDRESS"
SUPPORT_USERNAME = "@binary114"  # Replace with your actual support username

# States for conversation flow
ENTER_STARS, ENTER_WALLET = range(2)

def initialize_db():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            num_stars INTEGER NOT NULL,
            price REAL NOT NULL,
            user_wallet TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"Hello {user.username}! 😊\n"
        "Welcome to the Telegram Stars Shop!\n"
        "Please enter the number of stars you want to buy (minimum 50):"
    )
    return ENTER_STARS

async def enter_stars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    try:
        num_stars = int(update.message.text)
        if num_stars < 50:
            await update.message.reply_text("The minimum number of stars you can buy is 50. Please enter a valid number:")
            return ENTER_STARS

        price = num_stars * 0.003
        context.user_data['num_stars'] = num_stars
        context.user_data['price'] = price

        await update.message.reply_text(
            f"👤 Account: @{user.username}\n"
            f"🌟 You want to buy: {num_stars} stars\n"
            f"💰 Total price: {price:.3f} TON\n"
            f"📥 Please send the TON to this wallet: `{TON_WALLET_ADDRESS}`\n\n"
            "After making the payment, reply with the TON wallet address you used for the payment."
        )
        return ENTER_WALLET
    except ValueError:
        await update.message.reply_text("Please enter a valid number:")
        return ENTER_STARS

async def enter_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_wallet = update.message.text
    username = update.message.from_user.username
    num_stars = context.user_data['num_stars']
    price = context.user_data['price']

    # Save to SQLite
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (username, num_stars, price, user_wallet)
        VALUES (?, ?, ?, ?)
    """, (username, num_stars, price, user_wallet))
    conn.commit()
    conn.close()

    # Creating an inline keyboard with additional "Support" button
    keyboard = [
        [InlineKeyboardButton("Buy More Stars", callback_data='buy_more')],
        [InlineKeyboardButton("Cancel", callback_data='cancel')],
        [InlineKeyboardButton("Support", url=f"tg://user?id={SUPPORT_USERNAME[1:]}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Thank you for your payment! 😊\n"
        "We will verify your transaction and send your stars shortly.\n"
        "If you need assistance, please use the Support button below.\n\n"
        "If you have any issues, please contact support.",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

# Handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy_more':
        # Restart the bot by sending the /start command
        await query.edit_message_text("Restarting the process. Please wait...")
        # Send the start command to restart the flow
        await query.bot.send_message(chat_id=query.message.chat_id, text="/start")
        return ENTER_STARS
    elif query.data == 'cancel':
        await query.edit_message_text("Transaction canceled. Type /start to begin again.")
        return ConversationHandler.END

def main():
    initialize_db()
    app = ApplicationBuilder().token("7948474464:AAG1qeDeKFY_NGffDks5baAWIrhvZwlBUbM").build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTER_STARS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_stars)],
            ENTER_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_wallet)],
        },
        fallbacks=[]
    )

    # Add the button handler
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == '__main__':
    main()
