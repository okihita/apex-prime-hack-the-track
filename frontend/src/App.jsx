import { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Grid, Sky } from '@react-three/drei'
import Track from './components/Track'

function App() {
  const [trackData, setTrackData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    // Load track data
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
        {/* Lighting */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[100, 100, 50]} intensity={1} />
        
        {/* Sky */}
        <Sky sunPosition={[100, 20, 100]} />
        
        {/* Track */}
        <Track trackData={trackData} />
        
        {/* Ground grid */}
        <Grid 
          args={[2000, 2000]} 
          cellSize={50} 
          cellColor="#444" 
          sectionColor="#666"
          fadeDistance={1500}
        />
        
        {/* Camera controls */}
        <OrbitControls 
          enableDamping
          dampingFactor={0.05}
          minDistance={100}
          maxDistance={2000}
        />
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
        <div><strong>Apex Prime - Phase 1</strong></div>
        <div>Track: {trackData?.name}</div>
        <div>Points: {trackData?.points?.length}</div>
        <div style={{ marginTop: '10px', fontSize: '12px', opacity: 0.7 }}>
          Mouse: Orbit | Scroll: Zoom
        </div>
      </div>
    </div>
  )
}

export default App
