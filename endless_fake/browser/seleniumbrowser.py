import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

GAME_URL = "file:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "game", "embed.html")
CHROMEDRIVER_PATH = "./chromedriver"


class SeleniumBrowser:
    def __init__(self, url=None, chrome_driver=None):
        chrome_options = Options()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--allow-file-access-from-files")
        chrome_options.add_argument("--no-proxy-server")

        if chrome_driver is None:
            chrome_driver = CHROMEDRIVER_PATH

        self._url = GAME_URL if not url else url
        self._driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        self._driver.set_window_rect(x=10, y=0, width=500, height=640 + 133)
        self._driver.get(self._url)

    def get_position(self):
        position = self._driver.get_window_position()
        return position['x'], position['y']

    def shutdown(self):
        self._driver.quit()
