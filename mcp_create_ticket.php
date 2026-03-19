<?php

require __DIR__ . '/mcp_bootstrap.php';

$raw = getenv('OST_MCP_PAYLOAD');
if ($raw === false || $raw === '') {
    $raw = stream_get_contents(STDIN);
}

$payload = json_decode($raw, true);
if (!is_array($payload)) {
    mcp_emit_error('Invalid JSON payload');
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
    mcp_emit_error('Ticket creation failed', $errors);
}

mcp_emit_json(array(
    'status' => 'success',
    'ticket_number' => $ticket->getNumber(),
    'ticket_id' => $ticket->getId(),
    'subject' => $ticket->getSubject(),
    'email' => $payload['email'] ?? '',
    'name' => $payload['name'] ?? '',
));