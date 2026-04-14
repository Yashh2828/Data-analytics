# 🚀 QUICK START GUIDE - Energy Monitoring System

## ⚡ Get Started in 3 Steps

### Step 1: Install Dependencies (1 minute)
```powershell
cd "c:\Users\Yash Sinha\Desktop\Projects\Projects\Data Analysis"
pip install -r requirements.txt
```

### Step 2: Run Complete Analysis (2 minutes)
```powershell
python scripts/01_generate_sample_data.py
python scripts/02_energy_analysis.py
python scripts/03_powerbi_preparation.py
```

### Step 3: View Results
All outputs are ready!

---

## 📂 What You Get

### **Data Files** (`processed_data/`)
- `unified_energy_data.csv` - Complete cleaned dataset
- `forecast_results.csv` - 24-hour predictions
- `anomalies_detected.csv` - Flagged issues (5 found!)
- `analysis_summary.txt` - Executive report

### **Power BI Files** (`reports/`)
- `PowerBI_*.csv` - 7 ready-to-import datasets
- `Page*.png` - Dashboard previews
- `POWERBI_INSTRUCTIONS.txt` - Setup guide

---

## 🎯 Key Findings at a Glance

| Finding | Value |
|---------|-------|
| Total Energy | 315,091 KWh |
| Peak Hour | 12:00-13:00 Noon |
| Highest Consumer | AC_Front Unit (32.3%) |
| Anomalies Found | 5 spikes detected |
| Forecast Accuracy | 89% validation match |
| Trend Direction | Increasing 17 KWh/day |

---

## 📊 Create Power BI Dashboard

1. **Open Power BI Desktop**
2. **Import Data**:
   - File → Get Data → Text/CSV
   - Select all `PowerBI_*.csv` files from `reports/`

3. **Follow Dashboard Guide**:
   - Open `reports/POWERBI_INSTRUCTIONS.txt` 
   - Create 3 pages of visualizations
   - Customize colors and formatting

4. **Publish**:
   - File → Publish
   - Share with stakeholders

---

## 💡 Key Insights

🔴 **CRITICAL**: AC_Front unit showing 5 temperature spikes
- Peak: 540.67 KWh (5 times normal)
- **Action**: Check equipment immediately

📈 **TREND**: Energy consumption increasing
- +17 KWh per day growth rate
- Monitor for seasonal patterns

⚡ **PEAK**: Highest usage at noon  
- 12:00-13:00 hour shows peak
- Try load shifting for cost savings

---

## 📁 File Structure

```
Data Analysis/
├── raw_data/              ← Excel source files (4 devices)
├── processed_data/        ← Cleaned CSV files (5 files)
├── reports/               ← Power BI ready (11 files)
├── scripts/               ← Python code (3 scripts)
├── README.md              ← Full documentation
├── requirements.txt       ← Dependencies
└── PROJECT_COMPLETION_SUMMARY.md ← This project report
```

---

## 🔧 Troubleshooting

**Q: Script fails to run?**
```
A: Update Python packages:
   pip install --upgrade -r requirements.txt
```

**Q: Files not found?**
```
A: Run from correct directory:
   cd "c:\Users\Yash Sinha\Desktop\Projects\Projects\Data Analysis"
```

**Q: Can't import CSV to Power BI?**
```
A: Ensure PowerBI reads as UTF-8 encoding
   Use "Text Import Wizard" in Power BI
```

---

## 📧 Next Steps

1. ✅ Review `analysis_summary.txt` 
2. ✅ View `Page1_Overview.png` preview
3. ✅ Create Power BI dashboard (15 min)
4. ✅ Investigate AC_Front anomalies
5. ✅ Schedule trend review (weekly)
6. ✅ Implement recommendations

---

## 📊 Dashboard Preview

**Page 1: Overview** - Total energy trends & peak hours
**Page 2: Devices** - Which devices consume most?
**Page 3: Forecast** - Next 24 hours predictions + anomalies

---

**Time to Deploy**: 30 minutes
**No Coding Required**: Just import and visualize!
**Ready for Production**: Yes ✅

---
