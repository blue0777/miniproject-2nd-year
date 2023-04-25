import asyncio
from Setup import guu
import openai
from pyrogram import filters, Client
from textblob import TextBlob
import pymongo

# Set up MongoDB client and database
client = pymongo.MongoClient("mongodb+srv://cosmic:Soham3112@feed.gmzicww.mongodb.net/?retryWrites=true&w=majority")
db = client["feedback_collection"]
feedback_collection = db["Feedback"]

Soham = Client(name="OpenaiBot",api_id=guu.api_id,api_hash=guu.api_hash)

async def ai(query):
    openai.api_key = guu.openai_api_key
    completion = openai.Completion.create(engine=guu.model, prompt=query, max_tokens=guu.mxtoken, n=1, stop=None,temperature=0.7)
    result = completion.choices[0].text
    return result

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

@Soham.on_message(filters.command("feedback") & ~filters.group)
async def feedback_handler(bot, msg):
    feedback = msg.text.replace("/feedback ", "")

    user_id = msg.from_user.id
    username = msg.from_user.username

    feedback_collection.insert_one({
        "user_id": user_id,
        "username": username,
        "feedback": feedback
    })

    await bot.send_message(
        chat_id=user_id,
        text="Thank you for your feedback! We appreciate your response 🙂."
    )


@Soham.on_message(filters.command("start") & ~filters.group)
async def main(bot,msg):
    newbie = msg.from_user.id
    await bot.send_message(newbie, "" '👋 Hello ''!\n\n'
                    'My name is Hinata Hyuga. \n'
                    'And I am a telegram AI based chat-bot \n\n'
                    'Belongs to OpenAIs GPT-3 family \n'
                    'Im here to help answer any questions you may have about a variety of topics.\n'
                    'Feel free to ask me anything! ☺️\n\n'
                    'MADE BY : Bluecake  \n'
                    'Git-Hub Profile : https://github.com/blue0777\n'
                    'Git-Hub Reposotory : http://github.com/blue0777/TG-ChatGPT-Bot\n'
                    'Please leave your feedback @cosmic_89_bot')
    DEL = await msg.reply(f"Typing🤔.......")
    await asyncio.sleep(3)
    await DEL.delete(10)

@Soham.on_message(filters.text & ~filters.group)
async def main(bot, msg):
    newbie = msg.from_user.id
    ques = msg.text
    sentiment_score = get_sentiment(ques)
    if sentiment_score < -0.5:
        expression = "😔"
    elif sentiment_score < 0:
        expression = "😕"
    elif sentiment_score == 0:
        expression = "😐"
    elif sentiment_score < 0.5:
        expression = "🙂"
    else:
        expression = "😄"
    guu = await ai(ques)
    await asyncio.sleep(3)
    test = f"`{expression} {guu}`"
    await asyncio.sleep(1)
    await bot.send_message(newbie,test)


Soham.run()
