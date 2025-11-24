import cv2
import numpy as np
import json
from pathlib import Path
from scipy import ndimage
from skimage import morphology

def extract_path_from_image(image_path):
    img = cv2.imread(str(image_path))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Detect colored paths (not white/gray background)
    lower = np.array([0, 30, 30])
    upper = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Clean up mask
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Get skeleton (centerline)
    skeleton = morphology.skeletonize(mask > 0)
    
    # Find contours and order points
    points = np.column_stack(np.where(skeleton > 0))
    
    if len(points) == 0:
        return []
    
    # Sort points to create a path
    ordered = [points[0]]
    remaining = list(points[1:])
    
    while remaining and len(ordered) < len(points):
        last = ordered[-1]
        distances = [np.linalg.norm(last - p) for p in remaining]
        if not distances:
            break
        nearest_idx = np.argmin(distances)
        if distances[nearest_idx] < 50:  # Max gap threshold
            ordered.append(remaining.pop(nearest_idx))
        else:
            break
    
    # Simplify path (reduce points)
    ordered = np.array(ordered)
    simplified = [ordered[0]]
    for i in range(1, len(ordered) - 1):
        if i % 10 == 0:  # Keep every 10th point
            simplified.append(ordered[i])
    simplified.append(ordered[-1])
    
    # Normalize coordinates (flip Y, center, scale)
    simplified = np.array(simplified)
    h, w = img.shape[:2]
    normalized = simplified.copy().astype(float)
    normalized[:, 0] = (normalized[:, 0] - h/2) / h * 100  # Scale to ~100 units
    normalized[:, 1] = (normalized[:, 1] - w/2) / w * 100
    
    # Swap X,Y and flip Y for proper orientation
    path_3d = [[float(p[1]), 0.0, float(-p[0])] for p in normalized]
    
    return path_3d

def create_gltf(path_points, output_path, track_name):
    vertices = []
    indices = []
    
    # Create tube geometry along path
    radius = 2.0
    segments = 8
    
    for i, point in enumerate(path_points):
        for j in range(segments):
            angle = (j / segments) * 2 * np.pi
            x = point[0] + radius * np.cos(angle)
            y = point[1] + radius * np.sin(angle)
            z = point[2]
            vertices.extend([x, y, z])
    
    # Create indices for triangles
    for i in range(len(path_points) - 1):
        for j in range(segments):
            next_j = (j + 1) % segments
            
            a = i * segments + j
            b = i * segments + next_j
            c = (i + 1) * segments + j
            d = (i + 1) * segments + next_j
            
            indices.extend([a, b, c, b, d, c])
    
    # Create GLTF structure
    gltf = {
        "asset": {"version": "2.0", "generator": "Circuit Converter"},
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
            {
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": len(vertices) * 4
            },
            {
                "buffer": 0,
                "byteOffset": len(vertices) * 4,
                "byteLength": len(indices) * 2
            }
        ],
        "buffers": [{
            "byteLength": len(vertices) * 4 + len(indices) * 2,
            "uri": f"{track_name}.bin"
        }]
    }
    
    # Write GLTF
    with open(output_path, 'w') as f:
        json.dump(gltf, f, indent=2)
    
    # Write binary buffer
    bin_path = output_path.with_suffix('.bin')
    with open(bin_path, 'wb') as f:
        f.write(np.array(vertices, dtype=np.float32).tobytes())
        f.write(np.array(indices, dtype=np.uint16).tobytes())
    
    print(f"Created {output_path}")

# Process all PNG files
png_files = list(Path('.').glob('*_Map.png'))

for png_file in png_files:
    print(f"\nProcessing {png_file}...")
    track_name = png_file.stem.replace('_Map', '').replace('_', '-')
    
    path_points = extract_path_from_image(png_file)
    
    if path_points:
        output_gltf = Path(f"{track_name}.gltf")
        create_gltf(path_points, output_gltf, track_name)
        print(f"✓ Generated {len(path_points)} path points")
    else:
        print(f"✗ Could not extract path")

print("\n✓ All circuits converted!")
