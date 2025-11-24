"""
Parse GPS coordinates from telemetry CSV (optimized for large files)
"""
import pandas as pd
import numpy as np

def parse_gps_from_telemetry(csv_path, lap_number=2):
    """
    Extract GPS coordinates from telemetry CSV
    Only reads GPS data, not entire file
    """
    print(f"  Reading GPS data from lap {lap_number}...")
    
    # Read only GPS rows (much faster than reading entire file)
    chunks = []
    for chunk in pd.read_csv(csv_path, chunksize=100000):
        # Filter for specific lap and GPS data only
        gps_chunk = chunk[
            (chunk['lap'] == lap_number) & 
            (chunk['telemetry_name'].isin(['VBOX_Lat_Min', 'VBOX_Long_Minutes']))
        ]
        if not gps_chunk.empty:
            chunks.append(gps_chunk)
    
    if not chunks:
        print(f"  No GPS data found for lap {lap_number}")
        return []
    
    df = pd.concat(chunks, ignore_index=True)
    
    # Pivot to get lat/lon in same row
    lat_data = df[df['telemetry_name'] == 'VBOX_Lat_Min'][['timestamp', 'telemetry_value']]
    lon_data = df[df['telemetry_name'] == 'VBOX_Long_Minutes'][['timestamp', 'telemetry_value']]
    
    # Merge on timestamp
    merged = pd.merge(lat_data, lon_data, on='timestamp', suffixes=('_lat', '_lon'))
    
    # Convert to list of tuples
    gps_points = list(zip(merged['telemetry_value_lat'], merged['telemetry_value_lon']))
    
    print(f"  Found {len(gps_points)} GPS points")
    return gps_points

def lat_lon_to_meters(lat, lon, origin_lat, origin_lon):
    """Convert lat/lon to local Cartesian coordinates (meters)"""
    R = 6371000  # Earth radius
    
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    origin_lat_rad = np.radians(origin_lat)
    origin_lon_rad = np.radians(origin_lon)
    
    x = R * (lon_rad - origin_lon_rad) * np.cos(origin_lat_rad)
    y = R * (lat_rad - origin_lat_rad)
    
    return x, y

def gps_to_track_points(gps_points):
    """Convert GPS coordinates to local track coordinates"""
    if not gps_points:
        return []
    
    origin_lat, origin_lon = gps_points[0]
    
    track_points = []
    for lat, lon in gps_points:
        x, z = lat_lon_to_meters(lat, lon, origin_lat, origin_lon)
        track_points.append([x, 0, z])
    
    return track_points
