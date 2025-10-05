import { useState } from "react";
import Sidebar from "./Sidebar";
import Dashboard from "./pages/Dashboard";
import Services from "./pages/Services";
import Users from "./pages/Users";
import ServicePage from "./pages/ServicePage";
import type { Service } from "./pages/Services";

function Portal() {
    const [selected, setSelected] = useState(0);
    const [selectedService, setselectedService] = useState<Service | null>(null);

    const pages = [
        <Dashboard />,
        <Services onSelectService={setselectedService}/>,
        <Users />
    ];
    return (
        <div className="grid absolute w-screen h-screen inset-0 grid-cols-[360px_1fr]">
            <Sidebar selected={selected} setSelected={setSelected}/>
            <div className="flex-1 p-6">
                {selectedService
                    ? <ServicePage service={selectedService} onClose={() => setselectedService(null)}/>
                    : pages[selected]
                }
            </div>
        </div>
    )
    
};

export default Portal;