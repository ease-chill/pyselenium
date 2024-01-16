import requests
import platform, zipfile, os
from .config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import SessionNotCreatedException



def get_browser(working_dir,headless=False):

    driver_path = get_chromedriver(working_dir)

    if not driver_path:
        return None
    

    service = ChromeService(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")

    driver = None

    try:
        driver = webdriver.Chrome(service=service, options=options)

    except SessionNotCreatedException:
        print("Error: ChromeDriver is outdated. Updating ChromeDriver...")

        os.remove(driver_path)
        driver_path = get_chromedriver(update=True)

        if not driver_path:
            print("Error: Failed to update ChromeDriver.")
            return None

    if driver:
        return driver
    else:
        try:
            driver = webdriver.Chrome(service=service, options=options)
        except SessionNotCreatedException as e:
            print("Error: Failed to start browser after updating ChromeDriver.")
            print(f"Error message: {str(e)}")
            return None
    



def get_chromedriver(working_dir, update=False, channel='stable'):

    url = get_chromedriver_url(channel)


    # Check if chromedriver exists
    platform = get_platform()
    
    if platform == 'win32' or platform == 'win64':
        driver_filename = 'chromedriver.exe'
    else:
        driver_filename = 'chromedriver'

    driver_path = os.path.join(working_dir, driver_filename)


    if os.path.exists(driver_path) and not update:
        set_chromedriver_permissions(driver_path, platform)
        return driver_path
    

    if url:

        r = requests.get(url)
        if r.status_code == 200:
            with open('chromedriver.zip', 'wb') as f:
                f.write(r.content)

            with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
                for file in zip_ref.namelist():
                    file_name = file.split('/')[1]
                    if file_name.startswith('chromedriver'):

                        extract_path = os.path.join(working_dir, file_name)

                        with zip_ref.open(file) as file_in_zip, open(extract_path, 'wb') as extracted_file:
                            extracted_file.write(file_in_zip.read())

            os.remove('chromedriver.zip')

            set_chromedriver_permissions(extract_path, platform)

            return extract_path
        
    return None

def get_chromedriver_url(channel='stable'):

    r = requests.get(LATEST_CHROMEDRIVER_URLS)
    if r.status_code == 200:
        download_url_dict = r.json()
    else:
        download_url_dict = {}

    if not download_url_dict:
        return None

    channel = channel.title()

    pf = get_platform()

    download_urls = download_url_dict['channels'][channel]['downloads']['chromedriver']
    try:
        download_url = [
            download_url['url'] for download_url in download_urls
            if download_url['platform'] == pf
        ][0]
    except:
        return None
    
    return download_url
    


def set_chromedriver_permissions(driver_path, platform):
    if platform == 'win32' or platform == 'win64':
        pass
    else:
        os.chmod(driver_path, 755)

def get_platform():
    os_type = platform.system()
    if os_type == 'Linux':
        os_arch = 'linux64'
    elif os_type == 'Windows':
        arch = platform.machine()
        os_arch = 'win64' if arch.endswith('64') else 'win32'
    elif os_type == 'Darwin':
        arch = platform.machine()
        os_arch = 'mac-arm64' if arch == 'arm64' else 'mac-x64'

    return os_arch
