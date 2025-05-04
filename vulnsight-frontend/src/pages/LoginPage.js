import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
    const [name, setName] = useState("");
    const [target, setTarget] = useState("");
    const nav = useNavigate();

    const go = () => {
        localStorage.setItem("analyst", name);
        localStorage.setItem("target", target);
        nav("/newscan");
    };

    return (
        <div className="center">
            <h1>VulnSight</h1>
            <p>AI-powered cloud security scanner</p>
            <input placeholder="Your name" value={name} onChange={e => setName(e.target.value)} />
            <input placeholder="Target IP / Host" value={target} onChange={e => setTarget(e.target.value)} />
            <button onClick={go} disabled={!name || !target}>Log In & Scan</button>
        </div>
    );
}
