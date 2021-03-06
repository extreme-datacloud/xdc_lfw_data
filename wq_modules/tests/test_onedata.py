import pytest
import requests


@pytest.fixture
def supply_params():
    onedata_token = ("MDAyOGxvY2F00aW9uIG9uZXpvbmUuY2xvdWQuY25hZi"
                     "5pbmZuLml00CjAwMzBpZGVudGlmaWVyIDk4OTgwNjc1"
                     "MWU00NjhlZjA1ODZjNzMwZDNjNjVjN2IxCjAwMWFjaW"
                     "QgdGltZSA8IDE2MTcxNzY1NTkKMDAyZnNpZ25hdHVyZ"
                     "SChV36AW00frfBqr02CpD3B6SxVXnVMuP8vsHE6yEqJ"
                     "FsKgo")
    headers = {"X-Auth-Token": onedata_token}
    onezone_url = 'https://onezone.cloud.cnaf.infn.it/api/v3/onezone/user'
    oneprovider_url = ("https://cloud-90-147-75-163.cloud.ba.infn.it/api/"
                       "v3/oneprovider/configuration")
    return [headers, onezone_url, oneprovider_url]


def test_onezone_up(supply_params):
    r = requests.get(supply_params[1], headers=supply_params[0])
    assert r.status_code == 200


def test_provider_up(supply_params):
    r = requests.get(supply_params[2], headers=supply_params[0])
    assert r.status_code == 200
