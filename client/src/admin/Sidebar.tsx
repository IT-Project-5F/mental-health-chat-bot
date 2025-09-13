import AccountToggle from "./AccountToggle";

function Sidebar() {
    return (
        <div>
            
            <div className="overflow-y-scroll sticky top-0 h-screen bg-[#014532]">
                {/* TODO: Sidebar options */}
                <AccountToggle/>
            </div>

            {/* TODO: Plan toggle */}
        </div>
    )
};

export default Sidebar;