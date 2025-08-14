import pandas as pd
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly

st.title("📦 Amazon Product Sales Forecast")
st.write("Upload historical sales data (CSV with `ds` and `y` columns) to forecast future sales.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.write(data.head())

    # Check if required columns exist
    if "ds" not in data.columns or "y" not in data.columns:
        st.error("CSV must have 'ds' (date) and 'y' (sales) columns.")
    else:
        # Convert date column
        data["ds"] = pd.to_datetime(data["ds"])

        # Plot raw data
        st.subheader("Sales Over Time")
        st.line_chart(data.set_index("ds")["y"])

        # Forecast
        model = Prophet()
        model.fit(data)
        future = model.make_future_dataframe(periods=90)
        forecast = model.predict(future)

        st.subheader("Forecast")
        fig = plot_plotly(model, forecast)
        st.plotly_chart(fig)

        st.subheader("Forecast Data")
        st.write(forecast.tail())

else:
    st.info("Please upload a CSV file to get started.")
