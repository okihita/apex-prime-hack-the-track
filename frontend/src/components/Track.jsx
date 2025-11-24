import { useMemo } from 'react'
import { CatmullRomCurve3, Vector3, TubeGeometry } from 'three'

export default function Track({ trackData }) {
  const geometry = useMemo(() => {
    if (!trackData || !trackData.points) return null
    
    const points = trackData.points.map(p => new Vector3(p[0], p[1], p[2]))
    const curve = new CatmullRomCurve3(points, true)
    const tubeGeometry = new TubeGeometry(curve, 500, 10, 8, true)
    
    return tubeGeometry
  }, [trackData])
  
  if (!geometry) return null
  
  return (
    <group>
      {/* Main track surface - medium gray */}
      <mesh geometry={geometry} receiveShadow>
        <meshStandardMaterial 
          color="#666666"
          roughness={0.8}
          metalness={0.1}
        />
      </mesh>
      
      {/* White center line */}
      <mesh geometry={geometry}>
        <meshStandardMaterial 
          color="#ffffff"
          roughness={0.9}
          transparent
          opacity={0.3}
        />
      </mesh>
    </group>
  )
}
