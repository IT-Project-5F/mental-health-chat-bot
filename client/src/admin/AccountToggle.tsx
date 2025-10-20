import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";
import { useNavigate } from "react-router-dom";

type AccountProps = {
  username: string;
  role: string;
  email: string;
};

function AccountToggle({ username, role, email }: AccountProps) {
  const navigate = useNavigate();

  const getInitials = (username: string) => {
    return username.charAt(0).toUpperCase();
  };

  return (
    <div className="mb-6 p-0 sm:p-4">
      <div className="flex items-center gap-4">
        <Avatar className="size-12 sm:size-16">
          <AvatarFallback className="bg-gray-600 text-white font-bold text-lg sm:text-2xl">
            {getInitials(username)}
          </AvatarFallback>
        </Avatar>
        <div className="text-left text-white overflow-x-hidden flex-1 hidden sm:block">
          <h1 className="text-lg font-bold">{username}</h1>
          {role === "admin" && (
            <span className="inline-flex items-center text-xs bg-[#CBDB2F] text-[#01563E] px-2 py-0.5 rounded font-semibold mb-1">
              Admin
            </span>
          )}
          <p className="text-xs break-words opacity-90">{email || "---"}</p>
        </div>
      </div>
      <Button
        onClick={() => navigate("/")}
        className="mt-4 w-full bg-[#FFC2D4] text-[#01563E] hover:bg-[#FFB0C9] hover:text-[#01563E] font-semibold"
        size="sm"
      >
        <Home className="mr-2 h-4 w-4" />
        Back to Chatbot
      </Button>
    </div>
  );
}

export default AccountToggle;
