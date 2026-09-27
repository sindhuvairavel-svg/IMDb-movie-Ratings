from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get("https://www.imdb.com/chart/top/")

print("IMDb page opened successfully!")

input("Press Enter to close the browser...")

driver.quit()