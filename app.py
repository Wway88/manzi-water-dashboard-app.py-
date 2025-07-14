# manzi-water-dashboard-app.py-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Manzi Water Intelligence Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Manzi Water branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1E88E5 0%, #43A047 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1E88E5;
    }
    .critical-alert {
        background: #FFE5E5;
        border-left: 4px solid #E53935;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-metric {
        background: #E8F5E8;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-metric {
        background: #FFF3CD;
        border-left: 4px solid #FB8C00;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate comprehensive sample data
@st.cache_data
def generate_sample_data():
    # Date range
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='M')
    
    # Water Security Data
    np.random.seed(42)  # For reproducible results
    water_security = pd.DataFrame({
        'Date': dates,
        'Reservoir_Capacity_%': np.random.uniform(55, 80, len(dates)) * (1 - np.linspace(0, 0.2, len(dates))),
        'Drought_Status': np.random.choice(['GREEN', 'YELLOW', 'RED'], len(dates), p=[0.3, 0.4, 0.3]),
        'Pump_Downtime_Hours': np.random.uniform(8, 60, len(dates)) * (1 + np.linspace(0, 0.5, len(dates))),
        'Pipe_Leakage_Rate_%': np.random.uniform(14, 24, len(dates)) * (1 + np.linspace(0, 0.3, len(dates))),
        'Water_Loss_Ml_Monthly': np.random.uniform(110, 170, len(dates)) * (1 + np.linspace(0, 0.4, len(dates))),
        'Borehole_Active_Count': np.random.uniform(20, 45, len(dates)),
        'Quality_Tests_Passed_%': np.random.uniform(88, 99, len(dates))
    })
    
    # Financial Performance Data
    financial_data = pd.DataFrame({
        'Date': dates,
        'Billing_Amount_R': np.random.uniform(8000000, 13000000, len(dates)) * (1 + np.linspace(0, 0.5, len(dates))),
        'Revenue_Collected_R': lambda x: x * np.random.uniform(0.75, 0.92, len(dates)),
        'Energy_Costs_R': np.random.uniform(1100000, 2700000, len(dates)) * (1 + np.linspace(0, 1.2, len(dates))),
        'Load_Shedding_Hours': np.random.uniform(10, 160, len(dates)) * (1 + np.linspace(0, 2, len(dates))),
        'Infrastructure_ROI_%': np.random.uniform(7, 14, len(dates)) * (1 - np.linspace(0, 0.4, len(dates))),
        'OpEx_R': np.random.uniform(4000000, 6700000, len(dates)) * (1 + np.linspace(0, 0.6, len(dates))),
        'CapEx_R': np.random.uniform(1800000, 3500000, len(dates))
    })
    
    # Fix Revenue_Collected_R calculation
    financial_data['Revenue_Collected_R'] = financial_data['Billing_Amount_R'] * np.random.uniform(0.75, 0.92, len(dates))
    financial_data['Collection_Rate_%'] = (financial_data['Revenue_Collected_R'] / financial_data['Billing_Amount_R']) * 100
    
    # Customer Impact Data
    customer_impact = pd.DataFrame({
        'Date': dates,
        'Service_Interruptions_Count': np.random.uniform(15, 80, len(dates)) * (1 + np.linspace(0, 1.5, len(dates))),
        'Avg_Downtime_Hours': np.random.uniform(3, 11, len(dates)) * (1 + np.linspace(0, 1.2, len(dates))),
        'SANS241_Compliance_%': np.random.uniform(88, 99, len(dates)) * (1 - np.linspace(0, 0.08, len(dates))),
        'CSAT_Score': np.random.uniform(5.5, 8.5, len(dates)) * (1 - np.linspace(0, 0.25, len(dates))),
        'Complaints_Count': np.random.uniform(35, 130, len(dates)) * (1 + np.linspace(0, 1.8, len(dates))),
        'Zone_Most_Affected': np.random.choice(['Soweto_North', 'Alexandra_Central', 'Tembisa_East', 'Diepsloot'], len(dates)),
        'Population_Served': np.random.uniform(2400000, 2650000, len(dates))
    })
    
    # Forecasting Data
    forecast_years = list(range(2025, 2031))
    forecasting_data = pd.DataFrame({
        'Year': forecast_years,
        'Demand_Projection_Ml': [2850, 3020, 3180, 3350, 3520, 3700],
        'AI_Leakage_Prediction_%': [19.8, 21.2, 22.1, 22.8, 23.2, 23.5],
        'Climate_Risk_Score': [7.2, 7.8, 8.1, 8.4, 8.7, 9.0],
        'Investment_Required_R': [45000000, 52000000, 48000000, 55000000, 62000000, 68000000],
        'Population_Growth_%': [2.8, 2.9, 3.0, 3.1, 3.2, 3.3]
    })
    
    # IoT Telemetry Data
    iot_data = pd.DataFrame({
        'Station_ID': [f'MNZ{i:03d}' for i in range(1, 101)],
        'Location': np.random.choice(['Soweto_North', 'Alexandra_Central', 'Tembisa_East', 'Diepsloot', 'Midrand', 'Sandton'], 100),
        'Status': np.random.choice(['ONLINE', 'MAINTENANCE', 'CRITICAL'], 100, p=[0.75, 0.15, 0.10]),
        'Flow_Rate_L_min': np.random.uniform(0, 550, 100),
        'Pressure_kPa': np.random.uniform(0, 280, 100),
        'Temperature_C': np.random.uniform(15, 25, 100),
        'pH_Level': np.random.uniform(6.5, 8.0, 100),
        'Chlorine_mg_L': np.random.uniform(0.2, 1.2, 100)
    })
    
    return water_security, financial_data, customer_impact, forecasting_data, iot_data

# Load data
water_security, financial_data, customer_impact, forecasting_data, iot_data = generate_sample_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 Manzi Water Intelligence Dashboard</h1>
    <p>Executive Command Center - Real-time Water Utility Management</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔧 Dashboard Controls")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
    min_value=datetime(2022, 1, 1),
    max_value=datetime(2024, 12, 31)
)

zone_filter = st.sidebar.multiselect(
    "Select Zones",
    options=['Soweto_North', 'Alexandra_Central', 'Tembisa_East', 'Diepsloot', 'Midrand', 'Sandton'],
    default=['Soweto_North', 'Alexandra_Central', 'Tembisa_East', 'Diepsloot']
)

# Main Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏢 Executive Overview", "⚙️ Operations", "💰 Financial", "🔮 2030 Vision"])

with tab1:
    st.header("Executive Overview Dashboard")
    
    # Get latest data for KPIs
    latest_water = water_security.iloc[-1]
    latest_financial = financial_data.iloc[-1]
    latest_customer = customer_impact.iloc[-1]
    
    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        water_loss = latest_water['Water_Loss_Ml_Monthly']
        st.markdown(f"""
        <div class="kpi-card">
            <h3 style="color: #E53935;">💧 Water Loss</h3>
            <h1 style="color: #E53935;">{water_loss:.0f} Ml/month</h1>
            <p>↗️ 24% increase YoY</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        revenue_loss = (latest_financial['Billing_Amount_R'] - latest_financial['Revenue_Collected_R']) / 1000000
        st.markdown(f"""
        <div class="kpi-card">
            <h3 style="color: #E53935;">💸 Revenue Loss</h3>
            <h1 style="color: #E53935;">R{revenue_loss:.1f}M</h1>
            <p>↗️ Collection rate: {latest_financial['Collection_Rate_%']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        efficiency = (100 - latest_water['Pipe_Leakage_Rate_%'])
        st.markdown(f"""
        <div class="kpi-card">
            <h3 style="color: #FB8C00;">⚡ System Efficiency</h3>
            <h1 style="color: #FB8C00;">{efficiency:.1f}%</h1>
            <p>↘️ Below 85% target</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        csat = latest_customer['CSAT_Score']
        st.markdown(f"""
        <div class="kpi-card">
            <h3 style="color: #E53935;">😊 Customer Satisfaction</h3>
            <h1 style="color: #E53935;">{csat:.1f}/10</h1>
            <p>↘️ 18% decline YoY</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Critical Alerts
    st.markdown("""
    <div class="critical-alert">
        <h4>🚨 Critical Alerts</h4>
        <p><strong>Alexandra Central:</strong> 23 Ml/month leakage = R400K monthly loss</p>
        <p><strong>Load Shedding Impact:</strong> Energy costs up 95% vs 2022</p>
        <p><strong>SANS 241 Compliance:</strong> 3 zones below 95% threshold</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Leakage Hotspot Analysis")
        
        # Simulate zone-level leakage data
        zone_leakage = pd.DataFrame({
            'Zone': ['Alexandra_Central', 'Soweto_North', 'Tembisa_East', 'Diepsloot', 'Midrand', 'Sandton'],
            'Leakage_Ml': [23, 18, 12, 15, 8, 5],
            'Monthly_Loss_R': [400000, 320000, 210000, 260000, 140000, 90000],
            'Lat': [-26.1, -26.2, -25.9, -25.9, -25.9, -26.1],
            'Lon': [28.1, 27.9, 28.2, 28.0, 28.1, 28.0]
        })
        
        # Create bubble map
        fig = px.scatter_mapbox(
            zone_leakage, 
            lat="Lat", 
            lon="Lon", 
            size="Leakage_Ml",
            color="Monthly_Loss_R",
            hover_name="Zone",
            hover_data={"Leakage_Ml": True, "Monthly_Loss_R": ":,.0f"},
            color_continuous_scale="Reds",
            size_max=50,
            zoom=10
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=-26.0, lon=28.0)),
            height=400,
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Water Loss vs Infrastructure Investment")
        
        # Prepare data for trend analysis
        trend_data = water_security.merge(financial_data, on='Date')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=trend_data['Date'], 
                y=trend_data['Water_Loss_Ml_Monthly'],
                name="Water Loss (Ml/month)",
                line=dict(color='#E53935', width=3)
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Bar(
                x=trend_data['Date'], 
                y=trend_data['CapEx_R']/1000000,
                name="CapEx Investment (R M)",
                opacity=0.6,
                marker_color='#1E88E5'
            ),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Water Loss (Ml/month)", secondary_y=False)
        fig.update_yaxes(title_text="Investment (R Millions)", secondary_y=True)
        
        fig.update_layout(
            title="Investment vs Water Loss Correlation",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick Win Calculator
    st.subheader("💡 Quick Win Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leaks_to_fix = st.slider("Number of key leaks to fix", 1, 20, 10)
        
    with col2:
        avg_leak_size = st.slider("Average leak size (Ml/month)", 1.0, 5.0, 2.3)
        
    with col3:
        cost_per_ml = st.slider("Cost per Ml (R)", 10000, 25000, 17500)
    
    monthly_savings = leaks_to_fix * avg_leak_size * cost_per_ml
    annual_savings = monthly_savings * 12
    
    st.markdown(f"""
    <div class="success-metric">
        <h4>💰 Projected Savings</h4>
        <p><strong>Monthly Savings:</strong> R{monthly_savings:,.0f}</p>
        <p><strong>Annual Savings:</strong> R{annual_savings:,.0f}</p>
        <p><strong>ROI Timeline:</strong> 14 months payback period</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("⚙️ Operational Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚦 SANS 241 Compliance Dashboard")
        
        # Compliance metrics
        compliance_metrics = pd.DataFrame({
            'Parameter': ['pH Levels', 'Turbidity', 'E.coli', 'Free Chlorine', 'Total Coliform'],
            'Current_Value': [7.2, 2.8, 15, 0.8, 8],
            'SANS_241_Limit': [7.0, 1.0, 0, 0.5, 5],
            'Status': ['GREEN', 'YELLOW', 'RED', 'GREEN', 'YELLOW']
        })
        
        # Traffic light display
        for _, row in compliance_metrics.iterrows():
            if row['Status'] == 'GREEN':
                st.success(f"✅ {row['Parameter']}: {row['Current_Value']} (Compliant)")
            elif row['Status'] == 'YELLOW':
                st.warning(f"⚠️ {row['Parameter']}: {row['Current_Value']} (Attention needed)")
            else:
                st.error(f"❌ {row['Parameter']}: {row['Current_Value']} (Non-compliant)")
    
    with col2:
        st.subheader("🔧 Pump Station Status")
        
        # IoT status summary
        online_count = len(iot_data[iot_data['Status'] == 'ONLINE'])
        maintenance_count = len(iot_data[iot_data['Status'] == 'MAINTENANCE'])
        critical_count = len(iot_data[iot_data['Status'] == 'CRITICAL'])
        
        st.metric("🟢 Online Stations", online_count)
        st.metric("🟡 Maintenance Required", maintenance_count)
        st.metric("🔴 Critical Failures", critical_count)
        
        # Status distribution chart
        status_counts = iot_data['Status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color_discrete_map={
                'ONLINE': '#4CAF50',
                'MAINTENANCE': '#FB8C00',
                'CRITICAL': '#E53935'
            }
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Service Interruptions Heatmap
    st.subheader("🗺️ Service Interruption Analysis")
    
    # Create heatmap data
    interruption_data = customer_impact.groupby(['Zone_Most_Affected']).agg({
        'Service_Interruptions_Count': 'sum',
        'Avg_Downtime_Hours': 'mean'
    }).reset_index()
    
    fig = px.bar(
        interruption_data,
        x='Zone_Most_Affected',
        y='Service_Interruptions_Count',
        color='Avg_Downtime_Hours',
        title='Service Interruptions by Zone',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Real-time IoT Data Table
    st.subheader("📊 Real-time IoT Telemetry")
    
    # Filter critical stations
    critical_stations = iot_data[iot_data['Status'] == 'CRITICAL'].head(10)
    
    st.dataframe(
        critical_stations[['Station_ID', 'Location', 'Status', 'Flow_Rate_L_min', 'Pressure_kPa', 'pH_Level']],
        use_container_width=True
    )

with tab3:
    st.header("💰 Financial Performance")
    
    # Financial KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_collection = latest_financial['Collection_Rate_%']
        st.metric(
            "💳 Revenue Collection Rate",
            f"{current_collection:.1f}%",
            f"{current_collection - 90:.1f}% vs 2022"
        )
    
    with col2:
        current_energy = latest_financial['Energy_Costs_R'] / 1000000
        st.metric(
            "⚡ Energy Costs",
            f"R{current_energy:.1f}M",
            "95% increase vs 2022"
        )
    
    with col3:
        current_roi = latest_financial['Infrastructure_ROI_%']
        st.metric(
            "📈 Infrastructure ROI",
            f"{current_roi:.1f}%",
            f"{current_roi - 12.5:.1f}% vs 2022"
        )
    
    # Financial trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue Collection Trends")
        
        fig = px.line(
            financial_data,
            x='Date',
            y='Collection_Rate_%',
            title='Revenue Collection Rate Over Time',
            color_discrete_sequence=['#1E88E5']
        )
        
        fig.add_hline(y=85, line_dash="dash", line_color="red", annotation_text="Target: 85%")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Energy Cost vs Load Shedding")
        
        fig = px.scatter(
            financial_data,
            x='Load_Shedding_Hours',
            y='Energy_Costs_R',
            size='Energy_Costs_R',
            color='Date',
            title='Energy Costs vs Load Shedding Impact'
        )
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Project Pipeline
    st.subheader("🚧 Project Pipeline Tracker")
    
    project_data = pd.DataFrame({
        'Project_Type': ['Borehole Projects', 'Purification Plants', 'Pipe Replacement', 'IoT Upgrades'],
        'Completed': [5, 2, 23, 12],
        'In_Progress': [12, 3, 45, 28],
        'Planned': [8, 2, 67, 35],
        'Budget_R': [45000000, 125000000, 89000000, 34000000]
    })
    
    # Stacked bar chart for project progress
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name='Completed', x=project_data['Project_Type'], y=project_data['Completed'], marker_color='#4CAF50'))
    fig.add_trace(go.Bar(name='In Progress', x=project_data['Project_Type'], y=project_data['In_Progress'], marker_color='#FB8C00'))
    fig.add_trace(go.Bar(name='Planned', x=project_data['Project_Type'], y=project_data['Planned'], marker_color='#E53935'))
    
    fig.update_layout(barmode='stack', height=400, title='Project Pipeline Status')
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("🔮 2030 Vision & Scenario Planning")
    
    # Scenario simulator
    st.subheader("🎮 Interactive Scenario Simulator")
    
    climate_severity = st.slider(
        "Climate Change Severity (1-10)",
        min_value=1,
        max_value=10,
        value=7,
        help="Adjust climate impact severity for 2030 projections"
    )
    
    investment_level = st.selectbox(
        "Investment Level",
        ["Minimal (R30M)", "Moderate (R50M)", "Aggressive (R80M)"],
        index=1
    )
    
    # Calculate scenario outcomes
    base_demand = 3700
    climate_multiplier = 1 + (climate_severity - 5) * 0.05
    adjusted_demand = base_demand * climate_multiplier
    
    investment_impact = {
        "Minimal (R30M)": 0.8,
        "Moderate (R50M)": 0.6,
        "Aggressive (R80M)": 0.3
    }
    
    failure_probability = 25 * investment_impact[investment_level] * (climate_severity / 10)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📊 2030 Demand Projection",
            f"{adjusted_demand:.0f} Ml",
            f"{(adjusted_demand - 3700):.0f} Ml climate adjustment"
        )
    
    with col2:
        st.metric(
            "⚠️ System Failure Risk",
            f"{failure_probability:.1f}%",
            "Without intervention: 25%"
        )
    
    with col3:
        required_investment = 68000000 * climate_multiplier
        st.metric(
            "💰 Investment Required",
            f"R{required_investment/1000000:.0f}M",
            f"R{(required_investment - 68000000)/1000000:.0f}M climate premium"
        )
    
    # Forecasting charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Demand Growth Projections")
        
        # Adjust forecasting data based on scenario
   
