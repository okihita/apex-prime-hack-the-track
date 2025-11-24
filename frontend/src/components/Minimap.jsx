import { useEffect, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'
import { OrthographicCamera } from '@react-three/drei'

function TrackView({ modelPath }) {
  if (!modelPath) return null
  
  const gltf = useGLTF(modelPath)
  
  return (
    <>
      <ambientLight intensity={1} />
      <primitive object={gltf.scene} scale={10} />
    </>
  )
}

export default function Minimap({ modelPath }) {
  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      background: 'rgba(0,0,0,0.8)',
      padding: '10px',
      borderRadius: '4px',
      border: '1px solid #333'
    }}>
      <div style={{
        color: '#fff',
        fontFamily: 'monospace',
        fontSize: '10px',
        marginBottom: '5px',
        opacity: 0.6
      }}>
        MINIMAP
      </div>
      <div style={{
        width: '200px',
        height: '200px',
        border: '1px solid #333',
        background: '#000'
      }}>
        {modelPath && (
          <Canvas>
            <OrthographicCamera makeDefault position={[0, 500, 0]} zoom={1} />
            <TrackView modelPath={modelPath} />
          </Canvas>
        )}
      </div>
    </div>
  )
}
