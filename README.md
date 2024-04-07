
# Stock Market Data Visualization Dashboard

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)

## Overview

The Stock Market Data Visualization Dashboard is an interactive platform developed to enable users to explore and analyze the historical performance of selected stocks. This project is segmented into a frontend and a backend, both developed using Python. Dash serves as the frontend framework, while SQLite is used for data storage.

## Features

### Data Collection and Database Integration (Backend - `fetcher.py`)

- **API Source**: Utilizes the Alpha Vantage API for fetching historical stock data.
- **Database**: Employs SQLite for data storage, ensuring quick and efficient retrieval.

### Data Preprocessing (`fetcher.py`)

- **Data Cleaning**: Automatic data cleaning to handle missing or incomplete data.
- **Metrics**: Calculates additional metrics like daily returns and moving averages for enhanced investment decisions.

### Data Visualization (Frontend - `dasher.py`)

- **Framework**: Uses Dash for backend logic and interactivity.
- **Charts**: Line charts visualize historical stock price trends.
- **Interactivity**: Features like dropdowns and sliders enable users to select different stocks and timeframes.
- **Additional Visuals**: Includes a heatmap for stock correlation.

## Getting Started

### Prerequisites

- Python 3.9.x

### Installation and Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Anubhab-Dey/Stock-Market-Data-Visualization-Dashboard.git
    ```

2. **Navigate to the Project Folder**

    ```bash
    cd Stock-Market-Data-Visualization-Dashboard
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Launcher Script**

    ```bash
    python launcher.py
    ```

### Usage

Navigate to `http://127.0.0.1:8050/` in your web browser to view and interact with the dashboard.

---

Created by Anubhab Dey
Email: <anubhabdey2017@gmail.com>
