import os

celery_db_user = "user"
celery_db_pass = "pass"

# onedata path and info
onedata_mode = 0
onedata_token = "token"
onedata_url = "https://oneprovider-cnaf.cloud.cnaf.infn.it"
onedata_api = "/api/v3/oneprovider/"
onedata_user = "user"
onedata_space = "LifeWatch"
download_datasets = "datasets"

# local path and info
config_info = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
satelite_info = {'data_path': download_datasets, 'config_path': config_info}

# configure path
if onedata_mode == 1:
    datasets_path = '/onedata/' + onedata_user + '/'
    datasets_path = datasets_path + onedata_space + '/' + download_datasets
else:
    datasets_path = satelite_info['data_path']

# Credentials for Sentinel data
sentinel_pass = {'username': "lifewatch",
                 'password': "pass"}

# Credentials for Landsat data
landsat_pass = {'username': "lifewatch",
                'password': "pass"}

# info regions
regions = {
    "CdP": {
        "id": 210788,
        "coordinates": {
            "W": -2.830,
            "S": 41.820,
            "E": -2.690,
            "N": 41.910
        }
    },
    "Francia": {
        "id": 234185,
        "coordinates": {
            "W": 1.209,
            "S": 47.807,
            "E": 2.314,
            "N": 48.598
        }
    }
}

# actions
keywords = ['cloud_mask', 'cloud_coverage', 'water_mask', 'water_surface']
