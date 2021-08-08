# maplestory_mvp_finder
A python script that alerts you when mvps are found.

This script works by taking screenshots of your computer and searching for megaphone text. The script does not interact with your maplestory game, it just works based on screenshots.


# Requirements
- Python (2 or 3)
- Pip see here for an example (https://www.liquidweb.com/kb/install-pip-windows/)
- Tesseract, this is an optical recognition library we need to search for the megaphone tab (https://github.com/tesseract-ocr/tesseract/wiki)


# Install
- Clone/Download the repository
- Install all python requirements via pip, e.g `pip3 install -r requirements.txt` for python3, `pip install -r requirements.txt` for python2


# Setup (updating the mvp_notifier file)
- Set your tesseract exe location e.g `tesseractExeLocation = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'`
- You can configure a loot timer by setting `shouldPlayLootTimer = True` and choosing a time via `lootTimeSeconds = 115`
- You can configure a discord webhook url to send notifications to when you find a mvp via `sendMessageToDiscord = True` and `discord_url = ""`. You can create a webhook url via https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks 


# Running
- Run maplestory in windowed mode, with chat popped out
- Run the mvp notifier via `python ./mvp_notifier.py`
