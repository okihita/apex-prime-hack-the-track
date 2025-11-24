"""
Parse GPS coordinates from telemetry CSV
"""
import pandas as pd
import numpy as np

def parse_gps_from_telemetry(csv_path, lap_number=None):
    """
    Extract GPS coordinates from telemetry CSV
    
    Args:
        csv_path: Path to telemetry CSV file
        lap_number: Specific lap to extract (None = best lap)
    
    Returns:
        List of (lat, lon) tuples
    """
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Find best lap if not specified
    if lap_number is None:
        lap_number = find_best_lap(csv_path)
    
    # Filter for specific lap
    lap_data = df[df['lap'] == lap_number]
    
    # Extract GPS points
    lat_data = lap_data[lap_data['telemetry_name'] == 'VBOX_Lat_Min']
    lon_data = lap_data[lap_data['telemetry_name'] == 'VBOX_Long_Minutes']
    
    # Merge by timestamp
    gps_points = []
    for _, lat_row in lat_data.iterrows():
        timestamp = lat_row['timestamp']
        lon_row = lon_data[lon_data['timestamp'] == timestamp]
        if not lon_row.empty:
            lat = float(lat_row['telemetry_value'])
            lon = float(lon_row['telemetry_value'])
            gps_points.append((lat, lon))
    
    return gps_points

def find_best_lap(csv_path):
    """Find lap number with most complete data"""
    df = pd.read_csv(csv_path)
    
    # Count GPS points per lap
    lap_counts = df[df['telemetry_name'] == 'VBOX_Lat_Min'].groupby('lap').size()
    
    # Return lap with most points
    return lap_counts.idxmax()

def lat_lon_to_meters(lat, lon, origin_lat, origin_lon):
    """
    Convert lat/lon to local Cartesian coordinates (meters)
    
    Uses simple equirectangular projection (good enough for small areas)
    """
    # Earth radius in meters
    R = 6371000
    
    # Convert to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    origin_lat_rad = np.radians(origin_lat)
    origin_lon_rad = np.radians(origin_lon)
    
    # Calculate x, y in meters
    x = R * (lon_rad - origin_lon_rad) * np.cos(origin_lat_rad)
    y = R * (lat_rad - origin_lat_rad)
    
    return x, y

def gps_to_track_points(gps_points):
    """
    Convert GPS coordinates to local track coordinates
    
    Returns:
        List of [x, y, z] points (z=0 for flat track)
    """
    if not gps_points:
        return []
    
    # Use first point as origin
    origin_lat, origin_lon = gps_points[0]
    
    track_points = []
    for lat, lon in gps_points:
        x, z = lat_lon_to_meters(lat, lon, origin_lat, origin_lon)
        track_points.append([x, 0, z])  # y=0 for flat track
    
    return track_points

if __name__ == "__main__":
    # Test with Indianapolis data
    csv_path = "../data/indianapolis/R1_indianapolis_motor_speedway_telemetry.csv"
    
    print("Parsing GPS data...")
    gps_points = parse_gps_from_telemetry(csv_path)
    print(f"Found {len(gps_points)} GPS points")
    
    print("\nConverting to track coordinates...")
    track_points = gps_to_track_points(gps_points)
    print(f"Generated {len(track_points)} track points")
    print(f"First point: {track_points[0]}")
    print(f"Last point: {track_points[-1]}")
