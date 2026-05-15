#!/bin/bash
# Stop all nodes
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "cd ~/fisco/nodes/1.12.43.152 && bash stop_all.sh"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "cd ~/fisco/nodes/106.53.76.27 && bash stop_all.sh"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "cd ~/fisco/nodes/206.189.44.223 && bash stop_all.sh"

sleep 3

# Force wipe data independently of stop script status
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "rm -rf ~/fisco/nodes/1.12.43.152/node0/data ~/fisco/nodes/1.12.43.152/node1/data"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "rm -rf ~/fisco/nodes/106.53.76.27/node0/data ~/fisco/nodes/106.53.76.27/node1/data"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "rm -rf ~/fisco/nodes/206.189.44.223/node0/data ~/fisco/nodes/206.189.44.223/node1/data"

sleep 3

# Start all nodes
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "cd ~/fisco/nodes/1.12.43.152 && bash start_all.sh"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "cd ~/fisco/nodes/106.53.76.27 && bash start_all.sh"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "cd ~/fisco/nodes/206.189.44.223 && bash start_all.sh"
echo "CLUSTER WIPE AND RESTART COMPLETE"
