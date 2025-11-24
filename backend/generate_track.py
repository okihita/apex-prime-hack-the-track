"""
Generate 3D track mesh from GPS points
"""
import json
import numpy as np
from parse_gps import parse_gps_from_telemetry, gps_to_track_points

def smooth_points(points, window=5):
    """Smooth track points using moving average"""
    if len(points) < window:
        return points
    
    smoothed = []
    for i in range(len(points)):
        start = max(0, i - window // 2)
        end = min(len(points), i + window // 2 + 1)
        window_points = points[start:end]
        
        avg_x = sum(p[0] for p in window_points) / len(window_points)
        avg_y = sum(p[1] for p in window_points) / len(window_points)
        avg_z = sum(p[2] for p in window_points) / len(window_points)
        
        smoothed.append([avg_x, avg_y, avg_z])
    
    return smoothed

def downsample_points(points, target_count=500):
    """Reduce number of points while maintaining shape"""
    if len(points) <= target_count:
        return points
    
    step = len(points) / target_count
    indices = [int(i * step) for i in range(target_count)]
    
    return [points[i] for i in indices]

def generate_track_json(csv_path, output_path, track_name):
    """
    Generate track JSON file from telemetry CSV
    
    Args:
        csv_path: Path to telemetry CSV
        output_path: Where to save JSON
        track_name: Name of track (e.g., "indianapolis")
    """
    print(f"Generating track: {track_name}")
    
    # Parse GPS
    print("  Parsing GPS data...")
    gps_points = parse_gps_from_telemetry(csv_path)
    print(f"  Found {len(gps_points)} GPS points")
    
    # Convert to track coordinates
    print("  Converting to track coordinates...")
    track_points = gps_to_track_points(gps_points)
    
    # Downsample
    print("  Downsampling...")
    track_points = downsample_points(track_points, target_count=500)
    
    # Smooth
    print("  Smoothing...")
    track_points = smooth_points(track_points, window=5)
    
    # Close the loop (connect last point to first)
    if track_points:
        track_points.append(track_points[0])
    
    # Create JSON structure
    track_data = {
        "name": track_name,
        "points": track_points,
        "metadata": {
            "point_count": len(track_points),
            "source": csv_path
        }
    }
    
    # Save to file
    print(f"  Saving to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(track_data, f, indent=2)
    
    print(f"✓ Track generated: {len(track_points)} points")
    return track_data

if __name__ == "__main__":
    tracks = [
        ("../data/indianapolis/R1_indianapolis_motor_speedway_telemetry.csv", 
         "../frontend/public/tracks/indianapolis.json", 
         "Indianapolis Motor Speedway"),
        ("../data/barber/R1_barber_telemetry_data.csv", 
         "../frontend/public/tracks/barber.json", 
         "Barber Motorsports Park"),
        ("../data/COTA/Race 1/R1_cota_telemetry_data.csv", 
         "../frontend/public/tracks/cota.json", 
         "Circuit of the Americas"),
        ("../data/sebring/Sebring/Race 1/sebring_telemetry_R1.csv", 
         "../frontend/public/tracks/sebring.json", 
         "Sebring International Raceway"),
        ("../data/road-america/Road America/Race 1/R1_road_america_telemetry_data.csv", 
         "../frontend/public/tracks/road-america.json", 
         "Road America"),
    ]
    
    for csv_path, output_path, track_name in tracks:
        try:
            generate_track_json(csv_path, output_path, track_name)
            print()
        except Exception as e:
            print(f"✗ Failed to generate {track_name}: {e}\n")
