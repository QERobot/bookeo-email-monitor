"""
Configuration management for the email monitoring agent
"""

import os
from datetime import datetime

class Config:
    def __init__(self):
        # Email configuration
        self.email_address = os.getenv("EMAIL_ADDRESS", "robot@quantumescapesdanville.com")
        self.email_password = os.getenv("EMAIL_PASSWORD", "Agentlogin1234!")
        
        # Bookeo sender configuration
        self.bookeo_sender = os.getenv("BOOKEO_SENDER", "noreply@bookeo.com")
        
        # SMS configuration
        self.target_phone_number = os.getenv("TARGET_PHONE_NUMBER", "619-917-2605")
        
        # Monitoring configuration
        self.check_interval = int(os.getenv("CHECK_INTERVAL", "120"))  # 2 minutes default
        
        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_file = os.getenv("LOG_FILE", "email_monitor.log")
        
        # Twilio configuration (required environment variables)
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
    
    def validate(self):
        """Validate configuration settings"""
        errors = []
        
        # Check required email settings
        if not self.email_address:
            errors.append("EMAIL_ADDRESS is required")
        
        if not self.email_password:
            errors.append("EMAIL_PASSWORD is required")
        
        # Check required Twilio settings
        if not self.twilio_account_sid:
            errors.append("TWILIO_ACCOUNT_SID environment variable is required")
        
        if not self.twilio_auth_token:
            errors.append("TWILIO_AUTH_TOKEN environment variable is required")
        
        if not self.twilio_phone_number:
            errors.append("TWILIO_PHONE_NUMBER environment variable is required")
        
        # Check target phone number
        if not self.target_phone_number:
            errors.append("TARGET_PHONE_NUMBER is required")
        
        # Validate check interval
        if self.check_interval < 30:
            errors.append("CHECK_INTERVAL must be at least 30 seconds")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def print_config(self):
        """Print current configuration (hiding sensitive data)"""
        print("Current Configuration:")
        print(f"  Email Address: {self.email_address}")
        print(f"  Email Password: {'*' * len(self.email_password) if self.email_password else 'Not Set'}")
        print(f"  Bookeo Sender: {self.bookeo_sender}")
        print(f"  Target Phone: {self.target_phone_number}")
        print(f"  Check Interval: {self.check_interval} seconds")
        print(f"  Log Level: {self.log_level}")
        print(f"  Log File: {self.log_file}")
        print(f"  Twilio SID: {'*' * len(self.twilio_account_sid) if self.twilio_account_sid else 'Not Set'}")
        print(f"  Twilio Token: {'*' * len(self.twilio_auth_token) if self.twilio_auth_token else 'Not Set'}")
        print(f"  Twilio Phone: {self.twilio_phone_number if self.twilio_phone_number else 'Not Set'}")
