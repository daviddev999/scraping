import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from delete_resume_entries import delete_excess_resumes
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

# Global variables to keep track of the number of downloads and category bundle count
download_count = 0
category_bundle_count = 0

def collect_resume_urls(category_url):
    try:
        driver.get(category_url)
        time.sleep(5)  # Wait for the page to load (adjust the time as needed)

        # Find all resume links on the category page
        resume_links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://app.enhancv.com/resume/new?"]')
        resume_urls = [link.get_attribute('href') for link in resume_links]

        return resume_urls
    except UnexpectedAlertPresentException as e:
        # Handle unexpected alert
        alert_text = driver.switch_to.alert.text
        print(f"Unexpected alert encountered: {alert_text}")
        driver.switch_to.alert.accept()
        return []
    except Exception as e:
        print(f"Error occurred while collecting resume URLs: {str(e)}")
        return []


# Function to handle sign-in
def sign_in(username, password):
    # Navigate to the sign-in page
    sign_in_url = 'https://app.enhancv.com/login'
    driver.get(sign_in_url)
    
    # Wait for the email input field to be visible
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="email"]')))
    except TimeoutException:
        print("Timed out waiting for the email input field to be visible.")
    # Fill in the sign-in form
    driver.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)

    # Submit the form to sign in
    driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="signIn"]').click()
    time.sleep(5)  # Wait for the sign-in process to complete (adjust the time as needed)

# Function to change Chrome's default download path
def change_download_path(category_name):
    # Get the absolute path of the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a subdirectory for the category within the script directory
    category_dir = os.path.join(script_dir, category_name)
    os.makedirs(category_dir, exist_ok=True)

    # Define the download path as the subdirectory for the category
    download_path = category_dir

    # Set the download path using Chrome DevTools Protocol
    params = {'behavior': 'allow', 'downloadPath': download_path}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

# Function to get the current resume entries count
def get_resume_entries_count():
    try:
        # Find the div element containing the count
        count_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "DocumentTitle-module_title__T26Q1")]')))
        
        # Get the text content of the div element
        count_text = count_element.text
        
        # Extract the count from the text content (assuming the count is enclosed in parentheses)
        resume_count = int(count_text.split('(')[-1].split(')')[0])
        print(resume_count)
        return resume_count
    except Exception as e:
        # print(f"Error occurred while getting resume entries count: {str(e)}")
        return 100
    
# Function to download resumes from individual resume pages into separate folders
def download_resumes(resume_urls, category_name):
    global download_count, category_bundle_count

    # Calculate the total expected count of downloads if this category bundle is downloaded
    # expected_total_count = download_count + len(resume_urls)

    # # Check if the expected total count exceeds the limit
    # if expected_total_count > 100:
    #     print(f"Skipping download for category {category_name}. Total count exceeds 100.")
    #     delete_excess_resumes()

    # Increment category bundle count
    category_bundle_count += 1
    change_download_path(category_name)
    # Process the resumes for this category
    for url in resume_urls:
        # if download_count >= 100:
        #     print("Download limit reached. Exiting download process.")
        #     return  # Exit the function if download limit reached
        if get_resume_entries_count() > 90:
            delete_excess_resumes(driver=driver)
        driver.get(url)
        try:
            # Find and click on the link to trigger the modal
            time.sleep(10)
            download_link = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-test-id="toolbox-download-btn"]')))
            download_link.click()

            # Wait for the download button within the modal to become clickable
            download_button = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-pdf-variant-b.btn-primary')))
            # Click the download button to download the resume as PDF
            download_button.click()
            time.sleep(20)
            # Increment download count
            download_count += 1

        except Exception as e:
            print(f"Error occurred while processing {url}: {str(e)}")

    print(f"Downloaded {len(resume_urls)} resumes for category bundle {category_bundle_count}")

# Add Chrome WebDriver directory to system PATH
os.environ["PATH"] += os.pathsep + r'C:\Users\Administrator\.cache\selenium\chromedriver\win64\123.0.6312.105'

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Sign in
username = 'testtest333@gmail.com'
password = '123123123'
sign_in(username, password)

# Navigate to the resume examples page
driver.get('https://enhancv.com/resume-examples/')
time.sleep(5)

# Find all category links
category_link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.ListItem_listItem__3GTW1')

# Extract category URLs
category_urls = [element.get_attribute('href') for element in category_link_elements]

# Collect and download resumes for each category
for category_url in category_urls:
    category_name = category_url.split('/')[-2]  # Extract category name from URL
    print(f"Processing category: {category_name}")
    resume_urls = collect_resume_urls(category_url)
    download_resumes(resume_urls, category_name)

# Close the WebDriver
driver.quit()
