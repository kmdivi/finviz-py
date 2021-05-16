import asyncio
import datetime
import json
import sys

import requests
from pyppeteer import launch

ini_file = "settings.json"
TOKEN = ""
CHANNEL = ""


def load_json(filename="settings.json"):
    global TOKEN
    global CHANNEL
    json_file = open(filename, "r")
    json_data = json.load(json_file)
    TOKEN = json_data["token"]
    CHANNEL = json_data["channel"]


def upload_to_slack(filename):
    global TOKEN
    global CHANNEL
    dt = datetime.datetime.now()
    files = {"file": open(filename, "rb")}
    param = {
        "token": TOKEN,
        "channels": CHANNEL,
        "filename": "filename",
        "initial_comment": str(dt),
        "title": filename,
    }
    requests.post(url="https://slack.com/api/files.upload", params=param, files=files)


def check_args(argv):
    if len(argv) >= 1:
        return True
    else:
        return False


def get_filename(URL):
    filename = URL[URL.index("/") + 2 :]
    if "www." in filename:
        filename = filename.replace("www.", "")
    filename = filename[: filename.index(".")]

    return filename + ".png"


async def main():
    has_url = check_args(sys.argv)
    if not has_url:
        print("Input url to take screenshot.")
        exit(0)

    URL = sys.argv[1]
    filename = get_filename(sys.argv[1])

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

    browser = await launch()
    page = await browser.newPage()
    await page.setUserAgent(UA)
    await page.goto(URL)
    await page.screenshot({"path": filename, "fullPage": True})
    await browser.close()

    load_json(ini_file)
    upload_to_slack(filename)


asyncio.get_event_loop().run_until_complete(main())
