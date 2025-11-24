import cv2
import numpy as np
import json
from pathlib import Path
from skimage import morphology
from scipy.spatial import cKDTree

def extract_segment(mask):
    """Extract ordered points from a single segment"""
    skeleton = morphology.skeletonize(mask > 0)
    points = np.column_stack(np.where(skeleton > 0))
    
    if len(points) < 2:
        return []
    
    # Build adjacency graph
    tree = cKDTree(points)
    pairs = tree.query_pairs(r=2.0)
    
    adj = {i: [] for i in range(len(points))}
    for i, j in pairs:
        adj[i].append(j)
        adj[j].append(i)
    
    # Find endpoint (degree 1) or use first point
    start_idx = 0
    for i, neighbors in adj.items():
        if len(neighbors) == 1:
            start_idx = i
            break
    
    # Traverse path
    visited = set()
    path = []
    current = start_idx
    
    while current is not None:
        visited.add(current)
        path.append(points[current])
        
        next_node = None
        for neighbor in adj[current]:
            if neighbor not in visited:
                next_node = neighbor
                break
        current = next_node
    
    return np.array(path) if path else np.array([])

def extract_circuit(image_path):
    img = cv2.imread(str(image_path))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Extract each color segment separately
    segments = []
    
    # Blue (S1)
    blue_mask = cv2.inRange(hsv, np.array([100, 100, 100]), np.array([130, 255, 255]))
    if np.sum(blue_mask) > 100:
        kernel = np.ones((3,3), np.uint8)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
        blue_points = extract_segment(blue_mask)
        if len(blue_points) > 0:
            segments.append(('blue', blue_points))
    
    # Yellow (S2)
    yellow_mask = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([40, 255, 255]))
    if np.sum(yellow_mask) > 100:
        kernel = np.ones((3,3), np.uint8)
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
        yellow_points = extract_segment(yellow_mask)
        if len(yellow_points) > 0:
            segments.append(('yellow', yellow_points))
    
    # Pink/Magenta (S3)
    pink_mask = cv2.inRange(hsv, np.array([140, 100, 100]), np.array([170, 255, 255]))
    if np.sum(pink_mask) > 100:
        kernel = np.ones((3,3), np.uint8)
        pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_CLOSE, kernel)
        pink_points = extract_segment(pink_mask)
        if len(pink_points) > 0:
            segments.append(('pink', pink_points))
    
    # Red
    red_mask1 = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
    red_mask2 = cv2.inRange(hsv, np.array([170, 100, 100]), np.array([180, 255, 255]))
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    if np.sum(red_mask) > 100:
        kernel = np.ones((3,3), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_points = extract_segment(red_mask)
        if len(red_points) > 0:
            segments.append(('red', red_points))
    
    if not segments:
        return []
    
    # Connect segments by finding closest endpoints
    all_points = []
    for color, points in segments:
        all_points.extend(points.tolist())
    
    all_points = np.array(all_points)
    
    # Simplify
    step = max(1, len(all_points) // 300)
    simplified = all_points[::step]
    
    # Convert to 3D
    h, w = img.shape[:2]
    scale = 500.0 / max(h, w)
    
    path_3d = []
    for p in simplified:
        x = (p[1] - w/2) * scale
        z = -(p[0] - h/2) * scale
        path_3d.append([float(x), 0.0, float(z)])
    
    return path_3d

def create_gltf_line(path_points, output_path, track_name):
    if len(path_points) < 2:
        return
    
    vertices = []
    for p in path_points:
        vertices.extend(p)
    
    indices = list(range(len(path_points)))
    
    gltf = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": track_name}],
        "meshes": [{
            "primitives": [{
                "attributes": {"POSITION": 0},
                "indices": 1,
                "mode": 3
            }]
        }],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": len(path_points),
                "type": "VEC3",
                "max": [max(vertices[0::3]), max(vertices[1::3]), max(vertices[2::3])],
                "min": [min(vertices[0::3]), min(vertices[1::3]), min(vertices[2::3])]
            },
            {
                "bufferView": 1,
                "componentType": 5123,
                "count": len(indices),
                "type": "SCALAR"
            }
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(vertices) * 4},
            {"buffer": 0, "byteOffset": len(vertices) * 4, "byteLength": len(indices) * 2}
        ],
        "buffers": [{
            "byteLength": len(vertices) * 4 + len(indices) * 2,
            "uri": f"{track_name}.bin"
        }]
    }
    
    with open(output_path, 'w') as f:
        json.dump(gltf, f, indent=2)
    
    with open(output_path.with_suffix('.bin'), 'wb') as f:
        f.write(np.array(vertices, dtype=np.float32).tobytes())
        f.write(np.array(indices, dtype=np.uint16).tobytes())
    
    print(f"✓ {track_name}: {len(path_points)} points")

circuits = {
    'Barber': 'source/images/Barber_Circuit_Map.png',
    'COTA': 'source/images/COTA_Circuit_Map.png',
    'Indy': 'source/images/Indy_Circuit_Map.png',
    'Road-America': 'source/images/Road_America_Map.png',
    'Sebring': 'source/images/Sebring_Track_Sector_Map.png',
    'Sonoma': 'source/images/Sonoma_Map.png',
    'VIR': 'source/images/VIR_map.png'
}

for name, img_path in circuits.items():
    print(f"\nProcessing {name}...")
    path_points = extract_circuit(img_path)
    if path_points:
        create_gltf_line(path_points, Path(f'output/{name}.gltf'), name)
    else:
        print(f"✗ Failed")
