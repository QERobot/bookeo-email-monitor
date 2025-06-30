# Deploy to Render.com for Free 24/7 Operation

## Step 1: Create GitHub Repository

1. **Create a new GitHub repository:**
   - Go to https://github.com/new
   - Name it: `bookeo-email-monitor`
   - Make it public (required for free Render deployment)
   - Click "Create repository"

2. **Upload your code to GitHub:**
   - Download all files from this Replit project
   - Upload them to your new GitHub repository
   - **Important files to include:**
     - `main.py`
     - `email_monitor.py`
     - `sms_sender.py`
     - `config.py`
     - `logger_config.py`
     - `render_requirements.txt` (rename to `requirements.txt`)

## Step 2: Deploy to Render.com

1. **Sign up for Render.com:**
   - Go to https://render.com
   - Sign up with your GitHub account (free)

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `bookeo-email-monitor`

3. **Configure the deployment:**
   - **Name:** `bookeo-email-monitor`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Instance Type:** `Free` (0.1 CPU, 512MB RAM)

## Step 3: Set Environment Variables

In Render's dashboard, add these environment variables:

```
EMAIL_ADDRESS=robot@quantumescapesdanville.com
EMAIL_PASSWORD=your_app_password_from_yahoo
BOOKEO_SENDER=noreply@bookeo.com
TARGET_PHONE_NUMBER=619-917-2605
CHECK_INTERVAL=120
LOG_LEVEL=INFO
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

## Step 4: Add Keep-Alive Mechanism

To prevent the free service from sleeping, I'll create a simple HTTP endpoint that can be pinged every 10 minutes.

## Step 5: Deploy and Monitor

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Your agent will run 24/7 for free!

## Free Tier Limits
- **750 hours/month** - more than enough for 24/7 operation
- **Sleeps after 15 minutes** of no HTTP requests (we'll prevent this with keep-alive)
- **512MB RAM** - sufficient for email monitoring
- **Automatic SSL** and custom domain available

## Advantages over Replit
- ✅ Runs 24/7 even when you're not logged in
- ✅ Completely free
- ✅ More reliable for production services
- ✅ Automatic deployments from GitHub
- ✅ Built-in monitoring and logs

Would you like me to help you with any of these steps, or shall I modify the code to add the keep-alive HTTP endpoint first?