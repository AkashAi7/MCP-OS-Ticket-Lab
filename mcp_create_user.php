<?php

require __DIR__ . '/mcp_bootstrap.php';

$raw = getenv('OST_MCP_PAYLOAD');
if ($raw === false || $raw === '') {
    $raw = stream_get_contents(STDIN);
}

$payload = json_decode($raw, true);
if (!is_array($payload) || empty($payload['name']) || empty($payload['email'])) {
    mcp_emit_error('name and email are required');
}

$vars = array(
    'name' => $payload['name'],
    'email' => $payload['email'],
    'phone' => $payload['phone'] ?? '',
);

$user = User::fromVars($vars, true);
if (!$user) {
    mcp_emit_error('User creation failed');
}

mcp_emit_json(array(
    'status' => 'success',
    'user_id' => $user->getId(),
    'name' => $user->getName(),
    'email' => $user->getDefaultEmail() ? $user->getDefaultEmail()->address : ($payload['email'] ?? ''),
));