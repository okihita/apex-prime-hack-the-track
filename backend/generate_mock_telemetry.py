import json
import math

def generate_mock_telemetry(track_points, num_points=1000):
    """Generate mock telemetry for amateur racer"""
    telemetry = []
    
    for i in range(num_points):
        t = i / num_points
        point_idx = int(t * len(track_points)) % len(track_points)
        point = track_points[point_idx]
        
        # Amateur racer profile
        speed = 180 + math.sin(t * 20) * 30  # 150-210 km/h
        steering = math.sin(t * 40) * 15  # -15 to 15 degrees
        throttle = 0.7 + math.sin(t * 10) * 0.2  # 50-90%
        brake = max(0, -math.sin(t * 40) * 0.5)  # 0-50%
        
        telemetry.append({
            "position": point,
            "speed": speed,
            "steeringAngle": steering,
            "throttle": throttle,
            "brake": brake,
            "gear": 4,
            "rpm": 6000 + int(speed * 10),
            "lapTime": t * 90  # ~90 second lap
        })
    
    return telemetry

# Generate for missing tracks
tracks = ['cota', 'road-america', 'sebring', 'vir', 'sonoma']

for track_name in tracks:
    # Load track data
    with open(f'../frontend/public/tracks/{track_name}.json', 'r') as f:
        track_data = json.load(f)
    
    # Generate mock telemetry
    telemetry = generate_mock_telemetry(track_data['points'])
    
    # Save
    with open(f'../frontend/public/telemetry/{track_name}.json', 'w') as f:
        json.dump(telemetry, f)
    
    print(f"✅ Generated mock telemetry for {track_name}")
