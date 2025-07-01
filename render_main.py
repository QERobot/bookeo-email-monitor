"""
Enhanced Render.com version with improved keep-alive mechanism
This version prevents the free tier from sleeping by adding internal HTTP activity
"""

import time
import signal
import sys
import re
import threading
import requests
from datetime import datetime
from email_monitor import EmailMonitor
from sms_sender import SMSSender
from logger_config import setup_logger
from config import Config

# Simple HTTP server for keep-alive
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Email Monitor is running')
        elif self.path == '/keepalive':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Keep-alive ping received')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass

class EmailMonitoringAgent:
    def __init__(self):
        self.logger = setup_logger()
        self.config = Config()
        self.email_monitor = EmailMonitor(self.config, self.logger)
        self.sms_sender = SMSSender(self.config, self.logger)
        self.running = True
        self.service_url = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start HTTP server for keep-alive
        self.start_http_server()
        
        # Start internal keep-alive pinger
        self.start_keep_alive_pinger()
    
    def start_http_server(self):
        """Start HTTP server for health checks and keep-alive"""
        port = int(os.environ.get('PORT', 10000))  # Render assigns PORT
        
        def run_server():
            try:
                server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
                self.logger.info(f"HTTP server started on port {port}")
                server.serve_forever()
            except Exception as e:
                self.logger.error(f"HTTP server error: {str(e)}")
        
        # Run HTTP server in background thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
    
    def start_keep_alive_pinger(self):
        """Start internal keep-alive pinger to prevent sleeping"""
        def ping_self():
            while self.running:
                try:
                    # Wait 10 minutes between pings
                    time.sleep(600)  # 10 minutes
                    
                    if self.running:
                        # Try to ping our own health endpoint
                        try:
                            if not self.service_url:
                                # Try to determine our service URL from environment
                                render_service = os.environ.get('RENDER_SERVICE_NAME', 'bookeo-email-monitor')
                                self.service_url = f"https://{render_service}.onrender.com"
                            
                            response = requests.get(f"{self.service_url}/keepalive", timeout=30)
                            if response.status_code == 200:
                                self.logger.info("Keep-alive ping successful - service staying awake")
                            else:
                                self.logger.warning(f"Keep-alive ping returned status: {response.status_code}")
                        except Exception as ping_error:
                            self.logger.warning(f"Keep-alive ping failed: {str(ping_error)}")
                            
                except Exception as e:
                    self.logger.error(f"Keep-alive pinger error: {str(e)}")
        
        # Start keep-alive pinger in background thread
        pinger_thread = threading.Thread(target=ping_self, daemon=True)
        pinger_thread.start()
        self.logger.info("Internal keep-alive pinger started (10-minute intervals)")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def extract_booking_details(self, email_body):
        """Extract key booking details from Bookeo email"""
        details = {}
        
        try:
            # Extract Date
            date_match = re.search(r'Date:\s*(.+)', email_body)
            if date_match:
                details['date'] = date_match.group(1).strip()
            
            # Extract Time
            time_match = re.search(r'Time:\s*(.+)', email_body)
            if time_match:
                details['time'] = time_match.group(1).strip()
            
            # Extract Game
            game_match = re.search(r'Game:\s*(.+)', email_body)
            if game_match:
                details['game'] = game_match.group(1).strip()
            
            # Extract Participants
            participants_match = re.search(r'Participants:\s*(.+)', email_body)
            if participants_match:
                details['participants'] = participants_match.group(1).strip()
            
            # Extract Total price
            price_match = re.search(r'Total price:\s*(.+)', email_body)
            if price_match:
                details['price'] = price_match.group(1).strip()
            
            # Extract Customer name
            customer_match = re.search(r'Customer\s*([^\n]+)', email_body)
            if customer_match:
                details['customer'] = customer_match.group(1).strip()
            
            # Extract Customer email
            email_match = re.search(r'Email:\s*([^\s\n]+)', email_body)
            if email_match:
                details['customer_email'] = email_match.group(1).strip()
            
            # Extract Customer phone
            phone_match = re.search(r'Phone \(mobile\):\s*(.+)', email_body)
            if phone_match:
                details['customer_phone'] = phone_match.group(1).strip()
            
            # Extract Booking number
            booking_match = re.search(r'Booking number:\s*(.+)', email_body)
            if booking_match:
                details['booking_number'] = booking_match.group(1).strip()
                
        except Exception as e:
            self.logger.error(f"Error extracting booking details: {str(e)}")
        
        return details

    def process_new_bookeo_emails(self, emails):
        """Process and send SMS alerts for new Bookeo emails"""
        for email_info in emails:
            try:
                subject = email_info.get('subject', 'No Subject')
                email_body = email_info.get('body', '')
                
                # Extract booking details from email body
                booking_details = self.extract_booking_details(email_body)
                
                # Create detailed SMS message
                if booking_details:
                    message = "🔔 NEW BOOKEO BOOKING!\n"
                    
                    if 'date' in booking_details:
                        message += f"📅 Date: {booking_details['date']}\n"
                    if 'time' in booking_details:
                        message += f"⏰ Time: {booking_details['time']}\n"
                    if 'game' in booking_details:
                        message += f"🎮 Game: {booking_details['game']}\n"
                    if 'participants' in booking_details:
                        message += f"👥 Participants: {booking_details['participants']}\n"
                    if 'customer' in booking_details:
                        message += f"👤 Customer: {booking_details['customer']}\n"
                    if 'customer_phone' in booking_details:
                        message += f"📞 Phone: {booking_details['customer_phone']}\n"
                else:
                    # Fallback message if extraction fails
                    message = (
                        f"🔔 New Bookeo Booking!\n"
                        f"Subject: {subject}\n"
                        f"Check email for full details."
                    )
                
                # Send SMS notification
                success = self.sms_sender.send_notification(
                    self.config.target_phone_number,
                    message
                )
                
                if success:
                    self.logger.info(f"SMS alert sent successfully for booking: {booking_details.get('booking_number', 'Unknown')}")
                else:
                    self.logger.error(f"Failed to send SMS alert for email: {subject}")
                    
            except Exception as e:
                self.logger.error(f"Error processing email notification: {str(e)}")

    def run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        try:
            self.logger.info("Starting email monitoring cycle...")
            new_emails = self.email_monitor.check_for_bookeo_emails()
            
            if new_emails:
                self.logger.info(f"Found {len(new_emails)} new Bookeo email(s)")
                self.process_new_bookeo_emails(new_emails)
            else:
                self.logger.info("No new Bookeo emails found")
                
        except Exception as e:
            self.logger.error(f"Error in monitoring cycle: {str(e)}")

    def run(self):
        """Main monitoring loop"""
        try:
            # Test connections before starting main loop
            self.logger.info("Testing email connection...")
            if not self.email_monitor.test_connection():
                self.logger.error("Email connection test failed")
                return False
            
            self.logger.info("Testing Twilio connection...")
            if not self.sms_sender.test_connection():
                self.logger.error("Twilio connection test failed")
                return False
            
            self.logger.info("All connection tests passed. Starting monitoring...")
            
            # Main monitoring loop
            while self.running:
                self.run_monitoring_cycle()
                
                # Wait for next check (2 minutes)
                for _ in range(120):  # 120 seconds = 2 minutes
                    if not self.running:
                        break
                    time.sleep(1)
            
            self.logger.info("Email monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Critical error in monitoring loop: {str(e)}")
            return False

def main():
    """Entry point for the application"""
    agent = EmailMonitoringAgent()
    
    try:
        agent.run()
    except KeyboardInterrupt:
        agent.logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        agent.logger.error(f"Unexpected error: {str(e)}")
    finally:
        agent.running = False
        agent.logger.info("Email monitoring agent shutdown complete")

if __name__ == "__main__":
    main()