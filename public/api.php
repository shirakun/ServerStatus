<?php

use rapidweb\RWFileCache\RWFileCache;

require_once "../vendor/autoload.php";
require_once "../node.php";

function timesecond($seconds)
{
    $seconds = (int) $seconds;
    if ($seconds > 3600) {
        if ($seconds > 24 * 3600) {
            $days     = (int) ($seconds / 86400);
            $days_num = $days . "天";
            $seconds  = $seconds % 86400; //取余
        }
        $hours   = intval($seconds / 3600);
        $minutes = $seconds % 3600; //取余下秒数
        $time    = $days_num . $hours . "小时" . gmstrftime('%M分钟%S秒', $minutes);
    } else {
        $time = gmstrftime('%H小时%M分钟%S秒', $seconds);
    }
    return $time;
}

$cache = new RWFileCache();

$cache->changeConfig(["cacheDirectory" => "../cache"]);

$server_list = $cache->get('server_list');

if (empty($server_list)) {
    $server_list = [];
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // var_dump($_POST);
    if (!isset($_POST["user"]) || !isset($_POST['passwd'])) {
        echo json_encode(['status' => 0, 'msg' => "param error"]);
        exit;
    }

    if (!isset($server_config[$_POST['user']])) {
        echo json_encode(['status' => 0, 'msg' => "server error"]);
        exit;
    }

    if ($_POST['passwd'] != $server_config[$_POST['user']]['password']) {
        echo json_encode(['status' => 0, 'msg' => "auth error"]);
        exit;
    }

    // var_dump($server_list);
    if (!in_array($_POST['user'], $server_list)) {
        $server_list[] = $_POST['user'];
        $cache->set('server_list', $server_list);
    }

    $server_info = $_POST;
    unset($server_info['passwd']);
    $server_info['last_send_time'] = time();

    $server_info['online4'] = $server_info['online4'] == "True" ? true : false;
    $server_info['online6'] = $server_info['online6'] == "True" ? true : false;

    // {"load":"3.6","cpu":"1.0","hdd_total":"63282","last_send_time":1619234836}]

    $number_field = [
        'memory_used',
        'uptime',
        'swap_total',
        'swap_used',
        'memory_total',
        'network_tx',
        'hdd_used',
        'network_out',
        'network_in',
        'network_rx',
        'hdd_total',
    ];

    foreach ($number_field as $key => $value) {
        $server_info[$value] = intval($server_info[$value]);
    }

    $server_config = $server_config[$_POST['user']];

    unset($server_config['user'], $server_config['password']);

    $server_info = array_merge($server_info, $server_config);

    $cache->set("server_{$_POST['user']}_info", $server_info, 20);

} else {
    $json = [];
    foreach ($server_config as $server => $config) {
        $server_info = $cache->get("server_{$server}_info");
        if (empty($server_info) || $server_info->last_send_time + 20 < time()) {
            $server_info = $config;
            unset($server_config['password']);

            $server_info['network_tx']  = 0;
            $server_info['hdd_used']    = 0;
            $server_info['network_out'] = 0;
            $server_info['network_in']  = 0;
            $server_info['network_rx']  = 0;
        } else {
            $server_info['uptime'] = timesecond($server_info['uptime']);
        }

        if ($server_info['disabled'] == true) {
            continue;
        }
        $json[] = $server_info;
    }

    header('content-type:application/json;charset=utf-8');
    // var_dump($json);exit;
    echo json_encode([
        'servers' => $json,
        'updated' => time(),
    ]);

}
