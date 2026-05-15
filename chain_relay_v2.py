"""
chain_relay.py - 高性能交易中继 (Persistent Console)
保持 FISCO-BCOS 控制台进程常驻，避免 JVM 冷启动开销
"""

# ============================================================================
# DEPRECATED 模块说明（2026-02 合规重构后）
# 本文件下方所有标注 "# DEPRECATED 2026-02" 的代码块均已停用，
# 原属早期 RWA / DEX 原型阶段功能（如 mint_token 调用 SolarRWA 合约）。
# 当前项目定位为"分布式光伏 MRV 可信数据底座"，仅保留 store_data
# （SolarDataStore 合约数据存证）相关功能。停用代码仅作历史留痕。
# ============================================================================
import json
import sys
import time
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty

CONSOLE_PATH = "/home/ubuntu/fisco/console"
CONTRACT_ADDR = "0x075d963d8567395f024da3edce3d63bd2f5f4be3"

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
            # 启动后台线程读取输出
            self.reader_thread = threading.Thread(target=self._read_output, daemon=True)
            self.reader_thread.start()
            
            # 等待启动完成 (读取到第一个提示符 '>')
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

    def _wait_for_prompt(self, timeout=10):
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

    def execute(self, cmd):
        """执行命令并返回结果"""
        with self.lock:
            if self.process.poll() is not None:
                print("⚠️ 控制台已死，正在重启...")
                self.start_console()

            # 清空旧输出
            while not self.output_queue.empty():
                try: self.output_queue.get_nowait()
                except Empty: break

            # 发送空行唤醒 Console（清除残留 prompt）
            self.process.stdin.write("\n")
            self.process.stdin.flush()
            time.sleep(0.3)
            while not self.output_queue.empty():
                try: self.output_queue.get_nowait()
                except Empty: break

            # 发送命令
            full_cmd = cmd + "\n"
            self.process.stdin.write(full_cmd)
            self.process.stdin.flush()

            # 读取结果
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
                contract_addr = body.get("contractAddr", CONTRACT_ADDR)
                p = body.get("pvPower", 0)
                v = body.get("pvVoltage", 0)
                s = body.get("battSOC", 0)
                bv = body.get("battVoltage", 0)
                e = body.get("totalEnergy", 0)
                sig = body.get("signature", "no_sig")
                
                cmd = f'call SolarDataStore {contract_addr} storeData {p} {v} {s} {bv} {e} "{sig}"'
                raw_output = console.execute(cmd)
                
                success = "transaction executed successfully" in raw_output
                if "receipt timeout" in raw_output:
                    success = False

                tx_hash = ""
                for line in raw_output.split('\n'):
                    if 'transaction hash' in line:
                        tx_hash = line.split(':')[-1].strip()
                
                resp = {"success": success, "tx_hash": tx_hash, "output": raw_output[-300:]}

            # DEPRECATED 2026-02: 合规重构，已停用。原属早期 RWA / DEX 模块，不再对外提供。
            # elif action == "mint_token":
            #     contract_addr = body.get("contractAddr", "")
            #     device_id = body.get("deviceId", "NODE_001")
            #     total_energy = body.get("totalEnergy", 0)
            #
            #     if not contract_addr:
            #         resp = {"success": False, "error": "Missing contractAddr for SolarRWA"}
            #     else:
            #         cmd = f'call SolarRWA {contract_addr} storeDeviceData "{device_id}" {total_energy}'
            #         raw_output = console.execute(cmd)
            #
            #         success = "transaction executed successfully" in raw_output
            #         if "receipt timeout" in raw_output:
            #             success = False
            #
            #         tx_hash = ""
            #         for line in raw_output.split('\n'):
            #             if 'transaction hash' in line:
            #                 tx_hash = line.split(':')[-1].strip()
            #
            #         resp = {"success": success, "tx_hash": tx_hash, "output": raw_output[-300:]}
            
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
        pass  # 禁用 HTTP 日志打印以免刷屏

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
    server = HTTPServer(('127.0.0.1', port), RelayHandler)
    print(f"🚀 高性能中继已就绪，端口: {port}")
    server.serve_forever()
