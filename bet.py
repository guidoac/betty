from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from telegram import Bot

CHECKPOINT = 95

class KebetBot():
    def __init__(self):
        self.slots = []
        self.api_token = '7905621866:AAHdrCSjoVO2rm8Z-fJV-x5nY6e7TpvA_oU'
        self.chat_id = '5904792400'
        self.target = 'https://rtpkebet.com/#/home'
        self.driver = None
        self.page = None
        self.bot = Bot(token=self.api_token)

        self.initialize()


    def initialize(self):
        self.driver = webdriver.Chrome()
        wait = WebDriverWait(self.driver, 5000)
        self.driver.get(self.target)
        self.page = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gameBox')))

    def getKebetElements(self):
        try:
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

                if (distribution and int(rtp) > CHECKPOINT):
                    self.slots.append({
                        'name': name.text,
                        'distribution': distribution,
                        'RTP': int(rtp),
                        'Min': int(min),
                        'Max': int(max),
                        'Avg': int(avg),
                        'Oficial RTP': int(oficial_rtp),
                        'element': game
                    })
                    """ asyncio.run(self.betty(game)) """
        except:
            pass

    async def betty(self, game):
        try:
            game.find_element(By.CLASS_NAME, 'topBox').click()
            game.find_element(By.CLASS_NAME, 'maskBox').find_elements(By.CSS_SELECTOR, 'p')[1].click()
            """ await asyncio.sleep(1)
            bet_btn = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[1]/div/div/div/div[2]/div[2]/div[2]/button')
            bet_btn.click()
            await asyncio.sleep(1)
            bet_input = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[1]/div/div/div/div[2]/div[2]/div[3]/input')
            bet_input.send_keys('10') """
        
        except:
            pass

    def formatMessage(self):
        message = ''
        for slot in self.slots:
            perfect_slot = slot['RTP'] > CHECKPOINT and slot['distribution']

            message += f"**{slot['name']}** {'🌟' if perfect_slot else ''} \n"
            message += f"RTP {slot['RTP']}% {'📈' if slot['RTP'] > CHECKPOINT else '📉'}\n"
            message += f"Em distribuição? {'Sim' if slot['distribution'] else 'Não'}\n"
            message += f"Min: {slot['Min']}% {'📈' if slot['Min'] > CHECKPOINT else '📉'}\n"
            message += f"Max: {slot['Max']}% {'📈' if slot['Max'] > CHECKPOINT else '📉'}\n"
            message += f"Avg: {slot['Avg']}% {'📈' if slot['Avg'] > CHECKPOINT else '📉'}\n"
            message += f"Oficial RTP: {slot['Oficial RTP']}%\n\n"
            message += '-----------------------\n\n'
        return message

    def sendMessage(self):
        if (self.slots.__len__() > 0):
            self.bot.send_message(chat_id=self.chat_id, text=self.formatMessage())

    def closeDriver(self):
        self.driver.refresh()

while True:
    kebet = KebetBot()
    kebet.getKebetElements()
    kebet.sendMessage()
    kebet.closeDriver()
