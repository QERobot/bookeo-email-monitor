# Turbify (Yahoo Small Business) Email Setup Guide

## Step 1: Create an App Password for robot@quantumescapesdanville.com

Since your email is hosted by Turbify (formerly Yahoo Small Business), you need to generate an App Password instead of using your regular email password.

### How to Generate App Password:

1. **Sign in to Yahoo Account Security**
   - Go to: https://login.yahoo.com/account/security
   - Sign in with robot@quantumescapesdanville.com

2. **Enable Two-Step Verification (if not already enabled)**
   - Click "Two-step verification" 
   - Follow the setup process (you'll need a phone number)
   - This is required before you can create App Passwords

3. **Generate App Password**
   - Click "Generate app password" or "Manage app passwords"
   - Select "Other app" from the dropdown
   - Type: "Email Monitoring Agent" as the app name
   - Click "Generate"
   - **Copy the 16-character password** (it looks like: abcd efgh ijkl mnop)

4. **Save the App Password**
   - This will replace "Agentlogin1234!" in your configuration
   - You can only see this password once, so save it immediately

## Step 2: Update Your Email Password

Once you have the App Password, you need to update the environment variable:

1. In Replit, go to Secrets (the lock icon in sidebar)
2. Add or update: `EMAIL_PASSWORD` 
3. Set the value to your new 16-character App Password (without spaces)

## Step 3: Turbify IMAP Settings

Your email will use these settings:
- **IMAP Server**: imap.mail.yahoo.com
- **Port**: 993 (SSL)
- **Email**: robot@quantumescapesdanville.com
- **Password**: Your new App Password

## Step 4: Test the Connection

After updating the password, the monitoring agent will automatically:
1. Try connecting with the new App Password
2. Connect to Yahoo's IMAP servers (which Turbify uses)
3. Start monitoring for Bookeo emails
4. Send SMS alerts when found

## Troubleshooting

**If you can't find "Generate app password":**
- Make sure two-step verification is enabled first
- Look under Account Security > Sign-in and security
- Some accounts may call it "App passwords" or "Third-party app access"

**If connection still fails:**
- Double-check the App Password was copied correctly (no spaces)
- Ensure IMAP access is enabled in your Yahoo/Turbify settings
- Contact Turbify support if needed

## Alternative: Manual IMAP Settings

If the automatic Yahoo detection doesn't work, you can also try these Turbify-specific servers:
- imap.bizmail.yahoo.com:993
- imap.turbify.com:993 (if available)

The monitoring agent will automatically try these servers for your domain.