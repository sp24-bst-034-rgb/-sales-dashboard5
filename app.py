import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from PIL import Image

#  ---------- PAGE CONFIG ---------- 
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# ---------- BASE DIRECTORY ----------
BASE_DIR = Path(__file__).parent

# ---------- LOAD LOGO ----------
LOGO_PATH = BASE_DIR / "LOGO.webp.webp"
logo = Image.open(LOGO_PATH)

# ---------- LOAD & CACHE DATA ----------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"])

    for col in ["Revenue", "Profit", "Quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    return df

FILE_PATH = BASE_DIR / "product_sales_dataset_final (1) (1).csv"
df = load_data(FILE_PATH)

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["Introduction", "Dashboard", "Conclusion"])

# ================= INTRO TAB =================
with tab1:
    st.image(logo, width=220)
    st.title("Sales Dashboard")

    st.write("""
    This dashboard provides an **interactive analysis of Sales, Revenue and Profit performance**.

    ### Objectives
    - Understand monthly performance trends  
    - Compare regions and categories  
    - Evaluate profit contribution  
    - Support better business decisions  
    """)
    st.write("""
    ### What is Sales Analytics?
    Sales analytics is the process of collecting, analyzing and visualizing sales data in order to understand business performance. 
    It helps identify patterns in revenue, profit, product demand and customer behavior.

    ### Why Do We Use Dashboards?
    Dashboards convert large datasets into interactive visual summaries. They allow decision-makers to:
    - Monitor key performance indicators in real-time  
    - Identify profitable products and regions  
    - Detect seasonal trends in sales  
    - Compare performance over months and categories  
    - Make faster and more accurate business decisions  

    ### Role of Data Visualization
    Data visualization makes complex information simple by using graphs and charts. It:
    - reveals relationships between variables  
    - highlights trends and outliers  
    - supports quick decision-making  
    - prevents misinterpretation of raw data  

    ### Real-World Applications of Sales Dashboards
    - business performance monitoring  
    - inventory and stock management  
    - marketing campaign evaluation  
    - customer segmentation  
    - profitability comparison  
    """)

    # ---------- PREPARED BY SECTION ----------
    st.markdown("""
    <hr>
    <h3> Prepared By</h3>
    <p><b>Name:</b> Sania Javaid</p>
    <p><b>Course:</b> Data Visualization (Python Project)</p>
    <p><b>Instructor:</b> Sir Farooq Ahmad</p>
    <p><b>Date:</b> January 2026</p>
    """, unsafe_allow_html=True)

    st.success("Use the tabs above to navigate through the dashboard.")

# ================= DASHBOARD TAB =================
with tab2:
    st.sidebar.image(logo, width=180)
    st.sidebar.header("Filters")

    regions = st.sidebar.multiselect(
        "Select Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

    categories = st.sidebar.multiselect(
        "Select Category",
        sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

    show_heavy = st.sidebar.checkbox("Show Heavy Charts (Slow)", value=False)

    df_filtered = df[df["Region"].isin(regions) & df["Category"].isin(categories)]

    st.markdown("<h1 style='text-align:center;'> Sales Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # ---------- KPIs ----------
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Revenue", f"{df_filtered['Revenue'].sum():,.2f}")
    k2.metric("Total Profit", f"{df_filtered['Profit'].sum():,.2f}")
    k3.metric("Total Orders", len(df_filtered))
    st.divider()

    # ---------- SUMMARY TABLE ----------
    summary = df_filtered.groupby("Category").agg(
        Orders=("Order_ID", "count"),
        Quantity=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    summary["Profit Margin %"] = (summary["Profit"] / summary["Revenue"] * 100).round(2)

    st.subheader("Category Summary")
    st.dataframe(summary, use_container_width=True)
    st.markdown("---")

    # ---------- CHARTS ----------
    chart_list = [
        "Monthly Revenue Trend",
        "Monthly Profit Area",
        "Revenue vs Profit Bubble",
        "Profit Violin by Category",
        "Quantity Strip by Region",
        "Profit Box Plot",
        "3D Scatter",
        "Revenue vs Quantity Scatter",
        "Profit Heatmap (Month vs Category)",
        "Quantity Area Trend",
        "Revenue vs Profit Density"
    ]
    selected = st.sidebar.multiselect("Select Charts", chart_list, default=chart_list[:5])

    if "Monthly Revenue Trend" in selected:
        line = df_filtered.groupby("Month", as_index=False)["Revenue"].sum()
        st.plotly_chart(px.line(line, x="Month", y="Revenue", markers=True, title="Monthly Revenue Trend"), use_container_width=True)

    if "Monthly Profit Area" in selected:
        area = df_filtered.groupby("Month", as_index=False)["Profit"].sum()
        st.plotly_chart(px.area(area, x="Month", y="Profit", title="Monthly Profit Area"), use_container_width=True)

    if "Revenue vs Profit Bubble" in selected:
        st.plotly_chart(px.scatter(df_filtered, x="Revenue", y="Profit", size="Quantity", color="Region",
                                   title="Revenue vs Profit Bubble"), use_container_width=True)

    if "Profit Violin by Category" in selected:
        st.plotly_chart(px.violin(df_filtered, x="Category", y="Profit", color="Category", box=True, points="all",
                                  title="Profit Distribution by Category"), use_container_width=True)

    if "Quantity Strip by Region" in selected:
        st.plotly_chart(px.strip(df_filtered, x="Region", y="Quantity", color="Region", title="Quantity Distribution by Region"),
                        use_container_width=True)

    if "Profit Box Plot" in selected:
        st.plotly_chart(px.box(df_filtered, x="Category", y="Profit", color="Category", points="all",
                               title="Profit Box Plot by Category"), use_container_width=True)

    if "3D Scatter" in selected:
        st.plotly_chart(px.scatter_3d(df_filtered, x="Revenue", y="Profit", z="Quantity", color="Region", size="Profit",
                                      title="3D Scatter: Revenue vs Profit vs Quantity"), use_container_width=True)

    if "Revenue vs Quantity Scatter" in selected:
        st.plotly_chart(px.scatter(df_filtered, x="Revenue", y="Quantity", color="Category", size="Profit",
                                   title="Revenue vs Quantity Scatter"), use_container_width=True)

    if "Profit Heatmap (Month vs Category)" in selected:
        heatmap = df_filtered.groupby(["Month", "Category"], as_index=False)["Profit"].sum()
        heatmap_pivot = heatmap.pivot(index="Category", columns="Month", values="Profit")
        st.plotly_chart(px.imshow(heatmap_pivot, text_auto=True, aspect="auto", title="Profit Heatmap"), use_container_width=True)

    if "Quantity Area Trend" in selected:
        qty_area = df_filtered.groupby("Month", as_index=False)["Quantity"].sum()
        st.plotly_chart(px.area(qty_area, x="Month", y="Quantity", title="Quantity Trend Over Months"), use_container_width=True)

    if "Revenue vs Profit Density" in selected:
        st.plotly_chart(px.density_contour(df_filtered, x="Revenue", y="Profit", color="Region",
                                           title="Revenue vs Profit Density Contour"), use_container_width=True)

# ================= CONCLUSION TAB =================
with tab3:
    st.title("Conclusion & Insights")

    st.write("""
    ### Summary Insights
    The dashboard shows clear variation in revenue, profit and quantity across months, regions and product categories. 
    Some product categories generate high revenue but do not always produce high profit, which may be due to higher costs.

    ### What Managers Can Learn
    - Identify most profitable product categories  
    - Focus marketing on high-revenue regions  
    - Detect months showing declining performance  
    - Improve stock planning based on demand trends  
    - Understand that high sales do not always mean high profit  

    ### Limitations of the Analysis
    - Dashboard results depend on the dataset provided  
    - Missing or incorrect data may affect conclusions  
    - Past trends may not always predict future sales  

    ### Recommendations
    - Apply forecasting to plan inventory and production  
    - Use real-time data integration  
    - Improve pricing strategy for low-profit products  
    - Extend dashboard with customer demographics  

    ### Final Remark
    Dashboards convert **data into information, information into knowledge, and knowledge into better business decisions**.
    """)
