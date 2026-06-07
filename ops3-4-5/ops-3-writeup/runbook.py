import os
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
        margin: 0;
        padding: 0;
    }
    *, *::before, *::after { box-sizing: border-box; }
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
    ul, ol { margin-top: 0; margin-bottom: 12px; padding-left: 25px; }
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
    .diagram-container {
        background-color: #ffffff;
        border: 1px dashed #7f8c8d;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
        page-break-inside: avoid;
    }
    .diagram-container img {
        max-width: 100%;
        height: auto;
    }
    .caption {
        font-size: 9.5pt;
        color: #7f8c8d;
        font-style: italic;
        margin-top: 10px;
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
        <h1>Infrastructure Automation Runbook</h1>
        <div class="meta-info">
            Dean Leon | 934513949<br>
            Infrastructure Automation<br>
            CS 312 System Administration
        </div>
    </div>

    <h2>1. Runtime Architecture</h2>
    <p>The automated deployment pipeline consists of two primary flows: an image publishing pipeline via GitHub Actions and infrastructure provisioning via Terraform and Ansible. The EC2 instance is deployed with the <code>LabInstanceProfile</code>, allowing it to seamlessly authenticate to AWS ECR to pull the pinned Docker image and AWS S3 to restore persistent world data before the container starts.</p>
    
    <div class="diagram-container">
        <img src="diagram.png" alt="Architecture Diagram">
        <div class="caption">Architecture diagram generated using Mermaid.js</div>
    </div>

    <h2>2. Terraform Variables and Configuration</h2>
    <p>Infrastructure is modeled strictly as code using Terraform to guarantee reproducible and auditable environments. The following variables define the provisioning parameters:</p>
    <ul>
        <li><code>aws_region</code>: Specifies the target AWS region for deployment (e.g., <code>us-east-1</code>).</li>
        <li><code>instance_type</code>: Controls the compute capacity of the EC2 instance (set to <code>t3.medium</code> to support the memory requirements of the Minecraft container).</li>
        <li><code>key_name</code>: The identifier of the AWS key pair (e.g., <code>cs312-key</code>) used to associate the public SSH key with the newly provisioned host.</li>
        <li><code>private_key_path</code>: The local file path pointing to the `.pem` file used by the <code>local-exec</code> provisioner to authenticate Ansible's initial configuration run against the new EC2 instance.</li>
    </ul>
    <p><strong>State Management:</strong> Terraform state is stored locally in <code>terraform.tfstate</code>. This file is excluded from version control via <code>.gitignore</code> to prevent accidental exposure of resource IDs and sensitive outputs. The operator running <code>terraform apply</code> or <code>terraform destroy</code> is responsible for retaining the state file between operations. A remote S3 backend with state locking is not configured in this environment due to AWS Academy credential constraints, but would be the recommended approach for a production deployment.</p>

    <h2>3. Infrastructure Change Process</h2>
    <p>To ensure infrastructure auditability and prevent undocumented configuration drift, all modifications must flow through the version control system:</p>
    <ol>
        <li><strong>Branching:</strong> A teammate creates a feature branch from <code>main</code> (e.g., <code>feature/increase-ebs-storage</code>).</li>
        <li><strong>Code Modification:</strong> The teammate updates the state declarations in the Terraform files or task definitions in the Ansible playbook.</li>
        <li><strong>Review & PR:</strong> A Pull Request is opened against <code>main</code>. The team reviews the proposed changes and validates the dry-run output of <code>terraform plan</code>.</li>
        <li><strong>Merge & Apply:</strong> Once approved, the PR is merged. An authorized operator pulls the updated <code>main</code> branch locally and applies the new state using <code>terraform apply</code>.</li>
    </ol>

    <h2>4. Cost-Prevention Teardown Checklist</h2>
    <p>To prevent runaway resource costs in the AWS Academy Learner Lab environment, the infrastructure stack must be systematically destroyed when operations conclude.</p>
    <div class="checklist-box">
        <strong>Mandatory Teardown Sequence:</strong>
        <ul>
            <li><strong>1. Destroy Compute Infrastructure:</strong> Run <code>terraform destroy -auto-approve</code> to permanently terminate the EC2 instance, its root EBS volume, and associated Security Groups.</li>
            <li><strong>2. Purge Container Images:</strong> Navigate to the AWS Elastic Container Registry console, empty the <code>minecraft-server</code> repository of all published images, and delete the repository.</li>
            <li><strong>3. Purge Backup Data:</strong> Navigate to the AWS S3 console, open the persistent world backup bucket, permanently delete all contained backup archives, and delete the bucket.</li>
            <li><strong>4. End Session:</strong> Terminate the AWS Learner Lab session explicitly using the portal's "End Lab" function to revoke temporary credentials.</li>
        </ul>
    </div>

    <h2>5. World-Data Recovery Strategy</h2>
    <p>World data persistence is achieved by backing up the Minecraft <code>/data</code> directory to a dedicated S3 bucket. The Ansible playbook is responsible for restoring from this backup before container start, ensuring players return to the same world after any rebuild.</p>
    <ul>
        <li><strong>Backup location:</strong> World data is stored in an S3 bucket (e.g., <code>s3://minecraft-world-backup-&lt;account-id&gt;/world/</code>). The EC2 instance writes to this bucket via the permissions granted by <code>LabInstanceProfile</code> — no credentials are stored on disk.</li>
        <li><strong>Backup trigger:</strong> The operator runs <code>aws s3 sync /data s3://&lt;bucket&gt;/world/</code> before tearing down the instance, or a cron job on the host can perform periodic backups automatically.</li>
        <li><strong>Restore on rebuild:</strong> The Ansible playbook executes <code>aws s3 sync s3://&lt;bucket&gt;/world/ /data</code> before starting the Minecraft container. The restore runs first so the server loads the existing world rather than generating a new one. If the S3 path is empty (first deploy), the server generates a fresh world as expected.</li>
        <li><strong>Idempotency:</strong> <code>aws s3 sync</code> only transfers changed or missing files, so re-running the playbook against a live host does not overwrite an in-progress world with a stale backup.</li>
        <li><strong>Rebuild outcome:</strong> As demonstrated in Checkpoint 4 of the video, a full <code>terraform destroy</code> followed by <code>terraform apply</code> and the Ansible playbook restores the same world — no player progress is lost.</li>
    </ul>

    <h2>6. Video Demonstration &amp; Rebuild Proof</h2>
    <p>A video demonstration verifying the infrastructure automation, pipeline execution, and world-data recovery strategy can be found here: <br><a href="https://media.oregonstate.edu/media/t/1_xzwcuvd2">https://media.oregonstate.edu/media/t/1_xzwcuvd2</a></p>
    <p><strong>Note:</strong> The video was edited and sections of down time, i.e., waiting for the ec2 instance to reboot, were cut out.</p>
    <ul>
        <li><strong>Checkpoint 1 (00:14):</strong> <code>terraform apply</code> execution and automated Ansible playbook configuration.</li>
        <li><strong>Checkpoint 2 (00:57):</strong> Service validation via <code>nmap</code>, proving the port is open and the custom MOTD is active.</li>
        <li><strong>Checkpoint 3 (01:37):</strong> Verification of the GitHub Actions CI/CD pipeline triggering on a tag push and passing smoke tests.</li>
        <li><strong>Checkpoint 4 (02:01):</strong> Simulated server loss via <code>terraform destroy</code>, followed by an automated rebuild proving the S3 restoration of existing world data.</li>
    </ul>

    <div class="footer-attribution">
        <strong>Document Attribution:</strong><br>
        I used LLM assistance to format this document and to validate the technical accuracy of the content.
        <br>
        <a href="https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram">https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram</a>
    </div>
</body>
</html>
"""

output_pdf_path = 'Minecraft_Infrastructure_Automation_Runbook.pdf'
HTML(string=html_content, base_url=os.path.abspath(os.path.dirname(__file__)) + '/').write_pdf(output_pdf_path)
print(f"File generated successfully with tag: {output_pdf_path}")