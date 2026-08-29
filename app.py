import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("📊 E-Commerce Sales Analytics Dashboard")
st.markdown(
    "Analyze sales performance, profit trends, product categories, "
    "and regional business insights."
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    np.random.seed(42)

    dates = pd.date_range(
        start="2023-01-01",
        end="2024-12-31",
        freq="D"
    )

    categories = [
        "Electronics",
        "Furniture",
        "Clothing",
        "Home Appliances",
        "Sports"
    ]

    regions = [
        "North",
        "South",
        "East",
        "West"
    ]

    products = [
        "Laptop",
        "Smartphone",
        "Office Chair",
        "Table",
        "T-Shirt",
        "Shoes",
        "Washing Machine",
        "Refrigerator",
        "Football",
        "Treadmill"
    ]

    n = 2000

    data = pd.DataFrame({
        "Order_ID": range(1001, 1001 + n),
        "Order_Date": np.random.choice(dates, n),
        "Category": np.random.choice(categories, n),
        "Region": np.random.choice(regions, n),
        "Product": np.random.choice(products, n),
        "Sales": np.random.randint(100, 5000, n),
        "Quantity": np.random.randint(1, 10, n)
    })

    data["Profit"] = (
        data["Sales"] *
        np.random.uniform(0.05, 0.30, n)
    ).round(2)

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"]
    )

    return data


df = load_data()

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("🔎 Filter Data")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories))
]

# -------------------------------------------------
# KPI METRICS
# -------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "📦 Products Sold",
    f"{total_quantity:,}"
)

st.divider()

# -------------------------------------------------
# MONTHLY SALES TREND
# -------------------------------------------------

monthly_sales = (
    filtered_df
    .groupby(
        filtered_df["Order_Date"]
        .dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order_Date"] = (
    monthly_sales["Order_Date"]
    .astype(str)
)

fig_sales = px.line(
    monthly_sales,
    x="Order_Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

# -------------------------------------------------
# SALES BY CATEGORY
# -------------------------------------------------

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Product Category"
)

# -------------------------------------------------
# SALES BY REGION
# -------------------------------------------------

region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Regional Sales Distribution"
)

# -------------------------------------------------
# PROFIT BY CATEGORY
# -------------------------------------------------

category_profit = (
    filtered_df
    .groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig_profit = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    title="Profit by Category"
)

# -------------------------------------------------
# DISPLAY CHARTS
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

# -------------------------------------------------
# TOP PRODUCTS
# -------------------------------------------------

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Product",
    y="Sales",
    title="Top Performing Products"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# -------------------------------------------------
# DATA PREVIEW
# -------------------------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "E-Commerce Sales Analytics Dashboard | "
    "Built using Python, Pandas, Plotly and Streamlit"
)
