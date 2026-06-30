# Carbon Footprint Estimator

The Carbon Footprint Estimator is a Streamlit-based web application designed to help individuals calculate, analyze, and offset their travel-related carbon emissions. By logging different legs of a journey, users can visualize their cumulative carbon impact and receive tailored suggestions to reduce their footprint.

## Features

- **Multi-Leg Journey Logger**: Add multiple segments of travel to keep track of a cumulative trip or daily commute.
- **Support for Diverse Transportation Modes**: Calculated using realistic emission factors (kg CO2e per km) for petrol, diesel, hybrid, electric vehicles, motorbikes, buses, trains, and flights.
- **Unit Conversion**: Select between kilometers and miles as the default distance unit.
- **Dynamic Carbon Dashboard**: Displays total emissions, comparison to global daily and annual carbon benchmarks, and equivalent tree-absorption offset requirements.
- **Customized Carbon Reduction Tips**: Generates actionable, context-aware suggestions based on logged transportation choices.

## Emission Calculation Methodology

Calculations are based on average passenger emission factors (kg CO2e/km) derived from international environment agency databases (DEFRA/EPA):

- Petrol Car (Medium): 0.170 kg/km
- Diesel Car (Medium): 0.165 kg/km
- Hybrid Car (Medium): 0.110 kg/km
- Electric Vehicle (EV): 0.048 kg/km
- Motorbike: 0.113 kg/km
- Bus (Average Passenger): 0.096 kg/km
- Train (National Rail Passenger): 0.035 kg/km
- Short-haul Flight (< 3 Hours): 0.245 kg/km
- Long-haul Flight (> 3 Hours): 0.193 kg/km
- Bicycle / Walking: 0.000 kg/km

## Installation and Setup

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install streamlit pandas numpy
```

### Running the Application

To run the Streamlit application locally, execute the following command in the project directory:

```bash
streamlit run app.py
```

By default, the application will be accessible in your web browser at `http://localhost:8501`.

## File Structure

- `app.py`: Main application code, containing calculations, layout structure, and design elements.
- `README.md`: Documentation for the project.
"# Carbon-Footprint-Estimator" 
