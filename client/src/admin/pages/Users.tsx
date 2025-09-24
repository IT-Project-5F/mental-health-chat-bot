import type { User } from "./Columns"
import { userColumns } from "./Columns"
import { DataTable } from "../../components/ui/data-table"
import { useEffect, useState } from "react"

const initialData: User[] = [
    {
        name: "13YARN",
        email: "13yarn@gmail.com",
        verified: "pending",
    },
    {
        name: "1800 My Options",
        email: "13yarn@gmail.com",
        verified: "pending",
    },
    {
        name: "Australian Psychology Society",
        email: "13yarn@gmail.com",
        verified: "verified",
    },
]

function Users() {

    const [data, setData] = useState<User[]>([])

    useEffect(() => {
        setData(initialData)
    }, [])

    return (
        <div className="container mx-auto py-0">
            <DataTable columns={userColumns} data={data} pageSize={2} />
        </div>
    )
};

export default Users;