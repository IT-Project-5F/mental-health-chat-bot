import type { Service } from "./Columns"
import { columns } from "./Columns"
import { DataTable } from "../../components/ui/data-table"
import { useEffect, useState } from "react"

const initialData: Service[] = [
    {
        name: "13YARN",
        email: "13yarn@gmail.com",
        status: "active",
        type: "online"
    },
    {
        name: "1800 My Options",
        email: "13yarn@gmail.com",
        status: "active",
        type: "online"
    },
    {
        name: "Australian Psychology Society",
        email: "13yarn@gmail.com",
        status: "active",
        type: "online"
    },
]

function Services() {

    const [data, setData] = useState<Service[]>([])

    useEffect(() => {
        setData(initialData)
    }, [])

    return (
        <div className="container mx-auto py-0">
            <DataTable columns={columns} data={data} pageSize={10} />
        </div>
    )
};

export default Services;