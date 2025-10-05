# EffDirEditor

This project converts old MATLAB scripts (`WriteEffDir.m`, `IsolateEff.m`, etc.) for working with SimCity 4 EffDir files into Python.  
It also provides a way to build a **standalone EXE** so you can run the tool without needing Python installed.

## Features
- Read `.effdir` files
- Write `.effdir` files
- Isolate specific effects by name or index
- Cross-platform (Python), with Windows `.exe` build via GitHub Actions

## Usage
Once built, you can run:

## Build Instructions
If you want to build the `.exe` yourself:
1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Use PyInstaller:

Or use the provided **GitHub Action** which automatically builds the `.exe` in the cloud.

## Status
Work in progress — based on reverse-engineered MATLAB scripts.

# Effect Dir Editor v1.0

A tool to read, write, and isolate sections from `.effdir` files.

## Download
The latest build is available from the GitHub Actions artifacts:  
- Artifact name: **EffDirEditor-Package-v1.0.zip**  
- Inside, run: **Effect Dir Editor v1.0.exe**

## Features
- Read and write `.effdir` files
- Isolate and manipulate effects
- Portable EXE build for Windows

- # Effect Dir Editor v1.0

A Python-based EffDir file editor with isolation and writing capabilities.

## Version
v1.0

## Build
This app is automatically built on GitHub Actions into an artifact:
**EffDirEditor-Package-v1.0.zip**

