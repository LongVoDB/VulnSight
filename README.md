# VulnSight
# VulnSight – AI-Powered Cloud Security Scanner

**Course:** CIS-285I-25SP-01: CIS-285I Cloud Computing
**Team:** Vo, Yuv, Florida  
**Semester:** Spring 2025

---

## 1 Project Overview
VulnSight automates vulnerability scanning, penetration testing, and compliance
mapping via three AI-enhanced modules. Results are stored in DynamoDB so
analysts can track historical scans.

---

## 2 AWS Architecture

| Layer | AWS Service | Free-Tier  |
|-------|-------------|-------------------------|
| Front-end | Amazon S3 (static website) | ≤5 GB storage, free GET/PUT quotas |
| Back-end | Elastic Beanstalk (t3.micro) | 750 hrs/month EC2 free |
| Data | DynamoDB (ScanCases) | 25 RCU + 25 WCU free |
| CI/CD | GitHub Actions → AWS CLI | 2 000 min/mo free |



---

## 3 Live Demo S3 link

* **Front-end:** <http://vulnsight-frontend.s3-website.us-east-2.amazonaws.com>  


---

## 4 CI/CD Pipeline

| Trigger | Git branch | Workflow | Result |
|---------|------------|----------|--------|
| Code push | `main` | **Deploy Backend** | Builds ZIP, new EB version |
| Code push | `frontend` | **Deploy Frontend** | `npm run build` → sync to S3 |


---

## 5 Local Development

```bash
# Back-end
cd backend
pip install -r requirements.txt
python application.py

# Front-end
cd ../vulnsight-frontend
npm install
npm start

Difficulty encountered: More of a principle of sanitation pratices, We had to disable secret key scanning on github to get it to accept our openAI api keys due to time constraint
