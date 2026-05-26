import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Image
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = "ops-4-documentation.pdf"
IMAGE_FILENAME = "architecture.png"

styles = getSampleStyleSheet()

def style(name, parent='Normal', **kwargs):
    return ParagraphStyle(name, parent=styles[parent], **kwargs)

title_style    = style('DocTitle',    'Title',   fontSize=22, textColor=colors.HexColor('#1a1a2e'), spaceAfter=4)
subtitle_style = style('DocSubtitle', 'Normal',  fontSize=11, textColor=colors.HexColor('#4a4a6a'), spaceAfter=2, alignment=TA_CENTER)
h1_style       = style('H1',          'Heading1', fontSize=14, textColor=colors.HexColor('#1a1a2e'),
                        spaceBefore=18, spaceAfter=6, borderPad=4,
                        backColor=colors.HexColor('#e8eaf6'), borderWidth=0, leftIndent=-6)
h2_style       = style('H2',          'Heading2', fontSize=11, textColor=colors.HexColor('#283593'),
                        spaceBefore=12, spaceAfter=4)
body_style     = style('Body',        'Normal',   fontSize=9,  leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
bullet_style   = style('Bullet',      'Normal',   fontSize=9,  leading=13, leftIndent=16, spaceAfter=2,
                        bulletIndent=6)
code_style     = style('Code',        'Normal',   fontSize=8,  leading=12, fontName='Courier',
                        backColor=colors.HexColor('#f5f5f5'), leftIndent=12, rightIndent=12,
                        spaceAfter=6, spaceBefore=4, borderWidth=1,
                        borderColor=colors.HexColor('#e0e0e0'), borderPad=6)
label_style    = style('Label',       'Normal',   fontSize=8,  fontName='Helvetica-Bold',
                        textColor=colors.HexColor('#283593'))
note_style     = style('Note',        'Normal',   fontSize=8,  leading=12, leftIndent=12,
                        textColor=colors.HexColor('#555555'), spaceAfter=4)
link_style     = style('Link',        'Normal',   fontSize=9,  textColor=colors.HexColor('#1565c0'),
                        leading=14)

def h1(text):      return Paragraph(f"&nbsp;&nbsp;{text}", h1_style)
def h2(text):      return Paragraph(text, h2_style)
def body(text):    return Paragraph(text, body_style)
def bullet(text):  return Paragraph(f"• &nbsp;{text}", bullet_style)
def code(text):    return Paragraph(text.replace('\n','<br/>').replace(' ','&nbsp;'), code_style)
def note(text):    return Paragraph(f"<i>{text}</i>", note_style)
def link(url, label=None): return Paragraph(f'<link href="{url}" color="#1565c0">{label or url}</link>', link_style)
def sp(n=6):       return Spacer(1, n)
def hr():          return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#c5cae9'), spaceAfter=6, spaceBefore=6)

def section_table(rows):
    """Two-column key/value table."""
    data = [[Paragraph(k, label_style), Paragraph(v, body_style)] for k, v in rows]
    t = Table(data, colWidths=[1.6*inch, 5.2*inch])
    t.setStyle(TableStyle([
        ('VALIGN',    (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#f3f4fb')]),
        ('GRID',      (0,0), (-1,-1), 0.25, colors.HexColor('#c5cae9')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

def checklist_table(items):
    data = [[Paragraph('☐', label_style), Paragraph(item, body_style)] for item in items]
    t = Table(data, colWidths=[0.3*inch, 6.5*inch])
    t.setStyle(TableStyle([
        ('VALIGN',    (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#f3f4fb')]),
        ('GRID',      (0,0), (-1,-1), 0.25, colors.HexColor('#c5cae9')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch,
    title="Ops 4: Container Orchestration - Documentation",
    author="Dean Leon"
)

story = []

story += [
    sp(30),
    Paragraph("Ops 4: Container Orchestration", title_style),
    Paragraph("Minecraft on Kubernetes (k3s) - CS 312 System Administration", subtitle_style),
    Paragraph("Dean Leon &nbsp;·&nbsp; Student ID: 934513949", subtitle_style),
    sp(6),
    hr(),
    sp(8),
    section_table([
        ("Repository",    '<link href="https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram" color="#1565c0">https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram</link>'),
        ("Video",         '<link href="https://media.oregonstate.edu/media/t/1_hoshsdsl" color="#1565c0">https://media.oregonstate.edu/media/t/1_hoshsdsl</link>'),
        ("Checkpoints",   "CP1: 00:04 &nbsp;·&nbsp; CP2: 00:28 &nbsp;·&nbsp; CP3: 01:07 &nbsp;·&nbsp; CP4: 01:57"),
        ("AWS Region",    "us-east-1"),
        ("Instance",      "t3.medium · Ubuntu 22.04 LTS · 20 GB gp3"),
        ("Kubernetes",    "k3s v1.35.5+k3s1 (single-node)"),
        ("Image",         "998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:v1.20.4"),
    ]),
    sp(6),
    body("This document was made with Python's ReportLab library. LLMs were utlised to format the document, ensure that all required sections were included, "
        "and to verify the correctness of content. The architecture diagram was created with Mermaid.js and exported as a PNG. The video walkthrough was edited to remove sections of waiting in order to meet the 3 minute requirement."),
    sp(12),
    hr(),
]

story += [
    PageBreak(),
    h1("1. Architecture"),
    sp(4),
    body("The diagram below shows all components. Terraform provisions the EC2 host and security group. "
         "Ansible installs k3s, configures the ECR credential provider, restores world data from S3, "
         "and applies Kubernetes manifests. All AWS API calls from the node use the attached "
         "<b>LabInstanceProfile</b> IAM role, no credentials are hardcoded anywhere."),
    sp(10),
]

if os.path.exists(IMAGE_FILENAME):
    img = Image(IMAGE_FILENAME)
    max_width = 6.5 * inch
    if img.drawWidth > max_width:
        ratio = max_width / img.drawWidth
        img.drawWidth = max_width
        img.drawHeight = img.drawHeight * ratio
    story.append(img)
else:
    story.append(note(f"[Error: Missing {IMAGE_FILENAME}.]"))

story.append(sp(8))

story += [
    h1("2. Repository File Map"),
    sp(4),
    body("All submission files are in the <b>ops3-4/</b> directory of the repository."),
    sp(6),
    section_table([
        ("ops3-4/main.tf",                   "Terraform: EC2 instance, security group, Ansible trigger"),
        ("ops3-4/variables.tf",              "Terraform: input variable declarations"),
        ("ops3-4/terraform.tfvars",          "Terraform: key name, PEM path, SSH CIDR"),
        ("ops3-4/playbook.yml",              "Ansible: k3s install, ECR credential provider, S3 restore, manifest apply"),
        ("ops3-4/k8s/configmap.yml",         "Kubernetes ConfigMap, EULA, VERSION, MOTD, MEMORY"),
        ("ops3-4/k8s/pvc.yml",               "Kubernetes PersistentVolumeClaim, 10Gi local-path"),
        ("ops3-4/k8s/deployment.yml",        "Kubernetes Deployment, probes, resources, volume mount"),
        ("ops3-4/k8s/service.yml",           "Kubernetes Service, LoadBalancer :25565"),
        ("ops3-4/k8s/backup-cronjob.yml",    "Kubernetes CronJob, S3 backup every 6 hours"),
        ("ops3-4/checklist.sh",       "Video checkpoint command reference"),
    ]),
    sp(6),
]

story += [
    h1("3. Deployment Runbook"),
    sp(4),
    body("An operator with no prior knowledge of this setup should be able to deploy the server "
         "from scratch by following these steps in order."),
    sp(6),

    h2("3.1  Prerequisites"),
    bullet("AWS Academy lab started, CLI credentials pasted into <b>~/.aws/credentials</b>"),
    bullet("SSH key pair <b>cs312-key</b> exists in AWS and <b>~/.ssh/cs312-key.pem</b> exists locally"),
    bullet("Terraform ≥ 1.5, Ansible ≥ 2.14, Docker, nmap installed locally"),
    bullet("ECR repository <b>minecraft-server</b> exists, images <b>v1.20.4</b> and <b>v1.20.5</b> pushed"),
    bullet("S3 bucket <b>ops3-minecraft-bucket</b> exists (world data or empty)"),
    sp(6),

    h2("3.2  Push images to ECR (first time or after session reset)"),
    code(
        "aws ecr create-repository --repository-name minecraft-server --region us-east-1\n"
        "aws ecr get-login-password --region us-east-1 | \\\n"
        "  docker login --username AWS --password-stdin \\\n"
        "  998487032255.dkr.ecr.us-east-1.amazonaws.com\n\n"
        "docker pull itzg/minecraft-server:java21\n"
        "docker tag itzg/minecraft-server:java21 \\\n"
        "  998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:v1.20.4\n"
        "docker push 998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:v1.20.4\n\n"
        "# Tag same image as v1.20.5 for rollout demo\n"
        "docker tag ...v1.20.4 ...v1.20.5 && docker push ...v1.20.5"
    ),
    sp(4),

    h2("3.3  Provision infrastructure"),
    code(
        "cd ops3-4/\n"
        "# Set your IP in terraform.tfvars: ssh_allowed_cidr = \"YOUR.IP/32\"\n"
        "terraform init\n"
        "terraform apply\n"
        "# Terraform provisions EC2, then auto-runs Ansible.\n"
        "# Full run takes ~3-5 minutes. Note the output: server_public_ip"
    ),
    note("If Ansible fails partway through, re-run it directly: "
         "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i '<IP>,' -u ubuntu "
         "--private-key ~/.ssh/cs312-key.pem playbook.yml"),
    sp(4),

    h2("3.4  Verify deployment"),
    code(
        "ssh -i ~/.ssh/cs312-key.pem ubuntu@<PUBLIC_IP>\n"
        "sudo kubectl get nodes          # STATUS = Ready\n"
        "sudo kubectl get pods           # 1/1 Running (may take 90s)\n"
        "sudo kubectl get svc            # minecraft-service EXTERNAL-IP visible\n\n"
        "# From local machine:\n"
        "nmap -sV -Pn -p T:25565 <PUBLIC_IP>"
    ),
    sp(6),

    h2("3.5  Service exposure on port 25565"),
    body("The Kubernetes Service is type <b>LoadBalancer</b>. On single-node k3s, the built-in "
         "ServiceLB (klipper-lb) binds port 25565 directly on the host's network interface. "
         "The AWS Security Group allows TCP 25565 from 0.0.0.0/0. No Ingress controller or "
         "NodePort mapping is needed, players connect directly to the EC2 public IP on 25565."),
    sp(6),

    h2("3.6  Rollout to new image version"),
    code(
        "sudo kubectl set image deployment/minecraft-server \\\n"
        "  minecraft=998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:v1.20.5\n\n"
        "sudo kubectl rollout status deployment/minecraft-server\n"
        "sudo kubectl rollout history deployment/minecraft-server"
    ),
    sp(4),

    h2("3.7  Rollback to previous version"),
    code(
        "sudo kubectl rollout undo deployment/minecraft-server\n"
        "sudo kubectl rollout status deployment/minecraft-server\n\n"
        "# Verify server is joinable after rollback:\n"
        "nmap -sV -Pn -p T:25565 <PUBLIC_IP>"
    ),
    sp(6),
]

story += [
    PageBreak(),
    h1("4. Backup and Restore"),
    sp(4),

    h2("4.1  Backup procedure"),
    body("World data is backed up to S3 automatically by a Kubernetes CronJob that runs every 6 hours. "
         "The job mounts the same PVC as the Minecraft pod (read-only) and runs <b>aws s3 sync</b> "
         "using credentials from the node's IAM instance profile."),
    sp(4),
    body("To trigger a manual backup immediately:"),
    code(
        "sudo kubectl create job --from=cronjob/minecraft-s3-backup manual-backup-$(date +%s)\n"
        "sudo kubectl get jobs\n"
        "sudo kubectl logs job/manual-backup-<id>"
    ),
    sp(4),
    body("To verify backup contents in S3:"),
    code("aws s3 ls s3://ops3-minecraft-bucket/ --recursive --human-readable"),
    sp(6),

    h2("4.2  Step-by-step restore from S3"),
    body("Follow these steps exactly to restore world data on a fresh instance. "
         "The Ansible playbook runs the S3 sync <i>before</i> applying Kubernetes manifests, "
         "so the PV is pre-populated when the pod first starts."),
    sp(4),
]

restore_steps = [
    "Start AWS Academy lab session and refresh ~/.aws/credentials on your local machine.",
    "Confirm S3 bucket has data: <b>aws s3 ls s3://ops3-minecraft-bucket/</b>",
    "Run <b>terraform apply</b> from ops3-4/. Ansible will automatically sync S3 -> /opt/minecraft-data/ on the EC2 host.",
    "Ansible then applies all Kubernetes manifests. The Deployment mounts the PVC at /data.",
    "k3s local-path provisioner creates the PV directory under /var/lib/rancher/k3s/storage/ and "
      "the pod's /data is bind-mounted there.",
    "SSH into EC2 and verify: <b>sudo kubectl exec &lt;pod&gt; -- ls /data</b>, you should see world/, "
      "server.properties, etc.",
    "Connect with nmap or Minecraft client to confirm the server is running with restored world.",
]
for i, step in enumerate(restore_steps, 1):
    story.append(Paragraph(f"<b>{i}.</b> &nbsp;{step}", bullet_style))
story.append(sp(4))

story += [
    note("If restoring to an existing instance (no terraform apply): SSH in, run "
         "'aws s3 sync s3://ops3-minecraft-bucket/ /opt/minecraft-data/', "
         "then 'sudo kubectl rollout restart deployment/minecraft-server'."),
    sp(6),
]

story += [
    h1("5. Tradeoff Notes"),
    sp(4),

    h2("5.1  Workload controller: Deployment vs StatefulSet"),
    body("A <b>Deployment</b> with <b>strategy: Recreate</b> is used rather than a StatefulSet. "
         "A StatefulSet provides stable network identity and ordered pod management, which are "
         "valuable for clustered databases. Minecraft is a single-replica stateful workload with "
         "no peer discovery requirement, the stable hostname benefit of StatefulSet does not apply. "
         "A Deployment with Recreate strategy is simpler to operate and sufficient: it guarantees "
         "the old pod is fully terminated before the new one starts, preventing two processes from "
         "simultaneously holding the ReadWriteOnce PVC."),
    sp(4),

    h2("5.2  Persistence: local-path PVC vs cloud-managed EBS"),
    body("The k3s default <b>local-path</b> storage class provisions volumes on the node's local disk "
         "under /var/lib/rancher/k3s/storage/. This is simple and zero-cost. The tradeoff is that "
         "data is tied to the node: if the EC2 instance is <i>terminated</i> (not just rebooted), "
         "the PV data is lost. This is acceptable for this assignment because: (1) the assignment "
         "scope is single-node k3s, (2) world data is backed up to S3 every 6 hours, and (3) "
         "the restore procedure is documented and tested. In a production environment, an EBS-backed "
         "StorageClass (e.g. the AWS EBS CSI driver) would be preferred for node-independent durability."),
    sp(4),

    h2("5.3  Service exposure: LoadBalancer vs NodePort"),
    body("Service type <b>LoadBalancer</b> is used. On single-node k3s, ServiceLB (klipper-lb) "
         "binds the service port directly on the host without requiring an external load balancer. "
         "NodePort was avoided because it maps to a high port (30000-32767), requiring an extra "
         "firewall rule and forcing players to use a non-standard port. LoadBalancer keeps port 25565 "
         "standard and the security group rule minimal. Ingress is HTTP/HTTPS only and not applicable "
         "to the Minecraft TCP protocol."),
    sp(4),

    h2("5.4  Probe configuration"),
    body("All three probe types are configured using <b>tcpSocket</b> on port 25565. A TCP socket "
         "check is a weaker health signal than a true application-level check (an open port does not "
         "guarantee the server has finished loading the world), but Minecraft exposes no HTTP health "
         "endpoint. The <b>startupProbe</b> allows up to 10 × 30s = 300 seconds for initial JVM and "
         "world loading before liveness/readiness checks begin, preventing restart loops during "
         "warmup. Once the startupProbe succeeds, the livenessProbe restarts the pod if the port "
         "stops responding (crash detection), and the readinessProbe gates Service traffic until "
         "the port is open."),
    sp(4),

    h2("5.5  Resource requests and limits"),
    body("Requests (1 CPU, 2 Gi memory) guarantee the scheduler places the pod on a node with "
         "sufficient capacity and prevent eviction under normal load. Limits (2 CPU, 2500 Mi) "
         "cap resource consumption: the MEMORY env var sets the JVM heap to 2G, leaving ~500 Mi "
         "for JVM overhead and the OS. The CPU limit of 2 allows bursting during chunk generation "
         "without starving other system processes. On a t3.medium (2 vCPU, 4 GB), these limits "
         "leave ~1.5 GB for k3s system pods and the OS."),
    sp(6),
]

story += [
    PageBreak(),
    h1("6. Teardown Checklist"),
    sp(4),
    body("Complete all steps below after finishing the assignment to prevent runaway AWS credit consumption."),
    sp(8),
    checklist_table([
        "Run <b>terraform destroy</b> from ops3-4/ to terminate the EC2 instance and delete the security group.",
        "Confirm EC2 instance is terminated in the AWS Console (EC2 -> Instances).",
        "Confirm the security group <b>minecraft_security_group_ops4</b> has been deleted.",
        "Optionally delete the ECR repository to avoid storage costs: "
         "<b>aws ecr delete-repository --repository-name minecraft-server --force --region us-east-1</b>",
        "Optionally empty and delete the S3 backup bucket if world data is no longer needed: "
         "<b>aws s3 rb s3://ops3-minecraft-bucket --force</b>",
        "Click <b>End Lab</b> in the AWS Academy Learner Lab interface.",
        "Verify credit balance the next day, AWS Academy credits update daily, not in real time.",
        "Delete local terraform.tfstate if it contains sensitive output values.",
    ]),
    sp(12),
    hr(),
    sp(6),
    body("Cost controls in place during the assignment:"),
    bullet("<b>Instance size:</b> t3.medium (~$0.0416/hr), minimum viable for Minecraft + k3s overhead"),
    bullet("<b>Stop schedule:</b> End Lab after every session, terraform destroy when not recording"),
    bullet("<b>SSH restriction:</b> Security group limits port 22 to a single known IP (/32 CIDR)"),
    bullet("<b>No RDS or NAT gateway:</b> default VPC used, no additional billable network services"),
    bullet("<b>ECR/S3:</b> minimal storage, well under free tier thresholds for short assignment duration"),
]

doc.build(story)
print(f"PDF written to {OUTPUT}")