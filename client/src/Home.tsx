import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Map from "./Map";
import ChatContainer from "./chat/ChatContainer";
import QuickClose from "./QuickClose";
// import Listing from "./dropdown/Listing.tsx";
import { Button } from "./components/ui/button";

function Home() {
    const navigate = useNavigate();
    const [loggedIn, setLoggedIn] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (localStorage.getItem("access_token") || sessionStorage.getItem("access_token")) {
            setLoggedIn(true);
        }
    }, []);

    const handleLogOut = () => {

        setLoading(true);

        setTimeout(() => {
            if (localStorage.getItem("access_token")) {
                localStorage.removeItem("access_token");
                localStorage.removeItem("email_address");
                localStorage.removeItem("username");
            }
            if (sessionStorage.getItem("access_token")) {
                localStorage.removeItem("access_token");
                localStorage.removeItem("email_address");
                localStorage.removeItem("username");
            }

            setLoading(false);
            setLoggedIn(false);
        }, 2000);
    };

    return (
        <div className="w-screen flex overflow-hidden">
            <div className="absolute z-70 fixed top-3 sm:top-auto sm:bottom-5 left-5">
                { loggedIn ? (
                    <Button
                        onClick={handleLogOut}
                        variant={"secondary"}
                        size={"lg"}
                        disabled={loading}
                    >
                        {loading ? "Logging out" : "Log Out"}
                    </Button>
                    
                ) : (
                    <Button
                        onClick={() => navigate("/login")}
                        variant={"secondary"}
                        size={"lg"}
                    >
                        Login
                    </Button>
                )}
                
            </div>
            <div className="absolute z-60 fixed top-0 left-0 w-full group justify-center hidden sm:block">
                <div className="flex justify-end px-20 py-2 bg-[#DCEAAB] opacity-0 -translate-y-full transition-all duration-150 ease-in-out pointer-events-none group-hover:opacity-100 group-hover:translate-y-0 group-hover:pointer-events-auto">
                    <QuickClose/>
                </div>
            </div>
            <div className="absolute z-60 top-3 right-5 block sm:hidden">
                <QuickClose/>
            </div>
            <div className="absolute inset-0 z-0">
                <Map/>
            </div>
            {/* <div className="absolute inset-0 top-0 left-0 sm:top-10 sm:left-10">
                <Listing/>
            </div> */}
            <div>
                <ChatContainer/>
            </div>
        </div>
    )
}

export default Home;