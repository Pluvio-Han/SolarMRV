#!/bin/bash
ssh -n -f -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "sh -c 'cd ~/fisco/nodes/1.12.43.152 && bash stop_all.sh && nohup bash start_all.sh > /dev/null 2>&1 &'"
ssh -n -f -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "sh -c 'cd ~/fisco/nodes/106.53.76.27 && bash stop_all.sh && nohup bash start_all.sh > /dev/null 2>&1 &'"
ssh -n -f -o StrictHostKeyChecking=no root@206.189.44.223 "sh -c 'cd ~/fisco/nodes/206.189.44.223 && bash stop_all.sh && nohup bash start_all.sh > /dev/null 2>&1 &'"
