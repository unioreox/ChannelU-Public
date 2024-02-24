import os
from telegram import Update
from telegram.ext import ApplicationBuilder, filters, CommandHandler, MessageHandler
import GeminiAI

PORT = 8888
BotToken = os.environ.get('BOT_TOKEN')
channels = os.environ.get('CHANNELS').split(",")
AIKey = os.environ.get('AI_KEY')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
WEBHOOK_KEY = os.environ.get('WEBHOOK_KEY')
application = ApplicationBuilder().token(BotToken).build()


async def start_callback(update, context):
    startMessageText = "欢迎使用 UNi频道管理机器人\n"
    startMessageText += "我有以下功能\n"
    startMessageText += "1. 自动为频道原创内容添加标签\n"
    startMessageText += "2. 自动为频道原创内容添加版权\n"
    startMessageText += "3. 更多内容正在发现\n"
    await update.message.reply_text(startMessageText)

async def channelTextPost_callback(update, context):
    #channels is have chatid
    if update.channel_post is not None and str(update.channel_post.chat.id) in channels:
        if update.channel_post.text is not None and update.channel_post.text != "":
            print("Channel Text Post From："+str(update.channel_post.chat.id))
            tags_raw = GeminiAI.callAI(update.channel_post.text, AIKey)
            tags_array = tags_raw.split("||")
            tags_string = ""
            for tag in tags_array:
                tags_string += "#" + tag + " "
            
            
            await update.channel_post.edit_text(update.channel_post.text + "\n\nTAGs:" + tags_string + "\nSource @UNiChannelX by @ChannelU_BOT", 
                                                disable_web_page_preview=True,
                                                entities=update.channel_post.entities)
            
            print("TAGs Added")
        else:
            print("No Text")

        if update.channel_post.caption is not None and update.channel_post.caption != "":
            print("Channel Media Post From："+str(update.channel_post.chat.id))
            tags_raw = GeminiAI.callAI(update.channel_post.caption, AIKey)
            tags_array = tags_raw.split("||")
            tags_string = ""
            for tag in tags_array:
                tags_string += "#" + tag + " "
            
            await update.channel_post.edit_caption(update.channel_post.caption + "\n\nTAGs:" + tags_string + "\nSource @UNiChannelX by @ChannelU_BOT",
                                                caption_entities=update.channel_post.caption_entities)

            print("TAGs Added")
        else:
            print("No Caption")
    else:
        print("Not New Channel Post")    

application.add_handler(CommandHandler("start", start_callback))
application.add_handler(CommandHandler("help", start_callback))
application.add_handler(MessageHandler(filters.ChatType.CHANNEL and ~filters.FORWARDED , channelTextPost_callback))
application.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    secret_token=WEBHOOK_KEY,
    webhook_url=WEBHOOK_URL
)

