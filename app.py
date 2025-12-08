import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- IMPORTS FROM PACKAGE ---
from src.realestateCH.load import load_rent_data, load_buy_data
from src.realestateCH.metrics import compute_price_to_rent_ratio, rank_cantons_visual

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Swiss Real Estate Dashboard", layout="wide")

# ==========================================
# 1. LOAD DATA
# ==========================================
@st.cache_data
def get_data():
    try:
        df_rent = load_rent_data()
        df_buy = load_buy_data()
        
        # Standardize ZIP column names
        for d in [df_rent, df_buy]:
            if 'postal_code' in d.columns: d.rename(columns={'postal_code': 'zip_code'}, inplace=True)
            if 'zip' in d.columns: d.rename(columns={'zip': 'zip_code'}, inplace=True)
            
        return df_rent, df_buy
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_rent, df_buy = get_data()
if df_rent.empty: st.stop()

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.header("Filter Options")

# Market Choice
market_choice = st.sidebar.radio("Choose Market:", ["Rent", "Buy"])
df = df_rent if market_choice == "Rent" else df_buy
price_label = "Monthly Rent (CHF)" if market_choice == "Rent" else "Purchase Price (CHF)"

# Filters
all_cantons = sorted(df['canton'].astype(str).unique())
selected_cantons = st.sidebar.multiselect("Select Cantons:", all_cantons, default=all_cantons[:3])

st.sidebar.subheader("Rooms")
c1, c2 = st.sidebar.columns(2)
min_rooms = c1.number_input("Min", 1.0, 10.0, 1.0, 0.5)
max_rooms = c2.number_input("Max", 1.0, 100.0, 10.0, 0.5)

st.sidebar.subheader("Price")
c3, c4 = st.sidebar.columns(2)
min_price = c3.number_input("Min Price", 0, 10000000, 0, 100)
max_price = c4.number_input("Max Price", 0, 10000000, 10000, 100)

# ==========================================
# 3. DASHBOARD MAIN VIEW
# ==========================================
# Apply Filters
filtered_df = df.copy()
if selected_cantons: 
    filtered_df = filtered_df[filtered_df['canton'].isin(selected_cantons)]
filtered_df = filtered_df[
    (filtered_df['rooms'] >= min_rooms) & 
    (filtered_df['rooms'] <= max_rooms) &
    (filtered_df['price_chf'] >= min_price) & 
    (filtered_df['price_chf'] <= max_price)
]

st.title(f"🇨🇭 Swiss Real Estate: {market_choice} Market")

# KPIS
c1, c2, c3 = st.columns(3)
c1.metric("Total Listings", f"{len(filtered_df):,}")
c2.metric("Avg Price", f"CHF {filtered_df['price_chf'].mean():,.0f}" if not filtered_df.empty else "0")
c3.metric("Avg Area", f"{filtered_df['area_m2'].mean():,.0f} m²" if not filtered_df.empty and 'area_m2' in filtered_df.columns else "0")

st.divider()

# ==========================================
# 4. RANKING SECTION (Using Package)
# ==========================================
if market_choice == "Rent":
    # We pass the filtered dataframe so the ranking respects the sidebar
    rank_source = filtered_df
    metric_label = "Avg Rent/m²"
    rank_title = "🏆 Top Cantons by Rent: Price per m² (Filtered)"
    rank_info = "Most expensive cantons based on your filters."
else:
    rank_source = filtered_df
    metric_label = "Avg Buy Price/m²"
    rank_title = "🏆 Top Cantons by Buy: Price per m² (Filtered)"
    rank_info = "Most expensive cantons based on your filters."

st.subheader(rank_title)

if not rank_source.empty:
    col_rank_table, col_rank_desc = st.columns([1, 2])
    
    with col_rank_table:
        # CALLING PACKAGE FUNCTION HERE
        ranking_display = rank_cantons_visual(rank_source, metric_name=metric_label)
        
        st.dataframe(
            ranking_display,
            column_config={metric_label: st.column_config.NumberColumn(format="%.2f CHF")},
            hide_index=True,
            height=400,
            use_container_width=True
        )
    
    with col_rank_desc:
        st.info(rank_info)
        # Chart Logic
        if 'area_m2' in rank_source.columns:
            chart_df = rank_source.copy()
            chart_df['metric'] = chart_df['price_chf'] / chart_df['area_m2']
            chart_rank = chart_df.groupby('canton')['metric'].mean().reset_index().sort_values('metric', ascending=False).head(10)
            
            fig_top = go.Figure(go.Bar(
                x=chart_rank['canton'], 
                y=chart_rank['metric'],
                marker_color='gold',
                name=market_choice
            ))
            fig_top.update_layout(title=f"Visual Representation ({market_choice}/m²)", height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_top, use_container_width=True)
else:
    st.warning("No listings match your current filters.")

st.divider()

# ==========================================
# 5. MARKET COMPARISON CHART
# ==========================================
st.subheader("📊 Market Comparison: Rent vs. Buy")

# Filter logic for comparison (Strict on Rooms/Canton, Loose on Price)
m_rent = (df_rent['rooms'] >= min_rooms) & (df_rent['rooms'] <= max_rooms)
m_buy = (df_buy['rooms'] >= min_rooms) & (df_buy['rooms'] <= max_rooms)

if selected_cantons:
    m_rent &= df_rent['canton'].isin(selected_cantons)
    m_buy &= df_buy['canton'].isin(selected_cantons)

# Apply Price filter ONLY to the active market to keep comparison valid
if market_choice == "Rent":
    m_rent &= (df_rent['price_chf'] >= min_price) & (df_rent['price_chf'] <= max_price)
elif market_choice == "Buy":
    m_buy &= (df_buy['price_chf'] >= min_price) & (df_buy['price_chf'] <= max_price)

r_stats = df_rent[m_rent].groupby('canton')['price_chf'].mean().reset_index(name='Avg Rent')
b_stats = df_buy[m_buy].groupby('canton')['price_chf'].mean().reset_index(name='Avg Buy')
merged = pd.merge(r_stats, b_stats, on='canton', how='outer')

if not merged.empty:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=merged['canton'], y=merged['Avg Buy'], name="Buy Price", marker_color='#0068c9', offsetgroup=1), secondary_y=False)
    fig.add_trace(go.Bar(x=merged['canton'], y=merged['Avg Rent'], name="Rent Price", marker_color='#ff4b4b', offsetgroup=2), secondary_y=True)
    fig.update_layout(barmode='group', title="Buy vs Rent Price (Side-by-Side)", height=500, hovermode="x unified")
    fig.update_yaxes(title_text="Purchase Price (CHF)", secondary_y=False)
    fig.update_yaxes(title_text="Monthly Rent (CHF)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data for comparison.")

st.divider()

# ==========================================
# 6. RATIO ANALYSIS (Using Package)
# ==========================================
st.subheader("📈 Investment Analysis: Price-to-Rent Ratio")

if 'zip_code' in df_rent.columns:
    r_agg = df_rent[m_rent].groupby(['zip_code', 'canton'])['price_chf'].mean().reset_index()
    b_agg = df_buy[m_buy].groupby(['zip_code', 'canton'])['price_chf'].mean().reset_index()
    
    # CALLING PACKAGE FUNCTION HERE
    ratio_df = compute_price_to_rent_ratio(b_agg, r_agg)
    
    if not ratio_df.empty:
        rank_df = ratio_df.groupby('canton')['price_to_rent_ratio'].median().reset_index().sort_values('price_to_rent_ratio', ascending=False)
        
        c_left, c_right = st.columns([1, 2])
        with c_left:
            st.markdown("#### Years to Break Even")
            st.dataframe(rank_df.set_index('canton').style.format("{:.1f}"), height=400, use_container_width=True)
        with c_right:
            st.info("""
            **Price-to-Rent Ratio** represents the number of years of rent you would need to pay 
            to equal the purchase price of a similar property.
            
            - **High Ratio (> 25):** It is significantly cheaper to rent than to buy.
            - **Low Ratio (< 15):** Buying might be a better financial decision.
            
            *Note: Calculated based on median prices per zip code.*
            """)
            st.markdown("#### Visual Representation: Years to Break Even")
            fig_r = go.Figure(go.Bar(x=rank_df['canton'], y=rank_df['price_to_rent_ratio'], marker_colorscale='Viridis', marker_color=rank_df['price_to_rent_ratio']))
            fig_r.update_layout(xaxis_title="Canton", yaxis_title="Years")
            st.plotly_chart(fig_r, use_container_width=True)
    else:
        st.warning("Not enough overlapping zip codes to calculate ratios.")
else:
    st.error("Zip code data missing.")