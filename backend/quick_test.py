"""Quick test to generate track from sample data"""
import json

# Sample GPS points from Indianapolis (manually extracted)
sample_gps = [
    (39.793159, -86.238739),
    (39.793167, -86.238739),
    (39.793175, -86.238739),
    (39.793182, -86.238739),
    (39.793190, -86.238739),
    # Add more points in a loop pattern
]

# Generate a simple oval for demo
import numpy as np

# Create oval track (Indianapolis-like)
points = []
for i in range(100):
    angle = (i / 100) * 2 * np.pi
    # Oval shape
    x = 400 * np.cos(angle)
    z = 200 * np.sin(angle)
    points.append([float(x), 0.0, float(z)])

track_data = {
    "name": "Indianapolis Motor Speedway (Demo)",
    "points": points,
    "metadata": {
        "point_count": len(points),
        "source": "demo_data"
    }
}

# Save
import os
os.makedirs("../frontend/public/tracks", exist_ok=True)

with open("../frontend/public/tracks/indianapolis.json", 'w') as f:
    json.dump(track_data, f, indent=2)

print(f"✓ Demo track generated: {len(points)} points")
print("  Track: Indianapolis Motor Speedway (simplified oval)")
