import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export default function Car({ position, rotation, speed, steeringAngle }) {
  const carRef = useRef()
  const wheelsRef = useRef([])
  
  // Simple car geometry (box for now, will replace with 3D model later)
  const carWidth = 2
  const carLength = 4
  const carHeight = 1.5
  
  useFrame((state, delta) => {
    if (!carRef.current) return
    
    // Update car position and rotation
    if (position) {
      carRef.current.position.set(position[0], position[1], position[2])
    }
    if (rotation !== undefined) {
      carRef.current.rotation.y = rotation
    }
    
    // Rotate wheels based on speed
    if (wheelsRef.current && speed) {
      const wheelRotation = (speed / 100) * delta * 10
      wheelsRef.current.forEach(wheel => {
        if (wheel) wheel.rotation.x += wheelRotation
      })
    }
    
    // Steer front wheels
    if (wheelsRef.current[0] && wheelsRef.current[1] && steeringAngle !== undefined) {
      const steerAngle = (steeringAngle / 450) * 0.5 // Normalize steering
      wheelsRef.current[0].rotation.y = steerAngle
      wheelsRef.current[1].rotation.y = steerAngle
    }
  })
  
  return (
    <group ref={carRef}>
      {/* Car body */}
      <mesh position={[0, carHeight / 2, 0]}>
        <boxGeometry args={[carWidth, carHeight, carLength]} />
        <meshStandardMaterial color="#cc0000" metalness={0.6} roughness={0.4} />
      </mesh>
      
      {/* Wheels */}
      {/* Front Left */}
      <group position={[-carWidth / 2 - 0.3, 0.4, carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[0] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[0.4, 0.4, 0.3, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
      
      {/* Front Right */}
      <group position={[carWidth / 2 + 0.3, 0.4, carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[1] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[0.4, 0.4, 0.3, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
      
      {/* Rear Left */}
      <group position={[-carWidth / 2 - 0.3, 0.4, -carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[2] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[0.4, 0.4, 0.3, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
      
      {/* Rear Right */}
      <group position={[carWidth / 2 + 0.3, 0.4, -carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[3] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[0.4, 0.4, 0.3, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
    </group>
  )
}
