import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# --- Setup WebDriver ---
chrome_profile_path = r"C:/Users/lgspa/AppData/Local/Google/Chrome/User Data"
service = Service('C:/Users/lgspa/linkedin-scraper/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={chrome_profile_path}")
options.add_argument("start-maximized")

driver = webdriver.Chrome(service=service, options=options)

# --- Step 1: Manual Login ---
driver.get("https://www.linkedin.com/login")
input("🔐 Log in manually, then press ENTER here to continue...")

# --- Step 2: Go to Connections Page ---
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
time.sleep(5)

# --- Step 3: Scroll to Load Connections ---
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# --- Step 4: Get Profile URLs ---
connections = driver.find_elements(By.CSS_SELECTOR, "a.mn-connection-card__link")
profile_urls = list(set([c.get_attribute('href') for c in connections if c.get_attribute('href')]))

print(f"✅ Found {len(profile_urls)} profile URLs.")

# --- Step 5: Visit Profiles and Scrape Data ---
data = []

for url in profile_urls[:10]:  # Test with 10 profiles first
    print(f"\n🔎 Visiting: {url}")
    driver.get(url)
    time.sleep(4)

    # Scroll to load full profile
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1.5)

    # Name
    try:
        name = driver.find_element(By.TAG_NAME, 'h1').text.strip()
    except:
        name = ""

    # Info/About
    try:
        info = driver.find_element(By.CLASS_NAME, 'text-body-medium.break-words').text.strip()
    except:
        info = ""

    # Experience section (entire block text)
    try:
        exp_elements = driver.find_elements(By.XPATH, "//section[contains(@id, 'experience')]//li")
        experience = "\n".join([e.text.strip() for e in exp_elements if e.text.strip()])
    except:
        experience = ""

    # Education section (entire block text)
    try:
        edu_elements = driver.find_elements(By.XPATH, "//section[contains(@id, 'education')]//li")
        education = "\n".join([e.text.strip() for e in edu_elements if e.text.strip()])
    except:
        education = ""

    data.append({
        "Profile URL": url,
        "Name": name,
        "Info": info,
        "Experience": experience,
        "Education": education
    })

    print("✅ Scraped:", name)

    time.sleep(3)

# --- Step 6: Save to CSV ---
df = pd.DataFrame(data)
df.to_csv("linkedin_profiles.csv", index=False)
print("\n✅ Data saved to linkedin_profiles.csv")

driver.quit()
