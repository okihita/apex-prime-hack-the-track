import cv2
import numpy as np
import json
from pathlib import Path
from skimage import morphology

def extract_all_segments(image_path):
    img = cv2.imread(str(image_path))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    color_ranges = [
        ([0, 100, 100], [10, 255, 255]),
        ([170, 100, 100], [180, 255, 255]),
        ([100, 100, 100], [130, 255, 255]),
        ([20, 100, 100], [40, 255, 255]),
        ([140, 100, 100], [170, 255, 255]),
    ]
    
    all_points = []
    
    for lower, upper in color_ranges:
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        if np.sum(mask) > 100:
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.dilate(mask, kernel, iterations=1)
            
            skeleton = morphology.skeletonize(mask > 0)
            points = np.column_stack(np.where(skeleton > 0))
            if len(points) > 0:
                all_points.extend(points.tolist())
    
    if len(all_points) == 0:
        return []
    
    all_points = np.array(all_points)
    all_points = np.unique(all_points, axis=0)
    
    start_idx = np.argmin(all_points[:, 1])
    ordered = [all_points[start_idx]]
    remaining = list(range(len(all_points)))
    remaining.remove(start_idx)
    
    while remaining:
        last = ordered[-1]
        distances = [np.linalg.norm(last - all_points[i]) for i in remaining]
        nearest_idx = remaining[np.argmin(distances)]
        
        if distances[np.argmin(distances)] > 50:
            break
            
        ordered.append(all_points[nearest_idx])
        remaining.remove(nearest_idx)
    
    ordered = np.array(ordered)
    step = max(1, len(ordered) // 200)
    simplified = ordered[::step]
    
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
    
    # Flatten points for vertices
    vertices = []
    for p in path_points:
        vertices.extend(p)
    
    # Create line indices (just sequential)
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
                "mode": 3  # LINE_STRIP mode
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
    path_points = extract_all_segments(img_path)
    if path_points:
        create_gltf_line(path_points, Path(f'output/{name}.gltf'), name)
    else:
        print(f"✗ Failed")
