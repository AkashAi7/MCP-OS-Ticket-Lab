# Sample Tickets for osTicket

This directory contains tools to populate your osTicket installation with realistic sample tickets for testing and demonstration purposes.

## 📋 What's Included

### Sample Tickets Created

The scripts create **12 diverse sample tickets** covering various scenarios:

1. **High Priority Tickets:**
   - Account access issues (Emergency)
   - Application crashes after updates (Emergency)
   - Mobile app crashes on iOS (Emergency)
   - Billing duplicate charges (High)
   - Integration failures (High)
   - API rate limiting issues (High)

2. **Medium Priority Tickets:**
   - Enterprise pricing inquiries (Normal)
   - File upload limitations (Normal)

3. **Low Priority Tickets:**
   - Feature requests (Dark mode)
   - Positive feedback with suggestions
   - Non-profit discount inquiries

4. **Technical Issues:**
   - Data export problems
   - Integration failures (Slack)
   - Mobile app crashes
   - API rate limits

5. **Business Inquiries:**
   - Enterprise pricing
   - Non-profit discounts
   - Volume discounts

## 🚀 Methods to Create Sample Tickets

### Method 0: One-click local installer

```powershell
.\install-local.ps1 -ResetData
```

This is the preferred local path. It installs osTicket and creates sample tickets using osTicket's internal PHP APIs so the generated data matches the installed schema.

### Method 1: Python Script (Recommended)

**Prerequisites:**
```powershell
pip install mysql-connector-python
```

**Run the script:**
```powershell
python create_sample_tickets.py
```

**Features:**
- ✅ Creates 12 realistic tickets with full details
- ✅ Randomized creation dates (0-30 days ago)
- ✅ Various priorities (Low, Normal, High, Emergency)
- ✅ Different sources (Web, Email)
- ✅ Complete ticket threads with messages
- ✅ Progress feedback during creation

### Method 2: Direct SQL Import

**Using Docker:**
```powershell
Get-Content sample_tickets.sql | docker exec -i osticket-mysql mysql -uosticket -posticket123 osticket
```

**Or using MySQL client:**
```powershell
mysql -h localhost -P 3306 -u osticket -posticket123 osticket < sample_tickets.sql
```

### Method 3: phpMyAdmin

1. Open http://localhost:8081/
2. Login with credentials:
   - Username: `osticket`
   - Password: `osticket123`
3. Select `osticket` database
4. Go to SQL tab
5. Paste contents of `sample_tickets.sql`
6. Click "Go"

## 📊 Sample Ticket Details

| # | Subject | Priority | Category | Source |
|---|---------|----------|----------|--------|
| 1 | Cannot access my account | Emergency | Technical | Web |
| 2 | Billing inquiry - Duplicate charge | High | Billing | Email |
| 3 | Feature request - Dark mode | Low | Feedback | Web |
| 4 | Product not working after update | Emergency | Product Issue | Web |
| 5 | Question about enterprise pricing | Normal | Sales | Web |
| 6 | Integration with Slack not working | High | Technical | Email |
| 7 | Data export feature issue | High | Product Issue | Web |
| 8 | Great product! Minor suggestion | Low | Feedback | Web |
| 9 | Mobile app constantly crashing on iOS 17 | Emergency | Product Issue | Email |
| 10 | API rate limit too restrictive | High | Technical | Web |
| 11 | Cannot upload files larger than 5MB | Normal | Technical | Web |
| 12 | Non-profit discount inquiry | Low | General | Email |

## 🎯 Use Cases for Testing

These sample tickets are perfect for:

### 1. **Priority Management Testing**
- Emergency tickets requiring immediate attention
- High priority tickets for urgent issues
- Normal tickets for standard support
- Low priority tickets for enhancements

### 2. **Department Routing**
- Support department tickets
- Sales inquiries
- Technical support requests
- Billing issues

### 3. **Workflow Testing**
- Ticket assignment workflows
- SLA compliance testing
- Escalation procedures
- Auto-responses

### 4. **Reporting & Analytics**
- Ticket volume analysis
- Response time metrics
- Priority distribution
- Department workload

### 5. **Agent Training**
- Customer service scenarios
- Technical troubleshooting
- Handling difficult situations
- Professional communication

### 6. **Integration Testing**
- Email piping
- API functionality
- Notification systems
- Third-party integrations

## 🔧 Advanced Customization

### Modify Ticket Data

Edit `create_sample_tickets.py` to customize:

```python
SAMPLE_TICKETS = [
    {
        'name': 'Your Name',
        'email': 'your.email@example.com',
        'subject': 'Your Subject',
        'message': 'Your detailed message...',
        'priority_id': 1-4,  # 1=Low, 2=Normal, 3=High, 4=Emergency
        'topic_id': 1-5,     # Topic/Category
        'source': 'Web' or 'Email'
    },
    # Add more tickets...
]
```

### Add Staff Responses

After creating tickets, you can add agent responses:

```sql
-- Add a staff response to ticket #100001
INSERT INTO ost_thread_entry (thread_id, staff_id, type, poster, title, body, format, created)
SELECT t.thread_id, 1, 'R', 'Support Agent', 'Re: Your Ticket', 
'Thank you for contacting us. We are looking into your issue.',
'html', NOW()
FROM ost_thread t 
JOIN ost_ticket tk ON t.object_id = tk.ticket_id 
WHERE tk.number = 100001;
```

### Change Ticket Status

```sql
-- Mark ticket as resolved
UPDATE ost_ticket SET status_id = 3, isopen = 0 WHERE number = 100001;

-- Assign to staff member (staff_id = 1)
UPDATE ost_ticket SET staff_id = 1 WHERE number = 100002;
```

## 🎨 Ticket Priorities Explained

| Priority | ID | Use Case | Response Time |
|----------|----|----|---------------|
| **Low** | 1 | Feature requests, general inquiries | 72 hours |
| **Normal** | 2 | Standard support questions | 24 hours |
| **High** | 3 | Service affecting issues | 4 hours |
| **Emergency** | 4 | Critical system failures | 1 hour |

## 📈 Next Steps

After creating sample tickets:

1. **Access the Admin Panel**: http://localhost:8080/scp/
   - View all tickets
   - Assign tickets to staff
   - Change priorities and statuses
   - Add internal notes

2. **Test the User Portal**: http://localhost:8080/
   - Submit new tickets
   - Check ticket status
   - View responses

3. **Configure Email**:
   - Set up email piping
   - Configure SMTP for outgoing emails
   - Test email notifications

4. **Set up Automation**:
   - Create auto-responders
   - Set up SLA plans
   - Configure help topics

5. **Customize**:
   - Add custom fields
   - Create ticket filters
   - Set up departments and teams

## 🐛 Troubleshooting

### Python script fails to connect
```powershell
# Check if containers are running
docker ps

# Verify MySQL is accessible
docker exec osticket-mysql mysql -uosticket -posticket123 -e "SHOW DATABASES;"
```

### Tickets not appearing in osTicket
```powershell
# Clear osTicket cache
docker exec osticket-web rm -rf /var/www/html/data/cache/*

# Restart osTicket container
docker restart osticket-web
```

### Permission errors
```powershell
# Ensure proper permissions
docker exec osticket-web chown -R www-data:www-data /var/www/html/
```

## 📚 Additional Resources

- [osTicket Documentation](https://docs.osticket.com/)
- [osTicket Forum](https://forum.osticket.com/)
- [API Documentation](https://docs.osticket.com/en/latest/Developer%20Documentation/API/Tickets.html)

## 💡 Tips

- Start with a few tickets to test workflows
- Gradually add more as you configure the system
- Use different email addresses to simulate multiple customers
- Test email notifications with real email addresses
- Create staff accounts to test assignment features
