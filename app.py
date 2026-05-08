"""
pip install pandas
pip install steamlit
pip install matplotlib
"""
import streamlit as st
import pandas as pd
import time
from pathlib import Path


st.set_page_config(page_title="Security Log Analyzer", layout="wide")

st.title("Security Log Analyzer Dashboard")
st.write("Automatically refreshes log data every few seconds.")


refresh_seconds = st.sidebar.slider(
    "Refresh every X seconds",
    min_value=5,
    max_value=60,
    value=10
)

log_file = st.sidebar.selectbox(
    "Choose log file",
    ["sample_logs.csv", "system_network_log.csv"]
)

placeholder = st.empty()


def load_logs(file_path):
    if not Path(file_path).exists():
        return None

    logs = pd.read_csv(file_path)

    if "timestamp" in logs.columns:
        logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    return logs


while True:
    logs = load_logs(log_file)

    with placeholder.container():
        st.subheader(f"Viewing: {log_file}")

        if logs is None:
            st.error("Log file not found.")
        else:
            st.metric("Total Rows", len(logs))
            st.dataframe(logs)

            if {"status", "ip_address"}.issubset(logs.columns):
                failed_logins = logs[logs["status"] == "failed"]

                suspicious_ips = failed_logins["ip_address"].value_counts()
                suspicious_ips = suspicious_ips[suspicious_ips >= 3]

                col1, col2, col3 = st.columns(3)

                col1.metric("Total Logs", len(logs))
                col2.metric("Failed Logins", len(failed_logins))
                col3.metric("Suspicious IPs", len(suspicious_ips))

                st.subheader("Suspicious IP Addresses")

                if suspicious_ips.empty:
                    st.success("No suspicious IP addresses found.")
                else:
                    st.warning("Suspicious IP activity detected.")
                    st.dataframe(suspicious_ips)

                if "timestamp" in logs.columns:
                    successful_logins = logs[logs["status"] == "success"]

                    after_hours = successful_logins[
                        (successful_logins["timestamp"].dt.hour < 8) |
                        (successful_logins["timestamp"].dt.hour > 18)
                    ]

                    st.subheader("After-Hours Successful Logins")

                    if after_hours.empty:
                        st.success("No after-hours logins found.")
                    else:
                        st.warning("After-hours successful logins detected.")
                        st.dataframe(after_hours)

            else:
                st.info("This file does not contain login status data. Showing raw system/network data only.")

    time.sleep(refresh_seconds)
    st.rerun()