import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { getToken, decodeToken } from "@/utils/auth";

type DashboardProps = {
    onNavigate: (page: number) => void;
}

/**
 * Description:
 * - Welcome page of admin page
 * - Allow redirection (rerender) to other admin pages
 */
function Dashboard( { onNavigate }: DashboardProps ) {
    const [username, setUsername] = useState("User");

    useEffect(() => {
        const token = getToken();
        if (token) {
            const decoded = decodeToken(token);
            if (decoded) {
                setUsername(decoded.sub);
            }
        }
    }, []);

    return (
        <div className="flex flex-col justify-center items-center h-full gap-4">
            <h1 className="text-4xl">Welcome back, {username}!</h1>
            <p>Click on the buttons below to find out more about the admin portal!</p>
            <div className="flex flex-col sm:flex-row gap-4">
                <Button
                    size={"xl"}
                    onClick={() => onNavigate(1)}
                >
                    Services
                </Button>
                <Button
                    size={"xl"}
                    onClick={() => onNavigate(2)}
                >
                    Users
                </Button>
            </div>
        </div>
    )
};

export default Dashboard;