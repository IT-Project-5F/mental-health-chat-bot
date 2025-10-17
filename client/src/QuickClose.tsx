import { useNavigate } from "react-router-dom";
import { Button } from "./components/ui/button";

function QuickClose () {
    const navigate = useNavigate();
    return (
        <Button
            onClick={() => navigate("https://www.google.com/")}
            variant={"destructive"}
            size={"lg"}
        >
            Quick Close
        </Button>
    )
}

export default QuickClose;