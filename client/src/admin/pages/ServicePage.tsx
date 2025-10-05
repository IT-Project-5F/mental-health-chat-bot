import { Button } from "@/components/ui/button"

export type FullService = {
    organisation_name: string
    campus_name?: string,
    service_name: string
    region_name?: string,
    email: string
    phone: string,
    website: string
    notes?: string,
    expected_wait_time?: string,
    opening_hours_24_7?: boolean,
    opening_hours_standard?: boolean,
    opening_hours_extended?: boolean,
    op_hours_extended_details?: string,
    address?: string,
    suburb?: string,
    state?: "VIC" | "NSW" | "QLD" | "SA" | "WA" | "TAS" | "NT" | "ACT",
    postcode?: string,
    cost?: string,
    delivery_method?: string,
    level_of_care?: string,
    referral_pathway?: string,
    service_type?: string,
    target_population?: string,
    workforce_type?: string,
}

function ServicePage( { service, onClose }: { service: FullService, onClose?: () => void } ) {
    return (
        <div>
            <h1>{service.service_name}</h1>
            {service.notes && <p>{service.notes}</p>}
            <p>Organisation: {service.organisation_name}</p>
            <p>Email: {service.email}</p>
            <p>Phone: {service.phone}</p>
            <p>Website: {service.website}</p>
            {service.address && <p>Address: {service.address},</p>}
            {service.suburb && <p>{service.suburb},</p>}
            {service.state && <p>State: {service.state} </p>}
            {service.postcode && <p>{service.postcode}</p>}
            <Button onClick={onClose}>Close</Button>
        </div>
    );
}

export default ServicePage;