import type React from "react";

/* Types and Interfaces */
interface SuggestedActionButtonProps {
    text: string;
    icon?: React.ReactNode
    onAction: () => void;
    requiresUserToken: boolean; // False if action is available to all users, True if only available to verified healthcare accounts
}

const SuggestedActionButton: React.FC<SuggestedActionButtonProps> = ({ text, icon, onAction, requiresUserToken }) => {
    return (
        <button
            onClick={onAction} 
            style={{
                backgroundColor: '#FFDBE4',
                color: '#014532',
                borderColor: '#F291A9',
                boxShadow: `0 2px 0 0 #F291A9`,
            }}
            className="flex items-center justify-center max-w-xs sm:max-w-md p-3 rounded-full border-2 border-[#FDB4C6]
                bg-[#FFDBE4] text-[#014532] font-semibold text-sm shadow-lg
                hover:bg-[#FDB4C6] hover:border-[#F291A9] transition-all duration-150 ease-in-out
                hover:translate-y-0.5
                "
        >
            {icon && <span className="text-lg">{icon}</span>}
            <span>{text}</span>
        </button>
    );
};

export default SuggestedActionButton;