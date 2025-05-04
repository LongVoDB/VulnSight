import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getMyCases } from "../api";

// helper for timestamp → ISO
function toISO(ts) {
    return ts.replace(
        /(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})Z/,
        "$1-$2-$3T$4:$5:$6Z"
    );
}

export default function ScanResultPage() {
    const { id } = useParams();
    const nav = useNavigate();
    const analyst = localStorage.getItem("analyst") || "";
    const [item, setItem] = useState(null);
    const [panel, setPanel] = useState("");

    useEffect(() => {
        (async () => {
            const list = await getMyCases(analyst);
            setItem(list.find(c => c.case_id === id));
        })();
    }, [id, analyst]);

    if (!item) return <p style={{ padding: 20 }}>Loading…</p>;

    const niceDate = new Date(toISO(item.scan_timestamp)).toLocaleString();

    return (
        <div style={{ padding: 20, fontFamily: "Arial" }}>
            <h2>Scan Details</h2>

            <div style={{ marginBottom: 12 }}>
                <strong>ID:</strong> {item.case_id} &nbsp;
                <strong>Analyst:</strong> {item.user_name} &nbsp;
                <strong>Date:</strong> {niceDate}
            </div>

            {/* navigation */}
            <div style={{ marginBottom: 16 }}>
                <button onClick={() => nav(-1)}>⬅ Back</button>{" "}
                <button onClick={() => nav("/history")}>My History</button>{" "}
                <button onClick={() => nav("/history?all=true")}>All Cases</button>
            </div>

            {["scan_result", "pentest_result", "compliance_report"].map(k => (
                <div key={k} style={{ marginBottom: 12 }}>
                    <button onClick={() => setPanel(panel === k ? "" : k)}>
                        {k.replace("_", " ").toUpperCase()}
                    </button>
                    {panel === k && (
                        <pre style={{
                            whiteSpace: "pre-wrap",
                            background: "#f4f4f4",
                            padding: 10,
                            marginTop: 6
                        }}>
                            {item[k]}
                        </pre>
                    )}
                </div>
            ))}
        </div>
    );
}
