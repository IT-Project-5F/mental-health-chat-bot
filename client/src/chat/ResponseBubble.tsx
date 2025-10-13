/* Types and Interfaces */
interface ResponseBubbleProps {
    text: string;
}

const ResponseBubble: React.FC<ResponseBubbleProps> = ({ text }) => {
    return (
        <div className="
            max-w-[80%]
            p-3
            rounded-tr-2xl rounded-tl-md rounded-br-2xl rounded-bl-2xl
            bg-[#366B5D] text-white
            shadow-lg
            mr-auto
            break-words text-left
            self-start
            animate-slideIn
            "
            style={{ animation: 'slideIn 0.3s ease-out forwards' }}
        >
            <p className="whitespace-pre-wrap">{text}</p>
        </div>
    );
};

export default ResponseBubble;