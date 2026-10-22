# AUDIT: seladb/PcapPlusPlus（dev @ 4c3f7e5）

`python3 tools/audit_repo.py /home/user/work/ppp` 结果与人工复核：

| 命中 | 复核 | 结论 |
|---|---|---|
| `.pre-commit-config.yaml` | 标准 pre-commit 钩子（clang-format、cppcheck 等），本次未安装 pre-commit | 良性 |
| `Tests/ExamplesTest/conftest.py` | pytest 示例测试的参数解析，本次未运行 | 良性 |
| 二进制 `Tests/Pcap++Test/rpcapd/*.dll`、`rpcapd.exe` | Windows rpcapd 测试工具，Linux 构建不涉及 | 良性 |
| `Examples/PcapPlusPlus-benchmark/CMakeLists.txt` FetchContent google/benchmark | 只在构建 benchmark 示例时；本次 `-DPCAPPP_BUILD_EXAMPLES=OFF` | 良性 |
| 长十六进制串（X509Tests、CryptoKeyTests） | 证书/密钥测试夹具 | 良性 |
| `ci/install_windivert.ps1` 下载 WinDivert | Windows CI 脚本，不运行 | 良性 |
| 顶层 CMakeLists / Packet++ CMakeLists | 无下载、无 execute_process 网络操作 | 良性 |

结论：未发现恶意代码。构建参数：`-DPCAPPP_BUILD_PCAPPP=OFF -DPCAPPP_USE_PCAP=OFF -DPCAPPP_BUILD_EXAMPLES=OFF`（容器无 libpcap，Packet++Test 不需要）。
