import { useState } from 'react';
import TextInputField from './TextInputField';
import MultiSelectField from './MultiSelectField';
import { expectedWaitTimeOptions, costOptions, deliveryMethodOptions, levelOfCareOptions, referralPathwayOptions, 
    serviceTypeOptions, targetPopulationOptions, workforceTypeOptions } from './serviceFormOptions.ts' ;
import { request } from '../api.ts'

/* Interface */
interface ServiceFormData {
    organisationName: string;
    campusName: string;
    serviceName: string;
    regionName: string;
    email: string;
    phone: string;
    website: string;
    address: string;
    suburb: string;
    state: string;
    postcode: string;
    notes: string;
    expectedWaitTime: string;
    eligibilityAndDescription: string;
    opHours: string[];
    opHoursExtendedDetails: string;
    cost: string[];
    deliveryMethod: string[];
    levelOfCare: string[];
    referralPathway: string[];
    serviceType: string[];
    targetPopulation: string[];
    workforceType: string[];
    [key: string]: any;
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
const ServiceCreationForm: React.FC = () => {
    const [formData, setFormData] = useState<ServiceFormData>({
        organisationName: '',
        campusName: '',
        serviceName: '',
        regionName: '',
        email: '',
        phone: '',
        website: '',
        address: '',
        suburb: '',
        state: '',
        postcode: '',
        notes: '',
        expectedWaitTime: '',
        eligibilityAndDescription: '',
        opHours: [], // Holds strings to represent opHours247, opHoursStandard, opHoursExtended
        opHoursExtendedDetails: '',
        cost: [],
        deliveryMethod: [],
        levelOfCare: [],
        referralPathway: [],
        serviceType: [],
        targetPopulation: [],
        workforceType: []
    });

    // State for form validation errors; Name of the field is the key
    const [errors, setErrors] = useState<{ [key: string]: string }>({});


    /* Functions */
    // Function to handle changes to all form input fields (text input or multi select)
    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { id, value, type, name } = e.target;
        const fieldName = name || id;

        // Handle checkbox array values (for Select All / Deselect All)
        if (Array.isArray(value)) {
            setFormData(prev => ({
                ...prev,
                [fieldName]: value
            }));

            // Clear extended details if the "Extended Hours" checkbox was deselected
            if (fieldName === 'opHours' && !value.includes('Extended Hours')) {
                setFormData(prev => ({
                    ...prev,
                    opHoursExtendedDetails: ''
                }));
            }
            return;
        }

        // Handle changes to checkbox when selected 
        if (type === 'checkbox') {
            const input = e.target as HTMLInputElement; 
            const fieldName = name || id;

            // Add or remove checkbox value when checked or unchecked
            setFormData(prev => {
                const currentValues: string[] = prev[fieldName] || [];
                const updatedValues = input.checked
                    ? [...currentValues, value]
                    : currentValues.filter(v => v !== value);

                const updatedFormData = {
                    ...prev,
                    [fieldName]: updatedValues
                };


                // If "Extended Hours" checkbox for the "opHours" field was deselected, clear the text input for "opHoursExtendedDetails"
                if (fieldName === 'opHours' && !updatedValues.includes('Extended Hours')) {
                    updatedFormData.opHoursExtendedDetails = '';
                }

                return updatedFormData;
            });
            return;
        }

        // Update the form data for text inputs
        setFormData(prev => ({
            ...prev,
            [id]: value
        }));
    };


    // Function to handle form submission and ensure data is in a suitable format for record creation in database
    const handleFormSubmission = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        // Define required fields that must be filled out before submission
        const requiredFields = [
            'organisationName', 'serviceName', 'campusName', 'regionName', 'email', 'phone', 
            'expectedWaitTime', 'opHours', 'cost', 'deliveryMethod', 'levelOfCare', 
            'referralPathway', 'serviceType', 'targetPopulation', 'workforceType'
        ];
    
        // Create an errors object to store validation error messages
        const newErrors: { [key: string]: string } = {};

        // Check each required field. If field is empty, add an error message
        requiredFields.forEach(field => {
            const fieldValue = formData[field];
            if (Array.isArray(fieldValue)) {
                if (fieldValue.length === 0) {
                newErrors[field] = 'This field is required.';
                }
            } else if (!fieldValue) {
                newErrors[field] = 'This field is required.';
            }
        });

        // Handle conditional validation for "opHoursExtendedDetails" when "Extended Hours" checkbox is checked
        if (formData.opHours.includes('Extended Hours') && !formData.opHoursExtendedDetails) {
            newErrors.opHoursExtendedDetails = 'Details for Extended Hours are required.';
        }

        setErrors(newErrors);

        // Prevent submission if any errors exist
        if (Object.keys(newErrors).length > 0) {
            return;
        }

        // Helper to convert empty strings "" to null (for later database storage)
        const emptyToNull = (value: string) => value.trim() === "" ? null : value;

        /* Transform fields to format specified by database update API endpoint */
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

            // Reset form fields
            setFormData({
                organisationName: '',
                campusName: '',
                serviceName: '',
                regionName: '',
                email: '',
                phone: '',
                website: '',
                address: '',
                suburb: '',
                state: '',
                postcode: '',
                notes: '',
                expectedWaitTime: '',
                eligibilityAndDescription: '',
                opHours: [],
                opHoursExtendedDetails: '',
                cost: [],
                deliveryMethod: [],
                levelOfCare: [],
                referralPathway: [],
                serviceType: [],
                targetPopulation: [],
                workforceType: [] 
            })
        } catch (e) {
            console.error('Error saving service:', e);
        }
    };

    // Helper function to check if a field has an error
    const hasError = (field: keyof ServiceFormData): boolean => !!errors[field];

    /* Rendering and Styling */
    return (
        <div className="absolute w-screen h-screen bg-[#014532] inset-0 overflow-auto py-10">
        <form onSubmit={handleFormSubmission} className="flex flex-col items-center justify-center p-4">
            <h1 className="p-2 sm:p-6 text-lg sm:text-3xl font-bold text-[#CBDB2F]">Submit a New Service</h1>

            {/* General Information */}
            <h2 className="text-[#CBDB2F] font-bold text-xl mt-8 mb-4">General Information</h2>
            <div className="w-full max-w-lg space-y-4">
            <TextInputField id="organisationName" label="Organisation Name" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            <TextInputField id="campusName" label="Campus Name" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            <TextInputField id="serviceName" label="Service Name" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            <TextInputField id="regionName" label="Region Name" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>

            {/* Contact and Location */}
            <h2 className="text-[#CBDB2F] font-bold text-xl mt-8 mb-4">Contact and Location</h2>
            <div className="flex flex-col sm:flex-row flex-wrap justify-between w-full max-w-lg gap-4">
            <div className="w-full sm:w-[calc(50%-0.5rem)]">
                <TextInputField id="email" label="Email" type="email" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full sm:w-[calc(50%-0.5rem)]">
                <TextInputField id="phone" label="Phone" type="tel" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <TextInputField id="website" label="Website" type="url" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <TextInputField id="address" label="Address" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full sm:w-[calc(50%-0.5rem)]">
                <TextInputField id="suburb" label="Suburb" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full sm:w-[calc(50%-0.5rem)]">
                <TextInputField id="state" label="State" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <TextInputField id="postcode" label="Postcode" placeholder="" formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            </div>

            {/* Service Description */}
            <h2 className="text-[#CBDB2F] font-bold text-xl mt-8 mb-4">Service Description</h2>
            <div className="w-full max-w-lg space-y-4">
            <div className="flex flex-col items-start w-full">
                <label htmlFor="notes" className="m-2 text-[#CBDB2F] font-bold">Notes</label>
                <textarea
                id="notes"
                placeholder="Any additional notes about the service..."
                rows={4}
                value={formData.notes}
                onChange={handleChange}
                className="px-6 py-3 mb-2 w-full text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-3xl border-2 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-[#CBDB2F] transition duration-300 ease-in-out resize-none"
                />
            </div>
            <div className="flex flex-col items-start w-full">
                <label htmlFor="expectedWaitTime" className="m-2 text-[#CBDB2F] font-bold">Expected Wait Time</label>
                <select
                    id="expectedWaitTime"
                    value={formData.expectedWaitTime}
                    onChange={handleChange}
                    className={`px-6 py-3 mb-2 w-full text-[#014532] font-bold bg-white rounded-3xl border-2 transition duration-300 ease-in-out ${
                    hasError('expectedWaitTime') ? 'border-red-500 ring-2 ring-red-500' : 'border-[#01563E] focus:ring-1 focus:ring-[#CBDB2F]'
                    }`}
                >
                    <option value="">Select an option...</option>
                    {expectedWaitTimeOptions.map(option => (
                        <option key={option} value={option}>{option}</option>
                    ))}
                </select>
                {hasError('expectedWaitTime') && (
                <p className="text-red-500 text-sm mt-1">{errors.expectedWaitTime}</p>
                )}
            </div>
            <div className="flex flex-col items-start w-full">
                <label htmlFor="eligibilityAndDescription" className="m-2 text-[#CBDB2F] font-bold">Eligibility & Description</label>
                <textarea
                id="eligibilityAndDescription"
                placeholder="Who is eligible and a detailed description of the service..."
                rows={4}
                value={formData.eligibilityAndDescription}
                onChange={handleChange}
                className={`px-6 py-3 mb-2 w-full text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-3xl border-2 transition duration-300 ease-in-out ${
                    hasError('eligibilityAndDescription') ? 'border-red-500 ring-2 ring-red-500' : 'border-[#01563E] focus:ring-1 focus:ring-[#CBDB2F]'
                } resize-none`}
                />
                {hasError('eligibilityAndDescription') && (
                <p className="text-red-500 text-sm mt-1">{errors.eligibilityAndDescription}</p>
                )}
            </div>
            </div>

            {/* Operating Hours */}
            <h2 className="text-[#CBDB2F] font-bold text-xl mt-8 mb-2">Operating Hours</h2>
            <div className="flex flex-col items-start w-full max-w-lg space-y-2">
                {/* MultiSelectField component to allow multiple selections */}
                <MultiSelectField
                    id="opHours"
                    label="Operating Hours"
                    options={['24/7', 'Standard Hours', 'Extended Hours']}
                    formData={formData}
                    handleChange={handleChange}
                    hasError={hasError}
                    errors={errors}
                />
                {/* The extended details field only shows up if 'Extended Hours' is selected in the "opHours" array */}
                {formData.opHours.includes('Extended Hours') && (
                    <TextInputField
                        id="opHoursExtendedDetails"
                        label="Extended Hours Details"
                        placeholder="Extended hours details"
                        formData={formData}
                        handleChange={handleChange}
                        hasError={hasError}
                        errors={errors}
                    />
                )}
            </div>

            {/* Service Categorisation */}
            <h2 className="text-[#CBDB2F] font-bold text-xl mt-8 mb-2">Service Categorisation</h2>
            <div className="flex flex-col sm:flex-row flex-wrap justify-between w-full max-w-lg gap-4">
            <div className="w-full">
                <MultiSelectField id="cost" label="Cost" options={costOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <MultiSelectField id="deliveryMethod" label="Delivery Method" options={deliveryMethodOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <MultiSelectField id="levelOfCare" label="Level of Care" options={levelOfCareOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <MultiSelectField id="referralPathway" label="Referral Pathway" options={referralPathwayOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <MultiSelectField id="serviceType" label="Service Type" options={serviceTypeOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <MultiSelectField id="targetPopulation" label="Target Population" options={targetPopulationOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            <div className="w-full">
                <MultiSelectField id="workforceType" label="Workforce Type" options={workforceTypeOptions} formData={formData} handleChange={handleChange} hasError={hasError} errors={errors} />
            </div>
            </div>

            {/* Submit Button */}
            <div className="flex flex-col m-2 mt-8 sm:m-6 text-sm sm:text-lg">
            <button type="submit" className="px-8 sm:px-10 py-2 m-2 font-bold text-[#014532] bg-[#CBDB2F] rounded-3xl hover:bg-[#62BB46] hover:scale-105 duration-150">Submit</button>
            </div>
        </form>
        </div>
    );
};

export default ServiceCreationForm;