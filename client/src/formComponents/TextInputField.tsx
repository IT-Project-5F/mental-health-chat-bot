/**
 * Form field that handles typed inputs from the Keyboard. 
 * The field value will be stored in formData[id] as a single string value.
 * Validation errors are displayed below the input box. 
 */

/* Types and Interfaces */
interface TextInputFieldProps {
    id: string;
    label: string;
    type?: string;
    placeholder?: string;
    formData: Record<string, any>;
    handleChange: (e: React.ChangeEvent<any>) => void;
    hasError: (field: string) => boolean;
    errors: Record<string, string>;
}

const TextInputField: React.FC<TextInputFieldProps> = ({ id, label, type = "text", placeholder, formData, handleChange, hasError, errors, ...props }) => {
  return (
    <div className="flex flex-col items-start w-full">
        <label htmlFor={id} className="m-2 text-[#CBDB2F] font-bold">{label}</label>
        <input
        type={type}
        id={id}
        placeholder={placeholder}
        value={formData[id] || ''}
        onChange={handleChange}
        className={`px-6 py-3 mb-2 w-full text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-3xl border-2 transition duration-300 ease-in-out ${
            hasError(id) ? 'border-red-500 ring-2 ring-red-500' : 'border-[#01563E] focus:ring-1 focus:ring-[#CBDB2F]'
        }`}
        {...props}
        />
        {hasError(id) && <p className="text-red-500 text-sm mt-1">{errors[id]}</p>}
    </div>
  );
};

export default TextInputField;