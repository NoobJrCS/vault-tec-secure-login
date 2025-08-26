# project_config.py

import os
from dotenv import load_dotenv

# This function loads the variables from your .env file
load_dotenv()

class Config:
    """Set Flask configuration variables from .env file."""

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for signing cookies and other security-related needs
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')