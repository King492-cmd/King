import logging
import threading
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Poll,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    PollAnswerHandler,
    CallbackContext,
)

# --- Logging Setup ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(lev>

# --- Bot Token Add karo ---
 

# --- Sample Class 12 Questions Structure ---
QUESTIONS = {
    "excel question": {
          "Basic": [
    {
        "question": "1. Excel में Array Formula क्या होता है?",
        "options": [
            "(A) एक फॉर्मूला जो कई सेल्स पर एक साथ काम करता है",
            "(B) केवल एक सेल के लिए फॉर्मूला",
            "(C) डेटा जोड़ने का तरीका",
            "(D) केवल टेक्स्ट के लिए फॉर्मूला"
        ],
        "correct_option": 0
    },
    
    # --- Add Questions 9999+ add kar sakte ho ---
    
 }
}
# --- User Data Storage ---
user_data = {}
poll_id_to_user = {}

# --- /start command handler ---
def send_welcome(update: Update, context: CallbackContext):
    user = update.effective_user
    name = user.first_name or "User"
    user_id = str(user.id)
    username = user.username or "N/A"

    try:
        with open("users.txt", "r") as f:                                                                                         users = f.read().splitlines()
    except FileNotFoundError:
        users = []

    if not any(line.startswith(user_id + ",") for line in users):
        with open("users.txt", "a") as f:                                                                                         f.write(f"{user_id},{username},{name}\n")

    welcome_text = (
        f"👋 Welcome, {name}!\n\n"
        "📖 Class 12 Subjects: Hindi, English, Math, Science, Physics, Chemistry, etc.\n"
        "🕗 Time: <b>8 AM to 10 AM daily</b>\n\n"
        "👇 Tap below to start the quiz:"
    )
    keyboard = [[InlineKeyboardButton("🚀 Start Quiz", callback_data="start_quiz")]]                                      update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- Handle button presses ---
def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    data = query.data

    if data == "start_quiz":                                                                                                  keyboard = [[InlineKeyboardButton(sub, callback_data=f"subject:{sub}")] for sub in QUESTIONS]
        query.edit_message_text("📚 Choose your subject:", reply_markup=InlineKeyboardMarkup(keyboard))               
    elif data.startswith("subject:"):
        subject = data.split(":")[1]
        user_data[user_id] = {"subject": subject}
        keyboard = [
            [InlineKeyboardButton("🔹 Basic", callback_data="level:Basic")],
            [InlineKeyboardButton("🟡 Medium", callback_data="level:Medium")],
            [InlineKeyboardButton("🔴 Advanced", callback_data="level:Advanced")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_quiz")]
        ]
        query.edit_message_text(f"📘 {subject} ke liye level choose karo:", reply_markup=InlineKeyboardMarkup(keyboar>

    elif data.startswith("level:"):
        level = data.split(":")[1]
        subject = user_data[user_id]["subject"]
        questions = QUESTIONS.get(subject, {}).get(level, [])

        if not questions:
            query.edit_message_text("❌ No questions available for this level yet.")
            return
 user_data[user_id].update({
            "level": level,
            "q_index": 0,
            "questions": questions,
            "correct_count": 0,
            "wrong_count": 0,
            "timeout_count": 0
        })

        send_next_question(context, query.message.chat_id, user_id)

# --- Send quiz question ---
def send_next_question(context: CallbackContext, chat_id, user_id):
    q_data = user_data.get(user_id)
    if not q_data:
        return

    q_list = q_data["questions"]
    index = q_data["q_index"]

    if index >= len(q_list):
        send_quiz_result(context, chat_id, q_data)
        return

    question = q_list[index]
    message = context.bot.send_poll(
        chat_id=chat_id,
        question=f"Question {index + 1}/{len(q_list)}:\n{question['question']}",
        options=question["options"],
        type=Poll.QUIZ,
        correct_option_id=question["correct_option"],
        is_anonymous=False,
        open_period=30
    )

    q_data["q_index"] += 1
    poll_id_to_user[message.poll.id] = user_id

    # Auto-send next question after 18 sec
    threading.Timer(30, send_next_question, args=(context, chat_id, user_id)).start()

# --- Handle poll answer ---
def receive_poll_answer(update: Update, context: CallbackContext):
    answer = update.poll_answer
    poll_id = answer.poll_id
    user_id = poll_id_to_user.get(poll_id)

    if user_id is None:
        return

    q_data = user_data.get(user_id)
    index = q_data["q_index"] - 1
    correct_option = q_data["questions"][index]["correct_option"]

    if not answer.option_ids:
        q_data["timeout_count"] += 1
    elif answer.option_ids[0] == correct_option:
        q_data["correct_count"] += 1
    else:
        q_data["wrong_count"] += 1
# --- Show result ---
def send_quiz_result(context: CallbackContext, chat_id, q_data):
    correct = q_data.get("correct_count", 0)
    wrong = q_data.get("wrong_count", 0)
    timeout = q_data.get("timeout_count", 0)
    subject = q_data.get("subject")

    status = "✅ पास" if correct >= 1 else "❌ फेल"

    result_msg = (
        f"🎯 <b>Quiz समाप्त!</b>\n\n"
        f"✅ सही उत्तर: <b>{correct}</b>\n"
        f"❌ गलत उत्तर: <b>{wrong}</b>\n"
        f"⏱️ टाइम आउट: <b>{timeout}</b>\n"
        f"🏁 परिणाम: <b>{status}</b>"
    )
    context.bot.send_message(chat_id=chat_id, text=result_msg, parse_mode="HTML")

    # Show level menu again
    keyboard = [
        [InlineKeyboardButton("🔹 Basic", callback_data="level:Basic")],
        [InlineKeyboardButton("🟡 Medium", callback_data="level:Medium")],
        [InlineKeyboardButton("🔴 Advanced", callback_data="level:Advanced")],
        [InlineKeyboardButton("🔙 Back", callback_data="start_quiz")]
    ]
    context.bot.send_message(chat_id=chat_id, text=f"📘 {subject} ke liye level choose karo:", reply_markup=InlineKey>

# --- Main function ---
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", send_welcome))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    dp.add_handler(PollAnswerHandler(receive_poll_answer))

    print("🚀 Bot is running...")
    updater.start_polling()
    updater.idle()

# --- Run ---
if __name__ == "__main__":
    main()
# --- Script Write By MK King ---
