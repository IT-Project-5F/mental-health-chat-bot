import AccountToggle from "./AccountToggle";
import SidebarRoute from "./SidebarRoute";

type SidebarProps = {
    selected: number;
    setSelected: (index: number) => void;
}

function Sidebar({selected, setSelected}: SidebarProps) {
    return (
        <div>
            
            <div className="overflow-y-scroll sticky top-0 h-screen bg-[#014532] rounded-r-4xl">
                <AccountToggle/>
                <SidebarRoute selected={selected} setSelected={setSelected}/>
            </div>
        </div>
    )
};

export default Sidebar;