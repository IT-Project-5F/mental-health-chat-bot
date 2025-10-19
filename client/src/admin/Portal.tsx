import { useState } from "react";
import Sidebar from "./Sidebar";
import Dashboard from "./pages/Dashboard";
import Services from "./pages/Services";
import Users from "./pages/Users";
import ServicePage from "./pages/ServicePage";
import type { ServiceFormData } from "@/formComponents/service-form";
import { request } from "@/api";

function Portal() {
    const [selected, setSelected] = useState(0);
    const [selectedService, setselectedService] = useState<ServiceFormData | null>(null);

    // Retrieve username and email to parse to admin portal (dashboard and sidebar)
    const username = localStorage.getItem("username") || sessionStorage.getItem("username") || "Unknown User";
    const email = localStorage.getItem("email") || sessionStorage.getItem("email") || "No Email";

    const handleEditService = async (service: ServiceFormData) => {
        const result = await request("GET", `/api/database/${service.service_campus_key}`);
        setselectedService(result);
    }

    // Exit without change to services
    const handleClose = () => {
        const confirmClose = window.confirm("Exiting now will discard all form progress. Are you sure you want to exit?");
        if (confirmClose) {
            setselectedService(null);
        }
    };

    const pages = [
        <Dashboard onNavigate={setSelected} username={username}/>,
        <Services onEditService={handleEditService}/>,
        <Users />
    ];

    return (
        <div className="grid absolute w-screen h-screen inset-0 grid-cols-[60px_1fr] sm:grid-cols-[360px_1fr]">
            <Sidebar selected={selected} setSelected={setSelected} username={username} email={email}/>
            <div className="flex-1 p-6">
                {selectedService
                    ? <ServicePage service={selectedService} onClose={handleClose}/>
                    : pages[selected]
                }
            </div>
        </div>
    )
    
};

export default Portal;