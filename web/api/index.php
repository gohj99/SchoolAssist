<?php
// 设置错误报告级别
error_reporting(E_ALL);
ini_set('display_errors', 1);

// 后端服务的基础 URL
$backend_url = 'http://127.0.0.1:38534';

// 获取请求方法
$request_method = $_SERVER['REQUEST_METHOD'];

// 初始化响应数组
$response = array();

if ($request_method === 'POST') {
    // 获取 POST 请求的接口和数据
    $endpoint = $_POST['endpoint'] ?? '';
    $data = $_POST['data'] ?? '';

    if (empty($endpoint) || empty($data)) {
        http_response_code(400);
        $response['error'] = 'Missing endpoint or data in POST request';
    } else {
        // 构建后端请求 URL
        $url = $backend_url . '/' . ltrim($endpoint, '/');

        // 创建 POST 请求的上下文
        $options = array(
            'http' => array(
                'header'  => "Content-type: application/json\r\n",
                'method'  => 'POST',
                'content' => json_encode($data),
            ),
        );
        $context  = stream_context_create($options);

        // 发送请求并获取响应
        $result = file_get_contents($url, false, $context);

        if ($result === FALSE) {
            http_response_code(500);
            $response['error'] = 'Error accessing backend service';
        } else {
            $response = json_decode($result, true);
        }
    }
} elseif ($request_method === 'GET') {
    // 获取 GET 请求的接口
    $endpoint = $_GET['endpoint'] ?? '';

    if (empty($endpoint)) {
        http_response_code(400);
        $response['error'] = 'Missing endpoint in GET request';
    } else {
        // 构建后端请求 URL
        $url = $backend_url . '/' . ltrim($endpoint, '/');

        // 发送请求并获取响应
        $result = file_get_contents($url);

        if ($result === FALSE) {
            http_response_code(500);
            $response['error'] = 'Error accessing backend service';
        } else {
            $response = json_decode($result, true);
        }
    }
} else {
    http_response_code(405);
    $response['error'] = 'Method not allowed';
}

// 设置响应头为 JSON
header('Content-Type: application/json');

// 输出响应
echo json_encode($response);
?>
