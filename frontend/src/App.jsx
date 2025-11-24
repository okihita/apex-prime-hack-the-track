import { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Grid } from '@react-three/drei'
import Track from './components/Track'
import Minimap from './components/Minimap'

function Scene({ trackData, modelPath }) {
  return (
    <>
      <ambientLight intensity={0.4} />
      <directionalLight position={[100, 200, 100]} intensity={1.2} />
      <directionalLight position={[-100, 100, -100]} intensity={0.3} />
      
      <Track trackData={trackData} modelPath={modelPath} />
      
      <Grid 
        args={[4000, 4000]} 
        cellSize={10} 
        cellColor="#333" 
        sectionColor="#555"
        fadeDistance={2000}
        infiniteGrid
      />
      
      <OrbitControls 
        enableDamping
        dampingFactor={0.05}
        minDistance={50}
        maxDistance={800}
      />
    </>
  )
}

const TRACKS = [
  { id: 'indianapolis', name: 'Indianapolis', real: true, length: '4.014 km', turns: 14, model: '/models/Indy.gltf' },
  { id: 'barber', name: 'Barber', real: true, length: '3.740 km', turns: 17, model: '/models/Barber.gltf' },
  { id: 'cota', name: 'COTA', real: false, length: '5.513 km', turns: 20, model: '/models/COTA.gltf' },
  { id: 'road-america', name: 'Road America', real: false, length: '6.515 km', turns: 14, model: '/models/Road-America.gltf' },
  { id: 'sebring', name: 'Sebring', real: false, length: '6.019 km', turns: 17, model: '/models/Sebring.gltf' },
  { id: 'vir', name: 'VIR', real: false, length: '5.263 km', turns: 18, model: '/models/VIR.gltf' },
  { id: 'sonoma', name: 'Sonoma', real: false, length: '4.052 km', turns: 12, model: '/models/Sonoma.gltf' },
]

function App() {
  const [trackData, setTrackData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedTrack, setSelectedTrack] = useState('indianapolis')
  
  useEffect(() => {
    const handleKeyDown = (e) => {
      const currentIndex = TRACKS.findIndex(t => t.id === selectedTrack)
      
      if (e.key === 'ArrowLeft') {
        const prevIndex = (currentIndex - 1 + TRACKS.length) % TRACKS.length
        setSelectedTrack(TRACKS[prevIndex].id)
      } else if (e.key === 'ArrowRight') {
        const nextIndex = (currentIndex + 1) % TRACKS.length
        setSelectedTrack(TRACKS[nextIndex].id)
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [selectedTrack])
  
  useEffect(() => {
    setLoading(true)
    fetch(`/tracks/${selectedTrack}.json`)
      .then(res => res.json())
      .then(track => {
        setTrackData(track)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [selectedTrack])
  
  if (loading) {
    return (
      <div style={{
        width: '100vw',
        height: '100vh',
        background: '#000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#fff',
        fontFamily: 'monospace',
        fontSize: '14px'
      }}>
        Loading...
      </div>
    )
  }
  
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000' }}>
      <Canvas camera={{ position: [0, 300, 400], fov: 60 }}>
        <Scene trackData={trackData} modelPath={TRACKS.find(t => t.id === selectedTrack)?.model} />
      </Canvas>
      
      {/* Minimap */}
      <Minimap modelPath={TRACKS.find(t => t.id === selectedTrack)?.model} />
      
      {/* Track Selector */}
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap',
        maxWidth: '400px'
      }}>
        {TRACKS.map(track => (
          <button
            key={track.id}
            onClick={() => setSelectedTrack(track.id)}
            style={{
              padding: '10px 20px',
              background: selectedTrack === track.id ? '#fff' : 'rgba(255,255,255,0.1)',
              color: selectedTrack === track.id ? '#000' : '#fff',
              border: '1px solid #fff',
              borderRadius: '4px',
              cursor: 'pointer',
              fontFamily: 'monospace',
              fontSize: '12px',
              fontWeight: selectedTrack === track.id ? 'bold' : 'normal',
              transition: 'all 0.2s',
              opacity: track.real ? 1 : 0.5
            }}
          >
            {track.name} {!track.real && '(mock)'}
          </button>
        ))}
      </div>
      
      {/* Track Info */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        color: '#fff',
        fontFamily: 'monospace',
        fontSize: '12px',
        background: 'rgba(0,0,0,0.7)',
        padding: '15px',
        borderRadius: '4px',
        border: '1px solid #333',
        minWidth: '200px'
      }}>
        <div style={{ marginBottom: '10px', opacity: 0.6, fontSize: '10px' }}>TRACK INFO</div>
        <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '10px' }}>
          {trackData?.name || 'Unknown'}
        </div>
        
        {(() => {
          const track = TRACKS.find(t => t.id === selectedTrack)
          return track ? (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span style={{ opacity: 0.6 }}>Length:</span>
                <span style={{ fontWeight: 'bold' }}>{track.length}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span style={{ opacity: 0.6 }}>Turns:</span>
                <span style={{ fontWeight: 'bold' }}>{track.turns}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span style={{ opacity: 0.6 }}>Data Points:</span>
                <span style={{ fontWeight: 'bold' }}>{trackData?.points?.length || 0}</span>
              </div>
              <div style={{ 
                marginTop: '10px', 
                padding: '5px 8px', 
                background: track.real ? 'rgba(0,255,0,0.1)' : 'rgba(255,255,0,0.1)',
                border: `1px solid ${track.real ? '#0f0' : '#ff0'}`,
                borderRadius: '3px',
                fontSize: '10px',
                textAlign: 'center'
              }}>
                {track.real ? '✓ REAL GPS DATA' : '⚠ MOCK DATA'}
              </div>
            </>
          ) : null
        })()}
      </div>
      
      {/* Controls Info */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        color: '#fff',
        fontFamily: 'monospace',
        fontSize: '11px',
        background: 'rgba(0,0,0,0.7)',
        padding: '10px 15px',
        borderRadius: '4px',
        border: '1px solid #333',
        opacity: 0.6
      }}>
        <div>⬅️ ➡️ Arrow Keys: Switch Tracks</div>
        <div>🖱️ Left Click + Drag: Rotate</div>
        <div>🖱️ Right Click + Drag: Pan</div>
        <div>🖱️ Scroll: Zoom</div>
      </div>
    </div>
  )
}

export default App
