import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { X } from "lucide-react"
import { request } from '@/api';

type PasswordResetModalProps = {
    onClose: () => void;
}

function PasswordResetModal ({ onClose } : PasswordResetModalProps) {
    
    const [username, setUsername] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    
    const handleClose = () => {
        const confirmClose = window.confirm("Exiting now will discard all form progress. Are you sure you want to exit?");
        if (confirmClose) {
            onClose();
        }
    };
    
    const handlePasswordReset = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!username.trim()) {
            alert("Please provide a username")
            return;
        }

        setLoading(true);
        
        try {
            const result = await request("PUT", `/api/auth/reset/${username}`, { username }, true, "json");
            if (result && result.requestError) {
                setError(true);
            } else {
                setSuccess(true);
            }
        } catch (error) {
            console.error("Password reset error: ", error);
        } finally {
            setLoading(false);
        }
    }
    
    return (
        // Background of Modal Window - Not Scrollable
        <div className="fixed inset-0 bg-black/70 z-[9999] p-4 sm:p-8 flex items-center justify-center">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-[95vw] sm:max-w-3xl h-[80vh] flex flex-col relative transform transition-all duration-300 ease-out scale-100 opacity-100">
                
                {/* Modal Window Header */}
                <div className="flex sticky top-0 bg-gradient-to-r from-[#DCEAAB] to-[#A7C957] z-10 p-4 sm:p-6 border-b border-[#01563E] rounded-t-xl">
                    <h1 className="text-xl sm:text-2xl font-semibold text-[#014532]">Password Reset</h1>
                        <Button
                            onClick={handleClose}
                            variant={"outline"}
                            size={"icon"}
                            className="absolute top-4 right-4"
                        >
                            <X />
                        </Button>
                </div>

                {/* Service Creation Form Component */}
                <form onSubmit={handlePasswordReset} className="flex flex-col h-screen items-center justify-center bg-[#01563E]">
                    { error ? (
                        <p className="my-1 mr-1 text-red-300">
                            Password reset failed. Please try again.
                        </p>
                    ) : success ? (
                        <p className="my-1 mr-1 text-[#CBDB2F]">
                            Password reset link sent! Please check your email.
                        </p>
                    ) : (
                        <div>
                            <div className="flex flex-col items-start">
                                <label htmlFor="username" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Username</label>
                                <input
                                    id="username"
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="Your username"
                                    className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                                />
                            </div>
                            <div className="m-2 sm:m-6">
                                <Button size={"xl"} type="submit" disabled={loading}>
                                    {loading ? "Sending..." : "Send Reset Link"}
                                </Button>
                            </div>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
};


export default PasswordResetModal;