import { useState } from "react";
import { Link, Navigate, useNavigate, useLocation } from "react-router-dom";
import { request } from "@/api";
import { Button } from "@/components/ui/button";

/**
 * Description:
 * - Password reset page collects username and new password
 * - Must input new password twice to confirm
 */
function PasswordReset() {
    const navigate = useNavigate();
    const location = useLocation();

    // Extract password reset token from URL
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get("token") || "";

    // Redirect if user attempts to enter the page without a password reset email with token
    if (!token) {
        return <Navigate to="/login" replace />
    }

    const [username, setUsername] = useState("");
    const [new_password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    // Call backend to update password of a given username, require token
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Check for password before API call
        if (new_password !== confirmPassword) {
            alert("Passwords do not match")
            return
        }

        setLoading(true);

        try {
            const result = await request("PUT", "/api/auth/confirm_reset", { token, username, new_password }, true, "json");
            if (result && result.id) {
                setSuccess(true)
                setTimeout(() => navigate("/login"), 2000);
            }
        } catch (error) {
            console.error("Password reset error: ", error);
            alert("An error occurred during password reset. Please try again.");
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="absolute w-screen h-screen bg-[#01563E] inset-0">
            {success ? (
                // Same page re-render on password reset success
                <div className="flex flex-col items-center justify-center h-screen text-center text-[#CBDB2F] px-4 text-lg ">
                    <p className="my-1 mr-1 text-[#CBDB2F]">
                        Password reset successful! Redirecting to log in...
                    </p>
                    <p>
                        If you haven't been redirected after a few seconds,&nbsp;
                        <Link
                            to="/login"
                            className="text-[#CBDB2F] underline hover:text-white"
                        >
                            click here
                        </Link>
                    </p>
                </div>
            ) : (
                <form onSubmit={handleSubmit} className="flex flex-col h-screen items-center justify-center">
                    <h1 className="p-6 text-3xl font-bold text-[#CBDB2F]">Password Reset</h1>
                    <div className="flex flex-col items-start">
                        <label htmlFor="username" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Username</label>
                        <input
                            id="username"
                            type="text"
                            placeholder="Your Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                        />
                    </div>
                    <div className="flex flex-col items-start">
                        <label htmlFor="password" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">New Password</label>
                        <input
                            id="password"
                            type="password"
                            placeholder="New password"
                            value={new_password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                        />
                    </div>
                    <div className="flex flex-col items-start">
                        <label htmlFor="confirmPassword" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Confirm Password</label>
                        <input
                            id="confirmPassword"
                            type="password"
                            placeholder="Confirm password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                        />
                    </div>
                    <div className="m-2 sm:m-6">
                        <Button size={"xl"} type="submit" disabled={loading}>
                            {loading ? "Resetting...": "Reset"}
                        </Button>
                    </div>
                </form>
            )}
        </div>
    )
}

export default PasswordReset;