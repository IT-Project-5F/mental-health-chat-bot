import { useState } from "react";
import Sidebar from "./Sidebar";
import Dashboard from "./pages/Dashboard";

function Portal() {
    const [selected, setSelected] = useState(0);
    const pages = [<Dashboard />]
    return (
        <div className="grid absolute w-screen h-screen inset-0 grid-cols-[360px_1fr]">
            <Sidebar selected={selected} setSelected={setSelected}/>
            <div className="flex-1 p-6">{pages[selected]}</div>
        </div>
    )
    
};

export default Portal;