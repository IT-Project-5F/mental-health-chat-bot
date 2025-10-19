import AccountToggle from "./AccountToggle";
import SidebarRoute from "./SidebarRoute";

type SidebarProps = {
    selected: number;
    setSelected: (index: number) => void;
    username: string;
    email: string;
}

function Sidebar( { selected, setSelected, username, email }: SidebarProps) {
    return (
        <div className="flex justify-between">
            <div className="p-4 overflow-y-scroll top-0 sticky h-screen bg-[#014532] rounded-r-2xl">
                <AccountToggle username={username} role="admin" email={email}/>
                <hr />
                <SidebarRoute selected={selected} setSelected={setSelected}/>
            </div>
        </div>
    )
};

export default Sidebar;