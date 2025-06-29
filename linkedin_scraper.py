import os
import time
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Config Paths ===
chrome_profile_path = os.path.abspath("temp_chrome_profile")
chromedriver_path = r"C:/Users/lgspa/linkedin-scraper/chromedriver-win64/chromedriver.exe"
json_file_path = "linkedin_profiles.json"
scraped_urls_file = "scraped_urls.txt"

# === Setup WebDriver ===
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={chrome_profile_path}")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
wait = WebDriverWait(driver, 15)

# === Manual Login ===
driver.get("https://www.linkedin.com/login")
input("Please log in to LinkedIn manually and press ENTER to continue...")

# === Scroll to load all connections ===
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
print("📜 Scrolling to load all connections...")
prev_height, same_count, max_same = 0, 0, 5
while same_count < max_same:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        same_count += 1
    else:
        same_count = 0
        prev_height = new_height

# === Collect Profile URLs ===
elements = driver.find_elements(By.CSS_SELECTOR, "a.mn-connection-card__link")
profile_urls = list(set([e.get_attribute("href") for e in elements if e.get_attribute("href")]))
print(f"✅ Found {len(profile_urls)} profiles.")

# === Load already scraped URLs ===
if os.path.exists(scraped_urls_file):
    with open(scraped_urls_file, "r", encoding="utf-8") as f:
        scraped_urls = set(f.read().splitlines())
else:
    scraped_urls = set()

# === Load existing data ===
if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
else:
    existing_data = []

# === Helper Functions ===
def extract_experience():
    try:
        section = driver.find_element(By.XPATH, "//section[.//span[contains(text(),'Experience')]]")
        items = section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")
        experiences = []
        for item in items:
            lines = item.text.split('\n')
            entry = {
                "Title": lines[0] if len(lines) > 0 else "",
                "Company": lines[1] if len(lines) > 1 else "",
                "Type": next((l for l in lines if any(k in l for k in ["Full-time", "Internship", "Part-time"])), ""),
                "Duration": next((l for l in lines if "·" in l or "to" in l), ""),
                "Location": next((l for l in lines if any(p in l for p in ["India", "Remote", "Chennai", "Bangalore"])), ""),
                "Mode": "Remote" if "Remote" in item.text else ("On-site" if "On-site" in item.text else "")
            }
            experiences.append(entry)
        return experiences
    except:
        return []

def extract_education():
    try:
        section = driver.find_element(By.XPATH, "//section[.//span[contains(text(),'Education')]]")
        items = section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")
        educations = []
        for item in items:
            lines = item.text.split('\n')
            edu = {
                "College": lines[0] if len(lines) > 0 else "",
                "Department": lines[2] if len(lines) > 2 else "",
                "Years": next((l for l in lines if any(y in l for y in ["20", "-"])), "")
            }
            educations.append(edu)
        return educations
    except:
        return []

# === Scrape Profiles ===
for url in tqdm(profile_urls, desc="🔍 Scraping profiles"):
    if url in scraped_urls:
        continue

    try:
        driver.get(url)
        time.sleep(3)
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

        try:
            name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))).text.strip()
        except:
            name = ""

        experience = extract_experience()
        education = extract_education()

        profile_data = {
            "Profile URL": url,
            "Name": name,
            "Experience": experience,
            "Education": education
        }

        existing_data.append(profile_data)

        # === Save JSON incrementally ===
        with open(json_file_path, "w", encoding="utf-8") as jf:
            json.dump(existing_data, jf, indent=2, ensure_ascii=False)

        # === Save scraped URL ===
        with open(scraped_urls_file, "a", encoding="utf-8") as sf:
            sf.write(url + "\n")

    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        continue

driver.quit()
print("✅ Done! All scraped data saved.")
