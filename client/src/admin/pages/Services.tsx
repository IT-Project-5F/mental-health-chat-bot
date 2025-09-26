import type { Service } from "./Columns"
import { columns } from "./Columns"
import { DataTable } from "@/components/ui/data-table"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { request } from "@/api"

function Services() {
    const [data, setData] = useState<Service[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [query, setQuery] = useState("")

    const fetchServices = async (search: string) => {
        setLoading(true)
        setError(null)

        const result = await request("GET", `/api/database/by-name/${search}`)

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
                <DataTable columns={columns} data={data} pageSize={5} />
            )}
        </div>
    )
}

export default Services
