# Phase 4: Real Telemetry from CSV

## Goal
Load actual telemetry data from CSV files instead of simulated data.

## What's New

### Backend
- **parse_telemetry.py** - Extracts telemetry from CSV and syncs with GPS track

### Data Files
- `/frontend/public/telemetry/indianapolis.json` - Real telemetry data
- `/frontend/public/telemetry/barber.json` - Real telemetry data

### Features
- ✅ Real speed data from CSV
- ✅ Real RPM (nmot) from CSV
- ✅ Real gear data from CSV
- ✅ Real steering angle from CSV
- ✅ Synced with GPS track points
- ✅ 501 telemetry points per track

## Data Pipeline

1. **CSV Input** - Raw telemetry from race data
2. **Parser** - Extracts speed, RPM, gear, steering for specific lap
3. **GPS Sync** - Matches telemetry to track GPS points
4. **JSON Output** - Clean telemetry data for frontend

## Telemetry Data Structure

```json
{
  "name": "Track Name",
  "telemetry": [
    {
      "position": [x, y, z],
      "speed": 123.4,
      "rpm": 5678,
      "gear": 4,
      "steeringAngle": -12.3
    }
  ]
}
```

## Running

Frontend should auto-reload with new data.

If not:
```bash
cd frontend
npm run dev
```

## Regenerating Telemetry

```bash
cd backend
python3 parse_telemetry.py
```

## Demo Script

> "Now we're using real telemetry data from the actual races. Watch how the speed, RPM, and gear changes match the real driver inputs. This is the exact data from lap 2 of the race - every acceleration, every braking point, every gear shift."

## Success Criteria

- [x] Real CSV data loaded
- [x] Speed matches actual race data
- [x] RPM matches actual race data
- [x] Gear changes are realistic
- [x] Steering angle reflects track
- [x] Data synced with GPS track

## Next Steps

Phase 5: Add ghost car comparison and advanced features

## Notes

- Using lap 2 data (lap 1 often has formation/start issues)
- Only Indianapolis and Barber have GPS data
- Telemetry is matched 1:1 with track points (501 points each)
- Falls back to simulated data if telemetry file not found
