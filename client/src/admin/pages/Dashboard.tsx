import { Button } from "@/components/ui/button";

type DashboardProps = {
    onNavigate: (page: number) => void;
    username: string;
}

function Dashboard( { onNavigate, username }: DashboardProps ) {
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