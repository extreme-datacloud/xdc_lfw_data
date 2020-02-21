import pytest
from wq_modules import meteo
from wq_modules import config
import datetime
import pandas as pd
from datetime import timedelta
from datetime import datetime
from dateutil import parser
import hashlib
import os

@pytest.fixture
def supply_params():
  region = 'CdP'
  sd = datetime.strptime('10-10-2018', "%m-%d-%Y")
  ed = datetime.strptime('11-11-2018', "%m-%d-%Y")
  params = ["ID","Date","Temp"]
  hash_code='5638736afcb788f5aa377218d1cd1523'
  api_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ2aWxsYXJyakB1bmljYW4uZXMiLCJqdGkiOiJkZDc5ZjVmNy1hODQwLTRiYWQtYmMzZi1jNjI3Y2ZkYmUxNmYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTUyMDg0NzgyOSwidXNlcklkIjoiZGQ3OWY1ZjctYTg0MC00YmFkLWJjM2YtYzYyN2NmZGJlMTZmIiwicm9sZSI6IiJ9.LMl_cKCtYi3RPwLwO7fJYZMes-bdMVR91lRFZbUSv84'
  api_url = 'opendata.aemet.es'
  return [region,sd,ed,params,hash_code,api_token,api_url]

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
    hash_code = hashlib.md5(file_as_bytes(open(meteo_output['output'], 'rb'))).hexdigest()
    os.remove(meteo_output['output'])
    os.rmdir('datasets/%s' % supply_params[0])
    os.rmdir('datasets')
    assert hash_code == supply_params[4]
