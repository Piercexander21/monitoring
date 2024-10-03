from flask import Flask, render_template, jsonify, send_file
import pytesseract
from PIL import Image
from selenium.webdriver.chrome.service import Service
import os
import re
import json
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import matplotlib.pyplot as plt
from io import BytesIO



app = Flask(__name__)

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Facebook credentials (replace these with valid credentials)
FB_EMAIL = "piercexandergiron.ih@gmail.com"
FB_PASSWORD = "Piercexander_21"

# Instagram credentials
IG_USERNAME = "piercexandergiron.ih@gmail.com"
IG_PASSWORD = "piercexander21"

# Twitter credentials
TWITTER_USERNAME = "@Ai_automation21"
TWITTER_PASSWORD = "piercexander21"

# Facebook pages to scrape
FACEBOOK_PAGES = [
    {"url": "https://www.facebook.com/hontiverosrisa", "name": "Hontiveros Risa"},
    {"url": "https://www.facebook.com/WilbertLee2025", "name": "Wilbert Lee"},
    {"url": "https://www.facebook.com/cheldiokno", "name": "Chel Diokno"},
    {"url": "https://www.facebook.com/ROBINPADILLA.OFFICIAL", "name": "Robin Padilla"},
    {"url": "https://www.facebook.com/iamlorenlegarda", "name": "Loren Legarda"},
    {"url": "https://www.facebook.com/raffytulfoinaction", "name": "Raffy Tulfo"},
    {"url": "https://www.facebook.com/officialchizescudero", "name": "Chiz Escudero"},
    {"url": "https://www.facebook.com/SecMarkVillar", "name": "Mark Villar"},
    {"url": "https://www.facebook.com/alanpetercayetano", "name": "Alan Peter Cayetano"},
    {"url": "https://www.facebook.com/migzzubiri", "name": "Migz Zubiri"},
    {"url": "https://www.facebook.com/senatorbonggo", "name": "Bong Go"},
    {"url": "https://www.facebook.com/papaseclarrygadon/", "name": "Larry Gadon"},
    {"url": "https://www.facebook.com/Gringo.Honasan", "name": "Gringo Honasan"},
    {"url": "https://www.facebook.com/HarryRoque", "name": "Harry Roque"},
    {"url": "https://www.facebook.com/GeneralEleazar/", "name": "Guillermo Eleazar"},
    {"url": "https://www.facebook.com/giboteodoro/", "name": "Gilbert Teodoro"},
    {"url": "https://www.facebook.com/BenignoBamAquino/", "name": "Bam aquino"},
    {"url": "https://www.facebook.com/bongrevillajrph/", "name": "Bong Revilla"},
    {"url": "https://www.facebook.com/jinggoyestrada/", "name": "Jinggoy Estrada"},
    {"url": "https://www.facebook.com/joelvillanueva.ph/", "name": "Joel Villanueva"},
]

# YouTube channels to scrape
YOUTUBE_CHANNELS = [
    {"url": "https://www.youtube.com/@RisaHontiverosOfficial", "name": "Hontiveros Risa"},
    {"url": "https://www.youtube.com/@WilbertLee2025", "name": "Wilbert Lee"},
    {"url": "https://www.youtube.com/@attycheldiokno", "name": "Chel Diokno"},
    {"url": "https://www.youtube.com/channel/UCZ60pZNeTeD9pTc64oGOO-A", "name": "Robin Padilla"},
    {"url": "https://www.youtube.com/@senatorlorenlegarda", "name": "Loren Legarda"},
    {"url": "https://www.youtube.com/@RaffyTulfoInAction", "name": "Raffy Tulfo"},
    {"url": "https://www.youtube.com/@ChizEscuderoOfficial", "name": "Chiz Escudero"},
    {"url": "https://www.youtube.com/@senmarkvillar", "name": "Mark Villar"},
    {"url": "https://www.youtube.com/@Alanpetercayetano", "name": "Alan Peter Cayetano"},
    {"url": "https://www.youtube.com/@MigzZubiriYT", "name": "Migz Zubiri"},
    {"url": "https://www.youtube.com/@TESDAMAN", "name": "Joel Villanueva"},
    {"url": "https://www.youtube.com/c/JinggoyEstradaOfficial", "name": "Jinggoy Estrada"},
    {"url": "https://www.youtube.com/@BongRevillajrph", "name": "Bong Revilla"},
    {"url": "https://www.youtube.com/@herbertbautistaofficial2945", "name": "Herbert Bautista"},
    {"url": "https://www.youtube.com/user/giboteodoro", "name": "Gilbert Teodoro"},
    {"url": "https://www.youtube.com/@attyharryroque", "name": "Harry Roque"},
    {"url": "https://www.youtube.com/@gringohonasan8995", "name": "Gringo Honasan"},
    {"url": "https://www.youtube.com/@atty.larrygadon9341", "name": "Larry Gadon"},
    {"url": "https://www.youtube.com/@senatorbonggo", "name": "Bong Go"},
    {"url": "https://www.youtube.com/c/kikopangilinan", "name": "Kiko Pangilinan"},
]

# Instagram profiles to scrape
INSTAGRAM_PROFILES = [
    {"url": "https://www.instagram.com/hontiverosrisa/?hl=en", "name": "Hontiveros Risa"},
    {"url": "https://www.instagram.com/wilbertlee2025/?hl=en", "name": "Wilbert Lee"},
    {"url": "https://www.instagram.com/senatorbonggo/?hl=en", "name": "Bong Go"},
    {"url": "https://www.instagram.com/cheldiokno/?hl=en", "name": "Chel Diokno"},
    {"url": "https://www.instagram.com/bamaquino/?hl=en", "name": "Bam Aquino"},
    {"url": "https://www.instagram.com/robinhoodpadilla/?hl=en", "name": "Robin Padilla"},
    {"url": "https://www.instagram.com/raffytulfoinaction/?hl=en", "name": "Raffy Tulfo"},
    {"url": "https://www.instagram.com/escuderochiz/?hl=en", "name": "Chiz Escudero"},
    {"url": "https://www.instagram.com/iamlorenlegarda/?hl=en", "name": "Loren Legarda"},
    {"url": "https://www.instagram.com/senmarkvillar/?hl=en", "name": "Mark Villar"},
    {"url": "https://www.instagram.com/kiko.pangilinan/?hl=en", "name": "Kiko Pangilinan"},
    {"url": "https://www.instagram.com/migzzubiri/?hl=en", "name": "Migz Zubiri"},
    {"url": "https://www.instagram.com/joelvillanueva/?hl=en", "name": "Joel Villanueva"},
    {"url": "https://www.instagram.com/jinggoyestrada_/", "name": "Jinggoy Estrada"},
    {"url": "https://www.instagram.com/bongrevillajrph/?hl=en", "name": "Bong Revilla"},
    {"url": "https://www.instagram.com/herbertbautista/", "name": "Herbert Bautista"},
    {"url": "https://www.instagram.com/giboteodoroph/?hl=en", "name": "Gilbert Teodoro"},
    {"url": "https://www.instagram.com/harryroque/?hl=en", "name": "Harry Roque"},
    {"url": "https://www.instagram.com/Gringo_Honasan/", "name": "Gringo Honasan"},
    {"url": "https://www.instagram.com/atty.larrygadon/?hl=en", "name": "Larry Gadon"},
]

TWITTER_PROFILES = [
    {"url": "https://x.com/risahontiveros", "name": "Hontiveros Risa"},
    {"url": "https://twitter.com/wilbertlee2025", "name": "Wilbert Lee"},
    {"url": "https://twitter.com/SenatorBongGo", "name": "Bong Go"},
    {"url": "https://twitter.com/ChelDiokno", "name": "Chel Diokno"},
    {"url": "https://twitter.com/bamaquino", "name": "Bam Aquino"},
    {"url": "https://twitter.com/senrobinhood", "name": "Robin Padilla"},
    {"url": "https://twitter.com/IdolRaffyTulfo", "name": "Raffy Tulfo"},
    {"url": "https://twitter.com/saychiz", "name": "Chiz Escudero"},
    {"url": "https://twitter.com/loren_legarda", "name": "Loren Legarda"},
    {"url": "https://x.com/jvejercito", "name": "JV Ejercito"},
    {"url": "https://twitter.com/migzzubiri", "name": "Migz Zubiri"},
    {"url": "https://twitter.com/senatorjoelv", "name": "Joel Villanueva"},
    {"url": "https://x.com/jinggoyestrada_?lang=en", "name": "Jinggoy Estrada"},
    {"url": "https://twitter.com/senatorrevilla", "name": "Bong Revilla"},
    {"url": "https://twitter.com/giboteodoro", "name": "Gilbert Teodoro"},
    {"url": "https://twitter.com/WinGatchalian74", "name": "Win Gachalian"},
    {"url": "https://twitter.com/attyharryroque", "name": "Harry Roque"},
    {"url": "https://twitter.com/SenatorBinay", "name": "Nancy Binay"},
    {"url": "https://x.com/gringo_honasan", "name": "Gringo Honasan"},
    {"url": "https://twitter.com/generaleleazar", "name": "Guillermo Eleazar"},
]

# TikTok profiles to scrape
TIKTOK_PROFILES = [
    {"url": "https://www.tiktok.com/@wilbertlee2025", "name": "Wilbert Lee"},
    {"url": "https://www.tiktok.com/@senrisahontiveros", "name": "Hontiveros Risa"},
    {"url": "https://www.tiktok.com/@attycheldiokno", "name": "Chel Diokno"},
    {"url": "https://www.tiktok.com/@senatorrobinpadilla", "name": "Robin Padilla"},
    {"url": "https://www.tiktok.com/@loren_legarda", "name": "Loren Legarda"},
    {"url": "https://www.tiktok.com/@raffytulfoinaction", "name": "Raffy Tulfo"},
    {"url": "https://www.tiktok.com/@chizescudero", "name": "Chiz Escudero"},
    {"url": "https://www.tiktok.com/@senmarkvillar", "name": "Mark Villar"},
    {"url": "https://www.tiktok.com/@migzzubiritk", "name": "Migz Zubiri"},
    {"url": "https://www.tiktok.com/@senatorbonggo", "name": "Bong Go"},
    {"url": "https://www.tiktok.com/@attylorenzo_larry_gadon", "name": "Larry Gadon"},
    {"url": "https://www.tiktok.com/@gringo_honasan", "name": "Gringo Honasan"},
    {"url": "https://www.tiktok.com/@attyharryroque", "name": "Harry Roque"},
    {"url": "https://www.tiktok.com/@gilbertteodorojr", "name": "Gilbert Teodoro"},
    {"url": "https://www.tiktok.com/@bongrevillajr", "name": "Bong Revilla"},
    {"url": "https://www.tiktok.com/@kiko.pangilinan", "name": "Kiko Pangilinan"},
    {"url": "https://www.tiktok.com/@bamaquino.ph", "name": "Bam Aquino"},
    {"url": "https://www.tiktok.com/@wingatchalian74", "name": "Win Gachalian"},
    {"url": "https://www.tiktok.com/@senatorjoelvillanueva", "name": "Joel Villanueva"},
    {"url": "https://www.tiktok.com/@jinggoyestrada_", "name": "Jinggoy Estrada"},
]

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH = "chromedriver.exe"

# Initialize the driver for scraping
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def initialize_tiktok_driver():
    options = Options()
    # Do NOT add --headless, so the browser will pop up and be visible
    options.add_argument("--disable-notifications")  # Disable notifications
    driver_service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver


def login_to_facebook(driver):
    try:
        driver.get("https://www.facebook.com/")
        email_elem = driver.find_element(By.ID, "email")
        email_elem.send_keys(FB_EMAIL)
        password_elem = driver.find_element(By.ID, "pass")
        password_elem.send_keys(FB_PASSWORD)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(5)
    except Exception as e:
        print(f"Error during Facebook login: {e}")

def login_to_instagram(driver):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        username_elem = driver.find_element(By.NAME, "username")
        username_elem.send_keys(IG_USERNAME)
        password_elem = driver.find_element(By.NAME, "password")
        password_elem.send_keys(IG_PASSWORD)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(5)
    except Exception as e:
        print(f"Error during Instagram login: {e}")

def capture_screenshot(driver, page_url):
    try:
        driver.get(page_url)
        time.sleep(5)
        screenshot_path = os.path.join('static', f'screenshot_{page_url.split("/")[-2]}.png')
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot for {page_url}: {e}")
        return None

def capture_tiktok_screenshot(driver, page_url):
    try:
        # Ensure the 'static' directory exists
        if not os.path.exists('static'):
            os.makedirs('static')

        print(f"Navigating to TikTok profile: {page_url}")  # Debug log

        # Navigate to the TikTok profile URL
        driver.get(page_url)
        time.sleep(10)  # Wait for the page to fully load

        # Capture the screenshot
        screenshot_path = os.path.join('static', f'screenshot_{page_url.split("/")[-1]}.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")  # Debug message

        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot for {page_url}: {e}")
        return None


def capture_twitter_screenshot(driver, page_url):
    try:
        # Ensure the 'static' directory exists
        if not os.path.exists('static'):
            os.makedirs('static')

        # Step 1: Log in to Twitter/X if necessary
        driver.get("https://twitter.com/login")  # Twitter/X login page
        time.sleep(5)  # Wait for the login page to load

        # Find login form elements and input credentials
        try:
            username_input = driver.find_element(By.NAME, "text")
            username_input.send_keys(TWITTER_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for the password field to appear

            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)  # Wait for login to complete
        except Exception as e:
            print(f"Login error: {e}")

        # Step 2: Navigate to the Twitter profile URL
        driver.get(page_url)
        time.sleep(5)  # Wait for the page to fully load

        # Step 3: Zoom the page to 125%
        driver.execute_script("document.body.style.zoom='125%'")
        time.sleep(2)  # Wait for zoom effect

        # Step 4: Scroll down the page
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
        time.sleep(2)  # Wait for scrolling

        # Step 5: Capture the screenshot
        screenshot_path = os.path.join('static', f'screenshot_{page_url.split("/")[-2]}.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")  # Debug message

        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot for {page_url}: {e}")
        return None


def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        print(f"Error extracting text from image {image_path}: {e}")
        return ""

def parse_extracted_text(text, platform):
    if platform == 'facebook':
        followers_match = re.search(r'(\d+\.?\d*[KkMm]?)\s*followers', text)
    elif platform == 'instagram':
        followers_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+\.?\d*[KkMm]?)\s*followers', text)
    elif platform == 'twitter':
        followers_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+\.?\d*[KkMm]?)\s*[Ff]ollowers', text)
    elif platform == 'tiktok':
        followers_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+\.?\d*[KkMm]?)\s*Followers', text)
    else:
        followers_match = re.search(r'(\d+\.?\d*[KkMm]?)\s*subscribers', text)

    if followers_match:
        return followers_match.group(1)
    return "Count not found"

# Capture data for Facebook
def capture_facebook_pages():
    driver = initialize_driver()
    login_to_facebook(driver)
    all_pages_data = []
    for page in FACEBOOK_PAGES:
        screenshot_path = capture_screenshot(driver, page["url"])
        if screenshot_path:
            extracted_text = extract_text_from_image(screenshot_path)
            followers = parse_extracted_text(extracted_text, 'facebook')
            all_pages_data.append({
                "page_name": page["name"],
                "followers": followers,
                "url": page["url"]
            })
    driver.quit()
    return all_pages_data

def capture_tiktok_profiles():
    driver = initialize_tiktok_driver()
    all_profiles_data = []
    for profile in TIKTOK_PROFILES:
        screenshot_path = capture_tiktok_screenshot(driver, profile["url"])
        if screenshot_path:
            extracted_text = extract_text_from_image(screenshot_path)
            followers = parse_extracted_text(extracted_text, 'tiktok')
            all_profiles_data.append({
                "profile_name": profile["name"],
                "followers": followers,
                "url": profile["url"]
            })
    driver.quit()
    return all_profiles_data

# Capture data for YouTube
def capture_youtube_channels():
    driver = initialize_driver()
    all_channels_data = []
    for channel in YOUTUBE_CHANNELS:
        screenshot_path = capture_screenshot(driver, channel["url"])
        if screenshot_path:
            extracted_text = extract_text_from_image(screenshot_path)
            subscribers = parse_extracted_text(extracted_text, 'youtube')
            all_channels_data.append({
                "channel_name": channel["name"],
                "subscribers": subscribers,
                "url": channel["url"]
            })
    driver.quit()
    return all_channels_data

# Capture data for Instagram
def capture_instagram_profiles():
    driver = initialize_driver()
    login_to_instagram(driver)
    all_profiles_data = []
    for profile in INSTAGRAM_PROFILES:
        screenshot_path = capture_screenshot(driver, profile["url"])
        if screenshot_path:
            extracted_text = extract_text_from_image(screenshot_path)
            followers = parse_extracted_text(extracted_text, 'instagram')
            all_profiles_data.append({
                "profile_name": profile["name"],
                "followers": followers,
                "url": profile["url"]
            })
    driver.quit()
    return all_profiles_data

def capture_twitter_profiles():
    driver = initialize_driver()
    all_profiles_data = []
    for profile in TWITTER_PROFILES:
        screenshot_path = capture_twitter_screenshot(driver, profile["url"])
        if screenshot_path:
            extracted_text = extract_text_from_image(screenshot_path)
            followers = parse_extracted_text(extracted_text, 'twitter')
            all_profiles_data.append({
                "profile_name": profile["name"],
                "followers": followers,
                "url": profile["url"]
            })
    driver.quit()
    return all_profiles_data

# Routes for home, Facebook, YouTube, Twitter, and Instagram capture and graphs
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/youtube')
def youtube():
    return render_template('youtube.html')
@app.route('/instagram')
def instagram():
    return render_template('instagram.html')
@app.route('/twitter')
def twitter():
    return render_template('twitter.html')
@app.route('/tiktok')
def tiktok():
    return render_template('tiktok.html')

@app.route('/combine')
def combine():
    return render_template('combinedreport.html')
# Route to capture Facebook data
@app.route('/capture', methods=['GET'])
def capture_and_extract():
    # Path to store the extracted data
    json_file_path = os.path.join('static', 'extracted_data.json')
    archive_folder = os.path.join('static', 'archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Move the current extracted_data.json to the archive folder if it exists
    # Move the current extracted_data.json to the archive folder and replace extracted_data2.json if it exists
    if os.path.exists(json_file_path):
        archive_file = os.path.join(archive_folder, 'extracted_data2.json')

        # Remove the old archived file if it exists
        if os.path.exists(archive_file):
            os.remove(archive_file)

        # Move current extracted_data.json to archive and rename it
        shutil.move(json_file_path, archive_file)

    # Capture new Facebook data
    all_pages_data = capture_facebook_pages()
    print(all_pages_data)  # Debugging

    # Store new data in the main JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_pages_data, json_file)

    # Update the combined report after capturing Facebook data
    generate_combined_report()

    return jsonify(all_pages_data)



# Route to capture YouTube data
@app.route('/youtube_capture', methods=['GET'])
def capture_youtube_data():
    # Path to store the extracted data
    json_file_path = os.path.join('static', 'youtube_data.json')
    archive_folder = os.path.join('static', 'youtube_archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Move the current youtube_data.json to the archive folder and replace youtube_data2.json if it exists
    if os.path.exists(json_file_path):
        archive_file_2 = os.path.join(archive_folder, 'youtube_data2.json')
        archive_file_1 = os.path.join(archive_folder, 'youtube_data1.json')

        # Remove the old archived file if it exists
        if os.path.exists(archive_file_2):
            os.remove(archive_file_2)

        # Move youtube_data1.json to youtube_data2.json if it exists
        if os.path.exists(archive_file_1):
            shutil.move(archive_file_1, archive_file_2)

        # Move current youtube_data.json to youtube_data1.json
        shutil.move(json_file_path, archive_file_1)

    # Capture new YouTube data
    all_channels_data = capture_youtube_channels()  # Assuming capture_youtube_channels is your function to capture YouTube data
    print(all_channels_data)  # Debugging

    # Store new data in the main JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_channels_data, json_file)

        # Update the combined report after capturing Facebook data
    generate_combined_report()

    return jsonify(all_channels_data)

@app.route('/capture_tiktok', methods=['GET'])
def capture_tiktok_data():
    # Path to store the extracted TikTok data
    json_file_path = os.path.join('static', 'tiktok_data.json')
    archive_folder = os.path.join('static', 'tiktok_archive')

    # Ensure the TikTok archive folder exists
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Handle the archiving process:
    # - Keep tiktok_data1.json as the oldest.
    # - Overwrite tiktok_data2.json with the latest data.
    if os.path.exists(json_file_path):
        archive_file_1 = os.path.join(archive_folder, 'tiktok_data1.json')
        archive_file_2 = os.path.join(archive_folder, 'tiktok_data2.json')

        # If tiktok_data1.json doesn't exist, create it first (this will remain untouched)
        if not os.path.exists(archive_file_1):
            shutil.move(json_file_path, archive_file_1)
        else:
            # If tiktok_data1.json exists, replace tiktok_data2.json with the new data
            if os.path.exists(archive_file_2):
                os.remove(archive_file_2)
            shutil.move(json_file_path, archive_file_2)

    # Capture new TikTok data
    all_profiles_data = capture_tiktok_profiles()
    print(all_profiles_data)  # Debugging

    # Store new data in the main TikTok JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_profiles_data, json_file)

    # Update the combined report after capturing Facebook data
    generate_combined_report()

    return jsonify(all_profiles_data)


@app.route('/capture_instagram', methods=['GET'])
def capture_instagram_data():
    # Path to store the extracted data
    json_file_path = os.path.join('static', 'instagram_data.json')
    archive_folder = os.path.join('static', 'instagram_archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Move the current instagram_data.json to the archive folder and replace instagram_data2.json if it exists
    if os.path.exists(json_file_path):
        archive_file_2 = os.path.join(archive_folder, 'instagram_data2.json')
        archive_file_1 = os.path.join(archive_folder, 'instagram_data1.json')

        # Remove the old archived file if it exists
        if os.path.exists(archive_file_2):
            os.remove(archive_file_2)

        # Move instagram_data1.json to instagram_data2.json if it exists
        if os.path.exists(archive_file_1):
            shutil.move(archive_file_1, archive_file_2)

        # Move current instagram_data.json to instagram_data1.json
        shutil.move(json_file_path, archive_file_1)

    # Capture new Instagram data
    all_profiles_data = capture_instagram_profiles()  # Assuming capture_instagram_profiles is your function to capture Instagram data
    print(all_profiles_data)  # Debugging

    # Store new data in the main JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_profiles_data, json_file)

    # Update the combined report after capturing Facebook data
    generate_combined_report()

    return jsonify(all_profiles_data)


@app.route('/capture_twitter', methods=['GET'])
def capture_twitter_data():
    # Path to store the extracted data
    json_file_path = os.path.join('static', 'twitter_data.json')
    archive_folder = os.path.join('static', 'twitter_archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Move the current twitter_data.json to the archive folder and replace twitter_data2.json if it exists
    if os.path.exists(json_file_path):
        archive_file_2 = os.path.join(archive_folder, 'twitter_data2.json')
        archive_file_1 = os.path.join(archive_folder, 'twitter_data1.json')

        # Remove the old archived file if it exists
        if os.path.exists(archive_file_2):
            os.remove(archive_file_2)

        # Move twitter_data1.json to twitter_data2.json if it exists
        if os.path.exists(archive_file_1):
            shutil.move(archive_file_1, archive_file_2)

        # Move current twitter_data.json to twitter_data1.json
        shutil.move(json_file_path, archive_file_1)

    # Capture new Twitter data
    all_profiles_data = capture_twitter_profiles()  # Assuming capture_twitter_profiles is your function to capture Twitter data
    print(all_profiles_data)  # Debugging

    # Store new data in the main JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_profiles_data, json_file)

    # Update the combined report after capturing Facebook data
    generate_combined_report()

    return jsonify(all_profiles_data)

# Route to display a graph of Instagram followers
@app.route('/graph_instagram')
def graph_instagram_followers():
    all_profiles_data = capture_instagram_profiles()
    profile_names = [profile["profile_name"] for profile in all_profiles_data]
    followers = []
    for profile in all_profiles_data:
        if 'M' in profile["followers"]:
            followers.append(float(profile["followers"].replace('M', '')) * 1_000_000)
        elif 'K' in profile["followers"]:
            followers.append(float(profile["followers"].replace('K', '')) * 1_000)
        else:
            followers.append(float(profile["followers"]))
    fig, ax = plt.subplots()
    ax.bar(profile_names, followers, color='lightblue')
    ax.set_xlabel('Instagram Profiles')
    ax.set_ylabel('Number of Followers')
    ax.set_title('Instagram Followers')
    plt.xticks(rotation=45, ha="right")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Route to display a graph of YouTube subscribers
@app.route('/graph_youtube')
def graph_youtube_followers():
    all_channels_data = capture_youtube_channels()
    channel_names = [channel["channel_name"] for channel in all_channels_data]
    subscribers = []
    for channel in all_channels_data:
        if 'M' in channel["subscribers"]:
            subscribers.append(float(channel["subscribers"].replace('M', '')) * 1_000_000)
        elif 'K' in channel["subscribers"]:
            subscribers.append(float(channel["subscribers"].replace('K', '')) * 1_000)
        else:
            subscribers.append(float(channel["subscribers"]))
    fig, ax = plt.subplots()
    ax.bar(channel_names, subscribers, color='skyblue')
    ax.set_xlabel('YouTube Channels')
    ax.set_ylabel('Number of Subscribers')
    ax.set_title('YouTube Subscribers')
    plt.xticks(rotation=45, ha="right")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Function to compare two JSON files and generate a report
def compare_follower_data(archive_file, current_file, profile_key='page_name'):
    try:
        with open(archive_file, 'r') as old_file:
            old_data = json.load(old_file)

        with open(current_file, 'r') as new_file:
            new_data = json.load(new_file)
    except Exception as e:
        print(f"Error loading JSON files: {e}")
        return []

    report = []

    try:
        for new_profile in new_data:
            old_profile = next((profile for profile in old_data if profile[profile_key] == new_profile[profile_key]), None)

            if old_profile:
                old_followers = parse_follower_count(old_profile['followers'])
                new_followers = parse_follower_count(new_profile['followers'])

                if new_followers is not None and old_followers is not None:
                    # Ensure if both old_followers and new_followers are zero or if no data is present
                    if new_followers == 0 and old_followers == 0:
                        gain_or_loss_str = '0'
                    else:
                        gain_or_loss = int(new_followers - old_followers)

                        # Add "+" for gain and "-" for loss, or just "0" for no change
                        if gain_or_loss > 0:
                            gain_or_loss_str = f"+{gain_or_loss}"
                        elif gain_or_loss == 0:
                            gain_or_loss_str = "0"
                        else:
                            gain_or_loss_str = str(gain_or_loss)



                    report.append({
                        profile_key: new_profile[profile_key],
                        'old_followers': old_followers,
                        'new_followers': new_followers,
                        'gain_or_loss': gain_or_loss_str
                    })
    except KeyError as e:
        print(f"KeyError: {e} not found in the data.")
        return []

    return report


# Function to compare two JSON files and generate a TikTok report
def compare_tiktok_follower_data(archive_file, current_file, profile_key='profile_name'):
    with open(archive_file, 'r') as old_file:
        old_data = json.load(old_file)

    with open(current_file, 'r') as new_file:
        new_data = json.load(new_file)

    report = []

    # Compare each profile's followers
    for new_profile in new_data:
        old_profile = next((profile for profile in old_data if profile[profile_key] == new_profile[profile_key]), None)

        if old_profile:
            old_followers = parse_follower_count(old_profile['followers'])
            new_followers = parse_follower_count(new_profile['followers'])

            if new_followers is not None and old_followers is not None:
                # Ensure if both old_followers and new_followers are zero or if no data is present
                if new_followers == 0 and old_followers == 0:
                    gain_or_loss_str = '0'
                else:
                    gain_or_loss = int(new_followers - old_followers)

                    # Add "+" for gain and "-" for loss, or just "0" for no change
                    if gain_or_loss > 0:
                        gain_or_loss_str = f"+{gain_or_loss}"
                    elif gain_or_loss == 0:
                        gain_or_loss_str = "0"
                    else:
                        gain_or_loss_str = str(gain_or_loss)

                report.append({
                    profile_key: new_profile[profile_key],
                    'old_followers': old_followers,
                    'new_followers': new_followers,
                    'gain_or_loss': gain_or_loss_str
                })

    return report

def compare_youtube_follower_data(archive_file, current_file, profile_key='channel_name'):
    with open(archive_file, 'r') as old_file:
        old_data = json.load(old_file)

    with open(current_file, 'r') as new_file:
        new_data = json.load(new_file)

    report = []

    # Compare each profile's followers
    for new_profile in new_data:
        old_profile = next((profile for profile in old_data if profile[profile_key] == new_profile[profile_key]), None)

        if old_profile:
            old_subscribers = parse_follower_count(old_profile['subscribers'])
            new_subscribers = parse_follower_count(new_profile['subscribers'])

            if new_subscribers is not None and old_subscribers is not None:

                if new_subscribers == 0 and old_subscribers == 0:
                    gain_or_loss_str = '0'
                else:
                    gain_or_loss = int(new_subscribers - old_subscribers)

                    # Add "+" for gain and "-" for loss, or just "0" for no change
                    if gain_or_loss > 0:
                        gain_or_loss_str = f"+{gain_or_loss}"
                    elif gain_or_loss == 0:
                        gain_or_loss_str = "0"
                    else:
                        gain_or_loss_str = str(gain_or_loss)

                report.append({
                    profile_key: new_profile[profile_key],
                    'old_subscribers': old_subscribers,
                    'new_subscribers': new_subscribers,
                    'gain_or_loss': gain_or_loss_str
                })

    return report

def compare_instagram_follower_data(archive_file, current_file, profile_key='profile_name'):
    with open(archive_file, 'r') as old_file:
        old_data = json.load(old_file)

    with open(current_file, 'r') as new_file:
        new_data = json.load(new_file)

    report = []

    # Compare each profile's followers
    for new_profile in new_data:
        old_profile = next((profile for profile in old_data if profile[profile_key] == new_profile[profile_key]), None)

        if old_profile:
            old_followers = parse_follower_count(old_profile['followers'])
            new_followers = parse_follower_count(new_profile['followers'])

            if new_followers == 0 and old_followers == 0:
                gain_or_loss_str = '0'
            else:
                gain_or_loss = int(new_followers - old_followers)

                # Add "+" for gain and "-" for loss, or just "0" for no change
                if gain_or_loss > 0:
                    gain_or_loss_str = f"+{gain_or_loss}"
                elif gain_or_loss == 0:
                    gain_or_loss_str = "0"
                else:
                    gain_or_loss_str = str(gain_or_loss)

                report.append({
                    profile_key: new_profile[profile_key],
                    'old_followers': old_followers,
                    'new_followers': new_followers,
                    'gain_or_loss': gain_or_loss_str
                })

    return report

# Function to compare two JSON files and generate a report
def compare_twitter_follower_data(archive_file, current_file, profile_key='profile_name'):
    # Open the archived and current data files
    with open(archive_file, 'r') as old_file:
        old_data = json.load(old_file)

    with open(current_file, 'r') as new_file:
        new_data = json.load(new_file)

    report = []

    # Compare each profile's followers
    for new_profile in new_data:
        old_profile = next((profile for profile in old_data if profile[profile_key] == new_profile[profile_key]), None)

        if old_profile:
            old_followers = parse_follower_count(old_profile['followers'])
            new_followers = parse_follower_count(new_profile['followers'])

            if new_followers == 0 and old_followers == 0:
                gain_or_loss_str = '0'
            else:
                gain_or_loss = int(new_followers - old_followers)

                # Add "+" for gain and "-" for loss, or just "0" for no change
                if gain_or_loss > 0:
                    gain_or_loss_str = f"+{gain_or_loss}"
                elif gain_or_loss == 0:
                    gain_or_loss_str = "0"
                else:
                    gain_or_loss_str = str(gain_or_loss)

                report.append({
                    profile_key: new_profile[profile_key],
                    'old_followers': old_followers,
                    'new_followers': new_followers,
                    'gain_or_loss': gain_or_loss_str
                })

    return report


# Helper function to parse follower counts (in case they are formatted with K/M)
def parse_follower_count(follower_str):
    if 'M' in follower_str:
        return float(follower_str.replace('M', '')) * 1_000_000
    elif 'K' in follower_str:
        return float(follower_str.replace('K', '')) * 1_000
    else:
        try:
            return float(follower_str)
        except ValueError:
            return None


@app.route('/generate_report', methods=['GET'])
def generate_report():
    archive_folder = os.path.join('static', 'archive')

    # Ensure archive folder exists
    if not os.path.exists(archive_folder):
        return jsonify({"error": "No archived data found."}), 400

    latest_archive_file = 'extracted_data1.json'  # Replace this with your logic to find the correct archived file
    current_file = os.path.join('static', 'extracted_data.json')

    if not os.path.exists(os.path.join(archive_folder, latest_archive_file)):
        return jsonify({"error": "Archived data file not found."}), 400

    # Generate report by comparing archived and current data
    report = compare_follower_data(os.path.join(archive_folder, latest_archive_file), current_file)

    # Output the report to a file (optional)
    report_file_path = os.path.join('static', 'report.json')
    with open(report_file_path, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    return jsonify(report)

@app.route('/generate_tiktok_report', methods=['GET'])
def generate_tiktok_report():
    archive_folder = os.path.join('static', 'tiktok_archive')

    # Ensure tiktok_archive folder exists
    if not os.path.exists(archive_folder):
        return jsonify({"error": "No archived TikTok data found."}), 400

    # Set the file to compare
    archive_file = os.path.join(archive_folder, 'tiktok_data2.json')  # Archived file to compare against
    current_file = os.path.join('static', 'tiktok_data.json')

    if not os.path.exists(archive_file):
        return jsonify({"error": "Archived TikTok data file not found."}), 400

    # Generate report by comparing archived and current data, using 'profile_name' for TikTok
    report = compare_tiktok_follower_data(archive_file, current_file, profile_key='profile_name')

    # Output the report to a file (optional)
    report_file_path = os.path.join('static', 'tiktok_report.json')
    with open(report_file_path, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    return jsonify(report)

@app.route('/generate_youtube_report', methods=['GET'])
def generate_youtube_report():
    archive_folder = os.path.join('static', 'youtube_archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        return jsonify({"error": "No archived data found."}), 400

    latest_archive_file = 'youtube_data1.json'  # Find the appropriate archived file to compare
    current_file = os.path.join('static', 'youtube_data.json')

    if not os.path.exists(os.path.join(archive_folder, latest_archive_file)):
        return jsonify({"error": "Archived data file not found."}), 400

    # Generate report by comparing archived and current data
    report = compare_youtube_follower_data(
        os.path.join(archive_folder, latest_archive_file),
        current_file,
        profile_key='channel_name'  # YouTube uses 'channel_name'
    )

    # Output the report to a file (optional)
    report_file_path = os.path.join('static', 'youtube_report.json')
    with open(report_file_path, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    return jsonify(report)


@app.route('/generate_instagram_report', methods=['GET'])
def generate_instagram_report():
    archive_folder = os.path.join('static', 'instagram_archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        return jsonify({"error": "No archived data found."}), 400

    latest_archive_file = 'instagram_data1.json'  # Find the appropriate archived file to compare
    current_file = os.path.join('static', 'instagram_data.json')

    if not os.path.exists(os.path.join(archive_folder, latest_archive_file)):
        return jsonify({"error": "Archived data file not found."}), 400

    # Generate report by comparing archived and current data
    report = compare_follower_data(
        os.path.join(archive_folder, latest_archive_file),
        current_file,
        profile_key='profile_name'  # Instagram uses 'profile_name'
    )

    # Output the report to a file (optional)
    report_file_path = os.path.join('static', 'instagram_report.json')
    with open(report_file_path, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    return jsonify(report)

@app.route('/generate_twitter_report', methods=['GET'])
def generate_twitter_report():
    archive_folder = os.path.join('static', 'twitter_archive')

    # Ensure the archive folder exists
    if not os.path.exists(archive_folder):
        return jsonify({"error": "No archived data found."}), 400

    latest_archive_file = 'twitter_data1.json'  # Find the appropriate archived file to compare
    current_file = os.path.join('static', 'twitter_data.json')

    if not os.path.exists(os.path.join(archive_folder, latest_archive_file)):
        return jsonify({"error": "Archived data file not found."}), 400

    # Generate report by comparing archived and current data
    report = compare_twitter_follower_data(
        os.path.join(archive_folder, latest_archive_file),
        current_file,
        profile_key='profile_name'  # Twitter uses 'profile_name'
    )

    # Output the report to a file (optional)
    report_file_path = os.path.join('static', 'twitter_report.json')
    with open(report_file_path, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    return jsonify(report)

@app.route('/generate_combined_report', methods=['GET'])
def generate_combined_report():
    combined_data = []

    # Load all the social media data
    facebook_data = load_social_media_data('static/extracted_data.json')
    instagram_data = load_social_media_data('static/instagram_data.json')
    twitter_data = load_social_media_data('static/twitter_data.json')
    youtube_data = load_social_media_data('static/youtube_data.json')
    tiktok_data = load_social_media_data('static/tiktok_data.json')

    # Load all the report data for gain/loss
    facebook_report = load_social_media_data('static/report.json')
    instagram_report = load_social_media_data('static/instagram_report.json')
    twitter_report = load_social_media_data('static/twitter_report.json')
    youtube_report = load_social_media_data('static/youtube_report.json')
    tiktok_report = load_social_media_data('static/tiktok_report.json')

    # Collect all unique candidate names across all platforms
    all_candidates = set(
        [candidate['page_name'] for candidate in facebook_data] +
        [candidate['profile_name'] for candidate in instagram_data] +
        [candidate['profile_name'] for candidate in twitter_data] +
        [candidate['profile_name'] for candidate in tiktok_data] +
        [candidate['channel_name'] for candidate in youtube_data]  # YouTube uses 'channel_name'
    )

    # Combine data by candidate name and create graphs for each
    for candidate_name in all_candidates:
        candidate_data = {
            'name': candidate_name,
            'facebook_followers': get_followers_by_candidate(facebook_data, candidate_name, 'page_name'),
            'facebook_change': get_gain_loss_from_report(facebook_report, candidate_name),
            'instagram_followers': get_followers_by_candidate(instagram_data, candidate_name, 'profile_name'),
            'instagram_change': get_gain_loss_from_report(instagram_report, candidate_name),
            'twitter_followers': get_followers_by_candidate(twitter_data, candidate_name, 'profile_name'),
            'twitter_change': get_gain_loss_from_report(twitter_report, candidate_name),
            'tiktok_followers': get_followers_by_candidate(tiktok_data, candidate_name, 'profile_name'),
            'tiktok_change': get_gain_loss_from_report(tiktok_report, candidate_name),
            'youtube_subscribers': get_followers_by_candidate(youtube_data, candidate_name, 'channel_name'), # YouTube uses 'channel_name'
            'youtube_change': get_gain_loss_from_report(youtube_report, candidate_name)
        }

        # Filter out candidates with no data for any social media platform
        if any(candidate_data.values()):
            combined_data.append(candidate_data)

    return jsonify(combined_data)

# Helper function to load the gain/loss from the report
def get_gain_loss_from_report(report_data, candidate_name):
    # Search for the candidate in the report
    for entry in report_data:
        if 'page_name' in entry and entry['page_name'] == candidate_name:
            return entry.get('gain_or_loss', 0)  # Return gain or loss if found, else 0
        if 'profile_name' in entry and entry['profile_name'] == candidate_name:
            return entry.get('gain_or_loss', 0)  # Return gain or loss if found, else 0
        if 'channel_name' in entry and entry['channel_name'] == candidate_name:
            return entry.get('gain_or_loss', 0)  # For YouTube, return gain or loss if found, else 0
    return 0  # If no entry found, return 0

# Helper function to load social media data
def load_social_media_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

# Helper function to get followers or subscribers by candidate
def get_followers_by_candidate(data, candidate_name, name_key):
    for candidate in data:
        if name_key in candidate and candidate[name_key] == candidate_name:
            if 'followers' in candidate:
                return parse_follower_count(candidate['followers'])
            elif 'subscribers' in candidate:
                return parse_follower_count(candidate['subscribers'])
            else:
                return 0
    return 0

# Helper function to parse follower/subscriber counts
def parse_follower_count(follower_str):
    if isinstance(follower_str, str):
        if 'M' in follower_str:
            return float(follower_str.replace('M', '')) * 1_000_000
        elif 'K' in follower_str:
            return float(follower_str.replace('K', '')) * 1_000
        else:
            try:
                return float(follower_str.replace(',', ''))
            except ValueError:
                return 0
    return follower_str


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

