# FX & Inflation Dashboard Agent

An AI-powered Streamlit application for foreign exchange and inflation analysis. Upload your country's rates or inflation figures, get automatic trend analysis and commentary, and chat with specialized bots about inflation and exchange rates.

## Features

- **Data Upload & Analysis**: Paste exchange rates or inflation figures, get automatic trend analysis and AI-generated commentary
- **Inflation Bot**: Ask questions about inflation meaning, causes, effects, and measurements
- **Exchange Rate Bot**: Ask questions about exchange rate meaning, factors, and trade impacts
- **Data-Qualified Q&A**: Ask questions about your uploaded data and get AI-powered answers and advice

## Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fx-inflation-dashboard.git
cd fx-inflation-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

### Deployment to Streamlit Cloud

1. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push this code to your repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/YOUR_USERNAME/fx-inflation-dashboard.git
     git push -u origin main
     ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the main file path to `app/main.py`
   - Click "Deploy"

Your app will be deployed and accessible via a public URL.

## Usage

### Data Upload Tab
1. Paste your country's rates or inflation figures (Date/Value format)
2. Select data type (Inflation Rate, Exchange Rate, etc.)
3. Enter country name
4. Click "Analyze Data" to get automatic trend commentary

### Inflation Bot Tab
- Ask any question about inflation - meaning, causes, effects, measurements
- Get comprehensive answers powered by the AI agent

### Exchange Rate Bot Tab
- Ask questions about exchange rates - meaning, factors, trade impacts
- Get detailed explanations and insights

## Project Structure

```
fx-inflation-dashboard/
├── app/
│   └── main.py          # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.8+
- streamlit>=1.28.0
- pandas>=2.0.0

## License

MIT License
