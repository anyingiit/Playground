# AUDIT — OpenCHAMI/ochami @ f187792

- This package uses the same repository, base commit and audit as 426. See `contributions/426-OpenCHAMI-ochami-188/AUDIT.md`.
- The patch only changes `man/ochami-smd.1.sc`.
- Verification ran `make man`, which runs scdoc only.
- scdoc 1.11 was installed with apt.
- To reproduce the iface add bugs mentioned in the PR body, I ran a locally built binary against an unreachable 127.0.0.1:1. No external services were contacted.
