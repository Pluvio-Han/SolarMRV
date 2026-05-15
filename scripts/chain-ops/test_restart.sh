#!/bin/bash
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "cd ~/fisco/nodes/1.12.43.152 && bash start_all.sh"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "cd ~/fisco/nodes/106.53.76.27 && bash start_all.sh"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "cd ~/fisco/nodes/206.189.44.223 && bash start_all.sh"
