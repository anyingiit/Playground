# seladb/PcapPlusPlus#2278: QUIC v1 layer serialization

| 项 | 值 |
|---|---|
| Issue | https://github.com/seladb/PcapPlusPlus/issues/2278（跟踪 issue，按层分 PR） |
| Tier | 自由（与 301 同仓库，另一个层） |
| Labels | enhancement, good first issue |
| Status | ✅ ready（独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 20:40 UTC：issue 清单 QuicLayer 标“no PR listed”；`is:pr serialization` 无 QUIC；无人在 issue 认领 |
| AI 政策 | 同 301（AGENTS.md 欢迎 AI agent，无限制） |
| Base | `dev` @ 4c3f7e5 |
| DCO / CLA / changelog | 都不需要 |
| 需先认领 | 否 |
| 与 301 的关系 | 改不同文件，互不冲突，可以任意顺序提交；建议先交 301，等维护者对风格有反馈再交 302 |

## 改动
- `Packet++/header/QuicLayer.h`：7 个类各自的 `SerializedFields`（按继承链延续 ID，每层都带 `MaxID`，照 GreLayer），`protected: serializeLayer`。
- `Packet++/src/QuicLayer.cpp`：`toString()` 里的类型名 switch 提成静态函数 `quicPacketTypeToString`（输出不变），各层 `serializeLayer` 先调父类再写自己的字段。Establishment 的 Length 字段命名为 `payloadLength`，避免与公共字段 `length` 重名。
- `Tests/Packet++Test/Tests/QuicTests.cpp`：6 种包型的 JSON 断言 + 9 个类的 `all()` 数量/ID 检查。

## 验证
- 构建同 301（`-DPCAPPP_BUILD_PCAPPP=OFF -DPCAPPP_USE_PCAP=OFF -DPCAPPP_BUILD_EXAMPLES=OFF`）。
- 红：只回退 QuicLayer.h/.cpp → `Packet++Test -t quic` 1 passed / 1 failed（QuicV1ParsingTest）。
- 绿：2/2；全量 Packet++Test 280/280（OUILookup 需把数据文件放到运行目录，同 301）。
- ASan Debug 构建：`-t quic` 通过无报错；另外临时在 QuicV1MalformedPacketsTest 的 17 个畸形包后都调用序列化，ASan 也无报错（临时改动已撤销）。
- clang-format 19.1.6 已格式化。未跑 Pcap++Test、示例、cppcheck。

## 如何提交
```
tools/submit_pr.sh contributions/302-seladb-PcapPlusPlus-2278-quic seladb/PcapPlusPlus dev quic-serialization contributions/302-seladb-PcapPlusPlus-2278-quic/pr_title.txt contributions/302-seladb-PcapPlusPlus-2278-quic/pr_body.md
```

## 独立复核

结论：**PASS**（独立 agent，dev@4c3f7e5 新克隆 + ASan Debug 构建）。

- `git am` 干净；`-t quic` 2/2、全套 280/280；源改动回退后 `QuicV1ParsingTest` 失败（红）。
- clang-format 19.1.6 `--dry-run --Werror` 干净；toString() 输出不变。
- 手工构造的畸形包（零长 CID、CID/Token/Length 越界、截断 varint、Retry 不足 16 字节等）+ 30 万随机输入经 JsonSerializer，ASan 无报错。
- 上游：#2278 中 QUIC 无 PR、无人认领；无竞争 PR。
- 可选建议 1（叶子结构缺 `MaxID`，与 GRE 不一致）已采纳：Initial/Retry/VersionNegotiation/OneRtt 加 `MaxID`，测试加 `static_assert`；重跑 `-t quic` 2/2。其余两条（fixedBit 用整数、payloadLength 超大值转字符串）为风格/框架行为，未改。
