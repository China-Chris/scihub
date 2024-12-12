import os
import base58
import ed25519
import threading
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tqdm import tqdm

# 创建一个全局的计数器和锁
total_attempts = 0
total_attempts_lock = threading.Lock()
progress_bars = {}

# 彩色进度条的颜色列表
COLORS = [
    '\033[92m',  # 绿色
    '\033[94m',  # 蓝色
    '\033[95m',  # 紫色
    '\033[96m',  # 青色
    '\033[93m',  # 黄色
    '\033[91m',  # 红色
    '\033[97m',  # 白色
    '\033[90m',  # 灰色
]

# 自定义进度条格式，添加颜色支持
BAR_FORMAT = '{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'

def ensure_files_exist():
    if not os.path.exists('scihub_addresses.txt'):
        with open('scihub_addresses.txt', 'w') as f:
            f.write(f"Solana Addresses Log\nCreated: {datetime.now()}\n{'='*50}\n")

def is_scihub_address(address):
    try:
        decoded = base58.b58decode(address)
        text = decoded.decode('utf-8', errors='ignore').lower()
        return text.startswith('scihub')
    except:
        return False

def save_to_file(filename, address, private_key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as f:
        f.write(f"Time: {timestamp}\nAddress: {address}\nPrivate Key: {private_key}\n{'='*50}\n")

def generate_and_check_wallet():
    global total_attempts
    success_count = 0
    fail_count = 0
    thread_id = threading.current_thread().name
    thread_num = int(thread_id.split('-')[-1]) - 1
    start_time = time.time()
    
    # 为每个线程创建一个彩色进度条
    color = COLORS[thread_num % len(COLORS)]
    pbar = tqdm(total=1_000_000, 
                desc=f"{color}线程 {thread_id}\033[0m",  # 添加颜色到描述
                position=thread_num,
                bar_format=BAR_FORMAT,
                colour=color.replace('\033', ''),  # tqdm的颜色格式稍有不同
                leave=True)
    progress_bars[thread_id] = pbar
    
    while True:
        try:
            # 生成密钥对
            signing_key, verifying_key = ed25519.create_keypair()
            
            # 获取公钥和私钥
            private_key_bytes = signing_key.to_bytes()
            public_key_bytes = verifying_key.to_bytes()
            
            # 转换为 base58 格式
            private_key = base58.b58encode(private_key_bytes).decode('ascii')
            public_key = base58.b58encode(public_key_bytes).decode('ascii')
            
            # 更新进度条
            with total_attempts_lock:
                total_attempts += 1
                pbar.update(1)
                if pbar.n >= pbar.total:  # 如果达到目标，增加目标值
                    pbar.total *= 2
                pbar.set_postfix({
                    '总尝试': f'{total_attempts:,d}',
                    '速度': f'{pbar.n/(time.time()-start_time):.1f}/s'
                })
            
            # 检查是否满足条件并保存到相应文件
            if is_scihub_address(public_key):
                save_to_file('scihub_addresses.txt', public_key, private_key)
                success_count += 1
                print(f"\n{color}[线程 {thread_id}] ✨ 找到第 {success_count} 个符合条件的地址！✨\n地址: {public_key}\033[0m\n")
            else:
                fail_count += 1
                
        except Exception as e:
            continue

def main():
    ensure_files_exist()
    
    # 固定使用8个线程
    num_threads = 8
    print(f"\n启动 {num_threads} 个线程进行地址生成...\n")
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
            futures.append(executor.submit(generate_and_check_wallet))
        
        try:
            # 等待所有线程完成
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            print("\n正在优雅地停止所有线程...")
            # 关闭所有进度条
            for pbar in progress_bars.values():
                pbar.close()
            executor.shutdown(wait=False)
            print("\n程序已停止！")
            print("满足条件的地址已保存在 scihub_addresses.txt 文件中")

if __name__ == "__main__":
    print("开始寻找以 'scihub' 开头的地址...")
    print("按 Ctrl+C 可以停止程序")
    print("满足条件的地址将保存在 scihub_addresses.txt 文件中")
    main()
