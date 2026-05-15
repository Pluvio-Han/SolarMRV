#!/bin/bash
echo "Gwen:"
ssh -o StrictHostKeyChecking=no ubuntu@1.12.43.152 "cat ~/fisco/nodes/1.12.43.152/node0/conf/node.nodeid && cat ~/fisco/nodes/1.12.43.152/node1/conf/node.nodeid"
echo "Miles:"
ssh -o StrictHostKeyChecking=no ubuntu@106.53.76.27 "cat ~/fisco/nodes/106.53.76.27/node0/conf/node.nodeid && cat ~/fisco/nodes/106.53.76.27/node1/conf/node.nodeid"
echo "Peter:"
ssh -o StrictHostKeyChecking=no root@206.189.44.223 "cat ~/fisco/nodes/206.189.44.223/node0/conf/node.nodeid && cat ~/fisco/nodes/206.189.44.223/node1/conf/node.nodeid"
