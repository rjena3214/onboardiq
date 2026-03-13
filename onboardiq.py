"""
OnboardIQ — AI Employee Onboarding Pipeline
4-Agent System built with Claude API
Author: Ranjan Kumar Jena (github.com/rjena3214)
"""

import anthropic
import json
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────
# Set your API key as environment variable:
# Windows:  set ANTHROPIC_API_KEY=sk-ant-...
# Linux/Mac: export ANTHROPIC_API_KEY=sk-ant-...
# Or paste directly below (never push to GitHub with real key)

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")
MODEL   = "claude-sonnet-4-20250514"

client = anthropic.Anthropic(api_key=API_KEY)

# ── HELPERS ─────────────────────────────────────────

def call_agent(agent_name: str, prompt: str) -> str:
    """Call Claude API and return response text."""
    print(f"\n  ⚡ Running {agent_name}...")
    message = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    result = message.content[0].text
    print(f"  ✓  {agent_name} complete.")
    return result


def separator(title: str):
    print("\n" + "═" * 55)
    print(f"  {title}")
    print("═" * 55)


def get_input(prompt: str, required: bool = True) -> str:
    while True:
        val = input(prompt).strip()
        if val or not required:
            return val
        print("  ⚠  This field is required. Please enter a value.")


# ── AGENT PROMPTS ────────────────────────────────────

def agent1_prompt(data: dict) -> str:
    return f"""You are an expert HR onboarding specialist.

Company: {data['company']} | Industry: {data['industry']}
Culture: {data.get('culture') or 'Not specified'}
New Hire: {data['name']} | Role: {data['role']} | Department: {data.get('dept') or 'Not specified'}
Background: {data.get('background') or 'Not provided'}
Responsibilities: {data.get('responsibilities') or 'Not provided'}

Provide a thorough Role & Risk Analysis covering:

ROLE FIT ASSESSMENT
[Assess how well the candidate background matches the role]

ONBOARDING RISK FLAGS
[List 3-5 specific risks that could cause this employee to quit in week 1]

CRITICAL SUCCESS FACTORS
[What must happen in the first week for this person to succeed?]

MANAGER ACTION ITEMS
[5 specific things the manager must do before/during day 1]

MISREPRESENTATION CHECK
[Flag any areas where expectations may not match reality]

Be direct and specific. No generic HR language."""


def agent2_prompt(data: dict, analysis: str) -> str:
    return f"""You are a corporate training designer.

Company: {data['company']} | Role: {data['role']} | Department: {data.get('dept') or 'Not specified'}
Candidate Background: {data.get('background') or 'Not provided'}
Responsibilities: {data.get('responsibilities') or 'Not provided'}
Risk Analysis Summary: {analysis[:400]}

Design a structured 5-module onboarding training plan.

For each module use this exact format:
MODULE_1_TITLE: [title]
MODULE_1_DURATION: [e.g. 2 hours]
MODULE_1_CONTENT:
[Detailed training content — at least 100 words of actual training material]

MODULE_2_TITLE: [title]
MODULE_2_DURATION: [duration]
MODULE_2_CONTENT:
[Detailed content]

...continue for all 5 modules

Make content specific to the role. Not generic."""


def agent3_prompt(data: dict) -> str:
    return f"""You are an assessment designer for corporate onboarding.

Role: {data['role']} at {data['company']}
Department: {data.get('dept') or 'General'}
Responsibilities: {data.get('responsibilities') or 'Standard role responsibilities'}

Generate exactly 5 multiple choice questions to assess role readiness.

Return ONLY valid JSON array. No other text. No markdown. Format:
[{{"q":"Question?","options":["A. Option","B. Option","C. Option","D. Option"],"answer":0}}]

answer = index (0-3) of correct option.
Make questions specific to the role."""


def agent4_prompt(data: dict, analysis: str, case_id: str) -> str:
    return f"""You are an HR documentation specialist.

CASE: {case_id}
DATE: {datetime.now().strftime('%d %b %Y')}
COMPANY: {data['company']} ({data['industry']})
EMPLOYEE: {data['name']}
ROLE: {data['role']} | DEPARTMENT: {data.get('dept') or 'Not specified'}

Analysis Summary: {analysis[:500]}

Write a formal onboarding report covering:

EXECUTIVE SUMMARY
[3-4 sentences summarising onboarding readiness and key findings]

ONBOARDING STATUS
[Current status, timeline, what is complete vs pending]

KEY RECOMMENDATIONS FOR HR
[5 specific recommendations to ensure this employee succeeds]

30-DAY CHECK-IN AGENDA
[What HR should review at 30-day mark — specific questions and metrics]

90-DAY SUCCESS METRICS
[How to measure if this onboarding was successful at 90 days]

RISK MITIGATION PLAN
[Specific steps to address the risks identified in analysis]

Write formally but clearly. This is an official HR document."""


# ── ASSESSMENT ───────────────────────────────────────

def run_assessment(questions: list) -> int:
    separator("ASSESSMENT — Answer the Questions")
    print("  Type A, B, C, or D for each question.\n")

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"  Q{i}. {q['q']}")
        for opt in q['options']:
            print(f"       {opt}")
        
        while True:
            ans = input(f"\n  Your answer: ").strip().upper()
            if ans in ['A', 'B', 'C', 'D']:
                break
            print("  Please enter A, B, C or D.")
        
        chosen = ord(ans) - ord('A')
        correct = q['answer']
        
        if chosen == correct:
            print("  ✅ Correct!\n")
            score += 1
        else:
            print(f"  ❌ Incorrect. Correct answer: {q['options'][correct]}\n")
    
    return score


# ── SAVE REPORT ──────────────────────────────────────

def save_report(data: dict, results: dict, case_id: str):
    filename = f"OnboardIQ_{case_id}_{data['name'].replace(' ', '_')}.txt"
    
    content = f"""
ONBOARDIQ — OFFICIAL ONBOARDING REPORT
{"=" * 55}
Case ID    : {case_id}
Date       : {datetime.now().strftime('%d %b %Y %H:%M')}
Employee   : {data['name']}
Role       : {data['role']}
Department : {data.get('dept') or '—'}
Company    : {data['company']} ({data['industry']})
{"=" * 55}

━━ AGENT 1: ROLE & RISK ANALYSIS ━━
{results['analysis']}

━━ AGENT 2: TRAINING PLAN ━━
{results['training']}

━━ AGENT 3: ASSESSMENT RESULT ━━
Score: {results['score']}/{results['total']} ({round(results['score']/results['total']*100)}%)
Status: {"PASSED ✅" if results['score']/results['total'] >= 0.6 else "NEEDS REVIEW ⚠"}

━━ AGENT 4: HR REPORT ━━
{results['report']}

{"=" * 55}
Generated by OnboardIQ
github.com/rjena3214/onboardiq
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  📄 Report saved: {filename}")
    return filename


# ── MAIN PIPELINE ────────────────────────────────────

def main():
    print("\n")
    print("  ██████╗ ███╗   ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ ")
    print("  ██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗")
    print("  ██║   ██║██╔██╗ ██║██████╔╝██║   ██║███████║██████╔╝██║  ██║")
    print("  ██║   ██║██║╚██╗██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║")
    print("  ╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝")
    print("   ╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ")
    print("\n         AI Employee Onboarding Platform — 4 Agent Pipeline")
    print("         github.com/rjena3214  |  Built with Claude API\n")

    # ── STEP 1: Collect Company Info ──
    separator("STEP 1 — Company Information")
    data = {}
    data['company']         = get_input("  Company Name       : ")
    data['industry']        = get_input("  Industry / Sector  : ")
    data['culture']         = get_input("  Culture (optional) : ", required=False)

    # ── STEP 2: Collect Candidate Info ──
    separator("STEP 2 — Candidate Information")
    data['name']            = get_input("  Candidate Name     : ")
    data['role']            = get_input("  Job Role / Title   : ")
    data['dept']            = get_input("  Department         : ", required=False)
    data['background']      = get_input("  Background         : ", required=False)
    data['responsibilities'] = get_input("  Responsibilities   : ", required=False)

    # Generate Case ID
    case_id = f"OIQ-{datetime.now().strftime('%y%m%d%H%M')}"

    separator(f"PIPELINE STARTING — Case {case_id}")
    print(f"  Employee : {data['name']}")
    print(f"  Role     : {data['role']} at {data['company']}")
    print(f"  Running 4 AI agents...\n")

    results = {}

    # ── AGENT 1: Role & Risk Analysis ──
    separator("AGENT 01 — Role & Risk Analyser")
    results['analysis'] = call_agent("Agent 1", agent1_prompt(data))
    print("\n" + results['analysis'])

    # ── AGENT 2: Training Designer ──
    separator("AGENT 02 — Training Designer")
    results['training'] = call_agent("Agent 2", agent2_prompt(data, results['analysis']))
    print("\n" + results['training'])

    # ── AGENT 3: Assessment Engine ──
    separator("AGENT 03 — Assessment Engine")
    raw_q = call_agent("Agent 3", agent3_prompt(data))
    
    try:
        clean = raw_q.replace("```json", "").replace("```", "").strip()
        questions = json.loads(clean)
    except:
        print("  ⚠ Could not parse questions — using defaults.")
        questions = [
            {"q": f"What is the primary responsibility of a {data['role']}?",
             "options": ["A. Administrative tasks only", "B. Achieving role objectives and KPIs",
                        "C. Managing other departments", "D. None of the above"], "answer": 1},
            {"q": "How should you handle a task you are unfamiliar with?",
             "options": ["A. Ignore it", "B. Do it incorrectly", 
                        "C. Ask your manager or refer to training", "D. Delegate immediately"], "answer": 2},
            {"q": "What is the best way to update your manager on progress?",
             "options": ["A. Wait until asked", "B. Regular updates through agreed channels",
                        "C. Only report failures", "D. Avoid communication"], "answer": 1},
            {"q": "When should you escalate an issue?",
             "options": ["A. Never", "B. Only after solving it yourself",
                        "C. When it exceeds your authority or expertise", "D. Every minor issue"], "answer": 2},
            {"q": "How should you handle constructive feedback from your manager?",
             "options": ["A. Ignore it", "B. Accept and act on it constructively",
                        "C. Argue if you disagree", "D. Only accept positive feedback"], "answer": 1},
        ]

    # Run the assessment interactively
    score = run_assessment(questions)
    results['score'] = score
    results['total'] = len(questions)
    pct = round(score / len(questions) * 100)
    
    separator("ASSESSMENT RESULT")
    print(f"  Score  : {score}/{len(questions)} ({pct}%)")
    print(f"  Status : {'✅ PASSED' if pct >= 60 else '⚠  NEEDS REVIEW'}")

    # ── AGENT 4: Report Generator ──
    separator("AGENT 04 — Report Generator")
    results['report'] = call_agent("Agent 4", agent4_prompt(data, results['analysis'], case_id))
    print("\n" + results['report'])

    # ── SAVE ──
    separator("PIPELINE COMPLETE")
    filename = save_report(data, results, case_id)
    
    print(f"\n  ✅ Onboarding pipeline complete for {data['name']}")
    print(f"  Case ID : {case_id}")
    print(f"  Score   : {score}/{len(questions)} ({pct}%)")
    print(f"  Report  : {filename}")
    print("\n  Thank you for using OnboardIQ.")
    print("  github.com/rjena3214/onboardiq\n")


if __name__ == "__main__":
    main()
