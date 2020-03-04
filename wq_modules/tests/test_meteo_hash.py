import pytest
from wq_modules import meteo
from wq_modules import config
import datetime
import hashlib
import os
import requests
import time


@pytest.fixture
def supply_params():
    region = 'CdP'
    sd = datetime.datetime.strptime('10-10-2018', "%m-%d-%Y")
    ed = datetime.datetime.strptime('11-11-2018', "%m-%d-%Y")
    params = ["ID", "Date", "Temp"]
    hash_code = '5638736afcb788f5aa377218d1cd1523'
    api_token = ("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ2aWxsYXJyakB1bmljYW4uZXMiLC"
                 "JqdGkiOiJkZDc5ZjVmNy1hODQwLTRiYWQtYmMzZi1jNjI3Y2ZkYmUxNmYiL"
                 "CJpc3MiOiJBRU1FVCIsImlhdCI6MTUyMDg0NzgyOSwidXNlcklkIjoiZGQ3"
                 "OWY1ZjctYTg0MC00YmFkLWJjM2YtYzYyN2NmZGJlMTZmIiwicm9sZSI6IiJ"
                 "9.LMl_cKCtYi3RPwLwO7fJYZMes-bdMVR91lRFZbUSv84")
    api_url = 'opendata.aemet.es'
    onedata_token = ("MDAxNWxvY2F00aW9uIG9uZXpvbmUKMDAzMGlkZW500a"
                     "WZpZXIgOTAwNGNlNzBiYWQyMTYzYzY1YWY4NTNhZjQy"
                     "MGJlYWEKMDAxYWNpZCB00aW1lIDwgMTU4MzkxODYyOQ"
                     "owMDJmc2lnbmF00dXJlICmASYmuGx6CSPHwkf3s9pXW"
                     "2szUqJPBPoFEXIKOZ2L00Cg")
    headers = {"X-Auth-Token": onedata_token}
    onedata_prov = "https://cloud-90-147-75-163.cloud.ba.infn.it"
    onedata_api = "/api/v3/oneprovider/"
    onedata_space = "LifeWatch"
    return [region, sd, ed, params, hash_code, api_token, api_url,
            onedata_token, headers, onedata_prov, onedata_api,
            onedata_space]


def file_as_bytes(file):
    with file:
        return file.read()


def test_file1_method1(supply_params):
    os.mkdir('datasets')
    os.mkdir('datasets/%s' % supply_params[0])
    config.METEO_API_TOKEN = supply_params[5]
    config.METEO_API_URL = supply_params[6]
    m = meteo.Meteo(supply_params[1], supply_params[2], supply_params[0])
    m.params = supply_params[3]
    meteo_output = m.get_meteo()
    hash_code = hashlib.md5(
        file_as_bytes(open(meteo_output['output'], 'rb'))).hexdigest()
    os.remove(meteo_output['output'])
    os.rmdir('datasets/%s' % supply_params[0])
    os.rmdir('datasets')
    assert hash_code == supply_params[4]


def test_api_connection(supply_params):
    start_time = time.time()
    api_url = supply_params[6]
    api_token = supply_params[5]
    url = ("https://" + api_url + "/opendata/api/observacion/convencional"
           "/mensajes/tipomensaje/temp/?api_key=" + api_token)
    r = requests.get(url)
    assert r.status_code == 200
    total_time = time.time() - start_time
    assert total_time < 30.0


def test_metadata_attachment(supply_params):
    config.onedata_mode = 1
    config.onedata_token = supply_params[7]
    config.onedata_url = supply_params[9]
    config.onedata_api = supply_params[10]
    os.mkdir('datasets')
    os.mkdir('datasets/%s' % supply_params[0])
    config.METEO_API_TOKEN = supply_params[5]
    config.METEO_API_URL = supply_params[6]
    # rg = supply_params[0]
    # ons = supply_params[11]
    m = meteo.Meteo(supply_params[1], supply_params[2], supply_params[0])
    m.params = supply_params[3]
    meteo_output = m.get_meteo()
    file_out = meteo_output['output']
    file_out = file_out.replace('datasets/', '')
    url = ("https://cloud-90-147-75-163.cloud.ba.infn.it/api/v3/oneprovider"
           "/metadata/json/LifeWatch/CdP/temp_2018-10-10_2018-11-11.csv")
    r = requests.get(url, headers=supply_params[8])
    os.remove(meteo_output['output'])
    os.rmdir('datasets/%s' % supply_params[0])
    os.rmdir('datasets')
    assert r.status_code == 200
