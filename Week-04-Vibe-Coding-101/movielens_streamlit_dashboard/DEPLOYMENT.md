# Complete Deployment Instructions

These steps deploy the dashboard publicly with **GitHub + Streamlit Community Cloud**.

## 1. Put all project files in one folder

The root folder must contain at least:

```text
app.py
movie_ratings.csv
requirements.txt
README.md
BUILD_LOG.md
DEPLOYMENT.md
.streamlit/config.toml
```

Do **not** rename `movie_ratings.csv` unless you also update `DATA_PATH` in `app.py`.

---

## 2. Test locally first

From Terminal / PowerShell, move into the project folder:

```bash
cd PATH/TO/movielens_streamlit_dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install the exact dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Check that:

- all four question sections load;
- the genre multiselect works;
- the release-year slider changes Question 3;
- the custom minimum-rating slider works;
- the 50-rating and 150-rating top-five charts both display.

Stop the local server with `Ctrl+C`.

---

## 3. Create an empty PUBLIC GitHub repository

1. Sign in to GitHub.
2. Create a **new repository**.
3. Suggested name: `movielens-streamlit-dashboard`.
4. Set visibility to **Public** (the course assignment explicitly asks for a public deployment flow).
5. When creating the repo, leave it **empty** — do not initialize it with a GitHub README, `.gitignore`, or license. Your local project already contains its own README.
6. Copy the repository HTTPS URL. It will look like:

```text
https://github.com/YOUR-USERNAME/movielens-streamlit-dashboard.git
```

---

## 4. Initialize Git locally and push the project

Run these commands **inside the project folder**:

```bash
git init -b main
git add .
git commit -m "Build MovieLens Streamlit dashboard"
git remote add origin https://github.com/YOUR-USERNAME/movielens-streamlit-dashboard.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your real GitHub username.

If Git asks you to identify yourself before the commit, run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Then run the `git commit` and `git push` commands again.

### Verify the push

Refresh the GitHub repository page. You should see `app.py`, `movie_ratings.csv`, `requirements.txt`, and the other files.

---

## 5. Connect GitHub to Streamlit Community Cloud

1. Go to **https://share.streamlit.io**.
2. Sign in / continue with GitHub.
3. If prompted, authorize Streamlit to access your GitHub public repositories.
4. Make sure your new repository is visible to Streamlit.

---

## 6. Deploy the app

1. In Streamlit Community Cloud, click **Create app**.
2. Choose the option indicating that you already have an app/repository.
3. Select or enter:
   - **Repository:** `YOUR-USERNAME/movielens-streamlit-dashboard`
   - **Branch:** `main`
   - **Main file path / entrypoint:** `app.py`
4. Optional but recommended: open **Advanced settings** and choose **Python 3.12** so the cloud environment is explicit and reproducible.
5. No secrets are required for this project.
6. Click **Deploy**.

Streamlit will clone the GitHub repository, install packages from `requirements.txt`, and run `app.py`.

---

## 7. If deployment fails

Open the app's deployment logs and check the first red error.

Common fixes:

### `FileNotFoundError: movie_ratings.csv`

The CSV was not pushed, was renamed, or is not in the repository root. Confirm this exact file exists:

```text
movie_ratings.csv
```

### `ModuleNotFoundError`

Confirm `requirements.txt` exists in the repo root and contains:

```text
streamlit==1.64.0
pandas==3.0.6
plotly==7.1.0
```

Commit and push any fix:

```bash
git add .
git commit -m "Fix deployment"
git push
```

Streamlit Community Cloud should detect the GitHub update and redeploy.

### Git says `remote origin already exists`

Check the current remote:

```bash
git remote -v
```

If it is wrong, replace it:

```bash
git remote set-url origin https://github.com/YOUR-USERNAME/movielens-streamlit-dashboard.git
```

Then:

```bash
git push -u origin main
```

---

## 8. Final pre-submission check

1. Copy the public Streamlit URL, which will end in `.streamlit.app`.
2. Open a new **Incognito / Private** browser window.
3. Paste the URL there.
4. Confirm the dashboard loads without asking for your GitHub/Streamlit login.
5. Test at least one interactive control.
6. Submit **that public Streamlit URL** for the assignment.
7. Keep `BUILD_LOG.md`; the assignment says you will need the prompt/build history later.

## Updating the app later

Make edits locally, then:

```bash
git add .
git commit -m "Update dashboard"
git push
```

Streamlit Community Cloud monitors the connected repository and redeploys changes automatically.
