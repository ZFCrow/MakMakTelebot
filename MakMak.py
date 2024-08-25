import telebot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import constants
import functions
import os
import random
import urllib
from requests.exceptions import ReadTimeout
#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.triggers.cron import CronTrigger
import time

from keep_alive import keepAlive
keepAlive() 

print ("starting the bot...")

# from transformers import pipeline 
# print ("loading model")
# generator = pipeline(model="microsoft/DialoGPT-medium")
# print ("model loaded")

try:
    print ("initializing bot with environment variable")
    api_key = os.environ.get('MakMakTelegramBotAPIKey')
    bot = telebot.TeleBot(api_key)
except Exception as e: 
    print (f'Error occured: {e}') 
    pass 


conversationState=0

inline_keyboardYesNo = [[InlineKeyboardButton("Yes", callback_data="Yes"),
                    InlineKeyboardButton("No", callback_data="No")]]
reply_markupYesNo = InlineKeyboardMarkup(inline_keyboardYesNo)


inline_keyboardZFCrow = [[InlineKeyboardButton("Message Developer",url=f"tg://user?id={constants.zfchatId}")]]
reply_markupZFCrow=InlineKeyboardMarkup(inline_keyboardZFCrow)






def log(chatId,action):
    chat=bot.get_chat(chatId)
    print(f"{chatId} | {chat.username}| {action}")

def UserAuthorization(chatId):
      if str(chatId) == str(constants.zfchatId) or str(chatId) == str(constants.jqchatid):
          return True
      else:
          return False


#**********************************************************************Command Handling---------------------------------------------------------------------------


@bot.message_handler(commands=['bus'])
def busTiming(message): 
    chatId=message.chat.id
    action='busTiming command'
    log(chatId,action)
    bus = functions.getBusTiming()

    header = f"{'Bus Stop':<20} | {'Bus Number':<8} | Arrival Time" 
    sep = "-"*50
    #! sending it as a table as a string with markdown 
    tabletext = f"```\n{header}\n{sep}"
    for busStopName, arrivalTimeDict in bus.items():
        for busNumber, arrivalTime in arrivalTimeDict.items():
            tabletext += f"\n{busStopName:<20} | {busNumber:<8} | {arrivalTime}" 
    tabletext += "```"


    bot.reply_to(message, tabletext, parse_mode="Markdown") 


#! =====================================================
#! =====================================================
#! =====================================================
@bot.message_handler(commands=['pick'])
def randomPick(message):
    chatId=message.chat.id
    action='randomPick command'
    log(chatId,action)
    #*the first letter after /pick (including the spacing behind, will be starting from 6)
    list=message.text.split(' ')[1:]
    print (list)
    #* converting the msg to a list
    randomChoice = random.choice(list) 
    bot.reply_to(message,randomChoice) 

@bot.message_handler(commands=['rng'])
def randomPick(message):
    chatId=message.chat.id
    action='rng command'
    log(chatId,action)
    #*the first letter after /pick (including the spacing behind, will be starting from 6)
    list=message.text.split()[1:] 
    print (list) 
    try:
        first = int(list[0])
        second = int(list[1])
        randomNumber = random.randint(first, second)
        bot.reply_to(message,randomNumber)
    except:
        bot.reply_to(message,'your input is wrong!')



#TODO UNIQLO SCRAPER!






#**********************************************************************End of Command Handling---------------------------------------------------------------------------
#**********************************************************************Stickers/GIFS/PHOTOS Handling---------------------------------------------------------------------------
#* sticker replyer (literally just echo what sticker the user sent)
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    chatId=message.chat.id
    action='sent a sticker'
    log(chatId,action)
    sticker_id = message.sticker.file_id
    print(f'the sticker id:{sticker_id}')
    bot.send_sticker(message.chat.id,sticker_id)

@bot.message_handler(content_types=['animation', 'gif'])
def handle_sticker(message):
    chatId=message.chat.id
    action='sent a gif/animation'
    log(chatId,action)
    gif_id = message.animation.file_id
    print(f'the sticker id:{gif_id}')
    bot.send_animation(message.chat.id,gif_id)




#**********************************************************************Texts Handling---------------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def handle_text(message):

    chatId=message.chat.id
    action='sent a text'
    log(chatId,action)

    print(f'the text:{message.text}')
    reply_message=''
    try:
        conversation = [
                            {"role": "user", "content": message.text}
                        ]    
        responses = generator(conversation) 
        bot.reply_to(message, responses[0]['generated_text'][1]['content'])

        
    except:
        bot.reply_to(message,'sorry babe unable to chat now!')
#***************************************************************************************************************************************************************************************








#!==============================================================================Schedule tasks doesnt work for pythonanywhere ======================================
# #* scheduledTasks
# def scheduledsuggestedDates(bot):
#     try:

#         # Read the file into a DataFrame
#         df = pd.read_csv('suggesteddates.csv')
#         print(len(df))
#         print(f'DF empty: {df.empty}')

#         if df.empty:
#             print('file has no updates today!')
#             return

#         csvFile = open('suggesteddates.csv', 'r')
#         bot.send_message(constants.zfchatId,'dates suggested by users, do note that this file will be deleted from the server after it is sent')
#         bot.send_document(constants.zfchatId, csvFile)


#         # retrieve just the headers and overwrite the existed suggestedDates file, u dw to keep those data after u alr sent it to me
#         headers = list(df.columns)
#         df_headers = pd.DataFrame(columns=headers)
#         df_headers.to_csv('suggesteddates.csv', index=False)

#     except Exception as e:
#         print(e)
#         pass


# def alarmMakMak(bot):
#     for i in range(3):
#         bot.send_message(constants.jqchatid,'its 830am!')

# scheulder = BackgroundScheduler()
# scheulder.add_job(scheduledsuggestedDates, CronTrigger(hour=15, minute=36),args=[bot])
# scheulder.add_job(alarmMakMak, CronTrigger(hour=8, minute=30),args=[bot])
# #scheulder.start()



# scheduledsuggestedDates(bot)

#!==============================================================================Schedule tasks doesnt work for pythonanywhere ======================================

#!=================Depricated Functions that are not used anymore======================= 
# @bot.message_handler(commands=['addDates'])
# def datesAdder(message):
#     chatId=message.chat.id
#     action='datesAdder command'
#     log(chatId,action)

#     #authorize = False
#     authorize = UserAuthorization(chatId)
#     response=functions.DataAdder(message.text,authorize)
#     if authorize:
#         bot.reply_to(message,f'{response}{constants.kissingFaceWithSmilingEyes}' )
#     else:

#         bot.reply_to(message,'you aint authorized to add dates to the file, thus it will be added to the suggestion pile for developer to consider',reply_markup=reply_markupZFCrow)


# @bot.message_handler(commands=['randomdates'])
# def datesAdder(message):
#     chatId=message.chat.id
#     action='randomDates command'
#     log(chatId,action)

#     response=functions.RandomDates()
#     if response!='You didnt store any dates in me beforehand to tell you!':
#         bot.reply_to(message,'let me think let me think')
#         bot.reply_to(message,'hmmmm hmmm')
#         bot.reply_to(message,f'what about {response}? {constants.kissingFaceWithClosedEyes}' )
#     else:
#         bot.reply_to(message,response )


# @bot.message_handler(commands=['sendphoto'])
# def send_photo(message):
#     chatId=message.chat.id
#     action='photo command'
#     log(chatId,action)
#     try:

#         authorize = UserAuthorization(chatId)
#         if authorize:
#             files=os.listdir('photos')

#             #* filepath to be opened in sendphoto
#             photo=f'photos/{random.choice(files)}'
#             bot.send_photo(chat_id=message.chat.id, photo=open(photo,'rb'))

#         else:
#              bot.reply_to(message,'you aint authorized to use this function, text the developer to get access.',reply_markup=reply_markupZFCrow)
#     except Exception as e:
#         print(e)

#         bot.reply_to(message,'sorry babe function not avail now')

# @bot.message_handler(commands=['sendvideo'])
# def send_video(message):
#     chatId=message.chat.id
#     action='video command'
#     log(chatId,action)
#     try:
#         authorize = UserAuthorization(chatId)
#         if authorize:
#             files=os.listdir('videos')

#             #* filepath to be opened in sendphoto
#             video=f'videos/{random.choice(files)}'
#             bot.send_video(chat_id=message.chat.id, video=open(video,'rb'))

#         else:
#              bot.reply_to(message,'you aint authorized to use this function, text the developer to get access.',reply_markup=reply_markupZFCrow)

#     except:
#         bot.reply_to(message,'sorry babe function not avail now')


#! the site originally use for quotes has some bot protection, thus i cant use it anymore 
# @bot.message_handler(commands=['quote'])
# def send_quote(message):
#     chatId=message.chat.id
#     action='quote command'
#     log(chatId,action)

#     quote=functions.randomQuote()
#     print(quote)

#     bot.reply_to(message, quote)

#! pytube is buggy after the update, thus i cant use it anymore

# @bot.message_handler(commands=['yt'])
# def youtubeDownloader(message):
#     chatId=message.chat.id
#     action='youtubeDownloader command'
#     log(chatId,action)
#     bot.reply_to(message,'sorry babe function not avail now')


#! media handlers that i am not using now since i am not storing photos or videos in the server anymore     
# @bot.message_handler(content_types=["photo"])
# def handle_photo(message):
    
#     chatId=message.chat.id
#     action='sent a photo'
#     log(chatId,action)

#     authorize = UserAuthorization(chatId)
#     if authorize:
#         photoid=message.photo[-1].file_id
#         fileinfo=bot.get_file(photoid)
#         downloadedfile=bot.download_file(fileinfo.file_path)
#         # Save the downloaded photo to your local machine
#         filename=functions.get_unique_filename('photos','downloadedpic.jpg')

#         with open(f'photos/{filename}', "wb") as f:
#             f.write(downloadedfile)
#         bot.reply_to(message, "Photo saved to Server")
#     else:
#         bot.reply_to(message,'you aint authorized to save the photo to the server, do text developer to gain access',reply_markup=reply_markupZFCrow)




# @bot.message_handler(content_types=['video'])
# def handle_video(message):

#     chatId=message.chat.id
#     action='sent a video'
#     log(chatId,action)


#     authorize = UserAuthorization(chatId)
#     if authorize:
#         video_id = message.video.file_id
#         video_file = bot.get_file(video_id)
#         video_path = video_file.file_path
#         video_url = f'https://api.telegram.org/file/bot{bot.token}/{video_path}'
#         video_name = f'videos/{message.chat.id}_{video_id}.mp4'

#         # Download the video
#         urllib.request.urlretrieve(video_url, video_name)

#         # Send a message to the user
#         bot.reply_to(message, f'Thank you for the video! It has been saved as {video_name}.')
#     else:
#         bot.reply_to(message,'you aint authorized to save the video to the server, do text developer to gain access',reply_markup=reply_markupZFCrow)

#! ============================================================================================================== 



def startPolling():
    while True:
        try:
            bot.polling(none_stop=True,timeout=60)
        except ReadTimeout: 
            print ('ReadTimeout occured, retrying...') 
            continue
        except Exception as e: 
            print (f'Error occured: {e}') 
            time.sleep(5) 
            continue 



if __name__ == '__main__': 
    startPolling()