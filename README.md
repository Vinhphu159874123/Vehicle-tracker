# Vehicle Counting System

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)
![Ultralytics YOLO](https://img.shields.io/badge/Ultralytics%20YOLO-AGPL--3.0-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Apache--2.0-blue)
![Tracker](https://img.shields.io/badge/Tracking-ByteTrack-5C4EE5)


## System Preview
The figure below shows the current pipeline output, including ROI overlay, line-crossing boundary, object tracks, class labels, confidence, and directional counters.

![Vehicle counting pipeline preview](Demo/Screenshot%202026-03-27%20235833.png)

## Table of Contents
- [Problem Statement and Practical Relevance](#problem-statement-and-practical-relevance)
- [Overview](#1-overview)
- [Third-Party License Notice](#third-party-license-notice)
- [Research Context and Scope](#2-research-context-and-scope)
- [System Architecture](#3-system-architecture)
- [Repository Structure](#4-repository-structure)
- [Data Flow](#5-data-flow)
- [Installation](#6-installation)
- [Configuration](#7-configuration)
- [Running Procedure](#8-running-procedure)
- [Event and Storage Format](#9-event-and-storage-format)
- [Practical Tuning Guidelines](#10-practical-tuning-guidelines)
- [Known Limitations](#11-known-limitations)
- [Reproducibility Notes](#12-reproducibility-notes)
- [Conclusion](#13-conclusion)

## Problem Statement and Practical Relevance
In many operational sites (for example, access lanes, workshop yards, and loading areas), manual counting is unreliable when vehicles stop, reverse, or rotate near a gate boundary. This project addresses that issue by providing an automated direction-aware counting pipeline with logging support for operational monitoring.

The configured classes target practical mixed-traffic scenarios frequently observed in Vietnam:
- motorbike
- small_cart
- three_wheeler

This scope is intended for site-specific deployment after local calibration and model adaptation, rather than a universal model for all traffic conditions.

## 1. Overview
This project implements a video-based vehicle counting pipeline for estimating inbound and outbound traffic in a predefined region. The system combines object detection, multi-object tracking, region-of-interest filtering, and line-crossing logic to produce directional counts (IN and OUT) and event logs.

The primary engineering objective is to deliver a deployable counting workflow for practical surveillance environments, where vehicles may stop, reverse, or move in dense formations near the counting line.

The current implementation is designed for three target classes:
- motorbike
- small_cart
- three_wheeler

Application context:
- The selected classes are aligned with mixed-traffic scenes frequently observed in Vietnam, including informal utility vehicles such as small carts and three-wheelers.
- The system is intended for site-specific deployment (for example, yards, access roads, and loading zones) after local calibration of ROI, line geometry, and model weights.

Model note:
- YOLO backbones from Ultralytics (for example, yolov8n.pt or yolov8s.pt) are pretrained on COCO.
- The project can load a custom file such as best.pt, which is typically obtained by fine-tuning from a pretrained YOLO checkpoint on local labeled data.

## Third-Party License Notice
- Ultralytics YOLO codebase and package are distributed under AGPL-3.0 (or commercial terms from Ultralytics).
- OpenCV (cv2) is distributed under Apache-2.0 for OpenCV 4.x.
- Additional transitive dependencies may have their own licenses; users should review the dependency metadata in the runtime environment before production distribution.

## 2. Research Context and Scope
The system targets practical deployment scenarios where camera viewpoints are oblique, object scales vary, and motion can be intermittent near the counting line. To improve counting stability, the pipeline includes multiple anti-noise mechanisms:
- confidence and area filtering at detection time
- track age and displacement validation before counting
- per-track cooldown
- cross-track duplicate suppression in a short temporal-spatial window
- re-arm gating, requiring a tracked object to move sufficiently far from the line before it can be counted again

In operational terms, this design addresses common field issues such as repeated counting when a vehicle rotates near the boundary, fragmented tracks in crowded scenes, and short-term ID instability under occlusion.

## 3. System Architecture
The pipeline is organized into the following modules:

1. detector.py
   - Loads YOLO model weights.
   - Performs frame-level inference.
   - Filters detections by class, confidence, and minimum box area.
   - Applies ROI filtering via centroid-in-polygon testing.

2. tracker.py
   - Wraps ByteTrack from the supervision library.
   - Associates detections across frames and assigns persistent track IDs.
   - Propagates class metadata for each active track.

3. counter.py
   - Monitors centroid trajectories against a counting line.
   - Determines crossing direction (IN or OUT).
   - Applies anti-duplicate constraints before accepting an event.

4. logger.py
   - Persists events to CSV and SQLite.
   - Stores periodic summary records.

5. utils/visualization.py
   - Renders ROI, counting line, detections/tracks, counters, and FPS.

6. main.py
   - Orchestrates video capture and all processing stages.

7. utils/roi_selector.py
   - Provides interactive ROI and counting-line selection.

## 4. Repository Structure

```text
Car tracker/
├── app.py
├── config.py
├── counter.py
├── detector.py
├── logger.py
├── main.py
├── tracker.py
├── requirements.txt
├── data/
├── models/
├── static/
├── templates/
└── utils/
    ├── roi_selector.py
    └── visualization.py
```

## 5. Data Flow
1. Read frame from video file or RTSP stream.
2. Resize to configured display resolution.
3. Detect candidate objects using YOLO.
4. Retain only configured classes and valid detections.
5. Filter detections by ROI.
6. Update tracker and obtain stable track IDs.
7. Evaluate line crossing and direction.
8. Apply anti-duplicate rules.
9. Update counters and persist events.
10. Render visualization for monitoring.

## 6. Installation

### 6.1 Environment
- Python 3.9+
- Windows, Linux, or macOS
- GPU is recommended for real-time throughput

### 6.2 Dependencies

```bash
pip install -r requirements.txt
```

## 7. Configuration
All runtime parameters are centralized in config.py.

Important groups of parameters:
- Input source: VIDEO_SOURCE
- Model and detection: YOLO_MODEL, CONFIDENCE_THRESHOLD, MIN_BOX_AREA
- Class filtering: TARGET_CLASS_NAMES
- Geometry: ROI_POLYGON, LINE_START, LINE_END
- Tracking: TRACK_THRESH, TRACK_BUFFER, MATCH_THRESH
- Counting robustness: MIN_TRACK_AGE, MIN_DISPLACEMENT, COUNTING_COOLDOWN
- Duplicate suppression: DUPLICATE_EVENT_WINDOW, DUPLICATE_EVENT_DISTANCE

## 8. Running Procedure

### 8.1 Configure ROI and counting line

```bash
python utils/roi_selector.py
```

Use the interactive tool to define ROI and line geometry, then save to config.py.

### 8.2 Run offline processing

```bash
python main.py
```

Expected outputs:
- Real-time display window with ROI, line, boxes, labels, and counters
- Event logs in data/vehicle_log.csv
- SQLite records in data/logs.db

### 8.3 Optional web dashboard

```bash
python app.py
```

Then open:
- http://localhost:5000

## 9. Event and Storage Format

### 9.1 Event fields
Each accepted crossing event contains:
- timestamp
- direction
- track_id
- class_id
- class_name

### 9.2 SQLite tables
- events: per-crossing records
- summary: periodic aggregated counts

## 10. Practical Tuning Guidelines
For frequent double counting near the line:
- Increase COUNTING_COOLDOWN
- Increase MIN_TRACK_AGE
- Increase MIN_DISPLACEMENT
- Increase DUPLICATE_EVENT_WINDOW and DUPLICATE_EVENT_DISTANCE carefully

For missed detections:
- Decrease CONFIDENCE_THRESHOLD moderately
- Improve camera framing and object scale in ROI
- Retrain model with representative local data

For unstable tracking:
- Adjust TRACK_BUFFER and MATCH_THRESH
- Reduce detection noise via class and area filters

## 11. Known Limitations
- Accuracy depends strongly on camera angle, lighting, and class annotation quality.
- Occlusion and close object interactions can still cause ID switches.
- Generic pretrained weights may not represent local vehicle subtypes adequately.

## 12. Reproducibility Notes
To obtain reproducible experiments:
- Fix video source and ROI/line geometry.
- Keep configuration snapshots for each run.
- Record model version and thresholds with every evaluation.

## 13. Conclusion
This codebase provides a practical and extensible baseline for directional vehicle counting under real-world surveillance conditions. With calibrated geometry, scenario-specific thresholds, and local model fine-tuning, the system can support reliable monitoring workflows in mixed-traffic environments and produce auditable traffic logs for operational decision-making.
