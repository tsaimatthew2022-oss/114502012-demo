# Exercise 1 實作教學

這次實作會透過一支簡單的待辦清單 CLI 程式，練習 Git、GitHub 與 uv 的基本操作。整體流程對照簡報分成六個 Phase。

## Phase 1：建立專案環境

在正式開發前，先完成建立個人 Repository、Clone 到本機、並用 uv 初始化 Python 環境。

1. 登入 GitHub 後，開範例 repo：[https://github.com/GeorgeShiue/intro-to-csie-exercise-1](https://github.com/GeorgeShiue/intro-to-csie-exercise-1)，點頁面右上角綠色的 **Use this template** 按鈕 → 選 **Create a new repository**，建立自己的 repo
   - 這一步是把這個範例 repo 當「模板」，複製一份獨立的新 repo 到你自己的 GitHub 帳號底下（有自己的 commit 歷史，跟原本的範例 repo 沒有關聯）。這跟 fork 不同：fork 會保留與原 repo 的關聯，template 則不會，適合當作個人作業的起點
   - 依畫面指示輸入 repo 名稱，選擇 Public，按 **Create repository**
2. 在自己電腦上，把 repo clone 到本機資料夾：
   - **VS Code**：按 `Cmd+Shift+P`（Windows/Linux 是 `Ctrl+Shift+P`）打開命令面板，輸入並選擇 **Git: Clone** → 貼上自己 repo 的網址 → 選擇要存放的本機資料夾
   - **終端機**：先到自己的 GitHub repo 頁面，點右上角綠色的 **Code** 按鈕，複製 HTTPS 網址（例如 `https://github.com/<你的帳號>/<repo 名稱>.git`），再執行：

     ```bash
     git clone <剛剛複製的網址>
     ```
3. 用 VS Code 開啟這個資料夾，在內建終端機執行 `uv init`（可加 `--python 3.14` 指定版本），**在寫任何程式之前先把專案的環境準備好**
   - 這一步會產生：`pyproject.toml`（宣告這個專案用什麼 Python 版本、之後會裝什麼套件）、`.python-version`。因為資料夾裡已經有 `README.md`，uv 會把這個專案當成一個「package」來初始化，所以還會多產生 `src/<專案名稱>/__init__.py`（裡面有一個示範用的 `main()` 函式），`pyproject.toml` 裡也會多出 `[build-system]` 跟 `[project.scripts]` 這兩段設定
   - `src/` 底下這個範例套件跟這次的練習沒有關係，之後都是直接改根目錄的 `todo.py`，`src/` 資料夾可以留著不用管
4. 執行 `uv run todo.py` 確認能跑起來——**這一步會建立 `.venv` 資料夾、安裝好對應版本的 Python 並執行程式**，之後每次 `uv run` 都會沿用同一個環境

## Phase 2：專案版本管理

在 main 分支上做第一次 commit，並先把接下來會用到的兩條 feature 分支建立好。

1. 在 **main** 分支上做第一次 commit（這次會連 `pyproject.toml`、`.python-version`、`uv.lock` 一起進版控，`.venv/` 不進）：
   - **VS Code**：Source Control 面板勾選這些變更的檔案 → 輸入 commit 訊息 "init: exercise 1 project environment"→ 打勾送出 → 送出後點同步變更把 commit 推上 GitHub
   - **終端機**：

     ```bash
     git add .
     git commit -m "init: exercise 1 project environment"
     git push
     ```
2. 建立 `feature/delete-task` 分支（先不動工，晚點做 Feature 2 時才會用到）：
   - **VS Code**：點左下角目前分支名稱（此時是 `main`）→ 選 **Create new branch...** → 輸入 `feature/delete-task` → Enter（建立後會自動切換過去）
   - **終端機**：

     ```bash
     git checkout -b feature/delete-task   # 先開好，晚點才會用到
     ```

3. 切回 `main`，再從這裡建立 `feature/add-task` 分支（接下來要開始做這一條）：
   - **VS Code**：點左下角分支名稱（此時是 `feature/delete-task`）→ 切回 **main**（在清單裡選 `main`）→ 再點一次左下角分支名稱 → **Create new branch...** → 輸入 `feature/add-task` → Enter
   - **終端機**：

     ```bash
     git checkout main
     git checkout -b feature/add-task      # 接下來要開始做這一條
     ```

   這樣兩條分支的起點會是同一個 commit，`feature/delete-task` 停在這裡不動。

4. 確認目前所在分支是 `feature/add-task`（VS Code 左下角或終端機 `git branch` 都看得到），確認無誤後才開始做 Feature 1。

## Phase 3：新增任務防止重複機制

延續 `feature/add-task` 分支，強化 `add_task` 新增前的重複檢查，並更新展示畫面與驗證流程。

`todo.py` 已經在專案根目錄底下（Use this template 建立 repo、clone 下來時就一起帶過來了），目前裡面只有 `add_task`、`show_tasks`、`main` 這三個部分。

1. 切換到 `feature/add-task` 分支：用 VS Code 左下角分支名稱點一下選取，或終端機 `git checkout feature/add-task`
2. 修改 `todo.py`：強化 `add_task`，新增前先檢查任務名稱是否已存在，重複就不新增（並印一句提示）：

   ```python
   def add_task(name):
       if name in tasks:
           print(f"'{name}' already exists, skipping")
           return
       tasks.append(name)
   ```

3. 把 `show_tasks()` 的標題從陽春的 `=== 待辦清單 ===` 改成顯示目前共有幾項：

   ```python
   def show_tasks():
       print(f"=== To-Do List ({len(tasks)} items) ===")
       for i, t in enumerate(tasks, 1):
           print(f"{i}. {t}")
   ```

4. 在 `main()` 裡加一段呼叫，demo 一下防重複有作用（新增同一個名稱兩次，第二次會被擋下來）：

   ```python
   def main():
       add_task("Learn Git")
       add_task("Learn Git")
       show_tasks()
   ```

5. 執行 `uv run todo.py` 確認輸出正確（重複的任務有被擋下、標題有顯示項目數），接著 commit 並推上 GitHub：
   - **VS Code**：Source Control 面板勾選所有變更的檔案 → 輸入 commit 訊息 → 打勾送出 → 送出後上方會出現 **Publish Branch** 按鈕，點下去
   - **終端機**：

     ```bash
     git add .
     git commit -m "add: prevent duplicate task"
     git push -u origin feature/add-task
     ```

## Phase 4：PR 合併與同步

開啟 Pull Request、確認變更、合併，並把最新進度同步回本機。

1. 到 GitHub 網頁，點 **Compare & pull request**，base: `main` ← compare: `feature/add-task`
2. 看 **Files changed** 讀一下 diff，確認只有 `todo.py` 被改動；確認右側顯示 **Able to merge**，寫一句 PR 說明，接著點 **Create pull request** 建立這個 PR
3. PR 建立後，點 **Merge pull request** → 再點一次 **Confirm merge** 完成合併，接著回到本機把 main 同步到最新：
   - **VS Code**：左下角點分支名稱切回 **main** → 打開 Source Control 面板，點面板上方的 **Pull** 按鈕
   - **終端機**：

     ```bash
     git checkout main
     git pull
     ```
4. 執行 `uv run python todo.py`，確認 main 分支已經正確合併 Feature 1（重複的任務有被擋下、標題有顯示項目數）
5. （可選）刪除已合併的分支，養成清理習慣：
   - **VS Code**：左側 **Branches** 清單裡找到 `feature/add-task`，右鍵點選 **Delete Branch**
   - **終端機**：`git branch -d feature/add-task`

## Phase 5：刪除任務功能

在 `feature/delete-task` 分支上新增 `delete_task` 功能，讓使用者可以依名稱移除清單中的任務，最後開啟 PR。

`feature/delete-task` 這條分支是在做 Feature 1 之前就建立好的，所以它的起點還是「舊版」`todo.py`：`add_task` 還沒有防重複邏輯，標題那行還是最原始的 `=== 待辦清單 ===`。你會在這個舊版本上開發，等一下要 merge 回 main 時，main 已經被 Feature 1 更新過了，兩邊很可能會撞出衝突（conflict）——別慌，這是版本控制裡很常見的情況，Phase 6 會帶你一步步處理。

1. 切換到 `feature/delete-task`：
   - **VS Code**：左下角點分支名稱，從清單選 `feature/delete-task`
   - **終端機**：`git checkout feature/delete-task`

2. 在 `todo.py` 裡新增 `delete_task(name)` 函式：依名稱在清單中搜尋，找到就移除該筆資料；找不到時印出提示訊息，程式不會中斷執行

   ```python
   def delete_task(name):
       if name not in tasks:
           print(f"'{name}' not found, nothing to delete")
           return
       tasks.remove(name)
   ```

3. 也把標題那行改成顯示剩餘任務數（但用詞跟 Feature 1 不一樣）：

   ```python
   def show_tasks():
       print(f"=== To-Do List ({len(tasks)} remaining) ===")
       for i, t in enumerate(tasks, 1):
           print(f"{i}. {t}")
   ```

4. 在 `main()` 裡加一段呼叫，demo 一下 `delete_task` 有作用（依名稱刪除前後各印一次清單，並示範刪除不存在的名稱不會讓程式中斷）：

   ```python
   def main():
       add_task("Learn Git")
       show_tasks()
       delete_task("Learn Git")
       show_tasks()
       delete_task("Not Exist")
       show_tasks()
   ```

5. commit 並推上 GitHub：
   - **VS Code**：Source Control 面板勾選變更的檔案 → 輸入 commit 訊息 → 打勾送出 → 點 **Publish Branch**
   - **終端機**：

     ```bash
     git add .
     git commit -m "add: delete_task"
     git push -u origin feature/delete-task
     ```

6. 到 GitHub 網頁，點 **Compare & pull request** 開一個新 PR（base: `main` ← compare: `feature/delete-task`）
   - 這個頁面（Comparing changes）上，title 欄位會自動帶入剛剛的 commit 訊息（例如 `add: delete_task`），可以直接用或自己修改；description 欄位可留空或簡單寫一句說明
   - 注意頁面上方會出現紅字 **Can't automatically merge.**（如圖）——這是 GitHub 提前告訴你 `main` 跟 `feature/delete-task` 已經衝突了，但不影響先建立 PR，訊息旁也寫了 **Don't worry, you can still create the pull request.**
   - 確認無誤後點 **Create pull request** 建立這個 PR

## Phase 6：解決 Merge Conflict

PR 建立後會直接看到衝突狀態，接下來一步步排解衝突並完成合併。

1. PR 建立後，會直接進到這個 PR 的頁面，這時候就能看到衝突狀態，不用等到手動按 merge 才發現：
   - 標題旁邊會出現紅底的 **Merge conflicts** 標籤
   - 下面會有一個警告框寫 **This branch has conflicts that must be resolved**，並列出衝突的檔案（這裡是 `todo.py`），旁邊有 **Resolve conflicts** 按鈕
   - 原本的 **Merge pull request** 按鈕這時候會是灰色、按不下去的狀態，要等衝突解決後才會恢復

   衝突的原因是：兩邊都改了 `show_tasks()` 最上面那一行標題，但改成不一樣的內容。點進 **Resolve conflicts** 後，畫面上會看到類似這樣的衝突標記（下面的「main」「feature/delete-task」是用來標示這是哪一邊的版本，實際畫面上的呈現方式可能略有不同）：

   ```python
   <<<<<<< main
       print(f"=== To-Do List ({len(tasks)} items) ===")      # 這是 Feature 1 已經 merge 進 main 的版本
   =======
       print(f"=== To-Do List ({len(tasks)} remaining) ===")    # 這是你在 feature/delete-task 上寫的版本
   >>>>>>> feature/delete-task
   ```

   其他部分（`add_task` 的防重複邏輯、`delete_task`）都不會衝突，Git 會自動合併，只有標題這一行需要你自己決定怎麼處理。

2. **解決 conflict**：
   - 點 **Resolve conflicts** 右邊的下拉箭頭，選 **Edit on the web**（不要選 **Fix with Copilot**），會直接在 GitHub 網頁上打開衝突檔案的編輯畫面
   - 兩邊其實都在講同一件事（目前清單還有幾項），挑一種說法留下來就好，把衝突標記（`<<<<<<<`、`=======`、`>>>>>>>`）跟不要的那一行都刪掉，例如最後留下：

     ```python
     print(f"=== To-Do List ({len(tasks)} items) ===")
     ```

   - 畫面右上角原本紅色的 **1 conflict** 會消失，並出現綠色打勾的 **Resolved**，這時點右上角的 **Mark as resolved** 按鈕
   - 頁面會跳回 PR 畫面，出現綠色的 **Commit merge** 按鈕，點下去完成 merge

3. 點 Merge pull request → 再點一次 Confirm merge 完成合併，接著回到本機把 main 同步到最新：
   - **VS Code**：左下角點分支名稱切回 **main** → 打開 Source Control 面板，點面板上方的 **Pull** 按鈕
   - **終端機**：

     ```bash
     git checkout main
     git pull
     ```

   執行 `uv run todo.py` 確認兩個功能（新增防重複、依名稱刪除）都正常運作，標題顯示也正確

4. （可選）刪除已合併的分支，養成清理習慣：
   - **VS Code**：左側 **Branches** 清單裡找到 `feature/delete-task`，右鍵點選 **Delete Branch**
   - **終端機**：`git branch -d feature/delete-task`

## 繳交規範

- **繳交項目**：
  - GitHub repo 連結（須包含 Feature 1、2 兩次 PR 合併紀錄）
  - 一張 VS Code Git Graph 畫面截圖（需看得出分支與合併過程）
- **作業規定**：
  - 每份作業配分 2.5%
  - 需於課堂當天 23:59 前繳交

# Exercise 1 Tutorial

This exercise walks through the basics of Git, GitHub, and uv using a simple to-do list CLI program. The overall workflow mirrors the slide deck and is split into six phases.

## Phase 1: Setting Up the Project Environment

Before you start developing, complete three setup steps: create your own repository, clone it locally, and initialize the Python environment with uv.

1. After logging in to GitHub, open the sample repo: [https://github.com/GeorgeShiue/intro-to-csie-exercise-1](https://github.com/GeorgeShiue/intro-to-csie-exercise-1). Click the green **Use this template** button in the top-right corner → choose **Create a new repository** to create your own repo.
   - This step treats the sample repo as a "template" and copies it into an independent new repo under your own GitHub account (with its own commit history, unrelated to the original sample repo). This is different from forking: a fork keeps a link to the original repo, while a template does not — making it a good starting point for a personal assignment.
   - Follow the on-screen instructions to name your repo, select **Public**, and click **Create repository**.
2. On your own computer, clone the repo into a local folder:
   - **VS Code**: Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux) to open the command palette, type and select **Git: Clone** → paste your repo's URL → choose the local folder to save it in.
   - **Terminal**: Go to your GitHub repo page, click the green **Code** button, copy the HTTPS URL (e.g. `https://github.com/<your-username>/<repo-name>.git`), then run:

     ```bash
     git clone <the URL you just copied>
     ```
3. Open this folder in VS Code and run `uv init` in the built-in terminal (you can add `--python 3.14` to specify a version) — **get the project's environment ready before writing any code**.
   - This step generates `pyproject.toml` (declaring which Python version the project uses and which packages will be installed) and `.python-version`. Because the folder already has a `README.md`, uv initializes the project as a "package," so it also generates `src/<project-name>/__init__.py` (containing a sample `main()` function), and `pyproject.toml` gains two extra sections, `[build-system]` and `[project.scripts]`.
   - The sample package under `src/` is unrelated to this exercise. From here on you'll only be editing `todo.py` in the root directory — you can leave the `src/` folder alone.
4. Run `uv run todo.py` to confirm it works — **this step creates the `.venv` folder, installs the matching Python version, and runs the program**. Every subsequent `uv run` will reuse this same environment.

## Phase 2: Project Version Management

Make the first commit on the main branch, and set up the two feature branches you'll need later.

1. Make the first commit on the **main** branch (this commit will include `pyproject.toml`, `.python-version`, and `uv.lock` in version control, but not `.venv/`):
   - **VS Code**: In the Source Control panel, check the changed files → enter the commit message "init: exercise 1 project environment" → click the checkmark to commit → then click "Sync Changes" to push the commit to GitHub.
   - **Terminal**:

     ```bash
     git add .
     git commit -m "init: exercise 1 project environment"
     git push
     ```
2. Create the `feature/delete-task` branch (you won't start working on it yet — it'll be used later for Feature 2):
   - **VS Code**: Click the current branch name in the bottom-left corner (currently `main`) → select **Create new branch...** → type `feature/delete-task` → Enter (you'll automatically switch to it after creation).
   - **Terminal**:

     ```bash
     git checkout -b feature/delete-task   # created now, will be used later
     ```

3. Switch back to `main`, and create the `feature/add-task` branch from there (this is the one you'll start working on next):
   - **VS Code**: Click the branch name in the bottom-left corner (currently `feature/delete-task`) → switch back to **main** (select it from the list) → click the branch name again → **Create new branch...** → type `feature/add-task` → Enter.
   - **Terminal**:

     ```bash
     git checkout main
     git checkout -b feature/add-task      # starting work on this one next
     ```

   Both branches now start from the same commit; `feature/delete-task` stays put here.

4. Confirm you're currently on the `feature/add-task` branch (visible in the bottom-left of VS Code or via `git branch` in the terminal) — once confirmed, you're ready to start Feature 1.

## Phase 3: Preventing Duplicate Tasks

Continuing on the `feature/add-task` branch, strengthen `add_task`'s duplicate check before adding a task, and update the display and verification flow.

`todo.py` is already in the project root (it came along when you created the repo from the template and cloned it). Right now it only contains `add_task`, `show_tasks`, and `main`.

1. Switch to the `feature/add-task` branch: click the branch name in the bottom-left of VS Code, or run `git checkout feature/add-task` in the terminal.
2. Modify `todo.py`: strengthen `add_task` to check whether the task name already exists before adding it, and skip adding it (with a message) if it's a duplicate:

   ```python
   def add_task(name):
       if name in tasks:
           print(f"'{name}' already exists, skipping")
           return
       tasks.append(name)
   ```

3. Change the title line in `show_tasks()` from the plain `=== 待辦清單 ===` to show the current item count:

   ```python
   def show_tasks():
       print(f"=== To-Do List ({len(tasks)} items) ===")
       for i, t in enumerate(tasks, 1):
           print(f"{i}. {t}")
   ```

4. Add a call in `main()` to demo the duplicate check (add the same task name twice — the second one should be rejected):

   ```python
   def main():
       add_task("Learn Git")
       add_task("Learn Git")
       show_tasks()
   ```

5. Run `uv run todo.py` to confirm the output is correct (the duplicate task is rejected and the title shows the item count), then commit and push to GitHub:
   - **VS Code**: In the Source Control panel, check all the changed files → enter a commit message → click the checkmark to commit → a **Publish Branch** button will appear afterward — click it.
   - **Terminal**:

     ```bash
     git add .
     git commit -m "add: prevent duplicate task"
     git push -u origin feature/add-task
     ```

## Phase 4: PR Merge and Sync

Open a pull request, review the changes, merge it, and sync the latest progress back to your local machine.

1. On the GitHub website, click **Compare & pull request**, base: `main` ← compare: `feature/add-task`.
2. Review **Files changed** to check the diff — confirm only `todo.py` was modified; confirm **Able to merge** is shown on the right, write a brief PR description, then click **Create pull request** to open it.
3. After the PR is created, click **Merge pull request** → click **Confirm merge** to complete the merge, then sync `main` locally to the latest state:
   - **VS Code**: Click the branch name in the bottom-left to switch back to **main** → open the Source Control panel → click the **Pull** button at the top.
   - **Terminal**:

     ```bash
     git checkout main
     git pull
     ```
4. Run `uv run python todo.py` to confirm Feature 1 has been correctly merged into `main` (duplicate tasks are rejected, and the title shows the item count).
5. (Optional) Delete the merged branch to build a good cleanup habit:
   - **VS Code**: Find `feature/add-task` in the **Branches** list on the left, right-click and select **Delete Branch**.
   - **Terminal**: `git branch -d feature/add-task`

## Phase 5: Delete Task Feature

Add a `delete_task` feature on the `feature/delete-task` branch so users can remove a task from the list by name, then open a PR.

The `feature/delete-task` branch was created before Feature 1, so it still starts from the "old" version of `todo.py`: `add_task` doesn't have the duplicate check yet, and the title line is still the original `=== 待辦清單 ===`. You'll be developing on top of this older version, and since `main` has already been updated by Feature 1, the two branches will very likely conflict when you try to merge back — don't worry, this is a very common situation in version control, and Phase 6 will walk you through resolving it step by step.

1. Switch to `feature/delete-task`:
   - **VS Code**: Click the branch name in the bottom-left and select `feature/delete-task` from the list.
   - **Terminal**: `git checkout feature/delete-task`

2. Add a `delete_task(name)` function to `todo.py`: it searches the list by name and removes the matching entry if found; if not found, it prints a message without crashing the program.

   ```python
   def delete_task(name):
       if name not in tasks:
           print(f"'{name}' not found, nothing to delete")
           return
       tasks.remove(name)
   ```

3. Also change the title line to show the number of remaining tasks (using different wording from Feature 1):

   ```python
   def show_tasks():
       print(f"=== To-Do List ({len(tasks)} remaining) ===")
       for i, t in enumerate(tasks, 1):
           print(f"{i}. {t}")
   ```

4. Add a call in `main()` to demo `delete_task` working (print the list before and after deleting by name, and show that deleting a name that doesn't exist doesn't crash the program):

   ```python
   def main():
       add_task("Learn Git")
       show_tasks()
       delete_task("Learn Git")
       show_tasks()
       delete_task("Not Exist")
       show_tasks()
   ```

5. Commit and push to GitHub:
   - **VS Code**: In the Source Control panel, check the changed files → enter a commit message → click the checkmark to commit → click **Publish Branch**.
   - **Terminal**:

     ```bash
     git add .
     git commit -m "add: delete_task"
     git push -u origin feature/delete-task
     ```

6. On the GitHub website, click **Compare & pull request** to open a new PR (base: `main` ← compare: `feature/delete-task`).
   - On this page (Comparing changes), the title field will automatically be filled with your commit message (e.g. `add: delete_task`) — you can use it as is or edit it; the description field can be left blank or given a brief note.
   - Notice the red text **Can't automatically merge.** at the top of the page (as shown) — this is GitHub letting you know in advance that `main` and `feature/delete-task` already conflict, but it doesn't stop you from creating the PR; the message also says **Don't worry, you can still create the pull request.**
   - Once confirmed, click **Create pull request** to open it.

## Phase 6: Resolving the Merge Conflict

Right after the PR is created you'll see the conflict status — here's how to resolve it and complete the merge, step by step.

1. Once the PR is created, you'll land directly on the PR page, where the conflict status is already visible — no need to wait until you try to merge to discover it:
   - A red **Merge conflicts** label appears next to the title.
   - Below it, a warning box reads **This branch has conflicts that must be resolved**, listing the conflicting file (`todo.py` in this case), with a **Resolve conflicts** button next to it.
   - The **Merge pull request** button is grayed out and unclickable until the conflict is resolved.

   The cause of the conflict: both branches changed the title line at the top of `show_tasks()`, but with different content. Clicking into **Resolve conflicts** shows conflict markers like this (the "main" and "feature/delete-task" labels below indicate which side each version came from — the actual on-screen presentation may vary slightly):

   ```python
   <<<<<<< main
       print(f"=== To-Do List ({len(tasks)} items) ===")      # this is the version already merged into main from Feature 1
   =======
       print(f"=== To-Do List ({len(tasks)} remaining) ===")    # this is the version you wrote on feature/delete-task
   >>>>>>> feature/delete-task
   ```

   Everything else (the duplicate-check logic in `add_task`, and `delete_task`) doesn't conflict — Git merges those automatically. Only this one title line needs you to decide how to handle it.

2. **Resolve the conflict**:
   - Click the dropdown arrow next to **Resolve conflicts** and choose **Edit on the web** (not **Fix with Copilot**) — this opens the conflicting file's editor directly on the GitHub website.
   - Both sides are really saying the same thing (how many items are currently in the list), so just keep one version. Delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) along with the line you don't want to keep — for example, ending up with:

     ```python
     print(f"=== To-Do List ({len(tasks)} items) ===")
     ```

   - The red **1 conflict** in the top-right corner will disappear and change to a green checkmark labeled **Resolved** — click the **Mark as resolved** button in the top-right corner.
   - You'll be taken back to the PR page, where a green **Commit merge** button appears — click it to complete the merge.

3. Click **Merge pull request** → click **Confirm merge** again to complete the merge, then sync `main` locally to the latest state:
   - **VS Code**: Click the branch name in the bottom-left to switch back to **main** → open the Source Control panel → click the **Pull** button at the top.
   - **Terminal**:

     ```bash
     git checkout main
     git pull
     ```

   Run `uv run todo.py` to confirm both features (preventing duplicates, and deleting by name) work correctly, and that the title displays properly.

4. (Optional) Delete the merged branch to build a good cleanup habit:
   - **VS Code**: Find `feature/delete-task` in the **Branches** list on the left, right-click and select **Delete Branch**.
   - **Terminal**: `git branch -d feature/delete-task`

## Submission Requirements

- **What to submit**:
  - Your GitHub repo link (must include the two PR merge records for Feature 1 and Feature 2)
  - A screenshot of the VS Code Git Graph panel (branches and merges must be clearly visible)
- **Assignment policy**:
  - Each assignment is worth 2.5% of the grade
  - Must be submitted by 23:59 on the day of class