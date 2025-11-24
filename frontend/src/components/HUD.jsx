export default function HUD({ telemetry, lapTime }) {
  if (!telemetry) return null
  
  const speed = Math.round(telemetry.speed || 0)
  const rpm = Math.round(telemetry.rpm || 0)
  const gear = telemetry.gear || 'N'
  
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(3)
    return `${mins}:${secs.padStart(6, '0')}`
  }
  
  return (
    <div style={{
      position: 'absolute',
      bottom: 80,
      left: '50%',
      transform: 'translateX(-50%)',
      display: 'flex',
      gap: '20px',
      fontFamily: 'monospace',
      color: '#fff'
    }}>
      {/* Speed */}
      <div style={{
        background: 'rgba(0,0,0,0.8)',
        padding: '15px 25px',
        borderRadius: '10px',
        border: '2px solid #fff',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '48px', fontWeight: 'bold', lineHeight: '1' }}>
          {speed}
        </div>
        <div style={{ fontSize: '14px', opacity: 0.7, marginTop: '5px' }}>
          KM/H
        </div>
      </div>
      
      {/* RPM */}
      <div style={{
        background: 'rgba(0,0,0,0.8)',
        padding: '15px 25px',
        borderRadius: '10px',
        border: '2px solid #fff',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '48px', fontWeight: 'bold', lineHeight: '1' }}>
          {rpm}
        </div>
        <div style={{ fontSize: '14px', opacity: 0.7, marginTop: '5px' }}>
          RPM
        </div>
      </div>
      
      {/* Gear */}
      <div style={{
        background: 'rgba(0,0,0,0.8)',
        padding: '15px 25px',
        borderRadius: '10px',
        border: '2px solid #0f0',
        textAlign: 'center',
        minWidth: '80px'
      }}>
        <div style={{ fontSize: '48px', fontWeight: 'bold', lineHeight: '1', color: '#0f0' }}>
          {gear}
        </div>
        <div style={{ fontSize: '14px', opacity: 0.7, marginTop: '5px' }}>
          GEAR
        </div>
      </div>
      
      {/* Lap Time */}
      <div style={{
        background: 'rgba(0,0,0,0.8)',
        padding: '15px 25px',
        borderRadius: '10px',
        border: '2px solid #f00',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '32px', fontWeight: 'bold', lineHeight: '1', color: '#f00' }}>
          {formatTime(lapTime)}
        </div>
        <div style={{ fontSize: '14px', opacity: 0.7, marginTop: '5px' }}>
          LAP TIME
        </div>
      </div>
    </div>
  )
}
