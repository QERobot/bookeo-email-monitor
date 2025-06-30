#!/usr/bin/env python3
"""
Keep-alive service to ping the Render deployment every 10 minutes
Run this separately on any computer/service to keep the Render app awake
"""

import time
import requests
from datetime import datetime

def ping_service(url):
    """Ping the service to keep it awake"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print(f"✅ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Service pinged successfully")
            return True
        else:
            print(f"⚠️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Service responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ping failed: {str(e)}")
        return False

def main():
    """Main keep-alive loop"""
    # Replace with your Render app URL once deployed
    service_url = "https://your-app-name.onrender.com/health"
    
    print("🔄 Keep-alive service started")
    print(f"📡 Pinging: {service_url}")
    print("⏰ Interval: Every 10 minutes")
    print("=" * 50)
    
    while True:
        try:
            ping_service(service_url)
            # Sleep for 10 minutes (600 seconds)
            time.sleep(600)
            
        except KeyboardInterrupt:
            print("\n🛑 Keep-alive service stopped by user")
            break
        except Exception as e:
            print(f"💥 Unexpected error: {str(e)}")
            print("⏳ Retrying in 1 minute...")
            time.sleep(60)

if __name__ == "__main__":
    main()