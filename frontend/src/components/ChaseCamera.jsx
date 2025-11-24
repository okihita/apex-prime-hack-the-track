import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

export default function ChaseCamera({ target, distance = 50, height = 25 }) {
  const { camera } = useThree()
  const targetPos = useRef(new THREE.Vector3())
  const currentPos = useRef(new THREE.Vector3())
  const lookAtPos = useRef(new THREE.Vector3())
  const currentLookAt = useRef(new THREE.Vector3())
  
  useEffect(() => {
    if (target) {
      currentPos.current.copy(camera.position)
      currentLookAt.current.set(target.position[0], target.position[1], target.position[2])
    }
  }, [target, camera])
  
  useFrame(() => {
    if (!target || !target.position) return
    
    const carPos = new THREE.Vector3(
      target.position[0],
      target.position[1],
      target.position[2]
    )
    
    // Fixed offset behind car (don't use rotation, just follow position)
    const offset = new THREE.Vector3(0, height, distance)
    targetPos.current.copy(carPos).add(offset)
    
    // Very smooth camera movement (slower lerp = smoother)
    currentPos.current.lerp(targetPos.current, 0.02)
    camera.position.copy(currentPos.current)
    
    // Smooth look-at target
    lookAtPos.current.copy(carPos).add(new THREE.Vector3(0, 5, 0))
    currentLookAt.current.lerp(lookAtPos.current, 0.05)
    camera.lookAt(currentLookAt.current)
  })
  
  return null
}
