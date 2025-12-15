# 🔗 Shorty | The Premium Link Chopper

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Blazing%20Fast-009688)
![Status](https://img.shields.io/badge/Status-Live%20%26%20Kicking-success)
![Render](https://img.shields.io/badge/Deployed%20on-Render-black)

> **See it in action:** [https://shorty-the-cutter-url.onrender.com/](https://shorty-the-cutter-url.onrender.com/)

Welcome to **Shorty**. This isn't just another URL shortener; it's a full-stack app I built from the ground up. The goal? To take those nasty, long URLs and chop 'em down into something clean and shareable.

I built this to show off some serious Full Stack skills—combining a high-performance Python backend with a slick, modern frontend. No bloat, just code.

---

## 💡 What's the Deal?

Basically, you feed Shorty a long link (like a YouTube video or a Google Maps location), and it spits out a tiny, unique URL. But it doesn't stop there. 

I hooked it up with a **Dashboard** so you can track how many people are actually clicking your links. It's fully deployed on the cloud, backed by a database, and secured with some solid validation.

### The Highlights:
* **Full Stack & Production Ready:** From the database schema to the CSS animations, everything is linked up and live.
* **Smart Redirection:** Handles HTTP 307 redirects like a champ.
* **VIP Dashboard:** A password-protected Admin Panel to spy on your link stats (clicks, status, original URLs).
* **Bulletproof Validation:** You can't break it with "pizza" or fake links. We validate everything before it hits the DB.

---

## 🛠️ Under the Hood (Tech Stack)

### 🏎️ Backend (The Engine)
* **Python 3.10 & FastAPI:** Chose this because it's blazing fast and handles async requests way better than older frameworks.
* **SQLAlchemy & SQLite:** Managing the data persistence. Every link and click is stored safely.
* **Pydantic:** Using this for data validation. It keeps the data clean and consistent.
* **Security:** Implemented HTTP Basic Auth for the Admin panel. No unauthorized peeking.

### 🎨 Frontend (The Look & Feel)
I decided to go **Vanilla** here. No heavy frameworks like React or Angular—just pure, optimized performance.

* **HTML5 Semantic Structure:** Clean markup that makes sense.
* **Modern CSS3 & Glassmorphism:** I went for that premium "frosted glass" look.
    * *Animations:* Smooth fade-ins, hover effects, and a custom loading spinner.
    * *Responsive:* Looks dope on mobile and desktop.
* **Vanilla JavaScript (ES6+):**
    * **Async/Await:** Handles the API calls to the backend smoothly without freezing the UI.
    * **DOM Manipulation:** Updates the page dynamically (no page reloads needed to get your link).
    * **Toast Notifications:** Custom-built popups to let you know if things went right (✅) or wrong (🚫).
    * **Clipboard API:** One-click copy feature because nobody has time to highlight text manually.

---

## 🚀 How to Run This Bad Boy Locally

Wanna play around with the code? Here is how you set it up on your machine:

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/SergioC2410/url_shortener.git](https://github.com/SergioC2410/url_shortener.git)
    cd url_shortener/backend
    ```

2.  **Set up the Virtual Environment:**
    ```bash
    # If you're on Windows:
    python -m venv venv
    .\venv\Scripts\activate
    
    # If you're on Mac/Linux:
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the goods:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Fire it up:**
    ```bash
    uvicorn main:app --reload
    ```
    Boom! Go to `http://127.0.0.1:8000` in your browser.

---

## 🕵️ Admin Panel Access

Want to see the analytics? I built a dashboard for that.

* **URL:** `/admin` (e.g., `https://shorty-the-cutter-url.onrender.com/admin`)
* **The Secret Handshake (Credentials):**
    * User: `admin`
    * Pass: `1234`

---

## 📸 Snapshots

| The Main Stage | The Dashboard |
| :---: | :---: |
| *Clean, glass-morphism UI for shortening links* | *Live stats table with click counters* |

---

[Check out my GitHub](https://github.com/SergioC2410)