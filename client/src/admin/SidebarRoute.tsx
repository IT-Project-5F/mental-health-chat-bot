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
                    className={`w-25 sm:w-80 py-2 rounded-lg transform transition-all duration-200 hover:translate-x-2 text-[#014532]
                                ${selected === index ? "bg-gradient-to-r from-[#FFDBE4] to-[#E4F0E0]" : "bg-transparent"}`}
                    onClick={() => setSelected(index)}
                >
                    <div>{item}</div>
                </button>
            ))}
        </div>
    )
};

export default SidebarRoute;