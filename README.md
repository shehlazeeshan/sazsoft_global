# SaZSoft Global Marketing Ltd — Website

A 5-page Flask (Python) website: Home, Team, 3 service pages, Contact.
The contact form emails submissions to `alexanderbrookswikipediaeditor@gmail.com`.

## What's in this folder

```
sazsoft-website/
├── app.py                  → the whole backend (routes + email sending)
├── requirements.txt        → Python packages needed
├── .env.example            → template for your email credentials
├── templates/               → the 7 HTML pages (Jinja templates)
└── static/
    ├── css/style.css       → all styling
    └── js/script.js        → nav menu, animations, form submit
```

## 1. Tools to install first

1. **Python 3.10+** — download from https://python.org/downloads
   During install on Windows, tick **"Add Python to PATH"**.
2. **VS Code** — https://code.visualstudio.com
3. In VS Code, install the **"Python" extension** (by Microsoft) from the
   Extensions panel on the left (four-square icon).

## 2. Getting the project into VS Code

1. Create a folder on your computer, e.g. `sazsoft-website`.
2. Recreate the file structure above and paste each file's content in
   (I'll give you every file's code — just copy-paste each one into a new
   file with the matching name/path).
3. In VS Code: **File → Open Folder** → select `sazsoft-website`.

## 3. Install the Python packages

Open a terminal inside VS Code (**Terminal → New Terminal**), then run:

```bash
pip install -r requirements.txt
```

If `pip` isn't recognized, try `pip3` or `python -m pip install -r requirements.txt`.

## 4. Run the website locally

```bash
python app.py
```

You'll see something like `Running on http://127.0.0.1:5000`. Open that
link in your browser — the site is live on your own machine.

Press `CTRL + C` in the terminal to stop it.

## 5. Setting up the contact form email

The form works and validates input immediately, but to actually **send**
emails you need Gmail credentials:

1. Go to your Google Account → **Security** → turn on **2-Step Verification**
   (required for the next step).
2. Go to https://myaccount.google.com/apppasswords and create an **App
   Password** (name it e.g. "SaZSoft Website"). Google gives you a
   16-character code — copy it.
3. In your project folder, copy `.env.example` to a new file named `.env`.
4. Fill it in:
   ```
   SMTP_USERNAME=your-gmail-address@gmail.com
   SMTP_PASSWORD=the16characterapppassword
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   ```
5. Restart the app (`CTRL+C` then `python app.py` again). Now form
   submissions will actually land in `alexanderbrookswikipediaeditor@gmail.com`.

**Note:** `.env` holds a secret — never share it or upload it publicly
(e.g. don't push it to a public GitHub repo).

## 6. Team page emails

In `app.py`, the `TEAM` dictionary auto-generates placeholder emails like
`james.whitmore@sazsoftglobal.co.uk` for every team member (since you
didn't give individual emails, only the one contact-form address). Once
you register a real domain and mailboxes, update the `make_email()`
function or hard-code real addresses in `TEAM`.

## 7. Putting the site online (so it's not just on your computer)

Once you're happy locally, you'll want real hosting. Simple, cheap/free
options that work well with a small Flask app like this:

- **Render.com** (free tier, easiest — connect your GitHub repo, it
  detects Flask automatically)
- **PythonAnywhere** (free tier, Flask-friendly, good for beginners)
- **Railway.app**

All three: you push your code to GitHub, connect the repo, add your
`SMTP_USERNAME` / `SMTP_PASSWORD` as environment variables in their
dashboard (never commit `.env` itself), and they give you a live URL.
Happy to walk you through whichever one you pick.

## 8. Editing content later

- **Prices / timelines**: in `templates/service_wikipedia.html`,
  `service_webdev.html`, `service_graphic.html` — look for `<div class="price">`
  and the `.timeline` block.
- **Team members**: in `app.py`, inside the `TEAM` dictionary.
- **Colors**: in `static/css/style.css`, the `:root { ... }` block at the top.
