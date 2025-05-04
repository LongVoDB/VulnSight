import subprocess
import nmap
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

client = OpenAI(api_key='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')

def parse_nmap(xml_file):
    nm = nmap.PortScanner()
    nm.analyse_nmap_xml_scan(open(xml_file).read())
    services = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                service = nm[host][proto][port]['name']
                version = nm[host][proto][port]['version']
                services.append((service, version))
    return services

def fetch_cve(service, version):
    query = f"{service} {version}"
    url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select("div#TableWithRules table tr")[1:4]
    cves = [f"{row.find_all('td')[0].text.strip()}: {row.find_all('td')[1].text.strip()}" for row in rows if len(row.find_all('td')) >=2]
    return cves if cves else ["No CVE found"]

def analyze_with_gpt(scan_results):
    prompt = f"Given the following vulnerability scan results:\n\n{scan_results}\n\n" \
             "Clearly summarize, prioritize vulnerabilities by risk, and recommend clear mitigation steps."
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=700
    )
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Enter your customized Nmap command explicitly (e.g., nmap -sV --script=vuln -oX scan_results.xml 127.0.0.1):")
    nmap_command = input("Your Nmap command: ")
    subprocess.run(nmap_command, shell=True)

    services = parse_nmap('scan_results.xml')
    scan_results = ""
    for service, version in services:
        if version:
            cves = fetch_cve(service, version)
            scan_results += f"{service} {version}:\n" + "\n".join(cves) + "\n\n"
    
    analysis = analyze_with_gpt(scan_results)
    print("\n--- AI-driven Security Analysis & Recommendations ---\n")
    print(analysis)
