import asyncio
import datetime
import json
import requests
import sys
from pyppeteer import launch

URL = sys.argv[1]
filename = 'finviz.png'
ini_file = 'settings.json'
TOKEN = ''
CHANNEL = ''


def load_json(filename='settings.json'):
    global TOKEN
    global CHANNEL
    json_file = open(filename, 'r')
    json_data = json.load(json_file)
    TOKEN = json_data["token"]
    CHANNEL = json_data["channel"]


def upload_to_slack(filename):
    global TOKEN
    global CHANNEL
    dt = datetime.datetime.now()
    files = {'file': open(filename, 'rb')}
    param = {
            'token':TOKEN, 
            'channels':CHANNEL,
            'filename':"filename",
            'initial_comment': str(dt),
            'title': "finviz"
            }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(URL)
    await page.screenshot({'path': filename, 'fullPage': True})
    await browser.close()

    load_json(ini_file)
    upload_to_slack(filename)


asyncio.get_event_loop().run_until_complete(main())
