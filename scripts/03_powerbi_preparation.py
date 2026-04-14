"""
Power BI Data Integration & Visualization Preparation Script
Prepares data and creates visualizations for Power BI dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

class PowerBIPreparation:
    def __init__(self, processed_data_dir='processed_data', reports_dir='reports'):
        self.processed_data_dir = processed_data_dir
        self.reports_dir = reports_dir
        
    def load_processed_data(self):
        """Load all processed CSV files"""
        try:
            self.unified_data = pd.read_csv(os.path.join(self.processed_data_dir, 'unified_energy_data.csv'))
            self.forecast_data = pd.read_csv(os.path.join(self.processed_data_dir, 'forecast_results.csv'))
            self.actual_predicted = pd.read_csv(os.path.join(self.processed_data_dir, 'actual_vs_predicted.csv'))
            
            # Convert timestamp columns
            self.unified_data['Timestamp'] = pd.to_datetime(self.unified_data['Timestamp'])
            self.forecast_data['Timestamp'] = pd.to_datetime(self.forecast_data['Timestamp'])
            self.actual_predicted['Timestamp'] = pd.to_datetime(self.actual_predicted['Timestamp'])
            
            print("✓ All data files loaded successfully")
            
            # Check for anomalies file
            anomalies_file = os.path.join(self.processed_data_dir, 'anomalies_detected.csv')
            if os.path.exists(anomalies_file):
                self.anomalies = pd.read_csv(anomalies_file)
                self.anomalies['Timestamp'] = pd.to_datetime(self.anomalies['Timestamp'])
                print("✓ Anomalies file loaded")
            else:
                self.anomalies = pd.DataFrame()
                print("✓ No anomalies file found")
            
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def create_powerbi_data_sources(self):
        """Create clean data sources for Power BI"""
        print("\n" + "="*80)
        print("🔹 CREATING POWER BI DATA SOURCES")
        print("="*80)
        
        # 1. Summary KPIs
        summary_data = self._create_summary_kpis()
        summary_file = os.path.join(self.reports_dir, 'PowerBI_Summary_KPIs.csv')
        summary_data.to_csv(summary_file, index=False)
        print(f"\n✓ Summary KPIs: {summary_file}")
        
        # 2. Device Analysis Data
        device_analysis = self._create_device_analysis()
        device_file = os.path.join(self.reports_dir, 'PowerBI_Device_Analysis.csv')
        device_analysis.to_csv(device_file, index=False)
        print(f"✓ Device Analysis: {device_file}")
        
        # 3. Time Series Data
        timeseries_file = os.path.join(self.reports_dir, 'PowerBI_TimeSeries.csv')
        self.unified_data.to_csv(timeseries_file, index=False)
        print(f"✓ Time Series Data: {timeseries_file}")
        
        # 4. Forecast Data
        forecast_file = os.path.join(self.reports_dir, 'PowerBI_Forecasts.csv')
        self.forecast_data.to_csv(forecast_file, index=False)
        print(f"✓ Forecast Data: {forecast_file}")
        
        # 5. Actual vs Predicted
        actual_pred_file = os.path.join(self.reports_dir, 'PowerBI_Actual_vs_Predicted.csv')
        self.actual_predicted.to_csv(actual_pred_file, index=False)
        print(f"✓ Actual vs Predicted: {actual_pred_file}")
        
        # 6. Anomalies Data
        if not self.anomalies.empty:
            anomalies_file = os.path.join(self.reports_dir, 'PowerBI_Anomalies.csv')
            self.anomalies.to_csv(anomalies_file, index=False)
            print(f"✓ Anomalies Data: {anomalies_file}")
        
        # 7. Hourly Patterns
        hourly_patterns = self._create_hourly_patterns()
        hourly_file = os.path.join(self.reports_dir, 'PowerBI_Hourly_Patterns.csv')
        hourly_patterns.to_csv(hourly_file, index=False)
        print(f"✓ Hourly Patterns: {hourly_file}")
        
        print("\n✅ All Power BI data sources created!")
        
        return True
    
    def _create_summary_kpis(self):
        """Create summary KPI data"""
        total_consumption = self.unified_data['Energy_Consumption_KWh'].sum()
        avg_consumption = self.unified_data['Energy_Consumption_KWh'].mean()
        max_consumption = self.unified_data['Energy_Consumption_KWh'].max()
        min_consumption = self.unified_data['Energy_Consumption_KWh'].min()
        
        data = {
            'KPI_Name': ['Total Consumption', 'Average Consumption', 'Peak Consumption', 'Minimum Consumption'],
            'KPI_Value': [total_consumption, avg_consumption, max_consumption, min_consumption],
            'Unit': ['KWh', 'KWh', 'KWh', 'KWh']
        }
        
        return pd.DataFrame(data)
    
    def _create_device_analysis(self):
        """Create device-wise analysis data"""
        device_stats = self.unified_data.groupby('Device').agg({
            'Energy_Consumption_KWh': ['sum', 'mean', 'max', 'std', 'count']
        }).reset_index()
        
        device_stats.columns = ['Device', 'Total_Consumption', 'Avg_Consumption', 'Max_Consumption', 'Std_Dev', 'Records']
        
        # Add percentage
        total = device_stats['Total_Consumption'].sum()
        device_stats['Percentage'] = (device_stats['Total_Consumption'] / total * 100).round(2)
        
        # Add location
        device_stats['Location'] = device_stats['Device'].apply(lambda x: 
            'Office' if 'Office' in x else ('Library' if 'Library' in x else 'AC_Room')
        )
        
        return device_stats
    
    def _create_hourly_patterns(self):
        """Create hourly consumption patterns"""
        hourly_data = self.unified_data.copy()
        hourly_data['Hour'] = hourly_data['Timestamp'].dt.hour
        
        hourly_patterns = hourly_data.groupby(['Hour', 'Device']).agg({
            'Energy_Consumption_KWh': ['mean', 'min', 'max', 'std']
        }).reset_index()
        
        hourly_patterns.columns = ['Hour', 'Device', 'Avg_Consumption', 'Min_Consumption', 'Max_Consumption', 'Std_Dev']
        
        return hourly_patterns
    
    def create_visualizations(self):
        """Create comprehensive visualizations for analysis"""
        print("\n" + "="*80)
        print("🔹 CREATING VISUALIZATIONS")
        print("="*80)
        
        # Create figure with subplots for Page 1: Overview
        fig1 = plt.figure(figsize=(16, 10))
        fig1.suptitle('Page 1: Energy Consumption Overview', fontsize=16, fontweight='bold')
        
        # Plot 1: Total consumption over time
        ax1 = plt.subplot(2, 2, 1)
        daily_consumption = self.unified_data.groupby(self.unified_data['Timestamp'].dt.date)['Energy_Consumption_KWh'].sum()
        ax1.plot(daily_consumption.index, daily_consumption.values, linewidth=2, marker='o', color='#1f77b4')
        ax1.set_title('Daily Total Consumption Trend', fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Energy Consumption (KWh)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Average consumption
        ax2 = plt.subplot(2, 2, 2)
        avg_value = self.unified_data['Energy_Consumption_KWh'].mean()
        ax2.barh(['Average'], [avg_value], color='#2ca02c', height=0.5)
        ax2.set_title('Average Consumption', fontweight='bold')
        ax2.set_xlabel('Energy Consumption (KWh)')
        for i, v in enumerate([avg_value]):
            ax2.text(v + 5, i, f'{v:.2f} KWh', va='center')
        
        # Plot 3: Hourly trend
        ax3 = plt.subplot(2, 2, 3)
        hourly_avg = self.unified_data.groupby('Hour')['Energy_Consumption_KWh'].mean()
        ax3.plot(hourly_avg.index, hourly_avg.values, linewidth=2, marker='o', color='#d62728')
        ax3.set_title('Hourly Consumption Pattern', fontweight='bold')
        ax3.set_xlabel('Hour of Day')
        ax3.set_ylabel('Average Energy Consumption (KWh)')
        ax3.set_xticks(range(0, 24, 2))
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Key metrics
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        metrics_text = f"""
        KEY METRICS:
        
        Total Consumption: {self.unified_data['Energy_Consumption_KWh'].sum():.2f} KWh
        Average: {self.unified_data['Energy_Consumption_KWh'].mean():.2f} KWh
        Peak: {self.unified_data['Energy_Consumption_KWh'].max():.2f} KWh
        Min: {self.unified_data['Energy_Consumption_KWh'].min():.2f} KWh
        Std Dev: {self.unified_data['Energy_Consumption_KWh'].std():.2f}
        
        Peak Hour: {self.unified_data.groupby('Hour')['Energy_Consumption_KWh'].mean().idxmax()}:00
        Total Records: {len(self.unified_data):,}
        """
        ax4.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center', 
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        page1_file = os.path.join(self.reports_dir, 'Page1_Overview.png')
        plt.savefig(page1_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Page 1 (Overview): {page1_file}")
        plt.close()
        
        # ============ Page 2: Device Analysis ============
        fig2 = plt.figure(figsize=(16, 10))
        fig2.suptitle('Page 2: Device-wise Analysis', fontsize=16, fontweight='bold')
        
        devices = self.unified_data['Device'].unique()
        
        # Plot 1: Device consumption comparison
        ax1 = plt.subplot(2, 2, 1)
        device_totals = self.unified_data.groupby('Device')['Energy_Consumption_KWh'].sum().sort_values(ascending=True)
        colors = plt.cm.Set3(np.linspace(0, 1, len(device_totals)))
        ax1.barh(device_totals.index, device_totals.values, color=colors)
        ax1.set_title('Total Consumption by Device', fontweight='bold')
        ax1.set_xlabel('Energy Consumption (KWh)')
        for i, v in enumerate(device_totals.values):
            ax1.text(v + 100, i, f'{v:,.0f}', va='center')
        
        # Plot 2: Device pie chart
        ax2 = plt.subplot(2, 2, 2)
        ax2.pie(device_totals.values, labels=device_totals.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Energy Consumption Distribution', fontweight='bold')
        
        # Plot 3: Box plot comparison
        ax3 = plt.subplot(2, 2, 3)
        data_for_box = [self.unified_data[self.unified_data['Device'] == device]['Energy_Consumption_KWh'].values for device in devices]
        bp = ax3.boxplot(data_for_box, labels=devices, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        ax3.set_title('Consumption Distribution by Device', fontweight='bold')
        ax3.set_ylabel('Energy Consumption (KWh)')
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot 4: Device average comparison
        ax4 = plt.subplot(2, 2, 4)
        device_avg = self.unified_data.groupby('Device')['Energy_Consumption_KWh'].mean().sort_values(ascending=False)
        ax4.bar(range(len(device_avg)), device_avg.values, color=colors)
        ax4.set_xticks(range(len(device_avg)))
        ax4.set_xticklabels(device_avg.index, rotation=45, ha='right')
        ax4.set_title('Average Consumption by Device', fontweight='bold')
        ax4.set_ylabel('Average Energy Consumption (KWh)')
        for i, v in enumerate(device_avg.values):
            ax4.text(i, v + 2, f'{v:.1f}', ha='center')
        
        plt.tight_layout()
        page2_file = os.path.join(self.reports_dir, 'Page2_Device_Analysis.png')
        plt.savefig(page2_file, dpi=300, bbox_inches='tight')
        print(f"✓ Page 2 (Device Analysis): {page2_file}")
        plt.close()
        
        # ============ Page 3: Forecast & Anomalies ============
        fig3 = plt.figure(figsize=(16, 10))
        fig3.suptitle('Page 3: Forecasting & Anomaly Detection', fontsize=16, fontweight='bold')
        
        # Plot 1: Forecast sample
        ax1 = plt.subplot(2, 2, 1)
        device = self.actual_predicted['Device'].unique()[0]
        device_actual = self.actual_predicted[self.actual_predicted['Device'] == device].head(100)
        ax1.plot(device_actual['Timestamp'], device_actual['Actual'], label='Actual', linewidth=2, marker='o', markersize=4)
        ax1.plot(device_actual['Timestamp'], device_actual['Predicted'], label='Predicted', linewidth=2, linestyle='--', marker='s', markersize=4)
        ax1.set_title(f'Actual vs Predicted - {device}', fontweight='bold')
        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('Energy Consumption (KWh)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot 2: Forecast for all devices
        ax2 = plt.subplot(2, 2, 2)
        for device in self.forecast_data['Device'].unique():
            device_forecast = self.forecast_data[self.forecast_data['Device'] == device]
            ax2.plot(device_forecast['Timestamp'], device_forecast['Forecasted_Consumption'], 
                    label=device, linewidth=2, marker='o', markersize=4)
        ax2.set_title('Next 24 Hours Forecast', fontweight='bold')
        ax2.set_xlabel('Timestamp')
        ax2.set_ylabel('Forecasted Energy Consumption (KWh)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot 3: Anomalies
        ax3 = plt.subplot(2, 2, 3)
        if not self.anomalies.empty:
            # Plot normal data
            ax3.scatter(self.unified_data['Timestamp'], self.unified_data['Energy_Consumption_KWh'], 
                       alpha=0.5, s=10, label='Normal Data', color='blue')
            # Highlight anomalies
            ax3.scatter(self.anomalies['Timestamp'], self.anomalies['Energy_Consumption_KWh'], 
                       color='red', s=100, marker='x', linewidth=2, label='Anomalies')
            ax3.set_title('Anomaly Detection (Red = Anomalies)', fontweight='bold')
        else:
            ax3.scatter(self.unified_data['Timestamp'], self.unified_data['Energy_Consumption_KWh'], 
                       alpha=0.5, s=10, label='Normal Data', color='blue')
            ax3.set_title('No Anomalies Detected', fontweight='bold')
        ax3.set_xlabel('Timestamp')
        ax3.set_ylabel('Energy Consumption (KWh)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot 4: Residual plot
        ax4 = plt.subplot(2, 2, 4)
        if len(self.actual_predicted) > 0:
            residuals = self.actual_predicted['Actual'] - self.actual_predicted['Predicted']
            ax4.scatter(self.actual_predicted['Predicted'], residuals, alpha=0.6)
            ax4.axhline(y=0, color='r', linestyle='--', linewidth=2)
            ax4.set_title('Residual Plot (Accuracy Check)', fontweight='bold')
            ax4.set_xlabel('Predicted Values')
            ax4.set_ylabel('Residuals (Actual - Predicted)')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        page3_file = os.path.join(self.reports_dir, 'Page3_Forecast_Anomalies.png')
        plt.savefig(page3_file, dpi=300, bbox_inches='tight')
        print(f"✓ Page 3 (Forecast & Anomalies): {page3_file}")
        plt.close()
        
        print("\n✅ All visualizations created!")
        
        return True
    
    def generate_powerbi_instructions(self):
        """Generate instructions for creating Power BI dashboard"""
        instructions = """
╔════════════════════════════════════════════════════════════════════════════════╗
║           POWER BI DASHBOARD CREATION INSTRUCTIONS                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

📊 IMPORTING DATA INTO POWER BI
================================

1. OPEN POWER BI DESKTOP
   • Launch Power BI Desktop
   • Click "Get Data" → "Text/CSV"

2. IMPORT DATA SOURCES
   
   DATA SOURCES TO IMPORT (from 'reports' folder):
   ✓ PowerBI_Summary_KPIs.csv
   ✓ PowerBI_Device_Analysis.csv
   ✓ PowerBI_TimeSeries.csv
   ✓ PowerBI_Forecasts.csv
   ✓ PowerBI_Actual_vs_Predicted.csv
   ✓ PowerBI_Hourly_Patterns.csv
   ✓ PowerBI_Anomalies.csv (if available)

3. CREATE RELATIONSHIPS
   
   Connect tables using common columns:
   • TimeSeries → Device_Analysis: Device column
   • Forecasts → Summary_KPIs: Create measures from KPIs
   • Actual_vs_Predicted → TimeSeries: Device & Timestamp

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 PAGE 1: OVERVIEW
====================

VISUALIZATIONS:
├─ KPI Card: Total Consumption (KWh)
├─ KPI Card: Average Consumption
├─ KPI Card: Peak Consumption
├─ Line Chart: Daily Trend (Date vs Total KWh)
├─ Bar Chart: Consumption by Hour
└─ Matrix: Summary Statistics

FILTERS:
• Date Range Slicer
• Device Filter

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 PAGE 2: DEVICE ANALYSIS
===========================

VISUALIZATIONS:
├─ Pie Chart: Energy % by Device
├─ Bar Chart: Total Consumption by Device
├─ Box Plot: Consumption Distribution
├─ Table: Device Statistics (Total, Avg, Max, Min)
└─ Clustered Bar: Hourly Pattern by Device

FILTERS:
• Device Slicer
• Location Filter

KEY METRICS:
• Which device consumes most?
• Device contribution percentage
• Peak consumption device

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 PAGE 3: FORECASTING & ANOMALY DETECTION
============================================

VISUALIZATIONS:
├─ Line Chart: Actual vs Predicted (24-hour sample)
├─ Line Chart: Next 24h Forecast by Device
├─ Scatter Plot: Anomaly Visualization (Red points = Anomalies)
├─ Table: Top Anomalies Detected
└─ Gauge: Forecast Accuracy (R² Score)

FILTERS:
• Device Slicer
• Time Period Filter

KEY METRICS:
• Number of anomalies detected
• Anomaly severity (Z-score)
• Forecast accuracy (R² value)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 DESIGN RECOMMENDATIONS
==========================

COLOR SCHEME:
• Primary: #1f77b4 (Blue) - Normal consumption
• Alert: #d62728 (Red) - Anomalies
• Success: #2ca02c (Green) - Optimal
• Neutral: #7f7f7f (Gray) - Background

FONTS:
• Headers: Segoe UI, Bold, 14-16pt
• Labels: Segoe UI, Regular, 11-12pt

LAYOUT:
• Use white background
• Add company logo in header
• Include refresh timestamp
• Add drill-through filters

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 CUSTOM MEASURES (DAX FORMULAS)
=================================

Total Consumption:
    Total Consumption = SUM(TimeSeries[Energy_Consumption_KWh])

Average Consumption:
    Avg Consumption = AVERAGE(TimeSeries[Energy_Consumption_KWh])

Peak Consumption:
    Peak Consumption = MAX(TimeSeries[Energy_Consumption_KWh])

Consumption % by Device:
    Device % = DIVIDE([Total Consumption], CALCULATE([Total Consumption], ALL(Device_Analysis)))

Anomaly Count:
    Anomaly Count = COUNTA(Anomalies[Z_Score])

Forecast Accuracy:
    Forecast Accuracy = CALCULATE(AVERAGE(Actual_vs_Predicted[R2_Score]))

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 PUBLISHING & SHARING
=======================

1. Publish to Power BI Service
   File → Publish → Select Workspace

2. Set Up Automatic Refresh
   • Dataset Settings → Refresh Schedule
   • Set frequency (daily recommended)

3. Share Dashboard
   • Share → Enter email addresses
   • Set permission levels

4. Create Mobile Layout
   • View → Mobile Layout
   • Optimize for phone/tablet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VERIFICATION CHECKLIST
=========================

□ All data sources imported correctly
□ Relationships established
□ Date formats consistent
□ All visualizations showing data
□ Filters working properly
□ Navigation between pages smooth
□ KPI cards displaying correct values
□ Anomalies highlighted clearly
□ Forecast visualizations complete
□ Performance optimized (no slow queries)
□ Published and shared with stakeholders

════════════════════════════════════════════════════════════════════════════════
        For questions or issues, refer to the analysis_summary.txt report
════════════════════════════════════════════════════════════════════════════════
"""
        
        instructions_file = os.path.join(self.reports_dir, 'POWERBI_INSTRUCTIONS.txt')
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"\n✓ Power BI Instructions: {instructions_file}")
        
        return instructions_file
    
    def run_preparation(self):
        """Execute full Power BI preparation"""
        print("\n" + "=" * 80)
        print("POWER BI DATA INTEGRATION & VISUALIZATION PREPARATION")
        print("=" * 80)
        
        if not self.load_processed_data():
            print("❌ Failed to load processed data. Run 02_energy_analysis.py first.")
            return False
        
        self.create_powerbi_data_sources()
        self.create_visualizations()
        self.generate_powerbi_instructions()
        
        print("\n" + "=" * 80)
        print("✅ POWER BI PREPARATION COMPLETE!")
        print("=" * 80 + "\n")
        
        return True

def main():
    prep = PowerBIPreparation()
    prep.run_preparation()

if __name__ == "__main__":
    main()
