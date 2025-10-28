# 🤖 ROBO ADVISOR

A sophisticated Streamlit application that provides AI-powered ETF portfolio recommendations tailored to your investment profile and risk tolerance.

## Features

- **Personalized Portfolio Recommendations**: AI-driven suggestions based on your investment goals
- **Multi-Currency Support**: Invest in USD, EUR, GBP, CHF, JPY, CAD, or AUD
- **Interactive Visualizations**: Beautiful charts showing asset allocation and projected growth
- **Risk Management**: Clear understanding of portfolio risk and expected losses
- **ETF Focus**: Low-cost, liquid ETF recommendations with transparent fees
- **Buying Strategies**: Time-spread or price-range recommendations for each asset

## Installation

### Local Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API Key**:
   - Create a `.streamlit` folder in the project root
   - Create a `secrets.toml` file inside `.streamlit/`
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-api-key-here"
     ```
   - Get your API key from: https://platform.openai.com/api-keys

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and navigate to `http://localhost:8501`

## Deployment on Streamlit Cloud

### Step 1: Prepare Your Repository

1. Create a GitHub repository with the following structure:
   ```
   robo-advisor/
   ├── app.py
   ├── requirements.txt
   └── README.md
   ```

2. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/robo-advisor.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file (app.py)
5. Click "Advanced settings"
6. Add your secrets:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```
7. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app` in a few minutes!

## Usage Guide

### 1. Home Page
- Review the introduction and features
- Click "Get Started with Your Investment Plan"

### 2. Investment Profile (Input Page)
Fill in your investment preferences:
- **Currency**: Select your preferred investment currency
- **Investable Savings Amount**: Total amount you want to invest
- **Risk Profile**: Choose Low (Conservative), Medium (Balanced), or High (Aggressive)
- **Maximum Yearly Loss Tolerated**: The maximum percentage loss you're comfortable with
- **Investment Time Horizon**: How many years until you need the money

Click "Generate Investment Recommendation" to receive your personalized portfolio.

### 3. Results Page
Review your customized portfolio including:
- **Portfolio Overview**: Key metrics including risk level and expected returns
- **Portfolio Commentary**: AI explanation of why this portfolio suits your needs
- **Asset Allocation Table**: Detailed breakdown of recommended ETFs
- **Asset Details**: Descriptions and links for each recommended ETF
- **Visualization Charts**: 
  - Asset allocation by class (Equity, Bonds, etc.)
  - Asset allocation by currency
  - Portfolio value projection over time with uncertainty bands
- **Buying Strategies**: Recommended timing and price ranges for purchases

## Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **OpenAI API (gpt-4o-mini)**: AI-powered portfolio recommendations
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation and analysis

### API Configuration
The app uses OpenAI's `gpt-4o-mini` model to generate portfolio recommendations. The model considers:
- Current market conditions
- Your investment profile and risk tolerance
- ETF liquidity and management fees
- Optimal diversification strategies
- Time-appropriate buying strategies

### Error Handling
The application includes comprehensive error handling for:
- Invalid API keys
- API call failures
- Malformed JSON responses
- Invalid user inputs
- Missing required fields

## Security Notes

⚠️ **Important Security Considerations**:
- Never commit your `secrets.toml` file to version control
- Add `.streamlit/secrets.toml` to your `.gitignore` file
- Keep your OpenAI API key confidential
- For Streamlit Cloud deployment, use the platform's secure secrets management

## File Structure

```
robo-advisor/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .streamlit/
    └── secrets.toml           # API keys (DO NOT COMMIT)
```

## Customization

### Modify Currency Options
Edit the currency list in `show_input_page()`:
```python
currency = st.selectbox(
    "Currency",
    options=["USD", "EUR", "GBP", "CHF", "JPY", "CAD", "AUD", "CNY", "INR"],
    ...
)
```

### Adjust Risk Profiles
Modify risk profile options in `show_input_page()`:
```python
risk_profile = st.selectbox(
    "Risk Profile",
    options=["Very Low", "Low", "Medium", "High", "Very High"],
    ...
)
```

### Change Chart Colors
Customize visualization colors by modifying the Plotly chart configurations in `show_results_page()`.

## Troubleshooting

### "API key not found" Error
- Ensure `.streamlit/secrets.toml` exists and contains your API key
- For Streamlit Cloud, verify secrets are configured in app settings

### "Invalid JSON response" Error
- The AI model occasionally returns malformed responses
- Click "Generate New Recommendation" to retry
- If the issue persists, check your API key and quota

### Charts Not Displaying
- Ensure Plotly is installed: `pip install plotly`
- Clear browser cache and reload the page

### App Runs Slowly
- The AI generation typically takes 10-30 seconds
- Ensure stable internet connection
- Check OpenAI API status if delays persist

## Support

For issues or questions:
- OpenAI API Documentation: https://platform.openai.com/docs
- Streamlit Documentation: https://docs.streamlit.io
- Create an issue in this repository

## License

This project is provided as-is for educational and personal use.

## Disclaimer

⚠️ **Investment Disclaimer**: This application provides AI-generated suggestions for educational purposes only. It is not professional financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

---

Built with ❤️ using Streamlit and OpenAI