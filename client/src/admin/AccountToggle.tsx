import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

type AccountProps = {
    username: string;
    role: string;
    email: string;
}

function AccountToggle({username, role, email}: AccountProps) {
    return (
        <div className="mb-6 p-0 sm:p-4">
            <div className="flex items-center gap-8">
                <Avatar className="size-8 sm:size-16">
                    <AvatarImage src="https://github.com/shadcn.png"/>
                    <AvatarFallback>NA</AvatarFallback>
                </Avatar>
                <div className="text-left text-white overflow-x-hidden hidden sm:block">
                    <h1 className="text-lg font-bold">{username}</h1>
                    <p className="text-sm">{role}</p>
                    <p className="text-sm break-words">{email}</p>
                </div>
            </div>
        </div>
    )
};

export default AccountToggle;