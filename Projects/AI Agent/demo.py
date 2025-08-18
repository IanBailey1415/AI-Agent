#!/usr/bin/env python3
"""
Demo script for the Marine Business AI Agent
Shows key capabilities without requiring user interaction
"""

from marine_business_agent import MarineBusinessAgent
import json

def run_demo():
    """Run a demonstration of the Marine Business AI Agent"""
    print("🚢 Marine Business AI Agent - Demo Mode")
    print("=" * 50)
    
    # Initialize the agent
    csv_file = "merged_central_current - merged_central.csv"
    agent = MarineBusinessAgent(csv_file)
    
    if agent.data.empty:
        print("❌ No data loaded. Please check the CSV file.")
        return
    
    print(f"✅ Data loaded successfully: {len(agent.data)} businesses")
    
    # 1. Business Summary
    print("\n📊 BUSINESS SUMMARY")
    print("-" * 30)
    summary = agent.get_business_summary()
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # 2. Top Engine Service Businesses
    print("\n🔧 TOP ENGINE SERVICE BUSINESSES")
    print("-" * 40)
    engine_businesses = agent.find_engine_service_businesses()
    print(f"Found {len(engine_businesses)} engine service businesses")
    
    for i, (_, business) in enumerate(engine_businesses.head(5).iterrows()):
        print(f"{i+1}. {business['Company Name']} - {business['State']}")
        print(f"   Specialty: {business['Specialty']}")
        print(f"   Contact: {business['Contact Phone']}")
        if business['Engine_Keywords']:
            print(f"   Engine Brands: {', '.join(business['Engine_Keywords'])}")
        print()
    
    # 3. Westerbeke Dealers
    print("\n⚡ WESTERBEKE DEALERS")
    print("-" * 25)
    westerbeke_dealers = agent.find_westerbeke_dealers()
    print(f"Found {len(westerbeke_dealers)} Westerbeke dealers")
    
    for i, (_, dealer) in enumerate(westerbeke_dealers.head(5).iterrows()):
        print(f"{i+1}. {dealer['Company Name']} - {dealer['State']}")
        print(f"   Contact: {dealer['Contact Name']} - {dealer['Contact Phone']}")
        print()
    
    # 4. Large Marinas
    print("\n🏖️ LARGE MARINAS (50+ ft slips)")
    print("-" * 35)
    large_marinas = agent.find_marinas_by_size(50)
    print(f"Found {len(large_marinas)} marinas with 50+ ft slips")
    
    for i, (_, marina) in enumerate(large_marinas.head(5).iterrows()):
        print(f"{i+1}. {marina['Company Name']} - {marina['State']}")
        print(f"   Max slip size: {marina['Max_Slip_Size']} ft")
        print()
    
    # 5. Sales Leads
    print("\n🎯 TOP SALES LEADS")
    print("-" * 25)
    sales_leads = agent.generate_sales_leads('Engine Service')
    print(f"Generated {len(sales_leads)} sales leads for Engine Service")
    
    for i, (_, lead) in enumerate(sales_leads.head(5).iterrows()):
        print(f"{i+1}. {lead['Company Name']} - {lead['State']}")
        print(f"   Lead Score: {lead['Lead_Score']}")
        print(f"   Contact: {lead['Contact Phone']}")
        print(f"   Email: {lead['Contact Email']}")
        print()
    
    # 6. State Analysis
    print("\n🗺️ BUSINESS DISTRIBUTION BY STATE")
    print("-" * 40)
    state_counts = agent.data['State'].value_counts()
    print("Top 10 states by business count:")
    for state, count in state_counts.head(10).items():
        print(f"   {state}: {count} businesses")
    
    # 7. Export Report
    print("\n📄 EXPORTING ANALYSIS REPORT")
    print("-" * 35)
    agent.export_analysis_report('demo_marine_report.json')
    
    print("\n🎉 Demo completed successfully!")
    print("Check 'demo_marine_report.json' for the full analysis report.")
    print("\nTo run the full interactive version, use: python marine_business_agent.py")

if __name__ == "__main__":
    run_demo()
