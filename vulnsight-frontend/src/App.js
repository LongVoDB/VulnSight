import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import NewScanPage from "./pages/NewScanPage";
import ScanResultPage from "./pages/ScanResultPage";
import HistoryPage from "./pages/HistoryPage";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/newscan" element={<NewScanPage />} />
                <Route path="/scan/:id" element={<ScanResultPage />} />
                <Route path="/history" element={<HistoryPage />} />
            </Routes>
        </BrowserRouter>
    );
}
