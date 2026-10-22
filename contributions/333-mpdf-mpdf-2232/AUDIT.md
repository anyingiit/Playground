# AUDIT — mpdf/mpdf @ a981bb7 (development)

`python3 tools/audit_repo.py mpdf`: no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| composer.json scripts | `post-install-cmd` 只 `chmod('./tmp', 0777)`；本次 `--no-scripts` 安装，未执行 | 良性 |
| tests/bootstrap.php | 实例化一次 Mpdf 以定义常量 | 良性 |
| utils/ | 独立 CLI/浏览器脚本，未执行 | 未执行 |
| 依赖 | composer --prefer-source（git 源），phpunit 9.6 + yoast polyfills、setasign/fpdi 等知名包 | 良性 |
