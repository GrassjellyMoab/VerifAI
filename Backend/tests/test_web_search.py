# test_web_search.py
import pytest
from app.services.web_search import perform_web_search

def test_perform_web_search():
    query = "Latest scam. Turned off your outside tap, no water. Then put scan QR code for you to scan. All your bank accounts & money gone! BN. AEB IRARINEAYZK Ww, 27K. AM LAH ZE TS TERIA. PRP AAYERTT MP MEER T |"
    results = perform_web_search(query)
    # Assert the structure or at least check that you get some results back
    assert isinstance(results, list)
    assert len(results) > 0
