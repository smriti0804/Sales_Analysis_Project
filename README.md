# Sales_Analysis_Project

## Approach Used

The solution was developed using Python and Pandas for data cleaning, transformation, and analysis. All sheets from the Excel workbook were dynamically loaded and merged into a single DataFrame to avoid hardcoding. Data preprocessing included removing records with missing or zero revenue values and converting the Date column into datetime format for accurate filtering and aggregation.

For analysis, groupby operations and pivot tables were used to calculate regional revenue summaries and product-level insights. Visualizations were created using Matplotlib and Seaborn to display revenue trends and top-performing products. Additionally, a Streamlit dashboard was developed to provide an interactive interface with filters, KPIs, charts, and downloadable cleaned data functionality.

## Key Assumptions

It was assumed that all Excel sheets follow a consistent schema and contain required columns such as Date, Region, Revenue, Product, Units Sold, Salesperson, and Channel. The automation workflow assumes that Excel files placed inside the data folder contain valid sales records and that the Date column is available for generating weekly summaries.

## Challenges Faced

One challenge was designing the workflow dynamically without hardcoding sheet names or filenames. Another challenge involved handling multiple Excel sheets and ensuring proper date conversion for weekly filtering and aggregation. Building an interactive Streamlit dashboard with dynamic filters and charts while keeping the application responsive was also an important consideration.


Streamlit App Link: https://salesdashboard-3mu8m5ksrckybgggzjm2xz.streamlit.app/ 
