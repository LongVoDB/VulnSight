import subprocess
import nmap
from openai import OpenAI

client = OpenAI(api_key='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')

def parse_nmap_for_ports(xml_file):
    nm = nmap.PortScanner()
    nm.analyse_nmap_xml_scan(open(xml_file).read())
    ports = set()
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports.update(nm[host][proto].keys())
    return ports

def run_targeted_pentest(target, ports):
    ports_str = ",".join(str(port) for port in ports)
    command = f'nmap -sV -p {ports_str} --script=vuln,auth {target}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def ai_pentest_analysis(pentest_results):
    prompt = f"Given the following penetration testing results:\n\n{pentest_results}\n\n" \
             "Summarize critical vulnerabilities and clearly describe exploitability. Provide explicit recommended remediation steps."
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=700
    )
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    target_ip = input("Enter the target IP (e.g., 127.0.0.1): ")
    ports = parse_nmap_for_ports('scan_results.xml')

    print(f"Performing targeted penetration test on ports: {', '.join(map(str, ports))}")
    pentest_results = run_targeted_pentest(target_ip, ports)

    analysis = ai_pentest_analysis(pentest_results)

    # Explicitly saving results clearly to a file for Module 3
    with open('pentest_report.txt', 'w') as f:
        f.write(analysis)

    print("\n--- AI-driven Penetration Testing Analysis & Recommendations (saved to pentest_report.txt) ---\n")
    print(analysis)
