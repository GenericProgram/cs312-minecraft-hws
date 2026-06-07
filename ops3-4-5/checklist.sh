#!/bin/bash
# Ops 4 Video Recording Script
# All commands run on EC2 (SSH) unless marked [WSL2]

# ─────────────────────────────────────────────────────────────
# CHECKPOINT 1: k3s running and reachable (0:00)
# ─────────────────────────────────────────────────────────────
sudo kubectl get nodes
sudo kubectl get pods

# [WSL2] Run this from your local machine:
# nmap -sV -Pn -p T:25565 54.157.98.103


# ─────────────────────────────────────────────────────────────
# CHECKPOINT 2: Persistence after pod deletion
# ─────────────────────────────────────────────────────────────

# Get the current pod name first
POD=$(sudo kubectl get pods -l app=minecraft -o jsonpath='{.items[0].metadata.name}')

sudo kubectl delete pod $POD

# Watch the replacement come up
sudo kubectl get pods -w
# Press Ctrl+C once the new pod is 1/1 Running

# Get the new pod name and verify world data is still there
NEW_POD=$(sudo kubectl get pods -l app=minecraft -o jsonpath='{.items[0].metadata.name}')
sudo kubectl exec $NEW_POD -- ls /data


# ─────────────────────────────────────────────────────────────
# CHECKPOINT 3: Rollout to new version, then rollback
# Prerequisites: push v1.20.5 to ECR first from WSL2:
#   docker tag ...v1.20.4 ...v1.20.5
#   docker push ...v1.20.5
# ─────────────────────────────────────────────────────────────
sudo kubectl set image deployment/minecraft-server \
  minecraft=998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:v1.20.5

# Wait for rollout to complete
sudo kubectl rollout status deployment/minecraft-server

# Show rollout history
sudo kubectl rollout history deployment/minecraft-server

# Roll back to v1.20.4
sudo kubectl rollout undo deployment/minecraft-server
sudo kubectl rollout status deployment/minecraft-server

# [WSL2] Confirm server is joinable after rollback:
# nmap -sV -Pn -p T:25565 54.157.98.103


# ─────────────────────────────────────────────────────────────
# CHECKPOINT 4: Failure drill — bad image tag
# ─────────────────────────────────────────────────────────────

# Introduce the failure
sudo kubectl set image deployment/minecraft-server \
  minecraft=998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:does-not-exist

# Watch the new pod get stuck
sudo kubectl get pods -w
# Press Ctrl+C once you see ErrImagePull or ImagePullBackOff

# Show authoritative diagnostic output
BAD_POD=$(sudo kubectl get pods -l app=minecraft -o jsonpath='{.items[0].metadata.name}')
sudo kubectl describe pod $BAD_POD

# Roll back to restore service
sudo kubectl rollout undo deployment/minecraft-server
sudo kubectl rollout status deployment/minecraft-server

# Verify world data intact after recovery
RECOVERED_POD=$(sudo kubectl get pods -l app=minecraft -o jsonpath='{.items[0].metadata.name}')
sudo kubectl exec $RECOVERED_POD -- ls /data

# [WSL2] Final confirmation server is joinable:
# nmap -sV -Pn -p T:25565 54.157.98.103