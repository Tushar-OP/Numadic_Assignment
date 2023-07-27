# Vehicle Asset Report API

The Vehicle Asset Report API is a Python script that generates an Excel report containing asset information for a given time period. The API processes vehicle trails data stored in CSV files and trip information from "Trip-Info.csv" to compute various metrics for each unique vehicle.

## Prerequisites

- Python 3.x
- Pandas library: `pip install pandas`
- Haversine library: `pip install haversine`
- FastAPI library: `pip install fastapi`

## Usage

1. Clone the repository or download the files from the GitHub repository.

2. Place the un-zipped folder NU-raw-location-dump.zip (data\NU-raw-location-dump\EOL-dump) and the Trip-Info.csv file in the "data" folder inside the project directory.
```bash
   data
   ├── Trip-Info.csv
   └── NU-raw-location-dump
      └── EOL-dump
         ├── BR01GF0281.csv
         └── ...
```

4. Open a terminal or command prompt and navigate to the project directory.

5. Run the FastAPI web API using the following command:

   ```bash
   uvicorn main:app --reload

1. The FastAPI server will start running at http://localhost:8000. You can access the API documentation at http://localhost:8000/docs or http://localhost:8000/redoc.

2. To generate the asset report, make a POST request to the /generate_report endpoint with the desired start and end times in epoch format as query parameters.

3. The API will process the data, compute metrics, and generate an Excel report named "report_<start_time>_<end_time>.xlsx" in the project directory.

4. Download and open the file using Microsoft Excel or any compatible spreadsheet software to view the asset report.
