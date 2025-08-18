#!/usr/bin/env python3
"""
Marine Business AI Agent
A comprehensive AI agent for analyzing marine business data and assisting with boat engine sales
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
import json

class MarineBusinessAgent:
    def __init__(self, csv_file_path: str):
        """Initialize the Marine Business AI Agent with CSV data"""
        self.csv_file_path = csv_file_path
        self.data = None
        self.load_data()
        
    def load_data(self):
        """Load and clean the CSV data"""
        try:
            self.data = pd.read_csv(self.csv_file_path)
            print(f"✅ Successfully loaded {len(self.data)} marine businesses")
            self.clean_data()
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.data = pd.DataFrame()
    
    def clean_data(self):
        """Clean and standardize the data"""
        if self.data.empty:
            return
            
        # Remove rows with no company name
        self.data = self.data.dropna(subset=['Company Name'])
        
        # Clean phone numbers
        self.data['Contact Phone'] = self.data['Contact Phone'].astype(str).apply(self.clean_phone)
        
        # Extract state abbreviations
        self.data['State_Code'] = self.data['State'].str[:2]
        
        # Create specialty categories
        self.data['Specialty_Category'] = self.data['Specialty'].apply(self.categorize_specialty)
        
        # Extract engine-related keywords
        self.data['Engine_Keywords'] = self.data['Notes'].astype(str).apply(self.extract_engine_keywords)
        
        print(f"✅ Data cleaned and processed")
    
    def clean_phone(self, phone: str) -> str:
        """Clean and standardize phone numbers"""
        if pd.isna(phone) or phone == 'nan':
            return ''
        
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', str(phone))
        
        # Handle different phone number formats
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return str(phone).strip()
    
    def categorize_specialty(self, specialty: str) -> str:
        """Categorize business specialties"""
        if pd.isna(specialty):
            return 'Unknown'
        
        specialty_lower = str(specialty).lower()
        
        if any(word in specialty_lower for word in ['engine', 'diesel', 'motor']):
            return 'Engine Service'
        elif any(word in specialty_lower for word in ['generator', 'westerbeke']):
            return 'Generator Service'
        elif any(word in specialty_lower for word in ['marina', 'slip']):
            return 'Marina Services'
        elif any(word in specialty_lower for word in ['houseboat', 'rental']):
            return 'Houseboat Services'
        elif any(word in specialty_lower for word in ['repair', 'service']):
            return 'General Repair'
        elif any(word in specialty_lower for word in ['sales', 'dealer']):
            return 'Sales & Dealership'
        else:
            return 'Other'
    
    def extract_engine_keywords(self, notes: str) -> List[str]:
        """Extract engine-related keywords from notes"""
        if pd.isna(notes):
            return []
        
        notes_lower = str(notes).lower()
        keywords = []
        
        engine_terms = [
            'westerbeke', 'yanmar', 'volvo', 'mercury', 'mercruiser',
            'diesel', 'gas', 'engine', 'motor', 'generator', 'kohler',
            'cummins', 'cat', 'caterpillar', 'detroit', 'john deere'
        ]
        
        for term in engine_terms:
            if term in notes_lower:
                keywords.append(term)
        
        return keywords
    
    def get_business_summary(self) -> Dict[str, Any]:
        """Get overall business summary statistics"""
        if self.data.empty:
            return {}
        
        summary = {
            'total_businesses': len(self.data),
            'states_covered': self.data['State'].nunique(),
            'specialty_breakdown': self.data['Specialty_Category'].value_counts().to_dict(),
            'westerbeke_dealers': len(self.data[self.data['Notes'].str.contains('Westerbeke', case=False, na=False)]),
            'engine_service_businesses': len(self.data[self.data['Specialty_Category'] == 'Engine Service']),
            'generator_service_businesses': len(self.data[self.data['Specialty_Category'] == 'Generator Service']),
            'marina_services': len(self.data[self.data['Specialty_Category'] == 'Marina Services'])
        }
        
        return summary
    
    def find_engine_service_businesses(self, state: Optional[str] = None) -> pd.DataFrame:
        """Find businesses that provide engine services"""
        if self.data.empty:
            return pd.DataFrame()
        
        engine_businesses = self.data[
            (self.data['Specialty_Category'].isin(['Engine Service', 'Generator Service'])) |
            (self.data['Notes'].str.contains('engine|motor|diesel', case=False, na=False))
        ].copy()
        
        if state:
            engine_businesses = engine_businesses[engine_businesses['State'] == state]
        
        return engine_businesses.sort_values('Company Name')
    
    def find_westerbeke_dealers(self, state: Optional[str] = None) -> pd.DataFrame:
        """Find Westerbeke dealers"""
        if self.data.empty:
            return pd.DataFrame()
        
        westerbeke_dealers = self.data[
            self.data['Notes'].str.contains('Westerbeke', case=False, na=False)
        ].copy()
        
        if state:
            westerbeke_dealers = westerbeke_dealers[westerbeke_dealers['State'] == state]
        
        return westerbeke_dealers.sort_values('Company Name')
    
    def find_marinas_by_size(self, min_slip_size: int = 50) -> pd.DataFrame:
        """Find marinas that can accommodate boats of a certain size"""
        if self.data.empty:
            return pd.DataFrame()
        
        # Extract slip sizes from notes
        def extract_slip_size(notes):
            if pd.isna(notes):
                return 0
            
            # Look for patterns like "up to 100 ft" or "100-ft slips"
            patterns = [
                r'up to (\d+)\s*ft',
                r'(\d+)\s*ft slips',
                r'(\d+)\s*ft vessels',
                r'accommodates.*?(\d+)\s*ft'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, str(notes), re.IGNORECASE)
                if match:
                    return int(match.group(1))
            
            return 0
        
        self.data['Max_Slip_Size'] = self.data['Notes'].apply(extract_slip_size)
        
        large_marinas = self.data[
            (self.data['Max_Slip_Size'] >= min_slip_size) |
            (self.data['Specialty_Category'] == 'Marina Services')
        ].copy()
        
        return large_marinas.sort_values('Max_Slip_Size', ascending=False)
    
    def find_competitors_by_location(self, state: str, specialty: str = None) -> pd.DataFrame:
        """Find competitors in a specific state and specialty"""
        if self.data.empty:
            return pd.DataFrame()
        
        competitors = self.data[self.data['State'] == state].copy()
        
        if specialty:
            competitors = competitors[competitors['Specialty_Category'] == specialty]
        
        return competitors.sort_values('Company Name')
    
    def generate_sales_leads(self, target_specialty: str = 'Engine Service', 
                           min_contact_info: bool = True) -> pd.DataFrame:
        """Generate sales leads based on criteria"""
        if self.data.empty:
            return pd.DataFrame()
        
        leads = self.data[
            self.data['Specialty_Category'] == target_specialty
        ].copy()
        
        if min_contact_info:
            # Filter for businesses with at least phone or email
            leads = leads[
                (leads['Contact Phone'].notna() & leads['Contact Phone'] != '') |
                (leads['Contact Email'].notna() & leads['Contact Email'] != '')
            ]
        
        # Add lead scoring
        leads['Lead_Score'] = leads.apply(self.calculate_lead_score, axis=1)
        
        return leads.sort_values('Lead_Score', ascending=False)
    
    def calculate_lead_score(self, row) -> int:
        """Calculate lead score based on available information"""
        score = 0
        
        # Contact information
        if pd.notna(row['Contact Phone']) and row['Contact Phone'] != '':
            score += 2
        if pd.notna(row['Contact Email']) and row['Contact Email'] != '':
            score += 2
        if pd.notna(row['Website']) and row['Website'] != '':
            score += 1
        
        # Business details
        if pd.notna(row['Contact Name']) and row['Contact Name'] != '':
            score += 1
        if pd.notna(row['Notes']) and len(str(row['Notes'])) > 50:
            score += 1
        
        # Specialty relevance
        if row['Specialty_Category'] in ['Engine Service', 'Generator Service']:
            score += 3
        
        return score
    
    def export_analysis_report(self, output_file: str = 'marine_analysis_report.json'):
        """Export comprehensive analysis report"""
        if self.data.empty:
            print("❌ No data to analyze")
            return
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.get_business_summary(),
            'top_engine_service_businesses': self.find_engine_service_businesses().head(20).to_dict('records'),
            'westerbeke_dealers': self.find_westerbeke_dealers().to_dict('records'),
            'large_marinas': self.find_marinas_by_size(50).head(20).to_dict('records'),
            'sales_leads': self.generate_sales_leads().head(30).to_dict('records'),
            'state_breakdown': self.data['State'].value_counts().to_dict(),
            'specialty_breakdown': self.data['Specialty_Category'].value_counts().to_dict()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Analysis report exported to {output_file}")
    
    def interactive_analysis(self):
        """Interactive analysis interface"""
        print("\n🚢 Marine Business AI Agent - Interactive Analysis")
        print("=" * 50)
        
        while True:
            print("\nAvailable commands:")
            print("1. Business Summary")
            print("2. Find Engine Service Businesses")
            print("3. Find Westerbeke Dealers")
            print("4. Find Large Marinas")
            print("5. Generate Sales Leads")
            print("6. Export Report")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                summary = self.get_business_summary()
                print("\n📊 Business Summary:")
                for key, value in summary.items():
                    print(f"   {key.replace('_', ' ').title()}: {value}")
            
            elif choice == '2':
                state = input("Enter state (or press Enter for all): ").strip()
                businesses = self.find_engine_service_businesses(state if state else None)
                print(f"\n🔧 Engine Service Businesses ({len(businesses)} found):")
                for _, business in businesses.head(10).iterrows():
                    print(f"   {business['Company Name']} - {business['State']}")
                    print(f"     Specialty: {business['Specialty']}")
                    print(f"     Contact: {business['Contact Phone']}")
                    print()
            
            elif choice == '3':
                state = input("Enter state (or press Enter for all): ").strip()
                dealers = self.find_westerbeke_dealers(state if state else None)
                print(f"\n⚡ Westerbeke Dealers ({len(dealers)} found):")
                for _, dealer in dealers.head(10).iterrows():
                    print(f"   {dealer['Company Name']} - {dealer['State']}")
                    print(f"     Contact: {dealer['Contact Name']} - {dealer['Contact Phone']}")
                    print()
            
            elif choice == '4':
                min_size = input("Enter minimum slip size in feet (default 50): ").strip()
                min_size = int(min_size) if min_size.isdigit() else 50
                marinas = self.find_marinas_by_size(min_size)
                print(f"\n🏖️ Marinas with {min_size}+ ft slips ({len(marinas)} found):")
                for _, marina in marinas.head(10).iterrows():
                    print(f"   {marina['Company Name']} - {marina['State']}")
                    print(f"     Max slip size: {marina['Max_Slip_Size']} ft")
                    print()
            
            elif choice == '5':
                specialty = input("Enter target specialty (default: Engine Service): ").strip()
                specialty = specialty if specialty else 'Engine Service'
                leads = self.generate_sales_leads(specialty)
                print(f"\n🎯 Sales Leads for {specialty} ({len(leads)} found):")
                for _, lead in leads.head(10).iterrows():
                    print(f"   {lead['Company Name']} - {lead['State']}")
                    print(f"     Lead Score: {lead['Lead_Score']}")
                    print(f"     Contact: {lead['Contact Phone']}")
                    print()
            
            elif choice == '6':
                filename = input("Enter output filename (default: marine_analysis_report.json): ").strip()
                filename = filename if filename else 'marine_analysis_report.json'
                self.export_analysis_report(filename)
            
            elif choice == '7':
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please try again.")

def main():
    """Main function to run the Marine Business AI Agent"""
    csv_file = "merged_central_current - merged_central.csv"
    
    try:
        agent = MarineBusinessAgent(csv_file)
        
        if agent.data.empty:
            print("❌ Failed to load data. Please check the CSV file.")
            return
        
        # Run interactive analysis
        agent.interactive_analysis()
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")

if __name__ == "__main__":
    main()
