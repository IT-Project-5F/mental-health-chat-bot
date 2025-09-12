import { Link } from "react-router-dom";

function QuickClose () {
    return (
        <div className="fixed top-0 left-0 w-full group justify-center">
            <div className="flex justify-end px-20 py-2 bg-[#DCEAAB] opacity-100 -translate-y-full transition-all duration-150 ease-in-out pointer-events-none group-hover:opacity-100 group-hover:translate-y-0 group-hover:pointer-events-auto">
                <Link to="/register" className="flex items-center mx-2 px-10 py-2 text-lg font-semibold text-[#01563E] no-underline bg-[#FDB4C6] rounded-3xl">Quick Close</Link>
            </div>
        </div>
    )
}

export default QuickClose;