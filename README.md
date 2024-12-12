# Solana 地址生成器

一个高性能的 Solana 钱包地址生成器，用于生成特定前缀的地址并检查其 SOL 余额。

## 功能特点

- 多线程并行生成 Solana 地址
- 支持检查地址是否以 "scihub" 开头
- 实时检查地址 SOL 余额
- 彩色进度条显示生成进度
- 自动保存符合条件的地址

## 性能指标

- 单线程生成速度：约 165 地址/秒
- 8线程并行：约 1,320 地址/秒
- 24小时理论生成量：约 1.14亿个地址

## 依赖项

```
solana
base58
ed25519
tqdm
```

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/TokenTracker.git
cd TokenTracker
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

运行程序：
```bash
python sol_address_generator.py
```

## 输出文件

- `scihub_addresses.txt`: 保存以 "scihub" 开头的地址
- `other_addresses.txt`: 保存不以 "scihub" 开头的地址

## 文件格式

每个找到的地址都会记录以下信息：
```
Time: [生成时间]
Address: [钱包地址]
Private Key: [私钥]
SOL Balance: [SOL余额]
==================================================
```

## 注意事项

- 程序使用 Solana 主网 RPC 节点查询余额
- 可以通过 Ctrl+C 随时停止程序
- 私钥信息请妥善保管，不要泄露

## 性能优化建议

1. 增加线程数可提高生成速度
2. 使用本地 Solana RPC 节点可提高查询速度
3. 使用更强大的 CPU 可提升整体性能

## 许可证

MIT License
