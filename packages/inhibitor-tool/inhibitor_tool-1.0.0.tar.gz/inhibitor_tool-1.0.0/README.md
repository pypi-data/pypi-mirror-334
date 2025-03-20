```markdown
# inhibitor_tool

## Introduction
`inhibitor_tool` is a Python CLI tool for adding items to an inhibition list via an API, with authentication handled via `auth_token`.

## Installation
```bash
pip install inhibitor_tool
```

## Usage
1. **Configure `auth_token` and load environment variables**:
    ```bash
    echo 'export INHIBITOR_USERNAME="your_username"' >> ~/.auth_token
    echo 'export INHIBITOR_PASSWORD="your_password"' >> ~/.auth_token
    echo 'export AUTH_API="https://auth.example.com/token"' >> ~/.auth_token
    echo 'export INHIBITOR_API="https://inhibitor.example.com/add"' >> ~/.auth_token
    source ~/.auth_token
    ```

2. **Inhibit an item**:
    ```bash
    inhibitor-tool "Malicious IP: 192.168.1.1"
    ```
    The default TTL is 3 hours.

3. **Specify a custom TTL**:
    ```bash
    inhibitor-tool "Malicious IP: 192.168.1.1" --ttl 3600
    ```
    Here, `ttl=3600` means the item will be inhibited for 1 hour.

## Open-Source Information
- **Author**: mmwei3
- **Email**: mmwei3@iflytek.com
- **Date**: 2025-03-16
- **License**: MIT License
```

---

## **8. LICENSE (MIT 开源协议)**
```text
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## **9. `requirements.txt` (依赖)**
```text
requests
```

---

## **10. 打包与安装**
### **打包**
```bash
python setup.py sdist bdist_wheel
```
### **安装**
```bash
pip install dist/inhibitor_tool-1.0.0-py3-none-any.whl
```
### **卸载**
```bash
pip uninstall inhibitor_tool
```

---

这个项目提供了一个**完全可配置**的 CLI 工具，用于通过 API 执行抑制操作（Inhibition），支持鉴权和 pip 安装。