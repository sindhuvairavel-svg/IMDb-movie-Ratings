import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="IMDb Top 250 Movies",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
        radial-gradient(circle at top left, #252525 0%, #111111 35%, #080808 100%);
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: #FFD700;
        margin-bottom: 5px;
        text-shadow: 0px 0px 15px rgba(255,215,0,0.35);
    }

    .subtitle {
        text-align: center;
        color: #D0D0D0;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Metric cards */
    .metric-card {
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(145deg, #202020, #111111);
        border: 1px solid #333333;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.45);
        text-align: center;
        min-height: 135px;
        transition: 0.3s;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
        box-shadow: 0px 10px 30px rgba(255,215,0,0.18);
    }

    .metric-icon {
        font-size: 28px;
    }

    .metric-title {
        color: #AAAAAA;
        font-size: 14px;
        margin-top: 8px;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 25px;
        font-weight: bold;
        margin-top: 6px;
    }

    /* Section headings */
    .section-title {
        color: #FFD700;
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Movie cards */
    .movie-card {
        background: linear-gradient(135deg, #1d1d1d, #101010);
        border: 1px solid #303030;
        border-radius: 15px;
        padding: 15px 20px;
        margin: 8px 0px;
        transition: 0.3s;
    }

    .movie-card:hover {
        border-color: #FFD700;
        transform: translateX(5px);
        box-shadow: 0px 5px 20px rgba(255,215,0,0.12);
    }

    .movie-name {
        color: white;
        font-size: 18px;
        font-weight: 700;
    }

    .movie-info {
        color: #BBBBBB;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717, #090909);
        border-right: 1px solid #333333;
    }

    section[data-testid="stSidebar"] h2 {
        color: #FFD700;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700, #FFB300);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: #333333;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("imdb_movies.csv")

        # Remove unnamed columns
        df = df.loc[
            :,
            ~df.columns.str.contains("^Unnamed")
        ]

        return df

    except FileNotFoundError:

        return None


df = load_data()


# =========================================================
# FILE CHECK
# =========================================================

if df is None:

    st.error(
        "❌ imdb_movies.csv not found!"
    )

    st.info(
        "Make sure imdb_movies.csv and dashboard_app.py "
        "are in the same folder."
    )

    st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()


# =========================================================
# DATA CLEANING
# =========================================================

if "Rating" in df.columns:

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )


if "Rank" in df.columns:

    df["Rank"] = pd.to_numeric(
        df["Rank"],
        errors="coerce"
    )


if "Year" in df.columns:

    df["Year"] = (
        df["Year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎬 IMDb TOP 250 MOVIES</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore • Search • Filter • Analyze the world\'s top-rated movies'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "## 🎯 Dashboard Filters"
)

st.sidebar.markdown("---")


# Search

search_query = st.sidebar.text_input(
    "🔎 Search Movie",
    placeholder="Enter movie name..."
)


# Rating

if "Rating" in df.columns:

    rating_data = df["Rating"].dropna()

    min_rating = float(rating_data.min())
    max_rating = float(rating_data.max())

    selected_rating = st.sidebar.slider(
        "⭐ Minimum Rating",
        min_value=min_rating,
        max_value=max_rating,
        value=min_rating,
        step=0.1
    )

else:

    selected_rating = 0


# Year

if "Year" in df.columns:

    year_data = df["Year"].dropna()

    if len(year_data) > 0:

        min_year = int(year_data.min())
        max_year = int(year_data.max())

        selected_year = st.sidebar.slider(
            "📅 Minimum Year",
            min_value=min_year,
            max_value=max_year,
            value=min_year
        )

    else:

        selected_year = 0

else:

    selected_year = 0


# =========================================================
# FILTERING
# =========================================================

filtered_df = df.copy()


# Rating filter

if "Rating" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["Rating"] >= selected_rating
    ]


# Year filter

if (
    "Year" in filtered_df.columns
    and selected_year != 0
):

    filtered_df = filtered_df[
        filtered_df["Year"] >= selected_year
    ]


# Search

if search_query:

    if "Movie Name" in filtered_df.columns:

        filtered_df = filtered_df[
            filtered_df["Movie Name"]
            .astype(str)
            .str.contains(
                search_query,
                case=False,
                na=False
            )
        ]


# =========================================================
# METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Movie Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


# Total movies

with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🎥</div>
            <div class="metric-title">TOTAL MOVIES</div>
            <div class="metric-value">{len(filtered_df)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Average rating

with col2:

    if (
        len(filtered_df) > 0
        and "Rating" in filtered_df.columns
    ):

        avg_rating = filtered_df["Rating"].mean()

        avg_text = f"{avg_rating:.2f} ⭐"

    else:

        avg_text = "N/A"


    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-title">AVERAGE RATING</div>
            <div class="metric-value">{avg_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Top movie

with col3:

    if (
        len(filtered_df) > 0
        and "Movie Name" in filtered_df.columns
    ):

        if "Rank" in filtered_df.columns:

            top_data = filtered_df.sort_values(
                "Rank"
            )

            top_movie = top_data.iloc[0]["Movie Name"]

        else:

            top_movie = filtered_df.iloc[0]["Movie Name"]

    else:

        top_movie = "N/A"


    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🏆</div>
            <div class="metric-title">TOP MOVIE</div>
            <div class="metric-value">{top_movie}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Oldest year

with col4:

    if (
        len(filtered_df) > 0
        and "Year" in filtered_df.columns
    ):

        oldest = filtered_df["Year"].min()

        if pd.notna(oldest):

            oldest_text = str(int(oldest))

        else:

            oldest_text = "N/A"

    else:

        oldest_text = "N/A"


    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📅</div>
            <div class="metric-title">OLDEST MOVIE YEAR</div>
            <div class="metric-value">{oldest_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MOVIE TABLE
# =========================================================

st.markdown(
    '<div class="section-title">🎞️ Movie Collection</div>',
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    display_columns = []

    for column in [
        "Rank",
        "Movie Name",
        "Rating",
        "Year"
    ]:

        if column in filtered_df.columns:

            display_columns.append(column)


    display_df = filtered_df[
        display_columns
    ].copy()


    if "Rank" in display_df.columns:

        display_df = display_df.sort_values(
            "Rank"
        )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "⚠️ No movies match your filters."
    )


# =========================================================
# TOP 10 MOVIES
# =========================================================

st.markdown(
    '<div class="section-title">🏆 Top 10 Movies</div>',
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    top10 = filtered_df.copy()


    if "Rank" in top10.columns:

        top10 = top10.sort_values(
            "Rank"
        ).head(10)

    else:

        top10 = top10.head(10)


    for _, row in top10.iterrows():

        rank = row.get(
            "Rank",
            "N/A"
        )

        name = row.get(
            "Movie Name",
            "Unknown"
        )

        rating = row.get(
            "Rating",
            "N/A"
        )

        year = row.get(
            "Year",
            "N/A"
        )


        if pd.notna(rating):

            rating_text = f"{float(rating):.1f}"

        else:

            rating_text = "N/A"


        if pd.notna(year):

            year_text = str(int(year))

        else:

            year_text = "N/A"


        st.markdown(
            f"""
            <div class="movie-card">

                <div class="movie-name">
                    🏅 #{rank} &nbsp; {name}
                </div>

                <div class="movie-info">
                    ⭐ Rating: {rating_text}
                    &nbsp;&nbsp;&nbsp;
                    📅 Year: {year_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CHARTS
# =========================================================

st.markdown("---")

chart_col1, chart_col2 = st.columns(2)


# =========================================================
# RATING DISTRIBUTION
# =========================================================

with chart_col1:

    st.markdown(
        '<div class="section-title">⭐ Rating Distribution</div>',
        unsafe_allow_html=True
    )


    if (
        len(filtered_df) > 0
        and "Rating" in filtered_df.columns
    ):

        fig, ax = plt.subplots(
            figsize=(7, 4)
        )

        ax.hist(
            filtered_df["Rating"].dropna(),
            bins=10
        )

        ax.set_xlabel("IMDb Rating")

        ax.set_ylabel("Number of Movies")

        ax.set_title(
            "Movie Rating Distribution"
        )

        ax.grid(
            alpha=0.2
        )

        st.pyplot(fig)


# =========================================================
# MOVIES BY YEAR
# =========================================================

with chart_col2:

    st.markdown(
        '<div class="section-title">📅 Movies by Year</div>',
        unsafe_allow_html=True
    )


    if (
        len(filtered_df) > 0
        and "Year" in filtered_df.columns
    ):

        year_count = (
            filtered_df["Year"]
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
        )


        fig2, ax2 = plt.subplots(
            figsize=(7, 4)
        )

        ax2.plot(
            year_count.index,
            year_count.values,
            marker="o"
        )

        ax2.set_xlabel("Year")

        ax2.set_ylabel("Movies")

        ax2.set_title(
            "Movies by Release Year"
        )

        ax2.grid(
            alpha=0.2
        )

        st.pyplot(fig2)


# =========================================================
# FOOTER
# =========================================================
# Paste your Kutty Graph right here above the footer
    st.subheader("📊 Top 10 Movies Rating Chart")
    if not filtered_df.empty:
        chart_data = filtered_df.head(10).set_index("Movie Name")["Rating"]
        st.bar_chart(chart_data)
    else:
        st.warning("No data available to display the chart."

)