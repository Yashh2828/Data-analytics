"""
Generate Sample Energy Consumption Data
This script creates sample Excel files representing energy consumption
from different systems (Office, AC units, Library)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_office_data():
    """Generate office lighting and equipment energy consumption data"""
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(720)]  # 30 days
    
    # Office consumption pattern (higher during business hours)
    consumption = []
    for date in dates:
        hour = date.hour
        # Higher consumption during 9 AM to 6 PM
        if 9 <= hour < 18:
            base = np.random.normal(150, 20)  # KWh
        else:
            base = np.random.normal(50, 10)   # KWh
        consumption.append(max(base, 0))
    
    # Add some missing values
    indices = np.random.choice(len(dates), 10, replace=False)
    for idx in indices:
        consumption[idx] = np.nan
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Energy_Consumption_KWh': consumption
    })
    
    return df

def generate_ac_front_data():
    """Generate Front AC unit energy consumption data"""
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(720)]
    
    # AC consumption pattern (higher during hot hours)
    consumption = []
    for date in dates:
        hour = date.hour
        day = date.day
        # Higher consumption during 10 AM to 8 PM, especially on certain days
        if 10 <= hour < 20:
            base = np.random.normal(200 + (day % 10) * 5, 30)  # KWh
        else:
            base = np.random.normal(80, 15)  # KWh
        consumption.append(max(base, 0))
    
    # Add some missing values and anomalies
    indices = np.random.choice(len(dates), 15, replace=False)
    for idx in indices:
        if np.random.random() < 0.7:
            consumption[idx] = np.nan
        else:
            consumption[idx] = np.random.normal(450, 50)  # Anomaly spike
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Energy_Consumption_KWh': consumption
    })
    
    return df

def generate_ac_back_data():
    """Generate Back AC unit energy consumption data"""
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(720)]
    
    # Similar pattern to front AC but slightly different
    consumption = []
    for date in dates:
        hour = date.hour
        day = date.day
        if 10 <= hour < 20:
            base = np.random.normal(190 + (day % 8) * 4, 25)
        else:
            base = np.random.normal(75, 12)
        consumption.append(max(base, 0))
    
    # Add some missing values
    indices = np.random.choice(len(dates), 8, replace=False)
    for idx in indices:
        consumption[idx] = np.nan
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Energy_Consumption_KWh': consumption
    })
    
    return df

def generate_library_data():
    """Generate library energy consumption data"""
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(720)]
    
    # Library pattern (constant throughout day, but closed at night)
    consumption = []
    for date in dates:
        hour = date.hour
        # Open from 7 AM to 9 PM
        if 7 <= hour < 21:
            base = np.random.normal(120, 18)
        else:
            base = np.random.normal(20, 5)
        consumption.append(max(base, 0))
    
    # Add some missing values
    indices = np.random.choice(len(dates), 12, replace=False)
    for idx in indices:
        consumption[idx] = np.nan
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Energy_Consumption_KWh': consumption
    })
    
    return df

def main():
    """Generate all sample data files"""
    
    output_dir = 'raw_data'
    
    print("🔹 Generating Sample Energy Consumption Data...")
    
    # Generate data
    office_df = generate_office_data()
    ac_front_df = generate_ac_front_data()
    ac_back_df = generate_ac_back_data()
    library_df = generate_library_data()
    
    # Save to Excel
    files = {
        'Office_Energy.xlsx': office_df,
        'AC_Front_Energy.xlsx': ac_front_df,
        'AC_Back_Energy.xlsx': ac_back_df,
        'Library_Energy.xlsx': library_df
    }
    
    for filename, df in files.items():
        filepath = os.path.join(output_dir, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"✓ Created {filename} with {len(df)} records")
    
    print("\n✅ All sample data files created successfully!")
    print(f"📁 Files saved in '{output_dir}' directory")

if __name__ == "__main__":
    main()
