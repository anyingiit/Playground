# Smaug6739/Alexandrie#781 — Backend should not abort when S3 storage does not support PutBucketPolicy

| | |
|---|---|
| Issue | https://github.com/Smaug6739/Alexandrie/issues/781 |
| Tier | 自由 |
| Labels | backend, bug, good first issue |
| Status | 🚧 in progress — audit done, implementing |
| Duplicate-PR check | no open PR (search "bucket policy" in repo, 2026-09-24) |

Notes: root cause backend/app/minio.go setupPublicBucket -> os.Exit(1) on SetBucketPolicy error. No AI policy found in repo.
