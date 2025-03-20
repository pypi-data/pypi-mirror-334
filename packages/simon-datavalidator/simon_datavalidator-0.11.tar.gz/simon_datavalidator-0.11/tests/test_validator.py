import pytest
from datavalidator.validator import DataValidator

@pytest.fixture
def data_validator():
    return DataValidator()

def test_validate_email(data_validator):
    data_validator.data = "user@example.com"
    assert data_validator.validate_email() is True

    data_validator.data = "user@@example..com"
    assert data_validator.validate_email() is False

def test_validate_phone(data_validator):
    data_validator.data = "+1234567890"
    assert data_validator.validate_phone() is True

    data_validator.data = "123-abc-7890"
    assert data_validator.validate_phone() is False

def test_validate_date(data_validator):
    data_validator.data = "2023-12-31"
    assert data_validator.validate_date() is True

    data_validator.data = "31-12-2023"
    assert data_validator.validate_date() is False

    data_validator.data = "2025/02/14"
    assert data_validator.validate_date() is True

    data_validator.data = "2025-02-29"
    assert data_validator.validate_date() is False

def test_validate_url(data_validator):
    data_validator.data = "https://example.com"
    assert data_validator.validate_url() is True

    data_validator.data = "htp:/example"
    assert data_validator.validate_url() is False