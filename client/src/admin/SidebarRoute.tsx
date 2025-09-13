type SidebarRouteProps = {
    selected: number;
    setSelected: (index: number) => void;
}

function SidebarRoute({selected, setSelected}: SidebarRouteProps) {
    const menuItems = ["Dashboard", "Services", "Users"];

    return (
        <div className="flex flex-col items-center mt-8 space-y-4 font-bold">
            {/* Sidebar Buttons */}
            {menuItems.map((item, index) => (
                <button
                    key={item}
                    className={`w-80 py-2 rounded-lg
                                ${selected === index ? "text-[#014532] bg-gradient-to-r from-[#FFDBE4] to-[#E4F0E0]" : "text-white bg-transparent"}`}
                    onClick={() => setSelected(index)}
                >
                    {item}
                </button>
            ))}
        </div>
    )
};

export default SidebarRoute;