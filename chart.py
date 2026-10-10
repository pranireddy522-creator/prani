import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Medical Data Visualization Dashboard",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical Data Visualization Dashboard")
st.write("Upload a medical dataset to explore it using four interactive charts.")

# Upload dataset
uploaded_file = st.file_uploader(
    "Upload your medical dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Read CSV or Excel file
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Basic data cleaning
        df.columns = df.columns.astype(str).str.strip()
        df = df.dropna(how="all")

        if df.empty:
            st.error("The uploaded dataset is empty.")
            st.stop()

        st.success("Dataset uploaded successfully!")

        # Dataset overview
        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isna().sum().sum()))

        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Identify numeric and categorical columns
        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_cols = [
            col for col in df.columns
            if col not in numeric_cols
            and df[col].nunique(dropna=True) > 0
        ]

        # --------------------------------
        # CHART 1: BAR CHART
        # --------------------------------
        st.subheader("1. Bar Chart - Category Comparison")

        if categorical_cols:
            bar_col = st.selectbox(
                "Select a category for the bar chart",
                categorical_cols,
                key="bar"
            )

            bar_data = (
                df[bar_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(20)
                .reset_index()
            )
            bar_data.columns = [bar_col, "Count"]

            fig1 = px.bar(
                bar_data,
                x=bar_col,
                y="Count",
                title=f"Count of Records by {bar_col}",
                labels={bar_col: bar_col, "Count": "Number of Records"}
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No categorical columns are available for the bar chart.")

        # --------------------------------
        # CHART 2: PIE CHART
        # --------------------------------
        st.subheader("2. Pie Chart - Category Distribution")

        if categorical_cols:
            pie_col = st.selectbox(
                "Select a category for the pie chart",
                categorical_cols,
                key="pie"
            )

            pie_data = (
                df[pie_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )
            pie_data.columns = [pie_col, "Count"]

            fig2 = px.pie(
                pie_data,
                names=pie_col,
                values="Count",
                title=f"Distribution of {pie_col}",
                hole=0.3
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No categorical columns are available for the pie chart.")

        # --------------------------------
        # CHART 3: HISTOGRAM
        # --------------------------------
        st.subheader("3. Histogram - Numerical Data Distribution")

        if numeric_cols:
            hist_col = st.selectbox(
                "Select a numerical column",
                numeric_cols,
                key="hist"
            )

            fig3 = px.histogram(
                df,
                x=hist_col,
                nbins=30,
                title=f"Distribution of {hist_col}",
                labels={hist_col: hist_col}
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No numerical columns are available for the histogram.")

        # --------------------------------
        # CHART 4: CORRELATION HEATMAP
        # --------------------------------
        st.subheader("4. Heatmap - Medical Data Correlation")

        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()

            fig4 = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Correlation Between Numerical Variables"
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info(
                "The heatmap requires at least two numerical columns."
            )

        # Download cleaned dataset
        st.subheader("Download Data")

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Dataset as CSV",
            data=csv_data,
            file_name="medical_dataset_cleaned.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Unable to process the file: {e}")

else:
    st.info("Please upload a CSV or Excel medical dataset to start.")

st.caption(
    "Educational visualization only. Charts do not provide medical diagnoses."
)