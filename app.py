import streamlit as st
import pandas as pd
import numpy as np

# Set page config for a premium layout
st.set_page_config(
    page_title="EcoFootprint | Carbon Calculator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS
st.markdown("""
<style>
    /* Custom fonts and headers */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant gradient background for the headers */
    .header-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(56, 239, 125, 0.2);
    }
    
    .header-box h1 {
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    
    .header-box p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.95;
    }

    /* Style metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #11998e;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        color: #555;
    }

    /* Styled sections */
    .card {
        background-color: #f9fbf9;
        border: 1px solid #e0ede0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    }

    .card-title {
        color: #1b4d3e;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Specific badge styling */
    .badge {
        background-color: #e2f9ec;
        color: #1b7a43;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-alert {
        background-color: #ffebe9;
        color: #d73a49;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA & EMISSION FACTORS -----------------
# Emission factors represent kg CO2e per km traveled.
# Sources: DEFRA (UK Department for Environment, Food & Rural Affairs) / EPA averages.
EMISSION_FACTORS = {
    "Petrol Car (Medium)": 0.170,
    "Diesel Car (Medium)": 0.165,
    "Hybrid Car (Medium)": 0.110,
    "Electric Vehicle (EV)": 0.048,
    "Motorbike (Medium)": 0.113,
    "Bus (Average passenger)": 0.096,
    "Train (National Rail passenger)": 0.035,
    "Short-haul Flight (<3 hrs, passenger)": 0.245,
    "Long-haul Flight (>3 hrs, passenger)": 0.193,
    "Bicycle / Walking": 0.000
}

# Descriptions & icons for modes
TRANSPORT_DETAILS = {
    "Petrol Car (Medium)": {"icon": "🚗", "desc": "Standard fossil-fuel internal combustion engine car."},
    "Diesel Car (Medium)": {"icon": "🚙", "desc": "Slightly more efficient than petrol but emits high particulates."},
    "Hybrid Car (Medium)": {"icon": "🚘", "desc": "Combines engine and battery, lower city emissions."},
    "Electric Vehicle (EV)": {"icon": "⚡", "desc": "Zero tailpipe emissions; lifecycle depends on electrical grid mix."},
    "Motorbike (Medium)": {"icon": "🏍️", "desc": "Efficient for solo travel but emits more per passenger than bus/train."},
    "Bus (Average passenger)": {"icon": "🚌", "desc": "Highly efficient shared transport; emissions shared among passengers."},
    "Train (National Rail passenger)": {"icon": "🚆", "desc": "One of the greenest ways to travel long distances."},
    "Short-haul Flight (<3 hrs, passenger)": {"icon": "✈️", "desc": "High emissions due to take-off energy and radiative forcing at altitude."},
    "Long-haul Flight (>3 hrs, passenger)": {"icon": "🛫", "desc": "High altitude emissions; slightly lower per km than short flights."},
    "Bicycle / Walking": {"icon": "🚲", "desc": "Active travel. 100% emission-free and healthy!"}
}

# ----------------- HELPER FUNCTIONS -----------------
def convert_distance(distance: float, input_unit: str) -> float:
    """Converts input distance to standard Kilometers."""
    if input_unit == "Miles":
        return distance * 1.60934
    return distance

def calculate_emissions(distance_km: float, mode: str) -> float:
    """Calculates emissions in kg CO2e."""
    factor = EMISSION_FACTORS.get(mode, 0.0)
    return distance_km * factor

def generate_tips(mode: str, distance_km: float) -> list:
    """Generates eco-friendly reduction tips based on travel choices."""
    tips = []
    
    if mode in ["Petrol Car (Medium)", "Diesel Car (Medium)", "Hybrid Car (Medium)"]:
        if distance_km < 8:
            tips.append("🚲 **Active Travel**: For trips under 8 km, consider walking or riding a bicycle. It is healthy and produces zero emissions.")
        tips.append("🚌 **Public Transit**: Taking a bus or train instead of driving alone can cut emissions by up to 50-80%.")
        tips.append("👥 **Carpooling**: Share rides with colleagues or friends to split the vehicle's emissions among occupants.")
        tips.append("⚡ **Go Electric**: Switching to an Electric Vehicle (EV) can reduce emissions by up to 70% depending on your energy grid.")
        
    elif mode == "Electric Vehicle (EV)":
        tips.append("☀️ **Green Charging**: Try charging your EV during off-peak hours or using solar energy to maximize carbon savings.")
        tips.append("🛣️ **Eco-Driving**: Smooth acceleration, moderate speeds, and regenerative braking extend battery range and efficiency.")
        
    elif mode in ["Short-haul Flight (<3 hrs, passenger)", "Long-haul Flight (>3 hrs, passenger)"]:
        tips.append("🚆 **Train Alternative**: For land-based trips (especially under 1000 km), high-speed rail generates up to 85% less carbon than flying.")
        tips.append("✈️ **Direct Flights**: Take direct flights where possible. Takeoffs and landings consume the most fuel and generate the highest emissions.")
        tips.append("🌳 **Offsetting**: If you must fly, consider investing in certified gold standard carbon offsetting schemes.")
        
    elif mode == "Bus (Average passenger)" or mode == "Train (National Rail passenger)":
        tips.append("🙌 **Eco-Champion**: You're already using low-carbon shared transit! Keep it up!")
        tips.append("🚲 **First/Last Mile**: Use active travel (walking/biking) to get to and from the transit stations.")
        
    elif mode == "Bicycle / Walking":
        tips.append("🏅 **Hero Level**: Zero emissions! You are leading by example. Encourage others to join you in active commuting!")
        
    return tips

# ----------------- SESSION STATE -----------------
if "trips" not in st.session_state:
    st.session_state.trips = []

# ----------------- HEADER -----------------
st.markdown("""
<div class="header-box">
    <h1>🌍 EcoFootprint</h1>
    <p>Estimate travel emissions, visualize your environmental impact, and discover actionable paths to carbon reduction.</p>
</div>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
   # st.image("https://icons8.com/icon/81357/eco", width=250)
    #st.image("https://img.icons8.com/illustrations/external-flaticons-lineal-color-flat-icons/256/external-carbon-footprint-climate-change-flaticons-lineal-color-flat-icons.png", width=120)
    st.header("⚙️ Global Settings")
    
    unit = st.radio("Select Distance Unit", ["Kilometers", "Miles"], index=0)
    
    st.markdown("---")
    st.subheader("📊 Carbon Benchmarks")
    st.info("""
    **Global Annual Target**: ~2,000 kg (2 tonnes) CO2e per person to align with the Paris Agreement 1.5°C goal.
    
    *Current averages:*
    - US Citizen: ~14,500 kg / year
    - UK Citizen: ~5,200 kg / year
    - Global Avg: ~4,700 kg / year
    """)
    
    if st.button("🗑️ Reset All Trip Logs"):
        st.session_state.trips = []
        st.success("All trip logs cleared!")
        st.rerun()

# ----------------- TABS -----------------
tab1, tab2, tab3 = st.tabs(["📝 Log a Journey", "📊 Carbon Dashboard", "💡 Reduction Tips"])

# ----- TAB 1: LOG A JOURNEY -----
with tab1:
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        st.subheader("📥 Add a Travel Leg")
        
        with st.form("trip_form", clear_on_submit=True):
            trip_name = st.text_input("Trip Label / Description", placeholder="e.g., Daily Commute, Flight to Paris, Weekend Getaway")
            
            selected_mode = st.selectbox(
                "Select Transportation Mode",
                list(EMISSION_FACTORS.keys()),
                format_func=lambda x: f"{TRANSPORT_DETAILS[x]['icon']} {x}"
            )
            
            distance_val = st.number_input(
                f"Distance Traveled ({unit})",
                min_value=0.0,
                step=1.0,
                format="%.2f",
                help="Enter the one-way or round-trip distance"
            )
            
            submit_button = st.form_submit_button("➕ Log Journey Leg")
            
            if submit_button:
                # Validation checks
                if not trip_name.strip():
                    st.error("⚠️ Please enter a label/description for this trip.")
                elif distance_val <= 0.0:
                    st.error("⚠️ Distance must be greater than zero.")
                else:
                    # Convert to KM internally for calculations
                    distance_km = convert_distance(distance_val, unit)
                    emissions = calculate_emissions(distance_km, selected_mode)
                    
                    new_trip = {
                        "id": len(st.session_state.trips) + 1,
                        "name": trip_name.strip(),
                        "mode": selected_mode,
                        "distance_entered": distance_val,
                        "distance_km": distance_km,
                        "unit": unit,
                        "emissions_kg": round(emissions, 2)
                    }
                    st.session_state.trips.append(new_trip)
                    st.success(f"Trip leg '{trip_name}' logged successfully!")
                    st.rerun()
                    
    with col_info:
        st.subheader("ℹ️ Selected Mode Info")
        details = TRANSPORT_DETAILS[selected_mode]
        factor = EMISSION_FACTORS[selected_mode]
        
        st.markdown(f"### {details['icon']} {selected_mode}")
        st.markdown(f"*{details['desc']}*")
        
        # Display emission factor badge
        if factor == 0:
            st.markdown('<span class="badge">🌿 Zero Emissions</span>', unsafe_allow_html=True)
        elif factor < 0.08:
            st.markdown(f'<span class="badge">🟢 Low Emissions: {factor:.3f} kg CO2e/km</span>', unsafe_allow_html=True)
        elif factor < 0.15:
            st.markdown(f'<span class="badge">🟡 Moderate Emissions: {factor:.3f} kg CO2e/km</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="badge-alert">🔴 High Emissions: {factor:.3f} kg CO2e/km</span>', unsafe_allow_html=True)
            
        st.write("Calculations are based on average passenger occupancy where relevant.")

    st.markdown("---")
    st.subheader("📋 Current Trip Log")
    
    if len(st.session_state.trips) > 0:
        # Construct DataFrame for nice representation
        df = pd.DataFrame(st.session_state.trips)
        df_display = df[["id", "name", "mode", "distance_entered", "unit", "emissions_kg"]].copy()
        df_display.columns = ["ID", "Trip Label", "Transport Mode", f"Distance ({unit})", "Unit", "Emissions (kg CO2e)"]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Option to delete a leg
        col_del1, col_del2 = st.columns([1, 4])
        with col_del1:
            delete_id = st.number_input("Delete Trip ID", min_value=1, max_value=len(st.session_state.trips), step=1)
            if st.button("🗑️ Delete Leg"):
                # Filter out the selected trip and re-index
                st.session_state.trips = [t for t in st.session_state.trips if t["id"] != delete_id]
                # Re-assign IDs
                for idx, t in enumerate(st.session_state.trips):
                    t["id"] = idx + 1
                st.success(f"Trip ID {delete_id} deleted.")
                st.rerun()
    else:
        st.info("No trips logged yet. Use the form above to log your travel details.")

# ----- TAB 2: CARBON DASHBOARD -----
with tab2:
    if len(st.session_state.trips) == 0:
        st.info("Add travel legs in the 'Log a Journey' tab to view your dashboard analysis.")
    else:
        # Calculations
        df = pd.DataFrame(st.session_state.trips)
        total_emissions_kg = df["emissions_kg"].sum()
        total_dist_km = df["distance_km"].sum()
        
        # Equivalent stats
        # 1. Trees needed to offset in 1 year (1 mature tree absorbs ~22kg CO2/year)
        trees_offset = total_emissions_kg / 22.0
        # 2. Comparison to daily target (Target: ~5.5 kg/day to hit 2 tonnes/year)
        paris_daily_target = 5.48 # kg
        carbon_pct_of_target = (total_emissions_kg / paris_daily_target) * 100
        
        # Dashboard Grid Layout
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Emissions", f"{total_emissions_kg:,.2f} kg CO2e", help="Cumulative CO2 equivalent emissions from all logged travel.")
        with col_m2:
            st.metric("Trees Required", f"{trees_offset:.1f} Trees", help="Number of mature trees needed to absorb this amount of CO2 in one year.")
        with col_m3:
            st.metric("Daily Targets Logged", f"{total_emissions_kg / paris_daily_target:.1f} days", help="Equivalent to how many days of the sustainable carbon budget this travel uses up.")
            
        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📊 Emissions by Journey Leg")
            # Create a simple bar chart
            chart_df = df[["name", "emissions_kg"]].copy()
            chart_df = chart_df.rename(columns={"name": "Journey Leg", "emissions_kg": "Emissions (kg CO₂e)"})
            st.bar_chart(chart_df.set_index("Journey Leg"))
            
        with col_chart2:
            st.subheader("📊 Emissions by Transport Category")
            # Group by transport mode
            cat_df = df.groupby("mode")["emissions_kg"].sum().reset_index()
            cat_df.columns = ["Transport Mode", "Emissions (kg CO₂e)"]
            
            # Simple bar chart for categories
            st.bar_chart(cat_df.set_index("Transport Mode"), color="#11998e")
            
        st.markdown("---")
        st.subheader("💡 Environmental Context")
        
        # Construct some interactive benchmark comparison metrics
        avg_us_daily = 39.7 # kg CO2e
        avg_uk_daily = 14.2 # kg CO2e
        
        if total_emissions_kg > 0:
            st.markdown(f"""
            Here is how your logged emissions of **{total_emissions_kg:.2f} kg CO2e** compare to daily averages around the world:
            *   It is equivalent to **{(total_emissions_kg / avg_us_daily):.1f} times** the average US citizen's daily carbon footprint (~40 kg).
            *   It is equivalent to **{(total_emissions_kg / avg_uk_daily):.1f} times** the average UK citizen's daily carbon footprint (~14 kg).
            *   A typical passenger vehicle emits about **{total_emissions_kg / 0.17:.1f} km** worth of driving.
            """)

# ----- TAB 3: REDUCTION TIPS -----
with tab3:
    st.subheader("🌱 Personalized Reduction Strategies")
    
    if len(st.session_state.trips) == 0:
        st.info("Log your journeys to receive personalized tips based on your transport choices.")
        
        # General starter tips
        st.markdown("""
        ### General Tips for Low-Carbon Living:
        1. **Avoid unnecessary trips**: Batch errands together or substitute travel with virtual meetings where possible.
        2. **Choose active travel**: Walking, running, or cycling produce zero carbon emissions and improve cardiovascular health.
        3. **Embrace public transit**: Commuting by train or bus is significantly better for the environment than driving alone.
        4. **Adopt eco-driving habits**: Keep your tires inflated, reduce excess weight in the trunk, and drive smoothly to conserve fuel.
        5. **Transition to electricity**: If you own a vehicle, look into hybrid or battery-electric models for your next purchase.
        """)
    else:
        # Gather unique modes logged
        df = pd.DataFrame(st.session_state.trips)
        unique_modes = df["mode"].unique()
        
        has_tips = False
        for mode in unique_modes:
            mode_df = df[df["mode"] == mode]
            mode_distance = mode_df["distance_km"].sum()
            tips = generate_tips(mode, mode_distance)
            
            if tips:
                has_tips = True
                icon = TRANSPORT_DETAILS[mode]["icon"]
                st.markdown(f"### {icon} Tips for {mode} users")
                for tip in tips:
                    st.write(tip)
                st.markdown("")
                
        if not has_tips:
            st.write("You are doing great! All your logged journeys have zero emissions.")
