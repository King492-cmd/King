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

# --- Bot Token ---
# --- TOKEN = "7037066343:AAGUozQAv3PGePUYPtsVMdhDvG6eYaoplmM" ---

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

            
