# Phase 5: Ghost Car Comparison

## Goal
Add ghost car for lap comparison and performance analysis.

## What's New

### Components
- **GhostCar.jsx** - Semi-transparent cyan ghost car
- **ComparisonHUD.jsx** - Time comparison display

### Features
- ✅ Ghost car (cyan, semi-transparent)
- ✅ Time delta comparison (green = faster, red = slower)
- ✅ Side-by-side lap times
- ✅ Toggle ghost on/off
- ✅ 50-point offset (ghost ahead)
- ✅ Real-time comparison

## Ghost Car

### Visual Design
- Cyan color (#00ffff)
- 30% opacity
- Emissive glow
- Same geometry as player car

### Behavior
- Runs 50 points ahead of player
- Follows same telemetry data
- Always visible when enabled
- Independent of player car

## Comparison HUD

### Display Elements
- **Your Time** - Player's current lap time (white)
- **Ghost Time** - Ghost's lap time (cyan)
- **Delta** - Time difference (green if ahead, red if behind)

### Position
- Top-left corner
- Cyan border
- Semi-transparent background

## Controls

### Ghost Toggle Button
- Click "👻 Show Ghost" to enable
- Click "👻 Hide Ghost" to disable
- Button highlights cyan when active

## Running

Frontend should auto-reload.

If not:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173

## Demo Script

> "Now watch the ghost car - that cyan semi-transparent car ahead. It's running the same lap data but offset by a few seconds. The comparison HUD shows your time versus the ghost. Green delta means you're faster, red means you're slower. This is how professional drivers analyze their performance - comparing against their best lap or a teammate's lap."

## Success Criteria

- [x] Ghost car renders correctly
- [x] Ghost car is semi-transparent
- [x] Time comparison works
- [x] Delta calculation accurate
- [x] Toggle works smoothly
- [x] No performance issues

## Next Steps

Phase 6: Polish, effects, and final touches

## Notes

- Ghost offset is 50 points (about 2.5 seconds)
- Can be adjusted by changing `ghostOffset` prop
- Ghost uses same telemetry as player
- Future: Load different lap data for ghost
