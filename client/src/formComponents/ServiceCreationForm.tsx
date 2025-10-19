import { request } from '../api.ts'
import ServiceForm from './service-form.tsx';
import type { ServiceFormData } from './service-form.tsx';

interface ServiceCreationFormProps {
    onSuccess?: () => void;
}


/* Form is only accessible to verified emails belonging to Healthcare Professionals.
   When requested, form will pop up for healthcare professionals to fill out to create a new service in the database. 
    Fields:
     * organisation_name,campus_name,service_name,region_name,
     * email,phone,website,
     * notes,expected_wait_time,
     * opening_hours_24_7,opening_hours_standard,opening_hours_extended,op_hours_extended_details,
     * address,suburb,state,postcode,
     * cost,delivery_method,level_of_care,referral_pathway,service_type,target_population,workforce_type
    */
const ServiceCreationForm: React.FC<ServiceCreationFormProps> = ({ onSuccess }) => {

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

        /* Request to create a new database record with the update database API endpoint */
        try {
            const response = await request('POST', '/api/database', submissionData);
            console.log('Saved new service:', response);
            if (onSuccess) {
                onSuccess();
            }
        } catch (e) { 
            console.error('Error saving service:', e);
        }
    };

    /* Rendering and Styling */
    return (
        <div className="w-full h-full">
            <ServiceForm
                mode="create"
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default ServiceCreationForm;