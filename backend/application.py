from flask import Flask, request, jsonify
import boto3
import uuid
from datetime import datetime
from ai_vuln_analyzer import parse_nmap, fetch_cve, analyze_with_gpt
from ai_pen_test_module import parse_nmap_for_ports, run_targeted_pentest, ai_pentest_analysis
from ai_report import analyze_compliance
from flask_cors import CORS

application = Flask(__name__)  # <-- changed from app to application
CORS(application) 

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  # Use your region explicitly
table = dynamodb.Table('ScanCases')

@application.route('/scan', methods=['POST'])
def scan():
    data = request.json
    user_name = data['user_name']
    target = data['target']
    case_id = datetime.utcnow().strftime("%Y%m%d%H%M%SZ")

    # Assume 'scan_results.xml' already exists after user ran nmap manually
    services = parse_nmap('scan_results.xml')
    scan_results = ""
    for service, version in services:
        if version:
            cves = fetch_cve(service, version)
            scan_results += f"{service} {version}:\n" + "\n".join(cves) + "\n\n"

    vuln_analysis = analyze_with_gpt(scan_results)

    # Store explicitly to DynamoDB
    table.put_item(Item={
        'case_id': case_id,
        'user_name': user_name,
        'target': target,
        'scan_timestamp': case_id,
        'scan_result': vuln_analysis
    })

    return jsonify({"case_id": case_id, "analysis": vuln_analysis}), 200

@application.route('/pentest', methods=['POST'])
def pentest():
    data = request.json
    target = data['target']
    case_id = data['case_id']

    ports = parse_nmap_for_ports('scan_results.xml')
    pentest_results = run_targeted_pentest(target, ports)
    pentest_analysis = ai_pentest_analysis(pentest_results)

    table.update_item(
        Key={'case_id': case_id},
        UpdateExpression="set pentest_result=:r",
        ExpressionAttributeValues={':r': pentest_analysis}
    )

    return jsonify({"pentest_analysis": pentest_analysis}), 200

@application.route('/compliance', methods=['POST'])
def compliance():
    data = request.json
    case_id = data['case_id']

    item = table.get_item(Key={'case_id': case_id})['Item']
    pentest_analysis = item['pentest_result']
    compliance_report = analyze_compliance(pentest_analysis)

    table.update_item(
        Key={'case_id': case_id},
        UpdateExpression="set compliance_report=:c",
        ExpressionAttributeValues={':c': compliance_report}
    )

    return jsonify({"compliance_report": compliance_report}), 200

@application.route('/cases', methods=['GET'])
def list_cases():
    response = table.scan()
    return jsonify(response['Items']), 200

@application.route('/cases/<user_name>', methods=['GET'])
def user_cases(user_name):
    response = table.query(
        IndexName='user_name-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user_name').eq(user_name)
    )
    return jsonify(response['Items']), 200

if __name__ == "__main__":
    application.run(debug=True)  # <-- updated here as well
