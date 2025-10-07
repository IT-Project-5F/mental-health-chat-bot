/**
 * Form field that handles selection of multiple options. 
 * The field value will be stored in formData[id] as an array of string values. 
 * Validation errors are displayed below the input box. 
 */

/* Types and Interfaces */
interface MultiSelectFieldProps {
    id: string;
    label: string;
    options: string[];
    formData: Record<string, any>;
    handleChange: (e: React.ChangeEvent<any>) => void;
    hasError: (field: string) => boolean;
    errors: Record<string, string>;
}

const MultiSelectField: React.FC<MultiSelectFieldProps> = ({ id, label, options, formData, handleChange, hasError, errors }) => {
  // Option to select or deselect all checkboxes for that specific question
  const allSelected = options.every(opt => formData[id]?.includes(opt));
  const selectAllBoxes = () => {
    const newValues = allSelected ? [] : options;

    const event = {
      target: {
        type: "checkbox",
        name: id,
        value: newValues,
        checked: !allSelected,
      },
    } as unknown as React.ChangeEvent<HTMLInputElement>;
    
    handleChange(event);
  };
  
  return (
    <div className="flex flex-col items-start w-full">
        <div className="flex items-center justify-between w-full">
          <label className="m-2 text-[#CBDB2F] font-bold">{label}</label>
          <button
            type="button"
            onClick={selectAllBoxes}
            className="text-sm text-gray-300 font-semibold underline"
          >
            {allSelected ? "Deselect All" : "Select All"}
          </button>
        </div>

        {/* Checkbox */}
        <div className="flex flex-wrap w-full gap-2">
        {options.map((option) => (
            <label key={option} className="flex items-center text-[#014532] font-bold bg-[#DCEAAB] px-4 py-2 rounded-full border-2 border-[#01563E] cursor-pointer">
            <input
                type="checkbox"
                name={id}
                value={option}
                checked={formData[id]?.includes(option)}
                onChange={handleChange}
                className="mr-2 accent-[#01563E]"
            />
            {option}
            </label>
        ))}
        </div>
        {hasError(id) && <p className="text-red-500 text-sm mt-1">{errors[id]}</p>}
    </div>
  );
};

export default MultiSelectField;