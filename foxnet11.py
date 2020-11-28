import logging
import os
import time
os.system("color 2")

from telegram.ext import *
from telegram import *




# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def validateConfig():
	start = input(">>")

	if start == "run":	

		if os.path.exists("constants_beta.txt"):
			global TOKEN
			global INV
			global chat_name
			f = open("constants_beta.txt", "r")
			rawtoken = f.readline()
			rawinv = f.readline()
			chat_name = f.readline()
			TOKEN = rawtoken.rstrip()
			INV = rawinv.rstrip()

			f.close()
			main()
			return True
			
		else:
			new_config_file()
			return False

	elif start == "help":
		start_help_menu()

	elif  start == "quit":
		return

	elif start == "new":
		new_config_file()
		return False

	else:
		print(start + " is not a valid command.")
		validateConfig()
		return False

def start_help_menu():
	print("""
FoxxNet 1.1 Help

Commands:
"run"- Starts FoxxNet. Will prompt to create new configuration file if first run.
"help"- Opens this menu.
"quit"- Closes FoxxNet, only valid before server connection.
"new"- Creates new configuration file.

Once FoxxNet connects with Telegram's API, press 'ctrl+c' in order to terminate connection.

In order to change the group URL or Name, please communicate with your bot using the /help command in your
group. 
		""")
	validateConfig()
	return False	
			

def new_config_file():
	global TOKEN
	global INV
	global chat_name
	print("Configuration file not found. Please input data below:")
	api_key = input("API Key:>")
	chat_url = input("Chat URL:>")
	chat_name = input("Target Chat Name:>")
	
	f = open("constants_beta.txt", "w+")
	f.write('%s\n%s\n%s' % (api_key, chat_url, chat_name))
	f.close()
	print("Config File Created. Now Connecting FoxxNet to Telegram's API")
	TOKEN = api_key.rstrip()
	INV = chat_url.rstrip()
	main()
	return True


#checks if the person sending the command is an administrator
def check(update, context):
	global admins
	global user

	chat_id = update.message.chat_id
	chat_obj = update.effective_chat
	admins = chat_obj.get_administrators()
	admins = [x.user.name for x in admins]
	
	user = update.message.from_user.name

def help_menu(update, context):
	global admins
	global user
	global chat_id

	check(update, context)

	help_keyboard = [
		[InlineKeyboardButton("Command List", callback_data = '2')],
		[InlineKeyboardButton("About", callback_data = '3')]
	]

	if user in admins:
		
		chat_id = update.message.chat_id
		reply_markup = InlineKeyboardMarkup(help_keyboard)

		update.message.reply_text("Please select an option:", reply_markup = reply_markup)

	else:

		update.message.reply_text('Only Administrators can communicate with FoxxNet')




def tiny_kicks(update, context):
	global admins
	global user
	
	chat_id = update.message.chat_id
	reply_to = update.message.reply_to_message

	check(update, context)

	if user in admins:
		
		if reply_to == None:
			update.message.reply_text('Please reply to the Member you wish to kick.')

		else:	
						
			reply_user = reply_to.from_user
			chat_obj = update.effective_chat

			chat_obj.kick_member(reply_user.id)
			update.message.reply_text(reply_user.id + " has been removed from the chat.")

	else:
		update.message.reply_text('Only Administrators can communicate with FoxxNet')

def keyboard_test(update, context):
	global admins
	global user
	global INV
	global chat_name

	INV = INV.rstrip()
	check(update, context)

	keyboard = [
		[InlineKeyboardButton("Join " + chat_name, url = INV)],
		[InlineKeyboardButton("Delete Message", callback_data = '1')]
	]


	if user in admins:
		global mid
		global chat_id
		

		chat_id = update.message.chat_id
		reply_markup = InlineKeyboardMarkup(keyboard)
		res = update.message.reply_text('Please click the button below to join ' + chat_name, reply_markup=reply_markup)
		res
		mid = (res['message_id'])


	else:
		update.message.reply_text('Only Administrators can communicate with FoxxNet')

def button(update, context):
	global mid
	global chat_id
	global TOKEN
	

	TOKEN = TOKEN.rstrip()
	query = update.callback_query
	bot = Bot(TOKEN)

	query.answer()
	#delete the message with the invite link
	if query.data == '1':
		bot.deleteMessage(chat_id, mid)

	if query.data == '2':
		query.edit_message_text(text = "Command List: /ok sends invite link. /kick removes replied user from group.")

	if query.data == '3':
		query.edit_message_text(text = "FoxxNet Version 1.1 (c)2020. Created by Robert Aruvali.")


	else:
		return

def main():
	global TOKEN
	TOKEN = TOKEN.rstrip()
	
	try:
		updater = Updater(TOKEN, use_context=True)

		# Get the dispatcher to register handlers
		dp = updater.dispatcher

		# on different commands - answer in Telegram
		dp.add_handler(CommandHandler("ok", keyboard_test))
		dp.add_handler(CommandHandler("kick", tiny_kicks))
		dp.add_handler(CommandHandler("yeet", tiny_kicks))
		dp.add_handler(CallbackQueryHandler(button))
		dp.add_handler(CommandHandler("help", help_menu))

		updater.start_polling()

		updater.idle()
	except:
		print("An unknown error has occoured.")
		validateConfig()
		return False

print("""
8888888888                         888b    888          888   
888                                8888b   888          888   
888                                88888b  888          888   
8888888  .d88b.  888  888 888  888 888Y88b 888  .d88b.  888888
888     d88""88b `Y8bd8P' `Y8bd8P' 888 Y88b888 d8P  Y8b 888   
888     888  888   X88K     X88K   888  Y88888 88888888 888   
888     Y88..88P .d8""8b. .d8""8b. 888   Y8888 Y8b.     Y88b. 
888      "Y88P"  888  888 888  888 888    Y888  "Y8888   "Y888

Version 1.1
(c)2020 
""")


if __name__ == '__main__':
	if validateConfig():
		main()

'''
FoxxNet
(c)2020 Robert Aruvali
Release Dates:
1.0: 10/23/2020
1.1: 11/13/2020
'''
