#  Drowsiness Detection Application Using Machine Learning
#### A real-time, machine-learning powered safety system that detects driver fatigue using EAR (Eye Aspect Ratio) and MAR (Mouth Aspect Ratio) — built with OpenCV, Dlib & ML.

##  Table of Contents
- Project Overview

- Objective

- System Architecture

- Tech Stack

- Market Research Summary

- How It Works

- User Interface

- Results & Insights

- Conclusion

##  Project Overview
Drowsiness while driving is a leading cause of road accidents worldwide.
This project presents a real-time, non-invasive Drowsiness Detection Application that uses:

- Haar Cascade for face detection
- Dlib Landmark Predictor for eye & mouth detection
- EAR (Eye Aspect Ratio) for blink & eye-closure detection
- MAR (Mouth Aspect Ratio) for yawning detection
- Machine Learning for improved accuracy under lighting & angle variations

## System Architecture
<p align="center">
  <img src="https://raw.githubusercontent.com/Cojaya/Drowsiness_Detection_Application/main/System_Architecture.png" width="200">
</p>

## Tech Stack
| Component                      | Technology Used                                  |
| ------------------------------ | ------------------------------------------------ |
| **Programming Language**       | Python                                           |
| **Face Detection**             | Haar Cascade (OpenCV)                            |
| **Facial Landmark Detection**  | Dlib (68-point model)                            |
| **Feature Extraction**         | EAR (Eye Aspect Ratio), MAR (Mouth Aspect Ratio) |
| **Drowsiness Detection Logic** | Rule-Based ML Model (Threshold Classification)   |
| **Realtime Processing**        | OpenCV VideoCapture                              |
| **Alert System**               | Audio + Visual alerts                            |
| **Hardware**                   | Laptop/phone camera                              |

## Market Research Summary
### Primary Survey
- 66.7% experience drowsiness during long tasks
- 38.9% faced near-miss accidents
- Most common countermeasures:
  - Coffee 
  - Short naps
  - Alarms

### Secondary Research
- 77.8% trust AI-based monitoring solutions
- 66.7% prefer predictive alert systems over reactive ones
- Market demand is rising in:
  - Logistics & Transportation
  - Ride-hailing companies
  - Personal vehicle owners
  - Fleet safety management

## How It Works
### Step-by-Step Workflow
 #### 1. Start Application
 User launches the app and camera activates automatically.
 #### 2. Capture Video
 Continuous frame capture begins.
 #### 3. Face Detection
 Haar Cascade identifies the driver's face.
 #### 4. Facial Landmark Detection
 Dlib extracts eye & mouth coordinates.
#### 5. EAR & MAR Calculation
Used to detect blinking and yawning.
#### 6. Drowsiness Decision
If EAR ↓ threshold or MAR ↑ threshold → Drowsiness detected.
#### 7. Trigger Alert
System immediately plays an alarm or displays a warning.
#### 8. Continuous Monitoring
Loop continues until user stops the app.
#### 9. Stop Application
Monitoring ends manually.
 
## Results & Insights
- 88% of users experience drowsiness during long tasks
  
- Real-time alerts help prevent micro-sleep
  
- System is more comfortable than EEG headsets
  
- Predictive detection reduces risk of road accidents
  
- Suitable for:
  - Students
  - Long-distance drivers
  - Corporate employees
  - Fleet management companies

## Conclusion
This project delivers a reliable, efficient, and cost-effective AI solution for real-time drowsiness detection. By combining computer vision + machine learning, it enhances safety for drivers, students, and working professionals.

It sets the foundation for future smart driver-assistance systems and real-world deployment in transportation and workplace environments.

