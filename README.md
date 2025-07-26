# 🚗 capl-bridge

A Python-based bridge to integrate and automate **CAPL scripts** within **Vector CANalyzer** using COM automation.

This tool allows users to:
- Automatically compile and trigger CAPL functions from Python
- Send and read CAN bus signals
- Bridge Python test automation with Vector CANalyzer setups

---

## 📦 Features

- 🧠 CAPL function parsing and execution
- 🔁 CAN bus signal read/write support
- 🛠️ Starts/stops CANalyzer measurement from script
- 🪟 Built for Windows (uses `pywin32`)

---

## 🔧 Requirements

- Windows OS with **Vector CANalyzer** installed
- Python 3.6+
- CAPL script file (optional, but recommended)
- CANalyzer configuration file (`.cfg`)

Install Python dependencies:

```bash
pip install -r requirements.txt
