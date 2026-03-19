<?php

$path = '/var/www/html/include/ost-config.php';
$config = file_get_contents($path);
if ($config === false) {
    fwrite(STDERR, "Unable to read ost-config.php\n");
    exit(1);
}

$secretSalt = getenv('OST_LOCAL_SECRET_SALT') ?: bin2hex(random_bytes(16));
$replacements = array(
    "define('OSTINSTALLED',FALSE);" => "define('OSTINSTALLED',TRUE);",
    '%CONFIG-SIRI' => $secretSalt,
    '%ADMIN-EMAIL' => getenv('OST_LOCAL_ADMIN_EMAIL') ?: 'admin@local.test',
    '%CONFIG-DBHOST' => getenv('OST_LOCAL_DBHOST') ?: 'mysql',
    '%CONFIG-DBNAME' => getenv('OST_LOCAL_DBNAME') ?: 'osticket',
    '%CONFIG-DBUSER' => getenv('OST_LOCAL_DBUSER') ?: 'osticket',
    '%CONFIG-DBPASS' => getenv('OST_LOCAL_DBPASS') ?: 'osticket123',
    '%CONFIG-PREFIX' => getenv('OST_LOCAL_DBPREFIX') ?: 'ost_',
);

$updated = strtr($config, $replacements);
if (file_put_contents($path, $updated) === false) {
    fwrite(STDERR, "Unable to write ost-config.php\n");
    exit(1);
}

echo "Updated ost-config.php\n";