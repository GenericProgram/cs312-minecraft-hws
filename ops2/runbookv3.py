from weasyprint import HTML

def generate_runbook_html():
    return """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
            }
            h1, h2, h3 {
                color: #2c3e50;
            }
            h1 {
                border-bottom: 2px solid #444;
                padding-bottom: 5px;
            }
            h2 {
                margin-top: 25px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 3px;
            }
            pre {
                background: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
            code {
                font-family: monospace;
            }
            ul {
                margin-left: 20px;
            }
            .section {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>

        <h1>Minecraft Operator Runbook</h1>
        <p><strong>Dean Leon | CS 312</strong></p>

        <div class="section">
        <h2>0. Assumptions & Prerequisites</h2>
        <ul>
            <li>AWS account with EC2, ECR, and S3 access</li>
            <li>AWS CLI configured</li>
            <li>Ubuntu EC2 instance</li>
            <li>SSH access available</li>
        </ul>
        </div>

        <div class="section">
        <h2>1. Runtime Architecture</h2>
        <p>
        Internet → Security Group (25565) → EC2 → Docker → Minecraft Container → EBS Storage
        </p>
        <ul>
            <li>Port 25565 exposed</li>
            <li>Docker containerized runtime</li>
            <li>Persistent storage via bind mount</li>
        </ul>
        </div>

        <div class="section">
        <h2>2. Initial Deployment</h2>

        <h3>Install Dependencies</h3>
        <pre><code>sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker</code></pre>

        <h3>Authenticate to ECR</h3>
        <pre><code>aws ecr get-login-password --region us-east-1 \\
| docker login --username AWS --password-stdin &lt;ECR_URL&gt;</code></pre>

        <h3>Start Service</h3>
        <pre><code>docker compose up -d</code></pre>
        </div>

        <div class="section">
        <h2>3. Image Policy</h2>
        <ul>
            <li>No <code>latest</code> tag</li>
            <li>Use: mc-&lt;version&gt;-build&lt;num&gt;</li>
            <li>Stored in private ECR</li>
        </ul>
        </div>

        <div class="section">
        <h2>4. Upgrade & Rollback</h2>

        <h3>Upgrade</h3>
        <pre><code>docker compose up -d</code></pre>

        <h3>Validation</h3>
        <pre><code>docker compose ps
docker compose logs --tail=50
nmap -sV -Pn -p T:25565 localhost</code></pre>

        <h3>Rollback</h3>
        <pre><code>docker compose up -d</code></pre>
        </div>

        <div class="section">
        <h2>5. Backup & Restore</h2>

        <h3>Backup</h3>
        <pre><code>tar -czvf world-backup-$(date +%F).tar.gz data/
aws s3 cp world-backup.tar.gz s3://&lt;BUCKET&gt;/</code></pre>

        <h3>Restore</h3>
        <pre><code>docker compose down
rm -rf data/*
aws s3 cp backup.tar.gz .
tar -xzvf backup.tar.gz
docker compose up -d</code></pre>
        </div>

        <div class="section">
        <h2>6. Monitoring</h2>
        <pre><code>docker compose ps
docker compose logs
docker stats
htop</code></pre>
        </div>

        <div class="section">
        <h2>7. Failure Scenarios</h2>
        <ul>
            <li>Crash loop → check logs, rollback</li>
            <li>Port closed → check security group</li>
            <li>Connection issues → verify service + MOTD</li>
            <li>Corrupt data → restore backup</li>
        </ul>
        </div>

        <div class="section">
        <h2>8. Security</h2>
        <ul>
            <li>Restrict SSH access</li>
            <li>Use IAM roles</li>
            <li>Private S3 bucket</li>
        </ul>
        </div>

        <div class="section">
        <h2>9. Video</h2>
        <p>https://media.oregonstate.edu/media/t/1_tloxm5xl</p>
        </div>

        <div class="section">
        <h2>10. Attribution</h2>
        <p>itzg/minecraft-server, course repo, LLM assistance</p>
        </div>

    </body>
    </html>
    """

def generate_pdf():
    html_content = generate_runbook_html()
    HTML(string=html_content).write_pdf("Minecraft_Runbook.pdf")

if __name__ == "__main__":
    generate_pdf()
