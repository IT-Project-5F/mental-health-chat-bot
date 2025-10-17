import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-3xl text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-[#CBDB2F] text-[#01563E] hover:bg-[#62BB46]",
        destructive:
          "bg-[#FDB4C6] text-[#01563E] hover:bg-[#FFDBE4]",
        outline:
          "border border-[#014532] bg-background-transparent hover:bg-[#014532] hover:text-[#CBDB2F]",
        secondary:
          "bg-[#01563E] text-[#CBDB2F] hover:bg-[#CBDB2F] hover:text-[#01563E]",
        tertiary:
          "bg-[#62BB46] text-[#014532] hover:bg-[#014532] hover:text-[#62BB46]",
        ghost: "hover:border hover:border-white hover:text-white",
        ghostdark: "hover:border hover:border-[#014532] hover:text-[#014532]",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3 text-xs",
        lg: "h-10 px-8",
        xl: "h-11 px-8 text-lg",
        icon: "h-8 w-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
