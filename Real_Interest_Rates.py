import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime

# ----------------------------
# Settings: Time Range
# ----------------------------
start = datetime.datetime(1960, 1, 1)
end = datetime.datetime.today()

# ----------------------------
# Download data from FRED
# ----------------------------
# FEDFUNDS = Federal Funds Rate (monthly)
# GS10 = 10-Year Treasury Yield (monthly)
# CPIAUCSL = Consumer Price Index (CPI-U, monthly, seasonally adjusted)
series = {
    "FEDFUNDS": "Federal Funds Rate",
    "GS10": "10-Year Treasury Yield",
    "CPIAUCSL": "CPI (All Urban Consumers)"
}

data = pd.DataFrame()
for code, name in series.items():
    data[name] = pdr.DataReader(code, "fred", start, end)

# Forward-fill missing values (in case of NaN)
data.ffill(inplace=True)

# ----------------------------
# Calculate Year-over-Year Inflation Rate
# ----------------------------
data["CPI Inflation YoY (%)"] = data["CPI (All Urban Consumers)"].pct_change(12) * 100

# ----------------------------
# Compute Real Interest Rates: Nominal - Inflation
# ----------------------------
data["Real Fed Funds Rate (%)"] = data["Federal Funds Rate"] - data["CPI Inflation YoY (%)"]
data["Real 10Y Treasury Rate (%)"] = data["10-Year Treasury Yield"] - data["CPI Inflation YoY (%)"]

# Drop rows with missing values (first 12 months)
data.dropna(inplace=True)

# ----------------------------
# Plot the results
# ----------------------------
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Real Fed Funds Rate (%)"], label="Real Fed Funds Rate", linewidth=1.5)
plt.plot(data.index, data["Real 10Y Treasury Rate (%)"], label="Real 10-Year Treasury Rate", linewidth=1.5)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)

plt.title("US Real Interest Rates (1960–Present)\n(Fed Funds & 10-Year Treasury, CPI-Adjusted)")
plt.xlabel("Year")
plt.ylabel("Real Interest Rate (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
