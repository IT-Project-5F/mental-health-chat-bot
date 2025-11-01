import AccountToggle from "./AccountToggle";
import SidebarRoute from "./SidebarRoute";
import { useState, useEffect } from "react";
import { getToken, decodeToken, getUserEmail } from "@/utils/auth";

type SidebarProps = {
    selected: number;
    setSelected: (index: number) => void;
}

/**
 * Description:
 * - Admin portal sidebar
 * - Layout of account and routes
 */
function Sidebar({selected, setSelected}: SidebarProps) {
    const [username, setUsername] = useState("User");
    const [role, setRole] = useState("user");
    const [email, setEmail] = useState("---");

    useEffect(() => {
        const token = getToken();
        if (token) {
            const decoded = decodeToken(token);
            if (decoded) {
                setUsername(decoded.sub);
                setRole(decoded.role);
                const userEmail = getUserEmail();
                if (userEmail) {
                    setEmail(userEmail);
                }
            }
        }
    }, []);

    return (
        <div className="flex justify-between">
            <div className="p-4 overflow-y-scroll sticky h-screen bg-[#014532] rounded-r-2xl">
                <AccountToggle username={username} role={role} email={email}/>
                <hr className="border-[#CBDB2F] opacity-30" />
                <SidebarRoute selected={selected} setSelected={setSelected}/>
            </div>
        </div>
    )
};

export default Sidebar;