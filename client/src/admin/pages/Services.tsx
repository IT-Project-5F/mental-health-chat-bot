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
import type { ServiceFormData } from "@/formComponents/service-form"

type ServiceProps = {
    pageSize?: number
    onEditService: (service: ServiceFormData) => void
}

function Services({ pageSize = 10, onEditService }: ServiceProps) {
    const [data, setData] = useState<ServiceFormData[]>([])
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

    const handleDeleteService = async (service_name: string, service_campus_key: string) => {
        // Confirm before deleting service
        const confirmDecline = window.confirm(`Are you sure you want to delete the service "${service_name}"? This action cannot be undone.`);
        if (!confirmDecline) return;

        try {
            const result = await request("DELETE", `/api/database/${service_campus_key}`)
            console.log('Deleted service:', result);
            // Remove service from list
            setData(prev => prev.filter(service => service.service_name !== service_name))
            
        } catch (error) {
            console.error("Error deleting service: ", error)
            alert("An error occurred while deleting the service. Please try again.")
        }
    }

    // Define table columns (only displaying a few key fields for brevity)
    const getServiceData = (onEdit: (service: ServiceFormData) => void): ColumnDef<ServiceFormData>[] => [
        {
            accessorKey: "service_name",
            header: ({ column }) => {
                return (
                    <div className="flex items-center gap-2">
                        <span>Service</span>
                        <Button
                            variant={"ghost"}
                            size={"icon"}
                            className="opacity-50 hover:opacity-100 hover:border-none hover:text-[#CBDB2F]"
                            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        >
                            <ArrowUpDown />
                        </Button>
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
                        <Button
                            variant={"ghost"}
                            size={"icon"}
                            className="opacity-50 hover:opacity-100 hover:border-none hover:text-[#CBDB2F]"
                            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        >
                            <ArrowUpDown />
                        </Button>
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
                        <Button
                            variant={"ghost"}
                            size={"icon"}
                            className="opacity-50 hover:opacity-100 hover:border-none hover:text-[#CBDB2F]"
                            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        >
                            <ArrowUpDown />
                        </Button>
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
                        <Button
                            variant={"ghost"}
                            size={"icon"}
                            className="opacity-50 hover:opacity-100 hover:border-none hover:text-[#CBDB2F]"
                            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        >
                            <ArrowUpDown />
                        </Button>
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
                            <Button variant="ghostdark" size={"icon"}>
                                <span className="sr-only">Open menu</span>
                                <MoreHorizontal className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="rounded-md">
                            <DropdownMenuLabel>
                                <h1 className="font-semibold">Actions</h1>
                            </DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                onClick={() => onEdit(service)}
                            >
                                View
                            </DropdownMenuItem>
                            <DropdownMenuItem
                                onClick={() => {handleDeleteService(service.service_name, service.service_campus_key)}}
                            >
                                Delete
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                )
            },
        }
    ]

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
                    variant="secondary"
                    type="submit"
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
