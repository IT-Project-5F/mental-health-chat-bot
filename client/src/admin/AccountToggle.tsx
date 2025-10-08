import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

type AccountProps = {
    username: string;
    role: string;
    email: string;
}

function AccountToggle({username, role, email}: AccountProps) {
    return (
        <div className="mx-4 mt-2 px-4 py-6 border-b-1">
            <div className="flex items-center space-x-8">
                <Avatar className="size-12 sm:size-16">
                    <AvatarImage src="https://github.com/shadcn.png"/>
                    <AvatarFallback>NA</AvatarFallback>
                </Avatar>
                <div className="text-left text-[#014532] overflow-x-hidden hidden sm:block">
                    <h1 className="text-xl font-bold">{username}</h1>
                    <p className="text-sm">{role}</p>
                    <p className="text-sm break-words max-w-[180px]">{email}</p>
                </div>
            </div>
        </div>
    )
};

export default AccountToggle;