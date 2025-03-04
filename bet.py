from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import asyncio

from telegram import Bot

class KebetBot():
    def __init__(self):
        self.slots = []
        self.api_token = '7905621866:AAHdrCSjoVO2rm8Z-fJV-x5nY6e7TpvA_oU'
        self.chat_id = '5904792400'
        self.target = 'https://rtpkebet.com/#/home'







def getKebetElements():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5000)
    driver.get(TARGET_URL)

    # Locate the element by CSS and print its content 
    transcript = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gameBox')))
    games = transcript.find_elements(By.CLASS_NAME, 'gameItem')

    for game in games:
        name = game.find_element(By.CLASS_NAME, 'gameName')
        items = game.find_elements(By.CLASS_NAME, 'processItem')
        distribution = game.find_element(By.CLASS_NAME, 'arrow').get_attribute('src').startswith('https://rtpkebet.com/assets/down')
        rtp = items[0].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
        min = items[1].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
        max = items[2].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
        avg = items[3].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
        oficial_rtp = items[4].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')

        if (distribution and int(rtp) > 96):
            slots.append({
                'name': name.text,
                'RTP': rtp,
                'Min': min,
                'Max': max,
                'Avg': avg,
                'Oficial RTP': oficial_rtp,
            })

    driver.close()

def sendMessage(message):
    bot = Bot(token=API_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    while True:
        getKebetElements()
        print(str(slots))

asyncio.run(main())