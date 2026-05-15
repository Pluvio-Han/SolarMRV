#!/bin/bash
ssh -n -f -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "sh -c 'cd ~/fisco/nodes/1.12.43.152 && nohup bash start_all.sh > /dev/null 2>&1 &'"
ssh -n -f -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "sh -c 'cd ~/fisco/nodes/106.53.76.27 && nohup bash start_all.sh > /dev/null 2>&1 &'"
ssh -n -f -o StrictHostKeyChecking=no root@206.189.44.223 "sh -c 'cd ~/fisco/nodes/206.189.44.223 && nohup bash start_all.sh > /dev/null 2>&1 &'"
sleep 5
echo "VERIFYING Gwen:"
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "ps -ef | grep fisco-bcos | grep -v grep"
echo "VERIFYING Miles:"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "ps -ef | grep fisco-bcos | grep -v grep"
echo "VERIFYING Peter:"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "ps -ef | grep fisco-bcos | grep -v grep"
