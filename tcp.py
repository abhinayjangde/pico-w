import network
import socket
import time

# 1. Configure your network credentials
SSID = "Abhi's g34 5G"
PASSWORD = "wahitohai"
PORT = 80  # The TCP port you want to open

# 2. Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    ip_address = wlan.ifconfig()[0]
    print(f'Connected successfully! Pico W IP address: {ip_address}')

# 3. Open a TCP socket
# AF_INET = IPv4 protocol, SOCK_STREAM = TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to all network interfaces ('0.0.0.0') and your specified port
server_socket.bind(('0.0.0.0', PORT))

# Start listening for incoming connections (allow a backlog of up to 1 client queue)
server_socket.listen(1)
print(f'TCP server is now listening on port {PORT}...')
try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Browser connected from: {client_address}")
        
        # Read the browser's incoming HTTP request headers
        request = client_socket.recv(1024)
        
        # --- THE FIX: Format the response as a proper HTTP packet ---
        # Line 1: Tells the browser the request was successful (HTTP 200 OK)
        # Line 2: Tells the browser we are sending plain text or HTML
        # Line 3: A blank line (\r\n) to mark the end of the headers
        # Line 4: Your actual message text
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello, IoT Explorer!</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-color: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .icon-container {
            width: 70px;
            height: 70px;
            background-color: rgba(56, 189, 248, 0.1);
            border: 2px solid var(--accent-color);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px auto;
        }

        .icon {
            font-size: 32px;
        }

        h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }

        p {
            color: var(--text-muted);
            font-size: 16px;
            margin-bottom: 32px;
        }

        .badge-container {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }

        .badge {
            background-color: #0f172a;
            border: 1px solid #334155;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: var(--accent-color);
        }

        .btn {
            display: inline-block;
            background-color: var(--accent-color);
            color: #0f172a;
            font-weight: 700;
            text-decoration: none;
            padding: 14px 28px;
            border-radius: 8px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px 0 rgba(56, 189, 248, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(56, 189, 248, 0.6);
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="icon-container">
            <span class="icon">⚡</span>
        </div>
        <h1>Hello, IoT Explorer!</h1>
        <p>You have successfully tunneled into a live node. This webpage is being compiled and served entirely from a dual-core Raspberry Pi Pico W microcontroller sitting right on a workbench.</p>
        
        <div class="badge-container">
            <span class="badge">📡 Wi-Fi Active</span>
            <span class="badge">🐍 MicroPython</span>
            <span class="badge">🌐 TCP Port Open</span>
        </div>

        <a href="#" class="btn">Explore the Project</a>
    </div>

</body>
</html>
"""
        )
        
        # Send the properly formatted HTTP packet
        client_socket.send(http_response.encode('utf-8'))
        
        # Close the connection so the browser finishes loading the page
        client_socket.close()
        print("HTTP response sent successfully.\n")

except KeyboardInterrupt:
    print("\nShutting down server.")
finally:
    server_socket.close()