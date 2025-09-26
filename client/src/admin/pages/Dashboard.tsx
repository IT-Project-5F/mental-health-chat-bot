import Services from "./Services";
import Users from "./Users";

function Dashboard() {
    return (
        <div className="grid grid-cols-12 gap-4">
            <div className="col-span-12 lg:col-span-6">
                <h1 className="m-2">Services</h1>
                <Services />
            </div>
            <div className="col-span-12 lg:col-span-6">
                <h1 className="m-2">Users</h1>
                <Users pageSize={10}/>
            </div>
        </div>
    )
};

export default Dashboard;