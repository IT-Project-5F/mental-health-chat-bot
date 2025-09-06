type CardItemProps = {
  title: string
  address: string
  buttonText?: string
  buttonLink?: string
}

export function CardItem({ title, address, buttonText, buttonLink }: CardItemProps) {
  return (
    <div className="overflow-hidden rounded-2xl bg-[#62BB46] opacity-100 shadow-md hover:shadow-lg transition-shadow">
        <div className="p-6 text-left">
            <h2 className="my-1 text-md font-bold text-black">{title}</h2>
            <p className="text-sm font-semibold text-black">{address}</p>
            {buttonText && buttonLink && (
                <a
                    href={buttonLink}
                    target="_blank"
                    className="text-[#DCEAAB]"
                >
                    {buttonText}
                </a>
            )}
      </div>
    </div>
  )
}
