# Security Policy

## 🛡️ Responsible Disclosure & Usage

**WebFox** is a powerful reconnaissance framework intended for **authorized security testing, red teaming, and educational purposes only**.

By downloading, installing, or using this software, you agree to the following:
1.  **Authorization:** You will only scan targets you own or have explicit, written permission to test.
2.  **Compliance:** You will adhere to all local, state, and international laws regarding cybersecurity and network access (e.g., CFAA in the US, GDPR in Europe).
3.  **Liability:** The developers and contributors are **not responsible** for any misuse, damage, or legal consequences resulting from the use of this tool.

---

## 📦 Supported Versions

We only provide security updates and patches for the latest "Ultimate Edition" release.

| Version | Supported          | Status |
| :------ | :----------------- | :----- |
| v3.0+  | :white_check_mark: | **Active Maintenance** |
| v2.x    | :x:                | End of Life |
| < v2.0  | :x:                | Deprecated |

---

## 🐛 Reporting a Vulnerability

If you discover a security vulnerability **within the WebFox codebase itself** (e.g., unsafe file handling, dependency risks, or code injection flaws), please report it to us responsibly.

**DO NOT** open a public GitHub issue for sensitive security vulnerabilities.

### Reporting Process
1.  **Email:** Send details to `omp48095@gmail.com`.
2.  **Details:** Please include:
    * Step-by-step instructions to reproduce the issue.
    * The specific module or file involved (e.g., `core/basic/screenshot.py`).
    * Potential impact of the vulnerability.
3.  **Response:** We aim to acknowledge reports within **48 hours** and will provide an estimated timeline for a fix.

---

## ⚠️ Known Risks & Best Practices

Since WebFox performs active network scanning and interaction:
* **Root Privileges:** Some installation scripts require `sudo`. Always audit the code (specifically `install.sh`) before running it with elevated privileges.
* **WAF Blocking:** Aggressive scanning (high thread counts) may trigger IP bans from Cloudflare or AWS WAFs. Use the `-threads` argument responsibly.
* **False Positives:** Automated scanners may occasionally misidentify services. Always manually verify critical findings.

---

*Policy last updated: December 2025*

