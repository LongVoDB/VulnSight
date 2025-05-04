import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { getMyCases, getAllCases } from "../api";

// helper: "20250504012715Z"  →  "2025-05-04T01:27:15Z"
function toISO(ts) {
    return ts.replace(
        /(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})Z/,
        "$1-$2-$3T$4:$5:$6Z"
    );
}

export default function HistoryPage() {
    const nav = useNavigate();
    const location = useLocation();
    const me = localStorage.getItem("analyst") || "";
    const allMode = new URLSearchParams(location.search).get("all") === "true";
    const [rows, setRows] = useState([]);

    useEffect(() => {
        (async () => {
            setRows(allMode ? await getAllCases() : await getMyCases(me));
        })();
    }, [allMode, me]);

    return (
        <div style={{ padding: 20, fontFamily: "Arial" }}>
            <h2>{allMode ? "All Cases" : "My Cases"}</h2>

            {/* navigation bar */}
            <div style={{ marginBottom: 16 }}>
                <button onClick={() => nav("/")}>New Scan</button>{" "}
                <button onClick={() => nav("/history")}>My History</button>{" "}
                <button onClick={() => nav("/history?all=true")}>All Cases</button>
            </div>

            <table border="1" cellPadding="6">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Target</th>
                        <th>Owner</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {rows.map(r => (
                        <tr key={r.case_id}
                            style={{ cursor: "pointer" }}
                            onClick={() => nav(`/scan/${r.case_id}`)}>
                            <td>{r.case_id}</td>
                            <td>{r.target}</td>
                            <td>{r.user_name}</td>
                            <td>{new Date(toISO(r.scan_timestamp)).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
