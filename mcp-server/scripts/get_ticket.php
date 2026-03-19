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
if (!is_array($payload) || empty($payload['ticket_number'])) {
    fwrite(STDERR, json_encode(array('error' => 'ticket_number is required')));
    exit(1);
}

$ticket = Ticket::lookupByNumber($payload['ticket_number']);
if (!$ticket) {
    fwrite(STDERR, json_encode(array('error' => 'Ticket not found')));
    exit(1);
}

$status = $ticket->getStatus();
$owner = $ticket->getOwner();
$thread = $ticket->getThread();
$lastMessage = $thread ? $thread->getLastMessage() : null;

emit_json(array(
    'ticket_number' => $ticket->getNumber(),
    'ticket_id' => $ticket->getId(),
    'subject' => $ticket->getSubject(),
    'status' => $status ? $status->getName() : null,
    'email' => $ticket->getEmail(),
    'owner' => $owner ? (string) $owner : null,
    'dept' => $ticket->getDeptName(),
    'source' => $ticket->getSource(),
    'created' => $ticket->getCreateDate(),
    'updated' => $ticket->getLastUpdate(),
    'last_message' => $lastMessage ? (string) $lastMessage->getBody() : null,
    'url' => $ticket->getLink(),
));