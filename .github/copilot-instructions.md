# Sun Coral Dashboard - AI Coding Assistant Instructions

## Project Overview
This is a Dash (Python) web application for monitoring and managing sun coral (*Tubastraea spp.*) invasion in REBIO Arvoredo and surrounding areas. The dashboard visualizes field data, management actions, and ecological indicators for researchers and environmental managers.

## Architecture & Component Structure

### Entry Points & Initialization
- **`cs_index.py`**: Main entry point. Defines app layout with Dash Bootstrap theme, creates multi-tab interface (Dashboard + Methods), contains all callbacks for interactivity
- **`app.py`**: Minimal Dash app initialization with CYBORG theme. Import this (`from app import app`) when creating components that need app context (e.g., in `cs_controllers.py`)

### Modular Component Files (imported by cs_index.py)
- **`cs_controllers.py`**: UI controls (date picker, locality dropdown, indicator dropdown). Builds `REBIO_LOCALITIES` and `REBIO_ENTORNO_LOCALITIES` ID lists by mapping locality names to IDs from database
- **`cs_map.py`**: All map visualization functions (`build_map_figure`, `build_dafor_sum_map_figure`, `build_occurrence_map_figure`, etc.). Uses Mapbox token from `keys/mapbox_key`
- **`cs_histogram.py`**: Chart functions (`build_histogram_figure`, `build_locality_bar_figure`, `build_dafor_histogram_figure`, etc.)
- **`cs_tables.py`**: Table rendering components
- **`cs_methods.py`**: Static documentation/methodology layout for the "Métodos e Texto" tab

### Data Layer
- **`services/data_service.py`**: `CoralDataService` class - single source of truth for ALL data access. Every method queries MySQL via SQLAlchemy, returns pandas DataFrames
  - Query pattern: `pd.read_sql(query, db.engine)` where `db.engine` comes from `config/database.py`
  - Key methods: `get_locality_data()`, `get_dafor_data()`, `get_dpue_by_locality()`, `get_occurrences_data()`, `get_management_data()`, `get_days_since_last_management()`
  - Coordinates stored as JSON strings in DB, parsed using `json.loads()` and converted to lat/lon pairs
  - Distance calculations use `geopy.distance.geodesic()`

- **`config/database.py`**: Database connection via SQLAlchemy. Loads credentials from `.env` file. Uses PyMySQL driver with MariaDB/MySQL. Connection pooling enabled with `pool_pre_ping=True`

## Critical Patterns & Conventions

### Database Schema Naming
- Tables: `data_coralsol_locality`, `data_coralsol_dafor`, `data_coralsol_occurrence`, `data_coralsol_management`
- Columns use inconsistent casing (some PascalCase, some lowercase). **Always lowercase column names after reading**: `df.columns = df.columns.str.lower()`
- Date format in DB: dayfirst format (DD/MM/YYYY). Always parse as: `pd.to_datetime(df['date'], dayfirst=True)`

### Coordinate Handling
- Coordinates stored as JSON string arrays in DB: `"[[-27.28, -48.39], [-27.29, -48.40]]"`
- Parse pattern: `coords = json.loads(row['coords_local'])` or `json.loads(row['dafor_coords'])`
- For map plotting, extract first point for marker: `coords[0]` gives `[lat, lon]`
- Line/polygon plotting: use full coordinate list

### Locality Grouping Logic (cs_controllers.py)
- Special values in dropdown: `"rebiogrp"` (REBIO only), `"rebiogrp_entorno"` (REBIO + surrounding), `0` (all localities)
- `filter_localities()` function expands groups to ID lists before filtering DataFrames
- When filtering by `selected_localities`, check for these special values first, expand to IDs, then filter: `df[df['locality_id'].isin(ids)]`

### DAFOR Scale Processing
- DAFOR values stored as comma-separated strings: `"0,2,4,6,10"` representing scale [0=Absent, 2=Rare, 4=Occasional, 6=Frequent, 8=Abundant, 10=Dominant]
- Standard processing pattern in `data_service.py`:
  ```python
  df['dafor_value'] = df['dafor_value'].apply(
      lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
  )
  df = df.explode('dafor_value')
  df['dafor_value'] = pd.to_numeric(df['dafor_value'], errors='coerce')
  ```

### Callback Pattern (cs_index.py)
- All visualizations updated via single callback: `update_visuals()` with 4 inputs (indicator, locality, start/end date)
- Returns 14 outputs: 7 figures + 6 style dicts (show/hide charts) + 1 table
- Each indicator type (`dpue`, `dafor`, `occurrences`, `management`, `days_since_management`, `days_since_monitoring`) determines which charts/maps to show
- Use `style_hide = {'display': 'none'}` and `style_show = {'display': 'block'}` for conditional chart visibility

## Development Workflow

### Running the Application
```powershell
# Install dependencies
pip install -r requirements.txt

# Configure database credentials in .env file (see config/database.py)
# Run app
python cs_index.py
```

### Database Connection Setup
1. Create `.env` file with: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (default 3306), `DB_NAME`
2. Test connection: `python tests/test_connection.py` or `python test_mysql_direct.py`
3. Connection uses PyMySQL driver with SSL disabled for local/trusted networks

### Adding New Visualizations
1. Create visualization function in appropriate module (`cs_map.py` for maps, `cs_histogram.py` for charts)
2. Add data retrieval method to `CoralDataService` in `services/data_service.py` if needed
3. Add new output to `update_visuals()` callback in `cs_index.py`
4. Add corresponding `html.Div` with `dcc.Loading` and `dcc.Graph` in `dashboard_layout`
5. Set visibility logic in callback using style dicts

### Common Debugging Steps
- Check terminal logs - SQLAlchemy `echo=True` prints all queries
- Verify locality IDs: `print(name_to_id)` in `cs_controllers.py` shows mapping
- Filter debugging: `print(f"Filtering with IDs: {ids}")` before DataFrame filter
- Empty figures: Return `go.Figure()` for graceful handling in Dash

## Project-Specific Context
- **Portuguese language**: All UI labels, documentation, and variable names in Portuguese. Keep this convention
- **Ecological monitoring data**: DPUE (Detections Per Unit Effort), IAR-DAFOR (Relative Abundance Index using DAFOR scale)
- **Mapbox integration**: Token hardcoded in `cs_map.py` - consider moving to environment variable for production
- **Bootstrap theme**: Uses `dbc.themes.BOOTSTRAP` in cs_index.py (vs CYBORG in app.py) - consolidate if needed

## External Dependencies
- **Dash/Plotly**: Interactive visualizations and web framework
- **SQLAlchemy + PyMySQL**: Database ORM and MySQL driver
- **Geopy**: Geographic distance calculations
- **Pandas/NumPy**: Data manipulation
- **Dash Bootstrap Components**: UI components and layout
