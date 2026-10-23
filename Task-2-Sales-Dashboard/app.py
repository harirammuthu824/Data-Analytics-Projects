import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

st.title("Superstore Sales & Profit Dashboard")
st.caption("Interactive retail sales analysis using Python, Pandas, Streamlit, and Plotly.")

uploaded_file = st.file_uploader("Upload your Superstore CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Upload a Superstore CSV file to view the dashboard.")
    st.markdown("""
    **Expected columns:** Order Date, Sales, Profit, Category, Region, Order ID.

    The CSV should have one header row and consistent comma-separated columns.
    """)
    st.stop()

try:
    df = pd.read_csv(uploaded_file, encoding="latin-1")
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

df.columns = df.columns.str.strip()
required = ["Order Date", "Sales", "Profit", "Category", "Region", "Order ID"]
missing = [column for column in required if column not in df.columns]

if missing:
    st.error("Required columns are missing: " + ", ".join(missing))
    st.write("Columns found in your file:", df.columns.tolist())
    st.stop()

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df = df.dropna(subset=["Order Date", "Sales", "Profit"])

if df.empty:
    st.error("No valid sales records were found. Check the CSV file and date format.")
    st.stop()

st.sidebar.header("Dashboard Filters")
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

categories = sorted(df["Category"].dropna().astype(str).unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Product category", categories, default=categories
)
regions = sorted(df["Region"].dropna().astype(str).unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Region", regions, default=regions
)

filtered = df[
    df["Category"].astype(str).isin(selected_categories)
    & df["Region"].astype(str).isin(selected_regions)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["Order Date"].dt.date.between(start_date, end_date)
    ]

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order ID"].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Sales", f"${total_sales:,.2f}")
k2.metric("Total Profit", f"${total_profit:,.2f}")
k3.metric("Total Orders", f"{total_orders:,}")
k4.metric("Profit Margin", f"{profit_margin:.2f}%")

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

monthly = (
    filtered.assign(Month=filtered["Order Date"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)

st.subheader("Monthly Sales Trend")
st.plotly_chart(
    px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly Sales"),
    use_container_width=True,
)

left, right = st.columns(2)

category_summary = (
    filtered.groupby("Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)
with left:
    st.subheader("Sales by Category")
    st.plotly_chart(
        px.bar(category_summary, x="Category", y="Sales", title="Category Sales"),
        use_container_width=True,
    )

region_summary = (
    filtered.groupby("Region", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)
with right:
    st.subheader("Profit by Region")
    st.plotly_chart(
        px.bar(region_summary, x="Region", y="Profit", title="Regional Profit"),
        use_container_width=True,
    )

st.subheader("Category and Region Summary")
st.dataframe(category_summary, use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_superstore_sales.csv",
    mime="text/csv",
)

st.caption("Note: Dashboard findings depend on the dataset uploaded by the user.")
