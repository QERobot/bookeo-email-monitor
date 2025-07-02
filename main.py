#!/usr/bin/env python3
"""
Automated Email Monitoring Agent for Bookeo Notifications
Monitors robot@quantumescapesdanville.com for emails from noreply@bookeo.com
and sends SMS alerts when detected.
"""

import time
import signal
import sys
from datetime import datetime
from email_monitor import EmailMonitor
from sms_sender import SMSSender
from logger_config import setup_logger
from config import Config

class EmailMonitoringAgent:
    def __init__(self):
        self.logger = setup_logger()
        self.config = Config()
        self.email_monitor = EmailMonitor(self.config, self.logger)
        self.sms_sender = SMSSender(self.config, self.logger)
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def process_new_bookeo_emails(self, emails):
        """Process and send SMS alerts for new Bookeo emails"""
        for email_info in emails:
            try:
                subject = email_info.get('subject', 'No Subject')
                sender = email_info.get('from', 'Unknown Sender')
                received_time = email_info.get('date', 'Unknown Time')
                
                # Create SMS message
                message = (
                    f" New Bookeo Email Alert!\n"
                #    f"From: {sender}\n"
                #    f"Subject: {subject}\n"
                #    f"Time: {received_time}\n"
                #    f"Check your email for details."
                )
                
                # Send SMS notification
                success = self.sms_sender.send_notification(
                    self.config.target_phone_number,
                    message
                )
                
                if success:
                    self.logger.info(f"SMS alert sent successfully for email: {subject}")
                else:
                    self.logger.error(f"Failed to send SMS alert for email: {subject}")
                    
            except Exception as e:
                self.logger.error(f"Error processing email notification: {str(e)}")
    
    def run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        try:
            self.logger.info("Starting email monitoring cycle...")
            
            # Check for new Bookeo emails
            new_emails = self.email_monitor.check_for_bookeo_emails()
            
            if new_emails:
                self.logger.info(f"Found {len(new_emails)} new Bookeo email(s)")
                self.process_new_bookeo_emails(new_emails)
            else:
                self.logger.info("No new Bookeo emails found")
                
        except Exception as e:
            self.logger.error(f"Error during monitoring cycle: {str(e)}")
    
    def run(self):
        """Main monitoring loop"""
        self.logger.info("Email Monitoring Agent started")
        self.logger.info(f"Monitoring: {self.config.email_address}")
        self.logger.info(f"Target sender: {self.config.bookeo_sender}")
        self.logger.info(f"SMS alerts to: {self.config.target_phone_number}")
        self.logger.info(f"Check interval: {self.config.check_interval} seconds")
        
        # Validate configuration
        if not self.config.validate():
            self.logger.error("Configuration validation failed. Exiting...")
            return False
        
        # Test connections
        if not self.email_monitor.test_connection():
            self.logger.error("Email connection test failed.")
            self.logger.error("The agent will continue running and retry connections periodically.")
            self.logger.error("Check setup_instructions.md for troubleshooting steps.")
            # Don't exit - continue with monitoring loop for resilience
            
        if not self.sms_sender.test_connection():
            self.logger.error("SMS service connection test failed. Exiting...")
            return False
        
        self.logger.info("All connection tests passed. Starting monitoring...")
        
        # Main monitoring loop
        while self.running:
            try:
                cycle_start = datetime.now()
                self.run_monitoring_cycle()
                
                # Calculate sleep time to maintain consistent interval
                cycle_duration = (datetime.now() - cycle_start).total_seconds()
                sleep_time = max(0, self.config.check_interval - cycle_duration)
                
                if sleep_time > 0:
                    self.logger.debug(f"Sleeping for {sleep_time:.2f} seconds until next check")
                    time.sleep(sleep_time)
                else:
                    self.logger.warning(f"Monitoring cycle took longer than interval: {cycle_duration:.2f}s")
                    
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received. Shutting down...")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {str(e)}")
                self.logger.info(f"Waiting {self.config.check_interval} seconds before retry...")
                time.sleep(self.config.check_interval)
        
        self.logger.info("Email Monitoring Agent stopped")
        return True

def main():
    """Entry point for the application"""
    agent = EmailMonitoringAgent()
    
    try:
        success = agent.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        agent.logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
