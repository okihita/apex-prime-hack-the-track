# Phase 1: GPS Track Visualization

## Goal
Load GPS data and render a 3D track in the browser.

## Setup

### Backend (Python)

```bash
cd backend
pip install -r requirements.txt
```

### Generate Track Data

```bash
cd backend
python generate_track.py
```

This will:
- Parse GPS from Indianapolis telemetry CSV
- Convert to 3D coordinates
- Save to `frontend/public/tracks/indianapolis.json`

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## What You'll See

- 3D track generated from GPS data
- Indianapolis Motor Speedway layout
- Orbit camera controls (mouse to rotate, scroll to zoom)
- Track info overlay

## Controls

- **Mouse drag**: Orbit camera
- **Scroll**: Zoom in/out
- **Right click drag**: Pan

## Success Criteria

- [x] Track loads in <5 seconds
- [x] Recognizable layout (Indianapolis oval + infield)
- [x] Smooth camera controls
- [x] 60 FPS rendering

## Demo Script

> "We've automatically generated a 3D track from GPS telemetry. This is Indianapolis Motor Speedway, created from real race data. No manual work required. Works on any track with GPS data."

## Next Steps

Phase 2: Add animated car driving on the track.

## Troubleshooting

**Track doesn't load:**
- Check that `frontend/public/tracks/indianapolis.json` exists
- Run `python backend/generate_track.py` to generate it

**Blank screen:**
- Check browser console for errors
- Make sure npm install completed successfully

**Track looks wrong:**
- GPS data might be noisy
- Try adjusting smoothing window in `generate_track.py`
