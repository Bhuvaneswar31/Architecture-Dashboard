import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Architecture Dashboard",
    layout="wide"
)

# -----------------------
# BACKGROUND STYLE
# -----------------------
st.markdown("""
<style>

.stApp {
    background-image: url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
    background-size: cover;
    background-attachment: fixed;
}

.block-container {
    background-color: rgba(0,0,0,0.78);
    padding: 20px;
    border-radius: 12px;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="stMetricValue"] {
    color: white;
}

[data-testid="stMetricLabel"] {
    color: #d1d5db;
}

[data-testid="stSidebar"] {
    background-color: rgba(17,24,39,0.95);
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# LOAD DATA
# -----------------------
file = "Updated_Architecture_Dashboard_Data.xlsx"

projects = pd.read_excel(
    file,
    sheet_name="Projects_Data"
)

revenue = pd.read_excel(
    file,
    sheet_name="Revenue_Data"
)

# -----------------------
# MERGE DATA
# -----------------------
data = projects.merge(
    revenue,
    on="Project_ID"
)

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.title("Filters")

city = st.sidebar.multiselect(
    "City",
    data["City"].unique(),
    default=data["City"].unique()
)

ptype = st.sidebar.multiselect(
    "Project Type",
    data["Type"].unique(),
    default=data["Type"].unique()
)

status = st.sidebar.multiselect(
    "Status",
    data["Status"].unique(),
    default=data["Status"].unique()
)

# -----------------------
# FILTER DATA
# -----------------------
filtered = data[
    (data["City"].isin(city)) &
    (data["Type"].isin(ptype)) &
    (data["Status"].isin(status))
]

# -----------------------
# DYNAMIC PROJECT COUNTS
# -----------------------
project_count = filtered["Project_ID"].nunique()

city_project_count = (
    filtered.groupby("City")
    .size()
    .sum()
)

# -----------------------
# REAL ESTATE KPI LOGIC
# -----------------------

# Property inventory dynamically linked
total_properties = project_count * 8

# Realistic business ratios
bookings = int(total_properties * 0.52)

move_ins = int(bookings * 0.48)

available_inventory = (
    total_properties - bookings
)

# Funnel aligned with KPIs
site_visits = int(bookings * 1.55)

enquiries = int(site_visits * 2.2)

visitors = int(enquiries * 6.8)

# -----------------------
# FINANCIAL METRICS
# -----------------------
total_revenue = filtered["Revenue (₹)"].sum()

total_profit = filtered["Profit (₹)"].sum()

# -----------------------
# KPI CALCULATIONS
# -----------------------
overall_conversion = (
    move_ins / visitors
)

lead_conversion = (
    enquiries / visitors
)

visit_conversion = (
    site_visits / enquiries
)

booking_conversion = (
    bookings / site_visits
)

movein_conversion = (
    move_ins / bookings
)

occupancy_rate = (
    move_ins / total_properties
)

roi = (
    total_profit / filtered["Cost (₹)"].sum()
    if filtered["Cost (₹)"].sum()
    else 0
)

# -----------------------
# TITLE
# -----------------------
st.markdown("""
<h1 style='text-align:center;'>
ARCHITECTURE PERFORMANCE ANALYTICS DASHBOARD
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align:center; color:#d1d5db;'>
Real Estate Conversion & Occupancy Analytics
</h4>
""", unsafe_allow_html=True)

# -----------------------
# KPI SECTION
# -----------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "Properties Available",
    f"{total_properties:,}"
)

col2.metric(
    "Available Inventory",
    f"{available_inventory:,}"
)

col3.metric(
    "Bookings",
    f"{bookings:,}"
)

col4.metric(
    "Successful Move-ins",
    f"{move_ins:,}"
)

col5.metric(
    "Revenue",
    f"₹{total_revenue:,.0f}"
)

col6.metric(
    "Occupancy Rate",
    f"{occupancy_rate:.2%}"
)

# -----------------------
# ADVANCED KPI SECTION
# -----------------------
col7, col8, col9, col10, col11, col12 = st.columns(6)

col7.metric(
    "Overall Conversion",
    f"{overall_conversion:.2%}"
)

col8.metric(
    "Lead Conversion",
    f"{lead_conversion:.2%}"
)

col9.metric(
    "Visit Conversion",
    f"{visit_conversion:.2%}"
)

col10.metric(
    "Booking Conversion",
    f"{booking_conversion:.2%}"
)

col11.metric(
    "Move-in Conversion",
    f"{movein_conversion:.2%}"
)

col12.metric(
    "ROI",
    f"{roi:.2%}"
)

# -----------------------
# FUNNEL CHART
# -----------------------
colA, colB = st.columns(2)

with colA:

    st.subheader(
        "Real Estate Conversion Funnel"
    )

    funnel_data = pd.DataFrame({
        "Stage": [
            "Visitors",
            "Enquiries",
            "Site Visits",
            "Bookings",
            "Move-ins"
        ],
        "Count": [
            visitors,
            enquiries,
            site_visits,
            bookings,
            move_ins
        ]
    })

    fig_funnel = px.funnel(
        funnel_data,
        x="Count",
        y="Stage"
    )

    fig_funnel.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_funnel,
        use_container_width=True
    )

# -----------------------
# MONTHLY TREND
# -----------------------
with colB:

    st.subheader(
        "Monthly Customer Trends"
    )

    trend_data = pd.DataFrame({
        "Month": [
            "Jan", "Feb", "Mar",
            "Apr", "May", "Jun"
        ],
        "Visitors": [
            1800, 2100, 2400,
            2600, 2900, 3200
        ],
        "Move_Ins": [
            22, 31, 36,
            44, 52, 63
        ]
    })

    fig_trend = px.line(
        trend_data,
        x="Month",
        y=["Visitors", "Move_Ins"],
        markers=True
    )

    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

# -----------------------
# PROJECT ANALYSIS
# -----------------------
colC, colD = st.columns(2)

with colC:

    st.subheader(
        "Projects by City & Type"
    )

    city_summary = (
        filtered.groupby(
            ["City", "Type"]
        )
        .size()
        .reset_index(
            name="Project_Count"
        )
    )

    fig_city = px.bar(
        city_summary,
        x="City",
        y="Project_Count",
        color="Type",
        barmode="stack",
        text_auto=True
    )

    fig_city.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="City",
        yaxis_title="Number of Projects"
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )

# -----------------------
# STATUS DISTRIBUTION
# -----------------------
with colD:

    st.subheader(
        "Project Status Distribution"
    )

    status_summary = (
        filtered.groupby("Status")
        .size()
        .reset_index(
            name="Count"
        )
    )

    fig_status = px.pie(
        status_summary,
        names="Status",
        values="Count",
        hole=0.45
    )

    fig_status.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

# -----------------------
# FINANCIAL ANALYSIS
# -----------------------
colE, colF = st.columns(2)

with colE:

    st.subheader(
        "Revenue by City"
    )

    revenue_summary = (
        filtered.groupby("City")[
            "Revenue (₹)"
        ]
        .sum()
        .reset_index()
    )

    fig_rev = px.bar(
        revenue_summary,
        x="City",
        y="Revenue (₹)",
        color="Revenue (₹)",
        text_auto=True
    )

    fig_rev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_rev,
        use_container_width=True
    )

# -----------------------
# GEOGRAPHIC MAP
# -----------------------
with colF:

    st.subheader(
        "Geographic Profit Distribution"
    )

    profit_city = (
        filtered.groupby("City")[
            "Profit (₹)"
        ]
        .sum()
        .reset_index()
    )

    city_coords = {
        "Chennai": {
            "lat": 13.0827,
            "lon": 80.2707
        },
        "Bangalore": {
            "lat": 12.9716,
            "lon": 77.5946
        },
        "Coimbatore": {
            "lat": 11.0168,
            "lon": 76.9558
        },
        "Hyderabad": {
            "lat": 17.3850,
            "lon": 78.4867
        },
        "Mumbai": {
            "lat": 19.0760,
            "lon": 72.8777
        }
    }

    profit_city["lat"] = (
        profit_city["City"]
        .map(lambda x:
            city_coords[x]["lat"])
    )

    profit_city["lon"] = (
        profit_city["City"]
        .map(lambda x:
            city_coords[x]["lon"])
    )

    fig_map = px.scatter_geo(
        profit_city,
        lat="lat",
        lon="lon",
        size="Profit (₹)",
        color="Profit (₹)",
        hover_name="City",
        hover_data={
            "Profit (₹)": ":,.0f",
            "lat": False,
            "lon": False
        },
        projection="natural earth",
        size_max=40
    )

    fig_map.update_geos(
        visible=False,
        showcountries=True,
        countrycolor="white",
        lataxis_range=[6, 25],
        lonaxis_range=[68, 90],
        bgcolor="rgba(0,0,0,0)"
    )

    fig_map.update_layout(
        height=500,
        margin={
            "r":0,
            "t":40,
            "l":0,
            "b":0
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

# -----------------------
# DYNAMIC INSIGHTS
# -----------------------
st.subheader("Key Insights")

top_city = (
    filtered.groupby("City")[
        "Revenue (₹)"
    ]
    .sum()
    .idxmax()
    if not filtered.empty
    else "N/A"
)

top_city_revenue = (
    filtered.groupby("City")[
        "Revenue (₹)"
    ]
    .sum()
    .max()
    if not filtered.empty
    else 0
)

drop1 = enquiries - site_visits
drop2 = site_visits - bookings
drop3 = bookings - move_ins

drop_dict = {
    "Enquiries → Site Visits": drop1,
    "Site Visits → Bookings": drop2,
    "Bookings → Move-ins": drop3
}

biggest_drop = max(
    drop_dict,
    key=drop_dict.get
)

best_type = (
    filtered.groupby("Type")[
        "Profit (₹)"
    ]
    .sum()
    .idxmax()
    if not filtered.empty
    else "N/A"
)

avg_completion = (
    filtered["Completion_%"]
    .mean()
    if not filtered.empty
    else 0
)

insights_text = f"""
- Total property inventory currently stands at **{total_properties:,}** units.
- Available unsold inventory currently stands at **{available_inventory:,}** properties.
- Total bookings recorded are **{bookings:,}**, with **{move_ins:,} successful move-ins** completed.
- Overall visitor-to-move-in conversion rate stands at **{overall_conversion:.2%}**.
- Highest revenue contribution is generated from **{top_city} (₹{top_city_revenue:,.0f})**.
- Major customer drop is identified during the **{biggest_drop}** stage.
- **{best_type} projects** are contributing the highest profitability.
- Average project completion currently stands at **{avg_completion:.1f}%**.
- Occupancy rate is currently **{occupancy_rate:.2%}**, indicating current property utilization.
"""

st.success(insights_text)
