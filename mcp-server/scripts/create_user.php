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
if (!is_array($payload) || empty($payload['email'])) {
    fwrite(STDERR, json_encode(array('error' => 'email is required')));
    exit(1);
}

$user = User::fromVars(array(
    'name' => $payload['name'] ?? '',
    'email' => $payload['email'],
    'phone' => $payload['phone'] ?? '',
), true, false);

if (!$user) {
    fwrite(STDERR, json_encode(array('error' => 'User creation failed')));
    exit(1);
}

emit_json(array(
    'status' => 'success',
    'id' => $user->getId(),
    'name' => $user->getName(),
    'email' => $user->getEmail(),
));