import { useNavigate } from "react-router-dom";
import { LogOut, UserCircle } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { getToken, decodeToken, logout, getUserEmail } from "@/utils/auth";
import { useState, useEffect } from "react";

interface UserInfo {
  username: string;
  email: string;
  role: string;
}

export function NavUser() {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);

  useEffect(() => {
    const token = getToken();
    if (token) {
      const decoded = decodeToken(token);
      if (decoded) {
        // Get email from storage (stored during login)
        const email = getUserEmail() || "---";
        setUserInfo({
          username: decoded.sub,
          email: email,
          role: decoded.role,
        });
      }
    }
  }, []);

  const handleLogout = () => {
    logout();
    setUserInfo(null);
    navigate("/");
    window.location.reload();
  };

  const handleAdminPanel = () => {
    navigate("/admin");
  };

  const getInitials = (username: string) => {
    return username.charAt(0).toUpperCase();
  };

  // If not logged in, show Login button
  if (!userInfo) {
    return (
      <div className="fixed z-70 top-3 right-3 sm:bottom-5 sm:top-auto sm:right-auto sm:left-5">
        <Button
          onClick={() => navigate("/login")}
          className="bg-[#01563E] text-[#CBDB2F] hover:bg-[#014532] hover:text-[#B8C929] font-semibold px-6 py-2 sm:px-8 sm:py-3 text-sm sm:text-base"
          size="lg"
        >
          Login
        </Button>
      </div>
    );
  }

  const isAdmin = userInfo.role === "admin";
  const displayEmail = (!userInfo.email || userInfo.email === "No email") ? "---" : userInfo.email;

  return (
    <>
      {/* User Menu - Top Right on mobile, Bottom Left on desktop */}
      <div className="fixed z-70 top-3 right-3 sm:top-auto sm:right-auto sm:bottom-5 sm:left-5">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className="relative h-10 w-10 sm:h-auto sm:w-auto rounded-full sm:rounded-lg bg-[#01563E] hover:bg-[#014532] p-0 sm:px-3 sm:py-2 gap-2 shadow-md group"
            >
              <Avatar className="h-10 w-10 sm:h-8 sm:w-8">
                <AvatarFallback className="bg-[#CBDB2F] text-[#01563E] font-bold text-sm group-hover:bg-[#B8C929]">
                  {getInitials(userInfo.username)}
                </AvatarFallback>
              </Avatar>
              <div className="hidden sm:flex flex-col items-start text-left">
                <span className="text-sm font-semibold text-[#CBDB2F] group-hover:text-[#B8C929]">
                  {userInfo.username}
                </span>
                <span className="text-xs text-[#CBDB2F] opacity-80 group-hover:text-[#B8C929]">{displayEmail}</span>
              </div>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-56 bg-white border-2 border-[#01563E]"
            align="end"
            forceMount
          >
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-semibold text-[#01563E]">
                  {userInfo.username}
                </p>
                <p className="text-xs text-gray-600">{displayEmail}</p>
                {isAdmin && (
                  <span className="inline-flex items-center text-xs bg-[#CBDB2F] text-[#01563E] px-2 py-1 rounded font-semibold w-fit">
                    Admin
                  </span>
                )}
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator className="bg-[#01563E]" />
            {isAdmin && (
              <>
                <DropdownMenuItem
                  onClick={handleAdminPanel}
                  className="cursor-pointer text-[#01563E] hover:bg-[#DCEAAB] hover:text-[#01563E] focus:bg-[#DCEAAB] focus:text-[#01563E]"
                >
                  <UserCircle className="mr-2 h-4 w-4" />
                  <span>Admin Panel</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-gray-200" />
              </>
            )}
            <DropdownMenuItem
              onClick={handleLogout}
              className="cursor-pointer text-[#01563E] hover:bg-[#FFC2D4] hover:text-[#01563E] focus:bg-[#FFC2D4] focus:text-[#01563E]"
            >
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </>
  );
}
