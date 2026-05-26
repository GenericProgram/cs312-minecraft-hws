# Minecraft Operator Runbook

Dean Leon | CS 312

---

## 0. Assumptions & Prerequisites

* AWS account with permissions for EC2, ECR, and S3
* AWS CLI installed and configured (`aws configure`)
* SSH access to EC2 instance
* Ubuntu-based EC2 instance (t2.medium recommended)
* Docker and Docker Compose available or installable

---

## 1. Runtime Architecture

The Minecraft server is deployed as a containerized service on an EC2 instance.

**Traffic Flow:**
Internet Clients → AWS Security Group (TCP 25565) → EC2 Host → Docker → Minecraft Container → Persistent Storage (EBS via bind mount)

**Key Design Decisions:**

* Port 25565 exposed for Minecraft traffic
* Docker container isolates runtime
* Persistent data stored outside container (`/data` bind mount)
* EBS ensures durability across restarts

---

## 2. Initial Deployment (From Scratch)

### Step 1: Install Dependencies

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

### Step 2: Authenticate to AWS ECR

```bash
aws ecr get-login-password --region us-east-1 \
| docker login --username AWS --password-stdin <ECR_URL>
```

### Step 3: Create Project Directory

```bash
mkdir -p ~/minecraft-server
cd ~/minecraft-server
```

### Step 4: Create docker-compose.yml

```yaml
services:
  minecraft:
    image: <ECR_URL>/cs312-minecraft:mc-1.20.4-build1
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      VERSION: "1.20.4"
      MOTD: "Dean Leon - CS312"
    volumes:
      - ./data:/data
    restart: always
```

### Step 5: Start the Service

```bash
docker compose up -d
```

---

## 3. Container & Image Management

### Image Policy

* All images are stored in private ECR
* **Do NOT use `latest` tag**
* Use immutable tagging: `mc-<version>-build<number>`

### Build & Publish Workflow

```bash
# Authenticate
aws ecr get-login-password --region us-east-1 \
| docker login --username AWS --password-stdin <ECR_URL>

# Tag upstream image
docker tag itzg/minecraft-server:latest \
<ECR_URL>/cs312-minecraft:mc-1.20.5-build1

# Push image
docker push <ECR_URL>/cs312-minecraft:mc-1.20.5-build1
```

---

## 4. Upgrade and Rollback Runbook

### Pre-Change Checklist

* Backup world data to S3
* Verify backup exists
* Confirm new image exists in ECR
* Identify known-good rollback version

### Upgrade Execution

```bash
# Edit docker-compose.yml (update image + VERSION)
docker compose up -d
```

### Post-Change Validation

```bash
# Check container status
docker compose ps

# Check logs
docker compose logs --tail=50

# Verify port
nmap -sV -Pn -p T:25565 localhost
```

### Rollback Execution

```bash
# Revert docker-compose.yml to previous version
docker compose up -d
```

---

## 5. Backup and Restore (S3)

### Backup Procedure

```bash
cd ~/minecraft-server

tar -czvf world-backup-$(date +%F).tar.gz data/
aws s3 cp world-backup-$(date +%F).tar.gz s3://<BUCKET_NAME>/
```

### Restore Procedure

```bash
cd ~/minecraft-server

# Stop service
docker compose down

# Remove current data
sudo rm -rf data/*

# Download backup
aws s3 cp s3://<BUCKET_NAME>/world-backup-TARGET.tar.gz .

# Extract
sudo tar -xzvf world-backup-TARGET.tar.gz

# Restart service
docker compose up -d
```

---

## 6. Monitoring & Observability

### Check Container Health

```bash
docker compose ps
```

### View Logs

```bash
docker compose logs --tail=100
```

### Resource Usage

```bash
docker stats
htop
```

### Network Verification

```bash
nmap -sV -Pn -p T:25565 localhost
```

---

## 7. Failure Scenarios & Recovery

### Scenario 1: Container Crash Loop

* Check logs (`docker compose logs`)
* Rollback to previous image

### Scenario 2: Port Not Reachable

* Verify security group allows TCP 25565
* Confirm Docker port binding

### Scenario 3: Players Cannot Connect

* Verify server is running
* Check MOTD via nmap

### Scenario 4: Corrupted World Data

* Restore from S3 backup

---

## 8. Security Considerations

* Restrict SSH access via security group
* Use IAM roles instead of static credentials
* Keep S3 bucket private
* Do not expose unnecessary ports

---

## 9. Video Demonstration

Video: [https://media.oregonstate.edu/media/t/1_tloxm5xl](https://media.oregonstate.edu/media/t/1_tloxm5xl)

Checkpoints:

* 00:06
* 00:56
* 01:26
* 02:13

---

## 10. Attribution

* Upstream image: itzg/minecraft-server
* LLM assistance used for formatting and command validation
* Repository: [https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram](https://github.com/CS-312-001-S2026/minecraft-ops-GenericProgram)

---