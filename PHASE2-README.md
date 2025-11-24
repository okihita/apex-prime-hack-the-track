# Phase 2: Car Animation

## Goal
Animate a 3D car driving on the track using telemetry data.

## What's New

### Components
- **Car.jsx** - 3D car with animated wheels and steering
- **ChaseCamera.jsx** - Camera that follows the car
- **useTelemetry.js** - Hook to manage telemetry playback

### Features
- ✅ Red GR86-style car (simple box geometry)
- ✅ Wheels rotate based on speed
- ✅ Front wheels steer based on steering angle
- ✅ Car follows track path
- ✅ Chase camera mode
- ✅ Play/Pause controls
- ✅ Camera mode toggle (Orbit/Chase)

## Running

Frontend should still be running from Phase 1.

If not:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173

## Controls

### Playback
- **Play/Pause button** - Control animation
- **Camera button** - Toggle between Orbit and Chase cam

### Orbit Mode
- **Mouse drag** - Rotate camera
- **Scroll** - Zoom
- **Right click** - Pan

### Chase Mode
- Camera automatically follows car
- Smooth tracking with lerp

## Demo Script

> "Now watch the car drive the lap. This red GR86 is following the track path. The wheels rotate based on speed, and the front wheels steer. You can switch to chase camera to follow the car, or use orbit mode to view from any angle. The animation runs at 60 FPS with smooth interpolation."

## Success Criteria

- [x] Car moves smoothly (60 FPS)
- [x] Position follows track path
- [x] Steering looks realistic
- [x] Camera follows car naturally
- [x] Play/pause works
- [x] Camera modes work

## Next Steps

Phase 3: Add HUD with telemetry display (speed, RPM, gear, lap time)

## Notes

- Car is currently a simple box - will be replaced with proper 3D model later
- Telemetry is simulated for demo - will load from CSV in later phases
- Rotation calculation is simplified - will use proper heading from GPS in Phase 5
