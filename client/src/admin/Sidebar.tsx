import AccountToggle from "./AccountToggle";
import SidebarRoute from "./SidebarRoute";

type SidebarProps = {
    selected: number;
    setSelected: (index: number) => void;
}

function Sidebar({selected, setSelected}: SidebarProps) {
    return (
        <div>
            <div className="p-4 overflow-y-scroll sticky top-0 h-screen bg-[#014532] rounded-r-2xl">
                <AccountToggle username="johnthebest" role="admin" email="very_very_long_email_of_john_doe@gmail.com"/>
                <hr />
                <SidebarRoute selected={selected} setSelected={setSelected}/>
            </div>
        </div>
    )
};

export default Sidebar;