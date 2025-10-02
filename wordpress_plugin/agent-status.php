<?php
/**
 * Simple agent status checker
 * Visit: http://localhost/wordpress/wp-content/plugins/wordpress_plugin/agent-status.php
 */

echo "<h1>🤖 AI Agent Status Checker</h1>";

// Function to check if a port is responding
function check_agent_status($port, $name) {
    $urls_to_try = [
        "http://localhost:$port/docs",
        "http://localhost:$port/",
        "http://localhost:$port/health"
    ];
    
    foreach ($urls_to_try as $url) {
        $context = stream_context_create([
            'http' => [
                'timeout' => 2,
                'method' => 'GET'
            ]
        ]);
        
        $response = @file_get_contents($url, false, $context);
        if ($response !== false) {
            return ['status' => true, 'url' => $url, 'response_length' => strlen($response)];
        }
    }
    
    return ['status' => false, 'url' => null, 'response_length' => 0];
}

// Check common ports
$ports_to_check = [
    8001 => 'Abandonment Detector (Port 8001)',
    8002 => 'Email Generator (Port 8002)', 
    8005 => 'Abandonment Detector (Port 8005)',
    8006 => 'Abandonment Detector (Port 8006)'
];

echo "<table border='1' cellpadding='10' style='border-collapse: collapse;'>";
echo "<tr><th>Agent</th><th>Port</th><th>Status</th><th>Details</th></tr>";

foreach ($ports_to_check as $port => $name) {
    $result = check_agent_status($port, $name);
    $status_color = $result['status'] ? 'green' : 'red';
    $status_text = $result['status'] ? '✅ Running' : '❌ Stopped';
    $details = $result['status'] ? "Responding at {$result['url']} ({$result['response_length']} bytes)" : "No response";
    
    echo "<tr>";
    echo "<td>{$name}</td>";
    echo "<td>{$port}</td>";
    echo "<td style='color: {$status_color}; font-weight: bold;'>{$status_text}</td>";
    echo "<td>{$details}</td>";
    echo "</tr>";
}

echo "</table>";

// Show running agents summary
$running_agents = [];
foreach ($ports_to_check as $port => $name) {
    $result = check_agent_status($port, $name);
    if ($result['status']) {
        $running_agents[] = "$name (Port $port)";
    }
}

if (empty($running_agents)) {
    echo "<div style='background: #f8d7da; padding: 15px; border: 1px solid #f5c6cb; border-radius: 5px; margin: 20px 0;'>";
    echo "<h3>❌ No Agents Running</h3>";
    echo "<p>To start the agents, run these commands in your project directory:</p>";
    echo "<pre style='background: #f1f1f1; padding: 10px;'>";
    echo "python -m uvicorn agents.abandonment_detector.app:app --host 0.0.0.0 --port 8006\n";
    echo "python -m uvicorn agents.email_generator_offer_suggestor.app:app --host 0.0.0.0 --port 8002";
    echo "</pre>";
    echo "</div>";
} else {
    echo "<div style='background: #d4edda; padding: 15px; border: 1px solid #c3e6cb; border-radius: 5px; margin: 20px 0;'>";
    echo "<h3>✅ Running Agents:</h3>";
    echo "<ul>";
    foreach ($running_agents as $agent) {
        echo "<li>$agent</li>";
    }
    echo "</ul>";
    echo "</div>";
}

echo "<hr>";
echo "<h3>🔗 Useful Links:</h3>";
echo "<ul>";
foreach ($ports_to_check as $port => $name) {
    $result = check_agent_status($port, $name);
    if ($result['status']) {
        echo "<li><a href='http://localhost:$port/docs' target='_blank'>$name API Documentation</a></li>";
    }
}
echo "</ul>";
?>