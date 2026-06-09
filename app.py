import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as px
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgriSmart: AI-Driven Drone & Resource Optimizer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM THEMING / CSS ---
# Injecting custom CSS to lean into the Emerald, Mint, and Amber palette
st.markdown("""
    <style>
        /* Main background and text colors */
        .stApp {
            background-color: #f8f9fa;
        }
        /* Custom sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #114232;
        }
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p {
            color: #f7fdfa !important;
        }
        /* Metric Card styling overrides */
        div[data-testid="stMetricValue"] {
            color: #114232;
            font-weight: bold;
        }
        /* Success box custom tint */
        .stSuccess {
            background-color: #f0fdf4;
            border-left-color: #15803d;
        }
        /* Primary button custom color */
        div.stButton > button:first-child {
            background-color: #114232;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #87A922;
            color: white;
        }
    </style>
""", unsafe_unsafe_html=True)


# --- UTILITY & SIMULATION FUNCTIONS ---
def calculate_drone_metrics(crop, area, infestation):
    """Calculates drone mission parameters based on parameters."""
    # Base coefficients
    base_time_per_acre = 8  # minutes
    base_fluid_per_acre = 15 # Liters
    
    multiplier = {"Low": 1.0, "Medium": 1.4, "Severe": 2.0}.get(infestation, 1.0)
    
    total_time = area * base_time_per_acre * (1 + (multiplier * 0.1))
    total_fluid = area * base_fluid_per_acre * multiplier
    
    # 1 battery lasts approx 25 minutes
    batteries_required = max(1, int(np.ceil(total_time / 25)))
    
    # Altitude changes based on crop type canopy structure
    altitude = {"Wheat": 3.5, "Cotton": 4.0, "Rice": 3.0, "Maize": 5.0, "Sugarcane": 5.5}.get(crop, 4.0)
    speed = 6.5 if infestation == "Severe" else 8.0 # slower speed for deep coverage
    
    return {
        "flight_time": round(total_time, 1),
        "batteries": batteries_required,
        "fluid_volume": round(total_fluid, 1),
        "altitude": altitude,
        "speed": speed
    }

def get_npk_recommendations(crop):
    """Returns dynamic N-P-K ratios based on standard agronomic data."""
    ratios = {
        "Wheat": {"N": "120 kg/ha", "P": "60 kg/ha", "K": "40 kg/ha"},
        "Cotton": {"N": "150 kg/ha", "P": "60 kg/ha", "K": "60 kg/ha"},
        "Rice": {"N": "100 kg/ha", "P": "40 kg/ha", "K": "40 kg/ha"},
        "Maize": {"N": "180 kg/ha", "P": "80 kg/ha", "K": "60 kg/ha"},
        "Sugarcane": {"N": "250 kg/ha", "P": "75 kg/ha", "K": "100 kg/ha"}
    }
    return ratios.get(crop, {"N": "N/A", "P": "N/A", "K": "N/A"})


# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='text-align: center; color: #87A922;'>🌿 AgriSmart AI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 0.9rem; margin-top:-15px;'>Precision ICT Framework</p>", unsafe_allow_html=True)
st.sidebar.write("---")

page = st.sidebar.radio(
    "Navigate System Tasks:",
    [
        "📈 Dashboard (Overview)",
        "🛸 Drone Spraying Optimizer",
        "💧 Smart Irrigation & Resource Calculator",
        "🩺 Crop Health & AI Advisory",
        "📊 Market & Weather Insights"
    ]
)

st.sidebar.write("---")
st.sidebar.caption("⚡ Connected to Drone Fleet Node-04")
st.sidebar.caption("🛰️ Satellite Feed Sync: Active")


# ==============================================================================
# 1. DASHBOARD (OVERVIEW)
# ==============================================================================
if page == "📈 Dashboard (Overview)":
    # Banner
    st.markdown(
        """
        <div style="background-color: #114232; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-left: 8px solid #87A922;">
            <h1 style="color: white; margin: 0; font-size: 2.2rem;">Empowering Agriculture Through Precision ICT</h1>
            <p style="color: #F7fdfa; margin: 5px 0 0 0; opacity: 0.9;">Real-time farm resource distribution analytics, drone operations telemetry, and localized diagnostic tracking.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Area Managed", value="150 Acres", delta="🛡️ Active Sync")
    with col2:
        st.metric(label="Drone Fleet Status", value="88% Battery", delta="🔋 Ready for Takeoff", delta_color="normal")
    with col3:
        st.metric(label="Water Saved This Month", value="24%", delta="⬆️ 3.2% vs Last Month")
    with col4:
        st.metric(label="Next Scheduled Spray", value="04:00 PM Today", delta="🛸 Sector 3-B")
        
    st.write("---")
    
    # Central Dynamic Map Component / Plotly Chart
    st.subsection = st.markdown("### 🗺️ Sector Health & Biomass Density Mapping")
    
    # Create fake spatial grid for farm data representation
    np.random.seed(42)
    grid_size = 10
    x, y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
    # Generate mock NDVI (Normalized Difference Vegetation Index) values
    ndvi_values = np.random.uniform(0.2, 0.9, size=(grid_size, grid_size))
    
    fig = px.Figure(data=px.Heatmap(
        z=ndvi_values,
        x=[f"Grid X-{i}" for i in range(grid_size)],
        y=[f"Grid Y-{i}" for i in range(grid_size)],
        colorscale=[[0, "#e3f2fd"], [0.4, "#87A922"], [1, "#114232"]],
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Field NDVI Remote Sensing Overlay (Live Resolution Grid)",
        xaxis_title="Field Longitude Sectors",
        yaxis_title="Field Latitude Sectors",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# 2. DRONE SPRAYING OPTIMIZER
# ==============================================================================
elif page == "🛸 Drone Spraying Optimizer":
    st.markdown("## 🛸 Automated Drone Spraying & Flight Optimizer")
    st.markdown("Calculate flight missions, flight paths, and optimal fluid application metrics to limit agrochemical waste.")
    st.write("---")
    
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 📋 Mission Input Profiles")
        crop_type = st.selectbox("Target Crop Profile:", ["Wheat", "Cotton", "Rice", "Maize", "Sugarcane"])
        field_area = st.number_input("Field Surface Coverage Area (Acres):", min_value=1.0, max_value=500.0, value=25.0, step=0.5)
        infestation_level = st.selectbox("Current Pathogen/Pest Infestation Profile:", ["Low", "Medium", "Severe"])
        
        st.write("")
        calculate_btn = st.button("⚡ Calculate Drone Mission Parameters")
        
    with col_output:
        st.markdown("### 📊 Optimized Mission Dispatch Analytics")
        
        if calculate_btn:
            # Run simulation calculations
            metrics = calculate_drone_metrics(crop_type, field_area, infestation_level)
            
            # Display outputs dynamically
            o_col1, o_col2 = st.columns(2)
            with o_col1:
                st.metric("Est. Total Flight Duration", f"{metrics['flight_time']} Mins")
                st.metric("Payload Payload Volume Required", f"{metrics['fluid_volume']} Liters")
            with o_col2:
                st.metric("Battery Cycles Required", f"{metrics['batteries']} Packs")
                st.metric("Target Flight Altitude / Speed", f"{metrics['altitude']}m @ {metrics['speed']} m/s")
            
            st.write("---")
            st.success(f"""
                **🛸 Autonomous Pathing Summary Compiled Successfully:** Recommended system configurations match payload profiles for **{crop_type}** structural canopies. 
                Drone will cruise at an altitude of **{metrics['altitude']} meters** with variable multi-spectral terrain tracing enabled to match a context-driven payload output of **{metrics['fluid_volume']}L**.
            """)
        else:
            st.info("Adjust inputs on the left pane and select the computation trigger button to query localized flight paths.")


# ==============================================================================
# 3. SMART IRRIGATION & RESOURCE CALCULATOR
# ==============================================================================
elif page == "💧 Smart Irrigation & Resource Calculator":
    st.markdown("## 💧 Smart Irrigation Analytics & Soil NPK Matrix Tracker")
    st.markdown("Dynamically adjust hydro-sensors and cross-reference optimal crop mineral absorption indexes.")
    st.write("---")
    
    col_sliders, col_charts = st.columns([1, 1.2])
    
    with col_sliders:
        st.markdown("### 🌡️ Real-time Telemetry Feeds")
        target_crop_res = st.selectbox("Select Target Crop Variant:", ["Wheat", "Cotton", "Rice", "Maize", "Sugarcane"], key="irrigation_crop")
        soil_moisture = st.slider("Current Soil Moisture Content (%)", min_value=0, max_value=100, value=38)
        air_temp = st.slider("Ambient Surface Temperature (°C)", min_value=10, max_value=50, value=32)
        
        # Immediate reactive computation logic
        base_water_need = max(0, (65 - soil_moisture) * 120) if soil_moisture < 65 else 0
        if air_temp > 35:
            base_water_need *= 1.15 # Add heat mitigation offset volume
            
        st.write("---")
        st.markdown("### 🧪 Recommended Substrate Composition (NPK)")
        npk = get_npk_recommendations(target_crop_res)
        
        npk_col1, npk_col2, npk_col3 = st.columns(3)
        npk_col1.metric("Nitrogen (N)", npk["N"])
        npk_col2.metric("Phosphorus (P)", npk["P"])
        npk_col3.metric("Potassium (K)", npk["K"])

    with col_charts:
        st.markdown("### 📊 Resource Deficit Mapping Metrics")
        st.metric("Computed Volumetric Hydro Demand", f"{round(base_water_need, 1)} Liters / Acre")
        
        # Soil health Plotly gauge rendering
        fig_gauge = px.Indicator(
            mode = "gauge+number",
            value = soil_moisture,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Current Soil Volumetric Water Content vs Critical Level (65%)", 'font': {'size': 15}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#114232"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#ffcdd2'},
                    {'range': [30, 65], 'color': '#fff9c4'},
                    {'range': [65, 100], 'color': '#c8e6c9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 65
                }
            }
        )
        fig_gauge.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)


# ==============================================================================
# 4. CROP HEALTH & AI ADVISORY
# ==============================================================================
elif page == "🩺 Crop Health & AI Advisory":
    st.markdown("## 🩺 Computer Vision (CV) Plant Pathology Diagnostics")
    st.markdown("Upload structural images of field plant leaf tissue samples to run immediate semantic segmentation and diagnostic evaluations.")
    st.write("---")
    
    file_upload = st.file_uploader("Upload Target Leaf Profile Specimen (Supported formats: PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    
    if file_upload is not None:
        st.write("")
        # Layout splitting for uploaded image file validation and analysis layout representation
        col_img, col_diag = st.columns([1, 1.2])
        
        with col_img:
            st.image(file_upload, caption="Uploaded Specimen Context Feed", use_container_width=True)
            
        with col_diag:
            st.markdown("### ⚙️ Executing AI Pathology Neural Net Sequence...")
            # Simulate a real deep learning processing timeframe pipeline
            with st.spinner("Parsing image contours, texture distributions, and color variations..."):
                time.sleep(2.0)
                
            st.markdown("#### 🔬 Diagnostic Record Output Summary")
            
            # Mock diagnosis variables
            identified_issue = "Early Blight Fungus Vector (Alternaria solani)"
            confidence_index = 94.6
            
            st.warning(f"**Detected Vector Condition:** {identified_issue}")
            st.metric("Neural Architecture Confidence Metric", f"{confidence_index}%")
            
            st.markdown("##### 🛡️ Targeted Treatment Remediation Steps via Drone Dispatch")
            st.markdown("""
            * **Step 1:** Isolate affected zone layout vector grids via variable rate application (VRA) software presets.
            * **Step 2:** Configure multi-rotor payload configuration arrays with **Fungicide Variant Formula B-4**.
            * **Step 3:** Deploy low-altitude precision hover operations (3.0 meters) at 4.5 m/s down-wash turbulence to target leaf undersides.
            """)
    else:
        st.info("System awaiting sensory file stream input. Upload structural crop tissue imagery to initialize standard edge-node diagnostic loops.")


# ==============================================================================
# 5. MARKET & WEATHER INSIGHTS
# ==============================================================================
elif page == "📊 Market & Weather Insights":
    st.markdown("## 📊 Environmental Forecasts & Commodity Market Indexes")
    st.markdown("Cross-reference current atmospheric conditions against logistical crop commodity indices.")
    st.write("---")
    
    col_wx, col_mkt = st.columns([1, 1])
    
    with col_wx:
        st.markdown("### 🌤️ Drone Logistics Weather Grid (3-Day Horizon)")
        
        # Synthetic weather dataframe construction
        wx_data = pd.DataFrame({
            "Day Profile": ["Today (Current)", "Tomorrow", "Day 3 Prediction"],
            "Temp (°C)": [32, 34, 29],
            "Wind Speed (km/h)": [14, 28, 11],
            "Precipitation (%)": [10, 65, 15],
            "Drone Operations Flight Permission": ["🟢 Safe to Launch", "🔴 High Wind/Rain Danger", "🟢 Safe to Launch"]
        })
        st.table(wx_data)
        
        # Wind warning trigger alert parameter check
        current_wind_speed = 14 
        tomorrow_wind_speed = 28
        st.error(f"⚠️ **Flight Alert Level High:** Ground telemetry tracking indicates wind speeds will escalate to **{tomorrow_wind_speed} km/h** tomorrow. Discontinue automated low-payload multi-rotor drone paths to avoid roll destabilization risk factors.")
        
    with col_mkt:
        st.markdown("### 📈 Major Crop Commodity Pricing Dashboard")
        
        # Synthetic pricing tracking matrix template
        market_data = pd.DataFrame({
            "Crop Core Variant": ["Premium Wheat Grade-A", "Fine Basmati Rice", "Long-Staple Cotton Fiber", "Yellow Feed Maize", "Raw Crushed Sugarcane"],
            "Current Rate (Per Maund / 40kg)": ["PKR 4,200", "PKR 11,500", "PKR 8,800", "PKR 2,900", "PKR 480"],
            "Daily Percentage Variance": ["▲ +0.4%", "▼ -1.2%", "▲ +2.1%", "── 0.0%", "▲ +0.8%"],
            "Market Volume Index": ["High", "Medium", "High", "Low", "Critical"]
        })
        
        st.dataframe(market_data, use_container_width=True, hide_index=True)
        st.caption("🔄 Exchange indicators update concurrently with major agricultural distribution hubs every 15 minutes.")
