import { useState, useEffect, useRef } from 'react'

export function useTelemetry(data, isPlaying = true, offset = 0) {
  const [telemetryData, setTelemetryData] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [lapTime, setLapTime] = useState(0)
  const startTimeRef = useRef(Date.now())
  
  useEffect(() => {
    if (!data) return
    
    // Check if data has telemetry array (real data) or points array (simulated)
    if (data.telemetry) {
      // Real telemetry data
      setTelemetryData(data.telemetry)
    } else if (data.points) {
      // Generate simulated telemetry from track points
      const telemetry = data.points.map((point, i) => {
        const nextPoint = data.points[(i + 1) % data.points.length]
        const dx = nextPoint[0] - point[0]
        const dz = nextPoint[2] - point[2]
        const distance = Math.sqrt(dx * dx + dz * dz)
        const speed = Math.max(60, Math.min(250, distance * 60 * 3.6))
        
        const rpm = Math.min(8000, speed * 50 + 2000)
        
        let gear = 1
        if (speed > 40) gear = 2
        if (speed > 80) gear = 3
        if (speed > 120) gear = 4
        if (speed > 160) gear = 5
        if (speed > 200) gear = 6
        
        const prevPoint = data.points[(i - 1 + data.points.length) % data.points.length]
        const angle1 = Math.atan2(point[2] - prevPoint[2], point[0] - prevPoint[0])
        const angle2 = Math.atan2(nextPoint[2] - point[2], nextPoint[0] - point[0])
        const steeringAngle = (angle2 - angle1) * 100
        
        return {
          position: point,
          speed,
          rpm,
          gear,
          steeringAngle
        }
      })
      
      setTelemetryData(telemetry)
    }
  }, [data])
  
  useEffect(() => {
    if (!isPlaying || !telemetryData) return
    
    const interval = setInterval(() => {
      setCurrentIndex(prev => {
        const next = prev >= telemetryData.length - 1 ? 0 : prev + 1
        if (next === 0) {
          startTimeRef.current = Date.now()
          setLapTime(0)
        } else {
          setLapTime((Date.now() - startTimeRef.current) / 1000)
        }
        return next
      })
    }, 50)
    
    return () => clearInterval(interval)
  }, [isPlaying, telemetryData])
  
  const currentTelemetry = telemetryData?.[currentIndex]
  const ghostIndex = (currentIndex + offset) % (telemetryData?.length || 1)
  const ghostTelemetry = offset !== 0 ? telemetryData?.[ghostIndex] : null
  
  return {
    currentTelemetry: offset === 0 ? currentTelemetry : ghostTelemetry,
    lapTime,
    progress: telemetryData ? currentIndex / telemetryData.length : 0
  }
}
