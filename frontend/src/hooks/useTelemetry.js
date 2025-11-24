import { useState, useEffect } from 'react'

export function useTelemetry(trackData) {
  const [telemetryData, setTelemetryData] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(true)
  
  useEffect(() => {
    if (!trackData || !trackData.points) return
    
    // Generate simple telemetry data for demo
    // In real implementation, this would load from CSV
    const telemetry = trackData.points.map((point, i) => ({
      position: point,
      speed: 100 + Math.sin(i / 10) * 30, // Varying speed
      steeringAngle: Math.sin(i / 5) * 200, // Varying steering
      timestamp: i * 0.1
    }))
    
    setTelemetryData(telemetry)
  }, [trackData])
  
  useEffect(() => {
    if (!isPlaying || !telemetryData) return
    
    const interval = setInterval(() => {
      setCurrentIndex(prev => {
        if (prev >= telemetryData.length - 1) return 0
        return prev + 1
      })
    }, 50) // Update every 50ms (20 FPS for telemetry)
    
    return () => clearInterval(interval)
  }, [isPlaying, telemetryData])
  
  const currentTelemetry = telemetryData?.[currentIndex]
  
  return {
    currentTelemetry,
    isPlaying,
    setIsPlaying,
    progress: telemetryData ? currentIndex / telemetryData.length : 0
  }
}
