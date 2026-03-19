-- Sample Tickets for osTicket
-- This script creates diverse sample tickets with different priorities and scenarios

-- Set variables for ticket numbers (adjust based on your current max ticket number)
SET @ticket_start = 100001;
SET @now = NOW();

-- Ticket 1: High Priority - Account Access Issue
INSERT INTO ost_ticket (number, dept_id, topic_id, status_id, source, created, updated, isopen, isanswered) 
VALUES (@ticket_start, 1, 3, 1, 'Web', DATE_SUB(@now, INTERVAL 2 DAY), DATE_SUB(@now, INTERVAL 2 DAY), 1, 0);
SET @ticket_id1 = LAST_INSERT_ID();

INSERT INTO ost_ticket__cdata (ticket_id, subject, priority_id) 
VALUES (@ticket_id1, 'Cannot access my account', 4);

INSERT INTO ost_thread (object_id, object_type, created) 
VALUES (@ticket_id1, 'T', DATE_SUB(@now, INTERVAL 2 DAY));
SET @thread_id1 = LAST_INSERT_ID();

INSERT INTO ost_thread_entry (thread_id, type, poster, source, title, body, format, created) 
VALUES (@thread_id1, 'M', 'John Smith', 'Web', 'Cannot access my account',
'Hello, I have been trying to log in to my account for the past 2 hours but keep getting an error message saying "Invalid credentials". I have tried resetting my password twice but still cannot access my account. This is urgent as I need to access important documents. Please help!',
'html', DATE_SUB(@now, INTERVAL 2 DAY));

INSERT INTO ost_ticket_email_info (ticket_id, email, name) 
VALUES (@ticket_id1, 'john.smith@example.com', 'John Smith');

-- Ticket 2: High Priority - Billing Issue
INSERT INTO ost_ticket (number, dept_id, topic_id, status_id, source, created, updated, isopen, isanswered) 
VALUES (@ticket_start + 1, 1, 4, 1, 'Email', DATE_SUB(@now, INTERVAL 5 DAY), DATE_SUB(@now, INTERVAL 5 DAY), 1, 0);
SET @ticket_id2 = LAST_INSERT_ID();

INSERT INTO ost_ticket__cdata (ticket_id, subject, priority_id) 
VALUES (@ticket_id2, 'Billing inquiry - Duplicate charge', 3);

INSERT INTO ost_thread (object_id, object_type, created) 
VALUES (@ticket_id2, 'T', DATE_SUB(@now, INTERVAL 5 DAY));
SET @thread_id2 = LAST_INSERT_ID();

INSERT INTO ost_thread_entry (thread_id, type, poster, source, title, body, format, created) 
VALUES (@thread_id2, 'M', 'Sarah Johnson', 'Email', 'Billing inquiry - Duplicate charge',
'I noticed that I was charged twice for my subscription this month. The first charge was on the 1st for $49.99 and another charge on the 3rd for the same amount. Could you please investigate and refund the duplicate charge?',
'html', DATE_SUB(@now, INTERVAL 5 DAY));

INSERT INTO ost_ticket_email_info (ticket_id, email, name) 
VALUES (@ticket_id2, 'sarah.j@example.com', 'Sarah Johnson');

-- Ticket 3: Low Priority - Feature Request
INSERT INTO ost_ticket (number, dept_id, topic_id, status_id, source, created, updated, isopen, isanswered) 
VALUES (@ticket_start + 2, 1, 2, 1, 'Web', DATE_SUB(@now, INTERVAL 10 DAY), DATE_SUB(@now, INTERVAL 10 DAY), 1, 0);
SET @ticket_id3 = LAST_INSERT_ID();

INSERT INTO ost_ticket__cdata (ticket_id, subject, priority_id) 
VALUES (@ticket_id3, 'Feature request - Dark mode', 1);

INSERT INTO ost_thread (object_id, object_type, created) 
VALUES (@ticket_id3, 'T', DATE_SUB(@now, INTERVAL 10 DAY));
SET @thread_id3 = LAST_INSERT_ID();

INSERT INTO ost_thread_entry (thread_id, type, poster, source, title, body, format, created) 
VALUES (@thread_id3, 'M', 'Michael Chen', 'Web', 'Feature request - Dark mode',
'I would love to see a dark mode option added to the application. Many users work late at night and the current bright interface can be straining on the eyes. This would greatly improve the user experience.',
'html', DATE_SUB(@now, INTERVAL 10 DAY));

INSERT INTO ost_ticket_email_info (ticket_id, email, name) 
VALUES (@ticket_id3, 'mchen@techcorp.com', 'Michael Chen');

-- Ticket 4: Emergency - Application Crash
INSERT INTO ost_ticket (number, dept_id, topic_id, status_id, source, created, updated, isopen, isanswered) 
VALUES (@ticket_start + 3, 1, 5, 1, 'Web', DATE_SUB(@now, INTERVAL 1 DAY), DATE_SUB(@now, INTERVAL 1 DAY), 1, 0);
SET @ticket_id4 = LAST_INSERT_ID();

INSERT INTO ost_ticket__cdata (ticket_id, subject, priority_id) 
VALUES (@ticket_id4, 'Product not working after update', 4);

INSERT INTO ost_thread (object_id, object_type, created) 
VALUES (@ticket_id4, 'T', DATE_SUB(@now, INTERVAL 1 DAY));
SET @thread_id4 = LAST_INSERT_ID();

INSERT INTO ost_thread_entry (thread_id, type, poster, source, title, body, format, created) 
VALUES (@thread_id4, 'M', 'Emily Rodriguez', 'Web', 'Product not working after update',
'After the latest update yesterday, the software crashes every time I try to export data. I have tried reinstalling but the issue persists. My system is Windows 11, version 22H2. Error code: 0x80070002. Please provide a solution ASAP.',
'html', DATE_SUB(@now, INTERVAL 1 DAY));

INSERT INTO ost_ticket_email_info (ticket_id, email, name) 
VALUES (@ticket_id4, 'emily.r@example.com', 'Emily Rodriguez');

-- Ticket 5: Normal Priority - Sales Inquiry
INSERT INTO ost_ticket (number, dept_id, topic_id, status_id, source, created, updated, isopen, isanswered) 
VALUES (@ticket_start + 4, 2, 1, 1, 'Web', DATE_SUB(@now, INTERVAL 3 DAY), DATE_SUB(@now, INTERVAL 3 DAY), 1, 0);
SET @ticket_id5 = LAST_INSERT_ID();

INSERT INTO ost_ticket__cdata (ticket_id, subject, priority_id) 
VALUES (@ticket_id5, 'Question about enterprise pricing', 2);

INSERT INTO ost_thread (object_id, object_type, created) 
VALUES (@ticket_id5, 'T', DATE_SUB(@now, INTERVAL 3 DAY));
SET @thread_id5 = LAST_INSERT_ID();

INSERT INTO ost_thread_entry (thread_id, type, poster, source, title, body, format, created) 
VALUES (@thread_id5, 'M', 'David Thompson', 'Web', 'Question about enterprise pricing',
'Hi, I am interested in upgrading to an enterprise plan for our company (50+ users). Could you provide detailed pricing information and what additional features are included? Also, do you offer volume discounts?',
'html', DATE_SUB(@now, INTERVAL 3 DAY));

INSERT INTO ost_ticket_email_info (ticket_id, email, name) 
VALUES (@ticket_id5, 'david.t@example.com', 'David Thompson');

SELECT 'Sample tickets created successfully!' AS Result;
SELECT CONCAT('Created ', COUNT(*), ' sample tickets') AS Summary FROM ost_ticket WHERE number >= @ticket_start;
