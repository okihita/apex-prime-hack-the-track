import { useMemo } from 'react'
import { CatmullRomCurve3, Vector3, TubeGeometry } from 'three'

export default function Track({ trackData }) {
  const geometry = useMemo(() => {
    if (!trackData || !trackData.points) return null
    
    // Convert points to Vector3
    const points = trackData.points.map(p => new Vector3(p[0], p[1], p[2]))
    
    // Create smooth curve
    const curve = new CatmullRomCurve3(points, true) // true = closed loop
    
    // Create tube geometry along curve
    const tubeGeometry = new TubeGeometry(
      curve,
      500,  // segments
      10,   // radius (track width)
      8,    // radial segments
      true  // closed
    )
    
    return tubeGeometry
  }, [trackData])
  
  if (!geometry) return null
  
  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial 
        color="#333333" 
        roughness={0.8}
        metalness={0.2}
      />
    </mesh>
  )
}
