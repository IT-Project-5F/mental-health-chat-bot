/* Types and Interfaces */
interface SendBubbleProps {
    text: string;
}

const SendBubble: React.FC<SendBubbleProps> = ({ text }) => {
    return (
        <div className="
            max-w-[85%]
            p-3
            rounded-2xl
            bg-[#62BB46] text-white
            shadow-lg
            ml-auto
            break-words text-left
            self-end
            "
        >
            <p className="whitespace-pre-wrap">{text}</p>
        </div>
    );
};

export default SendBubble;
