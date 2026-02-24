#!/bin/bash
echo "Fixing Gwen..."
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "sed -i '/node.4=206.189.44.223:30300/a\    node.5=206.189.44.223:30301' ~/fisco/nodes/1.12.43.152/node0/config.ini && sed -i '/node.4=206.189.44.223:30300/a\    node.5=206.189.44.223:30301' ~/fisco/nodes/1.12.43.152/node1/config.ini"

echo "Fixing Miles..."
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "sed -i '/node.4=206.189.44.223:30300/a\    node.5=206.189.44.223:30301' ~/fisco/nodes/106.53.76.27/node0/config.ini && sed -i '/node.4=206.189.44.223:30300/a\    node.5=206.189.44.223:30301' ~/fisco/nodes/106.53.76.27/node1/config.ini"
echo "DONE"
