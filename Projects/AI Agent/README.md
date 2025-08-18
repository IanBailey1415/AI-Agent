# 🚢 Marine Business AI Agent

A simple AI tool that analyzes your marine business data and helps you find customers for boat engine sales.

## 🎯 What It Does

- Finds engine service businesses that need your products
- Identifies Westerbeke dealers for partnerships
- Locates large marinas that serve big boats
- Generates sales leads with contact information
- Analyzes your market by state and specialty

## 🚀 Quick Start

### 1. Install Python
- **Download Python 3.8 or higher** from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

### 2. Open Command Prompt
- Press `Win + R`, type `cmd`, press Enter
- Navigate to your project folder:
```cmd
cd "C:\Users\ianba\Github Resume\Projects\AI Agent"
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Run the Agent
```cmd
python demo.py
```

## 📊 Your Data

- **199 marine businesses** across 15 states
- **No database needed** - works directly with your CSV file
- **Automatic analysis** - categorizes businesses by specialty

## ❓ Why No SQL?

**You don't need SQL because:**
- ✅ Your dataset is small (199 businesses)
- ✅ CSV is faster for simple analysis
- ✅ No setup or maintenance required
- ✅ Works immediately on any computer

**Consider SQL later when you have:**
- 1,000+ businesses to manage
- Multiple users needing access
- Complex reporting requirements

## 🎮 How to Use

### Run Demo (See Everything):
```cmd
python demo.py
```

### Interactive Mode (Menu-Driven):
```cmd
python marine_business_agent.py
```

### Test Your Data:
```cmd
python test_csv.py
```

## 🔧 If Something Goes Wrong

### "python not found":
```cmd
python3 demo.py
```

### "pandas not found":
```cmd
pip install pandas numpy openpyxl xlrd
```

### "pip not found":
```cmd
python -m pip install -r requirements.txt
```

## 📁 Files You Need

- `marine_business_agent.py` - Main AI agent
- `demo.py` - Quick demonstration
- `merged_central_current - merged_central.csv` - Your data
- `requirements.txt` - Python packages needed

