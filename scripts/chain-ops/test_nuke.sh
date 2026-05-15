#!/bin/bash
# Force kill on Gwen
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "killall -9 fisco-bcos || true; rm -rf ~/fisco/nodes/1.12.43.152/node0/data ~/fisco/nodes/1.12.43.152/node1/data"
# Force kill on Miles
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "killall -9 fisco-bcos || true; rm -rf ~/fisco/nodes/106.53.76.27/node0/data ~/fisco/nodes/106.53.76.27/node1/data"
# Force kill on Peter
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "killall -9 fisco-bcos || true; rm -rf ~/fisco/nodes/206.189.44.223/node0/data ~/fisco/nodes/206.189.44.223/node1/data"

echo "VERIFYING ALL SERVERS ARE CLEAN..."
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "ps -ef | grep fisco-bcos | grep -v grep; ls -la ~/fisco/nodes/1.12.43.152/node0/data 2>/dev/null"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "ps -ef | grep fisco-bcos | grep -v grep; ls -la ~/fisco/nodes/106.53.76.27/node0/data 2>/dev/null"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "ps -ef | grep fisco-bcos | grep -v grep; ls -la ~/fisco/nodes/206.189.44.223/node0/data 2>/dev/null"

sleep 3

# Start all nodes
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "cd ~/fisco/nodes/1.12.43.152 && bash start_all.sh"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "cd ~/fisco/nodes/106.53.76.27 && bash start_all.sh"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "cd ~/fisco/nodes/206.189.44.223 && bash start_all.sh"
echo "CLUSTER WIPE AND RESTART COMPLETE"
