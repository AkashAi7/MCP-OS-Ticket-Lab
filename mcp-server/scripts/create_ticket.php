<?php

chdir('/var/www/html');
require 'main.inc.php';

function emit_json($data) {
    $json = json_encode($data, JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
    if ($json === false) {
        fwrite(STDERR, json_encode(array('error' => 'JSON encoding failed', 'details' => json_last_error_msg())));
        exit(1);
    }
    echo $json;
}

$raw = getenv('OST_MCP_PAYLOAD');
if ($raw === false || $raw === '') {
    $raw = stream_get_contents(STDIN);
}

$payload = json_decode($raw, true);
if (!is_array($payload)) {
    fwrite(STDERR, json_encode(array('error' => 'Invalid JSON payload')));
    exit(1);
}

$errors = array();
$vars = array(
    'deptId' => 1,
    'topicId' => (int) ($payload['topic_id'] ?? 1),
    'name' => $payload['name'] ?? '',
    'email' => $payload['email'] ?? '',
    'subject' => $payload['subject'] ?? '',
    'message' => $payload['message'] ?? '',
    'source' => $payload['source'] ?? 'API',
    'ip' => '127.0.0.1',
);

$ticket = Ticket::create($vars, $errors, 'api', false, false);
if (!$ticket) {
    fwrite(STDERR, json_encode(array('error' => 'Ticket creation failed', 'details' => $errors)));
    exit(1);
}

emit_json(array(
    'status' => 'success',
    'ticket_number' => $ticket->getNumber(),
    'ticket_id' => $ticket->getId(),
    'subject' => $ticket->getSubject(),
    'email' => $payload['email'] ?? '',
    'name' => $payload['name'] ?? '',
));