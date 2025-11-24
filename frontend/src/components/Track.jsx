import { useMemo } from 'react'
import { CatmullRomCurve3, Vector3, PlaneGeometry, DoubleSide } from 'three'
import * as THREE from 'three'

export default function Track({ trackData }) {
  const geometry = useMemo(() => {
    if (!trackData || !trackData.points) return null
    
    const points = trackData.points.map(p => new Vector3(p[0], p[1], p[2]))
    const curve = new CatmullRomCurve3(points, true)
    
    // Create flat ribbon geometry
    const trackWidth = 20 // Wide track
    const segments = 500
    const vertices = []
    const indices = []
    
    for (let i = 0; i <= segments; i++) {
      const t = i / segments
      const point = curve.getPoint(t)
      const tangent = curve.getTangent(t)
      
      // Calculate perpendicular vector for width
      const perpendicular = new Vector3(-tangent.z, 0, tangent.x).normalize()
      
      // Left and right edges
      const left = point.clone().add(perpendicular.clone().multiplyScalar(trackWidth / 2))
      const right = point.clone().sub(perpendicular.clone().multiplyScalar(trackWidth / 2))
      
      vertices.push(left.x, left.y, left.z)
      vertices.push(right.x, right.y, right.z)
      
      // Create triangles
      if (i < segments) {
        const base = i * 2
        indices.push(base, base + 1, base + 2)
        indices.push(base + 1, base + 3, base + 2)
      }
    }
    
    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))
    geometry.setIndex(indices)
    geometry.computeVertexNormals()
    
    return geometry
  }, [trackData])
  
  if (!geometry) return null
  
  return (
    <mesh geometry={geometry} receiveShadow rotation={[0, 0, 0]}>
      <meshStandardMaterial 
        color="#666666"
        roughness={0.8}
        metalness={0.1}
        side={DoubleSide}
      />
    </mesh>
  )
}
