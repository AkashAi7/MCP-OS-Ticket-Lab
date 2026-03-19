#!/usr/bin/env python3
"""
Sample Ticket Generator for osTicket
Creates various sample tickets with different priorities, statuses, and scenarios
"""

import mysql.connector
import random
from datetime import datetime, timedelta
import hashlib

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'osticket',
    'password': 'osticket123',
    'database': 'osticket'
}

# Sample ticket data
DEPARTMENTS = {
    1: "Support",
    2: "Sales", 
    3: "Technical Support"
}

TOPICS = {
    1: "General Inquiry",
    2: "Feedback",
    3: "Technical Support",
    4: "Billing",
    5: "Product Issue"
}

PRIORITIES = {
    1: "Low",
    2: "Normal",
    3: "High",
    4: "Emergency"
}

SAMPLE_TICKETS = [
    {
        'name': 'John Smith',
        'email': 'john.smith@example.com',
        'subject': 'Cannot access my account',
        'message': 'Hello, I have been trying to log in to my account for the past 2 hours but keep getting an error message saying "Invalid credentials". I have tried resetting my password twice but still cannot access my account. This is urgent as I need to access important documents. Please help!',
        'priority_id': 4,
        'topic_id': 3,
        'source': 'Web'
    },
    {
        'name': 'Sarah Johnson',
        'email': 'sarah.j@example.com',
        'subject': 'Billing inquiry - Duplicate charge',
        'message': 'I noticed that I was charged twice for my subscription this month. The first charge was on the 1st for $49.99 and another charge on the 3rd for the same amount. Could you please investigate and refund the duplicate charge?',
        'priority_id': 3,
        'topic_id': 4,
        'source': 'Email'
    },
    {
        'name': 'Michael Chen',
        'email': 'mchen@techcorp.com',
        'subject': 'Feature request - Dark mode',
        'message': 'I would love to see a dark mode option added to the application. Many users work late at night and the current bright interface can be straining on the eyes. This would greatly improve the user experience.',
        'priority_id': 1,
        'topic_id': 2,
        'source': 'Web'
    },
    {
        'name': 'Emily Rodriguez',
        'email': 'emily.r@example.com',
        'subject': 'Product not working after update',
        'message': 'After the latest update yesterday, the software crashes every time I try to export data. I have tried reinstalling but the issue persists. My system is Windows 11, version 22H2. Error code: 0x80070002. Please provide a solution ASAP.',
        'priority_id': 4,
        'topic_id': 5,
        'source': 'Web'
    },
    {
        'name': 'David Thompson',
        'email': 'david.t@example.com',
        'subject': 'Question about enterprise pricing',
        'message': 'Hi, I am interested in upgrading to an enterprise plan for our company (50+ users). Could you provide detailed pricing information and what additional features are included? Also, do you offer volume discounts?',
        'priority_id': 2,
        'topic_id': 1,
        'source': 'Web'
    },
    {
        'name': 'Lisa Wang',
        'email': 'lwang@startup.io',
        'subject': 'Integration with Slack not working',
        'message': 'I followed the integration guide to connect our workspace with Slack but notifications are not being sent. I have verified the webhook URL and permissions are correct. The test connection succeeds but actual notifications fail. Can you help troubleshoot?',
        'priority_id': 3,
        'topic_id': 3,
        'source': 'Email'
    },
    {
        'name': 'Robert Martinez',
        'email': 'robert.m@example.com',
        'subject': 'Data export feature issue',
        'message': 'When I try to export my data to CSV, the file downloads but is completely empty (0 KB). This happens with all export options - CSV, JSON, and XML. I need to export my data urgently for a presentation tomorrow.',
        'priority_id': 3,
        'topic_id': 5,
        'source': 'Web'
    },
    {
        'name': 'Jennifer Taylor',
        'email': 'jtaylor@consulting.com',
        'subject': 'Great product! Minor suggestion',
        'message': 'I have been using your product for 3 months now and I absolutely love it! Just wanted to suggest adding keyboard shortcuts for common actions. This would make navigation much faster for power users. Keep up the great work!',
        'priority_id': 1,
        'topic_id': 2,
        'source': 'Web'
    },
    {
        'name': 'Christopher Lee',
        'email': 'clee@example.com',
        'subject': 'Mobile app constantly crashing on iOS 17',
        'message': 'The mobile app crashes within seconds of opening on my iPhone 14 Pro running iOS 17.2. I have tried deleting and reinstalling, restarting my phone, and clearing the cache. Nothing works. Please fix this urgently!',
        'priority_id': 4,
        'topic_id': 5,
        'source': 'Email'
    },
    {
        'name': 'Amanda White',
        'email': 'awhite@enterprise.com',
        'subject': 'API rate limit too restrictive',
        'message': 'Our application needs to make frequent API calls but we are constantly hitting the rate limit (100 requests/hour). For our use case, we need at least 500 requests/hour. Is it possible to increase our limit or upgrade to a plan with higher limits?',
        'priority_id': 3,
        'topic_id': 3,
        'source': 'Web'
    },
    {
        'name': 'James Anderson',
        'email': 'janderson@example.com',
        'subject': 'Cannot upload files larger than 5MB',
        'message': 'I need to upload product documentation that is 8MB in size, but the system shows an error saying maximum file size is 5MB. This is a significant limitation. Can you increase the file size limit or allow me to upload in chunks?',
        'priority_id': 2,
        'topic_id': 3,
        'source': 'Web'
    },
    {
        'name': 'Patricia Garcia',
        'email': 'pgarcia@nonprofit.org',
        'subject': 'Non-profit discount inquiry',
        'message': 'Our organization is a registered 501(c)(3) non-profit. Do you offer any discounts or special pricing for non-profit organizations? We are very interested in your product but budget is a concern.',
        'priority_id': 1,
        'topic_id': 1,
        'source': 'Email'
    }
]

def create_connection():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def get_next_ticket_number(cursor):
    """Get the next available ticket number"""
    cursor.execute("SELECT MAX(CAST(number AS UNSIGNED)) FROM ost_ticket")
    result = cursor.fetchone()
    max_num = result[0] if result[0] else 100000
    return int(max_num) + 1

def create_ticket(cursor, ticket_data, ticket_number):
    """Create a ticket in the database"""
    now = datetime.now()
    created = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
    
    # Insert into ost_ticket
    ticket_sql = """
        INSERT INTO ost_ticket 
        (number, user_id, ticket_id, dept_id, topic_id, staff_id, team_id, 
         sla_id, ip_address, source, status_id, created, updated, duedate, 
         isanswered, isoverdue, isopen, reopened, closed, lastupdate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    status_id = random.choice([1, 2])  # 1=Open, 2=In Progress
    is_open = 1 if status_id in [1, 2] else 0
    
    ticket_values = (
        str(ticket_number),  # number (string)
        0,  # user_id (0 for guest)
        0,  # ticket_id (auto-generated)
        random.randint(1, 3),  # dept_id
        int(ticket_data['topic_id']),  # topic_id
        0,  # staff_id (unassigned)
        0,  # team_id
        0,  # sla_id
        f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",  # ip_address
        str(ticket_data['source']),  # source
        status_id,  # status_id
        created,  # created
        created,  # updated
        None,  # duedate
        0,  # isanswered
        0,  # isoverdue
        is_open,  # isopen
        None,  # reopened
        None,  # closed
        created  # lastupdate
    )
    
    cursor.execute(ticket_sql, ticket_values)
    ticket_id = cursor.lastrowid
    
    # Insert into ost_ticket__cdata (custom data)
    cdata_sql = """
        INSERT INTO ost_ticket__cdata (ticket_id, subject, priority_id)
        VALUES (%s, %s, %s)
    """
    cursor.execute(cdata_sql, (ticket_id, str(ticket_data['subject']), int(ticket_data['priority_id'])))
    
    # Insert into ost_thread (conversation thread)
    thread_sql = """
        INSERT INTO ost_thread (object_id, object_type, created)
        VALUES (%s, %s, %s)
    """
    cursor.execute(thread_sql, (ticket_id, 'T', created))
    thread_id = cursor.lastrowid
    
    # Insert into ost_thread_entry (initial message)
    entry_sql = """
        INSERT INTO ost_thread_entry 
        (thread_id, staff_id, user_id, type, poster, source, title, body, format, created, updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    poster = str(ticket_data['name'])
    body = str(ticket_data['message'])
    
    cursor.execute(entry_sql, (
        thread_id,
        0,  # staff_id
        0,  # user_id
        'M',  # type (M=Message)
        poster,
        str(ticket_data['source']),
        str(ticket_data['subject']),
        body,
        'html',  # format
        created,
        created
    ))
    
    # Insert into ost_ticket_email_info
    email_sql = """
        INSERT INTO ost_ticket_email_info (ticket_id, email, name)
        VALUES (%s, %s, %s)
    """
    cursor.execute(email_sql, (ticket_id, str(ticket_data['email']), str(ticket_data['name'])))
    
    return ticket_id, ticket_number

def main():
    """Main function to create sample tickets"""
    print("=" * 60)
    print("osTicket Sample Ticket Generator")
    print("=" * 60)
    
    conn = create_connection()
    if not conn:
        print("Failed to connect to database. Make sure osTicket containers are running.")
        return
    
    cursor = conn.cursor()
    
    try:
        # Check if tables exist
        cursor.execute("SHOW TABLES LIKE 'ost_ticket'")
        if not cursor.fetchone():
            print("Error: osTicket tables not found. Please complete the installation first.")
            return
        
        print(f"\nCreating {len(SAMPLE_TICKETS)} sample tickets...\n")
        
        ticket_number = get_next_ticket_number(cursor)
        created_tickets = []
        
        for i, ticket_data in enumerate(SAMPLE_TICKETS, 1):
            try:
                ticket_id, number = create_ticket(cursor, ticket_data, ticket_number)
                created_tickets.append({
                    'id': ticket_id,
                    'number': number,
                    'subject': ticket_data['subject'],
                    'priority': PRIORITIES.get(ticket_data['priority_id'], 'Unknown'),
                    'email': ticket_data['email']
                })
                print(f"✓ Created ticket #{number}: {ticket_data['subject'][:50]}...")
                ticket_number += 1
            except Exception as e:
                import traceback
                print(f"✗ Error creating ticket: {e}")
                print(f"Full error: {traceback.format_exc()}")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print(f"Successfully created {len(created_tickets)} tickets!")
        print("=" * 60)
        
        print("\n📊 Summary:")
        print(f"   Total tickets: {len(created_tickets)}")
        print(f"   Ticket range: #{created_tickets[0]['number']} - #{created_tickets[-1]['number']}")
        print(f"\n🌐 Access osTicket:")
        print(f"   User Portal: http://localhost:8080/")
        print(f"   Admin Panel: http://localhost:8080/scp/")
        print(f"   Default admin: admin / Admin1 (if using pre-built image)")
        
        print("\n📋 Sample tickets created:")
        for ticket in created_tickets[:5]:
            print(f"   • Ticket #{ticket['number']}: {ticket['subject']} [{ticket['priority']}]")
        if len(created_tickets) > 5:
            print(f"   ... and {len(created_tickets) - 5} more tickets")
        
    except Exception as e:
        import traceback
        print(f"\nError: {e}")
        print(f"Full traceback:\n{traceback.format_exc()}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
