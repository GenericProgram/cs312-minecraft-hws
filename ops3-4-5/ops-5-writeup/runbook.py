from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def create_pdf(filename="ops_5_writeup.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    h1 = styles['Heading1']
    h2 = styles['Heading2']
    normal = styles['Normal']
    
    story = []

    # Title & Header
    story.append(Paragraph("Ops 5: Observability and Incident Response Write-up", title_style))
    story.append(Paragraph("Author: Dean Leon", title_style))
    story.append(Spacer(1, 20))

    # Video Checkpoints
    story.append(Paragraph("1. Video Submission", h1))
    story.append(Paragraph("<b>Video Link:</b> <a href='https://media.oregonstate.edu/media/t/1_g1abc3tt'>https://media.oregonstate.edu/media/t/1_g1abc3tt</a>", normal))
    
    timestamps = [
        ListItem(Paragraph("<b>Checkpoint 1 (00:03):</b> Service reachable + Grafana dashboard showing all green values.", normal)),
        ListItem(Paragraph("<b>Checkpoint 2 (00:38):</b> Alert definitions and runbook explanations.", normal)),
        ListItem(Paragraph("<b>Checkpoint 3 (01:10):</b> Log investigation (interpreting startup logs and ErrImagePull events).", normal)),
        ListItem(Paragraph("<b>Checkpoint 4 (02:07):</b> Bad deploy incident drill and recovery.", normal))
    ]
    story.append(ListFlowable(timestamps, bulletType='bullet'))
    story.append(Spacer(1, 12))

    # Architecture Diagram Placeholder
    story.append(Paragraph("2. Updated Architecture Diagram", h1))
    story.append(Paragraph("<i>[Note: Please insert your updated architecture diagram here before final submission. The diagram should include EC2, k3s, Deployment, PVC, ECR, S3, plus the newly added Prometheus, Grafana, and node exporters.]</i>", normal))
    story.append(Spacer(1, 12))

    # Repo Link & File Map
    story.append(Paragraph("3. Repository & File Map", h1))
    story.append(Paragraph("<b>GitHub Link:</b> <a href='https://github.com/GenericProgram/cs312-minecraft-hws'>https://github.com/GenericProgram/cs312-minecraft-hws</a>", normal))
    
    file_map = [
        ListItem(Paragraph("<b>helm/monitoring-values.yaml:</b> Declarative, version-controlled deployment configurations for the kube-prometheus-stack.", normal)),
        ListItem(Paragraph("<b>k8s/monitoring/prometheus-rules.yml:</b> Declarative Prometheus alert rules for the cluster.", normal)),
        ListItem(Paragraph("<b>ops-5-writeup/runbooks.md:</b> On-call quickstart and response procedures.", normal)),
        ListItem(Paragraph("<b>k8s/deployment.yml:</b> Updated Minecraft deployment containing specific app configurations.", normal)),
        ListItem(Paragraph("<b>k8s/configmap.yml:</b> Minecraft environment variables and configurations.", normal))
    ]
    story.append(ListFlowable(file_map, bulletType='bullet'))
    story.append(Spacer(1, 12))

    # On-Call Quickstart
    story.append(Paragraph("4. On-Call Quickstart", h1))
    story.append(Paragraph("When paged, check the Grafana <i>Minecraft Server Health</i> dashboard first. If the pod is not ready, run <code>kubectl describe pod</code> to identify scheduling or image pull errors. If disk usage is full, check S3 backup logs to ensure data isn't accumulating unchecked on the local node.", normal))
    story.append(Spacer(1, 12))

    # Runbooks
    story.append(Paragraph("5. Alert Runbooks", h1))
    
    # Alert 1
    story.append(Paragraph("<b>Alert 1: MinecraftPodCrashLooping</b>", h2))
    story.append(Paragraph("<b>Symptom/Trigger:</b> Pod restart count is ≥ 5 in 10 minutes.", normal))
    story.append(Paragraph("<b>Player-Visible Impact:</b> Yes, players cannot connect or are actively being disconnected.", normal))
    story.append(Paragraph("<b>Resolution Steps:</b> Run <code>kubectl logs &lt;pod-name&gt; --previous</code> to identify the crash reason. Check for Java OutOfMemory errors, corrupted world files, or incompatible server versions.", normal))
    story.append(Spacer(1, 8))

    # Alert 2
    story.append(Paragraph("<b>Alert 2: NodeMemoryPressureHigh</b>", h2))
    story.append(Paragraph("<b>Symptom/Trigger:</b> Node memory usage is > 85% for 5 minutes.", normal))
    story.append(Paragraph("<b>Player-Visible Impact:</b> Indirectly (potential for server lag or eventual OOM crash).", normal))
    story.append(Paragraph("<b>Resolution Steps:</b> Check the Grafana dashboard to see if the Minecraft JVM or Grafana/Prometheus is consuming the memory. Consider upgrading the EC2 instance type (e.g., from t3.medium to t3.large) if baseline usage is too high.", normal))
    story.append(Spacer(1, 8))

    # Alert 3
    story.append(Paragraph("<b>Alert 3: NodeDiskUsageHigh</b>", h2))
    story.append(Paragraph("<b>Symptom/Trigger:</b> Root disk usage is > 80% for 5 minutes.", normal))
    story.append(Paragraph("<b>Player-Visible Impact:</b> Indirectly (world saves will fail if disk hits 100%).", normal))
    story.append(Paragraph("<b>Resolution Steps:</b> Clear old logs or temporary files. Verify that the automated cron backups to S3 are deleting local archives successfully after upload.", normal))
    story.append(Spacer(1, 12))

    # Cost Controls
    story.append(Paragraph("6. Cost Controls", h1))
    cost_controls = [
        ListItem(Paragraph("<b>Monitoring Stack Cleanup:</b> The monitoring stack can be removed to save resources by running <code>helm uninstall monitoring -n monitoring</code>.", normal)),
        ListItem(Paragraph("<b>Data Retention:</b> Prometheus data retention is explicitly limited to 3 days (<code>retention: 3d</code>) in the helm values to prevent disk bloat.", normal)),
        ListItem(Paragraph("<b>Instance Management:</b> The EC2 instance follows a strict stop schedule when not actively in use for lab environments.", normal))
    ]
    story.append(ListFlowable(cost_controls, bulletType='bullet'))

    # Build the PDF
    doc.build(story)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    create_pdf()