import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                    a: ({ node, ...props }) => (
                        <a  
                            className="markdown-link"
                            target="_blank"
                            rel="noopener noreferrer"
                            {...props}
                        />
                    ),
                }}
            >
                {text}
            </ReactMarkdown>
        </div>
    );
};

export default ResponseBubble;