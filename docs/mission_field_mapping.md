# Mission Field Mapping Documentation

This document describes how fields in the Mission model map to data extracted from DCS mission files by the Lua parser.

## General Information Fields

| Mission Model Field | Lua Parser Field | Description | Format |
|-------------------|------------------|-------------|---------|
| `name` | `mission_name` | The name of the mission | String |
| `description` | `description` | Brief description of the mission objectives | Text |
| `briefing` | `briefing` | Detailed tactical briefing | Text |
| `theatre` | `theatre` | The DCS theatre/map where the mission takes place | String |
| `required_modules` | `required_modules` | List of required DCS modules | String (comma-separated) |
| `roe` | `roe` | Rules of Engagement | String (enum: 'Weapons Hold', 'Weapons Tight', 'Weapons Free') |
| `munitions_restrictions` | `munitions_restrictions` | Restrictions on weapon usage | Text |

## Date and Time Fields

| Mission Model Field | Lua Parser Field | Description | Format |
|-------------------|------------------|-------------|---------|
| `mission_date` | `mission_date` | Real-world mission date (UTC) | Date (YYYY-MM-DD) |
| `mission_time` | `mission_time` | Real-world mission time (UTC) | Time (HH:MM) |
| `sim_date` | `sim_date` | In-game mission date | Date (YYYY-MM-DD) |
| `sim_time` | `sim_time` | In-game mission time | Time (HH:MM) |

## Weather Information Fields

| Mission Model Field | Lua Parser Field | Description | Format |
|-------------------|------------------|-------------|---------|
| `visibility` | `visibility` | Visibility in nautical miles | String |
| `cloud_base` | `cloud_base` | Cloud base altitude in feet | String |
| `wind_at_ground` | `wind_at_ground` | Ground level wind conditions | JSON: `{"speed": float, "direction": float}` |
| `wind_at_2000` | `wind_at_2000` | Wind at 2000m altitude | JSON: `{"speed": float, "direction": float}` |
| `wind_at_8000` | `wind_at_8000` | Wind at 8000m altitude | JSON: `{"speed": float, "direction": float}` |
| `qnh` | `qnh` | QNH pressure setting | String |
| `temperature` | `temperature` | Temperature in Celsius | String |
| `season` | `season` | Current season | String |

## Bulls Eye Information

| Mission Model Field | Lua Parser Field | Description | Format |
|-------------------|------------------|-------------|---------|
| `bullseye` | `bullseye` | Bulls eye coordinates | JSON: `{"lat": float, "long": float}` |

## Notes

1. All JSON fields (`wind_at_ground`, `wind_at_2000`, `wind_at_8000`, `bullseye`) should be initialized as empty dictionaries if no data is available.
2. Time fields should be in 24-hour format (HH:MM).
3. Date fields should be in ISO format (YYYY-MM-DD).
4. Wind direction values should be in degrees (0-360).
5. Wind speed values should be in knots.
6. The `status` field is managed by the application and not extracted from the Lua file.
