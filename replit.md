# Email Monitoring Agent

## Overview

This is a Python-based automated email monitoring system that continuously checks for Bookeo appointment notifications and sends SMS alerts via Twilio. The application monitors a specific email account (`robot@quantumescapesdanville.com`) for emails from Bookeo (`noreply@bookeo.com`) and forwards notifications to a target phone number via SMS.

## System Architecture

The system follows a modular, service-oriented architecture with clear separation of concerns:

- **Configuration Layer**: Centralized configuration management with environment variable support
- **Email Monitoring Service**: IMAP-based email checking with automatic server detection
- **SMS Notification Service**: Twilio-based SMS delivery system
- **Logging Infrastructure**: Comprehensive logging with file rotation and console output
- **Main Controller**: Orchestrates the monitoring loop and handles graceful shutdown

## Key Components

### Configuration Management (`config.py`)
- **Purpose**: Centralizes all configuration settings with sensible defaults
- **Environment Variable Support**: Secure credential management through environment variables
- **Validation**: Built-in configuration validation to catch setup issues early
- **Flexibility**: Configurable check intervals, phone numbers, and email settings

### Email Monitor (`email_monitor.py`)
- **IMAP Integration**: Automatic IMAP server detection based on email domain
- **Multi-Provider Support**: Works with Gmail, Outlook, Yahoo, and generic IMAP servers
- **Intelligent Filtering**: Filters emails by sender (Bookeo) and timestamp
- **Connection Management**: Robust connection handling with automatic reconnection

### SMS Sender (`sms_sender.py`)
- **Twilio Integration**: Uses Twilio REST API for reliable SMS delivery
- **Connection Testing**: Built-in connection validation and testing capabilities
- **Error Handling**: Comprehensive error handling for SMS delivery failures
- **Credential Security**: Secure credential management through environment variables

### Logging System (`logger_config.py`)
- **Dual Output**: Both console and file logging for development and production
- **Log Rotation**: Automatic log file rotation to prevent disk space issues
- **Configurable Levels**: Adjustable logging levels for different environments
- **Structured Format**: Consistent timestamp and message formatting

### Main Controller (`main.py`)
- **Event Loop**: Continuous monitoring with configurable intervals (default: 2 minutes)
- **Signal Handling**: Graceful shutdown on SIGINT and SIGTERM signals
- **Error Recovery**: Resilient operation with automatic error recovery
- **Service Orchestration**: Coordinates all components and handles the main workflow

## Data Flow

1. **Initialization Phase**:
   - Load configuration from environment variables
   - Initialize logging system
   - Setup Twilio client and test connection
   - Establish IMAP connection to email server

2. **Monitoring Loop**:
   - Check email inbox for new messages every 2 minutes (configurable)
   - Filter emails from Bookeo sender (`noreply@bookeo.com`)
   - Extract email metadata (subject, sender, timestamp)
   - Format notification message with booking details

3. **Notification Phase**:
   - Send SMS alert to target phone number (`619-917-2605`)
   - Log all activities (successes and failures)
   - Continue monitoring loop until shutdown signal

4. **Shutdown Phase**:
   - Handle SIGINT/SIGTERM signals gracefully
   - Close IMAP connections
   - Log shutdown completion

## External Dependencies

### Core Dependencies
- **imaplib**: Built-in Python library for IMAP email access
- **twilio**: Twilio Python SDK for SMS messaging
- **email**: Built-in Python library for email parsing
- **logging**: Built-in Python logging infrastructure

### Email Provider Support
- **Gmail**: Uses `imap.gmail.com:993` with App Password authentication
- **Outlook/Hotmail**: Uses `outlook.office365.com:993`
- **Yahoo**: Uses `imap.mail.yahoo.com:993`
- **Generic IMAP**: Automatic server detection for other providers

### Twilio Service
- **SMS Delivery**: Reliable SMS messaging through Twilio API
- **Free Trial**: Supports Twilio free trial accounts
- **Global Reach**: SMS delivery to various countries and carriers

## Deployment Strategy

### Environment Setup
- **Python 3.7+**: Minimum Python version requirement
- **Environment Variables**: Secure credential storage via `.env` file or system environment
- **IMAP Access**: Email account must have IMAP enabled (App Passwords for Gmail)
- **Twilio Account**: Free or paid Twilio account with phone number

### Production Considerations
- **Process Management**: Can be run as a systemd service or in a container
- **Monitoring**: Built-in logging for operational monitoring
- **Resource Usage**: Low CPU and memory footprint for continuous operation
- **Error Recovery**: Automatic reconnection and error handling for reliability

### Security Features
- **No Hardcoded Credentials**: All sensitive data managed through environment variables
- **Secure Connections**: SSL/TLS for both IMAP and Twilio API connections
- **Input Validation**: Configuration validation prevents common setup errors

## Changelog

```
Changelog:
- June 30, 2025. Initial setup
- June 30, 2025. Successfully configured Turbify email authentication with App Password
- June 30, 2025. Email monitoring agent fully operational and monitoring Bookeo emails
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```