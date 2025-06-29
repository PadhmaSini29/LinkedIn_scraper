from flask import Flask, render_template, request, redirect, url_for
import subprocess
import threading
import os

app = Flask(__name__)
SCRAPER_SCRIPT = os.path.join("scraper", "linkedin_scraper.py")

scraping_status = {"running": False, "message": "Idle"}

def run_scraper():
    global scraping_status
    scraping_status["running"] = True
    scraping_status["message"] = "Scraping in progress..."

    try:
        subprocess.run(["python", SCRAPER_SCRIPT], check=True)
        scraping_status["message"] = "✅ Scraping complete!"
    except subprocess.CalledProcessError as e:
        scraping_status["message"] = f"❌ Scraping failed: {e}"
    finally:
        scraping_status["running"] = False

@app.route("/")
def index():
    return render_template("index.html", status=scraping_status)

@app.route("/start", methods=["POST"])
def start_scraping():
    if not scraping_status["running"]:
        thread = threading.Thread(target=run_scraper)
        thread.start()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
