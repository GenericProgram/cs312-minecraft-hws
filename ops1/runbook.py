from weasyprint import HTML

#pip install weasyprint
#install gtk for windows project: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
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
            line-height: 1.5;
            color: #333;
            margin: 0;
            padding: 0;
            font-size: 10.5pt;
        }
        .header-banner {
            background-color: #1a2a3a;
            color: white;
            padding: 25px;
            text-align: center;
            border-radius: 4px;
            margin-bottom: 25px;
        }
        h1 { margin: 0; font-size: 20pt; letter-spacing: 0.5px; }
        h2 { 
            color: #2c3e50; 
            border-bottom: 2px solid #3498db; 
            padding-bottom: 5px;
            margin-top: 25px;
            font-size: 15pt;
        }
        h3 { color: #2980b9; font-size: 11pt; margin-top: 15px; margin-bottom: 5px; font-weight: bold; }
        
        .cmd-block {
            margin: 10px 0 20px 0;
        }
        .reasoning {
            font-weight: 600;
            color: #444;
            margin-bottom: 4px;
            display: block;
        }
        pre {
            background-color: #f4f4f4;
            color: #000;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 9.5pt;
            line-height: 1.2;
            border: 1px solid #ccc;
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            word-break: break-all;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        
        .security-note {
            background-color: #e7f5ff;
            border-left: 4px solid #228be6;
            padding: 10px 15px;
            margin: 15px 0;
            font-size: 10pt;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #dee2e6;
            padding: 8px 12px;
            text-align: left;
        }
        th { background-color: #f8f9fa; font-weight: bold; }
        .footer-attribution {
            margin-top: 40px;
            padding-top: 10px;
            border-top: 1px solid #ccc;
            font-size: 9pt;
            color: #666;
            font-style: italic;
        }
        .cost-item {
            margin-bottom: 15px;
        }
        .cost-label {
            font-weight: bold;
            color: #2c3e50;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header-banner">
        <h1>Ops 1: Manual Minecraft Server Runbook</h1>
        <p>Name: Dean Leon | Student ID: 934513949</p>
    </div>

    <h2>1. Infrastructure Overview</h2>
    <p>Manual deployment of a persistent PaperMC Minecraft server on AWS Academy.</p>
    
    <h3>Hardware Specifications</h3>
    <ul>
        <li><strong>Instance Type:</strong> <code>t3.small</code> (2 GiB RAM).</li>
        <li><strong>AMI:</strong> Ubuntu Server 24.04 LTS.</li>
        <li><strong>Storage:</strong> 12 GiB EBS gp3.</li>
    </ul>

    <h2>2. System Preparation & User Setup</h2>
    
    <div class="cmd-block">
        <span class="reasoning">Create a dedicated system user to isolate the application process for security</span>
        <pre>sudo useradd -r -m -d /opt/minecraft -s /bin/bash minecraft</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Update system repositories and install the required Java 21 runtime</span>
        <pre>sudo apt update
sudo apt install openjdk-21-jre-headless -y</pre>
    </div>

    <h2>3. Minecraft Server Installation</h2>
    
    <div class="cmd-block">
        <span class="reasoning">Create the application directory and assign ownership to the service user</span>
        <pre>sudo mkdir -p /opt/minecraft/server
sudo chown -R minecraft:minecraft /opt/minecraft</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Switch to the service user and navigate to the server folder</span>
        <pre>sudo su - minecraft
cd ~/server</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Download the PaperMC server software</span>
        <pre>curl -o paper.jar https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/130/downloads/paper-1.21.1-130.jar</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Run the server once to generate configuration files and then accept the EULA</span>
        <pre>java -Xms1G -Xmx1G -jar paper.jar --nogui
vim eula.txt</pre>
    </div>

    <h2>4. Configuration & RCON (Extra Credit)</h2>
    
    <div class="cmd-block">
        <span class="reasoning">Modify server settings for identity (MOTD) and remote administration (RCON)</span>
        <pre>vim /opt/minecraft/server/server.properties</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Install build tools and compile the mcrcon utility from source</span>
        <pre>sudo apt install git build-essential -y
git clone https://github.com/Tiiffi/mcrcon.git
cd mcrcon
make
sudo make install</pre>
    </div>

    <h2>5. Service Management (Systemd)</h2>
    
    <div class="cmd-block">
        <span class="reasoning">Create the background service configuration file</span>
        <pre>sudo vim /etc/systemd/system/minecraft.service</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Reload the systemd daemon, enable the service for boot, and start it</span>
        <pre>sudo systemctl daemon-reload
sudo systemctl enable minecraft.service
sudo systemctl start minecraft.service</pre>
    </div>

    <h2>6. Operational Procedures</h2>
    
    <div class="cmd-block">
        <span class="reasoning">Check if the server is active and running</span>
        <pre>sudo systemctl status minecraft.service</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Monitor the live server logs for errors or player connections</span>
        <pre>sudo journalctl -u minecraft.service -f</pre>
    </div>

    <div class="cmd-block">
        <span class="reasoning">Execute an administrative command while the server is running in the background</span>
        <pre>mcrcon -p admin "op [MINECRAFT_USERNAME]"</pre>
    </div>

    <div class="security-note">
        <strong>Security Note:</strong> RCON (25575) is restricted to <code>localhost</code>. SSH is required for administration.
    </div>

    <h2>7. Cost-Control Strategy</h2>
    
    <div class="cost-item">
        <span class="cost-label">Instance Size Choice & Rationale:</span>
        <p>A <code>t3.small</code> instance was selected for this deployment. While AWS Academy provides smaller instances, PaperMC usually requires a larger amount of ram, like 2GB of RAM to run Java 21 comfortably. Choosing a t3.small prevents OOM errors and kernel panics.</p>
    </div>

    <div class="cost-item">
        <span class="cost-label">Stop/Shutdown Schedule:</span>
        <p>To preserve lab credits, the instance follows a strict on demand schedule. The server is manually started at the beginning of a development or testing session and is shut down via the AWS Console immediately upon completion of the task. The server is never left running overnight or during periods of inactivity.</p>
    </div>

    <div class="cost-item">
        <span class="cost-label">Cost Guardrails:</span>
        <p>To prevent accidental credit exhaustion, I utilize <strong>lab session discipline</strong>. This involves setting a timer for each work session and verifying the instance state in the AWS Console before closing the browser. Additionally, the AWS Academy environment's built-in session timer acts as a hard guardrail to automatically terminate/stop resources if a session is accidentally left open.</p>
    </div>

    <div class="footer-attribution">
        <strong>Document Attribution:</strong><br>
        I used LLM assistance to format this document and to ensure that all CLI commands are correct.
        <br>
        <a href="https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram">https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram</a>
    </div>
</body>
</html>
"""


output_path = "Ops1_Manual_Minecraft_Server_Runbook.pdf"
HTML(string=html_content).write_pdf(output_path)
print(output_path)