import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

export default function ChaseCamera({ target, distance = 30, height = 15 }) {
  const { camera } = useThree()
  const targetPos = useRef(new THREE.Vector3())
  const currentPos = useRef(new THREE.Vector3())
  
  useEffect(() => {
    if (target) {
      currentPos.current.copy(camera.position)
    }
  }, [target, camera])
  
  useFrame(() => {
    if (!target || !target.position) return
    
    // Calculate target camera position (behind and above car)
    const carPos = new THREE.Vector3(
      target.position[0],
      target.position[1],
      target.position[2]
    )
    
    // Get car rotation to position camera behind it
    const carRotation = target.rotation || 0
    const offset = new THREE.Vector3(
      Math.sin(carRotation) * distance,
      height,
      Math.cos(carRotation) * distance
    )
    
    targetPos.current.copy(carPos).add(offset)
    
    // Smooth camera movement (lerp)
    currentPos.current.lerp(targetPos.current, 0.05)
    camera.position.copy(currentPos.current)
    
    // Look at car
    camera.lookAt(carPos.x, carPos.y + 2, carPos.z)
  })
  
  return null
}
