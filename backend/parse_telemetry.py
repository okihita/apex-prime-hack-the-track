"""
Parse telemetry data from CSV and sync with GPS track
"""
import pandas as pd
import json
import numpy as np

def parse_telemetry_data(csv_path, lap_number=2):
    """Extract telemetry for a specific lap"""
    print(f"  Reading telemetry for lap {lap_number}...")
    
    chunks = []
    for chunk in pd.read_csv(csv_path, chunksize=100000):
        lap_chunk = chunk[chunk['lap'] == lap_number]
        if not lap_chunk.empty:
            chunks.append(lap_chunk)
    
    if not chunks:
        print(f"  No telemetry found for lap {lap_number}")
        return []
    
    df = pd.concat(chunks, ignore_index=True)
    
    # Pivot telemetry data
    telemetry = {}
    for name in ['speed', 'nmot', 'gear', 'Steering_Angle', 'VBOX_Lat_Min', 'VBOX_Long_Minutes']:
        data = df[df['telemetry_name'] == name][['timestamp', 'telemetry_value']]
        if not data.empty:
            telemetry[name] = dict(zip(data['timestamp'], data['telemetry_value']))
    
    # Get all timestamps
    timestamps = sorted(set(df['timestamp']))
    
    # Build telemetry array
    result = []
    for i, ts in enumerate(timestamps):
        point = {
            'index': i,
            'speed': telemetry.get('speed', {}).get(ts, 0),
            'rpm': telemetry.get('nmot', {}).get(ts, 0),
            'gear': int(telemetry.get('gear', {}).get(ts, 1)),
            'steering': telemetry.get('Steering_Angle', {}).get(ts, 0),
            'lat': telemetry.get('VBOX_Lat_Min', {}).get(ts),
            'lon': telemetry.get('VBOX_Long_Minutes', {}).get(ts)
        }
        if point['lat'] and point['lon']:
            result.append(point)
    
    print(f"  Found {len(result)} telemetry points")
    return result

def generate_telemetry_json(csv_path, track_json_path, output_path, track_name):
    """Generate telemetry JSON synced with track"""
    print(f"Generating telemetry: {track_name}")
    
    # Load track
    with open(track_json_path, 'r') as f:
        track_data = json.load(f)
    
    # Parse telemetry
    telemetry = parse_telemetry_data(csv_path)
    
    if not telemetry:
        print("  No telemetry data found")
        return
    
    # Match telemetry to track points
    track_points = track_data['points']
    matched = []
    
    for i, track_point in enumerate(track_points):
        if i < len(telemetry):
            t = telemetry[i]
            matched.append({
                'position': track_point,
                'speed': float(t['speed']),
                'rpm': float(t['rpm']),
                'gear': int(t['gear']),
                'steeringAngle': float(t['steering'])
            })
    
    # Save
    output = {
        'name': track_name,
        'telemetry': matched
    }
    
    print(f"  Saving to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✓ Telemetry generated: {len(matched)} points")

if __name__ == "__main__":
    tracks = [
        ("../data/indianapolis/R1_indianapolis_motor_speedway_telemetry.csv",
         "../frontend/public/tracks/indianapolis.json",
         "../frontend/public/telemetry/indianapolis.json",
         "Indianapolis Motor Speedway"),
        ("../data/barber/R1_barber_telemetry_data.csv",
         "../frontend/public/tracks/barber.json",
         "../frontend/public/telemetry/barber.json",
         "Barber Motorsports Park"),
    ]
    
    for csv_path, track_path, output_path, track_name in tracks:
        try:
            generate_telemetry_json(csv_path, track_path, output_path, track_name)
            print()
        except Exception as e:
            print(f"✗ Failed: {e}\n")
