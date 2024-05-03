# TrafficModeling

# Project Description

Unity used for modeling traffic. Utilizing ML to make a pathfinder algorithm.

We will be utilizing LaTeX to write the documentation for this project.

## Tech Stack

Unity
Python
Blender
[TomTom API](https://developer.tomtom.com/)

>[!IMPORTANT]
> To access python venv in windows use: ```./API/Scripts/activate``` from the root folder

### API choices for TOMTOM

- Version number 4 selected for accurate data (current version used by TomTom) [See Here:](https://developer.tomtom.com/traffic-api/documentation/traffic-flow/raster-flow-tiles)
- Relative speed selected (to show relevant speed according to the area)
- Saves images to the folder ```./API/Images```

# Folder Structure

See the folder structure below:
```
.
├── API
│
├── BlenderModels
│
├── FinalPaper
│   ├── LaTeXFinalPaperFiles
│   │   └── Images
│   └── Sample
│       └── Images
│
├── ProjectUpdates
│   ├── Images
│   ├── Update1
│   ├── Update2
│   └── Update3
│
├── RelatedWorks
│
├── unity
│
└── Readme.md
```

# Using API

Assuming the user is in the TrafficModeling directory:

From the cmd line, type: 

```./API/TomTom.py LATITUDE LONGITUDE ZOOM STYLE --demo --verbose```

There are 2 optional flags:

1) demo: Which runs through a series of tests to showcase the program's capabilities

2) verbose: Explicitly states the step by step process of what the program is doing as it is doing it.