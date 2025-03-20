#Imports for automatic chromedriver update
from io import StringIO
import zipfile, os, logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a'),
        logging.StreamHandler()
    ]
)

CHROMEDRIVER_PATH = '.'
EXTRACTION_PATH = os.path.join(".","chromedriver.zip")

def get_update_url(platform):
    """
    Find the most recent chromedriver download link for the specified platform.

    :param platform: The platform for which to get the chromedriver (e.g., 'linux64', 'mac-arm64', 'mac-x64', 'win32', 'win64').
    :return: The URL of the most recent chromedriver download.
    :raises ValueError: If the platform is not in the target list.
    """
    
    #Find the most recent chromedriver download link from https://googlechromelabs.github.io/chrome-for-testing/#stable
    targ = ['linux64','mac-arm64','mac-x64','win32','win64']
    if platform not in targ:
        raise ValueError(f"Platform must be a download type in: {targ}")
    #Use requests module and bs4 to to parse html without a chromedriver
    url = 'https://googlechromelabs.github.io/chrome-for-testing/#stable'
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, "html.parser")
    tables = soup.find_all('table')
    df = pd.read_html(StringIO(str(tables)))[1]
    #Filter the website's table to get chromedriver for the input platform (will always be one row)
    df = df[(df["Binary"] == "chromedriver") & (df["Platform"] == platform)]
    #Get the URL element from this table
    return df.iloc[0]["URL"]
def download_zip_file(platform):
    """
    Download the most recent zip file of the chromedriver for the specified platform.

    :param platform: The platform for which to download the chromedriver.
    """
    url = get_update_url(platform)
    with requests.get(url,stream = True) as r:
        r.raise_for_status()
        #Download the zip file in chunks
        with open(EXTRACTION_PATH, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
def extract_specific_file(zip_file_path, platform, extract_to='.'):
    """
    Unzip the downloaded file and move the chromedriver to the specified location.

    :param zip_file_path: The path to the zip file.
    :param platform: The platform for which the chromedriver was downloaded.
    :param extract_to: The directory to extract the chromedriver to.
    """
    # Open the zip file in read mode
    to_extract = ''
    if platform == 'mac-arm64':
        to_extract = f'chromedriver-{platform}/chromedriver' #Python still interprets this as UNIX style joins, regardless of OS
    else:
        to_extract = f'chromedriver-{platform}/chromedriver.exe' #Python still interprets this as UNIX style joins, regardless of OS
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Get the list of files in the zip
        zip_contents = zip_ref.namelist()
        print(zip_contents)
        
        print(to_extract)
        # Check if the specific file is in the zip file
        if to_extract in zip_contents:
            # Extract the specific file to the desired location
            with zip_ref.open(to_extract) as source, open(os.path.join(extract_to, 'chromedriver.exe'), 'wb') as target:
                target.write(source.read())
            print(f"Extracted 'chromedriver.exe' to: {os.path.abspath(os.path.join(extract_to, 'chromedriver.exe'))}")
        else:
            print("File 'chromedriver.exe' not found in the zip archive.")
def update_driver(platform):
    """
    Update the chromedriver for the specified platform.

    :param platform: The platform for which to update the chromedriver.
    """
    download_zip_file(platform)
    extract_specific_file(os.path.join(".","chromedriver.zip"),platform,CHROMEDRIVER_PATH)
    os.remove(os.path.join(".","chromedriver.zip"))
