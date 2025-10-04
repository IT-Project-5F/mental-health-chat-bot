// Backend API
const BaseApiURL = "http://localhost:5001";

/**
 * Helper Function that acts as a wrapper for HTTP Requests.
 * Returns a JSON object.
 * 
 * Arguments:
 *  - method: HTTP method ("GET", "POST")
 *  - path: The specific API endpoint path
 *  - data: Optional object containing data to be sent with the HTTP request. Default is null.
 */
export const request = async(
    method: string,
    path: string,
    data: object | null = null,
    parseAsJson: boolean = true,
    contentType: "json" | "form" = "json" // default to JSON
) => {

    // Retrieve the token from local storage if it exists
    const token = localStorage.getItem("access_token");

    // Initialize headers and body for the fetch call
    let headers: Record<string, string> = {};
    let body: string | undefined;

    // Set headers and body based on content type
    if (contentType === "form" && data) {
        headers["Content-Type"] = "application/x-www-form-urlencoded";
        const formData = new URLSearchParams();
        for (const [key, value] of Object.entries(data)) {
            formData.append(key, String(value));
        }
        body = formData.toString();
    } else if (contentType === "json") {
        headers["Content-Type"] = "application/json";
        body = data ? JSON.stringify(data) : undefined;
    }

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    // Create an options object for the fetch call to allow configuration of request
    const options: RequestInit = {
        method,
        headers,
        body,
    };

    // Making requests to backend API and handling of responses
    try {
        const response = await fetch(BaseApiURL + path, options);
        
        // Case: Encountered API error when waiting for response
        if (!response.ok) {
            const errorText = await response.text();
            return { requestError: true, status: response.status, message: errorText };
        }

        // Case: Successful response with an empty body
        if (response.status == 204) {
            return (parseAsJson) ? { success: true } : "";
        }
        
        // Read response body as plaintext before parsing it as JSON
        const text = await response.text();
        if (parseAsJson == false) {
            return text.trim();
        }

        // Case: Successful response with empty body, no parsing required
        if (response.status == 200 && text.trim() == "") {
            return { success: true };
        }

        // Parse text as a JSON object
        try {
            return JSON.parse(text);
        } 
        catch (e) {
            return { requestError: true, status: 500, message: "Failed to parse JSON response"};
        }
    }
    catch (error: any) {
        return { requestError: true, status: 500, message: error.message };
    }
};