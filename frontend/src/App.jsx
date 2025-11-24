import { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Grid, Sky } from '@react-three/drei'
import Track from './components/Track'
import Car from './components/Car'
import ChaseCamera from './components/ChaseCamera'
import { useTelemetry } from './hooks/useTelemetry'

function Scene({ trackData, cameraMode }) {
  const { currentTelemetry } = useTelemetry(trackData)
  
  // Calculate car rotation from position
  const getCarRotation = () => {
    if (!currentTelemetry || !currentTelemetry.position) return 0
    return (currentTelemetry.steeringAngle || 0) / 200
  }
  
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[100, 100, 50]} intensity={1} />
      
      {/* Sky */}
      <Sky sunPosition={[100, 20, 100]} />
      
      {/* Track */}
      <Track trackData={trackData} />
      
      {/* Car */}
      {currentTelemetry && (
        <Car
          position={currentTelemetry.position}
          rotation={getCarRotation()}
          speed={currentTelemetry.speed}
          steeringAngle={currentTelemetry.steeringAngle}
        />
      )}
      
      {/* Ground grid */}
      <Grid 
        args={[2000, 2000]} 
        cellSize={50} 
        cellColor="#444" 
        sectionColor="#666"
        fadeDistance={1500}
      />
      
      {/* Camera */}
      {cameraMode === 'chase' && currentTelemetry ? (
        <ChaseCamera target={currentTelemetry} />
      ) : (
        <OrbitControls 
          enableDamping
          dampingFactor={0.05}
          minDistance={100}
          maxDistance={2000}
        />
      )}
    </>
  )
}

function App() {
  const [trackData, setTrackData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isPlaying, setIsPlaying] = useState(true)
  const [cameraMode, setCameraMode] = useState('orbit')
  
  useEffect(() => {
    fetch('/tracks/indianapolis.json')
      .then(res => res.json())
      .then(data => {
        setTrackData(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])
  
  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: '#000',
        color: '#fff',
        fontFamily: 'monospace'
      }}>
        Loading track...
      </div>
    )
  }
  
  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: '#000',
        color: '#f00',
        fontFamily: 'monospace'
      }}>
        Error: {error}
      </div>
    )
  }
  
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000' }}>
      <Canvas camera={{ position: [0, 500, 500], fov: 60 }}>
        <Scene trackData={trackData} cameraMode={cameraMode} />
      </Canvas>
      
      {/* UI Overlay */}
      <div style={{
        position: 'absolute',
        top: 20,
        left: 20,
        color: '#fff',
        fontFamily: 'monospace',
        fontSize: '14px',
        background: 'rgba(0,0,0,0.7)',
        padding: '10px',
        borderRadius: '5px'
      }}>
        <div><strong>Apex Prime - Phase 2</strong></div>
        <div>Track: {trackData?.name}</div>
        <div>Status: {isPlaying ? 'Playing' : 'Paused'}</div>
        <div>Camera: {cameraMode}</div>
        <div style={{ marginTop: '10px', fontSize: '12px', opacity: 0.7 }}>
          Red car driving on track
        </div>
      </div>
      
      {/* Controls */}
      <div style={{
        position: 'absolute',
        bottom: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '10px'
      }}>
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          style={{
            padding: '10px 20px',
            background: 'rgba(0,0,0,0.8)',
            color: '#fff',
            border: '1px solid #fff',
            borderRadius: '5px',
            cursor: 'pointer',
            fontFamily: 'monospace'
          }}
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>
        <button
          onClick={() => setCameraMode(cameraMode === 'orbit' ? 'chase' : 'orbit')}
          style={{
            padding: '10px 20px',
            background: 'rgba(0,0,0,0.8)',
            color: '#fff',
            border: '1px solid #fff',
            borderRadius: '5px',
            cursor: 'pointer',
            fontFamily: 'monospace'
          }}
        >
          📷 {cameraMode === 'orbit' ? 'Chase Cam' : 'Orbit Cam'}
        </button>
      </div>
    </div>
  )
}

export default App
