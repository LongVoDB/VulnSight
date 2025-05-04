import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { newScan, runPentest, runCompliance } from "../api";

export default function NewScanPage() {
    const nav = useNavigate();
    const analyst = localStorage.getItem("analyst");
    const target = localStorage.getItem("target");
    const [caseId, setCaseId] = useState(null);
    const [loading, setLoading] = useState(true);

    // run full 3-step scan once
    useEffect(() => {
        (async () => {
            try {
                const s = await newScan(analyst, target);
                await runPentest(s.case_id, target);
                await runCompliance(s.case_id);
                setCaseId(s.case_id);
            } finally { setLoading(false); }
        })();
    }, [analyst, target]);

    if (loading) return <p style={{ padding: 20 }}>⏳ Running full scan …</p>;

    return (
        <div style={{ padding: 20, fontFamily: "Arial" }}>
            <p>✅ Full scan finished!</p>
            <button onClick={() => nav(`/scan/${caseId}`)}>View results</button>{" "}
            <button onClick={() => nav("/history")}>My History</button>{" "}
            <button onClick={() => nav("/history?all=true")}>All Cases</button>
        </div>
    );
}
