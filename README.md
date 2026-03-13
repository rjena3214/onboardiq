# onboardiq
AI Employee Onboarding Platform — 4-Agent pipeline built with Claude API | Python + HTML

# 🚀 OnboardIQ — AI Employee Onboarding Platform

> **4-Agent AI Pipeline** that transforms employee onboarding using Claude API

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude-API-orange?logo=anthropic)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://rjena3214.github.io/onboardiq)

---

## 🎯 What is OnboardIQ?

OnboardIQ solves the biggest problem in employee onboarding:

- ❌ Employees quit in Week 1 because expectations don't match reality
- ❌ No structured training for the actual role
- ❌ Manager unavailable during critical first days
- ❌ Role responsibilities misrepresented during hiring

**OnboardIQ fixes this with a 4-Agent AI pipeline that runs in under 2 minutes.**

---

## 🤖 The 4-Agent Pipeline

```
Agent 1 → Role & Risk Analyser
Agent 2 → Training Designer  
Agent 3 → Assessment Engine
Agent 4 → HR Report Generator
```

| Agent | Job | Output |
|-------|-----|--------|
| **Agent 1** | Analyses role fit and flags onboarding risks | Risk report |
| **Agent 2** | Designs 5 custom training modules | Training plan |
| **Agent 3** | Generates 5 MCQ assessment questions | Interactive quiz |
| **Agent 4** | Creates official HR onboarding report | PDF-ready report |

---

## 📁 Project Structure

```
onboardiq/
├── index.html        ← Web version (runs in browser, no install)
├── onboardiq.py      ← Python version (runs in terminal)
└── README.md         ← You are here
```

---

## 🌐 Web Version (No Install Required)

**Live Demo:** [rjena3214.github.io/onboardiq](https://rjena3214.github.io/onboardiq)

1. Open the link
2. Enter your Anthropic API key
3. Fill in company and candidate details
4. Run the 4-agent pipeline
5. Download your onboarding report

---

## 🐍 Python Version — Full Setup Guide

### Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | 3.8+ | `python --version` |
| pip | Latest | `pip --version` |
| Anthropic API Key | Active | [console.anthropic.com](https://console.anthropic.com) |

---

### Step 1 — Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / Log in
3. Click **API Keys** → **Create Key**
4. Copy the key — it starts with `sk-ant-...`
5. **NEVER share this key or push it to GitHub**

---

### Step 2 — Install Python

**Windows:**
```
Download from python.org → Install → tick "Add to PATH"
```

**Mac:**
```bash
brew install python3
```

**Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

### Step 3 — Install Anthropic Library

```bash
pip install anthropic
```

Verify installation:
```bash
pip show anthropic
```

---

### Step 4 — Set Your API Key

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Mac / Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

> ⚠️ Set this every time you open a new terminal window.

---

### Step 5 — Clone the Repo

```bash
git clone https://github.com/rjena3214/onboardiq.git
cd onboardiq
```

---

### Step 6 — Run OnboardIQ

```bash
python onboardiq.py
```

---

## 📋 How to Use

When you run the script, it asks for details:

```
Company Name       : TechCorp India
Industry / Sector  : Software Development
Culture (optional) : Fast-paced startup
Candidate Name     : Priya Sharma
Job Role / Title   : Junior Python Developer
Department         : Engineering
Background         : 2 years Django, fresh grad
Responsibilities   : Build REST APIs, code review
```

**4 agents run automatically → saves report as:**
```
OnboardIQ_OIQ-XXXXXX_Priya_Sharma.txt
```

---

## 🔧 Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: anthropic` | `pip install anthropic` |
| `AuthenticationError` | Check API key is set correctly |
| `python not found` | Use `python3 onboardiq.py` |
| `pip not found` | Use `pip3 install anthropic` |

---

## 🗺️ Roadmap

| Stage | Status | Description |
|-------|--------|-------------|
| Stage 1 | ✅ Done | HTML + Python MVP |
| Stage 2 | 🔄 Day 30 | FastAPI + Supabase |
| Stage 3 | 📅 Day 55 | Stripe + SaaS launch |

---

## 👨‍💻 Author

**Ranjan Kumar Jena**
[![GitHub](https://img.shields.io/badge/GitHub-rjena3214-black?logo=github)](https://github.com/rjena3214)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/ranjan-jena-457637248)

> Built as part of the 75-Day AI Vibe Coder Challenge 🚀

---

## 📄 License

MIT License — free to use and modify.
