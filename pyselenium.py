import requests
import platform, zipfile, os
from .config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


def get_browser(headless=False):

    driver_path = get_chromedriver()

    if not driver_path:
        return None
    service = ChromeService(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=service, options=options)

    return driver



def get_chromedriver(channel='stable'):

    url = get_chromedriver_url(channel)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    

    if url:

        r = requests.get(url)
        if r.status_code == 200:
            with open('chromedriver.zip', 'wb') as f:
                f.write(r.content)

            with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
                for file in zip_ref.namelist():
                    file_name = file.split('/')[1]
                    if file_name.startswith('chromedriver'):

                        extract_path = os.path.join(script_dir, file_name)

                        with zip_ref.open(file) as file_in_zip, open(extract_path, 'wb') as extracted_file:
                            extracted_file.write(file_in_zip.read())

            os.remove('chromedriver.zip')

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
