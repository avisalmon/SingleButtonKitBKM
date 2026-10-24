# Get started: from zero to a chat that guides you

You do this part once per computer, in about 20-30 minutes. After that, the chat in VS Code does the work and tells
you what to do. The same steps, in Hebrew and English, are on the start page: https://avisalmon.github.io/SingleButtonKitBKM/

**For children:** an adult sets up the accounts (AI services have age limits: check the one you choose) and stays nearby.

## 1. Build the kit

Follow the [assembly video](https://www.youtube.com/watch?v=Jap-4eeCaNw) and [kit.md](kit.md). Plug it into USB:
Flappy should start. *You know it worked when* the button makes the bird fly.

## 2. VS Code, the editor

Download from https://code.visualstudio.com and install with the default options.
*You know it worked when* VS Code opens.

## 3. An AI chat inside VS Code (pick one)

* **Claude Code**: in VS Code, Extensions (the four-squares icon on the left) -> search "Claude Code" -> Install ->
  sign in with a Claude account (a paid plan is needed for long sessions).
* **GitHub Copilot**: needs a free GitHub account (https://github.com/signup). In VS Code, sign in to GitHub
  (the person icon, bottom left), open the Copilot chat and switch it to **Agent** mode.

*You know it worked when* you type `hello` in the chat and it answers.

## 4. Git, the tool that copies the project to your computer

Download from https://git-scm.com/downloads and install with the default options. Close and reopen VS Code afterwards.

## 5. Copy the project and open it

In VS Code: **Terminal -> New Terminal** (a panel where you type commands). Type these lines one at a time, pressing
Enter after each:

```powershell
mkdir C:\kit
cd C:\kit
git clone https://github.com/avisalmon/SingleButtonKitBKM.git
code SingleButtonKitBKM
```

A new VS Code window opens on the project. Click **Yes, I trust the authors**.

## 6. Say it

Open the AI chat in that window and type:

> **תגיד לי מה לעשות** (or: **Tell me what to do**)

From here the chat installs what is missing (Python, the tools, the USB driver), checks your kit, and builds with you.
It will ask before installing things; Windows will ask you to click "Yes".

## Words you'll meet

| Word | Means |
|---|---|
| Repository (repo) | a project folder with its whole history, kept on GitHub |
| Clone | copy a repository to your computer |
| Terminal | a window where you type commands instead of clicking |
| ESP32 | the small computer on the kit |
| Upload / flash | send a program from the computer into the kit |
| COM port | the "address" Windows gives the kit when it is plugged in |
| PlatformIO | the tool that turns code into a program the ESP32 can run |
| Pull updates | get the newest version of this guide from GitHub (the chat does it every session) |
