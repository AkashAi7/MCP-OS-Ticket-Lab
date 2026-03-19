<?php

require __DIR__ . '/mcp_bootstrap.php';

$raw = getenv('OST_MCP_PAYLOAD');
if ($raw === false || $raw === '') {
    $raw = stream_get_contents(STDIN);
}

$payload = json_decode($raw, true);
if (!is_array($payload) || empty($payload['ticket_number'])) {
    mcp_emit_error('A ticket_number value is required');
}

$ticket = Ticket::lookupByNumber($payload['ticket_number']);
if (!$ticket) {
    mcp_emit_error('Ticket not found', array('ticket_number' => $payload['ticket_number']));
}

$thread = $ticket->getThread();
mcp_emit_json(array(
    'status' => 'success',
    'ticket_id' => $ticket->getId(),
    'ticket_number' => $ticket->getNumber(),
    'subject' => $ticket->getSubject(),
    'status_name' => $ticket->getStatus() ? $ticket->getStatus()->getName() : null,
    'email' => $ticket->getEmail(),
    'name' => $ticket->getName(),
    'department' => $ticket->getDeptName(),
    'thread_id' => $thread ? $thread->getId() : null,
));