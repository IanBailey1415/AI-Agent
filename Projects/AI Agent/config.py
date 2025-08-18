# Configuration file for Marine Business AI Agent

# CSV file configuration
CSV_FILENAME = "merged_central_current - merged_central.csv"

# Business categorization keywords
ENGINE_KEYWORDS = [
    'westerbeke', 'yanmar', 'volvo', 'mercury', 'mercruiser',
    'diesel', 'gas', 'engine', 'motor', 'generator', 'kohler',
    'cummins', 'cat', 'caterpillar', 'detroit', 'john deere'
]

# Specialty categories and their keywords
SPECIALTY_CATEGORIES = {
    'Engine Service': ['engine', 'diesel', 'motor'],
    'Generator Service': ['generator', 'westerbeke'],
    'Marina Services': ['marina', 'slip'],
    'Houseboat Services': ['houseboat', 'rental'],
    'General Repair': ['repair', 'service'],
    'Sales & Dealership': ['sales', 'dealer']
}

# Lead scoring weights
LEAD_SCORING = {
    'contact_phone': 2,
    'contact_email': 2,
    'website': 1,
    'contact_name': 1,
    'detailed_notes': 1,
    'engine_specialty': 3,
    'generator_specialty': 3
}

# Marina slip size patterns for extraction
SLIP_SIZE_PATTERNS = [
    r'up to (\d+)\s*ft',
    r'(\d+)\s*ft slips',
    r'(\d+)\s*ft vessels',
    r'accommodates.*?(\d+)\s*ft',
    r'(\d+)\s*ft boats',
    r'vessels up to (\d+)\s*ft'
]

# Default values
DEFAULT_MIN_SLIP_SIZE = 50
DEFAULT_TARGET_SPECIALTY = 'Engine Service'
DEFAULT_OUTPUT_FILENAME = 'marine_analysis_report.json'

# Display settings
MAX_DISPLAY_ITEMS = 10
REPORT_ITEMS_LIMIT = 20
