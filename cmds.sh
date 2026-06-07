#cp3
sudo k3s kubectl logs -l app=minecraft -c minecraft --tail=20
sudo k3s kubectl get events --sort-by=.lastTimestamp -n default | tail -10

#cp4
sudo k3s kubectl set image deployment/minecraft-server minecraft=998487032255.dkr.ecr.us-east-1.amazonaws.com/minecraft-server:nonexistent-tag
sudo k3s kubectl rollout status deployment/minecraft-server
sudo k3s kubectl describe pod -l app=minecraft | grep -A8 "Events:"

sudo k3s kubectl rollout undo deployment/minecraft-server
sudo k3s kubectl rollout status deployment/minecraft-server

sudo k3s kubectl get pods

#on wsl
nmap -sV -Pn -p T:25565 18.234.67.8 