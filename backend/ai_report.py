# -*- coding: utf-8 -*-
import os
import openai

# Configure OpenAI API key explicitly (or via env var)
openai.api_key = "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"

def read_pentest_report():
    """Reads penetration test results from Module 2 explicitly."""
    with open('pentest_report.txt', 'r', encoding='utf-8') as file:
        return file.read()

def analyze_compliance(pentest_results):
    """Requests GPT-4o to analyze pentest results for compliance."""
    prompt = (
        "You are a cybersecurity compliance expert. Analyze the provided penetration testing "
        "report and explicitly evaluate compliance according to NIST Cybersecurity Framework (CSF) "
        "and ISO/IEC 27001 standards. Clearly identify compliance issues, explicitly list gaps, "
        "and provide concise and actionable recommendations for improvement. Also complete the report based on your assessment where you find lacking\n\n"
        f"Penetration Testing Report:\n{pentest_results}\n\n"
        "Explicitly structured Compliance Report:"
    )
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    compliance_report = response.choices[0].message.content.strip()
    return compliance_report

def save_compliance_report(report):
    """Saves the compliance report to a text file."""
    with open('compliance_report.txt', 'w', encoding='utf-8') as file:
        file.write(report)

def main():
    """Runs the compliance analysis workflow."""
    print("Starting compliance analysis...")

    pentest_results = read_pentest_report()
    compliance_report = analyze_compliance(pentest_results)
    
    save_compliance_report(compliance_report)
    
    print("Compliance analysis complete. Report saved as 'compliance_report.txt'.\n")
    print("=== COMPLIANCE REPORT ===\n")
    print(compliance_report)
if __name__ == "__main__":
    main()
