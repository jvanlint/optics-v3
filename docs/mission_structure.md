# DCS Mission File Structure

This document outlines the hierarchical structure of DCS World mission files (.miz), specifically focusing on how aircraft groups, units, and waypoints are organized.

## Flow of Execution

The process of uploading and displaying mission information follows these steps:

1. **File Upload**
   - User uploads a .miz file through the web interface
   - The file is received by the `upload_mission` view in `mission_parser/views.py`
   - The file is validated to ensure it's a .miz file

2. **File Processing**
   - The `MissionFileHandler` class extracts the mission.lua file from the .miz archive
   - The handler also extracts the localization dictionary (l10n/DEFAULT/dictionary) if present
   - The raw Lua content and localization dictionary are passed to the `MissionLuaParser`

3. **Lua Parsing**
   - The `MissionLuaParser` uses the `slpp` library to parse the Lua content into a Python dictionary
   - The parser extracts key mission information:
     - Mission description and objectives
     - Weather conditions
     - Date and time settings
     - Air units and their configurations
     - Bullseye reference point

4. **Text Localization**
   - The `TextLocalizer` class processes all text content:
     - Handles localization keys (e.g., "DictKey_123")
     - Processes newlines and formatting
     - Special handling for task descriptions (searches for keywords like "neutralise" or "objective")
   - Text processing includes:
     - Converting `\\\n` to actual newlines
     - Cleaning up whitespace and line breaks
     - Maintaining proper paragraph spacing

5. **Data Organization**
   - The parsed data is organized into a structured format:

     ```python
     {
         'weather': {...},
         'air_units': {...},
         'client_planes': {...},
         'date': {...},
         'formatted_date': 'DD/MM/YYYY',
         'formatted_time': 'HH:MM',
         'theatre': '...',
         'description': '...',
         'sortie': '...',
         'blue_task': '...',
         'bullseye_info': {...}
     }
     ```

6. **Template Rendering**
   - The organized data is passed to the template
   - The template displays the information in a structured format
   - Timezone filters are applied to convert UTC times to local time
   - Coordinate transformations are applied for bullseye and unit positions

7. **Display**
   - The final rendered page shows:
     - Mission description and objectives
     - Weather conditions with converted units
     - Date and time in local timezone
     - Air units with their configurations
     - Bullseye reference point with coordinates

## Basic Structure

```
mission
├── descriptionText          # Mission description (localized)
├── sortie                   # Mission sortie name (localized)
├── theatre                  # Map/terrain name
├── start_time              # Mission start time in seconds
├── date                    # Mission date information
│   ├── Year
│   ├── Month
│   └── Day
│
├── weather                 # Weather conditions
│   ├── clouds
│   │   └── base           # Cloud base height in meters
│   ├── season
│   │   └── temperature
│   ├── visibility
│   │   └── distance
│   ├── wind               # Wind conditions at different altitudes
│   │   ├── at8000
│   │   │   ├── speed     # Wind speed in m/s
│   │   │   └── dir       # Wind direction
│   │   ├── at2000
│   │   │   ├── speed
│   │   │   └── dir
│   │   └── atGround
│   │       ├── speed
│   │       └── dir
│   └── qnh                # Atmospheric pressure in mmHg
│
├── map                    # Map view settings
│   ├── centerX           # Center X coordinate
│   ├── centerY           # Center Y coordinate
│   └── zoom              # Map zoom level
│
└── coalition             # Coalition forces
    └── blue             # Blue coalition (friendly forces)
        ├── bullseye     # Reference point
        │   ├── x        # X coordinate
        │   └── y        # Y coordinate
        │
        └── country[x]   # Countries in coalition
            ├── name     # Country name
            │
            ├── plane    # Fixed-wing aircraft
            │   └── group[y]
            │       ├── name
            │       ├── frequency    # Group radio frequency
            │       ├── x, y         # Group position
            │       ├── units[z]     # Individual aircraft
            │       │   ├── name
            │       │   ├── type     # Aircraft type (F-16C, etc)
            │       │   ├── skill    # AI skill or "Client" for player
            │       │   ├── parking  # Parking spot number
            │       │   ├── heading  # Direction in radians
            │       │   ├── alt      # Altitude in meters
            │       │   ├── speed    # Speed in m/s
            │       │   ├── payload
            │       │   │   ├── fuel  # Fuel in kg
            │       │   │   ├── chaff
            │       │   │   ├── flare
            │       │   │   └── gun
            │       │   ├── callsign
            │       │   └── Radio    # Radio presets
            │       │       └── [radio_id]
            │       │           ├── channels     # Frequency presets
            │       │           └── modulations  # AM/FM settings
            │       │
            │       └── route
            │           └── points[i]
            │               ├── name
            │               ├── alt     # Altitude in meters
            │               ├── speed   # Speed in m/s
            │               ├── type    # Point type (takeoff, land, etc)
            │               ├── action  # Action at waypoint
            │               └── task    # Tasks at waypoint
            │                   ├── id   # Task identifier
            │                   └── params
            │                       └── tasks[]  # Subtasks
            │                           ├── id
            │                           └── params
            │                               └── action
            │                                   ├── id
            │                                   └── params
            │
            └── helicopter  # Rotary-wing aircraft
                └── group[y]
                    # Same structure as plane groups
```

## Structure Explanation

### Map Section

- Contains information about the mission map view
- `centerX` and `centerY`: Center point of the map view in meters
- `zoom`: Current zoom level of the map view
- These coordinates use the same Cartesian system as other coordinates in the mission

### Bullseye

- The bullseye is a reference point specific to each coalition
- Located under the coalition structure (blue/red)
- Coordinates are in meters relative to the map origin (0,0)
- Uses a Cartesian coordinate system:
  - x: East/West position in meters
  - y: North/South position in meters
- Note: These are NOT latitude/longitude coordinates

## Coordinate Conversion

DCS maps use a Cartesian coordinate system where:

- Origin (0,0) is specific to each map
- X increases eastward (in meters)
- Y increases northward (in meters)

### Using pyproj for Coordinate Transformation

DCS uses a Transverse Mercator projection for its coordinate system. We use pyproj to handle the conversion between DCS coordinates and latitude/longitude. Each map has specific projection parameters:

```python
# Example projection string for Persian Gulf map
proj_str = (
    "+proj=tmerc "           # Transverse Mercator projection
    "+lat_0=0 "             # Latitude of origin
    "+lon_0=57 "            # Central meridian
    "+k_0=0.9996 "          # Scale factor
    "+x_0=75000 "           # False easting
    "+y_0=0 "               # False northing
    "+towgs84=0,0,0,0,0,0,0 " # WGS84 datum transformation
    "+units=m "             # Units in meters
    "+vunits=m "            # Vertical units in meters
    "+ellps=WGS84 "         # WGS84 ellipsoid
    "+no_defs "             # Don't use defaults
    "+axis=neu"             # North/East/Up axis orientation
)

# Create transformer
transformer = Transformer.from_proj(
    Proj(proj_str),         # Source projection (DCS)
    Proj('epsg:4326'),      # Target projection (WGS84 lat/lon)
    always_xy=True          # Use x,y order for coordinates
)

# Convert coordinates (note: x and y are swapped in DCS)
lon, lat = transformer.transform(y, x)  # y,x order due to DCS convention
```

### Map Projection Parameters

Each DCS map has specific projection parameters stored in a JSON configuration:

```json
{
  "PersianGulf": {
    "central_meridian": 57,
    "scale_factor": 0.9996,
    "false_easting": 75000,
    "false_northing": 0
  }
}
```

The mission's `map` section can help verify coordinate conversions:

1. The `centerX` and `centerY` values provide a known reference point
2. These coordinates correspond to the center of the map view
3. Can be used with the map's origin point to verify coordinate calculations

Common DCS Map References:

- Persian Gulf: Origin = N26°10'16" E56°14'32" (verified from point N26°10'08" E56°14'21" at x:-306.45507484033, y:-253.39956020314)
  - Projection Parameters:
    - Central Meridian: 57°E
    - Scale Factor: 0.9996
    - False Easting: 75000m
    - False Northing: 0m
- Syria: Origin ≈ N32.8° E35.0°
  - Projection Parameters:
    - Central Meridian: 36°E
    - Scale Factor: 0.9996
    - False Easting: -400000m
    - False Northing: 0m
- Caucasus: Origin ≈ N43.2° E39.7°
  - Projection Parameters:
    - Central Meridian: 33°E
    - Scale Factor: 0.9996
    - False Easting: 500000m
    - False Northing: 0m

Note: The Persian Gulf parameters have been verified with actual mission data. Other map parameters are approximate and should be verified with known points.

### Group Level

- Each group represents a formation of aircraft
- Groups have their own radio frequency
- Groups contain individual units and a route plan

### Unit Level

- Units represent individual aircraft within a group
- Each unit has:
  - Type (aircraft model)
  - Speed
  - Name
  - Callsign
  - Heading (in radians, where 0 is north)

    ```python
    # Convert heading from radians to degrees
    heading_degrees = math.degrees(heading_radians)
    # Example: 1.4412992439976 radians ≈ 82.6 degrees
    ```

    - 0 radians = 0° (North)
    - π/2 radians ≈ 1.5708 = 90° (East)
    - π radians ≈ 3.1416 = 180° (South)
    - 3π/2 radians ≈ 4.7124 = 270° (West)

### Route and Waypoints

- Routes are composed of ordered points (waypoints)
- Each waypoint (point) has:
  - Name
  - Altitude
  - Action
  - Speed
  - Type
  - Tasks to perform

## Access Pattern

- Countries are accessed via index: `country[x]`
- Groups within countries: `group[y]`
- Units within groups: `units[z]`
- Waypoints in route: `points[i]`
- Tasks at waypoints: `task[j]`

This structure allows for complex mission planning with multiple aircraft groups, each following their own route with specific tasks at designated waypoints.
