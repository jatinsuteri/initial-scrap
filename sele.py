import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

os.environ['PATH'] += r'C:/selenium_driver'
driver = webdriver.Chrome()

driver.get('https://m.manganelo.com/wwww')
driver.implicitly_wait(5)

more_btn = '//div//div//div//div//a[@class="content-homepage-more a-h"]'
search_box = driver.find_element(By.XPATH, more_btn)
search_box.click()

action = ActionChains(driver)

exit_program = False

def fetch_data():
    with open('manga.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Rating', 'Link'])
        manga_tiles = driver.find_elements(By.CLASS_NAME, "content-genres-item")
        for tile in manga_tiles:
            try:
                title = tile.find_element(By.CLASS_NAME, "genres-item-name").text
                rating = tile.find_element(By.CLASS_NAME, "genres-item-rate").text
                link = tile.find_element(By.TAG_NAME, 'a').get_attribute('href')
                writer.writerow([title, rating, link])
                print(f"Title: {title}, Rating: {rating}")
            except NoSuchElementException:
                print('Error finding title or rating for a manga')

while not exit_program:
    print('''\nThis is a manga scraping tool. It scrapes top manga and their ratings.
Do you want a specific genre or all genres? Or do you want to exit? : \n''')
    preference = input().lower()

    if preference == 'all':
        fetch_data()
        print("Data stored in manga.csv")
        print('Exiting...')
        exit_program = True
    
    elif preference == 'exit':  
        exit_program = True
        print('Exiting...')

    elif preference == 'specific':
        try:
            expand = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "panel-advanced-search-tool"))
            )
            expand.click()

            genre_list = driver.find_elements(By.CLASS_NAME, "advanced-search-tool-genres-list")
            genres = [genre.text.strip() for genre in genre_list]
            genres = genres[0].split('\n')
            print("Available Genres: ", genres)

            genres_included = input('Enter the genres you want to include: ').split()
            genre_excluded = input('Enter the genres you want to exclude: ').split()

            for genre in genres_included:
                if genre.capitalize() not in genres:
                    print(f'Invalid genre "{genre}", please try again\n')
                else:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[title='{}']".format(genre.capitalize() + " Manga")))
                    )
                    element.click()

            for genre in genre_excluded:
                if genre.capitalize() not in genres:
                    print(f'Invalid genre "{genre}", please try again\n')
                else:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[title='{}']".format(genre.capitalize() + " Manga")))
                    )
                    action.double_click(element).perform()

            search = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "advanced-search-tool-apply"))
            )
            action.click(search).perform()
            time.sleep(5)

            fetch_data()
            
        except TimeoutException:
            print("Error: Unable to locate a necessary element on the page. Please try again.")
    
    else:
        print('Invalid input, please try again\n')

driver.quit()
