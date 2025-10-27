import { useState } from "react";
import Sidebar from "./Sidebar";
import Dashboard from "./pages/Dashboard";
import Services from "./pages/Services";
import Users from "./pages/Users";
import ServicePage from "./pages/ServicePage";
import ServiceCreationPage from "./pages/ServiceCreationPage";
import type { ServiceFormData } from "@/formComponents/service-form";
import { request } from "@/api";

function Portal() {
    const [selected, setSelected] = useState(0);
    const [selectedService, setselectedService] = useState<ServiceFormData | null>(null);
    const [createService, setCreateService] = useState(false);

    const handleEditService = async (service: ServiceFormData) => {
        const result = await request("GET", `/api/database/${service.service_campus_key}`);
        setselectedService(result);
    }

    const handleCreateService = () => {
        setCreateService(true);
    }

    const pages = [
        <Dashboard onNavigate={setSelected} />,
        <Services onEditService={handleEditService} onCreateService={handleCreateService}/>,
        <Users />
    ];

    return (
        <div className="grid absolute w-screen h-screen inset-0 grid-cols-[60px_1fr] sm:grid-cols-[360px_1fr]">
            <Sidebar selected={selected} setSelected={setSelected} />
            <div className="flex-1 p-6">
                {selectedService ? (
                    <ServicePage service={selectedService} onClose={() => setselectedService(null)}/>
                ) : createService ? (
                    <ServiceCreationPage onClose={() => setCreateService(false)} />
                ) : (
                    pages[selected]
                )
                }
            </div>
        </div>
    )
    
};

export default Portal;