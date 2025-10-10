import { House, Users, Clipboard } from "lucide-react";
import { Button } from "@/components/ui/button";

type SidebarRouteProps = {
    selected: number;
    setSelected: (index: number) => void;
}

function SidebarRoute( { selected, setSelected } : SidebarRouteProps) {
    const menuItems = [
        { name: "Dashboard", icon: <House /> },
        { name: "Services", icon: <Users /> },
        { name: "Users", icon: <Clipboard /> },
    ];

    return (
        <div className="flex flex-col items-center mt-4 sm:mt-8 space-y-4 font-bold">
            {/* Sidebar Buttons */}
            {menuItems.map((item, index) => (
                <Button
                    key={item.name}
                    variant={"ghost"}
                    size={"xl"}
                    className={`flex items-center justify-center text-[#CBDB2F] font-normal hover:text-[#CBDB2F] border-none transform transition-all duration-200 hover:translate-x-2
                                ${selected === index ? "font-bold" : ""}`}
                    onClick={() => setSelected(index)}
                >
                    <span>{item.icon}</span>
                    <span className="hidden sm:block">{item.name}</span>
                </Button>
            ))}
        </div>
    )
};

export default SidebarRoute;