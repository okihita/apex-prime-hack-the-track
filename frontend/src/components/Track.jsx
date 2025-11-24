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
    <mesh geometry={geometry} receiveShadow>
      <meshStandardMaterial 
        color="#1a1a1a"
        roughness={0.9}
        metalness={0.1}
      />
    </mesh>
  )
}
