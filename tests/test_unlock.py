from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pexpect
import sys

child = pexpect.spawn("ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@206.189.44.223", encoding='utf-8')
child.logfile_read = sys.stdout

try:
    child.expect('Current password:')
    child.sendline('71f5c672065c09e47fd5ba41a4')
    
    child.expect('New password:')
    child.sendline('Harry2006323')
    
    child.expect('Retype new password:')
    child.sendline('Harry2006323')
    
    child.expect('.*#') # wait for root prompt
    child.sendline('cd ~/fisco/nodes/206.189.44.223 && bash start_all.sh')
    
    child.expect('.*#')
    print("FINISHED STARTING NODES")
    child.sendline('exit')
    child.close()
except pexpect.TIMEOUT:
    print("Timeout occurred")
    print(child.before)
except Exception as e:
    print(e)
finally:
    if child.isalive():
        child.close()
