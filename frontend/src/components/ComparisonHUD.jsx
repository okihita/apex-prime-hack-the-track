export default function ComparisonHUD({ playerLapTime, ghostLapTime, timeDelta }) {
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(3)
    return `${mins}:${secs.padStart(6, '0')}`
  }
  
  const deltaColor = timeDelta > 0 ? '#f00' : '#0f0'
  const deltaSign = timeDelta > 0 ? '+' : ''
  
  return (
    <div style={{
      position: 'absolute',
      top: 80,
      left: 20,
      fontFamily: 'monospace',
      color: '#fff',
      background: 'rgba(0,0,0,0.8)',
      padding: '15px',
      borderRadius: '10px',
      border: '2px solid #00ffff'
    }}>
      <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '10px', color: '#00ffff' }}>
        GHOST COMPARISON
      </div>
      
      <div style={{ display: 'flex', gap: '20px', fontSize: '14px' }}>
        <div>
          <div style={{ opacity: 0.7, marginBottom: '5px' }}>Your Time</div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#fff' }}>
            {formatTime(playerLapTime)}
          </div>
        </div>
        
        <div>
          <div style={{ opacity: 0.7, marginBottom: '5px' }}>Ghost Time</div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#00ffff' }}>
            {formatTime(ghostLapTime)}
          </div>
        </div>
        
        <div>
          <div style={{ opacity: 0.7, marginBottom: '5px' }}>Delta</div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: deltaColor }}>
            {deltaSign}{timeDelta.toFixed(3)}s
          </div>
        </div>
      </div>
    </div>
  )
}
