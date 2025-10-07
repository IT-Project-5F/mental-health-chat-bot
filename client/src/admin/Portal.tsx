import { useState } from "react";
import Sidebar from "./Sidebar";
import Dashboard from "./pages/Dashboard";
import Services from "./pages/Services";
import Users from "./pages/Users";
import ServicePage, { type Service } from "./pages/ServicePage";
import { request } from "@/api";

function Portal() {
    const [selected, setSelected] = useState(0);
    const [selectedService, setselectedService] = useState<Service | null>(null);

    const handleEditService = async (service: Service) => {
        const result = await request("GET", `/api/database/${service.service_campus_key}`);
        setselectedService(result);
    }

    const pages = [
        <Dashboard />,
        <Services onEditService={handleEditService}/>,
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