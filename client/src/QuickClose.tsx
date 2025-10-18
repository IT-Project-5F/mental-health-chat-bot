import { Button } from "./components/ui/button";

function QuickClose () {
    return (
        <Button
            onClick={() => window.location.href = "https://www.google.com/"}
            variant={"destructive"}
            size={"lg"}
        >
            Quick Close
        </Button>
    )
}

export default QuickClose;