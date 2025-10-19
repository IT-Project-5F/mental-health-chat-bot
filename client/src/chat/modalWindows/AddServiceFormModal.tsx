import { useState } from 'react';
import ServiceCreationForm from "@/formComponents/ServiceCreationForm";

/* Types and Interfaces */
interface ModalProps {
    onClose: () => void;
    onSuccess?: () => void;
}

/**
 * Description:
 * - 'Add a New Service' Suggested Action button is only shown for verified (logged in) healthcare professional users
 * - Modal Window is rendered in the centre of screen when triggged by user clicking 'Suggested Action Button'
 */
const AddServiceFormModal: React.FC<ModalProps> = ({ onClose, onSuccess }) => {
    /* States */
    const [showDescription, setShowDescription] = useState(false);
    
    /* Exiting of pop-up window */
    const handleClose = () => {
        const confirmClose = window.confirm("Exiting now will discard all form progress. Are you sure you want to exit?");
        if (confirmClose) {
            onClose();
        }
    };
    

    /* Rendering and Styling */
    return (
        // Background of Modal Window - Not Scrollable
        <div className="fixed inset-0 bg-black/70 z-[9999] p-4 sm:p-8 flex items-center justify-center">
            {/* Modal Container */}
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-[95vw] sm:max-w-3xl md:max-w-4xl lg:max-w-5xl xl:max-w-6xl h-[90vh] flex flex-col relative transform transition-all duration-300 ease-out scale-100 opacity-100">
                
                {/* Modal Window Header */}
                <div className="sticky top-0 bg-gradient-to-r from-[#DCEAAB] to-[#A7C957] z-10 p-4 sm:p-6 border-b border-[#01563E] rounded-t-xl">
                    <div className="flex flex-col items-start space-y-2">
                        <h1 className="text-xl sm:text-2xl font-semibold text-[#014532]">Add A New Service</h1>
                        {/* Collapsible Description about Pop-up Window */}
                        <button
                            onClick={() => setShowDescription(!showDescription)}
                            className="text-sm text-[#014532] underline hover:text-[#013f2c] focus:outline-none"
                        >
                            {showDescription ? "Hide description" : "Show description"}
                        </button>
                        {showDescription && (
                        <p className="text-sm sm:text-base text-[#014532] text-left">
                            Please complete all required fields to submit a new service. Ensure details are accurate before submitting.
                        </p>
                        )}
                    </div>

                    {/* Close Button */}
                    <button
                        onClick={handleClose}
                        className="absolute top-4 right-4 p-2 rounded-full bg-red-500 hover:bg-red-600 text-white z-20 transition duration-150 hover:rotate-90"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>

                {/* Service Creation Form Component */}
                <div className="max-w-full overflow-x-hidden">
                    <ServiceCreationForm onSuccess={onSuccess} />
                </div>
            </div>
        </div>
    );
};


export default AddServiceFormModal;