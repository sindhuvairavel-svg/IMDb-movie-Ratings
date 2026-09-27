import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Chrome settings
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Start Chrome
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Open IMDb Top 250
driver.get("https://www.imdb.com/chart/top/")
time.sleep(5)

print("IMDb page opened successfully!")
print("Page title:", driver.title)

# Human verification
input("Complete Human Verification in Chrome, then press ENTER here...")

time.sleep(3)


# Find movie links
movie_links = driver.find_elements(
    By.XPATH,
    "//a[contains(@href, '/title/tt')]"
)

movies = []
seen = set()

for link in movie_links:

    try:
        movie_name = link.text.strip()

        if not movie_name:
            continue

        movie_name = movie_name.replace("\n", " ").strip()

        if movie_name in seen:
            continue

        # Get year and rating from the movie card
        parent = link.find_element(
            By.XPATH,
            "./ancestor::li[1]"
        )

        info = parent.text.strip()

        # Find year
        year_match = re.search(
            r"\b(19\d{2}|20\d{2})\b",
            info
        )

        if year_match:
            year = year_match.group(1)
        else:
            year = "N/A"

        # Find rating
        rating_match = re.search(
            r"\b([0-9]\.[0-9])\b",
            info
        )

        if rating_match:
            rating = rating_match.group(1)
        else:
            rating = "N/A"

        movies.append([
            len(movies) + 1,
            movie_name,
            year,
            rating
        ])

        seen.add(movie_name)

        if len(movies) >= 250:
            break

    except Exception:
        continue


# Display results
print()
print("==============================")
print("Movies found:", len(movies))
print("==============================")

for movie in movies:
    print(
        movie[0],
        "-",
        movie[1],
        "-",
        movie[2],
        "-",
        movie[3]
    )


# Save CSV
csv_file = "imdb_movies.csv"

with open(
    csv_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Rank",
        "Movie Name",
        "Year",
        "Rating"
    ])

    for movie in movies:
        writer.writerow(movie)


# Final output
print()
print("==============================")
print("Data saved successfully!")
print("==============================")
print("Total movies saved:", len(movies))
print("CSV file:", csv_file)


# Close Chrome
driver.quit()