#!/usr/bin/env python3
"""
Sample Ticket Generator for osTicket using HTTP API
Creates sample tickets via osTicket's public ticket creation API
"""

import requests
import random
from datetime import datetime

# osTicket API endpoint
OST_URL = "http://localhost:8080"
API_ENDPOINT = f"{OST_URL}/api/tickets.json"

# You need to get your API key from: Admin Panel -> Manage -> API Keys
# For this demo, we'll create tickets via the public form instead
PUBLIC_ENDPOINT = f"{OST_URL}/api/http.php/tickets.json"

# Sample ticket data
SAMPLE_TICKETS = [
    {
        'name': 'John Smith',
        'email': 'john.smith@example.com',
        'subject': 'Cannot access my account',
        'message': 'Hello, I have been trying to log in to my account for the past 2 hours but keep getting an error message saying "Invalid credentials". I have tried resetting my password twice but still cannot access my account. This is urgent as I need to access important documents. Please help!',
        'priority': 'urgent'
    },
    {
        'name': 'Sarah Johnson',
        'email': 'sarah.j@example.com',
        'subject': 'Billing inquiry - Duplicate charge',
        'message': 'I noticed that I was charged twice for my subscription this month. The first charge was on the 1st for $49.99 and another charge on the 3rd for the same amount. Could you please investigate and refund the duplicate charge?',
        'priority': 'high'
    },
    {
        'name': 'Michael Chen',
        'email': 'mchen@techcorp.com',
        'subject': 'Feature request - Dark mode',
        'message': 'I would love to see a dark mode option added to the application. Many users work late at night and the current bright interface can be straining on the eyes. This would greatly improve the user experience.',
        'priority': 'low'
    },
    {
        'name': 'Emily Rodriguez',
        'email': 'emily.r@example.com',
        'subject': 'Product not working after update',
        'message': 'After the latest update yesterday, the software crashes every time I try to export data. I have tried reinstalling but the issue persists. My system is Windows 11, version 22H2. Error code: 0x80070002. Please provide a solution ASAP.',
        'priority': 'emergency'
    },
    {
        'name': 'David Thompson',
        'email': 'david.t@example.com',
        'subject': 'Question about enterprise pricing',
        'message': 'Hi, I am interested in upgrading to an enterprise plan for our company (50+ users). Could you provide detailed pricing information and what additional features are included? Also, do you offer volume discounts?',
        'priority': 'normal'
    },
    {
        'name': 'Lisa Wang',
        'email': 'lwang@startup.io',
        'subject': 'Integration with Slack not working',
        'message': 'I followed the integration guide to connect our workspace with Slack but notifications are not being sent. I have verified the webhook URL and permissions are correct. The test connection succeeds but actual notifications fail. Can you help troubleshoot?',
        'priority': 'high'
    },
    {
        'name': 'Robert Martinez',
        'email': 'robert.m@example.com',
        'subject': 'Data export feature issue',
        'message': 'When I try to export my data to CSV, the file downloads but is completely empty (0 KB). This happens with all export options - CSV, JSON, and XML. I need to export my data urgently for a presentation tomorrow.',
        'priority': 'high'
    },
    {
        'name': 'Jennifer Taylor',
        'email': 'jtaylor@consulting.com',
        'subject': 'Great product! Minor suggestion',
        'message': 'I have been using your product for 3 months now and I absolutely love it! Just wanted to suggest adding keyboard shortcuts for common actions. This would make navigation much faster for power users. Keep up the great work!',
        'priority': 'low'
    },
    {
        'name': 'Christopher Lee',
        'email': 'clee@example.com',
        'subject': 'Mobile app constantly crashing on iOS 17',
        'message': 'The mobile app crashes within seconds of opening on my iPhone 14 Pro running iOS 17.2. I have tried deleting and reinstalling, restarting my phone, and clearing the cache. Nothing works. Please fix this urgently!',
        'priority': 'emergency'
    },
    {
        'name': 'Amanda White',
        'email': 'awhite@enterprise.com',
        'subject': 'API rate limit too restrictive',
        'message': 'Our application needs to make frequent API calls but we are constantly hitting the rate limit (100 requests/hour). For our use case, we need at least 500 requests/hour. Is it possible to increase our limit or upgrade to a plan with higher limits?',
        'priority': 'high'
    },
    {
        'name': 'James Anderson',
        'email': 'janderson@example.com',
        'subject': 'Cannot upload files larger than 5MB',
        'message': 'I need to upload product documentation that is 8MB in size, but the system shows an error saying maximum file size is 5MB. This is a significant limitation. Can you increase the file size limit or allow me to upload in chunks?',
        'priority': 'normal'
    },
    {
        'name': 'Patricia Garcia',
        'email': 'pgarcia@nonprofit.org',
        'subject': 'Non-profit discount inquiry',
        'message': 'Our organization is a registered 501(c)(3) non-profit. Do you offer any discounts or special pricing for non-profit organizations? We are very interested in your product but budget is a concern.',
        'priority': 'low'
    }
]

def create_ticket_via_web(ticket_data):
    """Create a ticket using the public web form"""
    # Prepare the data for submission
    data = {
        'name': ticket_data['name'],
        'email': ticket_data['email'],
        'phone': '',
        'subject': ticket_data['subject'],
        'message': ticket_data['message'],
        'topicId': '1',  # General Inquiry
        'ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }
    
    try:
        response = requests.post(
            f"{OST_URL}/open.php",
            data=data,
            timeout=10
        )
        return response.status_code == 200 or "ticket" in response.text.lower()
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Main function to create sample tickets"""
    print("=" * 60)
    print("osTicket Sample Ticket Generator (Web Form Method)")
    print("=" * 60)
    print(f"\nosTicket URL: {OST_URL}")
    print(f"Creating {len(SAMPLE_TICKETS)} sample tickets via web form...\n")
    
    created_count = 0
    
    for i, ticket_data in enumerate(SAMPLE_TICKETS, 1):
        print(f"[{i}/{len(SAMPLE_TICKETS)}] Creating: {ticket_data['subject'][:45]}...", end=" ")
        
        if create_ticket_via_web(ticket_data):
            created_count += 1
            print("✓")
        else:
            print("✗")
    
    print("\n" + "=" * 60)
    print(f"Completed! Created {created_count}/{len(SAMPLE_TICKETS)} tickets")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print(f"   1. View tickets: {OST_URL}/scp/ (Admin Panel)")
    print(f"   2. User portal: {OST_URL}/")
    print("\n💡 Note: Tickets created via web form will appear as 'Open' status")
    print("   You can assign them to staff, add responses, and change status in the admin panel.")

if __name__ == "__main__":
    main()
