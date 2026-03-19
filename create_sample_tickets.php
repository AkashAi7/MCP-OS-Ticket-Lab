<?php

chdir('/var/www/html');
require 'main.inc.php';

$_SERVER['REMOTE_ADDR'] = $_SERVER['REMOTE_ADDR'] ?: '127.0.0.1';

$tickets = array(
    array(
        'name' => 'John Smith',
        'email' => 'john.smith@example.com',
        'subject' => 'Cannot access my account',
        'message' => 'I have been trying to log in for the last two hours and password reset is not working. I need access before my next customer call.',
        'source' => 'Web',
    ),
    array(
        'name' => 'Sarah Johnson',
        'email' => 'sarah.j@example.com',
        'subject' => 'Duplicate billing charge this month',
        'message' => 'I can see two identical subscription charges on my card statement. Please confirm which one will be refunded.',
        'source' => 'Email',
    ),
    array(
        'name' => 'Michael Chen',
        'email' => 'mchen@techcorp.com',
        'subject' => 'Feature request for dark mode',
        'message' => 'Our support staff work night shifts and would benefit from a dark theme in the portal.',
        'source' => 'Web',
    ),
    array(
        'name' => 'Emily Rodriguez',
        'email' => 'emily.r@example.com',
        'subject' => 'Application crashes after latest update',
        'message' => 'Exporting reports started crashing immediately after yesterday\'s update. This is blocking our daily operations.',
        'source' => 'API',
    ),
    array(
        'name' => 'David Thompson',
        'email' => 'david.t@example.com',
        'subject' => 'Question about enterprise pricing',
        'message' => 'We are evaluating the platform for roughly 50 agents. Please send details about enterprise pricing and support options.',
        'source' => 'Web',
    ),
    array(
        'name' => 'Lisa Wang',
        'email' => 'lwang@startup.io',
        'subject' => 'Slack integration not delivering notifications',
        'message' => 'The webhook validates successfully, but no notifications arrive in Slack when new tickets are opened.',
        'source' => 'Email',
    ),
    array(
        'name' => 'Robert Martinez',
        'email' => 'robert.m@example.com',
        'subject' => 'CSV export downloads as an empty file',
        'message' => 'All export formats are generating empty files for me. I need the data for a presentation tomorrow morning.',
        'source' => 'Web',
    ),
    array(
        'name' => 'Jennifer Taylor',
        'email' => 'jtaylor@consulting.com',
        'subject' => 'Great product with one small suggestion',
        'message' => 'Keyboard shortcuts for common actions would make the agent experience much faster for heavy users.',
        'source' => 'Web',
    ),
    array(
        'name' => 'Christopher Lee',
        'email' => 'clee@example.com',
        'subject' => 'iOS app crashes immediately on launch',
        'message' => 'The mobile app closes within seconds on iOS 17.2, even after reinstalling and rebooting the device.',
        'source' => 'Email',
    ),
    array(
        'name' => 'Amanda White',
        'email' => 'awhite@enterprise.com',
        'subject' => 'API rate limit is too restrictive for our workload',
        'message' => 'We need several hundred API calls per hour for our integration and the current rate limit is too low.',
        'source' => 'API',
    ),
    array(
        'name' => 'James Anderson',
        'email' => 'janderson@example.com',
        'subject' => 'Unable to upload files larger than 5 MB',
        'message' => 'Our support team needs to attach larger product manuals. Please confirm whether the upload limit can be raised.',
        'source' => 'Web',
    ),
    array(
        'name' => 'Patricia Garcia',
        'email' => 'pgarcia@nonprofit.org',
        'subject' => 'Do you offer a non-profit discount?',
        'message' => 'We are a registered non-profit and would like to know whether discounted pricing is available.',
        'source' => 'Email',
    ),
);

$created = array();

foreach ($tickets as $ticket) {
    $errors = array();
    $vars = array(
        'deptId' => 1,
        'topicId' => 1,
        'name' => $ticket['name'],
        'email' => $ticket['email'],
        'subject' => $ticket['subject'],
        'message' => $ticket['message'],
        'source' => $ticket['source'],
        'ip' => '127.0.0.1',
    );

    $createdTicket = Ticket::create($vars, $errors, 'api', false, false);
    if (!$createdTicket) {
        fwrite(STDERR, sprintf("Failed to create sample ticket '%s': %s\n",
            $ticket['subject'], json_encode($errors)));
        exit(1);
    }

    $created[] = $createdTicket->getNumber();
}

echo sprintf("Created %d sample tickets: %s\n", count($created), implode(', ', $created));