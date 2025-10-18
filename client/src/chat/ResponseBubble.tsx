import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/* Types and Interfaces */
interface ResponseBubbleProps {
    text: string;
}

/* Format headings and fields */
const formatResponse = (text: string) => {
    return text.replace(/\[(.*?)\]/g, (_, p1) => `# ${p1}`);
}

const ResponseBubble: React.FC<ResponseBubbleProps> = ({ text }) => {
    const formattedResponse = formatResponse(text);
    
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
                    h1: ({ node, ...props }) => (
                        <div>
                        {/* Line separator before heading 1 */}
                        <hr className="border-t border-white/40 my-3" />
                        <h1
                            className="text-xl font-bold mb-1"
                            style={{ color: "#DCEAAB" }}
                            {...props}
                        />
                        </div>
                    ),
                    h3: ({ node, ...props }) => (
                        <div>
                            <hr className="border-t border-white/40 my-3" />
                            <h3
                                className="text-lg font-bold mb-1"
                                style={{ color: "#DCEAAB" }}
                                {...props}
                            />
                        </div>
                    ),
                    p: ({ node, ...props }) => (
                        <p
                        style={{
                            whiteSpace: "pre-wrap",
                            marginBottom: "1.25rem"
                        }}
                        >
                        {props.children}
                        </p>
                    ),
                }}
            >
                {formattedResponse}
            </ReactMarkdown>
        </div>
    );
};

export default ResponseBubble;