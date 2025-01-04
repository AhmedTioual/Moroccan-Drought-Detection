from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

class MapScraper:

    def __init__(self, download_path):
        # Set up Chrome options
        ops = Options()
        ops.binary_location = "/home/ahmed/chrome-linux64/chrome"  # Path to your custom Chrome binary
        ops.headless = False  # Set to True for headless mode
        ops.add_argument("--start-maximized")  # Ensure the browser is maximized

        # Set up download preferences before initializing WebDriver
        prefs = {
            "download.default_directory": download_path,  # Set the path to save the downloaded images
            "download.prompt_for_download": False,  # Disable download prompt
            "safebrowsing.enabled": True,  # Enable safe browsing to avoid warnings
        }
        ops.add_experimental_option("prefs", prefs)

        # Initialize WebDriver with the options and preferences
        self.driver = webdriver.Chrome(options=ops)
        
    def open_website(self):
        url = "https://drought.emergency.copernicus.eu/tumbo/edo/map/"
        self.driver.get(url)
        print("Website opened successfully.")
        time.sleep(5)  # Allow time for the page to load fully

    def cancel_cookies(self):
        try:
            # Locate the "Cancel" or "Dismiss" button for cookies
            cookies_button = self.driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')  # Update XPATH based on your website
            cookies_button.click()
            print("cookies  dismissed successfully.")
            time.sleep(1)  # Allow time for the action to complete
        except Exception as e:
            print("Could not dismiss cookies :", e)

    def cancel_statistics(self):
        try:
            time.sleep(5)
            statistics_button = self.driver.find_element(By.XPATH, "/html/body/figure/div/div[22]/div[2]/div[2]/button[1]")  # Update XPATH based on your website
            statistics_button.click()
            print("Anonymous usage statistics  dismissed successfully.")
            time.sleep(1)  # Allow time for the action to complete
        except Exception as e:
            print("Could not dismiss Anonymous usage statistics :", e)

    def zoom_all(self):
            try:
                zoom_all_button = self.driver.find_element(By.XPATH, "/html/body/figure/div/div[4]/div[3]/div[7]/button[2]")  # Update XPATH based on your website
                zoom_all_button.click()
                print("zoom_all successfully.")
                time.sleep(1)  # Allow time for the action to complete
            except Exception as e:
                print("Could not dismiss zoom_all :", e)

    def skip_warning(self):
            try:
                skip_warning_button = self.driver.find_element(By.XPATH, '//*[@id="warning_messages_panel"]/button')  # Update XPATH based on your website
                skip_warning_button.click()
                print("skip_warning successfully.")
                time.sleep(1)  # Allow time for the action to complete
            except Exception as e:
                print("Could not dismiss skip_warning :", e)
    
    def collapse(self):
            try:
                collapse_button = self.driver.find_element(By.XPATH, '//*[@id="layer_info_panel"]/div[1]/div[2]/button')  # Update XPATH based on your website
                collapse_button.click()
                print("collapse successfully.")
                time.sleep(1)  # Allow time for the action to complete
            except Exception as e:
                print("Could not dismiss skip_warning :", e)

    def options(self):
            try:
                options_button = self.driver.find_element(By.XPATH, '//*[@id="container_layer_tree_panel"]/div/ul/li[1]/div/div[2]/ul/li[1]/div/div[2]/ul/li[1]/div/div[1]/div[3]/button')  # Update XPATH based on your website
                options_button.click()
                print("options successfully.")
                time.sleep(1)  # Allow time for the action to complete
            except Exception as e:
                print("Could not dismiss options :", e)

    def opacity(self):
        try:
            button_xpath = '//*[@id="cdi_opacity_slider"]/div[1]/div[3]/button'
            
            while True:
                # Locate the button
                button = self.driver.find_element(By.XPATH, button_xpath)

                # Check if the button is disabled
                if button.get_attribute("disabled") == "true":
                    print("Button is disabled. Stopping clicks.")
                    break

                # Click the button
                button.click()
                print("opacity 100%.")
                time.sleep(100)  # Adjust sleep to match the loading time

        except Exception as e:
            print("Error during clicking:", e)

    def click_year_previous(self):
        try:
            button_xpath = '//*[@id="cdi_year_slider"]/div[1]/div[1]/button'
            
            while True:
                # Locate the button
                button = self.driver.find_element(By.XPATH, button_xpath)

                

                # Check if the button is disabled
                if button.get_attribute("disabled") == "true":
                    print("Button is disabled. Stopping clicks.")
                    break

                # Click the button
                button.click()
                print("Button clicked.")
                time.sleep(1)  # Adjust sleep to match the loading time

        except Exception as e:
            print("Error during clicking:", e)

    def click_month_previous(self):
        try:
            button_xpath = '//*[@id="cdi_month_slider"]/div[1]/div[1]/button'
            
            while True:
                # Locate the button
                button = self.driver.find_element(By.XPATH, button_xpath)

                # Check if the button is disabled
                if button.get_attribute("disabled") == "true":
                    print("Button is disabled. Stopping clicks.")
                    break

                # Click the button
                button.click()
                print("Button clicked.")
                time.sleep(1)  # Adjust sleep to match the loading time

        except Exception as e:
            print("Error during clicking:", e)

    def click_ten_day_period_previous(self):
        try:
            button_xpath = '//*[@id="cdi_tenDay_slider"]/div[1]/div[1]/button'
            
            while True:
                # Locate the button
                button = self.driver.find_element(By.XPATH, button_xpath)

                # Check if the button is disabled
                if button.get_attribute("disabled") == "true":
                    print("Button is disabled. Stopping clicks.")
                    break

                # Click the button
                button.click()
                print("Button clicked.")
                time.sleep(1)  # Adjust sleep to match the loading time

        except Exception as e:
            print("Error during clicking:", e)

    def extract_date_info(self):
        # Extract year, month, and day from the page
        year = self.driver.find_element(By.XPATH, '//*[@id="cdi_year_slider"]/div[1]/div[2]').text
        month = self.driver.find_element(By.XPATH, '//*[@id="cdi_month_slider"]/div[1]/div[2]').text
        day_range = self.driver.find_element(By.XPATH, '//*[@id="cdi_tenDay_slider"]/div[1]/div[2]').text

        # Map day range (1, 2, 3) to corresponding date format
        if day_range == "1":
            day = "01"
        elif day_range == "2":
            day = "11"
        elif day_range == "3":
            day = "21"
        else:
            day = "01"  # Default to 01 if something goes wrong

        return year, month, day

    def download_image(self):
        try:
            # Extract the date information for naming the image
            year, month, day = self.extract_date_info()
            filename = f"{year}-{month}-{day}.png"
            print(f"Generated filename: {filename}")

            # Locate the export button and click it
            export_button_xpath = '//*[@id="export_image_tool"]/button'
            export_button = self.driver.find_element(By.XPATH, export_button_xpath)
            export_button.click()
            print("Export button clicked. Waiting for download to complete...")

            # Wait for the file to appear in the download folder
            download_folder = "/home/ahmed/Desktop/Moroccan-Drought-Segmentation/satellite-images"
            max_wait_time = 60  # Maximum time to wait in seconds
            file_downloaded = False

            start_time = time.time()
            while time.time() - start_time < max_wait_time:
                downloaded_files = os.listdir(download_folder)
                for file in downloaded_files:
                    if file.endswith(".crdownload") or file.endswith(".tmp"):
                        # File is still downloading
                        print("Download in progress...")
                        time.sleep(1)
                        break
                else:
                    # Check if the file is completely downloaded
                    for file in downloaded_files:
                        if file.endswith(".png"):
                            # Rename the downloaded image
                            old_file_path = os.path.join(download_folder, file)
                            new_file_path = os.path.join(download_folder, filename)
                            os.rename(old_file_path, new_file_path)
                            print(f"Image saved as {filename}")
                            file_downloaded = True
                            break

                if file_downloaded:
                    break

            if not file_downloaded:
                print(f"Download timed out after {max_wait_time} seconds.")
                return False  # Indicate failure to download

        except Exception as e:
            print(f"Error during image download: {e}")
            return False  # Indicate failure to download

        return True  # Indicate success

    def next(self):
        try:
            button_xpath = '//*[@id="cdi_tenDay_slider"]/div[1]/div[3]/button'

            while True:
                # Download the image
                if not self.download_image():
                    print("Image download failed. Exiting...")
                    break

                # Locate the button
                button = self.driver.find_element(By.XPATH, button_xpath)

                # Check if the button is disabled
                if button.get_attribute("disabled") == "true":
                    print("Next Button is disabled. Stopping clicks.")
                    break

                # Click the button
                button.click()
                print("Next")
                time.sleep(2)

        except Exception as e:
            print("Error during clicking:", e)

        finally:
            self.close_browser()


if __name__ == "__main__":
    
    # Define the directory to save the downloaded images
    download_path = os.path.expanduser("~/Desktop/Moroccan-Drought-Segmentation/satellite-images")

    # Ensure the directory exists
    os.makedirs(download_path, exist_ok=True)

    scraper = MapScraper(download_path)
    try:
        scraper.open_website()
        scraper.cancel_cookies()
        scraper.cancel_statistics()
        #scraper.zoom_all()
        scraper.skip_warning()
        scraper.collapse()
        #scraper.options()
        scraper.opacity()
        scraper.click_year_previous()
        scraper.click_month_previous()
        scraper.click_ten_day_period_previous()
        scraper.next()
        # Indicate further actions here
    finally:
        scraper.close_browser()
