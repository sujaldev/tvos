from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote_plus, unquote_plus


def structure_results(results):
    structure = []
    for result in results:
        media_title = result.find_element(By.XPATH, "./div[2]").get_attribute("innerText")
        thumbnail_img = result.find_element(By.XPATH, "./div[1]//img").get_attribute("src")
        media_link = result.get_attribute("href")

        structure.append({
            "media_title": media_title,
            "media_link": quote_plus(media_link),
            "thumbnail": thumbnail_img
        })

    return structure


class API:
    BASE_URL = "https://vidembed.io/search.html?keyword="
    SEARCH_RESULTS_XPATH = "/html/body/div[1]/section/div[1]/div[5]/div/div[3]/div[1]/div/div/ul/li/a"
    IFRAME_XPATH = "/html/body/div[1]/section/div[1]/div[5]/div/div[1]/div[1]/div[1]/iframe"
    AD_POLL = 5

    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(10)

    def recreate_driver(self):
        self.driver.close()
        self.driver = webdriver.Chrome(options=self.options)

    def __get_iframe(self, media_page_url):
        self.driver.get(media_page_url)
        iframe = self.driver.find_element(By.XPATH, self.IFRAME_XPATH)
        iframe_source = iframe.get_attribute("src")
        return iframe_source

    def __get_media_source_from_iframe(self, iframe_url):
        self.driver.get(iframe_url)

        # Bypass ad popups
        for i in range(self.AD_POLL):
            try:
                ActionChains(self.driver).move_by_offset(100, 100).click().perform()
            except Exception as e:
                print(f"Exception during skipping popups: {e}")

        video_element = self.driver.find_element(By.XPATH, "//video")
        return video_element.get_attribute("src")

    # SEARCH DATABASE
    def search(self, query_string):
        query_url = self.BASE_URL + quote_plus(query_string)
        self.driver.get(query_url)
        results = self.driver.find_elements(By.XPATH, self.SEARCH_RESULTS_XPATH)
        return structure_results(results)

    # GET STREAMING URL FOR MEDIA
    def get_media_source(self, media_page_url):
        media_page_url = unquote_plus(media_page_url)
        iframe_url = self.__get_iframe(media_page_url)
        source_url = self.__get_media_source_from_iframe(iframe_url)

        self.recreate_driver()
        return source_url
