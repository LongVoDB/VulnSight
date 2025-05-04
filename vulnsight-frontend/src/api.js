const BASE = "http://vulnsight-env2.eba-fpfs72ed.us-east-2.elasticbeanstalk.com";

export async function newScan(user, target) {
    const r = await fetch(`${BASE}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_name: user, target })
    });
    return r.json(); // { case_id, analysis }
}

export async function runPentest(case_id, target) {
    const r = await fetch(`${BASE}/pentest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_id, target })
    });
    return r.json(); // { pentest_analysis }
}

export async function runCompliance(case_id) {
    const r = await fetch(`${BASE}/compliance`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_id })
    });
    return r.json(); // { compliance_report }
}

export async function getMyCases(user) {
    const r = await fetch(`${BASE}/cases/${user}`);
    return r.json();
}

export async function getAllCases() {
    const r = await fetch(`${BASE}/cases`);
    return r.json();
}
