from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('1.12.43.152', username='evanhan', password='Hanrui0402')
stdin, stdout, stderr = ssh.exec_command('cat ~/fisco/chain_relay_v2.py')
print("--- SCRIPT ---")
print(stdout.read().decode())
stdin, stdout, stderr = ssh.exec_command('tail -n 20 ~/fisco/relay.log')
print("--- LOG ---")
print(stdout.read().decode())
ssh.close()
