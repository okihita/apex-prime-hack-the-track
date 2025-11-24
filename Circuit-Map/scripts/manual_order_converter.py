import cv2
import numpy as np
import json
from pathlib import Path
from skimage import morphology
from scipy.spatial import cKDTree

def extract_and_order_segment(mask, reverse=False):
    """Extract points from segment and order them"""
    skeleton = morphology.skeletonize(mask > 0)
    points = np.column_stack(np.where(skeleton > 0))
    
    if len(points) < 2:
        return []
    
    # Build graph
    tree = cKDTree(points)
    pairs = tree.query_pairs(r=2.0)
    
    adj = {i: [] for i in range(len(points))}
    for i, j in pairs:
        adj[i].append(j)
        adj[j].append(i)
    
    # Find endpoints
    endpoints = [i for i, neighbors in adj.items() if len(neighbors) == 1]
    
    if not endpoints:
        start_idx = 0
    else:
        start_idx = endpoints[0]
    
    # Traverse
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
    
    if reverse:
        path = path[::-1]
    
    return np.array(path) if path else np.array([])

def extract_barber_circuit(image_path):
    """Manually order Barber segments correctly"""
    img = cv2.imread(str(image_path))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3,3), np.uint8)
    
    # Extract blue segment (S1)
    blue_mask = cv2.inRange(hsv, np.array([100, 100, 100]), np.array([130, 255, 255]))
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
    blue_points = extract_and_order_segment(blue_mask)
    
    # Extract yellow segment (S2)
    yellow_mask = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([40, 255, 255]))
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
    yellow_points = extract_and_order_segment(yellow_mask)
    
    # Extract pink segment (S3)
    pink_mask = cv2.inRange(hsv, np.array([140, 100, 100]), np.array([170, 255, 255]))
    pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_CLOSE, kernel)
    pink_points = extract_and_order_segment(pink_mask)
    
    # Find which endpoints connect
    # Blue should connect to yellow at one end, pink at the other
    segments = []
    if len(blue_points) > 0:
        segments.append(blue_points)
    if len(yellow_points) > 0:
        segments.append(yellow_points)
    if len(pink_points) > 0:
        segments.append(pink_points)
    
    if not segments:
        return []
    
    # Try to connect segments by finding closest endpoints
    connected = list(segments[0])
    remaining = segments[1:]
    
    while remaining:
        last_point = connected[-1]
        first_point = connected[0]
        
        best_idx = -1
        best_dist = float('inf')
        connect_to_end = True
        reverse_segment = False
        
        for i, seg in enumerate(remaining):
            # Check all 4 connection possibilities
            d1 = np.linalg.norm(last_point - seg[0])
            d2 = np.linalg.norm(last_point - seg[-1])
            d3 = np.linalg.norm(first_point - seg[0])
            d4 = np.linalg.norm(first_point - seg[-1])
            
            min_dist = min(d1, d2, d3, d4)
            if min_dist < best_dist:
                best_dist = min_dist
                best_idx = i
                if min_dist == d1:
                    connect_to_end = True
                    reverse_segment = False
                elif min_dist == d2:
                    connect_to_end = True
                    reverse_segment = True
                elif min_dist == d3:
                    connect_to_end = False
                    reverse_segment = True
                else:
                    connect_to_end = False
                    reverse_segment = False
        
        if best_idx >= 0:
            seg = remaining.pop(best_idx)
            if reverse_segment:
                seg = seg[::-1]
            if connect_to_end:
                connected.extend(seg.tolist())
            else:
                connected = seg.tolist() + connected
    
    connected = np.array(connected)
    
    # Simplify
    step = max(1, len(connected) // 300)
    simplified = connected[::step]
    
    # Add closing point
    if len(simplified) > 10:
        simplified = np.vstack([simplified, simplified[0]])
    
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

print("\nProcessing Barber...")
path_points = extract_barber_circuit('source/images/Barber_Circuit_Map.png')
if path_points:
    create_gltf_line(path_points, Path('output/Barber.gltf'), 'Barber')
else:
    print("✗ Failed")
