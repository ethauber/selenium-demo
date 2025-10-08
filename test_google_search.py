from __future__ import annotations
import os, time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


start_url_google: str = "https://www.google.com"
search_input_name_attr: str = "q"
google_consent_button_id: str = "L2AGLb"
result_title_css: str = "h3"
query_text: str = "Selenium Python"

max_wait_for_element_seconds: int = 10
max_wait_for_page_seconds: int = 15
max_wait_for_consent_seconds: int = 3
demo_step_pause_seconds: float = 0.0
max_titles_to_print: int = 5


def running_under_pytest() -> bool:
    # pytest sets PYTEST_CURRENT_TEST in env
    return "PYTEST_CURRENT_TEST" in os.environ


def build_driver(headless: bool) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,800")
    drv = webdriver.Chrome(service=Service(), options=opts)
    drv.set_page_load_timeout(max_wait_for_page_seconds)
    return drv


def dismiss_google_consent_if_present(driver: webdriver.Chrome) -> None:
    try:
        WebDriverWait(driver, max_wait_for_consent_seconds).until(
            EC.element_to_be_clickable((By.ID, google_consent_button_id))
        ).click()
        time.sleep(demo_step_pause_seconds)
    except Exception:
        pass


def perform_search_and_collect_titles(driver: webdriver.Chrome) -> List[str]:
    driver.get(start_url_google)
    time.sleep(demo_step_pause_seconds)
    dismiss_google_consent_if_present(driver)

    box = WebDriverWait(driver, max_wait_for_element_seconds).until(
        EC.presence_of_element_located((By.NAME, search_input_name_attr))
    )
    box.clear()
    box.send_keys(query_text)
    box.submit()

    WebDriverWait(driver, max_wait_for_element_seconds).until(
        EC.title_contains("Selenium")
    )
    titles = [
        el.text.strip()
        for el in driver.find_elements(By.CSS_SELECTOR, result_title_css)
        if el.text.strip()
    ]
    return titles


# ---------- pytest entry ----------
def test_google_search_prints_titles():
    headless_mode = running_under_pytest()
    driver = build_driver(headless=headless_mode)
    try:
        titles = perform_search_and_collect_titles(driver)
        print("\nSearch results:")
        for t in titles[:max_titles_to_print]:
            print("-", t)
        assert "Selenium" in driver.title
    finally:
        driver.quit()


if __name__ == "__main__":
    headless_mode = False  # visible window when not under pytest
    driver = build_driver(headless=headless_mode)
    try:
        titles = perform_search_and_collect_titles(driver)
        print("\nSearch results:")
        for t in titles[:max_titles_to_print]:
            print("-", t)
        print("\nPage title:", driver.title)
        print("Close the window to finish.")
        # keep window open for manual viewing
        WebDriverWait(driver, 300).until(lambda d: False)
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()
