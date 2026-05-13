import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("Sales Analysis Dashboard")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    excel_file = pd.ExcelFile(uploaded_file)

    all_data = []

    for sheet in excel_file.sheet_names:
        df = pd.read_excel(uploaded_file, sheet_name=sheet)
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    # Cleaning
    combined_df = combined_df.dropna(subset=['Revenue'])
    combined_df = combined_df[combined_df['Revenue'] != 0]

    combined_df['Date'] = pd.to_datetime(combined_df['Date'])

    # Sidebar filters
    st.sidebar.header("Filters")

    region = st.sidebar.multiselect(
        "Region",
        combined_df['Region'].unique(),
        default=combined_df['Region'].unique()
    )

    product = st.sidebar.multiselect(
        "Product",
        combined_df['Product'].unique(),
        default=combined_df['Product'].unique()
    )

    salesperson = st.sidebar.multiselect(
        "Salesperson",
        combined_df['Salesperson'].unique(),
        default=combined_df['Salesperson'].unique()
    )

    channel = st.sidebar.multiselect(
        "Channel",
        combined_df['Channel'].unique(),
        default=combined_df['Channel'].unique()
    )

    filtered_df = combined_df[
        (combined_df['Region'].isin(region)) &
        (combined_df['Product'].isin(product)) &
        (combined_df['Salesperson'].isin(salesperson)) &
        (combined_df['Channel'].isin(channel))
    ]

    # Display dataset
    st.subheader("Cleaned Dataset")
    st.dataframe(filtered_df)

    # KPIs
    total_revenue = filtered_df['Revenue'].sum()
    total_quantity = filtered_df['Units_Sold'].sum()
    avg_revenue = filtered_df['Revenue'].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"{total_revenue:,.2f}")
    col2.metric("Total Quantity Sold", f"{total_quantity:,.0f}")
    col3.metric("Average Revenue", f"{avg_revenue:,.2f}")

    # Revenue by Product
    product_revenue = (
        filtered_df.groupby('Product')['Revenue']
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        product_revenue,
        x='Product',
        y='Revenue',
        title='Revenue by Product'
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Monthly revenue trend
    filtered_df['Month'] = filtered_df['Date'].dt.strftime('%Y-%m')

    monthly_revenue = (
        filtered_df.groupby('Month')['Revenue']
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        monthly_revenue,
        x='Month',
        y='Revenue',
        title='Monthly Revenue Trend'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Tree map
    salesperson_revenue = (
        filtered_df.groupby('Salesperson')['Revenue']
        .sum()
        .reset_index()
    )

    fig3 = px.treemap(
        salesperson_revenue,
        path=['Salesperson'],
        values='Revenue',
        title='Revenue by Salesperson'
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Pie chart
    channel_revenue = (
        filtered_df.groupby('Channel')['Revenue']
        .sum()
        .reset_index()
    )

    fig4 = px.pie(
        channel_revenue,
        names='Channel',
        values='Revenue',
        title='Revenue by Channel'
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Top 5 products
    st.subheader("Top 5 Products by Revenue")

    top_products = (
        filtered_df.groupby('Product')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    st.table(top_products)

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download Cleaned Data",
        csv,
        "cleaned_sales_data.csv",
        "text/csv"
    )