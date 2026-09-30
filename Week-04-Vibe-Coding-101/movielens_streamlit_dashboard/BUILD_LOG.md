# Build Log — Week 4 MovieLens Dashboard

This is the raw build record from the ChatGPT-assisted session. Keep it for next week's reflection/audit work.

## Moment 1 — Start from the assignment, not a generic dashboard

**Prompt / instruction:**
> "do this assignment and give me complete instructions too to deply it;"

**What AI produced first:**
A plan to inspect the assignment and dataset before writing code, then build all four required visualizations, interactive controls, and deployment files.

**What changed and why:**
Instead of immediately generating a generic movie dashboard, the build was constrained to the exact four assignment questions and the required Streamlit deployment path.

---

## Moment 2 — Decide what “genre distribution” means with multi-genre movies

**Prompt / instruction from the assignment:**
> "What's the distribution of genres among the movies that were rated? (Movies can have multiple genres — have the AI explain how it handled that before it counts anything.)"

**What AI produced first:**
The genre field was split on `|` so a movie can belong to multiple genres.

**What changed and why:**
The final distribution counts **unique movies per genre**, not rating rows per genre. This matches the wording “movies that were rated” and prevents a frequently rated movie from being counted hundreds of times in the genre-distribution chart. A movie with multiple genres contributes once to each of its genres, so counts overlap.

---

## Moment 3 — Make the 50-vs-150 comparison impossible to miss

**Prompt / instruction from the assignment:**
> "What are the top 5 best-rated movies, once you only count movies with at least 50 ratings? What changes if you raise that floor to 150?"

**What AI produced first:**
A reusable minimum-rating-floor calculation and the idea of an interactive floor slider.

**What changed and why:**
The final dashboard shows the **50-rating and 150-rating top-five charts side by side** so the required comparison is always visible, then adds a separate custom-floor slider as extra interactivity. This avoids accidentally hiding one of the required answers behind a widget setting.
