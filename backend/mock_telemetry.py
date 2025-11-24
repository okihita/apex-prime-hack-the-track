import json
import math

# Load Indianapolis as template
with open('../frontend/public/telemetry/indianapolis.json', 'r') as f:
    template = json.load(f)

# Tracks to generate
tracks = ['cota', 'road-america', 'sebring', 'vir', 'sonoma']

for track_name in tracks:
    # Load track points
    with open(f'../frontend/public/tracks/{track_name}.json', 'r') as f:
        track_data = json.load(f)
    
    # Use template structure, update positions if track has points
    telemetry = []
    for i, entry in enumerate(template):
        new_entry = entry.copy()
        
        # If track has points, use them
        if track_data.get('points') and len(track_data['points']) > 0:
            idx = int(i / len(template) * len(track_data['points'])) % len(track_data['points'])
            new_entry['position'] = track_data['points'][idx]
        
        telemetry.append(new_entry)
    
    # Save
    with open(f'../frontend/public/telemetry/{track_name}.json', 'w') as f:
        json.dump(telemetry, f)
    
    print(f"✅ {track_name}")

print("✅ All mock telemetry generated")
