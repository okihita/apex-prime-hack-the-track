import { useState, useEffect } from 'react'

export function useTelemetry(trackData, isPlaying = true) {
  const [telemetryData, setTelemetryData] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  
  useEffect(() => {
    if (!trackData || !trackData.points) return
    
    console.log('Generating telemetry for', trackData.points.length, 'points')
    
    // Generate simple telemetry data for demo
    const telemetry = trackData.points.map((point, i) => ({
      position: point,
      speed: 100 + Math.sin(i / 10) * 30,
      steeringAngle: Math.sin(i / 5) * 200,
      timestamp: i * 0.1
    }))
    
    setTelemetryData(telemetry)
    console.log('Telemetry generated:', telemetry[0])
  }, [trackData])
  
  useEffect(() => {
    if (!isPlaying || !telemetryData) return
    
    const interval = setInterval(() => {
      setCurrentIndex(prev => {
        const next = prev >= telemetryData.length - 1 ? 0 : prev + 1
        return next
      })
    }, 50)
    
    return () => clearInterval(interval)
  }, [isPlaying, telemetryData])
  
  const currentTelemetry = telemetryData?.[currentIndex]
  
  return {
    currentTelemetry,
    progress: telemetryData ? currentIndex / telemetryData.length : 0
  }
}
