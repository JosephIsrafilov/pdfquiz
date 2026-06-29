import pytest
import os
from flask import Flask

def test_secret_key_production():
    """Test that starting in production without a valid SECRET_KEY raises RuntimeError."""
    from app import create_app
    from app.config import Config
    
    # Save original env and config
    orig_env = os.environ.get("SECRET_KEY")
    orig_config = Config.SECRET_KEY
    
    # Remove SECRET_KEY or set to default
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]
    
    # Flask app config will pick up from environment or default
    Config.SECRET_KEY = "change-this-secret-key"
    
    try:
        with pytest.raises(RuntimeError, match="A strong SECRET_KEY must be set in production."):
            create_app()
    finally:
        # Restore
        Config.SECRET_KEY = orig_config
        if orig_env:
            os.environ["SECRET_KEY"] = orig_env
        else:
            if "SECRET_KEY" in os.environ:
                del os.environ["SECRET_KEY"]
