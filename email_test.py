#!/usr/bin/env python3
"""
Quick email authentication test
"""

import imaplib
import socket

def test_specific_login():
    """Test specific email login scenarios"""
    email = "robot@quantumescapesdanville.com"
    password = "Agentlogin1234!"
    
    # Most likely scenarios for this domain
    test_configs = [
        ("imap.gmail.com", 993, "Google Workspace"),
        ("outlook.office365.com", 993, "Microsoft 365"),
        ("imap.mail.yahoo.com", 993, "Yahoo Business"),
    ]
    
    for server, port, provider in test_configs:
        print(f"\nTesting {provider} ({server}:{port})")
        try:
            socket.setdefaulttimeout(8)
            conn = imaplib.IMAP4_SSL(server, port)
            
            # Try login
            try:
                conn.login(email, password)
                print(f"✅ SUCCESS: Connected via {provider}")
                
                # Test basic operations
                conn.select('INBOX')
                status, messages = conn.search(None, 'ALL')
                if status == 'OK':
                    email_count = len(messages[0].split()) if messages[0] else 0
                    print(f"📧 Found {email_count} emails in inbox")
                
                conn.logout()
                return server, port, provider
                
            except imaplib.IMAP4.error as e:
                error_msg = str(e).lower()
                if 'authentication failed' in error_msg or 'invalid credentials' in error_msg:
                    print(f"❌ Authentication failed for {provider}")
                    print("   Possible issues:")
                    print("   - Incorrect password")
                    print("   - Need App Password (for Gmail/Google Workspace)")
                    print("   - Two-factor authentication required")
                    print("   - Account not set up with this provider")
                else:
                    print(f"❌ IMAP error: {e}")
            except Exception as e:
                print(f"❌ Login error: {e}")
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        try:
            conn.logout()
        except:
            pass
    
    return None, None, None

if __name__ == "__main__":
    print("Testing email authentication...")
    server, port, provider = test_specific_login()
    
    if server:
        print(f"\n🎉 Working configuration: {provider}")
        print(f"Server: {server}:{port}")
    else:
        print("\n❌ Authentication failed with all major providers")
        print("\nNext steps:")
        print("1. Verify the email password is correct")
        print("2. Check if the email uses Google Workspace, Microsoft 365, or another provider")
        print("3. Enable App Passwords if using Gmail/Google")
        print("4. Contact the email administrator for IMAP settings")