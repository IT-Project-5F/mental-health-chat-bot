function AccountToggle() {
    return (
        <div className="mx-4 mt-2 px-4 py-6 border-b-1">
            <div className="flex items-center space-x-6">
                <h1 className="rounded-full bg-white text-gray-500 w-20 h-20 flex items-center justify-center">Avatar</h1>
                <div className="text-left overflow-x-hidden">
                    <h1 className="text-xl font-bold">John Doe</h1>
                    <p className="text-sm">admin</p>
                    <p className="text-sm break-words max-w-[180px]">very_very_long_email_of_johndoe@health.vic.org.au</p>
                </div>
            </div>
        </div>
    )
};

export default AccountToggle;