from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="MovieLens Ratings Dashboard",
    page_icon="🎬",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "/Users/ace-xeon/Desktop/fall-2026/ctp/ds-fall-2026/Week-04-Vibe-Coding-101/data/movie_ratings.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and lightly validate the provided MovieLens ratings file."""
    df = pd.read_csv(DATA_PATH)

    required = {"user_id", "movie_id", "rating", "title", "year", "genres"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating", "genres", "title"])
    return df


def movie_genre_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per unique movie-genre combination."""
    movies = df[["movie_id", "title", "genres"]].drop_duplicates(subset="movie_id")
    return movies.assign(genre=movies["genres"].str.split("|")).explode("genre")


def rating_genre_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per rating-genre combination."""
    return df.assign(genre=df["genres"].str.split("|")).explode("genre")


def movie_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate mean rating and rating count for each movie."""
    return (
        df.groupby(["movie_id", "title"], as_index=False)
        .agg(avg_rating=("rating", "mean"), rating_count=("rating", "size"))
    )


def top_movies(stats: pd.DataFrame, floor: int, n: int = 5) -> pd.DataFrame:
    """Return the highest-rated movies with at least `floor` ratings."""
    return (
        stats.loc[stats["rating_count"] >= floor]
        .sort_values(
            ["avg_rating", "rating_count", "title"],
            ascending=[False, False, True],
        )
        .head(n)
        .copy()
    )


def horizontal_bar(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    title: str,
    x_title: str,
    hover_data: dict | None = None,
    x_range: list[float] | None = None,
):
    """Create a consistently formatted sorted horizontal bar chart."""
    chart_data = data.copy().sort_values(x, ascending=True)
    fig = px.bar(
        chart_data,
        x=x,
        y=y,
        orientation="h",
        hover_data=hover_data,
        title=title,
    )
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=None,
        margin=dict(l=10, r=20, t=55, b=10),
        height=max(420, 28 * len(chart_data)),
    )
    fig.update_yaxes(
        categoryorder="array",
        categoryarray=chart_data[y].tolist(),
    )
    if x_range is not None:
        fig.update_xaxes(range=x_range)
    return fig


# ---------- Load + headline metrics ----------
df = load_data()
movie_genres = movie_genre_table(df)
rating_genres = rating_genre_table(df)
stats = movie_stats(df)

st.title("🎬 MovieLens Ratings Dashboard")
st.caption(
    "Interactive exploration of the four required MovieLens questions: genre mix, "
    "genre satisfaction, release-year trends, and best-rated movies with minimum-rating floors."
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Ratings", f"{len(df):,}")
m2.metric("Movies", f"{df['movie_id'].nunique():,}")
m3.metric("Users", f"{df['user_id'].nunique():,}")
m4.metric("Overall mean rating", f"{df['rating'].mean():.2f} / 5")

all_genres = sorted(movie_genres["genre"].dropna().unique().tolist())
valid_years = df["year"].dropna().astype(int)
min_year, max_year = int(valid_years.min()), int(valid_years.max())

with st.sidebar:
    st.header("Interactive controls")
    selected_genres = st.multiselect(
        "Genres shown in Questions 1–2",
        options=all_genres,
        default=all_genres,
        help="This changes which genre bars are displayed; it does not alter the underlying ratings.",
    )
    year_range = st.slider(
        "Release-year range for Question 3",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    custom_floor = st.slider(
        "Custom minimum ratings for Question 4 explorer",
        min_value=1,
        max_value=500,
        value=100,
        step=1,
    )

if not selected_genres:
    st.info("No genres selected, so Questions 1–2 are showing all genres.")
    selected_genres = all_genres

# ---------- Q1 ----------
st.divider()
st.header("1. Genre Breakdown")
st.write(
    "**How multi-genre movies are handled:** the pipe-separated genre field is split into "
    "individual genres. For this distribution, each **unique movie** is counted once in every "
    "genre it belongs to. A movie tagged `Action|Adventure` contributes one movie to Action and "
    "one movie to Adventure, so genre counts are overlapping rather than mutually exclusive."
)

q1 = (
    movie_genres[movie_genres["genre"].isin(selected_genres)]
    .groupby("genre", as_index=False)
    .agg(movie_count=("movie_id", "nunique"))
)

fig1 = horizontal_bar(
    q1,
    x="movie_count",
    y="genre",
    title="Number of Rated Movies by Genre",
    x_title="Unique movies",
    hover_data={"movie_count": ":,.0f"},
)
fig1.update_traces(texttemplate="%{x:,.0f}", textposition="outside", cliponaxis=False)
st.plotly_chart(fig1, width="stretch")

# ---------- Q2 ----------
st.divider()
st.header("2. Genre Satisfaction")
st.caption(
    "For genre averages, each rating is attached to every genre assigned to its movie. "
    "This preserves all genre memberships instead of forcing a movie into one genre."
)

q2 = (
    rating_genres[rating_genres["genre"].isin(selected_genres)]
    .groupby("genre", as_index=False)
    .agg(
        avg_rating=("rating", "mean"),
        rating_count=("rating", "size"),
        movie_count=("movie_id", "nunique"),
    )
)

fig2 = horizontal_bar(
    q2,
    x="avg_rating",
    y="genre",
    title="Average Rating by Genre",
    x_title="Mean rating (1–5)",
    hover_data={
        "avg_rating": ":.3f",
        "rating_count": ":,.0f",
        "movie_count": ":,.0f",
    },
    x_range=[0, 5],
)
fig2.update_traces(texttemplate="%{x:.2f}", textposition="outside", cliponaxis=False)
st.plotly_chart(fig2, width="stretch")

if not q2.empty:
    highest = q2.loc[q2["avg_rating"].idxmax()]
    lowest = q2.loc[q2["avg_rating"].idxmin()]
    c1, c2 = st.columns(2)
    c1.metric("Highest average genre", highest["genre"], f"{highest['avg_rating']:.3f}")
    c2.metric("Lowest average genre", lowest["genre"], f"{lowest['avg_rating']:.3f}")

# ---------- Q3 ----------
st.divider()
st.header("3. Ratings Over Movie Release Years")
st.caption(
    "This groups ratings by the movie's **release year** (`year`), not the year when the user submitted the rating."
)

q3_source = df.dropna(subset=["year"]).copy()
q3_source["year"] = q3_source["year"].astype(int)
q3_source = q3_source[q3_source["year"].between(year_range[0], year_range[1])]
q3 = (
    q3_source.groupby("year", as_index=False)
    .agg(mean_rating=("rating", "mean"), rating_count=("rating", "size"))
    .sort_values("year")
)

fig3 = px.line(
    q3,
    x="year",
    y="mean_rating",
    markers=True,
    hover_data={"rating_count": ":,.0f", "mean_rating": ":.3f"},
    title="Mean Rating by Movie Release Year",
)
fig3.update_layout(
    xaxis_title="Movie release year",
    yaxis_title="Mean rating",
    yaxis_range=[1, 5],
    height=480,
    margin=dict(l=10, r=20, t=55, b=10),
)
st.plotly_chart(fig3, width="stretch")

# ---------- Q4 ----------
st.divider()
st.header("4. Best Movies, With a Minimum-Rating Floor")
st.write(
    "The floor is applied to the **number of ratings per movie**. Movies below the floor are removed first; "
    "the remaining movies are ranked by mean rating. Ties are broken by more ratings, then title."
)

left, right = st.columns(2)
for container, floor in [(left, 50), (right, 150)]:
    top = top_movies(stats, floor)
    with container:
        st.subheader(f"At least {floor} ratings")
        if top.empty:
            st.warning("No movies meet this floor.")
        else:
            fig = horizontal_bar(
                top,
                x="avg_rating",
                y="title",
                title=f"Top 5 — Minimum {floor} Ratings",
                x_title="Mean rating (1–5)",
                hover_data={"avg_rating": ":.3f", "rating_count": ":,.0f"},
                x_range=[0, 5],
            )
            fig.update_layout(height=390)
            fig.update_traces(texttemplate="%{x:.3f}", textposition="outside", cliponaxis=False)
            st.plotly_chart(fig, width="stretch")
            st.dataframe(
                top[["title", "avg_rating", "rating_count"]]
                .rename(
                    columns={
                        "title": "Movie",
                        "avg_rating": "Mean rating",
                        "rating_count": "# ratings",
                    }
                )
                .style.format({"Mean rating": "{:.3f}", "# ratings": "{:,}"}),
                hide_index=True,
                width="stretch",
            )

floor50 = top_movies(stats, 50)
floor150 = top_movies(stats, 150)
only_50 = [title for title in floor50["title"] if title not in set(floor150["title"])]
new_150 = [title for title in floor150["title"] if title not in set(floor50["title"])]

if only_50 or new_150:
    st.markdown("**What changes when the floor rises from 50 to 150?**")
    if only_50:
        st.write("Drop out of the top 5:", ", ".join(only_50))
    if new_150:
        st.write("Enter the top 5:", ", ".join(new_150))

with st.expander("Explore a custom minimum-rating floor"):
    custom_top = top_movies(stats, custom_floor)
    st.write(f"Top movies with at least **{custom_floor}** ratings:")
    if custom_top.empty:
        st.warning("No movies meet this floor. Lower the slider.")
    else:
        st.dataframe(
            custom_top[["title", "avg_rating", "rating_count"]]
            .rename(
                columns={
                    "title": "Movie",
                    "avg_rating": "Mean rating",
                    "rating_count": "# ratings",
                }
            )
            .style.format({"Mean rating": "{:.3f}", "# ratings": "{:,}"}),
            hide_index=True,
            width="stretch",
        )

st.divider()
st.caption("Built by Aakash Gharti Chhetri")
