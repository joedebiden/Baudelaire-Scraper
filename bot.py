import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from setup import banner

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
        text="Bienvenue, je suis le bot de la FemratAgency, choisissez une action."
        )
    
# ==== fonction echo renvoi le message ====
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
        )


# ==== fonction réponse /caps ====
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_caps
        )

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

# ==== fonction pour rejoindre un channel ou groupe ====
async def join_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        group_id = context.args[0]
        try:
            await context.bot.join_chat(chat_id=group_id)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Bot a rejoint le groupe/canal avec ID {group_id}."
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Erreur en rejoignant le groupe/canal : {e}"
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Veuillez fournir un ID de groupe/canal après la commande."
        )



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ==== section handler ====
    start_handler = CommandHandler('start', start)  
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    my_info_handler = CommandHandler('my_info', my_info)
    join_group_handler = CommandHandler('join_group', join_group)



    # ==== section application add handler ====
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(my_info_handler)
    application.add_handler(join_group_handler)

    


    application.run_polling()
    
