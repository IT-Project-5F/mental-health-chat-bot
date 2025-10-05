import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "../../components/ui/data-table"
import { useEffect, useState } from "react"
import { request } from "@/api"

import {
    ArrowUpDown
} from "lucide-react";

type UserProps = {
    pageSize?: number
}

export type User = {
    name: string
    email: string
    verified: "pending" | "verified"
}

export const userColumns: ColumnDef<User>[] = [
    {
        accessorKey: "name",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Name</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    },
    {
        accessorKey: "email",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Email</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    },
    {
        accessorKey: "verified",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Verified</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    }
]

function Users({ pageSize = 20 }: UserProps) {

    const [data, setData] = useState<User[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
            const fetchUsers = async () => {
                setLoading(true)
                setError(null)
    
                const result = await request("GET", "/api/users/")
    
                if (result.requestError) {
                    setError(result.message)
                } else {
                    setData(result)
                }
    
                setLoading(false)
            }
            fetchUsers()
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