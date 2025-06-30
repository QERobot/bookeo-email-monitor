#!/usr/bin/env python3
"""
Simple connection test to debug email server issues
"""

import socket
import imaplib
import sys

def test_imap_servers():
    """Test various IMAP server configurations"""
    domain = "quantumescapesdanville.com"
    
    # List of IMAP servers to try
    servers_to_try = [
        ("imap.quantumescapesdanville.com", 993),
        ("mail.quantumescapesdanville.com", 993),
        ("quantumescapesdanville.com", 993),
        ("imap.quantumescapesdanville.com", 143),
        ("mail.quantumescapesdanville.com", 143),
        # Common hosting providers
        ("imap.gmail.com", 993),  # in case it's forwarded to Gmail
        ("outlook.office365.com", 993)  # in case it's using Office365
    ]
    
    for server, port in servers_to_try:
        print(f"\nTesting {server}:{port}")
        
        # Test basic connectivity
        try:
            socket.setdefaulttimeout(5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((server, port))
            sock.close()
            
            if result == 0:
                print(f"✓ Port {port} is open on {server}")
                
                # Try IMAP connection
                try:
                    if port == 993:
                        conn = imaplib.IMAP4_SSL(server, port)
                    else:
                        conn = imaplib.IMAP4(server, port)
                        conn.starttls()
                    
                    print(f"✓ IMAP connection successful to {server}:{port}")
                    
                    # Try to login
                    try:
                        conn.login("robot@quantumescapesdanville.com", "Agentlogin1234!")
                        print(f"✓ Login successful to {server}:{port}")
                        conn.logout()
                        return server, port
                    except Exception as e:
                        print(f"✗ Login failed: {str(e)}")
                        try:
                            conn.logout()
                        except:
                            pass
                        
                except Exception as e:
                    print(f"✗ IMAP connection failed: {str(e)}")
            else:
                print(f"✗ Port {port} is closed or unreachable on {server}")
                
        except Exception as e:
            print(f"✗ Network error: {str(e)}")
    
    return None, None

if __name__ == "__main__":
    print("Testing IMAP server connectivity...")
    server, port = test_imap_servers()
    
    if server:
        print(f"\n🎉 Working server found: {server}:{port}")
    else:
        print("\n❌ No working IMAP servers found")
        print("\nPossible issues:")
        print("1. Domain doesn't have IMAP server configured")
        print("2. Firewall blocking connections")
        print("3. Email is hosted by a third-party provider")
        print("4. Credentials are incorrect")