from src.telegram_media_downloader.config.settings import TelegramConfig

def test_from_env(monkeypatch):
    monkeypatch.setenv('TELEGRAM_API_ID', '123')
    monkeypatch.setenv('TELEGRAM_API_HASH', 'hash')
    monkeypatch.setenv('TELEGRAM_PHONE', '+1234567890')
    monkeypatch.setenv('TELEGRAM_SESSION', 'mysession')
    config = TelegramConfig.from_env()
    assert config.api_id == 123
    assert config.api_hash == 'hash'
    assert config.phone_number == '+1234567890'
    assert config.session_name == 'mysession'


def test_validate_all_errors():
    config = TelegramConfig(api_id=0, api_hash='', phone_number='', session_name='')
    errors = config.validate()
    assert 'API_ID is required' in errors[0]
    assert 'API_HASH is required' in errors[1]
    assert 'PHONE_NUMBER is required' in errors[2]
    assert 'SESSION_NAME cannot be empty' in errors[3]


def test_validate_success():
    config = TelegramConfig(api_id=1, api_hash='h', phone_number='+1', session_name='s')
    assert config.validate() == []


def test_validate_phone_number_format():
    config = TelegramConfig(api_id=1, api_hash='h', phone_number='123', session_name='s')
    errors = config.validate()
    assert 'PHONE_NUMBER must include country code' in errors[0]


def test_repr_hides_sensitive():
    config = TelegramConfig(api_id=1, api_hash='h', phone_number='+1234567890', session_name='s')
    r = repr(config)
    assert 'api_id=1' in r
    assert '+12*****' in r
    assert 'api_hash' not in r 