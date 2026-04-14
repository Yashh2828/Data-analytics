"""
Industrial IoT Energy Monitoring - Data Analysis & Forecasting
This script performs comprehensive energy consumption analysis, forecasting, and anomaly detection
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

class EnergyAnalyzer:
    def __init__(self, raw_data_dir='raw_data', processed_data_dir='processed_data'):
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        self.datasets = {}
        self.unified_data = None
        self.forecast_results = None
        self.anomalies = None
        
    # ============================================================================
    # TASK 1 & 2: DATA COLLECTION, UNDERSTANDING, CLEANING & PREPARATION
    # ============================================================================
    
    def load_and_understand_data(self):
        """Load all Excel files and display understanding of the data"""
        print("\n" + "="*80)
        print("🔹 TASK 1 & 2: DATA COLLECTION, UNDERSTANDING, CLEANING & PREPARATION")
        print("="*80)
        
        # Find all Excel files
        excel_files = [f for f in os.listdir(self.raw_data_dir) if f.endswith('.xlsx')]
        
        if not excel_files:
            print("⚠️  No Excel files found. Please run 01_generate_sample_data.py first")
            return False
        
        print(f"\n📂 Found {len(excel_files)} Excel files:")
        
        for file in excel_files:
            filepath = os.path.join(self.raw_data_dir, file)
            df = pd.read_excel(filepath)
            
            # Only process files with correct structure (Timestamp + Energy_Consumption_KWh)
            if len(df.columns) != 2 or 'Energy_Consumption_KWh' not in df.columns:
                print(f"\n⏭️  Skipping {file} (incorrect format - not standard energy data)")
                continue
            
            device_name = file.replace('_Energy.xlsx', '')
            self.datasets[device_name] = df
            
            print(f"\n📊 {device_name}:")
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Data Types:\n{df.dtypes}")
            print(f"   Missing Values: {df.isnull().sum().sum()}")
            print(f"   Sample:\n{df.head(3)}")
        
        if len(self.datasets) == 0:
            print("❌ No valid dataset files found in correct format")
            return False
        
        return True
    
    def clean_and_prepare_data(self):
        """Clean and prepare all datasets"""
        print("\n" + "-"*80)
        print("🧹 CLEANING & PREPARATION")
        print("-"*80)
        
        cleaned_datasets = {}
        
        for device_name, df in self.datasets.items():
            print(f"\n🔧 Processing {device_name}...")
            
            # Step 1: Convert timestamp to datetime
            if 'Timestamp' in df.columns:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            elif 'timestamp' in df.columns.str.lower():
                ts_col = [col for col in df.columns if 'timestamp' in col.lower()][0]
                df = df.rename(columns={ts_col: 'Timestamp'})
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            # Step 2: Standardize column names
            column_mapping = {}
            for col in df.columns:
                if 'consumption' in col.lower() or 'kwh' in col.lower() or 'energy' in col.lower():
                    column_mapping[col] = 'Energy_Consumption_KWh'
            
            df = df.rename(columns=column_mapping)
            
            # Step 3: Handle missing values (forward fill then backward fill)
            df['Energy_Consumption_KWh'] = df['Energy_Consumption_KWh'].ffill().bfill()
            
            # Step 4: Remove duplicates
            df = df.drop_duplicates(subset=['Timestamp'], keep='first')
            
            # Step 5: Sort by timestamp
            df = df.sort_values('Timestamp').reset_index(drop=True)
            
            print(f"   ✓ Timestamps converted to datetime")
            print(f"   ✓ Columns standardized")
            print(f"   ✓ Missing values handled: {df['Energy_Consumption_KWh'].isnull().sum()}")
            print(f"   ✓ Duplicates removed: {len(df)} records remain")
            
            cleaned_datasets[device_name] = df
        
        self.datasets = cleaned_datasets
        return True
    
    # ============================================================================
    # TASK 3: DATA INTEGRATION
    # ============================================================================
    
    def integrate_data(self):
        """Merge all datasets into one unified table"""
        print("\n" + "="*80)
        print("🔹 TASK 3: DATA INTEGRATION")
        print("="*80)
        
        all_data = []
        
        for device_name, df in self.datasets.items():
            df_copy = df.copy()
            
            # Add Device column
            df_copy['Device'] = device_name
            
            # Determine Location based on device name
            if 'Office' in device_name:
                df_copy['Location'] = 'Office'
            elif 'AC' in device_name or 'Library' in device_name:
                df_copy['Location'] = 'AC_Room' if 'AC' in device_name else 'Library'
            else:
                df_copy['Location'] = 'Other'
            
            all_data.append(df_copy)
        
        # Merge all data
        self.unified_data = pd.concat(all_data, ignore_index=True)
        self.unified_data = self.unified_data.sort_values('Timestamp').reset_index(drop=True)
        
        print(f"\n✓ Unified dataset created:")
        print(f"  Shape: {self.unified_data.shape}")
        print(f"  Columns: {list(self.unified_data.columns)}")
        print(f"\n  Devices: {self.unified_data['Device'].unique().tolist()}")
        print(f"  Locations: {self.unified_data['Location'].unique().tolist()}")
        print(f"\n  Sample:\n{self.unified_data.head(10)}")
        
        return True
    
    # ============================================================================
    # TASK 4: DATA ANALYSIS
    # ============================================================================
    
    def analyze_data(self):
        """Perform comprehensive data analysis"""
        print("\n" + "="*80)
        print("🔹 TASK 4: DATA ANALYSIS")
        print("="*80)
        
        # Total energy consumption
        total_consumption = self.unified_data['Energy_Consumption_KWh'].sum()
        print(f"\n📊 ENERGY CONSUMPTION SUMMARY:")
        print(f"   Total Energy Consumption: {total_consumption:,.2f} KWh")
        
        # Average usage
        avg_consumption = self.unified_data['Energy_Consumption_KWh'].mean()
        print(f"   Average Consumption: {avg_consumption:,.2f} KWh")
        
        # Peak consumption
        peak_consumption = self.unified_data['Energy_Consumption_KWh'].max()
        peak_time = self.unified_data.loc[self.unified_data['Energy_Consumption_KWh'].idxmax(), 'Timestamp']
        print(f"   Peak Consumption: {peak_consumption:,.2f} KWh at {peak_time}")
        
        # Device-wise comparison
        print(f"\n🔧 DEVICE-WISE COMPARISON:")
        device_stats = self.unified_data.groupby('Device')['Energy_Consumption_KWh'].agg([
            ('Total', 'sum'),
            ('Average', 'mean'),
            ('Max', 'max'),
            ('Min', 'min'),
            ('Std Dev', 'std')
        ]).round(2)
        print(device_stats)
        
        # Location-wise comparison
        print(f"\n📍 LOCATION-WISE COMPARISON:")
        location_stats = self.unified_data.groupby('Location')['Energy_Consumption_KWh'].agg([
            ('Total', 'sum'),
            ('Average', 'mean'),
            ('Percentage', lambda x: f"{(x.sum()/total_consumption)*100:.1f}%")
        ]).round(2)
        print(location_stats)
        
        # Peak consumption time
        self.unified_data['Hour'] = self.unified_data['Timestamp'].dt.hour
        hourly_consumption = self.unified_data.groupby('Hour')['Energy_Consumption_KWh'].mean()
        peak_hour = hourly_consumption.idxmax()
        print(f"\n⏰ PEAK CONSUMPTION TIME:")
        print(f"   Peak Hour: {peak_hour}:00 - {peak_hour+1}:00 ({hourly_consumption[peak_hour]:,.2f} KWh avg)")
        
        # Trend analysis
        print(f"\n📈 TREND ANALYSIS:")
        daily_consumption = self.unified_data.groupby(self.unified_data['Timestamp'].dt.date)['Energy_Consumption_KWh'].sum()
        trend_slope = (daily_consumption.iloc[-1] - daily_consumption.iloc[0]) / len(daily_consumption)
        trend_direction = "📈 Increasing" if trend_slope > 0 else "📉 Decreasing"
        print(f"   {trend_direction}")
        print(f"   Daily Average: {daily_consumption.mean():,.2f} KWh")
        print(f"   Trend Slope: {trend_slope:.2f} KWh per day")
        
        return device_stats
    
    # ============================================================================
    # TASK 5: FEATURE ENGINEERING
    # ============================================================================
    
    def create_features(self):
        """Create features for analysis and forecasting"""
        print("\n" + "="*80)
        print("🔹 TASK 5: FEATURE ENGINEERING")
        print("="*80)
        
        # Extract temporal features
        self.unified_data['Hour'] = self.unified_data['Timestamp'].dt.hour
        self.unified_data['Day_of_Week'] = self.unified_data['Timestamp'].dt.day_name()
        self.unified_data['Date'] = self.unified_data['Timestamp'].dt.date
        self.unified_data['Is_Weekend'] = self.unified_data['Timestamp'].dt.dayofweek >= 5
        
        # Rolling averages
        for window in [6, 12, 24]:  # 6-hour, 12-hour, 24-hour rolling average
            self.unified_data[f'Rolling_Avg_{window}h'] = self.unified_data.groupby('Device')['Energy_Consumption_KWh'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
        
        print(f"\n✓ Features created:")
        print(f"   New columns: {[col for col in self.unified_data.columns if col not in ['Timestamp', 'Energy_Consumption_KWh', 'Device', 'Location']]}")
        print(f"\n  Sample with features:\n{self.unified_data[['Timestamp', 'Device', 'Energy_Consumption_KWh', 'Hour', 'Day_of_Week', 'Rolling_Avg_24h']].head(10)}")
        
        return True
    
    # ============================================================================
    # TASK 6: FORECASTING (LINEAR REGRESSION)
    # ============================================================================
    
    def forecast(self, periods=24):
        """Build Linear Regression forecasting model"""
        print("\n" + "="*80)
        print("🔹 TASK 6: FORECASTING (LINEAR REGRESSION)")
        print("="*80)
        
        self.forecast_results = {}
        
        for device in self.unified_data['Device'].unique():
            device_data = self.unified_data[self.unified_data['Device'] == device].copy()
            device_data = device_data.sort_values('Timestamp').reset_index(drop=True)
            
            # Prepare features for model
            device_data['TimeIndex'] = range(len(device_data))
            device_data['Hour_Encoded'] = device_data['Hour'].values
            device_data['Is_Weekend_Int'] = device_data['Is_Weekend'].astype(int).values
            
            # Features for prediction
            X = device_data[['TimeIndex', 'Hour_Encoded', 'Is_Weekend_Int', 'Rolling_Avg_24h']].bfill().values
            y = device_data['Energy_Consumption_KWh'].values
            
            # Train model
            model = LinearRegression()
            model.fit(X, y)
            
            # Make predictions for the dataset
            predictions = model.predict(X)
            
            # Forecast future periods
            last_time_index = device_data['TimeIndex'].max()
            future_indices = np.arange(last_time_index + 1, last_time_index + periods + 1)
            
            future_X = []
            for idx in future_indices:
                # Extract hour (cycling through 24 hours)
                hour = int((idx % 24))
                is_weekend = int((idx // 24) % 7 >= 5)
                rolling_avg = device_data['Rolling_Avg_24h'].iloc[-1] if len(device_data) > 0 else 100
                future_X.append([idx, hour, is_weekend, rolling_avg])
            
            future_X = np.array(future_X)
            future_predictions = model.predict(future_X)
            future_predictions = np.maximum(future_predictions, 0)  # Ensure no negative values
            
            # Create forecast dataframe
            last_timestamp = device_data['Timestamp'].max()
            future_timestamps = [last_timestamp + timedelta(hours=i+1) for i in range(periods)]
            
            forecast_df = pd.DataFrame({
                'Timestamp': future_timestamps,
                'Forecasted_Consumption': future_predictions,
                'Device': device
            })
            
            self.forecast_results[device] = {
                'model': model,
                'forecast': forecast_df,
                'r2_score': model.score(X, y),
                'actual_vs_predicted': pd.DataFrame({
                    'Timestamp': device_data['Timestamp'],
                    'Actual': y,
                    'Predicted': predictions,
                    'Device': device
                })
            }
            
            print(f"\n🤖 {device} Forecast Model:")
            print(f"   R² Score: {self.forecast_results[device]['r2_score']:.4f}")
            print(f"   Model Coefficients: {model.coef_}")
            print(f"   Intercept: {model.intercept_:.2f}")
            print(f"\n   Next {periods} hours forecast (sample):")
            print(forecast_df.head(5))
        
        return self.forecast_results
    
    # ============================================================================
    # TASK 7: ANOMALY DETECTION (Z-SCORE)
    # ============================================================================
    
    def detect_anomalies(self, z_threshold=3):
        """Detect anomalies using Z-score method"""
        print("\n" + "="*80)
        print("🔹 TASK 7: ANOMALY DETECTION (Z-SCORE)")
        print("="*80)
        
        self.unified_data['Z_Score'] = self.unified_data.groupby('Device')['Energy_Consumption_KWh'].transform(
            lambda x: np.abs(stats.zscore(x))
        )
        
        # Identify anomalies (Z-score > threshold)
        self.anomalies = self.unified_data[self.unified_data['Z_Score'] > z_threshold].copy()
        self.anomalies = self.anomalies.sort_values('Z_Score', ascending=False)
        
        print(f"\n🚨 ANOMALIES DETECTED (Z-Score > {z_threshold}):")
        print(f"   Total Anomalies: {len(self.anomalies)}")
        
        if len(self.anomalies) > 0:
            anomaly_stats = self.anomalies.groupby('Device').size()
            print(f"\n   Anomalies by Device:")
            for device, count in anomaly_stats.items():
                print(f"      {device}: {count} anomalies")
            
            print(f"\n   Top 10 Anomalies:")
            print(self.anomalies[['Timestamp', 'Device', 'Energy_Consumption_KWh', 'Z_Score']].head(10))
            
            # Anomaly types
            print(f"\n   Anomaly Analysis:")
            spikes = self.anomalies[self.anomalies['Energy_Consumption_KWh'] > self.unified_data['Energy_Consumption_KWh'].mean() * 1.5]
            drops = self.anomalies[self.anomalies['Energy_Consumption_KWh'] < self.unified_data['Energy_Consumption_KWh'].mean() * 0.5]
            print(f"      Unusual Spikes: {len(spikes)}")
            print(f"      Unusual Drops: {len(drops)}")
        else:
            print("   ✓ No anomalies detected!")
        
        return self.anomalies
    
    # ============================================================================
    # TASK 8: OUTPUT GENERATION
    # ============================================================================
    
    def generate_outputs(self):
        """Save all processed data and results"""
        print("\n" + "="*80)
        print("🔹 TASK 8: OUTPUT GENERATION")
        print("="*80)
        
        # Save unified clean dataset
        unified_file = os.path.join(self.processed_data_dir, 'unified_energy_data.csv')
        self.unified_data.to_csv(unified_file, index=False)
        print(f"\n✓ Saved unified dataset: {unified_file}")
        
        # Save forecast results for all devices
        forecast_file = os.path.join(self.processed_data_dir, 'forecast_results.csv')
        all_forecasts = pd.concat([result['forecast'] for result in self.forecast_results.values()], ignore_index=True)
        all_forecasts.to_csv(forecast_file, index=False)
        print(f"✓ Saved forecast results: {forecast_file}")
        
        # Save anomalies
        if len(self.anomalies) > 0:
            anomalies_file = os.path.join(self.processed_data_dir, 'anomalies_detected.csv')
            self.anomalies.to_csv(anomalies_file, index=False)
            print(f"✓ Saved anomalies: {anomalies_file}")
        
        # Save actual vs predicted
        actual_pred_file = os.path.join(self.processed_data_dir, 'actual_vs_predicted.csv')
        all_actual_pred = pd.concat([result['actual_vs_predicted'] for result in self.forecast_results.values()], ignore_index=True)
        all_actual_pred.to_csv(actual_pred_file, index=False)
        print(f"✓ Saved actual vs predicted: {actual_pred_file}")
        
        # Generate summary report
        summary = self._generate_summary_report()
        summary_file = os.path.join(self.processed_data_dir, 'analysis_summary.txt')
        with open(summary_file, 'w') as f:
            f.write(summary)
        print(f"✓ Saved analysis summary: {summary_file}")
        
        print(f"\n✅ All outputs saved to '{self.processed_data_dir}' directory")
        
        return True
    
    def _generate_summary_report(self):
        """Generate summary report"""
        report = "="*80 + "\n"
        report += "INDUSTRIAL IOT ENERGY MONITORING - ANALYSIS SUMMARY REPORT\n"
        report += "="*80 + "\n\n"
        
        # Basic Statistics
        report += "1. ENERGY CONSUMPTION SUMMARY\n"
        report += "-"*80 + "\n"
        report += f"   Total Consumption: {self.unified_data['Energy_Consumption_KWh'].sum():,.2f} KWh\n"
        report += f"   Average Consumption: {self.unified_data['Energy_Consumption_KWh'].mean():,.2f} KWh\n"
        report += f"   Peak Consumption: {self.unified_data['Energy_Consumption_KWh'].max():,.2f} KWh\n"
        report += f"   Period: {self.unified_data['Timestamp'].min()} to {self.unified_data['Timestamp'].max()}\n\n"
        
        # Device Comparison
        report += "2. DEVICE-WISE CONSUMPTION\n"
        report += "-"*80 + "\n"
        for device in self.unified_data['Device'].unique():
            device_data = self.unified_data[self.unified_data['Device'] == device]
            total = device_data['Energy_Consumption_KWh'].sum()
            avg = device_data['Energy_Consumption_KWh'].mean()
            percentage = (total / self.unified_data['Energy_Consumption_KWh'].sum()) * 100
            report += f"   {device}: {total:,.2f} KWh ({percentage:.1f}%) | Avg: {avg:,.2f} KWh\n"
        
        report += "\n"
        
        # Peak Hours
        report += "3. PEAK CONSUMPTION ANALYSIS\n"
        report += "-"*80 + "\n"
        hourly = self.unified_data.groupby('Hour')['Energy_Consumption_KWh'].mean()
        peak_hour = hourly.idxmax()
        report += f"   Peak Hour: {peak_hour}:00 - {peak_hour+1}:00\n"
        report += f"   Peak Consumption: {hourly[peak_hour]:,.2f} KWh\n\n"
        
        # Anomalies
        report += "4. ANOMALY DETECTION\n"
        report += "-"*80 + "\n"
        report += f"   Total Anomalies Found: {len(self.anomalies)}\n"
        if len(self.anomalies) > 0:
            for device in self.anomalies['Device'].unique():
                count = len(self.anomalies[self.anomalies['Device'] == device])
                report += f"   {device}: {count} anomalies\n"
        
        report += "\n"
        
        # Forecast Accuracy
        report += "5. FORECAST MODEL PERFORMANCE\n"
        report += "-"*80 + "\n"
        for device, results in self.forecast_results.items():
            r2 = results['r2_score']
            report += f"   {device}: R² Score = {r2:.4f}\n"
        
        report += "\n"
        
        # Recommendations
        report += "6. KEY INSIGHTS & RECOMMENDATIONS\n"
        report += "-"*80 + "\n"
        
        # Find highest consumer
        highest_consumer = self.unified_data.groupby('Device')['Energy_Consumption_KWh'].sum().idxmax()
        report += f"   • Highest Energy Consumer: {highest_consumer}\n"
        
        # Peak usage analysis
        office_peak = self.unified_data[self.unified_data['Device'].str.contains('Office', na=False)]['Energy_Consumption_KWh'].mean()
        ac_peak = self.unified_data[self.unified_data['Device'].str.contains('AC', na=False)]['Energy_Consumption_KWh'].mean()
        if ac_peak > office_peak:
            report += f"   • AC Units consume significantly more energy during peak hours\n"
            report += f"   • Recommendation: Optimize AC temperature settings or schedules\n"
        
        # Anomaly recommendation
        if len(self.anomalies) > 0:
            report += f"   • {len(self.anomalies)} anomalies detected - investigate equipment malfunction\n"
            report += f"   • Recommendation: Check for faulty sensors or equipment degradation\n"
        
        report += f"   • Implement time-based scheduling to reduce peak-hour consumption\n"
        report += f"   • Monitor forecast accuracy and adjust models as needed\n"
        
        report += "="*80 + "\n"
        
        return report
    
    # ============================================================================
    # MAIN EXECUTION
    # ============================================================================
    
    def run_full_analysis(self):
        """Execute complete analysis pipeline"""
        print("\n" + "=" * 80)
        print("=" * 80)
        print("INDUSTRIAL IOT ENERGY MONITORING SYSTEM - COMPLETE ANALYSIS")
        print("=" * 80)
        print("█" * 80)
        
        # Check if raw data exists
        if not self.load_and_understand_data():
            return False
        
        # Execute all tasks in sequence
        self.clean_and_prepare_data()
        self.integrate_data()
        self.analyze_data()
        self.create_features()
        self.forecast(periods=24)
        self.detect_anomalies(z_threshold=3)
        self.generate_outputs()
        
        print("\n" + "=" * 80)
        print("=" * 80)
        print("✅ ANALYSIS COMPLETE - All outputs generated!")
        print("=" * 80 + "\n")
        
        return True

def main():
    analyzer = EnergyAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
