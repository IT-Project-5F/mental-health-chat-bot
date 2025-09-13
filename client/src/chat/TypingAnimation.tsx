const TypingAnimation: React.FC = () => {
    return (
        <div className="flex items-center space-x-2 px-4 py-2 rounded-2xl w-fit">
            <svg xmlns="http://www.w3.org/2000/svg" width="50" height="20" viewBox="0 0 50 20" fill="none">
                <circle cx="5" cy="10" r="5" fill="#D9D9D9" className="animate-bounce" style={{ animationDelay: '0ms' }} />
                <circle cx="25" cy="10" r="5" fill="#D9D9D9" className="animate-bounce" style={{ animationDelay: '150ms' }} />
                <circle cx="45" cy="10" r="5" fill="#D9D9D9" className="animate-bounce" style={{ animationDelay: '300ms' }} />
            </svg>
        </div>
    )
}

export default TypingAnimation;