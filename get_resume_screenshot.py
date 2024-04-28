from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Function to capture and save screenshot of the resume detail section
def capture_resume_detail_screenshot(url, output_path):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load (adjust the time as needed)

    # Execute JavaScript to hide other elements on the page except the resume detail section
    driver.execute_script("""
        // Hide elements outside the resume detail section
        var elementsToHide = document.querySelectorAll('body > *:not(.resume-editor-wrapper.feedback-wrapper.relative)');
        elementsToHide.forEach(function(element) {
            element.style.display = 'none';
        });

        // Adjust styles of the resume detail section
        var resumeDetailSection = document.querySelector('.resume-editor-wrapper.feedback-wrapper.relative');
        resumeDetailSection.style.position = 'relatvie';
    """)

    # Capture screenshot of the resume detail section
    driver.save_screenshot(output_path)

# Set up Chrome WebDriver with existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=ChromeProfile")  # Path to your Chrome profile directory
import os
os.environ["PATH"] += os.pathsep + r'C:\Users\Administrator\.cache\selenium\chromedriver\win64\123.0.6312.105'

# Set up Selenium WebDriver
driver = webdriver.Chrome()
# Example usage
resume_url = 'https://app.enhancv.com/resume/new?example=predefined-D2Kf8L38NLEjo016YEeu5avewoKFg4BPf0JK0xZz'  # Example resume URL
output_image_path = 'resume_detail.png'  # Output image path
capture_resume_detail_screenshot(resume_url, output_image_path)

# Close the WebDriver
driver.quit()