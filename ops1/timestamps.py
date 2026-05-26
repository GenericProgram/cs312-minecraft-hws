from weasyprint import HTML

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 15mm 12mm;
            background-color: #ffffff;
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            font-size: 11pt;
        }
        .header-banner {
            background-color: #1a2a3a;
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 4px;
            margin-bottom: 30px;
        }
        h1 { margin: 0; font-size: 22pt; letter-spacing: 0.5px; }
        .student-info { margin-top: 10px; font-size: 12pt; opacity: 0.9; }
        
        h2 { 
            color: #2c3e50; 
            border-bottom: 2px solid #3498db; 
            padding-bottom: 5px;
            margin-top: 30px;
        }

        .link-container {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 20px;
            border-radius: 4px;
            text-align: center;
            margin: 20px 0;
        }
        .video-link {
            font-family: 'Consolas', monospace;
            color: #2980b9;
            text-decoration: none;
            font-weight: bold;
            font-size: 12pt;
            word-break: break-all;
        }
        
        .timestamp-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .timestamp-table th {
            background-color: #2c3e50;
            color: white;
            text-align: left;
            padding: 12px;
        }
        .timestamp-table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .time-code {
            font-family: 'Consolas', monospace;
            font-weight: bold;
            color: #e67e22;
            width: 20%;
        }
        .checkpoint-name {
            font-weight: 600;
        }

        .footer {
            margin-top: 50px;
            font-size: 9pt;
            color: #7f8c8d;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header-banner">
        <h1>Ops 1: Video Demonstration</h1>
        <div class="student-info">Dean Leon | Student ID: 934513949</div>
    </div>

    <h2>1. Media Link</h2>
    <p>The following link directs to the video demonstration of the Minecraft server deployment and configuration checkpoints hosted on the Oregon State University media portal.</p>
    
    <div class="link-container">
        <a href="https://media.oregonstate.edu/media/t/1_5xh1j5c9" class="video-link">
            https://media.oregonstate.edu/media/t/1_5xh1j5c9
        </a>
    </div>

    <h2>2. Demonstration Timestamps</h2>
    <p>Key checkpoints and extra credit requirements are documented at the following intervals:</p>

    <table class="timestamp-table">
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="time-code">00:04</td>
                <td class="checkpoint-name">Checkpoint 1: AWS console visible with account ID, SSH login shown, dedicated `minecraft` user existence proven (e.g., `id minecraft`).</td>
            </tr>
            <tr>
                <td class="time-code">01:24</td>
                <td class="checkpoint-name">Checkpoint 2: Instance is rebooted, then `nmap -sV -Pn -p T:25565 <public-ip>` output shows port open and Minecraft service responding with custom MOTD containing name or student ID. Server port can differ from default.</td>
            </tr>
            <tr>
                <td class="time-code">01:36</td>
                <td class="checkpoint-name">Checkpoint 3: After reboot, `systemctl status` (or equivalent) confirms the service is active and enabled; uptime/PID is consistent with a post-reboot start.</td>
            </tr>
            <tr>
                <td class="time-code">01:50</td>
                <td class="checkpoint-name">RCON Extra Credit 3: Remote Console Demo</td>
            </tr>
            <tr>
                <td class="time-code">02:08</td>
                <td class="checkpoint-name">Checkpoint 4: Service is stopped, status confirms it is stopped, service is restarted, and health is confirmed</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        Used LLM to format timestamps.
        <br>
        <a href="https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram">https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram</a>
    </div>
</body>
</html>
"""

output_path = "Ops1_Video_Timestamps.pdf"
HTML(string=html_content).write_pdf(output_path)
print(f"Successfully generated: {output_path}")