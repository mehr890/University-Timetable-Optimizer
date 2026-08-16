import streamlit as st
import pandas as pd
import joblib
from itertools import product

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="University Timetable Optimizer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 University Timetable Optimizer")
st.write(
    "Generate a personalized, clash-free university timetable "
    "using Machine Learning and optimization."
)

# --------------------------------------------------
# LOAD DATA + MODEL
# --------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("cleaned_timetable.csv")

    data["start_min"] = (
        pd.to_timedelta(
            data["Start Time"].astype(str)
        ).dt.total_seconds() / 60
    )

    data["end_min"] = (
        pd.to_timedelta(
            data["End Time"].astype(str)
        ).dt.total_seconds() / 60
    )

    data["duration"] = (
        data["end_min"] - data["start_min"]
    )

    return data


@st.cache_resource
def load_model():
    return joblib.load("best_timetable_model.pkl")


df = load_data()
model = load_model()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("🎯 Student Preferences")

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

preferred_days = st.sidebar.multiselect(
    "Preferred Days",
    days,
    default=["Monday", "Tuesday", "Wednesday"]
)

avoid_days = st.sidebar.multiselect(
    "Days to Avoid",
    days,
    default=["Friday"]
)

latest_time = st.sidebar.slider(
    "Latest Preferred Class End Time",
    min_value=12,
    max_value=21,
    value=17
)

max_classes = st.sidebar.slider(
    "Maximum Classes Per Day",
    min_value=1,
    max_value=5,
    value=3
)

generate = st.sidebar.button(
    "🚀 Generate Timetable",
    type="primary"
)

# --------------------------------------------------
# CLASH FUNCTION
# --------------------------------------------------

def count_clashes(schedule):

    clashes = 0

    for i in range(len(schedule)):

        for j in range(i + 1, len(schedule)):

            row1 = schedule.iloc[i]
            row2 = schedule.iloc[j]

            if row1["Day"] == row2["Day"]:

                if (
                    row1["start_min"] < row2["end_min"]
                    and
                    row2["start_min"] < row1["end_min"]
                ):
                    clashes += 1

    return clashes


# --------------------------------------------------
# GAP FUNCTION
# --------------------------------------------------

def calculate_gaps(schedule):

    total_gap = 0

    for day in schedule["Day"].unique():

        day_schedule = schedule[
            schedule["Day"] == day
        ].sort_values("start_min")

        for i in range(len(day_schedule) - 1):

            current_end = day_schedule.iloc[i]["end_min"]
            next_start = day_schedule.iloc[i + 1]["start_min"]

            gap = next_start - current_end

            if gap > 0:
                total_gap += gap

    return total_gap


# --------------------------------------------------
# GENERATE TIMETABLE
# --------------------------------------------------

def generate_timetable():

    module_groups = [
        group.to_dict("records")
        for _, group in df.groupby("Module Code")
    ]

    best_schedule = None
    best_score = float("-inf")

    for combination in product(*module_groups):

        schedule = pd.DataFrame(combination)

        # ------------------------------------------
        # Clash penalty
        # ------------------------------------------

        clashes = count_clashes(schedule)

        if clashes > 0:
            continue

        # ------------------------------------------
        # Daily workload
        # ------------------------------------------

        daily_counts = (
            schedule.groupby("Day")
            .size()
        )

        overload = sum(
            max(0, count - max_classes)
            for count in daily_counts
        )

        # ------------------------------------------
        # Preferred days
        # ------------------------------------------

        preferred_count = schedule[
            "Day"
        ].isin(preferred_days).sum()

        # ------------------------------------------
        # Avoided days
        # ------------------------------------------

        avoided_count = schedule[
            "Day"
        ].isin(avoid_days).sum()

        # ------------------------------------------
        # Late classes
        # ------------------------------------------

        late_count = (
            schedule["end_min"]
            > latest_time * 60
        ).sum()

        # ------------------------------------------
        # ML prediction
        # ------------------------------------------

        predicted_rating = model.predict(
            schedule[
                [
                    "Module Code",
                    "Day",
                    "start_min",
                    "end_min",
                    "duration"
                ]
            ]
        )

        schedule["Predicted_Rating"] = predicted_rating

        # ------------------------------------------
        # Score
        # ------------------------------------------

        original_rating = schedule["Rating"].sum()

        ml_rating = predicted_rating.sum()

        gap = calculate_gaps(schedule)

        score = (
            original_rating
            + (0.5 * ml_rating)
            + (5 * preferred_count)
            - (15 * avoided_count)
            - (10 * late_count)
            - (3 * gap)
            - (10 * overload)
        )

        if score > best_score:

            best_score = score
            best_schedule = schedule.copy()

    return best_schedule, best_score


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

if generate:

    with st.spinner("Generating personalized timetable..."):

        schedule, score = generate_timetable()

    if schedule is not None:

        st.success("✅ Timetable generated successfully!")

        # ------------------------------------------
        # Metrics
        # ------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Optimization Score",
            round(score, 2)
        )

        col2.metric(
            "Clashes",
            count_clashes(schedule)
        )

        col3.metric(
            "Modules",
            len(schedule)
        )

        col4.metric(
            "Days Used",
            schedule["Day"].nunique()
        )

        # ------------------------------------------
        # TIMETABLE TABLE
        # ------------------------------------------

        st.subheader("📅 Personalized Timetable")

        display_df = schedule[
            [
                "Module Code",
                "Title",
                "Day",
                "Start Time",
                "End Time",
                "Rating",
                "Predicted_Rating"
            ]
        ].copy()

        day_order = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4
        }

        display_df["day_order"] = (
            display_df["Day"].map(day_order)
        )

        display_df = (
            display_df
            .sort_values(
                ["day_order", "Start Time"]
            )
            .drop(columns=["day_order"])
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # ------------------------------------------
        # DAILY WORKLOAD
        # ------------------------------------------

        st.subheader("📊 Classes Per Day")

        daily_counts = (
            schedule.groupby("Day")
            .size()
            .reindex(days, fill_value=0)
        )

        st.bar_chart(daily_counts)

        # ------------------------------------------
        # DOWNLOAD
        # ------------------------------------------

        csv = display_df.to_csv(index=False)

        st.download_button(
            "⬇️ Download Timetable",
            csv,
            "personalized_timetable.csv",
            "text/csv"
        )

    else:

        st.error(
            "No conflict-free timetable could be generated "
            "with these preferences."
        )

else:

    st.info(
        "👈 Select your preferences and click "
        "**Generate Timetable**."
    )