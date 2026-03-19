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
if (!is_array($payload) || empty($payload['ticket_id']) || empty($payload['message'])) {
    fwrite(STDERR, json_encode(array('error' => 'ticket_id and message are required')));
    exit(1);
}

$ticket = Ticket::lookupByNumber($payload['ticket_id']);
if (!$ticket && ctype_digit((string) $payload['ticket_id'])) {
    $ticket = Ticket::lookup((int) $payload['ticket_id']);
}

if (!$ticket) {
    fwrite(STDERR, json_encode(array('error' => 'Ticket not found')));
    exit(1);
}

$errors = array();
$vars = array(
    'response' => $payload['message'],
    'poster' => 'MCP Assistant',
    'staffId' => 0,
    'alert' => false,
    'reply-to' => 'none',
    'ccs' => array(),
    'ip_address' => '127.0.0.1',
);

$response = $ticket->postReply($vars, $errors, false, false);
if (!$response) {
    fwrite(STDERR, json_encode(array('error' => 'Reply failed', 'details' => $errors)));
    exit(1);
}

emit_json(array(
    'status' => 'success',
    'ticket_number' => $ticket->getNumber(),
    'response_id' => $response->getId(),
));