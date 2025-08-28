// Properties of Response Bubble
interface ResponseBubbleProps {
    text: string;
}

const ResponseBubble: React.FC<ResponseBubbleProps> = ({ text }) => {
    return (
        <div className="
            max-w-xs
            p-3
            rounded-2xl border-1 border-solid border-gray-300
            bg-[#366B5D] text-white
            shadow-lg
            break-words text-left
            self-start
            "    
        >
            <p>{text}</p>
        </div>
    );
};

export default ResponseBubble;