import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

function AccountToggle() {
    return (
        <div className="mx-4 mt-2 px-4 py-6 border-b-1">
            <div className="flex items-center space-x-8">
                <Avatar className="size-12 sm:size-16">
                    <AvatarImage src="https://github.com/shadcn.png"/>
                    <AvatarFallback>JD</AvatarFallback>
                </Avatar>
                <div className="text-left text-white overflow-x-hidden hidden sm:block">
                    <h1 className="text-xl font-bold">John Doe</h1>
                    <p className="text-sm">admin</p>
                    <p className="text-sm break-words max-w-[180px]">very_very_long_email_of_johndoe@health.vic.org.au</p>
                </div>
            </div>
        </div>
    )
};

export default AccountToggle;