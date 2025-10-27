import { Button } from "@/components/ui/button";
import { X } from "lucide-react";
import ServiceCreationForm from "@/formComponents/ServiceCreationForm";

interface ServiceCreationPageProps {
    onClose?: () => void;
}

function ServiceCreationPage( { onClose }: ServiceCreationPageProps) {
    return (
        <div className="relative top-0 inset-0">
            <ServiceCreationForm onSuccess={onClose} />

            <Button
                onClick={onClose}
                variant={"ghost"}
                size={"icon"}
                className="absolute top-0 right-0 m-4 p-2"
            >
                <X className="text-white cursor-pointer" />
            </Button>
        </div>
    )
}

export default ServiceCreationPage;