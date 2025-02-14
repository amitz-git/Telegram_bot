from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# Replace with your own bot token from BotFather
TOKEN = '7732801366:AAHJDr4liOx_lZWD7iPrzT45qfTWvNjDta8'

# Dictionary to keep track of active timers
active_timers = {}

def format_time(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    # Format with leading zeros
    hours = f"{hours:02}"
    minutes = f"{minutes:02}"
    seconds = f"{seconds:02}"
    
    # Build the time string
    if days > 0:
        return f"{days} day, {hours}:{minutes}:{seconds}"
    else:
        return f"{hours}:{minutes}:{seconds}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I can help you with multiple countdown timers.\n"
        "Use /timer <seconds> to start the countdown.\n"
        "Use /stop to stop your active countdown."
    )

async def countdown(user_id, message, total_seconds, context):
    try:
        while total_seconds > 0:
            await asyncio.sleep(1)  # Update every 1 seconds
            total_seconds -= 1
            if total_seconds < 0:
                total_seconds = 0
            
            try:
                await message.edit_text(f"{format_time(total_seconds)} remaining...")
            except Exception as e:
                print(f"Error updating message: {e}")

        await context.bot.send_message(chat_id=message.chat_id, text="⏰ Time's up!")

    except asyncio.CancelledError:
        await context.bot.send_message(chat_id=message.chat_id, text="⏹ Timer stopped.")
    finally:
        # Clean up the user's timer from active timers
        if user_id in active_timers:
            del active_timers[user_id]

async def timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Check if the user already has an active timer
    if user_id in active_timers:
        await update.message.reply_text("You already have a timer running! Use /stop to cancel it first.")
        return
    
    try:
        # Get the time in seconds from the command argument
        total_seconds = int(context.args[0])
        if total_seconds <= 0:
            await update.message.reply_text("Please enter a positive number of seconds.")
            return
        
        await update.message.reply_text(f"Countdown started for {format_time(total_seconds)}!")

        # Countdown logic
        message = await update.message.reply_text(f"{format_time(total_seconds)} remaining...")

        # Store the task to track active timers
        task = asyncio.create_task(countdown(user_id, message, total_seconds, context))
        active_timers[user_id] = task

    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /timer <seconds>")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # Check if the user has an active timer
    if user_id in active_timers:
        # Cancel the task
        active_timers[user_id].cancel()
        del active_timers[user_id]
        await update.message.reply_text("⏹ Timer stopped.")
    else:
        await update.message.reply_text("You don't have any active timers.")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(CommandHandler("stop", stop))

    application.run_polling()

if __name__ == '__main__':
    main()

