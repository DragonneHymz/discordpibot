from bs4 import BeautifulSoup as BS
import requests, discord, os
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import tasks
from dotenv import load_dotenv

def findPiAtMicroCenter():
    websiteHTML= requests.get("https://www.microcenter.com/product/643085/pizero2w?src=raspberrypi&storeID=141").text

    soup=BS(websiteHTML, 'html.parser')
    availability= soup.find('span', class_="inventoryCnt").text
    if availability != '0 NEW IN STOCK':
        webhook.send(availability)
        webhook.send("https://www.microcenter.com/product/643085/pizero2w?src=raspberrypi&storeID=141")

if __name__=='__main__':
    client = discord.Client()
    webhook= Webhook.from_url('https://discord.com/api/webhooks/992255580301443262/nlqgxJKaaepUgTjDgr4OXvf8aqfzb_8RNkme0sKcv9KIwMp7pkKRHJjMTKcQO9vm93q4', adapter=RequestsWebhookAdapter())
    load_dotenv()
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content.startswith('$status'):
            await message.channel.send('Online')

    @tasks.loop(minutes=60)
    async def checkStore():
        findPiAtMicroCenter()

    @client.event
    async def on_ready():
        channel= client.get_channel(992255538048008203)
        #await channel.send('Logged in as {0.user} '.format(client))
        checkStore.start()

    client.run(os.getenv('KEY'))
