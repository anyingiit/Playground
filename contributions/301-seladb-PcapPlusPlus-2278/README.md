# seladb/PcapPlusPlus#2278: GTPv1 / GTPv2 layer serialization

| 项 | 值 |
|---|---|
| Issue | https://github.com/seladb/PcapPlusPlus/issues/2278（跟踪 issue，按层分 PR） |
| Tier | 自由（PcapPlusPlus，~3k★，近一个月合并了十几个序列化 PR） |
| Labels | enhancement, good first issue |
| Status | ✅ ready（独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 20:10 UTC：issue 清单里 GtpLayer (v1/v2) 标“no PR listed”；`is:pr serialization` 25 条与 `is:pr gtp` 9 条里都没有 GTP 序列化 PR。issue 只有 seladb、egecetin 两条评论，无人认领 GTP。注意：开着的 #2323（GTPv1 addExtension UAF 修复）也改 GtpLayer.cpp，但在不同函数，冲突概率低 |
| AI 政策 | 仓库有 AGENTS.md（写给 AI agent 的开发指南），无限制；CONTRIBUTING 无 AI 条款 |
| Base | `dev`（CONTRIBUTING 要求 PR 指向 dev）@ 4c3f7e5 |
| DCO / CLA / changelog | 都不需要 |
| 需先认领 | 否（其他贡献者都是直接开 PR，PR 正文写 “Part of #2278”） |

## 问题理解
#2259 加了序列化基础设施，#2278 跟踪把它推广到每个 Packet++ 层：每层要有 `SerializedFields`（含 `all()`）、`serializeLayer()` 覆盖、Doxygen 注释、测试（检查输出和 `all()`）。GTP v1/v2 还没人做。

## 改动
- `Packet++/header/GtpLayer.h`：`GtpV1Layer::SerializedFields`（9 个字段 + 数组项 `Extension`）和 `GtpV2Layer::SerializedFields`（8 个字段 + 数组项 `InformationElement`），`protected: serializeLayer`。
- `Packet++/src/GtpLayer.cpp`：描述符定义（ID 从 `MaxID + 1` 起，数组项 ID 0，照 RadiusLayer）和两个 `serializeLayer`。可选字段（v1 的 sequenceNumber/npduNumber/extensions，v2 的 teid/messagePriority）不存在时省略，照 NTP 的做法；v2 messageType 写头里的原始值，未知类型不会变成 0。
- `Packet++/src/GtpLayer.cpp` 另加私有 `getIEDataLen()`：GTPv2 的 4 个 IE 访问函数原来用 `m_Data + getHeaderLen() - basePtr`，messageLength 小于固定头时会下溢成巨大 size_t 越界读（复核发现，ASan 实测 heap-buffer-overflow）；序列化会必经此路径，所以一起修。
- `Tests/Packet++Test/Tests/GtpTests.cpp`：`serializeToJson` 小工具；两个 parsing 测试里全部 10 个夹具的 JSON 断言 + 新建 GTPv1 层（带 N-PDU）断言 + 两个 `all()` 检查 + 越界回归测试（两段短 messageLength 头）。

## 验证
- 构建：`cmake -S . -B build -DPCAPPP_BUILD_PCAPPP=OFF -DPCAPPP_USE_PCAP=OFF -DPCAPPP_BUILD_EXAMPLES=OFF && cmake --build build -j4`（容器无 libpcap）。
- 红：只回退 GtpLayer.h/.cpp（测试照样能编译，因为 `GtpV1Layer::SerializedFields` 会继承到 `Layer::SerializedFields`）→ `Packet++Test -t gtp` 4 passed / 2 failed（两个 parsing 测试）。
- 绿：6/6 passed。
- 全量 `Packet++Test`：280/280 passed（OUILookup 需要把 `3rdParty/OUIDataset/PCPP_OUIDataset.json` 放到运行目录，与本改动无关，不放时 base 也失败）。
- 越界回归：ASan Debug 构建（`-fsanitize=address`）下，去掉 clamp → `heap-buffer-overflow READ of size 2` in `GtpV2InformationElement::getDataSize`；加上 → `-t gtp` 6/6 通过，无 ASan 错误（LeakSanitizer 只报 MemPlumber 自身的 backtrace 记录，与改动无关，用 `ASAN_OPTIONS=detect_leaks=0` 跑）。
- clang-format 19.1.6（项目指定版本，pip 装）格式化过。
- 未跑：Pcap++Test、示例、cppcheck、MemPlumber 内存检查（本构建打印 “Skipping memory leak check”）。新代码不分配堆内存。

## 需要提交者注意
- PR 目标分支是 **dev**。
- 仓库无 PR 模板。

## 如何提交
```
tools/submit_pr.sh contributions/301-seladb-PcapPlusPlus-2278 seladb/PcapPlusPlus dev gtp-serialization contributions/301-seladb-PcapPlusPlus-2278/pr_title.txt contributions/301-seladb-PcapPlusPlus-2278/pr_body.md
```

## 独立复核
- 第 1 轮（2026-10-22 20:30 UTC，独立 agent）：**FAIL**——①GTPv2 messageLength 小于固定头时序列化越界读（旧 getter 缺陷，但序列化让它必经）；②PR 正文“every existing GTP fixture”说法不实。其余（apply、红→绿、280/280、clang-format、ID/命名/格式惯例、上游无竞争）均通过。
- 已修：按建议加 `getIEDataLen()` clamp + 回归测试（ASan 红→绿已验证）；补齐 parsing 测试里另外 3 个夹具的 JSON 断言；PR 正文改为准确描述并说明这处修复。

### 复审（第 2 轮）：PASS

- dev@4c3f7e5 新克隆 + ASan：`-t gtp` 6/6、全套 280/280；源改动回退后两个解析测试失败（红）。
- 只回退 clamp：ASan 在新回归测试中报 `GtpV2InformationElement::getDataSize()` heap-buffer-overflow，加回后通过。
- clang-format 干净；ID 连续无空洞、可选字段缺省省略，与 Ntp/Radius 一致；30 万随机输入 ASan 无报错。
- 与上游开放 PR #2323（GTPv1 addExtension UAF）不冲突（`git apply --check` 通过）。PR 正文数字与声明均核实无误。
