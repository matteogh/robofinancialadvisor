import streamlit as st
import json
from openai import OpenAI
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="ROBO ADVISOR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)


def get_openai_recommendation(investable_amount, risk_profile, max_yearly_loss, time_horizon, currency):
    """Call OpenAI API to get portfolio recommendation"""
    try:
        # Get API key from secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Given the current financial market situation, and the financial expectations over the next 6 months, please propose a balanced portfolio investing in Liquid ETFs preferably with low management fees that can maximize the return over {time_horizon} years keeping the risk limited to have a maximum yearly loss of {max_yearly_loss}%. The portfolio can invest up to {investable_amount} {currency}.
Make sure the proposed ETFs are chosen based on the investments profile given, do not provide general ETFs but rather ETFs that are optimal for the given risk profile: {risk_profile}.
Also propose a time spread or a price range over which the investor can buy each asset (typically over the next 6 months maximum).

For each asset proposed provide a short explanation of the asset (max 2 sentences, potentially adding an external link for more details).

In addition, there must be a comment to the proposed portfolio, explaining the reason why this proposal is an optimal portfolio given the current market situation and the investor preferences.

Please return the result in the following JSON format:
{{
  "portfolio": [
    {{
      "asset_name": "ETF Name",
      "ticker": "TICKER",
      "allocation_percentage": 25.0,
      "investment_amount": 10000,
      "asset_class": "Equity/Bond/Commodity/etc",
      "currency": "USD",
      "description": "Brief description of the asset",
      "link": "https://example.com",
      "buying_strategy": "Buy over next 3 months or between $X-$Y"
    }}
  ],
  "portfolio_commentary": "Explanation of why this portfolio is optimal",
  "expected_annual_return": 7.5,
  "risk_level": "{risk_profile}",
  "max_expected_yearly_loss": {max_yearly_loss}
}}"""

        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial advisor specializing in ETF portfolio construction. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],         
            temperature=0.7
        )
        print('received OPENAI response')
        # Extract and parse JSON response
        response_text = response.choices[0].message.content
        
        # Try to extract JSON if wrapped in markdown
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        portfolio_data = json.loads(response_text.strip())
        return portfolio_data
        
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None


def show_home_page():
    """Display the home page"""
    st.markdown('<div class="main-header">🤖 ROBO ADVISOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Robo Advisor is here to help you in planning and understanding a thoughtful way to invest your savings, with a clear and simple investing through ETF and a transparent risk management</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop", width='stretch')
        
        st.markdown("### Why Choose Our Robo Advisor?")
        st.markdown("""
        - 🎯 **Personalized Recommendations**: Tailored to your risk profile and investment goals
        - 📊 **ETF Focus**: Low-cost, diversified investment options
        - 🔒 **Risk Management**: Clear understanding of potential losses
        - 🌍 **Multi-Currency Support**: Invest in your preferred currency
        - 🤖 **AI-Powered**: Leveraging advanced algorithms for optimal portfolio construction
        """)
        
        if st.button("Get Started with Your Investment Plan", type="primary"):
            st.session_state.page = 'input'
            st.rerun()


def show_input_page():
    """Display the input form page"""
    st.markdown('<div class="main-header">📝 Investment Profile</div>', unsafe_allow_html=True)
    st.markdown("Please provide your investment preferences to receive a personalized portfolio recommendation.")
    
    with st.form("investment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            currency = st.selectbox(
                "Currency",
                options=["USD", "EUR", "GBP", "CHF", "JPY", "CAD", "AUD"],
                help="Select your preferred investment currency"
            )
            
            investable_amount = st.number_input(
                f"Investable Savings Amount ({currency})",
                min_value=1000,
                max_value=10000000,
                value=50000,
                step=1000,
                help="Enter the total amount you want to invest"
            )
            
            risk_profile = st.selectbox(
                "Risk Profile",
                options=["Low", "Medium", "High"],
                index=1,
                help="Low: Conservative, Medium: Balanced, High: Aggressive"
            )
        
        with col2:
            max_yearly_loss = st.number_input(
                "Maximum Yearly Loss Tolerated (%)",
                min_value=1.0,
                max_value=50.0,
                value=15.0,
                step=1.0,
                help="The maximum percentage loss you're comfortable with in a year"
            )
            
            time_horizon = st.number_input(
                "In how many years you plan to use your savings",
                min_value=1,
                max_value=30,
                value=5,
                step=1,
                help="Your investment time horizon in years"
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🚀 Generate Investment Recommendation", type="primary")
        
        if submitted:
            # Validate inputs
            if investable_amount < 1000:
                st.error("Investable amount must be at least 1,000")
            elif max_yearly_loss <= 0:
                st.error("Maximum yearly loss must be greater than 0")
            elif time_horizon < 1:
                st.error("Time horizon must be at least 1 year")
            else:
                # Store user inputs
                st.session_state.user_inputs = {
                    'investable_amount': investable_amount,
                    'risk_profile': risk_profile,
                    'max_yearly_loss': max_yearly_loss,
                    'time_horizon': time_horizon,
                    'currency': currency
                }
                
                # Show loading spinner
                with st.spinner("🤖 Analyzing market conditions and generating your personalized portfolio..."):
                    portfolio_data = get_openai_recommendation(
                        investable_amount,
                        risk_profile,
                        max_yearly_loss,
                        time_horizon,
                        currency
                    )
                    
                    if portfolio_data:
                        st.session_state.portfolio_data = portfolio_data
                        st.session_state.page = 'results'
                        st.success("✅ Portfolio generated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to generate portfolio recommendation. Please try again.")
    
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()


def show_results_page():
    """Display the results page with portfolio recommendations"""
    if not st.session_state.portfolio_data:
        st.warning("No portfolio data available. Please generate a recommendation first.")
        if st.button("Go to Input Page"):
            st.session_state.page = 'input'
            st.rerun()
        return
    
    portfolio_data = st.session_state.portfolio_data
    user_inputs = st.session_state.user_inputs
    
    st.markdown('<div class="main-header">📊 Your Personalized Portfolio</div>', unsafe_allow_html=True)
    
    # Risk indicators
    st.markdown("### 🎯 Portfolio Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Risk Level", portfolio_data.get('risk_level', 'N/A'))
    
    with col2:
        st.metric("Expected Annual Return", f"{portfolio_data.get('expected_annual_return', 0):.2f}%")
    
    with col3:
        st.metric("Max Expected Yearly Loss", f"{portfolio_data.get('max_expected_yearly_loss', 0):.2f}%")
    
    with col4:
        st.metric("Investment Horizon", f"{user_inputs['time_horizon']} years")
    
    # Risk indicator with color coding
    risk_level = portfolio_data.get('risk_level', 'Medium')
    risk_color = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}.get(risk_level, 'gray')
    max_loss = portfolio_data.get('max_expected_yearly_loss', 0)
    
    st.markdown(f"""
    <div style="background-color: {risk_color}; padding: 1rem; border-radius: 10px; color: white; text-align: center; margin: 1rem 0;">
        <h3>Risk Level: {risk_level}</h3>
        <p>Maximum Expected Yearly Loss: {max_loss:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Portfolio Commentary
    st.markdown("### 💡 Portfolio Commentary")
    st.info(portfolio_data.get('portfolio_commentary', 'No commentary available'))
    
    # Portfolio Table
    st.markdown("### 📋 Asset Allocation")
    portfolio_df = pd.DataFrame(portfolio_data['portfolio'])
    
    # Create display dataframe
    display_df = portfolio_df[['asset_name', 'ticker', 'allocation_percentage', 'investment_amount', 'asset_class', 'currency', 'buying_strategy']].copy()
    display_df.columns = ['Asset Name', 'Ticker', 'Allocation %', 'Investment Amount', 'Asset Class', 'Currency', 'Buying Strategy']
    display_df['Allocation %'] = display_df['Allocation %'].apply(lambda x: f"{x:.2f}%")
    display_df['Investment Amount'] = display_df['Investment Amount'].apply(lambda x: f"{user_inputs['currency']} {x:,.2f}")
    
    st.dataframe(display_df,width='stretch' , hide_index=True)
    
    # Show descriptions and links
    with st.expander("📖 Asset Details"):
        for _, asset in portfolio_df.iterrows():
            st.markdown(f"**{asset['asset_name']} ({asset['ticker']})**")
            st.markdown(f"{asset['description']}")
            if 'link' in asset and asset['link']:
                st.markdown(f"[More information]({asset['link']})")
            st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Asset Class Allocation Pie Chart
        st.markdown("### 🥧 Allocation by Asset Class")
        asset_class_data = portfolio_df.groupby('asset_class')['allocation_percentage'].sum().reset_index()
        fig_asset_class = px.pie(
            asset_class_data,
            values='allocation_percentage',
            names='asset_class',
            title='Asset Class Distribution',
            hole=0.4
        )
        fig_asset_class.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_asset_class, width='stretch')
    
    with col2:
        # Currency Allocation Pie Chart
        st.markdown("### 💱 Allocation by Currency")
        currency_data = portfolio_df.groupby('currency')['allocation_percentage'].sum().reset_index()
        fig_currency = px.pie(
            currency_data,
            values='allocation_percentage',
            names='currency',
            title='Currency Distribution',
            hole=0.4
        )
        fig_currency.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_currency, width='stretch')
    
    # Expected Return Projection Chart
    st.markdown("### 📈 Portfolio Value Projection")
    
    years = list(range(user_inputs['time_horizon'] + 1))
    initial_amount = user_inputs['investable_amount']
    expected_return = portfolio_data.get('expected_annual_return', 7.5) / 100
    
    # Calculate projected values
    base_values = [initial_amount * ((1 + expected_return) ** year) for year in years]
    upper_values = [initial_amount * ((1 + expected_return + 0.02) ** year) for year in years]
    lower_values = [initial_amount * ((1 + expected_return - 0.02) ** year) for year in years]
    
    fig_projection = go.Figure()
    
    # Add uncertainty bands
    fig_projection.add_trace(go.Scatter(
        x=years + years[::-1],
        y=upper_values + lower_values[::-1],
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=True,
        name='Uncertainty Range (±2%)'
    ))
    
    # Add expected value line
    fig_projection.add_trace(go.Scatter(
        x=years,
        y=base_values,
        mode='lines+markers',
        name='Expected Value',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig_projection.update_layout(
        title=f'Portfolio Value Projection Over {user_inputs["time_horizon"]} Years',
        xaxis_title='Years',
        yaxis_title=f'Portfolio Value ({user_inputs["currency"]})',
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_projection, width='stretch')
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Generate New Recommendation", type="primary"):
            st.session_state.page = 'input'
            st.session_state.portfolio_data = None
            st.rerun()


# Main app logic
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## Navigation")
        if st.button("🏠 Home", width='stretch'):
            st.session_state.page = 'home'
            st.rerun()
        if st.button("📝 Investment Profile", width='stretch'):
            st.session_state.page = 'input'
            st.rerun()
        if st.button("📊 Results", width='stretch', disabled=st.session_state.portfolio_data is None):
            st.session_state.page = 'results'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This Robo Advisor uses AI to provide personalized ETF portfolio recommendations based on your investment profile.")
    
    # Display appropriate page
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'input':
        show_input_page()
    elif st.session_state.page == 'results':
        show_results_page()


if __name__ == "__main__":
    main()