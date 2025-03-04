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
        self.driver = None
        self.page = None

        self.initialize()


    def initialize(self):
        self.driver = webdriver.Chrome()
        wait = WebDriverWait(self.driver, 5000)
        self.driver.get(self.target)
        self.page = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gameBox')))

    def getKebetElements(self):
        games = self.page.find_elements(By.CLASS_NAME, 'gameItem')

        for game in games:
            name = game.find_element(By.CLASS_NAME, 'gameName')
            items = game.find_elements(By.CLASS_NAME, 'processItem')
            distribution = game.find_element(By.CLASS_NAME, 'arrow').get_attribute('src').startswith('https://rtpkebet.com/assets/down')
            rtp = items[0].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
            min = items[1].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
            max = items[2].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
            avg = items[3].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')
            oficial_rtp = items[4].find_element(By.CLASS_NAME, 'el-progress--without-text').get_attribute('aria-valuenow')

            if (distribution and int(rtp) > 90):
                self.slots.append({
                    'name': name.text,
                    'distribution': distribution,
                    'RTP': rtp,
                    'Min': min,
                    'Max': max,
                    'Avg': avg,
                    'Oficial RTP': oficial_rtp,
                })

    def formatMessage(self):
        message = ''
        for slot in self.slots:
            message += f"{slot['name']}: RTP {slot['RTP']}%\n"
            message += f"Em distribuição? {'Sim' if slot['distribution'] else 'Não'}\n"
            message += f"Min: {slot['Min']}%\n"
            message += f"Max: {slot['Max']}%\n"
            message += f"Avg: {slot['Avg']}%\n"
            message += f"Oficial RTP: {slot['Oficial RTP']}%\n\n"
            message += '---\n'
        return message

    def sendMessage(self):
        bot = Bot(token=self.api_token)
        bot.send_message(chat_id=self.chat_id, text=self.formatMessage())

    def closeDriver(self):
        self.driver.close()

while True:
    kebet = KebetBot()
    kebet.getKebetElements()
    kebet.sendMessage()
    kebet.closeDriver()
