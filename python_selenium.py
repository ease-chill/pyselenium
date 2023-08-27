from selenium import webdriver
import platform

def automate_browser(url):

    operating_system = check_os()
    if 
    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome()

    # Go to the specified URL
    driver.get(url)

    # Do something with the web page, e.g. find an element and click it
    element = driver.find_element_by_id("my-button")
    element.click()

    # Close the browser
    driver.quit()


def check_os():
    return platform.system()

check_os()


# automate_browser("https://www.google.com")

