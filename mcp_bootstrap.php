<?php

chdir('/var/www/html');
require 'main.inc.php';

$_SERVER['REMOTE_ADDR'] = $_SERVER['REMOTE_ADDR'] ?: '127.0.0.1';

function mcp_write_result($json) {
    $resultFile = getenv('OST_MCP_RESULT_FILE');
    if ($resultFile) {
        file_put_contents($resultFile, $json);
    }
}

function mcp_emit_json($data) {
    $json = json_encode($data, JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
    if ($json === false) {
        mcp_emit_error('JSON encoding failed', json_last_error_msg());
    }
    mcp_write_result($json);
    echo $json;
}

function mcp_emit_error($message, $details = null, $exitCode = 1) {
    $payload = array('error' => $message);
    if ($details !== null) {
        $payload['details'] = $details;
    }

    $json = json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
    if ($json === false) {
        $json = '{"error":"Unknown MCP helper failure"}';
    }

    mcp_write_result($json);
    fwrite(STDERR, $json);
    exit($exitCode);
}