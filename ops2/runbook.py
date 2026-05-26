from weasyprint import HTML

html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {
        size: A4;
        margin: 20mm 15mm;
        background-color: #fdfcfaf0;
    }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
        line-height: 1.5;
        font-size: 10.5pt;
        background-color: #fdfcfaf0;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 10px;
        border-bottom: 2px solid #34495e;
    }
    h1 {
        color: #2c3e50;
        font-size: 22pt;
        margin: 0 0 10px 0;
    }
    .meta-info {
        font-size: 11pt;
        color: #7f8c8d;
    }
    h2 {
        color: #2980b9;
        font-size: 14pt;
        margin-top: 25px;
        margin-bottom: 10px;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 4px;
        page-break-after: avoid;
    }
    h3 {
        color: #34495e;
        font-size: 12pt;
        margin-top: 15px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }
    p { margin-top: 0; margin-bottom: 12px; }
    ul { margin-top: 0; margin-bottom: 12px; padding-left: 25px; }
    li { margin-bottom: 6px; }
    
    pre {
        background-color: #2b3a42;
        color: #ecf0f1;
        padding: 10px 12px;
        border-radius: 4px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        white-space: pre-wrap;
        word-wrap: break-word;
        page-break-inside: avoid;
        margin-bottom: 15px;
    }
    code {
        background-color: #eaeded;
        color: #c0392b;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9.5pt;
    }
    .diagram-box {
        background-color: #ecf0f1;
        border: 1px dashed #7f8c8d;
        padding: 15px;
        text-align: center;
        font-family: monospace;
        font-size: 10pt;
        margin-bottom: 15px;
        page-break-inside: avoid;
    }
    .checklist-box {
        background-color: #e8f6f3;
        border-left: 4px solid #1abc9c;
        padding: 10px 15px;
        margin-bottom: 15px;
        page-break-inside: avoid;
    }
    .checklist-box strong { color: #16a085; }
    .footer-attribution {
        margin-top: 40px;
        padding-top: 10px;
        border-top: 1px solid #ccc;
        font-size: 9pt;
        color: #666;
        font-style: italic;
    }
</style>
</head>
<body>

    <div class="header">
        <h1>Runbook</h1>
        <div class="meta-info">
            Dean Leon | 934513949<br>
            Containerized Minecraft Server<br>
            CS 312 System Administration
        </div>
    </div>

    <h2>1. Runtime Architecture</h2>
    <p>The service is deployed on a t2.medium Amazon EC2 instance running Ubuntu. The Minecraft server is containerized using Docker and orchestrated via Docker Compose. Traffic flows from the internet through an AWS Security Group (allowing TCP/25565) to the host machine, which forwards it to the container. State is explicitly decoupled from the container lifecycle using a host bind mount.</p>
    <div class="diagram-box">
        [ Internet Clients ] --> (TCP: 25565)<br>
               |<br>
        [ AWS Security Group ]<br>
               |<br>
        [ EC2 Host (Ubuntu) ]<br>
               |-- Docker Port Binding (0.0.0.0:25565 -> 25565/tcp)<br>
               |<br>
        [ Minecraft Container ]<br>
               |-- Bind Mount (/data -> ~/minecraft-server/data)<br>
               |<br>
        [ EBS Persistent Storage ]
    </div>

    <h2>2. Container Deployment Definition</h2>
    <p>The service is defined in <code>docker-compose.yml</code>. It specifies the immutable image from the private ECR, sets runtime configuration via environment variables, and mounts persistent storage.</p>
<pre>services:
  minecraft:
    image: ECR_URL.dkr.ecr.us-east-1.amazonaws.com/cs312-minecraft:mc-1.20.4-build1
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      VERSION: "1.20.4"
      MOTD: "Dean Leon - CS312"
    volumes:
      - ./data:/data
    restart: always</pre>

    <h2>3. ECR Usage & Image Tag Policy</h2>
    <p>We utilize a private Amazon Elastic Container Registry (ECR) to host immutable images. Deployments must pin a specific image tag; the <code>latest</code> tag is strictly prohibited in production deployments.</p>
    <ul>
        <li><strong>Image Provenance:</strong> We re-tag the widely trusted <code>itzg/minecraft-server</code> base image. This upstream image is open-source, maintained by a highly active community, and provides reliable mechanisms for runtime version selection and EULA acceptance.</li>
        <li><strong>Tagging Scheme:</strong> <code>mc-&lt;version&gt;-build&lt;number&gt;</code> (e.g., <code>mc-1.20.4-build1</code>). If runtime configurations change (such as pinning a different <code>VERSION=...</code>), a new build number or version number is issued to guarantee distinct deployable assets.</li>
    </ul>

    <h2>4. Build & Publish</h2>
    <p>To prepare a new version for deployment, the image must be tagged locally and pushed to the ECR.</p>
<pre># 1. Authenticate Docker to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 998487032255.dkr.ecr.us-east-1.amazonaws.com

# 2. Tag the trusted upstream image with our immutable scheme
docker tag itzg/minecraft-server:latest 998487032255.dkr.ecr.us-east-1.amazonaws.com/cs312-minecraft:mc-1.20.5-build1

# 3. Push to ECR repository
docker push 998487032255.dkr.ecr.us-east-1.amazonaws.com/cs312-minecraft:mc-1.20.5-build1</pre>

    <h2>5. Upgrade and Rollback Runbook</h2>
    <div class="checklist-box">
        <strong>Pre-Change Checklist</strong>
        <ul>
            <li>Backup world data to S3 prior to initiating any deployment changes.</li>
            <li>Verify the backup artifact exists and is visible in the S3 bucket.</li>
            <li>Verify both the target upgrade version and the known-good rollback version exist in the ECR repository.</li>
        </ul>
    </div>
    
    <h3>Upgrade Execution</h3>
    <ol>
        <li>Edit <code>docker-compose.yml</code>. Update the <code>image:</code> line to the new tag (e.g., <code>mc-1.20.5-build1</code>) and update the <code>VERSION:</code> environment variable appropriately.</li>
        <li>Apply the configuration: <code>docker compose up -d</code></li>
    </ol>

    <h3>Post-Change Validation</h3>
    <ul>
        <li>Run <code>docker compose ps</code> to confirm the container status is <strong>Up</strong>.</li>
        <li>Run <code>nmap -sV -Pn -p T:25565 localhost</code> to verify the port is open and the service is responding with the correct MOTD.</li>
        <li>Review logs using <code>docker compose logs --tail=50</code> for any fatal crash loops.</li>
    </ul>

    <h3>Rollback Execution</h3>
    <p>If the validation fails, immediately execute a rollback. Rebuilding from scratch is not required due to our immutable caching.</p>
    <ol>
        <li>Edit <code>docker-compose.yml</code>. Revert the <code>image:</code> tag and the <code>VERSION:</code> variable back to the prior known-good state (e.g., <code>1.20.4</code>).</li>
        <li>Apply the configuration: <code>docker compose up -d</code></li>
        <li>Repeat the Post-Change Validation steps.</li>
    </ol>

    <h2>6. Backup and Restore Runbook (S3)</h2>
    <p>Backups are stored in a private S3 bucket (<code>cs312-mc-backups-998487032255</code>). A bucket lifecycle rule expires artifacts older than 7 days. This 7-day retention period was chosen because it minimizes AWS storage costs while providing ample coverage for game-state rollback.</p>
    
    <h3>Backup Procedure</h3>
<pre>cd ~/minecraft-server
# Compress the host-mounted data directory
tar -czvf world-backup-$(date +%F).tar.gz data/
# Upload to S3
aws s3 cp world-backup-$(date +%F).tar.gz s3://cs312-mc-backups-998487032255/</pre>

    <h3>Restore Procedure</h3>
<pre>cd ~/minecraft-server
# 1. Stop the active server to prevent file lock conflicts
docker compose down

# 2. Clear corrupted/current world data (use caution)
sudo rm -rf data/*

# 3. Retrieve the target backup from S3
aws s3 cp s3://cs312-mc-backups-998487032255/world-backup-TARGET.tar.gz .

# 4. Extract data in place
sudo tar -xzvf world-backup-TARGET.tar.gz

# 5. Bring the service online
docker compose up -d</pre>

    <h2>7. Video Demonstration</h2>
    <p>A video demonstration of the tasks can be found here: <a href="https://media.oregonstate.edu/media/t/1_tloxm5xl">https://media.oregonstate.edu/media/t/1_tloxm5xl</a></p>
    <p><strong>Note:</strong> The video was edited and sections of down time, i.e., waiting for the ec2 instance to reboot, were cut out.</p>
    <ul>
        <li><strong>Checkpoint 1:</strong> 00:06</li>
        <li><strong>Checkpoint 2:</strong> 00:56</li>
        <li><strong>Checkpoint 3:</strong> 01:26</li>
        <li><strong>Checkpoint 4:</strong> 02:13</li>
    </ul>

<div class="footer-attribution">
        <strong>Document Attribution:</strong><br>
        I used LLM assistance to format this document and to ensure that all CLI commands are correct.
        <br>
        <a href="https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram">https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram</a>
    </div>
</body>
</html>
"""

output_path = 'Minecraft_Operator_Runbook.pdf'
HTML(string=html_content).write_pdf(output_path)
print(f"File generated successfully at {output_path}")