import { House, Users, Clipboard, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

type SidebarRouteProps = {
    selected: number;
    setSelected: (index: number) => void;
}

/**
 * Description:
 * - List of admin portal pages
 */
function SidebarRoute( { selected, setSelected } : SidebarRouteProps) {
    const navigate = useNavigate();
    const menuItems = [
        { name: "Dashboard", icon: <House /> },
        { name: "Services", icon: <Users /> },
        { name: "Users", icon: <Clipboard /> },
    ];

    const handleLogOut = async (e: React.FormEvent) => {
        e.preventDefault();
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");
        localStorage.removeItem("email");
        localStorage.removeItem("role");
        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("username");
        sessionStorage.removeItem("email");
        sessionStorage.removeItem("role");
        navigate('/login')
    }

    return (
        <div className="flex flex-col items-center mt-4 sm:mt-8 space-y-4 font-bold">
            {/* Sidebar Buttons */}
            {menuItems.map((item, index) => (
                <Button
                    key={item.name}
                    variant={"ghost"}
                    size={"xl"}
                    className={`flex items-center justify-center text-[#CBDB2F] font-normal hover:text-[#CBDB2F] border-none transform transition-all duration-200 hover:translate-x-2
                                ${selected === index ? "font-bold translate-x-2 sm:translate-none" : ""}`}
                    onClick={() => setSelected(index)}
                >
                    <span>{item.icon}</span>
                    <span className="hidden sm:block">{item.name}</span>
                </Button>
            ))}
            
            {/* Log out button */}
            <Button
                variant={"ghost"}
                size={"xl"}
                className="flex items-center justify-center text-[#CBDB2F] font-normal hover:text-[#CBDB2F] border-none transform transition-all duration-200 hover:translate-x-2"
                onClick={handleLogOut}
            >
                <span><LogOut /></span>
                <span className="hidden sm:block">Logout</span>
            </Button>
        </div>
    )
};

export default SidebarRoute;