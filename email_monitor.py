"""
Email monitoring module for checking IMAP mailbox for Bookeo emails
"""

import imaplib
import email
import email.utils
import socket
from datetime import datetime, timedelta
from email.header import decode_header
import re

class EmailMonitor:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.last_check_time = None
        self.connection = None
    
    def connect_to_mailbox(self):
        """Establish IMAP connection to the mailbox"""
        try:
            # Determine IMAP server based on email domain
            domain = self.config.email_address.split('@')[1].lower()
            
            # List of IMAP servers to try for the domain
            imap_servers = []
            
            if 'gmail' in domain:
                imap_servers = [('imap.gmail.com', 993)]
            elif 'outlook' in domain or 'hotmail' in domain or 'live' in domain:
                imap_servers = [('outlook.office365.com', 993)]
            elif 'yahoo' in domain:
                imap_servers = [('imap.mail.yahoo.com', 993)]
            else:
                # For custom domains, try common hosting providers first
                # Check for Turbify/Yahoo Small Business first for this domain
                if 'quantumescapesdanville' in domain:
                    imap_servers = [
                        ('imap.mail.yahoo.com', 993),  # Turbify uses Yahoo infrastructure
                        ('imap.bizmail.yahoo.com', 993),  # Alternative Yahoo business server
                        ('imap.gmail.com', 993),  # Backup: Google Workspace
                        ('outlook.office365.com', 993),  # Backup: Microsoft 365
                    ]
                else:
                    imap_servers = [
                        # Major hosting providers (most common)
                        ('imap.gmail.com', 993),  # Google Workspace
                        ('outlook.office365.com', 993),  # Microsoft 365
                        ('imap.mail.yahoo.com', 993),  # Yahoo Business/Turbify
                        # Domain-specific servers
                        (f'imap.{domain}', 993),
                        (f'mail.{domain}', 993),
                        (f'{domain}', 993),
                        # Common hosting providers
                        ('imap.hostgator.com', 993),
                        ('imap.godaddy.com', 993),
                        ('mail.privateemail.com', 993),
                        # Fallback to non-SSL
                        (f'imap.{domain}', 143),
                        (f'mail.{domain}', 143)
                    ]
            
            # Try each server configuration
            old_timeout = socket.getdefaulttimeout()
            for imap_server, port in imap_servers:
                try:
                    self.logger.info(f"Attempting connection to IMAP server: {imap_server}:{port}")
                    
                    # Set socket timeout to 10 seconds
                    socket.setdefaulttimeout(10)
                    
                    # Create IMAP connection
                    if port == 993:
                        self.connection = imaplib.IMAP4_SSL(imap_server, port)
                    else:
                        self.connection = imaplib.IMAP4(imap_server, port)
                        self.connection.starttls()
                    
                    self.connection.login(self.config.email_address, self.config.email_password)
                    
                    # Restore original timeout after successful connection
                    socket.setdefaulttimeout(old_timeout)
                    
                    self.logger.info(f"Successfully connected to mailbox via {imap_server}:{port}")
                    return True
                    
                except Exception as server_error:
                    self.logger.debug(f"Failed to connect to {imap_server}:{port} - {str(server_error)}")
                    if self.connection:
                        try:
                            self.connection.close()
                            self.connection.logout()
                        except:
                            pass
                        self.connection = None
                    continue
            
            # Restore timeout if all connections failed
            socket.setdefaulttimeout(old_timeout)
            
            # If we get here, all servers failed
            self.logger.error(f"Failed to connect to any IMAP server for domain {domain}")
            self.logger.error("Please check:")
            self.logger.error("1. Email credentials are correct")
            self.logger.error("2. IMAP is enabled for this email account")
            self.logger.error("3. Network connectivity and firewall settings")
            return False
            
        except Exception as e:
            self.logger.error(f"Error connecting to mailbox: {str(e)}")
            return False
    
    def disconnect_from_mailbox(self):
        """Close IMAP connection"""
        try:
            if self.connection:
                self.connection.close()
                self.connection.logout()
                self.connection = None
                self.logger.debug("Disconnected from mailbox")
        except Exception as e:
            self.logger.error(f"Error disconnecting from mailbox: {str(e)}")
    
    def test_connection(self):
        """Test the email connection"""
        self.logger.info("Testing email connection...")
        if self.connect_to_mailbox():
            self.disconnect_from_mailbox()
            return True
        return False
    
    def decode_email_header(self, header):
        """Decode email header that might be encoded"""
        if header is None:
            return ""
        
        try:
            decoded_parts = decode_header(header)
            decoded_string = ""
            
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        decoded_string += part.decode(encoding)
                    else:
                        decoded_string += part.decode('utf-8', errors='ignore')
                else:
                    decoded_string += str(part)
            
            return decoded_string
        except Exception as e:
            self.logger.error(f"Error decoding header '{header}': {str(e)}")
            return str(header) if header else ""
    
    def parse_email_message(self, raw_email):
        """Parse raw email message and extract relevant information"""
        try:
            msg = email.message_from_bytes(raw_email)
            
            # Extract email information
            email_info = {
                'from': self.decode_email_header(msg.get('From', '')),
                'to': self.decode_email_header(msg.get('To', '')),
                'subject': self.decode_email_header(msg.get('Subject', '')),
                'date': self.decode_email_header(msg.get('Date', '')),
                'message_id': msg.get('Message-ID', ''),
            }
            
            # Extract body content
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                        except:
                            continue
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    body = ""
            
            email_info['body'] = body[:500]  # Limit body to first 500 chars
            
            return email_info
            
        except Exception as e:
            self.logger.error(f"Error parsing email message: {str(e)}")
            return None
    
    def is_from_bookeo(self, email_info):
        """Check if email is from Bookeo"""
        sender = email_info.get('from', '').lower()
        return self.config.bookeo_sender.lower() in sender
    
    def is_recent_email(self, email_info):
        """Check if email was received after last check"""
        if self.last_check_time is None:
            # If this is the first check, only consider emails from the last hour
            self.last_check_time = datetime.now() - timedelta(hours=1)
        
        try:
            # Parse email date
            date_str = email_info.get('date', '')
            if not date_str:
                return True  # If no date, consider it new
            
            # Simple date parsing (email dates can be complex)
            email_date = email.utils.parsedate_to_datetime(date_str)
            if email_date.tzinfo is None:
                # If no timezone info, assume UTC
                email_date = email_date.replace(tzinfo=email.utils.tzutc())
            
            # Convert to naive datetime for comparison
            email_date_naive = email_date.replace(tzinfo=None)
            
            return email_date_naive > self.last_check_time
            
        except Exception as e:
            self.logger.error(f"Error parsing email date '{date_str}': {str(e)}")
            return True  # If we can't parse the date, consider it new
    
    def check_for_bookeo_emails(self):
        """Check mailbox for new emails from Bookeo"""
        new_bookeo_emails = []
        
        try:
            # Connect to mailbox
            if not self.connect_to_mailbox():
                return new_bookeo_emails
            
            # Select INBOX
            self.connection.select('INBOX')
            
            # Search for emails from Bookeo
            search_criteria = f'FROM "{self.config.bookeo_sender}"'
            
            # If we have a last check time, search for recent emails
            if self.last_check_time:
                # Format date for IMAP search (DD-MMM-YYYY)
                since_date = self.last_check_time.strftime("%d-%b-%Y")
                search_criteria += f' SINCE {since_date}'
            
            self.logger.debug(f"Searching with criteria: {search_criteria}")
            
            # Perform search
            status, messages = self.connection.search(None, search_criteria)
            
            if status != 'OK':
                self.logger.error(f"Email search failed: {status}")
                return new_bookeo_emails
            
            # Get list of email IDs
            email_ids = messages[0].split()
            self.logger.debug(f"Found {len(email_ids)} potential emails")
            
            # Process each email
            for email_id in email_ids:
                try:
                    # Fetch email
                    status, email_data = self.connection.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        self.logger.error(f"Failed to fetch email {email_id}")
                        continue
                    
                    # Parse email
                    raw_email = email_data[0][1]
                    email_info = self.parse_email_message(raw_email)
                    
                    if email_info is None:
                        continue
                    
                    # Check if it's from Bookeo and is recent
                    if self.is_from_bookeo(email_info) and self.is_recent_email(email_info):
                        new_bookeo_emails.append(email_info)
                        self.logger.info(f"Found new Bookeo email: {email_info['subject']}")
                
                except Exception as e:
                    self.logger.error(f"Error processing email {email_id}: {str(e)}")
                    continue
            
            # Update last check time
            self.last_check_time = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error checking for Bookeo emails: {str(e)}")
        
        finally:
            self.disconnect_from_mailbox()
        
        return new_bookeo_emails
