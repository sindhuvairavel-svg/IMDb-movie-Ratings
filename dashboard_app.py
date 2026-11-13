import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import random

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
# CUSTOM 3D CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: radial-gradient(circle at top left, #222222 0%, #0d0d0d 40%, #050505 100%);
        color: white;
    }

    /* Main title with 3D shadow */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: #FFD700;
        margin-bottom: 5px;
        text-shadow: 0px 4px 15px rgba(255,215,0,0.4), 0px 1px 2px rgba(0,0,0,0.9);
    }

    .subtitle {
        text-align: center;
        color: #C0C0C0;
        font-size: 17px;
        margin-bottom: 35px;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.6);
    }

    /* 3D Metric cards */
    .metric-card {
        padding: 22px;
        border-radius: 20px;
        background: linear-gradient(145deg, #222222, #0d0d0d);
        border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 15px 35px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.1);
        text-align: center;
        min-height: 135px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.03);
        border-color: #FFD700;
        box-shadow: 0 20px 40px rgba(255,215,0,0.25), inset 0 1px 0 rgba(255,255,255,0.2);
    }

    .metric-icon {
        font-size: 30px;
        filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5));
    }

    .metric-title {
        color: #AAAAAA;
        font-size: 13px;
        letter-spacing: 1px;
        margin-top: 8px;
        font-weight: 600;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 26px;
        font-weight: bold;
        margin-top: 6px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }

    /* Section headings */
    .section-title {
        color: #FFD700;
        font-size: 24px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
        text-shadow: 0 2px 8px rgba(255,215,0,0.2);
    }

    /* 3D Movie cards */
    .movie-card {
        background: linear-gradient(145deg, #1f1f1f, #111111);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 22px;
        margin: 10px 0px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }

    .movie-card:hover {
        border-color: #FFD700;
        transform: translateY(-4px) translateX(4px);
        box-shadow: 0 12px 30px rgba(255,215,0,0.2), inset 0 1px 0 rgba(255,255,255,0.1);
    }

    .movie-name {
        color: white;
        font-size: 18px;
        font-weight: 700;
    }

    .movie-info {
        color: #BBBBBB;
        font-size: 14px;
        margin-top: 6px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717, #080808);
        border-right: 1px solid rgba(255,255,255,0.05);
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
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,215,0,0.5);
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
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        return df
    except FileNotFoundError:
        return None

df = load_data()


# =========================================================
# FILE CHECK
# =========================================================

if df is None:
    st.error("❌ imdb_movies.csv not found!")
    st.info("Make sure imdb_movies.csv and dashboard_app.py are in the same folder.")
    st.stop()


# =========================================================
# CLEAN COLUMN NAMES & DATA
# =========================================================

df.columns = df.columns.str.strip()

if "Rating" in df.columns:
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

if "Rank" in df.columns:
    df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")

if "Year" in df.columns:
    df["Year"] = df["Year"].astype(str).str.extract(r"(\d{4})")[0]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")


# =========================================================
# HEADER
# =========================================================

st.markdown('<div class="main-title">🎬 IMDb TOP 250 MOVIES</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explore • Search • Filter • Analyze the world\'s top-rated movies</div>', unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🎯 Dashboard Filters")
st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔎 Search Movie", placeholder="Enter movie name...")

# Genre Filter (கால்பந்து/ஜெனார் காலம் இருந்தால் மட்டும் ஒர்க் ஆகும்)
selected_genre = "All"
if "Genre" in df.columns:
    genres = ["All"] + sorted(df["Genre"].dropna().unique().tolist())
    selected_genre = st.sidebar.selectbox("🎭 Select Genre", genres)

if "Rating" in df.columns:
    rating_data = df["Rating"].dropna()
    min_rating = float(rating_data.min())
    max_rating = float(rating_data.max())
    selected_rating = st.sidebar.slider("⭐ Minimum Rating", min_value=min_rating, max_value=max_rating, value=min_rating, step=0.1)
else:
    selected_rating = 0

if "Year" in df.columns:
    year_data = df["Year"].dropna()
    if len(year_data) > 0:
        min_year = int(year_data.min())
        max_year = int(year_data.max())
        selected_year = st.sidebar.slider("📅 Minimum Year", min_value=min_year, max_value=max_year, value=min_year)
    else:
        selected_year = 0
else:
    selected_year = 0

# Advanced Sorting Options
sort_by = st.sidebar.selectbox("🔄 Sort By", ["Rank (Ascending)", "Rating (Highest First)", "Year (Newest First)"])


# =========================================================
# FILTERING & SORTING
# =========================================================

filtered_df = df.copy()

if "Rating" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Rating"] >= selected_rating]

if "Year" in filtered_df.columns and selected_year != 0:
    filtered_df = filtered_df[filtered_df["Year"] >= selected_year]

if selected_genre != "All" and "Genre" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

if search_query:
    if "Movie Name" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Movie Name"].astype(str).str.contains(search_query, case=False, na=False)]

# Sorting application
if "Rank" in filtered_df.columns and sort_by == "Rank (Ascending)":
    filtered_df = filtered_df.sort_values("Rank", ascending=True)
elif "Rating" in filtered_df.columns and sort_by == "Rating (Highest First)":
    filtered_df = filtered_df.sort_values("Rating", ascending=False)
elif "Year" in filtered_df.columns and sort_by == "Year (Newest First)":
    filtered_df = filtered_df.sort_values("Year", ascending=False)


# =========================================================
# SURPRISE ME FEATURE (RANDOM MOVIE PICKER)
# =========================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎲 What to Watch?")
if st.sidebar.button("🎲 Surprise Me!"):
    if not filtered_df.empty:
        random_movie = filtered_df.sample(1).iloc[0]
        st.sidebar.success(f"🎉 **{random_movie.get('Movie Name', 'Movie')}** (⭐ {random_movie.get('Rating', 'N/A')})")
    else:
        st.sidebar.warning("No movies found to pick!")


# =========================================================
# METRICS (3D Cards)
# =========================================================

st.markdown('<div class="section-title">📊 Movie Overview</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎥</div>
            <div class="metric-title">TOTAL MOVIES</div>
            <div class="metric-value">{len(filtered_df)}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if len(filtered_df) > 0 and "Rating" in filtered_df.columns:
        avg_rating = filtered_df["Rating"].mean()
        avg_text = f"{avg_rating:.2f} ⭐"
    else:
        avg_text = "N/A"

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-title">AVERAGE RATING</div>
            <div class="metric-value">{avg_text}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if len(filtered_df) > 0 and "Movie Name" in filtered_df.columns:
        if "Rank" in filtered_df.columns:
            top_data = filtered_df.sort_values("Rank")
            top_movie = top_data.iloc[0]["Movie Name"]
        else:
            top_movie = filtered_df.iloc[0]["Movie Name"]
    else:
        top_movie = "N/A"

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🏆</div>
            <div class="metric-title">TOP MOVIE</div>
            <div class="metric-value" style="font-size: 16px; margin-top: 10px;">{top_movie}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    if len(filtered_df) > 0 and "Year" in filtered_df.columns:
        oldest = filtered_df["Year"].min()
        oldest_text = str(int(oldest)) if pd.notna(oldest) else "N/A"
    else:
        oldest_text = "N/A"

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📅</div>
            <div class="metric-title">OLDEST MOVIE YEAR</div>
            <div class="metric-value">{oldest_text}</div>
        </div>
    """, unsafe_allow_html=True)


# =========================================================
# MOVIE TABLE & CSV DOWNLOAD BUTTON
# =========================================================

st.markdown('<div class="section-title">🎞️ Movie Collection</div>', unsafe_allow_html=True)

if len(filtered_df) > 0:
    display_columns = [col for col in ["Rank", "Movie Name", "Rating", "Year", "Genre"] if col in filtered_df.columns]
    display_df = filtered_df[display_columns].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # CSV Download Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Movies as CSV",
        data=csv_data,
        file_name="imdb_filtered_movies.csv",
        mime="text/csv",
    )
else:
    st.warning("⚠️ No movies match your filters.")


# =========================================================
# TOP 10 MOVIES (3D Cards)
# =========================================================

st.markdown('<div class="section-title">🏆 Top 10 Movies</div>', unsafe_allow_html=True)

if len(filtered_df) > 0:
    top10 = filtered_df.head(10)
    
    for _, row in top10.iterrows():
        rank = row.get("Rank", "N/A")
        name = row.get("Movie Name", "Unknown")
        rating = f"{float(row.get('Rating')): .1f}" if pd.notna(row.get("Rating")) else "N/A"
        year = str(int(row.get("Year"))) if pd.notna(row.get("Year")) else "N/A"

        st.markdown(f"""
            <div class="movie-card">
                <div class="movie-name">🏅 #{rank} &nbsp; {name}</div>
                <div class="movie-info">⭐ Rating: {rating} &nbsp;&nbsp;&nbsp; 📅 Year: {year}</div>
            </div>
        """, unsafe_allow_html=True)


# =========================================================
# CHARTS
# =========================================================

st.markdown("---")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="section-title">⭐ Rating Distribution</div>', unsafe_allow_html=True)
    if len(filtered_df) > 0 and "Rating" in filtered_df.columns:
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#111111')
        ax.set_facecolor('#161616')
        ax.hist(filtered_df["Rating"].dropna(), bins=10, color='#FFD700', edgecolor='#222222')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('#FFD700')
        ax.set_xlabel("IMDb Rating")
        ax.set_ylabel("Number of Movies")
        ax.set_title("Movie Rating Distribution")
        ax.grid(alpha=0.15, color='white')
        st.pyplot(fig)

with chart_col2:
    st.markdown('<div class="section-title">📅 Movies by Year</div>', unsafe_allow_html=True)
    if len(filtered_df) > 0 and "Year" in filtered_df.columns:
        year_count = filtered_df["Year"].dropna().astype(int).value_counts().sort_index()
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        fig2.patch.set_facecolor('#111111')
        ax2.set_facecolor('#161616')
        ax2.plot(year_count.index, year_count.values, marker="o", color='#FFD700', linewidth=2)
        ax2.tick_params(colors='white')
        ax2.xaxis.label.set_color('white')
        ax2.yaxis.label.set_color('white')
        ax2.title.set_color('#FFD700')
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Movies")
        ax2.set_title("Movies by Release Year")
        ax2.grid(alpha=0.15, color='white')
        st.pyplot(fig2)


# =========================================================
# DIRECTOR ANALYSIS (If Director Column Exists)
# =========================================================

if "Director" in df.columns:
    st.markdown('<div class="section-title">🎬 Top Directors in Top 250</div>', unsafe_allow_html=True)
    director_counts = filtered_df["Director"].dropna().value_counts().head(10)
    if not director_counts.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        fig3.patch.set_facecolor('#111111')
        ax3.set_facecolor('#161616')
        director_counts.plot(kind='bar', color='#FFD700', ax=ax3)
        ax3.tick_params(colors='white', rotation=45)
        ax3.xaxis.label.set_color('white')
        ax3.yaxis.label.set_color('white')
        ax3.set_xlabel("Director")
        ax3.set_ylabel("Count")
        ax3.grid(alpha=0.15, color='white')
        st.pyplot(fig3)


# =========================================================
# FOOTER CHART
# =========================================================

st.subheader("📊 Top 10 Movies Rating Chart")
if not filtered_df.empty:
    chart_data = filtered_df.head(10).set_index("Movie Name")["Rating"]
    st.bar_chart(chart_data)
else:
    st.warning("No data available to display the chart.")
