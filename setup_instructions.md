# Email Authentication Setup Guide

## Current Issue
The email monitoring agent cannot connect to robot@quantumescapesdanville.com because authentication is failing with all major email providers.

## Possible Solutions

### 1. Check Email Provider
Your email domain `quantumescapesdanville.com` needs to be configured with the correct IMAP settings. Here's how to find them:

**Option A: Contact Your Email Administrator**
- Ask your IT administrator for IMAP server settings
- You need: server address, port, and any special authentication requirements

**Option B: Check Email Client Settings**
- Look at your existing email client (Outlook, Apple Mail, etc.)
- Note the incoming server settings

### 2. Common Email Hosting Scenarios

**If using Google Workspace:**
- Server: `imap.gmail.com:993`
- You need an "App Password" instead of your regular password
- Enable 2-factor authentication first
- Generate App Password at: https://myaccount.google.com/apppasswords

**If using Microsoft 365:**
- Server: `outlook.office365.com:993`
- May need App Password depending on security settings
- Check admin center for authentication requirements

**If using cPanel/Web Hosting:**
- Server usually: `mail.yourdomain.com:993` or `imap.yourdomain.com:993`
- Use your regular email password
- Contact hosting provider if unsure

### 3. Alternative Authentication Methods

**App Passwords (Recommended for Gmail/Google):**
1. Enable 2-factor authentication on your Google account
2. Go to Google Account settings > Security > App passwords
3. Generate a new app password for "Mail"
4. Use this 16-character password instead of your regular password

**OAuth (Advanced):**
- Some providers require OAuth instead of password authentication
- This requires additional setup and API credentials

### 4. Test Your Settings
Once you have the correct IMAP settings, update the environment variables:
```
EMAIL_ADDRESS=robot@quantumescapesdanville.com
EMAIL_PASSWORD=your_app_password_or_correct_password
```

## Current Workaround
The monitoring agent is designed to be resilient. If email access fails, it will:
1. Log detailed error messages
2. Continue attempting to connect periodically
3. Alert you about connection issues

This means once you fix the email authentication, the agent will automatically start working without needing to restart.