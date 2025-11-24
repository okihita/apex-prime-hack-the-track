import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

export default function Car({ position, rotation, speed, steeringAngle }) {
  const carRef = useRef()
  const wheelsRef = useRef([])
  
  // Bigger car
  const carWidth = 8
  const carLength = 16
  const carHeight = 6
  
  useFrame((state, delta) => {
    if (!carRef.current) return
    
    // Update car position and rotation
    if (position) {
      carRef.current.position.set(position[0], position[1] + carHeight/2, position[2])
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
      const steerAngle = (steeringAngle / 450) * 0.5
      wheelsRef.current[0].rotation.y = steerAngle
      wheelsRef.current[1].rotation.y = steerAngle
    }
  })
  
  if (!position) return null
  
  return (
    <group ref={carRef}>
      {/* Car body - brighter red with emissive */}
      <mesh position={[0, 0, 0]} castShadow>
        <boxGeometry args={[carWidth, carHeight, carLength]} />
        <meshStandardMaterial 
          color="#ff0000"
          emissive="#660000"
          emissiveIntensity={0.3}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>
      
      {/* Wheels - bigger */}
      {/* Front Left */}
      <group position={[-carWidth / 2 - 1, -carHeight/2 + 1.5, carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[0] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[1.5, 1.5, 1, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
      
      {/* Front Right */}
      <group position={[carWidth / 2 + 1, -carHeight/2 + 1.5, carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[1] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[1.5, 1.5, 1, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
      
      {/* Rear Left */}
      <group position={[-carWidth / 2 - 1, -carHeight/2 + 1.5, -carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[2] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[1.5, 1.5, 1, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
      
      {/* Rear Right */}
      <group position={[carWidth / 2 + 1, -carHeight/2 + 1.5, -carLength / 3]}>
        <mesh
          ref={el => wheelsRef.current[3] = el}
          rotation={[0, 0, Math.PI / 2]}
        >
          <cylinderGeometry args={[1.5, 1.5, 1, 16]} />
          <meshStandardMaterial color="#111" />
        </mesh>
      </group>
    </group>
  )
}
