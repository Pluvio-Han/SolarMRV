"""
chain_relay.py - 高性能交易中继 (Persistent Console)
保持 FISCO-BCOS 控制台进程常驻，避免 JVM 冷启动开销

v2 优化:
  - 发送命令前先发空行唤醒 Console，解决首次请求空响应
  - prompt 等待超时从 10s 提升到 30s
  - 检测 receipt timeout 并正确返回失败
  - 增强 success 判断条件
"""
import json
import sys
import time
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty

CONSOLE_PATH = "/home/ubuntu/fisco/console"
CONTRACT_ADDR = "0xf5a9bb3817e8a2f7de1adfbebff27cb540a7d5e2"

class PersistentConsole:
    def __init__(self):
        self.process = None
        self.lock = threading.Lock()
        self.output_queue = Queue()
        self.start_console()

    def start_console(self):
        try:
            print("🚀 正在启动 FISCO-BCOS 控制台...")
            self.process = subprocess.Popen(
                ["bash", "start.sh"],
                cwd=CONSOLE_PATH,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            self.reader_thread = threading.Thread(target=self._read_output, daemon=True)
            self.reader_thread.start()
            self._wait_for_prompt(timeout=30)
            print("✅ 控制台启动成功，随时待命!")
        except Exception as e:
            print(f"❌ 启动失败: {e}")

    def _read_output(self):
        """后台读取 stdout 并放入队列"""
        while True:
            if self.process.poll() is not None:
                break
            char = self.process.stdout.read(1)
            if char:
                self.output_queue.put(char)

    def _wait_for_prompt(self, timeout=30):
        """读取直到出现 prompt >"""
        buffer = ""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                char = self.output_queue.get(timeout=0.1)
                buffer += char
                if buffer.strip().endswith(">"):
                    return buffer
            except Empty:
                continue
        return buffer

    def _drain_queue(self):
        """清空输出队列"""
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except Empty:
                break

    def execute(self, cmd):
        """执行命令并返回结果"""
        with self.lock:
            if self.process.poll() is not None:
                print("⚠️ 控制台已死，正在重启...")
                self.start_console()

            # 清空旧输出
            self._drain_queue()

            # 发送空行唤醒 Console (清除空闲残留 prompt)
            self.process.stdin.write("\n")
            self.process.stdin.flush()
            time.sleep(0.3)
            self._drain_queue()

            # 发送命令
            self.process.stdin.write(cmd + "\n")
            self.process.stdin.flush()

            # 读取结果 (超时 30 秒)
            output = self._wait_for_prompt(timeout=30)
            return output

console = PersistentConsole()

class RelayHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}
            
            action = body.get("action", "")
            
            if action == "store_data":
                p = body.get("pvPower", 0)
                v = body.get("pvVoltage", 0)
                s = body.get("battSOC", 0)
                bv = body.get("battVoltage", 0)
                e = body.get("totalEnergy", 0)
                sig = body.get("signature", "no_sig")
                
                cmd = f'call SolarDataStore {CONTRACT_ADDR} storeData {p} {v} {s} {bv} {e} "{sig}"'
                raw_output = console.execute(cmd)
                
                # 检测 receipt timeout (明确返回失败)
                if "receipt timeout" in raw_output.lower():
                    resp = {"success": False, "error": "transaction_receipt_timeout", "output": raw_output[-200:]}
                else:
                    success = ("Return message: Success" in raw_output 
                              or "transaction executed successfully" in raw_output)
                    tx_hash = ""
                    for line in raw_output.split('\n'):
                        if 'transaction hash' in line.lower():
                            tx_hash = line.split(':')[-1].strip()
                    
                    resp = {"success": success, "tx_hash": tx_hash, "output": raw_output[-200:]}
            
            elif action == "ping":
                resp = {"success": True, "status": "active"}
            
            else:
                resp = {"success": False, "error": f"unknown action: {action}"}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            
        except Exception as ex:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(ex)}).encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
    server = HTTPServer(('127.0.0.1', port), RelayHandler)
    print(f"🚀 高性能中继已就绪，端口: {port}")
    server.serve_forever()
