import { Button } from "@/components/ui/button"
import { useState } from "react"
import ServiceForm, { type ServiceFormData } from "@/formComponents/service-form"
import { X } from "lucide-react"
import { request } from "@/api"


interface ServicePageProps {
    service: ServiceFormData;
    onClose?: () => void;
}

function ServicePage( { service, onClose }: ServicePageProps ) {
    const [loading, setLoading] = useState(false);

    // Convert api data to form data
    const apiToForm = (s: any): ServiceFormData => ({
        organisationName: s.organisation_name || "",
        campusName: s.campus_name || "",
        serviceName: s.service_name || "",
        regionName: s.region_name || "",
        email: s.email || "",
        phone: s.phone || "",
        website: s.website || "",

        address: s.address || "",
        suburb: s.suburb || "",
        state: s.state || "",
        postcode: s.postcode || "",

        notes: s.notes || "",
        expectedWaitTime: s.expected_wait_time || "",
        eligibilityAndDescription: s.eligibility_and_description || "",

        opHours: [
            ...(s.opening_hours_24_7 ? ['24/7'] : []),
            ...(s.opening_hours_standard ? ['Standard Hours'] : []),
            ...(s.opening_hours_extended ? ['Extended Hours'] : [])
        ],
        opHoursExtendedDetails: s.op_hours_extended_details || "",

        cost: s.cost ? s.cost.split(", ").filter((item: string) => item) : [],
        deliveryMethod: s.delivery_method ? s.delivery_method.split(", ").filter((item: string) => item) : [],
        levelOfCare: s.level_of_care ? s.level_of_care.split(", ").filter((item: string) => item) : [],
        referralPathway: s.referral_pathway ? s.referral_pathway.split(", ").filter((item: string) => item) : [],
        serviceType: s.service_type ? s.service_type.split(", ").filter((item: string) => item) : [],
        targetPopulation: s.target_population ? s.target_population.split(", ").filter((item: string) => item) : [],
        workforceType: s.workforce_type ? s.workforce_type.split(", ").filter((item: string) => item) : [],

        // Hidden fields
        service_campus_key: s.service_campus_key || ""
    })
    
    const handleSubmit = async (formData: ServiceFormData) => {
        // Helper to convert empty strings "" to null (for later database storage)
        const emptyToNull = (value: string) => value.trim() === "" ? null : value;
        const submissionData = {
            organisation_name: emptyToNull(formData.organisationName),
            campus_name: emptyToNull(formData.campusName),
            service_name: emptyToNull(formData.serviceName),
            region_name: emptyToNull(formData.regionName),
            email: emptyToNull(formData.email),
            phone: emptyToNull(formData.phone),
            website: emptyToNull(formData.website),

            address: emptyToNull(formData.address),
            suburb: emptyToNull(formData.suburb),
            state: emptyToNull(formData.state),
            postcode: emptyToNull(formData.postcode),
            
            notes: emptyToNull(formData.notes),
            expected_wait_time: emptyToNull(formData.expectedWaitTime),
            eligibility_and_description: emptyToNull(formData.eligibilityAndDescription),

            // Convert "opHours" array to boolean values for each of opHours247, opHoursStandard, opHoursExtended
            opening_hours_24_7: formData.opHours.includes('24/7'),
            opening_hours_standard: formData.opHours.includes('Standard Hours'),
            opening_hours_extended: formData.opHours.includes('Extended Hours'),
            op_hours_extended_details: emptyToNull(formData.opHoursExtendedDetails),
            
            // Required multi-select fields cannot be null, and they must be joined into a single string
            cost: formData.cost.join(", "),
            delivery_method: formData.deliveryMethod.join(", "),
            level_of_care: formData.levelOfCare.join(", "),
            referral_pathway: formData.referralPathway.join(", "),
            service_type: formData.serviceType.join(", "),
            target_population: formData.targetPopulation.join(", "),
            workforce_type: formData.workforceType.join(", ")
        };

        try {
            setLoading(true);
            
            const response = await request("PUT", `/api/database/${service.service_campus_key}`, submissionData);
            console.log('Service updated: ', response);
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
                initialData={apiToForm(service)}
                mode="edit"
                onSubmit={handleSubmit}
            />
            {/* Close Button. Does not save changes. */}
            {/* TODO: Additional action (e.g. Changes are not saved. Are you sure?) */}
            <Button
                onClick={onClose}
                disabled={loading}
                className="absolute top-0 right-0 m-4 p-2 border-1 border-transparent hover:bg-transparent hover:border-white rounded-full"
            >
                <X className="right-4 text-white cursor-pointer"/>
            </Button>
        </div>
    )
}


export default ServicePage;