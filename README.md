
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

#### **Important Note**
- **Database Paths**: Make sure to **update the database paths** in both `dasher.py` and `fetcher.py` to the present working directory where these files are located.

### Data Preprocessing (`fetcher.py`)

- **Data Cleaning**: Automatic data cleaning to handle missing or incomplete data.
- **Metrics**: Calculates additional metrics like daily returns and moving averages for enhanced investment decisions.

#### **Warning**
- **Database Corruption**: Delete the `stock_data.db` file every time before running `fetcher.py` if it exists. Failing to do so can corrupt the database.

### Data Visualization (Frontend - `dasher.py`)

- **Framework**: Uses Dash for backend logic and interactivity.
- **Charts**: Line charts visualize historical stock price trends.
- **Interactivity**: Features like dropdowns and sliders enable users to select different stocks and timeframes.
- **Additional Visuals**: Includes a heatmap for stock correlation and a table for key performance metrics.

### Dashboard Design

- **UI/UX**: Designed to be user-friendly and visually appealing.
- **Styling**: Custom styling applied through an external CSS file (`styles.css`).

## Getting Started

### Prerequisites

- Python 3.x
- SQLite

### Installation and Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/StockMarketDashboard.git
    ```

2. **Navigate to the Project Folder**
    ```bash
    cd StockMarketDashboard
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Data Fetcher Script (Backend)**
    ```bash
    python fetcher.py
    ```

#### **Emphasis**
- **Run `fetcher.py` Before `dasher.py`**: It's **mandatory** to run `fetcher.py` at least once before running `dasher.py` to populate the SQLite database.

5. **Run Dash Application (Frontend)**
    ```bash
    python dasher.py
    ```

### Usage

Navigate to `http://127.0.0.1:8050/` in your web browser to view and interact with the dashboard.

---

Created by Anubhab Dey
Email: anubhabdey2017@gmail.com
