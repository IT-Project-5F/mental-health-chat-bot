import type { User } from "./Columns"
import { userColumns } from "./Columns"
import { DataTable } from "../../components/ui/data-table"
import { useEffect, useState } from "react"
import { request } from "@/api"

type UserProps = {
    pageSize?: number
}

function Users({ pageSize = 20 }: UserProps) {

    const [data, setData] = useState<User[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
            const fetchServices = async () => {
                setLoading(true)
                setError(null)
    
                const result = await request("GET", "/api/users")
    
                if (result.requestError) {
                    setError(result.message)
                } else {
                    setData(result)
                }
    
                setLoading(false)
            }
            fetchServices()
        }, [])
    
        if (loading) {
            return (
                <div>Loading...</div>
            )
        }
        if (error) {
            return (
                <div className="text-red-500">Error: {error} </div>
            )
        }

    return (
        <div className="container mx-auto py-0">
            <DataTable columns={userColumns} data={data} pageSize={pageSize} />
        </div>
    )
};

export default Users;