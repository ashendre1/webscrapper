from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import csv
from bs4 import BeautifulSoup

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('https://www.linkedin.com/login')

# Fill in the username and password
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys('your_username_here')

# Wait for the password field to be present and fill in the password
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys('your_password_here')

# Click on the sign in button
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

# Wait for the home page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ember20')))

# Now navigate to the feed
website = 'your linkedin post url here'
driver.get(website)

while True:
    try:
        load_more_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'comments-comments-list__load-more-comments-button')))
        load_more_button.click()
    except TimeoutException:
        break  # exit the loop if the button is no longer found

print('All comments loaded')

driver.get(website)

# Parse the page source with BeautifulSoup
bs_obj = BeautifulSoup(driver.page_source, 'html.parser')

data = []

# Find all comment divs
comment_divs = bs_obj.find_all('div', class_='comments-comment-item comments-comments-list__comment-item')
print(f"Total comments: {len(comment_divs)}")
for div in comment_divs:
    name = div.find('span', class_='comments-post-meta__name-text').text
    linkedin_url = div.find('a', class_='app-aware-link')['href']
    position = div.find('span', class_='comments-post-meta__headline').text
    comment_text = div.find('span', class_='comments-comment-item__main-content').text

    data.append({
        'name': name,
        'linkedin_url': linkedin_url,
        'position': position,
        'comment_text': comment_text
    })


with open('linkedin_comments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "LinkedIn URL", "Current Position", "Comment Text"])  # write header
    writer.writerows(data) 


# Quit the driver
driver.quit()
