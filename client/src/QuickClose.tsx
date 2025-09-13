import { Link } from "react-router-dom";

function QuickClose () {
    return (
        <Link
            to="/register"
            className="flex items-center justify-center mx-2 px-4 sm:px-10 py-2 text-md sm:text-lg font-semibold text-[#01563E] no-underline bg-[#FDB4C6] rounded-3xl hover:bg-[#FFDBE4]"
            >
                Quick Close
        </Link>
    )
}

export default QuickClose;