#!/bin/bash
for port in node0 node1; do
    ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "sed -i '/node.5/d' ~/fisco/nodes/1.12.43.152/$port/config.ini && sed -i '/node.4=206.189.44.223:30300/a\    node.5=206.189.44.223:30301' ~/fisco/nodes/1.12.43.152/$port/config.ini"
    ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "sed -i '/node.5/d' ~/fisco/nodes/106.53.76.27/$port/config.ini && sed -i '/node.4=206.189.44.223:30300/a\    node.5=206.189.44.223:30301' ~/fisco/nodes/106.53.76.27/$port/config.ini"
done

# Restart Gwen and Miles
ssh -n -f -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "sh -c 'cd ~/fisco/nodes/1.12.43.152 && bash stop_all.sh && nohup bash start_all.sh > /dev/null 2>&1 &'"
ssh -n -f -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "sh -c 'cd ~/fisco/nodes/106.53.76.27 && bash stop_all.sh && nohup bash start_all.sh > /dev/null 2>&1 &'"
# Restart Peter to make sure it reconnects fast
ssh -n -f -o StrictHostKeyChecking=no root@206.189.44.223 "sh -c 'cd ~/fisco/nodes/206.189.44.223 && bash stop_all.sh && nohup bash start_all.sh > /dev/null 2>&1 &'"
