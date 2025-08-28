// Properties of Sender Bubble
interface SendBubbleProps {
    text: string;
}

const SendBubble: React.FC<SendBubbleProps> = ({ text }) => {
    return (
        <div className="
            max-w-xs
            p-3
            rounded-2xl
            bg-[#62BB46] text-white
            shadow-lg
            ml-12
            break-words text-left
            self-end
            "
        >
            <p>{text}</p>
        </div>
    );
};

export default SendBubble;
