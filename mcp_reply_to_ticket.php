<?php

require __DIR__ . '/mcp_bootstrap.php';

$raw = getenv('OST_MCP_PAYLOAD');
if ($raw === false || $raw === '') {
    $raw = stream_get_contents(STDIN);
}

$payload = json_decode($raw, true);
if (!is_array($payload) || empty($payload['ticket_id']) || empty($payload['message'])) {
    mcp_emit_error('ticket_id and message are required');
}

$ticket = Ticket::lookupByNumber($payload['ticket_id']);
if (!$ticket) {
    $ticket = Ticket::lookup($payload['ticket_id']);
}

if (!$ticket) {
    mcp_emit_error('Ticket not found', array('ticket_id' => $payload['ticket_id']));
}

$staff = Staff::lookup(1);
if (!$staff) {
    mcp_emit_error('Default staff user not found');
}

$vars = array(
    'response' => $payload['message'],
    'reply_status_id' => $ticket->getStatusId(),
);

$errors = array();
$reply = $ticket->postReply($vars, $errors, $staff, false);
if (!$reply) {
    mcp_emit_error('Reply failed', $errors);
}

mcp_emit_json(array(
    'status' => 'success',
    'ticket_number' => $ticket->getNumber(),
    'thread_entry_id' => method_exists($reply, 'getId') ? $reply->getId() : null,
));