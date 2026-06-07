import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

def create_pdf(filename="ops_5_writeup.pdf"):
    # Initialize document with standard margins
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom Styles mapping the Ops 4 aesthetics
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=6,
        textColor=colors.HexColor("#1e3a8a")
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=12
    )
    h1 = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#1e3a8a")
    )
    h2 = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#334155")
    )
    normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leading=14
    )
    code_block = ParagraphStyle(
        'Code',
        parent=normal,
        fontName='Courier',
        fontSize=9,
        leftIndent=20,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderPadding=(4, 4, 4, 4)
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=normal,
        spaceAfter=4
    )
    
    story = []

    # Title & Header Block
    story.append(Paragraph("<b>Ops 5: Observability and Incident Response</b>", title_style))
    story.append(Paragraph("Minecraft on Kubernetes (k3s) - CS 312 System Administration", subtitle_style))
    story.append(Paragraph("Dean Leon | Student ID: 934513949", subtitle_style))
    story.append(Spacer(1, 10))

    # Top Informational Table
    info_label_style = ParagraphStyle(
        'InfoLabel',
        parent=normal,
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0f172a")
    )
    info_val_style = ParagraphStyle(
        'InfoVal',
        parent=normal,
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0f172a")
    )
    info_data = [
        ["Repository", "https://github.com/GenericProgram/cs312-minecraft-hws"],
        ["Video", "https://media.oregonstate.edu/media/t/1_g1abc3tt"],
        ["Checkpoints", "CP1: 00:03 | CP2: 00:38 | CP3: 01:10 | CP4: 02:07"],
        ["AWS Region", "us-east-1"],
        ["Instance", "t3.large, Ubuntu 22.04 LTS, 20 GB gp3"],
        ["Kubernetes", "k3s v1.35.5+k3s1 (single-node)"],
        ["Image", "998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:v1.20.4"]
    ]
    formatted_info_data = [
        [Paragraph(row[0], info_label_style), Paragraph(row[1], info_val_style)]
        for row in info_data
    ]
    info_table = Table(formatted_info_data, colWidths=[100, 400])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1"))
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))

    # 1. Architecture
    story.append(Paragraph("1. Architecture", h1))
    
    img_filename = os.path.join(os.path.dirname(__file__), "architecture.png")
    if os.path.exists(img_filename):
        img = Image(img_filename)
        max_width = 468  # 6.5 inches at 72 dpi
        if img.drawWidth > max_width:
            ratio = max_width / img.drawWidth
            img.drawWidth = max_width
            img.drawHeight = img.drawHeight * ratio
        story.append(img)
        story.append(Spacer(1, 10))
    else:
        story.append(Paragraph("<i>[Error: architecture.png not found]</i>", normal))
    story.append(Paragraph("The architecture builds upon the Ops 4 baseline, integrating the Minecraft server workload (with a <font name='Courier'>minecraft-exporter</font> sidecar) alongside the monitoring components in a dedicated <font name='Courier'>monitoring</font> namespace. The Minecraft server container image is pulled from a secure AWS ECR registry, and persistent world state backups are synchronized to an AWS S3 bucket. Prometheus scrapes host-level metrics via the Node Exporter daemonset, pod-level metrics via kube-state-metrics, and application-level metrics via the Minecraft exporter. Grafana provides visualization of these metrics, which is accessed securely via an SSH port-forward tunnel rather than exposing Grafana or Prometheus to the public web.", normal))
    story.append(Spacer(1, 10))

    # 2. Repository File Map
    story.append(Paragraph("2. Repository File Map", h1))
    story.append(Paragraph("All Ops 5 submission files are organized in the <b>ops3-4-5/</b> directory.", normal))
    
    file_map_data = [
        ["helm/monitoring-values.yaml", "Declarative configurations, limits, and retention for kube-prometheus-stack."],
        ["k8s/monitoring/namespace.yml", "Namespace isolation for the observability stack."],
        ["k8s/monitoring/prometheus-rules.yml", "Declarative Prometheus alerts (CrashLoop, Mem/Disk pressure)."],
        ["ops-5-writeup/ops_5_writeup.pdf", "Self-contained PDF documentation including architecture, runbooks, and incident postmortem."],
        ["playbook.yml", "Updated Ansible playbook triggering k3s, configuring ECR/S3, and applying manifests."],
        ["k8s/deployment.yml", "Minecraft server deployment containing the primary server container, the RCON prometheus-exporter sidecar, and liveness/readiness/startup probes."],
        ["k8s/configmap.yml", "Minecraft environment variables (pinned to version 1.20.4 to prevent Java 21 crash)."],
        ["k8s/service.yml", "Kubernetes Service exposing Minecraft TCP (25565) and RCON (25575) ports."],
        ["k8s/pvc.yml", "Persistent Volume Claim mapping the Minecraft world-data directory to persistent host storage."],
        ["k8s/rcon-secret.yml", "Kubernetes Secret storing the sensitive RCON password securely."],
        ["k8s/backup-cronjob.yml", "Kubernetes CronJob for automated world-state synchronization to S3."],
        ["terraform.tfvars", "Terraform variables reflecting the t3.large instance scaling."]
    ]
    file_code_style = ParagraphStyle(
        'FileCode',
        parent=normal,
        fontName='Courier',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )
    formatted_file_map_data = [
        [Paragraph(row[0], file_code_style), Paragraph(row[1], normal)]
        for row in file_map_data
    ]
    file_table = Table(formatted_file_map_data, colWidths=[180, 320])
    file_table.setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1"))
    ]))
    story.append(file_table)
    story.append(Spacer(1, 10))

    # 3. Deployment Runbook
    story.append(Paragraph("3. Deployment Runbook", h1))
    story.append(Paragraph("An operator can deploy the full monitoring stack onto the existing Ops 4 baseline by following these steps.", normal))
    
    story.append(Paragraph("<b>3.1 Prerequisites & Foundation Fixes</b>", h2))
    story.append(Paragraph("Ensure the EC2 instance is scaled to a <font name='Courier'>t3.large</font> via Terraform to accommodate the memory overhead of JVM, Prometheus, and Grafana simultaneously. The Minecraft ConfigMap must explicitly pin <font name='Courier'>VERSION: \"1.20.4\"</font> to prevent the container from fetching the latest version, which causes a Java 21 initialization crash.", normal))
    
    story.append(Paragraph("<b>3.2 Install Helm & Deploy Monitoring Stack</b>", h2))
    story.append(Paragraph("SSH into the EC2 instance and run the following to install Helm and the Prometheus stack declaratively:", normal))
    story.append(Paragraph("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | sudo bash", code_block))
    story.append(Paragraph("sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm repo add prometheus-community https://prometheus-community.github.io/helm-charts<br/>sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm repo update", code_block))
    story.append(Paragraph("sudo k3s kubectl create namespace monitoring", code_block))
    story.append(Paragraph("sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm install monitoring prometheus-community/kube-prometheus-stack \\<br/>  --namespace monitoring \\<br/>  -f /opt/minecraft-k8s/monitoring-values.yaml", code_block))

    story.append(Paragraph("<b>3.3 Apply Alerts & Port-Forward Grafana</b>", h2))
    story.append(Paragraph("Apply the Prometheus rules manifest to register the alerts:", normal))
    story.append(Paragraph("sudo k3s kubectl apply -f /opt/minecraft-k8s/monitoring/prometheus-rules.yml", code_block))
    story.append(Paragraph("To access Grafana without exposing it publicly, establish a secure SSH tunnel from the local WSL machine:", normal))
    story.append(Paragraph("ssh -i ~/.ssh/cs312-key.pem -L 3000:localhost:3000 ubuntu@[EC2-IP] \\<br/>  \"sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80\"", code_block))
    story.append(Paragraph("Access the dashboard at <font name='Courier'>http://localhost:3000</font>.", normal))
    story.append(Spacer(1, 10))

    # 4. Observability and Dashboards
    story.append(Paragraph("4. Observability and Dashboards", h1))
    story.append(Paragraph("The custom <b>Minecraft Server Health</b> dashboard aggregates critical metrics to answer the operator question: <i>\"Is my service healthy right now?\"</i> at a single glance.", normal))
    
    dash_items = [
        ListItem(Paragraph("<b>Node Health Panels:</b> Gauges tracking Node Memory Usage %, Node CPU Usage %, and Node Disk Usage % ensure the underlying EC2 instance is not saturated.", bullet_style)),
        ListItem(Paragraph("<b>Pod Health Panels:</b> Stats tracking Minecraft Pod Restarts and Pod Ready status. To clean up the visualization and hide historical terminated pods, these queries wrap the raw metric in a <font name='Courier'>sum()</font> function.", bullet_style)),
        ListItem(Paragraph("<b>Pod Resource Consumption Panels:</b> Tracks CPU and memory resource consumption specifically for the Minecraft container (using <font name='Courier'>container_cpu_usage_seconds_total</font> and <font name='Courier'>container_memory_working_set_bytes</font>) to detect memory leaks and CPU throttling before they affect gameplay.", bullet_style)),
        ListItem(Paragraph("<b>Minecraft-Specific Signal:</b> The dashboard tracks application-level metrics via the <font name='Courier'>minecraft-exporter</font> sidecar. Specifically, <font name='Courier'>minecraft_players_online</font> visualizes active player counts, and <font name='Courier'>minecraft_rcon_up</font> validates active RCON connectivity to the server. Together, these signals verify that the Minecraft application engine is healthy and accepting TCP connections, providing a robust application-layer check compared to basic container running states (<font name='Courier'>kube_pod_container_status_running</font>).", bullet_style))
    ]
    story.append(ListFlowable(dash_items, bulletType='bullet'))
    story.append(Spacer(1, 10))

    # 5. Alert Runbooks
    story.append(Paragraph("5. Alert Runbooks & On-Call Quickstart", h1))
    story.append(Paragraph("<b>On-Call Quickstart:</b> When paged, check the Grafana <i>Minecraft Server Health</i> dashboard first. To determine if the outage is user-visible, check the Grafana dashboard's <i>Pod Ready</i> and <i>Service Reachability</i> panels (or run <font name='Courier'>nmap -sV -Pn -p T:25565 [IP]</font>). If the Minecraft port is closed or the pod ready state is 0, players cannot connect. If the pod is not ready, run <font name='Courier'>kubectl describe pod</font> to identify scheduling or image pull errors. Check S3 backup logs if disk usage is full.", normal))
    
    story.append(Paragraph("<b>5.1 Alert: MinecraftPodCrashLooping</b>", h2))
    story.append(Paragraph("<b>Trigger:</b> <font name='Courier'>increase(kube_pod_container_status_restarts_total...[10m]) >= 5</font>", normal))
    story.append(Paragraph("<b>Player-Visible Impact:</b> Yes. Players cannot connect or are actively being disconnected repeatedly.", normal))
    story.append(Paragraph("<b>Threshold Justification:</b> 5 restarts within a 10-minute window indicates a genuine crash loop rather than a standard initialization delay.", normal))
    story.append(Paragraph("<b>First-Response & Resolution Steps:</b>", normal))
    story.append(Paragraph("1. Retrieve the logs of the crashed container's previous execution:", normal))
    story.append(Paragraph("sudo k3s kubectl logs -l app=minecraft -c minecraft --previous", code_block))
    story.append(Paragraph("2. Look for JVM initialization errors. If there is a Java version mismatch, update the ConfigMap to pin the correct version:", normal))
    story.append(Paragraph("sudo k3s kubectl patch configmap minecraft-config --type=merge -p '{\"data\":{\"VERSION\": \"1.20.4\"}}'", code_block))
    story.append(Paragraph("3. Perform a rollout restart to apply the configuration:", normal))
    story.append(Paragraph("sudo k3s kubectl rollout restart deployment/minecraft-server", code_block))
    
    story.append(Paragraph("<b>5.2 Alert: NodeMemoryPressureHigh</b>", h2))
    story.append(Paragraph("<b>Trigger:</b> Available memory / Total memory * 100 > 85% for 5m.", normal))
    story.append(Paragraph("<b>Player-Visible Impact:</b> Indirectly. May cause server lag or an eventual out-of-memory kill (which occurred to the Grafana pod during setup).", normal))
    story.append(Paragraph("<b>Threshold Justification:</b> 85% provides an early warning buffer, allowing time to scale resources before a hard OOM kill occurs.", normal))
    story.append(Paragraph("<b>First-Response & Resolution Steps:</b>", normal))
    story.append(Paragraph("1. Identify memory-intensive pods on the cluster namespace:", normal))
    story.append(Paragraph("sudo k3s kubectl top pods -A", code_block))
    story.append(Paragraph("2. Identify memory-intensive processes running directly on the host:", normal))
    story.append(Paragraph("top -o %MEM -b -n 1 | head -n 20", code_block))
    story.append(Paragraph("3. If Prometheus or Grafana is consuming excessive memory, update their limits in the monitoring values:", normal))
    story.append(Paragraph("sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm upgrade monitoring prometheus-community/kube-prometheus-stack -n monitoring -f /opt/minecraft-k8s/monitoring-values.yaml", code_block))

    story.append(Paragraph("<b>5.3 Alert: NodeDiskUsageHigh</b>", h2))
    story.append(Paragraph("<b>Trigger:</b> Root disk usage is > 80% for 5 minutes.", normal))
    story.append(Paragraph("<b>Player-Visible Impact:</b> Indirectly. World saves and S3 backups will silently fail if disk hits 100%.", normal))
    story.append(Paragraph("<b>Threshold Justification:</b> 80% warns the operator early so they can clear space before world corruption occurs.", normal))
    story.append(Paragraph("<b>First-Response & Resolution Steps:</b>", normal))
    story.append(Paragraph("1. Check host disk usage by directory to locate large files:", normal))
    story.append(Paragraph("sudo du -sh /* 2>/dev/null | sort -h", code_block))
    story.append(Paragraph("2. Prune containerd builder and container image caches:", normal))
    story.append(Paragraph("sudo crictl rmi --prune", code_block))
    story.append(Paragraph("3. Vacuum system journal logs to free space instantly:", normal))
    story.append(Paragraph("sudo journalctl --vacuum-time=1d", code_block))
    story.append(Spacer(1, 10))

    # 6. Log Investigation and Incident Drill
    story.append(Paragraph("6. Log Investigation & Incident Drill", h1))
    
    story.append(Paragraph("<b>6.1 Log Investigation</b>", h2))
    story.append(Paragraph("To retrieve raw logs, execute the following command to tail the last 20 lines of the Minecraft server container log:", normal))
    story.append(Paragraph("sudo k3s kubectl logs -l app=minecraft -c minecraft --tail=20", code_block))
    story.append(Paragraph("Look for the line: <font name='Courier'>[Server thread/INFO]: Done (...s)! For help, type \"help\"</font>. This specific event confirms the JVM has finished loading the world and is actively accepting TCP connections.", normal))
    story.append(Paragraph("<b>Log Location & Search Strategy:</b> Logs physically reside on the EC2 host under the containerd runtime directories (specifically at <font name='Courier'>/var/log/pods/default_minecraft-server-.../*</font>) and are retrievable via the Kubernetes API. When troubleshooting an incident, the operator should first search for keywords like <font name='Courier'>WARN</font>, <font name='Courier'>ERROR</font>, <font name='Courier'>Exception</font>, or <font name='Courier'>OutOfMemory</font>, and verify container initialization by looking for the <font name='Courier'>Done</font> startup confirmation.", normal))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>6.2 Incident Drill: Bad Deployment Rollout</b>", h2))
    drill_items = [
        ListItem(Paragraph("<b>Failure Introduced:</b> An update was deployed utilizing an invalid image tag:", bullet_style)),
        ListItem(Paragraph("sudo k3s kubectl set image deployment/minecraft-server minecraft=...:nonexistent-tag", code_block)),
        ListItem(Paragraph("<b>Detection:</b> The <font name='Courier'>kubectl rollout status</font> command hung indefinitely. A diagnostic check of the events (<font name='Courier'>sudo k3s kubectl get events --sort-by=.lastTimestamp</font>) explicitly highlighted an <font name='Courier'>ErrImagePull</font> and subsequent <font name='Courier'>ImagePullBackOff</font> error.", bullet_style)),
        ListItem(Paragraph("<b>Recovery:</b> The deployment was seamlessly reverted to the previous functional ReplicaSet:", bullet_style)),
        ListItem(Paragraph("sudo k3s kubectl rollout undo deployment/minecraft-server", code_block)),
        ListItem(Paragraph("<b>Confirmation:</b> Executed <font name='Courier'>nmap -sV -Pn -p T:25565 [IP]</font> to confirm the port was open and the MOTD broadcasted correctly.", bullet_style))
    ]
    story.append(ListFlowable(drill_items, bulletType='bullet', start=''))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>6.3 Incident Postmortem & Prevention</b>", h2))
    story.append(Paragraph("<b>Root Cause:</b> A bad deploy was executed by setting the Minecraft deployment to a non-existent image tag. This caused Kubernetes to transition the pod to an <font name='Courier'>ErrImagePull</font> and <font name='Courier'>ImagePullBackOff</font> state, halting the rollout.<br/><b>Recovery:</b> Executed <font name='Courier'>kubectl rollout undo</font> to rollback to the previous stable ReplicaSet.<br/><b>Prevention:</b> Implement a pre-push image verification process or a validation step in our deployment scripts to verify that image tags exist in the ECR registry before updating the deployment manifest.", normal))
    story.append(Spacer(1, 10))

    # 7. Cost Controls & Teardown Checklist
    story.append(Paragraph("7. Cost Controls & Teardown Checklist", h1))
    
    cost_items = [
        ListItem(Paragraph("<b>Data Retention Limitations:</b> Prometheus metrics retention is explicitly capped to 3 days (<font name='Courier'>retention: 3d</font>) in <font name='Courier'>monitoring-values.yaml</font> to prevent EBS disk bloat over time.", bullet_style)),
        ListItem(Paragraph("<b>Memory Guardrails:</b> Strict memory requests (256Mi) and limits (512Mi) are placed on the Prometheus and Grafana pods to prevent them from starving the Minecraft JVM.", bullet_style)),
        ListItem(Paragraph("<b>Automated Stop Schedule:</b> The EC2 instance is configured with a nightly stop schedule (e.g. stopped daily at 7:00 PM via AWS Instance Scheduler or cron) to prevent idle compute billing when the lab is not in use.", bullet_style)),
        ListItem(Paragraph("<b>Monitoring Stack Teardown:</b> Run <font name='Courier'>helm uninstall monitoring -n monitoring</font> to instantly drop the resource load of the observability stack.", bullet_style)),
        ListItem(Paragraph("<b>Infrastructure Teardown:</b> Run <font name='Courier'>terraform destroy</font> from <font name='Courier'>ops3-4-5/</font> on the local machine after recording completes to terminate the EC2 instance and avoid unwanted billing. Note: This teardown is performed outside the video walkthrough itself.", bullet_style))
    ]
    story.append(ListFlowable(cost_items, bulletType='bullet'))

    # Build the PDF
    doc.build(story)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    create_pdf()