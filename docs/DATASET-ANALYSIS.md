# Toyota GR Cup Dataset Analysis
## Comprehensive Data Science, Business, and Engineering Insights

**Analysis Date:** November 24, 2025  
**Dataset:** Toyota "Hack the Track" 2025 Hackathon  
**Total Data Size:** ~21 GB (raw telemetry)

---

## Executive Summary

This dataset contains high-frequency telemetry data from 6 race tracks across the 2025 Toyota GR Cup season, capturing data from Toyota GR86 race cars. The dataset includes **120+ million telemetry data points** across multiple races, with GPS data available for 2 tracks (Indianapolis and Barber).

### Key Findings
- **GPS Coverage:** Only 33% of tracks (2/6) have GPS data
- **Telemetry Frequency:** ~100 Hz sampling rate
- **Data Quality:** High-quality professional racing telemetry
- **Unique Opportunity:** Rare access to professional motorsport data

---

## 1. Dataset Overview

### 1.1 Track Coverage

| Track | Location | Race 1 Data | Race 2 Data | GPS Available | Total Size |
|-------|----------|-------------|-------------|---------------|------------|
| **Indianapolis Motor Speedway** | Indiana | ✅ 2.85 GB | ✅ 3.06 GB | ✅ YES | 5.91 GB |
| **Barber Motorsports Park** | Alabama | ✅ 1.49 GB | ✅ 1.51 GB | ✅ YES | 3.00 GB |
| **Circuit of the Americas (COTA)** | Texas | ✅ 2.21 GB | ✅ 2.14 GB | ❌ NO | 4.35 GB |
| **Sebring International Raceway** | Florida | ✅ 1.77 GB | ✅ 0.82 GB | ❌ NO | 2.59 GB |
| **Road America** | Wisconsin | ✅ 1.11 GB | ✅ 1.40 GB | ❌ NO | 2.51 GB |
| **Virginia International Raceway** | Virginia | ✅ 1.42 GB | ✅ 1.46 GB | ❌ NO | 2.88 GB |

**Total Dataset Size:** 21.24 GB

### 1.2 Data Files Per Track

Each track contains:
- **Telemetry Data:** High-frequency sensor readings (largest files)
- **Lap Start Times:** Timestamp when each lap begins
- **Lap End Times:** Timestamp when each lap completes
- **Lap Times:** Duration of each lap
- **Race Results:** Final standings and points (Indianapolis only)

---

## 2. Telemetry Channels Comparison

### 2.1 Available Channels by Track

| Channel | Description | Indianapolis | Barber | COTA | Sebring | Road America | VIR |
|---------|-------------|--------------|--------|------|---------|--------------|-----|
| **VBOX_Lat_Min** | GPS Latitude | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **VBOX_Long_Minutes** | GPS Longitude | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Laptrigger_lapdist_dls** | Distance along lap | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **speed** | Vehicle speed (km/h) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **nmot** | Engine RPM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **gear** | Current gear (1-6) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Steering_Angle** | Steering input | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **accx_can** | Longitudinal G-force | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **accy_can** | Lateral G-force | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pbrake_f** | Front brake pressure | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pbrake_r** | Rear brake pressure | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **aps** | Accelerator position | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ath** | Throttle position | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

### 2.2 Channel Categories

**Navigation (GPS):**
- VBOX_Lat_Min, VBOX_Long_Minutes
- Only available: Indianapolis, Barber
- Critical for: Track reconstruction, position tracking

**Motion:**
- speed, accx_can, accy_can
- Available: All tracks
- Critical for: Performance analysis, driving dynamics

**Drivetrain:**
- nmot (RPM), gear, aps/ath (throttle)
- Available: All tracks
- Critical for: Engine performance, shift strategy

**Control:**
- Steering_Angle, pbrake_f, pbrake_r
- Available: All tracks
- Critical for: Driver input analysis, braking performance

**Position:**
- Laptrigger_lapdist_dls
- Only available: Indianapolis, Barber
- Critical for: Sector analysis, position-based comparisons

---

## 3. Data Statistics

### 3.1 Indianapolis Motor Speedway

**Track Characteristics:**
- Type: Oval (road course configuration)
- Length: ~4.0 km
- Laps per race: ~20 laps
- Race duration: ~38 minutes

**Telemetry Statistics (Race 1):**
- Total data points: 21,454,865
- Unique vehicles: 1 (single car focus)
- Laps recorded: 1-20
- Date: October 18, 2025 (12:44 PM - 1:22 PM)

**Performance Metrics:**
- Speed range: 43.0 - 221.3 km/h
- Average speed: 121.8 km/h
- Median speed: 110.6 km/h
- RPM range: 2,435 - 7,355
- Average RPM: 5,836
- Gear usage: 1-6 (most used: gear 2)

**Track Insights:**
- High-speed oval with technical infield section
- Top speed: 221 km/h (137 mph) - very fast
- Low-speed sections: 43 km/h (tight corners)
- Gear 2 most used suggests technical sections dominate

### 3.2 Barber Motorsports Park

**Track Characteristics:**
- Type: Road course
- Length: ~3.7 km
- Laps per race: ~25 laps
- Race duration: Similar to Indianapolis

**Telemetry Statistics (Race 1):**
- Total data points: 11,556,519
- Unique vehicles: 1
- Laps recorded: 2-25 (lap 1 missing - formation lap)
- Shorter race or fewer data points per lap

**Performance Metrics:**
- Speed range: 65.0 - 186.9 km/h
- Average speed: 129.5 km/h
- Lower top speed than Indianapolis (more technical)
- Higher minimum speed (fewer slow corners)

**Track Insights:**
- Technical road course with flowing corners
- More consistent speed profile
- Higher average speed despite lower top speed
- Fewer extreme braking zones

