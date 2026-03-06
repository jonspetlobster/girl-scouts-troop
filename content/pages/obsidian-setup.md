# Setting Up Obsidian to Edit the Website

This is a one-time setup. After this, editing the website is as easy as editing a document and clicking one button.

---

## What You'll Need

- A computer (Mac or Windows)
- A free GitHub account (you already have one if Jon set one up for you)
- Two free apps: **GitHub Desktop** and **Obsidian**

---

## Step 1: Install GitHub Desktop

GitHub Desktop is an easy app that keeps your files synced with the website.

1. Go to **desktop.github.com** and download GitHub Desktop
2. Install it and open it
3. Sign in with your GitHub account (the same one Jon set up)

---

## Step 2: Clone the Repo (Download the Files)

"Cloning" just means downloading a copy of the website files to your computer.

1. In GitHub Desktop, click **File → Clone Repository**
2. Search for `girl-scouts-troop`
3. Choose where to save it on your computer (Desktop is fine)
4. Click **Clone**

You now have a folder called `girl-scouts-troop` on your computer.

---

## Step 3: Install Obsidian

1. Go to **obsidian.md** and download Obsidian
2. Install it and open it
3. On the welcome screen, click **Open folder as vault**
4. Navigate to the `girl-scouts-troop` folder you just cloned
5. Select the **`content`** folder inside it (not the whole repo — just `content`)
6. Click Open

You'll now see all the content files in Obsidian's sidebar.

---

## Step 4: Install the Obsidian Git Plugin

This plugin lets you save your edits directly to the website from inside Obsidian.

1. In Obsidian, click the **Settings** gear (bottom left)
2. Click **Community plugins**
3. Click **Turn on community plugins** (if asked)
4. Click **Browse** and search for **Obsidian Git**
5. Click **Install**, then **Enable**
6. Close settings

---

## Step 5: Test It!

1. Open any file in Obsidian (try `meetings/2026-03-12-first-meeting.md`)
2. Make a small change — add a word anywhere
3. Press **Ctrl+P** (Windows) or **Cmd+P** (Mac) to open the Command Palette
4. Type **commit** and select **Obsidian Git: Commit all changes**
5. Type a short note like "updated first meeting plan" and press Enter
6. Then type **push** and select **Obsidian Git: Push**

That's it! Within about 30 seconds, the website will update automatically.

---

## Day-to-Day Editing

**To edit existing content:**
1. Find the file in Obsidian's sidebar
2. Edit it like a regular document
3. Cmd+P → "commit" → type a note → Enter
4. Cmd+P → "push"

**To add a new meeting plan (or activity, etc.):**
1. Right-click the `meetings` folder in the sidebar → New note
2. Name it like: `2026-04-05-spring-hike`
3. Paste the template from `README.md` at the top
4. Fill in your content
5. Commit and push (same steps as above)

**To get updates Jon made:**
1. Cmd+P → type "pull" → select **Obsidian Git: Pull**

---

## Quick Cheat Sheet

| What you want to do | Command |
|---|---|
| Save changes to website | Commit → Push |
| Get Jon's latest changes | Pull |
| Open command palette | Cmd+P (Mac) / Ctrl+P (Windows) |

---

## Stuck? 

If something looks wrong after you push, don't worry — nothing is permanent. Jon can always fix it. Just let him know what happened.
