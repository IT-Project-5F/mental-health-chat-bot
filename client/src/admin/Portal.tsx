import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";

function Portal() {
    return (
        <div className="grid absolute w-screen h-screen inset-0 grid-cols-[240px_1fr]">
            <Sidebar/>
            <Dashboard/>
        </div>
    )
    
};

export default Portal;