import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from setup import banner


#a faire un mp sender (lien tg modifiable), un message bouton avec le lien du canal tg (lien modifiable)
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
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="/join_group" + "\n" + "/my_info" + "\n")


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



# ==== fonction pour rejoindre un channel ou groupe ====
async def join_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        group_id = context.args[0]
        try:
            
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


# ==== fonction pour vérifier l'appartenance du bot ====
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        group_id = context.args[0]
        try:
            chat_member = await context.bot.get_chat_member(group_id, context.bot.id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Le bot est déjà membre du groupe/canal avec ID {group_id}."
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Le bot n'est pas membre du groupe/canal avec ID {group_id}."
                )
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Erreur en vérifiant le groupe/canal : {e}"
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
    help_handler = CommandHandler('help', help) 
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #caps_handler = CommandHandler('caps', caps)
    my_info_handler = CommandHandler('my_info', my_info)
    join_group_handler = CommandHandler('join_group', join_group)
    check_handler = CommandHandler('check', check)




    # ==== section application add handler ====
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    #application.add_handler(echo_handler)
    #application.add_handler(caps_handler)
    application.add_handler(my_info_handler)
    application.add_handler(join_group_handler)
    application.add_handler(check_handler)

    


    application.run_polling()
    
