# Campus Navigation and Fiber Deployment System

## Overview

Data Structures and Algorithms project for campus navigation with walking and shuttle edges, time-dependent shortest paths, and minimum-cost fiber deployment.

## Technical Highlights

- Custom MinHeap implementation with index-1 root.
- Time-dependent Dijkstra for shuttle waiting times.
- CSV map parsing and validation.
- Union-Find and Kruskal MST for fiber deployment.
- Automated tests and stress checks.

## Tech Stack

Python, Data Structures, Graphs, Dijkstra, Kruskal, Union-Find, CSV

## Results

- Official small-map route MainGate -> Library -> Lab reaches Lab at minute 6.
- MST test-case cost: 15.
- Large-map MST cost: 59.
- Stress review covered thousands of heap, route, and MST cases.

## How to Run or Review

- Run tests: `python test_campus_nav.py`.
- Run interactive menu: `python campus_nav.py`.

## Public Portfolio Notes

- This repository is prepared as a clean public GitHub portfolio version.
- Original course reports that contain student IDs or private details are not committed.
- The committed material focuses on source code, safe visuals, result screenshots, and a technical summary.
