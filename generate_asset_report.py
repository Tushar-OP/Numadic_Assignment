import pandas as pd
from haversine import haversine


# Function to calculate haversine distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return haversine((lat1, lon1), (lat2, lon2))

# Function to generate the asset report
def generate_asset_report(start_time, end_time):
    # Load data from the zipped folder and Trip-Info.csv
    # Assuming the zipped folder is already extracted and its contents are in a 'data' folder
    data_folder = 'data/'
    vehicle_data_folder = 'data/NU-raw-location-dump/EOL-dump/'

    # Define the data types for each column in the vehicle trails CSV files
    vehicle_trails_dtypes = {
        'fk_asset_id': str,
        'lic_plate_no': str,
        'lat': float,
        'lon': float,
        'lname': str,
        'tis': int,
        'spd': float,
        'harsh_acceleration': bool,
        'hbk': bool,
        'osf': bool
    }

    # Define the data types for the Trip-Info.csv file
    trip_info_dtypes = {
        'trip_id': str,
        'transporter_name': str,
        'quantity': int,
        'vehicle_number': str,
        'date_time': str
    }

    # Load trip info data
    try:
        trip_info = pd.read_csv(data_folder + 'Trip-Info.csv', dtype=trip_info_dtypes)
    except FileNotFoundError:
        return None
    
    # Convert the date_time column into epoch timestamp for better comparison
    trip_info['date_time'] = pd.to_datetime(trip_info['date_time'], format='%Y%m%d%H%M%S').apply(lambda x: int(x.timestamp()))

    # Filter trips based on start_time and end_time
    trip_info_filtered = trip_info[(trip_info['date_time'] >= start_time) & (trip_info['date_time'] <= end_time)]

    # Initialize a dictionary to store asset report data
    asset_report_data = {
        'License plate number': [],
        'Distance': [],
        'Number of Trips Completed': [],
        'Average Speed': [],
        'Transporter Name': [],
        'Number of Speed Violations': []
    }

    # Loop through each unique vehicle and compute the required metrics
    for vehicle_id in trip_info_filtered['vehicle_number'].unique():
        try:
            vehicle_data = pd.read_csv(vehicle_data_folder + vehicle_id + '.csv', dtype=vehicle_trails_dtypes)
        except FileNotFoundError:
            continue

        # Drop the first column as it is an index column
        vehicle_data = vehicle_data.drop(vehicle_data.columns[0], axis=1)

        # Filter vehicle trails based on start_time and end_time
        vehicle_data_filtered = vehicle_data[(vehicle_data['tis'] >= start_time) & (vehicle_data['tis'] <= end_time)]

        if len(vehicle_data_filtered.index) == 0:
            continue
        
        vehicle_data_filtered = vehicle_data_filtered.sort_values(by = ['tis'], ascending=True)

        vehicle_data_filtered_for_distance = vehicle_data_filtered.dropna(subset=['lat','lon'])

        lat1, lon1 = vehicle_data_filtered_for_distance.iloc[0][['lat', 'lon']]

        lat2, lon2 = vehicle_data_filtered_for_distance.iloc[-1][['lat', 'lon']]

        distance = calculate_distance(lat1, lon1, lat2, lon2)

        trip_info_for_current_vehicle = trip_info_filtered[trip_info_filtered['vehicle_number'] == vehicle_id]

        asset_report_data['License plate number'].append(vehicle_id)
        asset_report_data['Distance'].append(distance)
        asset_report_data['Number of Trips Completed'].append(len(trip_info_for_current_vehicle.index))
        asset_report_data['Average Speed'].append(vehicle_data_filtered['spd'].mean())
        asset_report_data['Transporter Name'].append(', '.join(trip_info_for_current_vehicle['transporter_name'].unique()))
        asset_report_data['Number of Speed Violations'].append(len(vehicle_data_filtered[vehicle_data_filtered['osf'] == True].index))

    # Create a DataFrame from the asset_report_data dictionary
    asset_report_df = pd.DataFrame(asset_report_data)

    # Check if there is any data, else return null
    if len(asset_report_df.index) == 0:
        return None

    # Generate Excel file from the DataFrame
    output_path = 'asset_report.xlsx'
    
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    asset_report_df.to_excel(writer, sheet_name='Report', index=False)

    for column in asset_report_df:
        column_length = max(asset_report_df[column].astype(str).map(len).max(), len(column))
        col_idx = asset_report_df.columns.get_loc(column)
        writer.sheets['Report'].set_column(col_idx, col_idx, column_length)

    writer.close()

    return output_path  # Return the file path to the generated Excel report
