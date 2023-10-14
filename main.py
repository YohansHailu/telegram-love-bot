# say hello when its click /start on telegram bot using python module
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Application, MessageHandler, filters
import random

Token = "6679054737:AAFM6nRQX9awCu2FnLGQv0X3BS02aOUjVH4"
botUsername = "@pefectmatchfinderbot"
joId = "689754386"

Questions = [
    "*Question 1*, On a scale of 1 to 15, How important is communication and emotional intelligence in a life partner?\n\n"
    "1: Not important\n"
    "15: Extremely important",

    "*Question 2*, On a scale of 1 to 15, How much do you value shared values and longterm goals in a relationship?\n\n"
    "1: Not important\n"
    "15: Extremely important",

    "*Question 3*, On a scale of 1 to 15, How important is physical attraction and compatibility in a life partner?\n\n"
    "1: Not important\n"
    "15: Extremely important",

    "*Final Question*\n\n"
    "Please provide me with a list of individuals whom you believe could be potential matches, in one line and make sure to separate them using space"

]

Answers = []
print("started...")
async def start_command(update , context):
    user_id = update.message.from_user.id
    print("I got the id ", user_id)
    await update.message.reply_text(f"Hello{update.message.from_user.first_name}, Welcome to Love Bot")
    await update.message.reply_text('I will ask you 3 questions and you have to answer them')

    Answers.clear()
    await update.message.reply_text('Lets start')

    await update.message.reply_text(Questions[0], parse_mode='MarkdownV2')

async def matchme_command(update , context):

    print("start command")
    await update.message.reply_text('Hello, Wellcome to Love Bot')
    await update.message.reply_text('I will ask you 3 questions and you have to answer them')

    Answers.clear()
    await update.message.reply_text('Lets start')

    await update.message.reply_text(Questions[0], parse_mode='MarkdownV2')
# add message handler
async def messageHandler(update, context):
    

    text = update.message.text
    # if text is not a number between 1 to 15 then ask again and say it should be 1 to 5
    if len(Answers) < len(Questions) - 1:
        if not text.isdigit() or int(text) < 1 or int(text) > 15:
            await update.message.reply_text("Please enter a number between 1 to 15")
            return

    if len(Answers) == len(Questions) - 1:
        # check if all the names are valid
        names = text.strip().split()
        for name in names:
            if not name.strip() or len(name.strip()) < 3 or len(name.strip()) > 20 or name.strip().isdigit():
                await update.message.reply_text("Please enter a valid names, " + name, " is not valid")
                return

    ## write text and all the details like time and user name to text file
    Answers.append(text)
    if len(Answers) < len(Questions):
        await update.message.reply_text("great, next question")
        await update.message.reply_text(Questions[len(Answers)], parse_mode='MarkdownV2')
    else:
        await update.message.reply_text("We are done")
        # await update.message.reply_text("Your answers are" +" " + " ".join(Answers[:-1]))
        
        names = Answers[-1].strip().split()
        # pick random one from the list
        await update.message.reply_text("--------------------------------------------------------")
        # await update.message.reply_text("\#Your match is " + random.choice(names), parse_mode='MarkdownV2')
        await update.message.reply_text("--------------------------------------------------------")


        await update.message.reply_text("type /matchme if what want to get matched again")


        Answers.clear()

    await context.bot.send_message(chat_id=joId, text= update.message.from_user.first_name + " Answers: " + " \n " + "\n".join(Answers))

async def help_command(update , context):
    help_text = '''
    *Available commands:*
    /start  Start the bot and matching you
    /matchme start matching you 
    /help  Show available commands and usage
    '''


    await update.message.reply_text(help_text)

async def error(update, context):
    print(f"Update {update} caused error {context.error}")
    # replay and start over the bot

    await update.message.reply_text("\#\# Error\n\n*Sorry, it's not you, it's me\. Let's start again\!* 💥💔", parse_mode='MarkdownV2')
    Answers.clear()
    await update.message.reply_text(Questions[0])

app = Application.builder().token(Token).build()
app.add_handler(CommandHandler('start', start_command))
app.add_handler(CommandHandler('matchme', matchme_command))
app.add_handler(MessageHandler(filters.TEXT ,messageHandler))
app.add_error_handler(error)

print("polling...")
app.run_polling(poll_interval=1)

