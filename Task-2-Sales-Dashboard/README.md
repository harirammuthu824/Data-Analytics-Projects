# Task 2: Interactive Sales & Profit Dashboard

## Objective
Build an interactive dashboard to explore Superstore sales and profitability.

## Tools
- Python
- Streamlit
- Pandas
- Plotly

## Features
- KPI cards for Sales, Profit, Orders, and Profit Margin
- Date range filter
- Product category and region filters
- Monthly sales trend
- Category-wise sales
- Region-wise profit
- Summary table and filtered CSV download

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

5. Upload a valid Superstore CSV file in the browser page.

## Expected CSV columns
`Order Date`, `Sales`, `Profit`, `Category`, `Region`, `Order ID`

This is a Python dashboard alternative and does not generate a Power BI `.pbix` file.
