/* Types and Interfaces */
interface SuggestedQueryButtonProps {
    text: string;
    onClick: (query: string) => void;
}

const SuggestedQueryButton: React.FC<SuggestedQueryButtonProps> = ({ text, onClick }) => {
    return (
        <button
            onClick={() => onClick(text)} 
            style={{
                backgroundColor: '#FFDBE4',
                color: '#014532',
                borderColor: '#F291A9',
                boxShadow: `0 2px 0 0 #F291A9`,
            }}
            className="max-w-xs sm:max-w-md p-3 rounded-full border-2 border-[#FDB4C6]
                bg-[#FFDBE4] text-[#014532] font-semibold text-sm shadow-lg
                hover:bg-[#FDB4C6] hover:border-[#F291A9] transition-all duration-150 ease-in-out
                hover:translate-y-0.5
                "
        >
            <p className="whitespace-pre-wrap">{text}</p>
        </button>
    );
};

export default SuggestedQueryButton;