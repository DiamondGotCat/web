<?php
$headers = getallheaders();
$ip = $_SERVER['REMOTE_ADDR'];
$userAgent = $headers['User-Agent'] ?? '';
$cfCountry = $_SERVER['HTTP_CF_IPCOUNTRY'] ?? '';
$cfRay = $headers['CF-Ray'] ?? '';

$data = [
    'ip' => $ip,
    'user_agent' => $userAgent,
    'country' => $cfCountry,
    'cf_ray' => $cfRay,
];
$json = escapeshellarg(json_encode($data));

$cmd = "python3 /var/www/python/dgc-analytics-add.py $json";
$output = shell_exec($cmd);
$result = json_decode($output, true);

try {
    $pdo = new PDO('mysql:host=localhost;dbname=analytics;', 'root', '565628', [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    ]);
    $stmt = $pdo->prepare("INSERT INTO access_logs (ip, country, cf_ray, user_agent, browser, os, device)
                           VALUES (?, ?, ?, ?, ?, ?, ?)");
    $stmt->execute([
        $result['ip'],
        $result['country'],
        $result['cf_ray'],
        $result['user_agent'],
        $result['browser'],
        $result['os'],
        $result['device']
    ]);
} catch (Exception $e) {
    error_log("[DGC-Analytics] DB保存エラー: " . $e->getMessage());
}
?>