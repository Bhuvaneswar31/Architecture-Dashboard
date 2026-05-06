import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Architecture Dashboard", layout="wide")

# -----------------------
# BACKGROUND IMAGE
# -----------------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
    background-size: cover;
    background-attachment: fixed;
}
.block-container {
    background-color: rgba(0,0,0,0.75);
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# LOAD DATA
# -----------------------
file = "Architecture_Dashboard_Data.xlsx"

projects = pd.read_excel(file, sheet_name="Projects_Data")
funnel = pd.read_excel(file, sheet_name="Funnel_Data")
revenue = pd.read_excel(file, sheet_name="Revenue_Data")

data = projects.merge(revenue, on="Project_ID")

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.title("Filters")

city = st.sidebar.multiselect("City", data["City"].unique(), default=data["City"].unique())
ptype = st.sidebar.multiselect("Project Type", data["Type"].unique(), default=data["Type"].unique())
status = st.sidebar.multiselect("Status", data["Status"].unique(), default=data["Status"].unique())

filtered = data[
    (data["City"].isin(city)) &
    (data["Type"].isin(ptype)) &
    (data["Status"].isin(status))
]

# -----------------------
# KPI CALCULATIONS
# -----------------------
total_projects = filtered["Project_ID"].nunique()
completed = filtered[filtered["Status"]=="Completed"]["Project_ID"].count()
active = filtered[filtered["Status"]=="Ongoing"]["Project_ID"].count()

total_revenue = filtered["Revenue (₹)"].sum()
total_profit = filtered["Profit (₹)"].sum()

visitors = funnel["Visitors"].sum()
enquiries = funnel["Enquiries"].sum()
visits = funnel["Site_Visits"].sum()
clients = funnel["Clients"].sum()

# -----------------------
# ADVANCED KPI CALCULATIONS (NEW ADDED)
# -----------------------
overall_conversion = clients / visitors if visitors else 0
lead_conversion = enquiries / visitors if visitors else 0
visit_conversion = visits / enquiries if enquiries else 0
client_conversion = clients / visits if visits else 0
roi = total_profit / filtered["Cost (₹)"].sum() if filtered["Cost (₹)"].sum() else 0

# -----------------------
# TITLE
# -----------------------
st.markdown("<h1 style='text-align:center;'>ARCHITECTURE PERFORMANCE ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Data Visualization & Business Insights</h4>", unsafe_allow_html=True)

# -----------------------
# KPI SECTION
# -----------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Projects", total_projects)
col2.metric("Active", active)
col3.metric("Completed", completed)
col4.metric("Clients", clients)
col5.metric("Revenue", f"₹{total_revenue:,.0f}")
col6.metric("Profit", f"₹{total_profit:,.0f}")

# -----------------------
# ADVANCED KPIs (UPDATED AS REQUESTED)
# -----------------------
col7, col8, col9, col10, col11 = st.columns(5)

col7.metric("Overall Conversion", f"{overall_conversion:.2%}")
col8.metric("Lead Conversion", f"{lead_conversion:.2%}")
col9.metric("Visit Conversion", f"{visit_conversion:.2%}")
col10.metric("Client Conversion", f"{client_conversion:.2%}")
col11.metric("ROI", f"{roi:.2%}")

# -----------------------
# FUNNEL + TREND
# -----------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("Conversion Funnel")

    funnel_data = pd.DataFrame({
        "Stage": ["Visitors", "Enquiries", "Site Visits", "Clients"],
        "Count": [visitors, enquiries, visits, clients]
    })

    fig_funnel = px.funnel(funnel_data, x="Count", y="Stage")
    st.plotly_chart(fig_funnel, use_container_width=True)

with colB:
    st.subheader("Monthly Trends")

    fig_trend = px.line(
        funnel,
        x="Month",
        y=["Visitors", "Clients"],
        markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------
# PROJECT ANALYSIS
# -----------------------
colC, colD = st.columns(2)

with colC:
    st.subheader("Projects by City")
    fig_city = px.bar(filtered, x="City", color="Type")
    st.plotly_chart(fig_city, use_container_width=True)

with colD:
    st.subheader("Project Status")
    fig_status = px.pie(filtered, names="Status", hole=0.4)
    st.plotly_chart(fig_status, use_container_width=True)

# -----------------------
# FINANCIAL ANALYSIS
# -----------------------
colE, colF = st.columns(2)

with colE:
    st.subheader("Revenue by Project")
    fig_rev = px.bar(filtered, x="Project_Name", y="Revenue (₹)")
    st.plotly_chart(fig_rev, use_container_width=True)

with colF:
    st.subheader("Profit by City")
    profit_city = filtered.groupby("City")["Profit (₹)"].sum().reset_index()
    fig_profit = px.bar(profit_city, x="City", y="Profit (₹)")
    st.plotly_chart(fig_profit, use_container_width=True)

# -----------------------
# DYNAMIC INSIGHTS (UPDATED)
# -----------------------
st.subheader("Key Insights")

# Safe calculations
top_city = filtered.groupby("City")["Revenue (₹)"].sum().idxmax() if not filtered.empty else "N/A"
top_city_revenue = filtered.groupby("City")["Revenue (₹)"].sum().max() if not filtered.empty else 0

# Conversion drop analysis
drop1 = enquiries - visits
drop2 = visits - clients

if drop1 > drop2:
    biggest_drop = "Enquiries → Site Visits"
else:
    biggest_drop = "Site Visits → Clients"

# Best performing project type
best_type = filtered.groupby("Type")["Profit (₹)"].sum().idxmax() if not filtered.empty else "N/A"

# Completion insight
avg_completion = filtered["Completion_%"].mean() if not filtered.empty else 0

# Build dynamic insights text
insights_text = f"""
- Overall conversion rate is **{overall_conversion:.2%}**, based on current filtered data.
- Highest revenue is generated from **{top_city} (₹{top_city_revenue:,.0f})**.
- Major drop observed in **{biggest_drop} stage**, indicating process inefficiency.
- **{best_type} projects** are generating the highest profit.
- Average project completion stands at **{avg_completion:.1f}%**.
- ROI is currently **{roi:.2%}**, reflecting financial performance.
"""

st.success(insights_text)