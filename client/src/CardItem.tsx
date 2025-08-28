type CardItemProps = {
  title: string
  address: string
  buttonText?: string
  buttonLink?: string
}

export function CardItem({ title, address, buttonText, buttonLink }: CardItemProps) {
  return (
    <div className="overflow-hidden max-w-sm rounded-2xl bg-[#62BB46] shadow-md hover:shadow-lg transition-shadow">
        <div className="p-6 text-left">
            <h2 className="text-sm font-semibold text-black">{title}</h2>
            <p className="text-black mt-2">{address}</p>
            {buttonText && buttonLink && (
                <a
                    href={buttonLink}
                    target="_blank"
                >
                    {buttonText}
                </a>
            )}
      </div>
    </div>
  )
}
