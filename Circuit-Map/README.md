# Circuit Maps - 3D GLTF Models

Racing circuit track paths converted to Three.js-compatible GLTF format.

## Circuits

- **Barber** - Barber Motorsports Park
- **COTA** - Circuit of the Americas
- **Indy** - Indianapolis Motor Speedway
- **Road-America** - Road America
- **Sebring** - Sebring International Raceway
- **Sonoma** - Sonoma Raceway
- **VIR** - Virginia International Raceway

## Structure

```
├── output/          # GLTF and binary files
├── source/
│   ├── pdfs/       # Original PDF files
│   └── images/     # Extracted PNG images
└── scripts/        # Conversion scripts and example
```

## Usage

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('output/Barber.gltf', (gltf) => {
    scene.add(gltf.scene);
});
```

See `scripts/example.html` for a complete demo.
