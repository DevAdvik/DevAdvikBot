import requests, telebot, os, qrcode
from time import sleep
from telebot.types import InlineKeyboardMarkup as ikm
from telebot.types import InlineKeyboardButton as ikb
from linkshortener import shortener
#from alive import keep_alive (Only to keep the bot alive on Replit Server)

#---ASSIGN VALUES--#
token = os.environ["token"] #Your bot token
shortkey= os.environ["shortio"] #short.io API Key
authorized_users = [1763528606, 1808250692, 1060264505, 1733839967, 1703111890]
shortiourl = "https://api.short.io/links/"

cmds = """All available commands:
• /shorturl - Link shortener
• /shorten - Link shortener on custom domain (Authorized Users)
• /qr - Make QR Codes
• /contact - Contact me
"""

#keep_alive()

bot = telebot.TeleBot(token, parse_mode="HTML")

print("Bot successfully started! Running now...")


@bot.message_handler(commands=["start", "home"])
def start(msg):
	m = msg.chat.id
	bot.send_message(m, "Ciao! I'mma bot that can perform various functions. Hit /cmds for all commands!")


#----LINK SHORTENER ON CUSTOM DOMAIN----#
@bot.message_handler(commands=["shorten"])
def shortio(msg):
	m = msg.chat.id
	if m in authorized_users:
		url = bot.send_message(msg.from_user.id, "Send the URL you wanna shorten or send /cancel to cancel current process:")
		bot.register_next_step_handler(url, shorten)
	else:
		contact = ikm()
		contact.add(ikb("Contact The Dev", url="t.me/advik_143"), ikb("Email", url="https://u.advik.dev/email"))
		bot.send_message(msg.chat.id, "Unauthorized User!", reply_markup=contact)
		
def shorten(msg):
	global longurl
	longurl = msg.text
	if longurl.lower() == "/cancel":
		bot.send_message(msg.chat.id, "Link Shortening cancelled.")
	else:
		domain = ["https://", "http://", "www.", "ww1.", "mailto:"]
		exists = 0
		for starting in domain:
			if longurl.startswith(starting):
				exists =1
		if exists != 1:
			bot.reply_to(msg, "Invalid Link! Are you fcking dumb?")
			sleep(0.8)
			shortio(msg)
		else:
			path = bot.send_message(msg.from_user.id, "Enter shortlink alias or send /skip to skip this")
			bot.register_next_step_handler(path, final)
	
def final(msg):
    alias = msg.text
    if alias.lower() == "/skip":
        data = requests.post("https://api.short.io/links", {
		"domain":"u.advik.dev",
		"originalURL":longurl
		}, headers = {"authorization":shortkey},
		json = True)
        data = data.json()
        shortlink = data['secureShortURL']
        linkid = data['id']
        
        bot.send_message(msg.from_user.id, f"Done! \nThe shortened URL is: {shortlink} \nLink ID: <code>{linkid}</code>", disable_web_page_preview=True)
        
        bot.send_message(1060264505, f"{msg.from_user.first_name} created a link: \nShortlink: {shortlink} \nLink ID: <code>{linkid}</code>", disable_web_page_preview=True)
    else:
        data = requests.post("https://api.short.io/links", {
		"domain":"u.advik.dev",
		"originalURL":longurl,
		"path":alias
		}, headers = {"authorization":shortkey},
		json = True)
        data = data.json()
        shortlink = data['secureShortURL']
        linkid = data['id']
		
        if msg.from_user.id != 1060264505:
            bot.send_message(1060264505, f"{msg.from_user.first_name} created a link: {shortlink}\nLink ID: <code>{linkid}</code>", disable_web_page_preview=True)
            
        bot.send_message(msg.from_user.id, f"Done! \nThe shortened URL is: {shortlink} \nLink ID: <code>{linkid}</code>", disable_web_page_preview=True)


@bot.message_handler(commands=["del", "delete"])
def deleteurl(msg):
	if msg.chat.id == 1060264505:
		getid = bot.send_message(msg.chat.id, "Send the Link ID to delete:")
		bot.register_next_step_handler(getid, deleteid)
		
def deleteid(msg):
	LinkID = str(msg.text)
	deleteheaders = {'authorization': shortkey}
	response = requests.request("DELETE", shortiourl+LinkID, headers=deleteheaders).json()
	
	if "success" in response:
		bot.send_message(msg.chat.id, "Link Deleted Successfully!")
	elif "error" in response:
		reason = response ["error"]
		bot.send_message(msg.chat.id, f"Error Occurred: {reason}")
	else:
		bot.send_message(msg.chat.id, f"Something happened, but idk. Here's the error code: <code>{response}</code>")


#----LINK SHORTENER FOR EVERYONE----#
@bot.message_handler(commands=["shorturl"])
def pysh(msg):
	m = msg.from_user.id
	url = bot.send_message(m, "Send the URL you wanna shorten or send /cancel to cancel current operation:")
	bot.register_next_step_handler(url, create)
	
def create(msg):
	m = msg.chat.id
	longurl = msg.text
	if longurl.lower() == "/cancel":
		bot.send_message(m, "Link Shortening Cancelled!")
	else:
		shorturl = shortener(longurl)
		bot.send_message(m, f"Done!\nShortened URL: {shorturl}", disable_web_page_preview=True)


#----CONTACT COMMAND----#
@bot.message_handler(commands=["contact", "dev"])
def contactme(msg):
	mrkp = ikm()
	mrkp.add(ikb("Email", url="https://u.advik.dev/email"), ikb("Reddit", url="https://u.advik.dev/"))
	mrkp.add(ikb("Source Code", url="https://u.advik.dev/DABot"))
	bot.reply_to(msg, "Yo, I'mma bot made by @advik_143. Hit me up if you have any question or you wanna suggest a new function.", reply_markup=mrkp)


#--ALL COMMANDS--#
@bot.message_handler(commands=["cmds", "commands"])
def commands(msg):
	bot.send_message(msg.chat.id, cmds)



@bot.message_handler(commands=["qr"])
def qrcoded(msg):
 cde = bot.send_message(msg.chat.id, "Send the text you wanna convert to QR Code: \n(Or send /cancel to cancel current operation)")
 bot.register_next_step_handler(cde, texts)
 
def texts(msg):
 raw = msg.text
 if raw.lower()  == "/cancel":
  bot.reply_to(msg, "Cancelled current operation")
 else:
  img = qrcode.make(raw)
  img.save("qrcode.png")
  qr = open("qrcode.png", "rb")
  bot.send_photo(msg.chat.id, qr, caption="Here's the QR Code!")
  qr.close()


while True:
	try:
		bot.polling()
		telebot.apihelper.SESSION_TIME_TO_LIVE = 2000
	except:
		sleep(1)
