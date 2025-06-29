# 🕵️‍♂️ LinkedIn Connection Scraper

A Python-based web scraper using Selenium to extract details (Name, Experience, Education) from your LinkedIn connections.  
Supports **incremental scraping**, **resume after interruption**, and saves results in structured **JSON** format.

---

## 🚀 Features

- ✅ Scrapes name, job experience, and education history
- 🧠 Stores results in structured JSON format
- 🔁 Skips already-scraped profiles (`scraped_urls.txt`)
- 🔒 Uses your real LinkedIn session (manual login)
- 💾 Saves progress live — no data loss on crash/interrupt

---

## 📦 Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver (matching your browser version)
- LinkedIn account (manual login required)

---

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/PadhmaSini29/linkedin-scraper.git
cd linkedin-scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Create a virtual environment if needed:
> ```bash
> python -m venv venv
> venv\Scripts\activate
> ```

### 3. Download ChromeDriver

- Match your Chrome version: https://chromedriver.chromium.org/downloads
- Extract and place it under:
  ```
  ./chromedriver-win64/chromedriver.exe
  ```

---

## 🛠 Configuration

Ensure your folder has this structure:

```
linkedin-scraper/
│
├── linkedin_scraper.py
├── linkedin_profiles.json         ← output JSON file (auto-generated)
├── scraped_urls.txt               ← tracks completed profiles
├── temp_chrome_profile/           ← browser session data
├── chromedriver-win64/
│   └── chromedriver.exe
└── requirements.txt
```

---

## ▶️ Usage

```bash
python linkedin_scraper.py
```

1. A Chrome window opens.
2. **Manually log in** to LinkedIn.
3. Press **ENTER** in the terminal once logged in.
4. Scraper will scroll and collect profile links.
5. Begins scraping each profile and saves them incrementally.

---

## 🧾 Output Format (JSON)

```json
[
  {
    "Profile URL": "https://linkedin.com/in/...",
    "Name": "John Doe",
    "Experience": [
      {
        "Title": "Software Engineer",
        "Company": "Google",
        "Duration": "Jan 2020 - Present",
        "Location": "Remote",
        "Mode": "Remote"
      }
    ],
    "Education": [
      {
        "College": "MIT",
        "Department": "Computer Science",
        "Years": "2015 - 2019"
      }
    ]
  }
]
```

---

## 📌 Notes

- 🔐 This script uses your real session. No scraping credentials or automation login.
- ❌ Do **not share or abuse** this scraper — it’s meant for **personal use**.
- 🛡️ Respect [LinkedIn’s Terms of Service](https://www.linkedin.com/legal/user-agreement).

---

## 🧠 Author

**Your Name**  
[GitHub Profile](https://github.com/PadhmaSini29)


