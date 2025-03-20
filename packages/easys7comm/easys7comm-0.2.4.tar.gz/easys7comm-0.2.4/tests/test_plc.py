import pytest
from src.easys7comm import PLC

@pytest.fixture
def plc():
    return PLC("10.254.176.81")

@pytest.mark.integration_test
def test_plc_connection(plc):
    assert plc.get_connected() == True
    plc.close()