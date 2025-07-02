"""
SMS sending module using Twilio for notifications
"""

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

class SMSSender:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.client = None
        self.setup_twilio_client()
    
    def setup_twilio_client(self):
        """Initialize Twilio client with credentials"""
        try:
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            
            if not account_sid or not auth_token:
                self.logger.error("Twilio credentials not found in environment variables")
                return False
            
            self.client = Client(account_sid, auth_token)
            self.logger.info("Twilio client initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Twilio client: {str(e)}")
            return False
    
    def test_connection(self):
        """Test Twilio connection by validating account"""
        self.logger.info("Testing Twilio connection...")
        
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return False
        
        try:
            # Try to fetch account information to test connection
            account = self.client.api.accounts(self.client.username).fetch()
            self.logger.info(f"Twilio connection successful. Account: {account.friendly_name}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Twilio connection test failed: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error testing Twilio connection: {str(e)}")
            return False
    
    def format_phone_number(self, phone_number):
        """Format phone number for Twilio (ensure it starts with +1)"""
        # Remove any non-digit characters
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Add country code if not present
        if len(clean_number) == 10:
            return f"+1{clean_number}"
        elif len(clean_number) == 11 and clean_number.startswith('1'):
            return f"+{clean_number}"
        elif clean_number.startswith('+'):
            return phone_number
        else:
            return f"+1{clean_number}"
    
    def send_notification(self, to_phone_number, message):
        """Send SMS notification via Twilio"""
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return False
        
        try:
            # Get Twilio phone number from environment
            from_phone = os.getenv("TWILIO_PHONE_NUMBER")
            if not from_phone:
                self.logger.error("TWILIO_PHONE_NUMBER not found in environment variables")
                return False
            
            # Format phone numbers
            formatted_to = self.format_phone_number(to_phone_number)
            formatted_from = self.format_phone_number(from_phone)
            
            self.logger.info(f"Sending SMS from {formatted_from} to {formatted_to}")
            
            # Send SMS
            twilio_message = self.client.messages.create(
                body=message[:50],  # Limit message length  # was [:1600 and shortened to 50 to minimize cost and use free service
                from_=formatted_from,
                to=formatted_to
            )
            
            self.logger.info(f"SMS sent successfully. Message SID: {twilio_message.sid}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Twilio error sending SMS: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error sending SMS notification: {str(e)}")
            return False
    
    def send_test_message(self, to_phone_number):
        """Send a test message to verify SMS functionality"""
        test_message = (
            "Email Monitor Test\n"
            "test message"
        )
        
        self.logger.info("Sending test SMS message...")
        return self.send_notification(to_phone_number, test_message)
