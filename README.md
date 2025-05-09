# Intelligent Parking Detection System

![System Architecture](https://github.com/user-attachments/assets/6833d7f4-44c0-4900-aeca-09d4be58ff15)

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
  - [Overview](#overview)
  - [Data Flow](#data-flow)
- [Technical Implementation](#technical-implementation)
  - [Components](#components)
- [Dashboard Features](#dashboard-features)
- [Performance](#performance)
- [Setup Instructions](#setup-instructions)
- [Future Improvements](#future-improvements)
- [License](#license)

## Introduction

This project develops an automated solution for real-time parking space detection using computer vision and IoT technologies. The system combines three main components:

1. Camera image capture module
2. AI vehicle detection service
3. Visualization interface

All components are orchestrated by Node-RED, a visual programming platform designed for IoT applications.

## System Architecture

### Overview

The system uses a distributed architecture with interconnected modules communicating via MQTT protocol:

- Connected camera for image capture
- MQTT broker for message management
- YOLOv5-based prediction API
- Node-RED dashboard for visualization

### Data Flow

1. Camera captures parking space images at regular intervals
2. Images are encoded in base64 and published to MQTT topic
3. Node-RED receives images and forwards them to prediction API
4. YOLOv5 model analyzes images for vehicle detection
5. Analysis results are returned to Node-RED
6. Node-RED updates user interface with current parking status

## Technical Implementation

### Components

#### 1. MQTT Publisher (Image Capture)
- Uses OpenCV to access camera
- Captures images at regular intervals
- Resizes images for optimal performance
- Encodes images to base64 with URI prefix
- Publishes to "camera/frame" MQTT topic
- Includes rate limiting delay

#### 2. Vehicle Detection API
- FastAPI endpoint with YOLOv5 model
- Processes images and detects vehicles
- Returns "occupied" or "empty" status
- Key features:
  - Loads pre-trained YOLOv5 model
  - Exposes `/predict` endpoint
  - Handles image preprocessing
  - Performs object detection
  - Returns simple status

#### 3. Distance Sensor Simulator
- Simulates ultrasonic distance sensor
- Provides complementary data to camera
- Enhances reliability in challenging conditions

#### 4. Node-RED Orchestration
Key nodes:
- MQTT Input: Subscribes to "camera/frame"
- Base64 to Buffer: Converts received data
- Prepare HTTP Payload: Formats for API
- Enhanced Data Fusion: Combines camera and sensor data

Data fusion features:
- Checks data freshness (30s threshold)
- Implements advanced fusion logic
- Maintains parking statistics
- Keeps event history
- Determines UI update needs

## Dashboard Features

![Dashboard UI](https://github.com/user-attachments/assets/a6fd0139-538f-4882-84a1-600e84f891b5)

The Node-RED dashboard provides:

- **Live Camera View**
  - Real-time video feed
  - Visual detection indicators
  - Status overlay (VACANT/OCCUPIED)

- **Distance Gauge**
  - Ultrasonic sensor readings
  - Visual distance representation

- **Status Indicator**
  - Clear color coding (Green=Vacant, Red=Occupied)
  - Immediate visual feedback

- **Parking Statistics**
  - Total vehicles detected
  - Average parking duration
  - Utilization trends

- **Recent Activity**
  - Timestamped events
  - Duration information
  - Historical record

## Performance

| Metric               | Value                     |
|----------------------|---------------------------|
| Detection Accuracy   | ~95% (normal conditions)  |
| Processing Speed     | ~2 images/second          |
| Reliability          | Enhanced by sensor fusion |

Key advantages:
- Robust performance across lighting conditions
- Low latency suitable for parking monitoring
- Reduced false positives through multi-sensor approach

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js and Node-RED
- Mosquitto MQTT broker
- YOLOv5 weights file

### Installation
1. Clone repository:
   ```bash
   git clone https://github.com/your-repo/parking-detection.git
   cd parking-detection
   ```
2. Install Python dependencies:
  ```bash
    pip install -r requirements.txt
  ```  
3. Set up MQTT broker:
  ```bash
    sudo apt install mosquitto mosquitto-clients
    mosquitto -v
  ```
4. Launch services:
  ```bash
    # Start detection API
    uvicorn api:app --reload
    
    # Run camera publisher
    python camera_publisher.py
    
    # Start Node-RED
    node-red
  ```  
5. Import Node-RED flow:
   -Access Node-RED UI (typically http://localhost:1880)
   -Import parking_flow.json
