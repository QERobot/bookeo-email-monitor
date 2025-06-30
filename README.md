# Bookeo Email Monitoring Agent

An automated Python agent that monitors emails for Bookeo notifications and sends SMS alerts using Twilio.

## Features

- **Automated Email Monitoring**: Checks robot@quantumescapesdanville.com every 2 minutes
- **Bookeo Detection**: Identifies emails from noreply@bookeo.com
- **SMS Alerts**: Sends notifications to 619-917-2605 via Twilio
- **Persistent Monitoring**: Runs continuously with error recovery
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Secure Configuration**: Uses environment variables for credentials

## Prerequisites

- Python 3.7 or higher
- Twilio account (free trial available)
- Email account with IMAP access enabled

## Setup Instructions

### 1. Get Twilio Credentials (Free)

1. Sign up for a free Twilio account at https://www.twilio.com/try-twilio
2. Complete the verification process
3. In the Twilio Console, find your:
   - Account SID
   - Auth Token
   - Twilio Phone Number (you'll get a free trial number)

### 2. Prepare Email Account

For Gmail accounts:
1. Enable 2-Factor Authentication
2. Generate an App Password (not your regular password)
3. Use the App Password as EMAIL_PASSWORD

For other providers, ensure IMAP access is enabled.

### 3. Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required Twilio Settings
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Email Settings (defaults provided)
EMAIL_ADDRESS=robot@quantumescapesdanville.com
EMAIL_PASSWORD=Agentlogin1234!

# Optional Settings
BOOKEO_SENDER=noreply@bookeo.com
TARGET_PHONE_NUMBER=619-917-2605
CHECK_INTERVAL=120
LOG_LEVEL=INFO
