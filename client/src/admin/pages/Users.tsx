import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "../../components/ui/data-table"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
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

type UserProps = {
    pageSize?: number
}

export type User = {
    id: number
    username: string
    email_address: string
    location?: string
}

function Users({ pageSize = 20 }: UserProps) {

    const [users, setUsers] = useState<User[]>([])
    const [pendingUsers, setPendingUsers] = useState<User[]>([])
    const [loading, setLoading] = useState(true)
    const [loadingPending, setLoadingPending] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [errorPending, setErrorPending] = useState<string | null>(null)

    // Fetch all users from the backend including pending users
    useEffect(() => {
        const fetchUsers = async () => {
            setLoading(true)
            setError(null)
            try {
                const result = await request("GET", "/api/users/")

                if (result.requestError) {
                    setError(result.message)
                } else {
                    setUsers(result)
                }
            } catch (error) {
                setError("An error occurred while fetching users.")
                console.error("Error fetching users: ", error)
            } finally {
                setLoading(false)
            }
        }
        fetchUsers()
    }, [])

    // Fetch pending users from the backend
    useEffect(() => {
        const fetchPendingUsers = async () => {
            setLoadingPending(true)
            setErrorPending(null)
            try {
                const result = await request("GET", "/api/users/pending")

                if (result.requestError) {
                    setErrorPending(result.message)
                } else {
                    setPendingUsers(result)
                }
            } catch (error) {
                setErrorPending("An error occurred while fetching pending users.")
                console.error("Error fetching pending users: ", error)
            } finally {
                setLoadingPending(false)
            }
        }
        fetchPendingUsers()
    }, [])

    const handleAcceptUser = async (username: string) => {
        // Confirm before accepting user
        const confirmAccept = window.confirm(`Are you sure you want to accept the user "${username}"?`);
        if (!confirmAccept) return;

        try {
            const result = await request("POST", `/api/users/accept/${username}`)
            console.log('Accepted user:', result);
            // Remove user from pending list
            setPendingUsers(prev => prev.filter(user => user.username !== username))
        } catch (error) {
            console.error("Error accepting user: ", error)
            alert("An error occurred while accepting the user. Please try again.")
        }
    }

    const handleDeclineUser = async (username: string) => {
        // Confirm before declining user
        const confirmDecline = window.confirm(`Are you sure you want to decline the user "${username}"? This action cannot be undone.`);
        if (!confirmDecline) return;

        try {
            const result = await request("DELETE", `/api/users/decline/${username}`)
            console.log('Declined user:', result);
            // Remove user from pending list
            setPendingUsers(prev => prev.filter(user => user.username !== username))
            
        } catch (error) {
            console.error("Error declining user: ", error)
            alert("An error occurred while declining the user. Please try again.")
        }
    }

    const handleDeleteUser = async (username: string) => {
        // Confirm before deleting user
        const confirmDecline = window.confirm(`Are you sure you want to delete the user "${username}"? This action cannot be undone.`);
        if (!confirmDecline) return;

        try {
            const result = await request("DELETE", `/api/users/${username}`)
            console.log('Deleted user:', result);
            // Remove user from list
            setUsers(prev => prev.filter(user => user.username !== username))
            
        } catch (error) {
            console.error("Error deleting user: ", error)
            alert("An error occurred while deleting the user. Please try again.")
        }
    }

    // Define table columns for all users
    const userData: ColumnDef<User>[] = [
        {
            accessorKey: "username",
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
            accessorKey: "email_address",
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
            accessorKey: "location",
            header: ({ column }) => {
                return (
                    <div className="flex items-center">
                        <span>Location</span>
                        <ArrowUpDown
                            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                            className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                        />
                    </div>
                )
            },
        }
    ]

    // Define table columns for verified users. Allow deleting users
    const getVerifiedUsers = (handleDeleteUser: (username: string) => void): ColumnDef<User>[] => [
        ...userData,
        {
            id: "actions",
            cell: ({ row }) => {
                const user = row.original
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
                                onClick={() => { handleDeleteUser(user.username) }}
                            >
                                Delete
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                )
            }
        }
    ]

    // Define table columns for pending users. Allow accepting and declining pending users
    const getPendingUsers = (handleAcceptUser: (username: string) => void, handleDeclineUser: (username: string) => void): ColumnDef<User>[] => [
        ...userData,
        {
            id: "actions",
            cell: ({ row }) => {
                const user = row.original
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
                                onClick={() => { handleAcceptUser(user.username) }}
                            >
                                Accept
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                onClick={() => { handleDeclineUser(user.username) }}
                            >
                                Reject
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                )
            }
        }
    ]

    return (
        <div className="container mx-auto py-0 space-y-6">
            <div>
                <h2 className="mb-4">Pending Users</h2>
                {loadingPending ? (
                    <div>Loading...</div>
                ) : errorPending ? (
                    <div className="text-red-500">Error: {error}</div>
                ) : (
                    <DataTable columns={getPendingUsers(handleAcceptUser, handleDeclineUser)} data={pendingUsers} pageSize={pageSize} />
                )}
            </div>
            <div>
                <h2 className="mb-4">All Users</h2>
                {loading ? (
                    <div>Loading...</div>
                ) : error ? (
                    <div className="text-red-500">Error: {error}</div>
                ) : (
                    <DataTable columns={getVerifiedUsers(handleDeleteUser)} data={users} pageSize={pageSize} />
                )}
            </div>
        </div>
    )
};

export default Users;