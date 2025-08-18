#!/usr/bin/env python3
"""
Simple test script to verify CSV data can be read
"""

import csv
import sys

def test_csv():
    """Test reading the CSV file"""
    csv_file = "merged_central_current - merged_central.csv"
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            print(f"✅ Successfully read CSV file")
            print(f"📊 Total rows: {len(rows)}")
            print(f"📋 Headers: {rows[0] if rows else 'No headers'}")
            
            if len(rows) > 1:
                print(f"📝 First business: {rows[1][1]} - {rows[1][0]}")  # Company Name - State
                print(f"🔧 Sample specialties found:")
                
                # Count unique states
                states = set()
                specialties = set()
                for row in rows[1:]:  # Skip header
                    if len(row) > 0:
                        states.add(row[0])  # State
                    if len(row) > 6:
                        specialties.add(row[6])  # Specialty
                
                print(f"   States: {len(states)} unique states")
                print(f"   Sample states: {', '.join(list(states)[:5])}")
                print(f"   Sample specialties: {', '.join(list(specialties)[:5])}")
            
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file}")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

if __name__ == "__main__":
    test_csv()
