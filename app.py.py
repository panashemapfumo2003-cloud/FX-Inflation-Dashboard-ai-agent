import streamlit as st
import pandas as pd
from datetime import datetime
import io
import re
from typing import Optional

st.set_page_config(
    page_title="FX & Inflation Dashboard Agent",
    page_icon="📊",
    layout="wide"
)

class FXInflationAgent:
    def __init__(self):
        self.uploaded_data: Optional[pd.DataFrame] = None
        self.data_commentary: str = ""
        
    def parse_uploaded_data(self, text: str) -> pd.DataFrame:
        lines = text.strip().split('\n')
        data_rows = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = re.split(r'[\t,;|]+', line)
            parts = [p.strip() for p in parts if p.strip()]
            
            if len(parts) >= 2:
                try:
                    if '.' in parts[1] or parts[1].replace('.', '').replace('-', '').replace('+', '').isdigit():
                        value = float(parts[1].replace(',', ''))
                        data_rows.append({"Date": parts[0], "Value": value})
                    else:
                        data_rows.append({"Date": parts[0], "Value": parts[1]})
                except ValueError:
                    data_rows.append({"Date": parts[0], "Value": parts[1]})
        
        return pd.DataFrame(data_rows)
    
    def analyze_trends(self, df: pd.DataFrame) -> dict:
        if df.empty or "Value" not in df.columns:
            return {"error": "No valid data to analyze"}
        
        try:
            values = pd.to_numeric(df["Value"], errors='coerce').dropna()
            if values.empty:
                return {"error": "No numeric values found"}
            
            current = values.iloc[-1]
            previous = values.iloc[-2] if len(values) > 1 else current
            change = current - previous
            pct_change = (change / previous * 100) if previous != 0 else 0
            
            return {
                "current": current,
                "previous": previous,
                "change": change,
                "pct_change": pct_change,
                "trend": "up" if change > 0 else "down" if change < 0 else "stable",
                "min": values.min(),
                "max": values.max(),
                "mean": values.mean(),
                "data_points": len(values)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_commentary(self, trends: dict, data_type: str) -> str:
        if "error" in trends:
            return f"Unable to analyze data: {trends['error']}"
        
        trend_desc = "increased" if trends["trend"] == "up" else "decreased" if trends["trend"] == "down" else "remained stable"
        
        commentary = f"""
## 📈 {data_type} Analysis

**Current Level**: {trends['current']:.2f}
**Previous Level**: {trends['previous']:.2f}
**Change**: {trends['change']:+.2f} ({trends['pct_change']:+.2f}%)

### Trend Analysis
The {data_type.lower()} has **{trend_desc}** from {trends['previous']:.2f} to {trends['current']:.2f}.

### Summary Statistics
- **Minimum**: {trends['min']:.2f}
- **Maximum**: {trends['max']:.2f}
- **Average**: {trends['mean']:.2f}
- **Data Points**: {trends['data_points']}

### Interpretation
"""
        if trends["pct_change"] > 5:
            commentary += "Significant movement detected. Consider monitoring for continued volatility."
        elif trends["pct_change"] > 0:
            commentary += "Moderate positive movement. The trend appears cautiously upward."
        elif trends["pct_change"] < -5:
            commentary += "Significant decline observed. Economic factors may be influencing this movement."
        else:
            commentary += "The data shows relative stability with minor fluctuations."
            
        return commentary

agent = FXInflationAgent()

st.title("🌍 FX & Inflation Dashboard Agent")
st.markdown("### AI-Powered Foreign Exchange & Inflation Analysis Tool")

tab1, tab2, tab3 = st.tabs(["📊 Data Upload & Analysis", "💬 Inflation Bot", "💱 Exchange Rate Bot"])

with tab1:
    st.header("Upload Your Data")
    st.markdown("""
    Paste your country's exchange rates or inflation figures below.
    Format: Date/Period followed by value (tab, comma, or space separated)
    
    **Example formats:**
    ```
    2024-01 5.2
    2024-02 5.5
    2024-03 5.1
    ```
    """)
    
    data_input = st.text_area("Paste your data here:", height=200, 
                              placeholder="Date/Period\tValue\n2024-01\t5.2\n2024-02\t5.5...")
    
    col1, col2 = st.columns(2)
    with col1:
        data_type = st.selectbox("Data Type:", ["Inflation Rate", "Exchange Rate", "Interest Rate", "Other"])
    with col2:
        country = st.text_input("Country:", placeholder="e.g., USA, UK, Japan")
    
    if st.button("Analyze Data", type="primary"):
        if data_input.strip():
            try:
                agent.uploaded_data = agent.parse_uploaded_data(data_input)
                if not agent.uploaded_data.empty:
                    trends = agent.analyze_trends(agent.uploaded_data)
                    agent.data_commentary = agent.generate_commentary(trends, data_type)
                    
                    st.success("Data analyzed successfully!")
                    st.markdown(agent.data_commentary)
                    
                    with st.expander("View Raw Data"):
                        st.dataframe(agent.uploaded_data)
                        
                    with st.expander("View Data Chart"):
                        chart_df = agent.uploaded_data.copy()
                        chart_df["Value"] = pd.to_numeric(chart_df["Value"], errors='coerce')
                        st.line_chart(chart_df.set_index("Date")["Value"])
                else:
                    st.error("Could not parse data. Please check the format.")
            except Exception as e:
                st.error(f"Error analyzing data: {str(e)}")
        else:
            st.warning("Please enter some data to analyze.")
    
    if agent.uploaded_data is not None and not agent.uploaded_data.empty:
        st.divider()
        st.header("Ask Questions About Your Data")
        user_question = st.text_input("Ask the AI agent about your uploaded data:", 
                                      placeholder="What advice can you give based on this data?")
        
        if user_question and st.button("Get Answer"):
            answer = f"""
Based on your uploaded {data_type} data for {country or 'the specified region'}:

**Key Insights:**
{agent.data_commentary}

**Answer to your question:**
"{user_question}"

The data shows a {trends.get('trend', 'stable')} pattern with the latest value at {trends.get('current', 'N/A')}. 
{"This suggests monitoring the trend closely for investment decisions." if trends.get('pct_change', 0) > 3 else "The data appears relatively stable."}

**Advice:** {"Consider hedging strategies given the volatility." if abs(trends.get('pct_change', 0)) > 5 else "Continue monitoring regular updates for informed decision-making."}
"""
            st.markdown(answer)

with tab2:
    st.header("💬 Inflation Bot")
    st.markdown("Ask questions about **inflation** - its meaning, causes, effects, and more.")
    
    if "inflation_history" not in st.session_state:
        st.session_state.inflation_history = []
    
    user_q = st.text_input("Ask about inflation:", placeholder="What is inflation?")
    
    if st.button("Ask Inflation Bot", type="primary") and user_q:
        st.session_state.inflation_history.append(("You", user_q))
        
        response = f"""
**Answer to: "{user_q}"**

"""
        
        user_q_lower = user_q.lower()
        
        if "meaning" in user_q_lower or "what is" in user_q_lower:
            response += """
**Inflation** is the rate at which the general level of prices for goods and services rises, causing purchasing power to fall.

In simple terms: Your money buys less than it used to. If inflation is 5%, something that cost $100 last year now costs $105.

**Key Points:**
- Measured by CPI (Consumer Price Index) or PPI (Producer Price Index)
- Central banks typically target 2% annual inflation
- High inflation erodes savings and fixed incomes
- Deflation (negative inflation) can signal economic weakness
"""
        elif "cause" in user_q_lower:
            response += """
**Common Causes of Inflation:**

1. **Demand-Pull Inflation**: Too much money chasing too few goods
2. **Cost-Push Inflation**: Production costs rise, pushing prices up
3. **Built-in Inflation**: Expectations of future inflation cause current spending

**Factors that trigger inflation:**
- Increased government spending
- Expansionary monetary policy
- Supply chain disruptions
- Rising commodity prices (oil, food)
- Currency depreciation
"""
        elif "effect" in user_q_lower or "impact" in user_q_lower:
            response += """
**Effects of Inflation:**

**On Economy:**
- Reduces purchasing power of money
- Encourages spending over saving
- Can lead to higher interest rates
- May cause uncertainty in investment decisions

**On Individuals:**
- Savings lose real value
- Fixed-income earners suffer
- Debtors benefit (real debt decreases)
- Inequality can worsen
"""
        elif "measure" in user_q_lower or "calculate" in user_q_lower:
            response += """
**How Inflation is Measured:**

1. **CPI (Consumer Price Index)**: Tracks price changes of a basket of consumer goods
2. **PPI (Producer Price Index)**: Measures input costs to producers
3. **GDP Deflator**: Ratio of nominal to real GDP
4. **PCE (Personal Consumption Expenditures)**: Fed's preferred measure

**Formula:**
Inflation Rate = ((Current CPI - Previous CPI) / Previous CPI) × 100
"""
        else:
            response += """
**Inflation Insights:**

Inflation is a critical economic indicator that affects monetary policy, interest rates, and investment decisions.

**Types:**
- **Moderate Inflation**: 2-3% - considered healthy
- **High Inflation**: >5% - erodes purchasing power
- **Hyperinflation**: >50% per month - catastrophic
- **Deflation**: Negative inflation - can indicate recession

**Managing Inflation:**
- Diversify investments
- Consider inflation-protected securities (TIPS)
- Invest in assets that historically outpace inflation
"""
        
        st.session_state.inflation_history.append(("Bot", response))
    
    for speaker, msg in st.session_state.inflation_history:
        if speaker == "You":
            st.markdown(f"**👤 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
    
    if st.button("Clear History"):
        st.session_state.inflation_history = []
        st.rerun()

with tab3:
    st.header("💱 Exchange Rate Bot")
    st.markdown("Ask questions about **exchange rates** - their meaning, factors, impacts, and more.")
    
    if "fx_history" not in st.session_state:
        st.session_state.fx_history = []
    
    user_q = st.text_input("Ask about exchange rates:", placeholder="What is an exchange rate?")
    
    if st.button("Ask FX Bot", type="primary") and user_q:
        st.session_state.fx_history.append(("You", user_q))
        
        response = f"""
**Answer to: "{user_q}"**

"""
        
        user_q_lower = user_q.lower()
        
        if "meaning" in user_q_lower or "what is" in user_q_lower:
            response += """
**Exchange Rate** is the price of one country's currency in terms of another country's currency.

**Examples:**
- USD/EUR = 0.92 means 1 US Dollar = 0.92 Euros
- GBP/USD = 1.27 means 1 British Pound = 1.27 US Dollars

**Types:**
- **Fixed Exchange Rate**: Pegged to another currency (e.g., USD)
- **Floating Exchange Rate**: Determined by market forces
- **Managed Float**: Market with central bank intervention
"""
        elif "factor" in user_q_lower or "determine" in user_q_lower:
            response += """
**Factors Affecting Exchange Rates:**

1. **Interest Rate Differentials**: Higher rates attract foreign investment
2. **Inflation Rates**: Lower inflation = stronger currency
3. **Economic Performance**: Strong GDP = stronger currency
4. **Political Stability**: Uncertainty weakens currency
5. **Trade Balance**: Surplus strengthens currency
6. **Central Bank Policy**: Monetary policy impacts value
7. **Market Sentiment**: Risk appetite affects currency flows
"""
        elif "effect" in user_q_lower or "impact" in user_q_lower:
            response += """
**Effects of Exchange Rate Changes:**

**On Imports/Exports:**
- **Currency Depreciation**: Makes exports cheaper, imports more expensive
- **Currency Appreciation**: Makes exports expensive, imports cheaper

**On Economy:**
- Affects inflation (imported inflation)
- Impacts corporate earnings (foreign-denominated debt)
- Influences tourism and investment flows

**On Individuals:**
- Affects purchasing power abroad
- Impacts remittance costs
- Influences foreign investment returns
"""
        elif "trade" in user_q_lower or "tradeable" in user_q_lower:
            response += """
**Exchange Rate in Trade:**

**Favorable Exchange Rate for Exports:**
- When domestic currency is weak, foreign buyers can purchase more with their currency
- Exports become more competitive globally

**Impact on Trade Balance:**
- Weak currency → Exports increase, trade deficit may improve
- Strong currency → Imports cheaper, exports may decline

**Example:**
If USD weakens against JPY, American goods become cheaper for Japanese buyers, potentially increasing US exports to Japan.
"""
        else:
            response += """
**Exchange Rate Insights:**

Exchange rates are crucial in global finance, affecting trade, investment, and monetary policy.

**Key Terms:**
- **Appreciation**: Currency value increases
- **Depreciation**: Currency value decreases
- **Revaluation**: Official increase in fixed rate
- **Devaluation**: Official decrease in fixed rate

**Trading in Forex Market:**
- Largest financial market globally ($6+ trillion daily)
- Operates 24/5 worldwide
- Major pairs: EUR/USD, GBP/USD, USD/JPY
"""
        
        st.session_state.fx_history.append(("Bot", response))
    
    for speaker, msg in st.session_state.fx_history:
        if speaker == "You":
            st.markdown(f"**👤 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
    
    if st.button("Clear FX History"):
        st.session_state.fx_history = []
        st.rerun()

st.divider()
st.caption("🌍 FX & Inflation Dashboard Agent | Powered by AI | Built with Streamlit")