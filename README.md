# Vehicle Asset Report API

The Vehicle Asset Report API is a Python script that generates an Excel report containing asset information for a given time period. The API processes vehicle trails data stored in CSV files and trip information from "Trip-Info.csv" to compute various metrics for each unique vehicle.

## Prerequisites

- Python 3.x
- Pandas library: `pip install pandas`
- Haversine library: `pip install haversine`
- FastAPI library: `pip install fastapi`

## Usage

1. Clone the repository or download the files from the GitHub repository.

2. Place the zipped folder (NU-raw-location-dump.zip) and the Trip-Info.csv file in the "data" folder inside the project directory.

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the FastAPI web API using the following command:

   ```bash
   uvicorn main:app --reload
