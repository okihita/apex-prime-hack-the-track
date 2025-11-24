import cv2
import numpy as np
import json
from pathlib import Path
from scipy import ndimage
from skimage import morphology

def extract_circuit_path(image_path):
    img = cv2.imread(str(image_path))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Detect all colored paths
    lower = np.array([0, 30, 30])
    upper = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Clean up
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # Get skeleton
    skeleton = morphology.skeletonize(mask > 0)
    
    # Find all skeleton points
    points = np.column_stack(np.where(skeleton > 0))
    
    if len(points) == 0:
        return []
    
    # Build adjacency graph
    from scipy.spatial import cKDTree
    tree = cKDTree(points)
    
    # Find all points within distance 2 (8-connected)
    pairs = tree.query_pairs(r=2.0)
    
    # Build adjacency list
    adj = {i: [] for i in range(len(points))}
    for i, j in pairs:
        adj[i].append(j)
        adj[j].append(i)
    
    # Find endpoint or start from any point
    start_idx = 0
    for i, neighbors in adj.items():
        if len(neighbors) == 1:  # Endpoint
            start_idx = i
            break
    
    # Traverse the path
    visited = set()
    path = []
    current = start_idx
    
    while current is not None:
        visited.add(current)
        path.append(points[current])
        
        # Find next unvisited neighbor
        next_node = None
        for neighbor in adj[current]:
            if neighbor not in visited:
                next_node = neighbor
                break
        
        current = next_node
    
    # If path is too short, try all connected components
    if len(path) < len(points) * 0.5:
        # Just use all points sorted by position
        path = points[np.argsort(points[:, 0])]
    
    # Simplify - keep every Nth point
    step = max(1, len(path) // 200)  # Target ~200 points
    simplified = path[::step]
    
    # Normalize to 3D coordinates
    h, w = img.shape[:2]
    scale = 200.0 / max(h, w)
    
    path_3d = []
    for p in simplified:
        x = (p[1] - w/2) * scale
        z = -(p[0] - h/2) * scale
        path_3d.append([float(x), 0.0, float(z)])
    
    return path_3d

def create_gltf(path_points, output_path, track_name):
    if len(path_points) < 2:
        print(f"Not enough points for {track_name}")
        return
    
    vertices = []
    indices = []
    radius = 3.0
    segments = 8
    
    # Create tube geometry
    for i, point in enumerate(path_points):
        for j in range(segments):
            angle = (j / segments) * 2 * np.pi
            x = point[0]
            y = point[1] + radius * np.cos(angle)
            z = point[2] + radius * np.sin(angle)
            vertices.extend([x, y, z])
    
    # Create triangles
    for i in range(len(path_points) - 1):
        for j in range(segments):
            next_j = (j + 1) % segments
            
            a = i * segments + j
            b = i * segments + next_j
            c = (i + 1) * segments + j
            d = (i + 1) * segments + next_j
            
            indices.extend([a, b, c, b, d, c])
    
    # Close the loop if endpoints are close
    if len(path_points) > 10:
        dist = np.linalg.norm(np.array(path_points[0]) - np.array(path_points[-1]))
        if dist < 20:
            i = len(path_points) - 1
            for j in range(segments):
                next_j = (j + 1) % segments
                a = i * segments + j
                b = i * segments + next_j
                c = j
                d = next_j
                indices.extend([a, b, c, b, d, c])
    
    gltf = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": track_name}],
        "meshes": [{
            "primitives": [{
                "attributes": {"POSITION": 0},
                "indices": 1,
                "mode": 4
            }]
        }],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": len(vertices) // 3,
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
    
    bin_path = output_path.with_suffix('.bin')
    with open(bin_path, 'wb') as f:
        f.write(np.array(vertices, dtype=np.float32).tobytes())
        f.write(np.array(indices, dtype=np.uint16).tobytes())
    
    print(f"✓ {track_name}: {len(path_points)} points")

# Process all images
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
    path_points = extract_circuit_path(img_path)
    if path_points:
        create_gltf(path_points, Path(f'output/{name}.gltf'), name)
    else:
        print(f"✗ Failed to extract path")
