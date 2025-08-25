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
        }
    ]
    return (
        <div>
            <button
                className="relative flex p-4 item-center bg-[#014532] group"
                onClick={() => close(!open)}
            >
                <svg className="w-6 h-6" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 12.5L15 17.5L10 12.5" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 13.5L16 18.5L11 13.5" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M16 0.5C24.5604 0.5 31.5 7.43959 31.5 16C31.5 24.5604 24.5604 31.5 16 31.5C7.43959 31.5 0.5 24.5604 0.5 16C0.5 7.43959 7.43959 0.5 16 0.5Z" stroke="black"/>
                </svg>

                <span>Counsellor near Melbourne</span>
            </button>
            {open && (
                <div className="space-y-6 p-6 bg-[#DCEAAB]">
                    {cards.map((card, index) => (
                        <CardItem key={index} {...card} />
                    ))}
                </div>
            )}
        </div>
    )
}

export default Listing;