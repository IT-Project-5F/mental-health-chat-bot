import { Button } from "@/components/ui/button"
import { useState } from "react"
import ServiceForm from "@/formComponents/service-form"
import type { ServiceFormData } from "@/formComponents/service-form"
import { X } from "lucide-react"
import { request } from "@/api"


interface ServicePageProps {
    service: ServiceFormData;
    onClose?: () => void;
}

function ServicePage( { service, onClose }: ServicePageProps ) {
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (formData: ServiceFormData) => {
        try {
            setLoading(true);
            // Prepare the data to be submitted
            const submissionData = {
                organisation_name: formData.organisationName,
                campus_name: formData.campusName,
                service_name: formData.serviceName,
                region_name: formData.regionName,
                email: formData.email,
                phone: formData.phone,
                website: formData.website,

                address: formData.address,
                suburb: formData.suburb,
                state: formData.state,
                postcode: formData.postcode,
                
                notes: formData.notes,
                expected_wait_time: formData.expectedWaitTime,
                eligibility_and_description: formData.eligibilityAndDescription,

                // Convert "opHours" array to boolean values for each of opHours247, opHoursStandard, opHoursExtended
                opening_hours_24_7: formData.opHours.includes('24/7'),
                opening_hours_standard: formData.opHours.includes('Standard Hours'),
                opening_hours_extended: formData.opHours.includes('Extended Hours'),
                op_hours_extended_details: formData.opHoursExtendedDetails,
                
                // Required multi-select fields cannot be null, and they must be joined into a single string
                cost: formData.cost.join(", "),
                delivery_method: formData.deliveryMethod.join(", "),
                level_of_care: formData.levelOfCare.join(", "),
                referral_pathway: formData.referralPathway.join(", "),
                service_type: formData.serviceType.join(", "),
                target_population: formData.targetPopulation.join(", "),
                workforce_type: formData.workforceType.join(", ")
            };

            const response = await request("PUT", `/api/database/${service.service_campus_key}`, submissionData);
            console.log('Saved new service:', response);
        } catch (error) {
            console.error("Error saving service: ", error);
            alert("An error occurred while editing the service. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="relative top-0 inset-0">
            <ServiceForm
                initialData={service}
                mode="edit"
                onSubmit={handleSubmit}
            />
            <Button
                onClick={onClose}
                disabled={loading}
                className="absolute top-0 right-0 m-4 p-2 border-1 border-transparent hover:bg-transparent hover:border-white rounded-full"
            >
                <X className="right-4 text-white cursor-pointer"/>
            </Button>
            {/* <div className="flex justify-end mt-4">
                <Button
                    variant="outline"
                    onClick={onClose}
                    disabled={loading}
                >
                    Close
                </Button>
            </div> */}
        </div>
    )
}


export default ServicePage;