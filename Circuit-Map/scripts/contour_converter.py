import cv2
import numpy as np
import json
from pathlib import Path
from scipy.interpolate import splprep, splev

def extract_centerline_from_contours(image_path, detect_black=False):
    img = cv2.imread(str(image_path))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    if detect_black:
        # Detect thick black lines (track outline)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Get black pixels
        _, black_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        
        # Erode to remove thin lines (numbers, labels)
        kernel_erode = np.ones((3,3), np.uint8)
        mask = cv2.erode(black_mask, kernel_erode, iterations=2)
        
        # Dilate to connect segments and restore track thickness
        kernel_dilate = np.ones((7,7), np.uint8)
        mask = cv2.dilate(mask, kernel_dilate, iterations=4)
        
        # Close gaps
        kernel_close = np.ones((9,9), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    else:
        # Get all colored areas (not background)
        lower = np.array([0, 30, 30])
        upper = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        # Clean up
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.dilate(mask, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return []
    
    # Get largest contour (should be track, not legend)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Filter: track must be at least 10% of image area
    img_area = img.shape[0] * img.shape[1]
    min_area = img_area * 0.10
    
    largest_contour = None
    for contour in contours:
        if cv2.contourArea(contour) >= min_area:
            largest_contour = contour
            break
    
    if largest_contour is None:
        # Fallback to largest
        largest_contour = contours[0]
    
    # Approximate to reduce points and smooth tiny spikes
    epsilon = 0.001 * cv2.arcLength(largest_contour, True)  # Balanced value
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)
    
    # Extract points
    points = approx.reshape(-1, 2)
    
    # Convert to 3D - match exact plane dimensions
    h, w = img.shape[:2]
    aspect = w / h
    
    # Plane is 700 height, width = 700 * aspect
    plane_height = 700
    plane_width = 700 * aspect
    
    path_3d = []
    for p in points:
        x = (p[0] / w - 0.5) * plane_width
        z = (p[1] / h - 0.5) * plane_height
        path_3d.append([float(x), 0.0, float(z)])
    
    # Close the loop
    if len(path_3d) > 0:
        path_3d.append(path_3d[0])
    
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
    'Barber': ('source/images/Barber_Circuit_Map.png', False),
    'COTA': ('source/images/COTA_Circuit_Map.png', True),
    'Indy': ('source/images/Indy_Circuit_Map.png', True),
    'Road-America': ('source/images/Road_America_Map.png', True),
    'Sebring': ('source/images/Sebring_Track_Sector_Map.png', True),
    'Sonoma': ('source/images/Sonoma_Map.png', True),
    'VIR': ('source/images/VIR_map.png', True)
}

for name, (img_path, detect_black) in circuits.items():
    print(f"\nProcessing {name}...")
    path_points = extract_centerline_from_contours(img_path, detect_black)
    if path_points:
        create_gltf_line(path_points, Path(f'output/{name}.gltf'), name)
    else:
        print(f"✗ Failed")
