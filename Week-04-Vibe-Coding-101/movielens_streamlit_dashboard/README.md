# Week 4 — MovieLens Streamlit Dashboard

A Streamlit dashboard answering the four required MovieLens questions from the Week 4 “Vibe Coding” assignment.

## Required questions covered

1. **Genre Breakdown** — distribution of genres among rated movies.
2. **Genre Satisfaction** — average rating by genre.
3. **Ratings Over Time** — mean rating by movie release year.
4. **Best Movies, With a Floor** — top 5 with at least 50 ratings vs. at least 150 ratings.

## Key analytical choices

- The `genres` field is pipe-separated, so it is split/exploded.
- **Question 1:** each unique movie counts once in every genre it belongs to. Counts overlap across genres.
- **Question 2:** each rating contributes to every genre assigned to its movie.
- **Question 3:** uses the movie's `year` (release year), not `rating_year`.
- **Question 4:** filters movies by rating count first, then sorts by mean rating. Ties are broken by rating count, then title.

## Interactive controls

- Genre multiselect for Questions 1–2.
- Release-year range slider for Question 3.
- Custom minimum-rating floor explorer for Question 4.

## Project files

```text
movielens_streamlit_dashboard/
├── app.py
├── movie_ratings.csv
├── requirements.txt
├── README.md
├── BUILD_LOG.md
├── DEPLOYMENT.md
└── .streamlit/
    └── config.toml
```

## Run locally

Python 3.12 is recommended to match Streamlit Community Cloud's current default.

```bash
python -m venv .venv
```

Activate the environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and launch:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints in the terminal (normally `http://localhost:8501`).

See `DEPLOYMENT.md` for the full GitHub + Streamlit Community Cloud deployment walkthrough.
