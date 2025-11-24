import { useMemo, Suspense } from 'react'
import { useGLTF } from '@react-three/drei'
import { CatmullRomCurve3, Vector3 } from 'three'
import * as THREE from 'three'

function TrackModel({ modelPath }) {
  const gltf = useGLTF(modelPath)
  return <primitive object={gltf.scene} scale={10} />
}

export default function Track({ trackData, modelPath }) {
  
  const { trackGeometry, centerLineGeometry } = useMemo(() => {
    if (!trackData || !trackData.points || trackData.points.length < 3) {
      return { trackGeometry: null, centerLineGeometry: null }
    }
    
    const points = trackData.points.map(p => new Vector3(p[0], p[1], p[2]))
    const curve = new CatmullRomCurve3(points, true)
    
    // Center line for debugging
    const centerLinePoints = curve.getPoints(500)
    const centerLineGeometry = new THREE.BufferGeometry().setFromPoints(centerLinePoints)
    
    // Track surface
    const trackWidth = 20
    const segments = 500
    const vertices = []
    const indices = []
    
    for (let i = 0; i <= segments; i++) {
      const t = i / segments
      const point = curve.getPoint(t)
      const tangent = curve.getTangent(t)
      
      const perpendicular = new Vector3(-tangent.z, 0, tangent.x).normalize()
      
      const left = point.clone().add(perpendicular.clone().multiplyScalar(trackWidth / 2))
      const right = point.clone().sub(perpendicular.clone().multiplyScalar(trackWidth / 2))
      
      vertices.push(left.x, left.y, left.z)
      vertices.push(right.x, right.y, right.z)
      
      if (i < segments) {
        const base = i * 2
        indices.push(base, base + 1, base + 2)
        indices.push(base + 1, base + 3, base + 2)
      }
    }
    
    const trackGeometry = new THREE.BufferGeometry()
    trackGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))
    trackGeometry.setIndex(indices)
    trackGeometry.computeVertexNormals()
    
    return { trackGeometry, centerLineGeometry }
  }, [trackData])
  
  if (!trackGeometry && !modelPath) return null
  
  return (
    <group>
      {modelPath ? (
        <Suspense fallback={null}>
          <TrackModel modelPath={modelPath} />
        </Suspense>
      ) : trackGeometry ? (
        <>
          <mesh geometry={trackGeometry} receiveShadow>
            <meshStandardMaterial 
              color="#1a1a1a"
              roughness={0.95}
              metalness={0.05}
            />
          </mesh>
          <line geometry={centerLineGeometry}>
            <lineBasicMaterial color="#ffffff" linewidth={3} opacity={0.8} transparent />
          </line>
        </>
      ) : null}
    </group>
  )
}
