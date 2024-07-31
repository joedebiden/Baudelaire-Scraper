import logging
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from setup import banner

#TO DO : patch the use of /invite command in mp cause it broke the bot, 
# command of bot only work in group chat & mp but not in channel
# carefull with the use of /invite command in mp, need to respect tos (to check)
# security breach with the use of /invite command in group, to be able only use by admin 

load_dotenv()
TOKEN = os.getenv('TOKEN')


# ==== section logging ==== > voir docs 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
banner()
print("Bot is running...\n")



# ==== fonction réponse /start ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="To use the bot properly type /help"
        )

# ==== fonction réponse /help ====
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "Here are the commands you can use:\n"
        "/help - Get help\n"
        "/my_info - Get your information\n"
        "/invite - Invite users to a group chat\n"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=help_message
    )


''' fonction inutile -> abandonnée
# ==== fonction echo renvoi le message ====
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
        )


 fonction inutile -> abandonnée
# ==== fonction réponse /caps ====
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_caps
        )
'''

# ==== fonction info user ====
async def my_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if update.effective_chat.type == 'private':
        info = (
            f"Votre ID : {user.id}\n"
            f"Nom d'utilisateur : {user.username}\n"
            f"Nom complet : {user.full_name}\n"
            f"Langue : {user.language_code}"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=info
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Cette commande est uniquement disponible en message privé."
        )

# ==== fonction send message invite ====
async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        link = context.args[0]

        # création des boutons inline avec le lien d'invitation
        keyboard = [[InlineKeyboardButton("Join this", url=link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # envoi du message avec le lien d'invitation
        chat_members = await context.bot.get_chat_administrators(update.effective_chat.id)
        for member in chat_members:
            try: 
                await context.bot.send_message(
                    chat_id=member.user.id,
                    text="Join this group is 200""%"" better",
                    reply_markup=reply_markup
                )
            except Exception as e:
                logger.error(f"error while sending messages to {member.user.id}: {e}")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide a link to the group"
        )




if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ==== section handler ====
    start_handler = CommandHandler('start', start) 
    help_handler = CommandHandler('help', help) 
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #caps_handler = CommandHandler('caps', caps)
    my_info_handler = CommandHandler('my_info', my_info)
    invite_handler = CommandHandler('invite', invite)




    # ==== section application add handler ====
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    #application.add_handler(echo_handler)
    #application.add_handler(caps_handler)
    application.add_handler(my_info_handler)
    application.add_handler(invite_handler)

    


    application.run_polling()
    
