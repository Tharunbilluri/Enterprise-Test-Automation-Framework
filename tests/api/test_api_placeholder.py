"""API test placeholders — requests-based suite extension point."""

from __future__ import annotations

import pytest
import requests


@pytest.mark.api
@pytest.mark.skip(reason="API suite scaffold — enable when backend contracts are available")
def test_api_health_placeholder() -> None:
    """Example future API check using requests."""
    response = requests.get("https://www.saucedemo.com/", timeout=15)
    assert response.status_code == 200
