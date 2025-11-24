export default function GhostCar({ position, rotation, speed, steeringAngle }) {
  if (!position) return null
  
  return (
    <group position={position}>
      {/* Car body - semi-transparent */}
      <mesh position={[0, 1, 0]} castShadow>
        <boxGeometry args={[4, 2, 8]} />
        <meshStandardMaterial 
          color="#00ffff" 
          transparent 
          opacity={0.3}
          emissive="#00ffff"
          emissiveIntensity={0.5}
        />
      </mesh>
      
      {/* Wheels */}
      {[
        [-2, 0.5, 3],
        [2, 0.5, 3],
        [-2, 0.5, -3],
        [2, 0.5, -3]
      ].map((pos, i) => (
        <mesh key={i} position={pos} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.8, 0.8, 0.5, 16]} />
          <meshStandardMaterial 
            color="#00ffff" 
            transparent 
            opacity={0.3}
          />
        </mesh>
      ))}
    </group>
  )
}
