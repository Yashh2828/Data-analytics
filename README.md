# Industrial IoT Energy Monitoring System
## Complete Data Analysis & Forecasting Project

---

## 📋 PROJECT OVERVIEW

**Objective**: Analyze energy consumption from IoT devices, forecast trends, and detect anomalies.

**Deliverables**:
- ✅ Cleaned dataset: 2,880 hourly records
- ✅ Predictive models: 24-hour forecasts  
- ✅ Anomaly detection: 5 issues found
- ✅ Power BI dashboard: 3 interactive pages
- ✅ Executive report: Key insights & recommendations

**Timeline**: 30-day observation (Jan 1-31, 2024)
**Update**: April 14, 2026

---

## 📊 QUICK RESULTS - METRICS AT A GLANCE

| Metric | Value | Status |
|--------|-------|--------|
| **Total Energy** | 315,091 KWh | Baseline |
| **Average/Hour** | 109.41 KWh | Monitored |
| **Peak Value** | 540.67 KWh | ⚠️ Alert |
| **Peak Time** | 12:00-13:00 | Action |
| **Top Consumer** | AC_Front (32.3%) | Optimize |
| **Anomalies** | 5 spikes | Investigate |
| **Trend** | +17 KWh/day | Increasing |
| **Forecast Model** | R² 0.11-0.14 | Baseline |

---

## 🚀 HOW TO USE - 3 STEPS

### Step 1: Install
```bash
cd "c:\Users\Yash Sinha\Desktop\Projects\Projects\Data Analysis"
pip install -r requirements.txt
```

### Step 2: Run Analysis
```bash
python scripts/01_generate_sample_data.py
python scripts/02_energy_analysis.py
python scripts/03_powerbi_preparation.py
```

### Step 3: View Results
- **Data**: Check `processed_data/` folder
- **Dashboard**: Follow `reports/POWERBI_INSTRUCTIONS.txt`
- **Report**: Read `processed_data/analysis_summary.txt`

**Time**: 5 minutes total

---

## 📁 PROJECT FILES

### Raw Data (`raw_data/`)
```
Office_Energy.xlsx              720 hourly records
AC_Front_Energy.xlsx            720 hourly records
AC_Back_Energy.xlsx             720 hourly records
Library_Energy.xlsx             720 hourly records
```

### Analysis Output (`processed_data/`)
```
unified_energy_data.csv         Complete cleaned dataset (2,880 rows)
forecast_results.csv            24-hour forecasts (96 rows)
actual_vs_predicted.csv         Model validation data
anomalies_detected.csv          5 identified anomalies
analysis_summary.txt            Executive report
```

### Power BI Ready (`reports/`)
```
PowerBI_Summary_KPIs.csv        KPI metrics
PowerBI_Device_Analysis.csv     Device statistics
PowerBI_TimeSeries.csv          Time series data
PowerBI_Forecasts.csv           Forecast data
PowerBI_Actual_vs_Predicted.csv Model accuracy
PowerBI_Hourly_Patterns.csv     Hourly aggregates
PowerBI_Anomalies.csv           Anomaly details
Page1_Overview.png              Dashboard screenshot
Page2_Device_Analysis.png       Dashboard screenshot
Page3_Forecast_Anomalies.png    Dashboard screenshot
POWERBI_INSTRUCTIONS.txt        Dashboard setup guide
```

### Scripts (`scripts/`)
```
01_generate_sample_data.py      Data generation
02_energy_analysis.py           Main analysis engine
03_powerbi_preparation.py       Power BI preparation
```

---

## 🔍 KEY FINDINGS

### Finding #1: Device Energy Distribution
| Device | Total KWh | % Share | Average |
|--------|-----------|---------|---------|
| AC_Front | 101,686 | 32.3% | 141.23 |
| AC_Back | 93,253 | 29.6% | 129.52 |
| Office | 63,242 | 20.1% | 87.84 |
| Library | 56,908 | 18.1% | 79.04 |

**Insight**: AC units consume 61.9% of total energy → **Primary optimization target**

---

### Finding #2: Peak Usage Pattern
- **Peak Hour**: 12:00-13:00 (Noon)
- **Peak Value**: 179.23 KWh average
- **Peak Period**: Business hours 9 AM - 6 PM
- **Off-Peak Reduction**: 55% lower at night

**Insight**: Implement demand management during peak hours for cost savings

---

### Finding #3: Anomalies Detected (5 Total)

| Date | Time | Device | KWh | Z-Score | Type |
|------|------|--------|-----|---------|------|
| Jan 8 | 07:00 | AC_Front | 540.67 | 5.11 | SPIKE |
| Jan 17 | 09:00 | AC_Front | 421.47 | 3.59 | SPIKE |
| Jan 11 | 12:00 | AC_Front | 420.89 | 3.58 | SPIKE |
| Jan 21 | 12:00 | AC_Front | 420.60 | 3.57 | SPIKE |
| Jan 15 | 15:00 | AC_Front | 395.81 | 3.26 | SPIKE |

**Insight**: AC_Front unit shows abnormal consumption spikes → **Requires immediate investigation**

---

### Finding #4: Consumption Trend
- **Direction**: INCREASING
- **Rate**: +17.03 KWh per day
- **Duration**: 30-day period
- **Total Impact**: ~510 additional KWh over month

**Insight**: Monitor trend cause (weather? equipment degradation?)

---

### Finding #5: Forecast Accuracy

| Device | R² Score | Quality |
|--------|----------|---------|
| AC_Back | 0.1350 | Low |
| AC_Front | 0.1121 | Low |
| Office | 0.0304 | Very Low |
| Library | 0.1152 | Low |

**Insight**: Current model captures time-based patterns only. External factors (weather, occupancy) needed for improvement.

---

## 💡 RECOMMENDATIONS

### IMMEDIATE (This Week)
1. **Investigate AC_Front Unit**
   - 5 anomalies detected with 3-5x normal consumption
   - Check thermostat calibration
   - Inspect for equipment degradation/failure

2. **Peak Hour Management**
   - Identify non-critical loads
   - Shift operations to off-peak hours
   - Expected savings: 15-20%

### SHORT-TERM (1 Month)
1. **Enhance Forecasting**
   - Add weather data
   - Include occupancy information
   - Expected R² improvement: 0.50+

2. **Real-time Monitoring**
   - Set anomaly alerts (Z-score > 3)
   - Dashboard refresh: Hourly
   - Integrate with maintenance system

### LONG-TERM (3-6 Months)
1. **Energy Efficiency Program**
   - AC optimization: 15-20% reduction target
   - LED lighting upgrade
   - Improve building insulation

2. **Advanced Analytics**
   - ARIMA/Prophet forecasting models
   - Pattern clustering analysis
   - Predictive maintenance ML

---

# 📊 POWER BI DASHBOARD

## 📄 Page 1: Overview

### Visuals
- KPI Cards:
  - Total Energy Consumption
  - Average Consumption
  - Peak Consumption

- Charts:
  - Daily Energy Consumption Trend (Last 30 Days)
  - Hourly Energy Usage Pattern

- Filter:
  - Device Slicer

### Use Case
Executive summary and trend monitoring of overall energy consumption.


---

## 📄 Page 2: Device Analysis

### Visuals
- Pie Chart:
  - Energy Distribution by Device

- Bar Chart:
  - Device-wise Comparison (Total, Average, Peak)

- Box Plot / Column Chart:
  - Consumption Range (Min vs Max)

- Table:
  - Device Statistics:
    - Total Consumption
    - Average Consumption
    - Peak Consumption
    - Percentage Contribution

- Filter:
  - Location Slicer

### Use Case
Device performance comparison to identify high consumption and inefficiencies.


---

## 🚀 Key Highlights
- Interactive filters for dynamic analysis
- Multi-page dashboard for structured insights
- Comparative and trend-based visualizations
- Supports data-driven decision making

---

## 🔧 TECHNICAL DETAILS

### Technology Stack
```
Python 3.12
Pandas 3.0.2          - Data manipulation
NumPy 2.4.4           - Numerical computing
Scikit-learn 1.8.0    - Machine learning
Matplotlib 3.10.8     - Visualizations
Seaborn 0.13.2        - Statistical plots
SciPy 1.17.1          - Statistical analysis
Power BI              - Dashboard & reporting
```

### Data Processing Steps
1. **Data Ingestion**: Load 4 Excel files
2. **Cleaning**: Handle missing values, standardize formats
3. **Integration**: Combine datasets with device/location tags
4. **Analysis**: Calculate statistics and trends
5. **Feature Engineering**: Create temporal features
6. **Modeling**: Train Linear Regression forecasts
7. **Anomaly Detection**: Z-score statistical test
8. **Output**: Generate reports & Power BI data

### Data Quality
| Metric | Value |
|--------|-------|
| Total Records | 2,880 |
| Missing Values | 0 (after cleaning) |
| Duplicates | 0 |
| Time Range | 30 days |
| Frequency | Hourly (consistent) |
| Completeness | 100% |

---


**Updated**: April 14, 2026

For questions or issues, refer to detailed documentation files in project directory.

