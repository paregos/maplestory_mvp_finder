import mss
import mss.tools
import cv2  
import numpy as np  
import pytesseract
import time
import re
import requests
import discord
import random
import string
import os
from playsound import playsound

# The time between searches for mvp in seconds
mvpSearchTimeSeconds = 5

# Tesseract exe location
tesseractExeLocation = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# If you want to have a loot timer sound as well set this to True, otherwise False
shouldPlayLootTimer = True
lootTimeSeconds = 2

# If you want to send messages to a discord channel whenever you find an mvp
# Follow this guide on how to get a webhook url https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
sendMessageToDiscord = False
discord_url = ""

# Mvp text regex
mvpTextRegex = "(((ch)|(cc)).{0,10}([xX]){2})|(([xX]{2}).{0,10}((ch)|(cc)))|([xX]{2}:\d)|([xX]:\d{2})|((shri|mush|mvp|maya).{0,10}([xX]|[:]\d|\d))|(([xX]|[:]\d|\d).{0,10}(shri|mush|mvp))|((shri|mush|mvp).{0,10}(shri|mush|mvp))"


with mss.mss() as sct:
    pytesseract.pytesseract.tesseract_cmd = tesseractExeLocation
    starttime = time.time()
    lastLootTime = time.time()

    old_megaphone_tab_image_name = None

    while True:

        ## check loot time if enabled
        if shouldPlayLootTimer:
            if time.time() >= lootTimeSeconds+lastLootTime:
                playsound('Ding.mp3')
                lastLootTime = time.time()

        ## screenshot all monitors
        output = "megaphone_tab_search_space.png"
        sct.shot(mon=-1, output='megaphone_tab_search_space.png')

        ## Look for megaphone tab
        image = cv2.imread(output)
        template = cv2.imread("megaphone_bar_title.png")
        result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
        index = np.unravel_index(result.argmax(),result.shape)
        print(index)

        ## Debug screenshot where we think the megaphone tab is
        croppedMegaphoneTab = image[index[0]:index[0]+145+27, index[1]:index[1]+390]
        cv2.imwrite("./megaphonetab.png", croppedMegaphoneTab)

        ## Get the last two lines of chat
        croppedLastTwoLines = image[index[0]+145:index[0]+145+27, index[1]:index[1]+390]
        new_megaphone_tab_image_name =  "./captures/"+str(time.time())+".png"
        cv2.imwrite(new_megaphone_tab_image_name, croppedLastTwoLines)

        ## compare new screenshot to old
        if old_megaphone_tab_image_name is not None:
            #compare old and new images
            if open(old_megaphone_tab_image_name,"rb").read() == open(new_megaphone_tab_image_name,"rb").read():
                print("No new megaphone detected")

                ## delete newly saved screnshot as its not unique
                os.remove(new_megaphone_tab_image_name)

                time.sleep(5.0 - ((time.time() - starttime) % 5.0))
                continue
            else:
                print("New megaphone detected")
                ## delete old saved screenshot as its not the most recent
                os.remove(old_megaphone_tab_image_name)

        ## update new screenshot to be old
        old_megaphone_tab_image_name = new_megaphone_tab_image_name

        ## get megaphone tab text
        text = pytesseract.image_to_string(croppedLastTwoLines)
        print("========New text from smega=========")
        print(text)

        mvpFound = re.search(mvpTextRegex, text, re.IGNORECASE)

        if mvpFound:
            print("YES! We have a match!")
            # Play mvp sound
            playsound('Bruh.mp3')
            if sendMessageToDiscord:
                webhook = discord.Webhook.from_url(discord_url, adapter=discord.RequestsWebhookAdapter())
                mvp_screenshot = discord.File(croppedLastTwoLines)
                webhook.send("Lads found a new MVP pogs in the chat", file=mvp_screenshot)
        else:
            print("No match")


        time.sleep(mvpSearchTimeSeconds - ((time.time() - starttime) % mvpSearchTimeSeconds))

