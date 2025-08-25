type CardItemProps = {
  title: string
  address: string
  buttonText?: string
  buttonLink?: string
}

export function CardItem({ title, address, buttonText, buttonLink }: CardItemProps) {
  return (
    <div className="max-w-sm bg-[#62BB46] rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
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
