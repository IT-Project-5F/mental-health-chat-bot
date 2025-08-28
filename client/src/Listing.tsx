import { useState } from "react";
import { CardItem } from "./CardItem.tsx"


function Listing() {
    const [open, close] = useState(false)

    const cards = [
        {
            title: "13YARN",
            address: "Online Service",
            buttonText: "View Details",
            buttonLink: "https://www.13yarn.org.au/"
        },
        {
            title: "1800 My Options",
            address: "8/255 Bourke St, Melbourne VIC",
            buttonText: "View Details",
            buttonLink: "https://www.1800myoptions.org.au/"
        },
        {
            title: "Australian Psychology Society",
            address: "Level 11, 257 Collins Street",
            buttonText: "View Details",
            buttonLink: "https://psychology.org.au/find-a-psychologist"
        },
        {
            title: "Australian Psychology Society",
            address: "Level 11, 257 Collins Street",
            buttonText: "View Details",
            buttonLink: "https://psychology.org.au/find-a-psychologist"
        }
    ]
    return (
        <div className="relative inline-block">
            <div className="relative z-10 flex w-100 h-20 p-6 space-x-4 rounded-2xl bg-[#014532] items-center">
                <span className="relative w-8 h-8 group" onClick={() => close(!open)}>
                    <svg className={`${open ? 'hidden' : 'block'} absolute w-8 h-8`} viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 12.5L15 17.5L10 12.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <svg className={`${open ? 'block' : 'hidden'} absolute w-8 h-8`} viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10 17.5L15 12.5L20 17.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <svg className="absolute w-8 h-8 opacity-0 transition-opacity duration-200 group-hover:opacity-100" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 0.5C24.5604 0.5 31.5 7.43959 31.5 16C31.5 24.5604 24.5604 31.5 16 31.5C7.43959 31.5 0.5 24.5604 0.5 16C0.5 7.43959 7.43959 0.5 16 0.5Z" stroke="white" stroke-width="1"/>
                    </svg>
                </span>
                <h1 className="text-2xl font-bold text-white">Counsellor near Melbourne</h1>
            </div>
            {open && (
                <div className="overflow-y-auto z-0 max-h-134 pt-24 p-6 -mt-20 space-y-6 bg-[#DCEAAB] rounded-2xl">
                    {cards.map((card, index) => (
                        <CardItem key={index} {...card} />
                    ))}
                </div>
            )}
        </div>
    )
}

export default Listing;