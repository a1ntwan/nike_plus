from os import environ
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
from time import sleep
import datetime
from loguru import logger
import boto3

size_to_num = {'5': 1, '5.5': 2, '6': 3, '6.5': 4, '7': 5, '7.5': 6, '8': 7, '8.5': 8, '9': 9, '9.5': 10, '10': 11,
               '10.5': 12, '11': 13, '11.5': 14, '12': 15}

URL = environ['URL']
PRODUCT_ID = environ['PRODUCT_ID']
EMAIL = environ['EMAIL']
PASS = environ['PASS']
SIZE = environ['SIZE']
NAME = environ['NAME']
CVV = environ['CVV']
USER_AGENT = environ['USER_AGENT']
PROXY = environ['PROXY']


s3_session = boto3.Session(
    aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
)

proxy = {
       'proxy': {
           'https': PROXY
           }
       }

defender = 'defender.crx'
webrtc = 'webrtc.crx'
executable_path = Service('/sneakers/chromedriver/chromedriver')


class Nike:
    def __init__(self):
        """Use/not headless Chrome. Hide Selenium. Open the page with Chrome"""
        window = Display(visible=0, size=(1366, 768))
        self.window = window
        self.window.start()
        options = ChromeOptions()
        options.add_argument('--window-size=1366,768')
        options.add_extension(defender)
        options.add_extension(webrtc)
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('ignore-certificate-errors')
        options.add_argument(f'user-agent={USER_AGENT}')

        driver = webdriver.Chrome(
            seleniumwire_options=proxy,
            options=options,
            service=executable_path,
            service_args=['--verbose', '--log-path=/sneakers/logs/chrdrv.log']
        )
        self.driver = driver
        self.ip = ''

    def page_open(self, page=None):
        """Open the web-page"""
        self.driver.get(page)

    def my_ip(self):
        """Check my proxy ip"""
        self.driver.get('https://ipinfo.io/ip')
        self.ip = self.driver.find_element(By.TAG_NAME, 'body').text
        print(f'My ip is: {self.ip}')

    def load(self, by, string, rule):
        """Waiting for the element to apply to"""
        wait = WebDriverWait(self.driver, 30)
        element_await = wait.until(rule((by, string)))
        element_await.click()

    def form_fill(self, by, string, keys=None):
        """Dealing with input"""
        element_input = self.driver.find_element(by, string)
        element_input.click()
        element_input.send_keys(f'{keys}')

    def pre_login(self):
        """Pre-login operations"""
        actions = ActionChains(self.driver)
        sign_in = self.driver.find_element(By.CLASS_NAME, 'join-log-in')
        actions.move_to_element(sign_in).click().perform()

    def login(self):
        """Login, if error do it one more time"""
        self.driver.find_elements(By.TAG_NAME, 'input')[1].send_keys(EMAIL)
        self.driver.find_elements(By.TAG_NAME, 'input')[2].send_keys(PASS, Keys.ENTER)
        sleep(1)
        while True:
            if self.driver.find_elements(By.CLASS_NAME, 'nike-unite-error-panel'):
                self.driver.find_element(By.CLASS_NAME, 'nike-unite-error-close').click()
                print(datetime.datetime.now(), 'Login failed')
                self.driver.find_elements(By.TAG_NAME, 'input')[2].send_keys(PASS, Keys.ENTER)
                sleep(1)
            else:
                break

    def choose_size(self):
        """Choose size"""
        s = size_to_num.get(SIZE) - 1
        self.driver.find_elements(By.CLASS_NAME, 'size-grid-button')[s].click()

    def cvv_frame(self):
        """Switch to CVV iFrame"""
        iframe = self.driver.find_element(By.ID, 'paymentsIframe')
        self.driver.switch_to.frame(iframe)

    def button_submit_all(self):
        """Click submit order button"""
        actions = ActionChains(self.driver)
        button_s = self.driver.find_element(By.ID, 'stored-cards-paynow')
        actions.move_to_element(button_s).click().perform()

    def close(self):
        """Closing the browser"""
        self.driver.close()
        self.driver.quit()
        self.window.stop()

    def screen(self):
        """Making a final screenshot and uploading it to S3, placing public_ip in a name"""
        self.driver.save_screenshot(f'{self.ip}--screen.png')
        s3 = s3_session.resource('s3')
        s3.meta.client.upload_file(f'{self.ip}--screen.png', 'nike-drop-bucket', f'{self.ip}--screen.png')

    @staticmethod
    def logger():
        """Adding Exceptions Logs"""
        return logger.add("/sneakers/logs/sneakers_err.log", format="{time} {level} {message}", level="DEBUG")


def drop_nike():
    """Drop time function"""
    drop = datetime.datetime(
        int(environ['YEAR']),
        int(environ['MONTH']),
        int(environ['DAY']),
        int(environ['HOUR']),
        int(environ['MINUTE']),
        int(environ['SECOND'])
    )
    delta = drop - datetime.datetime.now()
    if drop.day >= datetime.datetime.now().day and drop.time() > datetime.datetime.now().time():
        return delta.seconds
    return 0


DATE = drop_nike()


@logger.catch
def main():
    try:
        # Open the browser, turn on logs
        nike = Nike()
        nike.logger()
        nike.my_ip()
        nike.page_open('https://www.nike.com/ru/launch')
        print(datetime.datetime.now(), 'The page is loaded successfully')

        # Accept cookies
        # nike.load(By.CLASS_NAME, 'btn-lg', EC.element_to_be_clickable)
        # print(datetime.datetime.now(), 'Cookies accepted')

        # Pre-login
        nike.load(By.CLASS_NAME, 'join-log-in', EC.element_to_be_clickable)
        nike.pre_login()
        print(datetime.datetime.now(), 'Pre-login actions succeeded')

        # Login
        nike.load(By.NAME, 'emailAddress', EC.element_to_be_clickable)
        nike.login()
        print(datetime.datetime.now(), 'Logged in successfully')

        # Sleep and go
        sleep(DATE) if DATE != 0 else True
        nike.page_open(f'{URL}')
        print(datetime.datetime.now(), "Let's go")

        # Choose size and order
        nike.choose_size()
        sleep(1)
        nike.load(By.CLASS_NAME, 'ncss-btn-primary-dark', EC.element_to_be_clickable)
        sleep(1)
        print(datetime.datetime.now(), 'Size chosen')
        sleep(2)
        nike.page_open('https://www.nike.com/ru/cart')

        # Delivery options (member-landing, shipping-form, billing-form)
        sleep(1)
        nike.load(By.CLASS_NAME, 'e16pwdtm0', EC.element_to_be_clickable)
        sleep(1)
        nike.load(By.CLASS_NAME, 'btn--fluid', EC.element_to_be_clickable)
        sleep(1)
        nike.load(By.CLASS_NAME, 'btn--fluid', EC.element_to_be_clickable)
        sleep(1)
        nike.load(By.CLASS_NAME, 'btn--fluid', EC.element_to_be_clickable)
        print(datetime.datetime.now(), 'Done with delivery options')
        sleep(1)

        # CVV input and submit
        sleep(1)
        nike.cvv_frame()
        nike.form_fill(By.ID, 'cardCvc-input', CVV)
        sleep(1)
        nike.button_submit_all()
        print(datetime.datetime.now(), 'Submitted order')
        sleep(450)
        nike.screen()
        print(datetime.datetime.now(), 'Screen')
        nike.close()
        print(datetime.datetime.now(), 'Done successfully')
        exit(0)
    except TimeoutException:
        print(datetime.datetime.now(), 'TimeoutException')
        exit(8)


if __name__ == '__main__':
    main()
