from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Function to delete excess resumes one by one
def delete_excess_resumes(driver):
    try:
        # Go to the main dashboard page
        driver.get('https://app.enhancv.com/')

        while True:
            # Wait for the delete buttons to be visible
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.DocumentCard-module_actionBtnDelete__btQRk')))

            # Get all delete buttons
            delete_buttons = driver.find_elements(By.CSS_SELECTOR, '.DocumentCard-module_actionBtnDelete__btQRk')

            if not delete_buttons:
                print("No delete buttons found. Exiting.")
                return

            # Loop through each delete button
            for delete_button in delete_buttons:
                try:
                    # Click the delete button for the current resume
                    delete_button.click()

                    # Wait for the confirm input to be visible
                    confirm_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="confirm"]')))

                    # Type "DELETE" into the confirm input field
                    confirm_input.send_keys('delete')
                    time.sleep(1)
                    # Wait for the confirm button to be clickable
                    confirm_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Delete Resume"]')))

                    # Click the confirm button
                    confirm_button.click()

                    print("Deleted one excess resume.")

                except StaleElementReferenceException:
                    print("Stale element reference encountered. Refinding delete buttons.")
                    break  # Break out of the inner loop and re-find delete buttons

                except ElementClickInterceptedException:
                    print("Element click intercepted. Trying again after a short wait.")
                    time.sleep(1)

                except ElementNotInteractableException:
                    print("Element not interactable. Trying again after a short wait.")
                    time.sleep(1)

                except Exception as e:
                    print(f"Error deleting excess resume: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        # Go to the main dashboard page
        driver.get('https://app.enhancv.com/')

        # Wait for the delete buttons to be visible
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.DocumentCard-module_actionBtnDelete__btQRk')))

        # Get all delete buttons
        delete_buttons = driver.find_elements(By.CSS_SELECTOR, '.DocumentCard-module_actionBtnDelete__btQRk')

        if not delete_buttons:
            print("No delete buttons found. Exiting.")
            return

        # Loop through each delete button
        for delete_button in delete_buttons:
            try:
                # Click the delete button for the current resume
                delete_button.click()

                # Wait for the confirm input to be visible
                confirm_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="confirm"]')))

                # Type "DELETE" into the confirm input field
                confirm_input.send_keys('delete')
                time.sleep(2)
                # Wait for the confirm button to be clickable
                confirm_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Delete Resume"]')))

                # Click the confirm button
                confirm_button.click()

                print("Deleted one excess resume.")

            except StaleElementReferenceException:
                # Refind the delete buttons
                delete_buttons = driver.find_elements(By.CSS_SELECTOR, '.DocumentCard-module_actionBtnDelete__btQRk')
                print("Stale element reference encountered. Refinding delete buttons.")

            except ElementClickInterceptedException:
                print("Element click intercepted. Trying again after a short wait.")
                time.sleep(1)

            except ElementNotInteractableException:
                print("Element not interactable. Trying again after a short wait.")
                time.sleep(1)

            except Exception as e:
                print(f"Error deleting excess resume: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Set up Selenium WebDriver
# driver = webdriver.Chrome()

# # Sign in
# sign_in(username, password)

# # Delete excess resumes
# delete_excess_resumes()

# # Close the WebDriver
# driver.quit()
