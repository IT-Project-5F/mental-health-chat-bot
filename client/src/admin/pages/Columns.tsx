import type { ColumnDef } from "@tanstack/react-table";
import { ArrowUpDown } from "lucide-react";

export type Service = {
    name: string
    email: string
    status: "active" | "inactive" | "expired"
    type: "online" | "in-person" | "hybrid"
}

export type User = {
    name: string
    email: string
    verified: "pending" | "verified"
}

export const columns: ColumnDef<Service>[] = [
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
        filterFn: "includesString"
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
        accessorKey: "status",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Status</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    },
    {
        accessorKey: "type",
        header: ({ column }) => {
            return (
                <div className="flex items-center">
                    <span>Type</span>
                    <ArrowUpDown
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="m-1 p-1 rounded-lg opacity-50 hover:opacity-100"
                    />
                </div>
            )
        },
    }
]

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