---
name: share-my-project
description: >
  Back up or share the learner's projects from my_projects/ to their own GitHub repository, kept separate from this
  guide so pulling updates never conflicts. Optional; needs a GitHub account (an adult decides for children).
  TRIGGER: "save my projects", "back up my work", "share my game", "put my project on GitHub", "send my game to a friend",
  "תשמור את הפרויקטים", "גיבוי", "לשתף את המשחק", "להעלות לגיטהאב".
---

# Share my project

`my_projects/` is ignored by this repo's git on purpose: the guide updates freely and never touches the learner's work.
Backing it up means making **my_projects its own git repository**, pushed to the learner's own GitHub account.

## Before anything

* **Age and consent**: GitHub accounts are for ages 13 and up. For a younger learner, an adult creates and owns the account
  and approves sharing. Ask: "Is this your GitHub account, or a parent's or teacher's?"
* **Public or private?** Private by default. Public only when they want to show it, and after checking that no project has a
  `secrets.h` or any name, school or address in the code or comments. Explain why in one sentence.

## Steps

1. GitHub CLI: `gh --version`; if missing, `winget install --id GitHub.cli -e`. Log in: `gh auth login` (the learner
   completes it in the browser).
2. Make my_projects a repository of its own (a nested repo; the guide's git still ignores the folder):
   ```powershell
   cd my_projects
   git init -b main
   Set-Content .gitignore ".pio/`ninclude/secrets.h"
   git add . ; git commit -m "My Single Button kit projects"
   gh repo create my-kit-projects --private --source . --push
   ```
3. Later saves: `cd my_projects; git add .; git commit -m "<what changed>"; git push`. Do it when they ask, never on your own.
4. Sharing one game with a friend who also has the kit: they copy the project folder into their own `my_projects/`
   and ask their chat to upload it.

Ask before every step that publishes anything (creating the repo, pushing, making it public).
