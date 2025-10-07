import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/components/ui/data-table"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { request } from "@/api"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import {
    ArrowUpDown,
    MoreHorizontal
} from "lucide-react";
import type { Service } from "./ServicePage";

type ServiceProps = {
    pageSize?: number
    onEditService: (service: Service) => void
}

export const getServiceData = (onEdit: (service: Service) => void): ColumnDef<Service>[] => [
    {
        accessorKey: "service_name",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Service</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        }
    },
    {
        accessorKey: "organisation_name",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Org Name</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        }
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
        accessorKey: "phone",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Phone</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    },
    {
        accessorKey: "website",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Website</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    },
    {
        id: "actions",
        cell: ({ row }) => {
            const service = row.original
            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Open menu</span>
                            <MoreHorizontal className="h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel><h1>Actions</h1></DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                            onClick={() => onEdit(service)}
                        >
                            View
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        {/* TODO: Delete Action */}
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        }
    }
]

function Services({ pageSize = 10, onEditService }: ServiceProps) {
    const [data, setData] = useState<Service[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [query, setQuery] = useState("")

    const fetchServices = async (search: string) => {
        setLoading(true)
        setError(null)

        const result = await request("GET", `/api/database/search?q=${search}`)

        if (result.requestError) {
            setError(result.message)
            setData([])
        } else {
            setData(result)
        }

        setLoading(false)
    }

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault()
        if (!query.trim()) return
        fetchServices(query.trim())
    }

    return (
        <div className="container mx-auto py-4">
            {/* Search bar */}
            <form onSubmit={handleSearch} className="flex gap-2 mb-4">
                <Input
                    type="text"
                    placeholder="Search by name..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <Button
                    type="submit"
                    className="bg-[#014532] hover:bg-[#62BB46]"
                >
                    Search
                </Button>
            </form>

            {loading && <div>Loading...</div>}
            {error && <div className="text-red-500">Error: {error}</div>}

            {/* Results */}
            {!loading && !error && data.length > 0 && (
                <DataTable
                    columns={getServiceData(onEditService)}
                    data={data}
                    pageSize={pageSize}
                />
            )}
        </div>
    )
}

export default Services
