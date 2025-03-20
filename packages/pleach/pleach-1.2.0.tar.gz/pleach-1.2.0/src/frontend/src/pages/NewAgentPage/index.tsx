import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { ChevronRight } from "lucide-react";
import React, { ChangeEvent, FormEvent, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../../components/ui/button";
import OnboardingImage from "../../mosaic/images/flow-page-1.jpg";

interface FormDataType {
  // Step 1
  flowName: string;
  flowDescription: string;
  projectType: string;

  // Step 2
  inputType: string;

  // Step 3
  needPrompt: boolean;
  systemPrompt: string;

  // Step 4
  llmType: string;

  // Step 5
  outputType: string;

  // Additional properties that were missing
  useMemory: boolean;
  useDatasource: boolean;
}

interface FlowNodeType {
  id: string;
  type: string;
  position: {
    x: number;
    y: number;
  };
  data: {
    node: {
      template: Record<string, any>;
      description: string;
    };
  };
}

interface FlowEdgeType {
  source: string;
  target: string;
  id: string;
}

interface FlowObjectType {
  name: string;
  description: string;
  data: {
    nodes: FlowNodeType[];
    edges: FlowEdgeType[];
  };
}

const DynamicFlowStepper = () => {
  const navigate = useCustomNavigate();

  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<FormDataType>({
    // Step 1
    flowName: '',
    flowDescription: '',
    projectType: '',
    
    // Step 2
    inputType: 'chatInput',
    
    // Step 3
    needPrompt: false,
    systemPrompt: '',
    
    // Step 4
    llmType: 'bedrock',
    
    // Step 5
    outputType: 'chatOutput',
    
    // Additional properties
    useMemory: false,
    useDatasource: false,
  });

  const totalSteps = 6;

  // Project types for dropdown
  const projectTypes = ['Banking', 'Health', 'IT'];
  
  // Input types for radio
  const inputTypes = [
    { id: 'chatInput', label: 'Chat Input', description: 'Interactive chat interface for user inputs' },
    { id: 'textInput', label: 'Text Input', description: 'Simple text field for user inputs' },
  ];
  
  // LLM types for radio
  const llmTypes = [
    { id: 'bedrock', label: 'Amazon Bedrock', description: 'AWS Bedrock powered by Claude and other models' },
    { id: 'openai', label: 'OpenAI GPT', description: 'Powerful GPT models from OpenAI' },
    { id: 'anthropic', label: 'Anthropic Claude', description: 'Claude models directly from Anthropic' },
    { id: 'meta', label: 'Meta Llama', description: 'Open source Llama models from Meta' },
  ];
  
  // Output types for radio
  const outputTypes = [
    { id: 'chatOutput', label: 'Chat Output', description: 'Conversational response format' },
    { id: 'textOutput', label: 'Text Output', description: 'Plain text response format' },
  ];

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleRadioChange = (name: string, value: string | boolean) => {
    setFormData({
      ...formData,
      [name]: value === 'true' ? true : value === 'false' ? false : value
    });
  };

  const nextStep = () => {
    setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    setCurrentStep(currentStep - 1);
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Create a flow object similar to the sample JSON
    const flowObject: FlowObjectType = {
      name: formData.flowName,
      description: formData.flowDescription,
      data: {
        nodes: [
          {
            id: `${formData.inputType}-node`,
            type: "genericNode",
            position: { x: 0, y: 0 },
            data: {
              node: {
                template: {},
                description: `${formData.inputType === 'chatInput' ? 'Get chat inputs from the Playground.' : 'Get text input from the Playground.'}`,
              }
            }
          }
        ],
        edges: []
      }
    };
    
    // Add prompt node if needed
    if (formData.needPrompt) {
      flowObject.data.nodes.push({
        id: "Prompt-node",
        type: "genericNode",
        position: { x: 50, y: 300 },
        data: {
          node: {
            template: {
              template: {
                value: formData.systemPrompt
              }
            },
            description: "Create a prompt template with dynamic variables."
          }
        }
      });
      
      // Add an edge connecting prompt to LLM
      flowObject.data.edges.push({
        source: "Prompt-node",
        target: `${formData.llmType}-node`,
        id: `edge-prompt-llm`
      });
    }
    
    // Add LLM node
    flowObject.data.nodes.push({
      id: `${formData.llmType}-node`,
      type: "genericNode",
      position: { x: 400, y: 0 },
      data: {
        node: {
          template: {},
          description: `Generate text using ${formData.llmType}.`
        }
      }
    });
    
    // Add output node
    flowObject.data.nodes.push({
      id: `${formData.outputType}-node`,
      type: "genericNode",
      position: { x: 800, y: 200 },
      data: {
        node: {
          template: {},
          description: `Display a ${formData.outputType === 'chatOutput' ? 'chat' : 'text'} message in the Playground.`
        }
      }
    });
    
    // Add basic connections
    flowObject.data.edges.push(
      {
        source: `${formData.inputType}-node`,
        target: `${formData.llmType}-node`,
        id: `edge-input-llm`
      },
      {
        source: `${formData.llmType}-node`,
        target: `${formData.outputType}-node`,
        id: `edge-llm-output`
      }
    );
    
    // Display the final object
    console.log('Flow configuration object:', flowObject);
    console.log('Form data collected:', formData);
    
    // Detailed logging of what will be created
    console.log(`Creating a flow with ${flowObject.data.nodes.length} nodes and ${flowObject.data.edges.length} edges`);
    console.log(`Input type: ${formData.inputType}, Output type: ${formData.outputType}, LLM: ${formData.llmType}`);
    console.log(`Using prompt: ${formData.needPrompt}, System prompt: ${formData.systemPrompt}`);
    
    // Use the navigate function from the hook to redirect
    navigate('/flow/0273926e-e261-4e42-b937-76e1f16eb7d5/folder/1974a1a2-be35-4ded-8996-e53f8e556e5e');
  };

  // Button component to match UI requirements
  const Button = ({ 
    children, 
    className = "", 
    variant = "primary", 
    type = "button", 
    onClick = () => {},
    disabled = false
  }: { 
    children: React.ReactNode; 
    className?: string; 
    variant?: "primary" | "outline" | "secondary"; 
    type?: "button" | "submit"; 
    onClick?: () => void;
    disabled?: boolean;
  }) => {
    const baseClasses = "px-4 py-2 rounded-md font-medium focus:outline-none transition-colors";
    const variantClasses = {
      primary: "bg-violet-500 text-white hover:bg-violet-600",
      outline: "border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800",
      secondary: "bg-gray-100 text-gray-800 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
    };
    
    return (
      <button 
        type={type} 
        className={`${baseClasses} ${variantClasses[variant]} ${className}`}
        onClick={onClick}
        disabled={disabled}
      >
        {children}
      </button>
    );
  };

  // Radio option component for consistent styling
  const RadioOption = ({ 
    id, 
    name, 
    label, 
    description, 
    checked, 
    onChange,
    icon
  }: { 
    id: string; 
    name: string; 
    label: string; 
    description: string;
    checked: boolean;
    onChange: () => void;
    icon?: React.ReactNode;
  }) => {
    return (
      <label className="relative block cursor-pointer mb-3">
        <input 
          type="radio" 
          id={id} 
          name={name} 
          className="peer sr-only" 
          checked={checked} 
          onChange={onChange}
        />
        <div className="flex items-center bg-white text-sm font-medium text-gray-800 dark:text-gray-100 p-4 rounded-lg dark:bg-gray-800 border border-gray-200 dark:border-gray-700/60 hover:border-gray-300 dark:hover:border-gray-600 shadow-xs transition">
          {icon || (
            <svg className="w-6 h-6 shrink-0 fill-current mr-4" viewBox="0 0 24 24">
              <path className="text-violet-500" d="m12 10.856 9-5-8.514-4.73a1 1 0 0 0-.972 0L3 5.856l9 5Z" />
              <path className="text-violet-300" d="m11 12.588-9-5V18a1 1 0 0 0 .514.874L11 23.588v-11Z" />
              <path className="text-violet-200" d="M13 12.588v11l8.486-4.714A1 1 0 0 0 22 18V7.589l-9 4.999Z" />
            </svg>
          )}
          <div>
            <span className="block">{label}</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">{description}</span>
          </div>
        </div>
        <div
          className="absolute inset-0 border-2 border-transparent peer-checked:border-violet-400 dark:peer-checked:border-violet-500 rounded-lg pointer-events-none"
          aria-hidden="true"
        ></div>
      </label>
    );
  };


  return (
    <div className="flex h-full w-full flex-col">
      <div className="flex h-full w-full overflow-hidden">
        {/* Content */}
        <div className="h-full w-full overflow-auto md:w-3/4">
          <div className="flex min-h-full flex-col">
            <div className="flex-4">
              {/* Progress bar */}
              <div className="px-4 pb-8 pt-12">
                <div className="mx-auto w-full max-w-md">
                  <div className="relative">
                    <div
                      className="absolute left-0 top-1/2 -mt-px h-0.5 w-full bg-gray-200 dark:bg-gray-700/60"
                      aria-hidden="true"
                    ></div>
                    <ul className="relative flex w-full justify-between">
                    {[1, 2, 3, 4, 5, 6].map((step) => (
                        <li key={step}>
                          <button
                            onClick={() => step <= currentStep && setCurrentStep(step)}
                            className={`flex items-center justify-center w-6 h-6 rounded-full text-xs font-semibold ${
                              currentStep >= step
                                ? 'bg-violet-500 text-white'
                                : 'bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-400'
                            }`}
                          >
                            {step}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className="px-4 py-8">
              <div className="mx-auto max-w-md">
                <form onSubmit={handleSubmit}>
                  {/* Step 1: Flow Information */}
                  {currentStep === 1 && (
                    <>
                      <h1 className="mb-6 text-3xl font-bold text-gray-800 dark:text-gray-100">
                        Flow Information
                      </h1>

                      <div className="mb-8 space-y-4">
                        <div>
                          <label
                            className="mb-1 block text-sm font-medium"
                            htmlFor="flow-name"
                          >
                            Flow Name <span className="text-red-500">*</span>
                          </label>
                          <input
                            id="flow-name"
                            name="flowName"
                            className="form-input w-full rounded-lg border border-gray-300 p-2 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            type="text"
                            required
                            value={formData.flowName}
                            onChange={handleChange}
                          />
                        </div>

                        <div>
                          <label
                            className="mb-1 block text-sm font-medium"
                            htmlFor="flow-description"
                          >
                            Flow Description{" "}
                            <span className="text-red-500">*</span>
                          </label>
                          <textarea
                            id="flow-description"
                            name="flowDescription"
                            className="form-input w-full rounded-lg border border-gray-300 p-2 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            rows={3}
                            required
                            value={formData.flowDescription}
                            onChange={handleChange}
                          />
                        </div>

                        <div>
                          <label
                            className="mb-1 block text-sm font-medium"
                            htmlFor="project-type"
                          >
                            Project Type <span className="text-red-500">*</span>
                          </label>
                          <select
                            id="project-type"
                            name="projectType"
                            className="form-select w-full rounded-lg border border-gray-300 p-2 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            required
                            value={formData.projectType}
                            onChange={handleChange}
                          >
                            <option value="">Select a project type</option>
                            {projectTypes.map((type) => (
                              <option key={type} value={type}>
                                {type}
                              </option>
                            ))}
                          </select>
                        </div>
                      </div>
                    </>
                  )}

                  {/* Step 2: Input Type Selection */}
                  {currentStep === 2 && (
                    <>
                      <h1 className="mb-6 text-3xl font-bold text-gray-800 dark:text-gray-100">
                        Select Input Type
                      </h1>

                      <div className="mb-8 space-y-3">
                        {inputTypes.map((type) => (
                          <RadioOption
                            key={type.id}
                            id={type.id}
                            name="inputType"
                            label={type.label}
                            description={type.description}
                            checked={formData.inputType === type.id}
                            onChange={() =>
                              handleRadioChange("inputType", type.id)
                            }
                          />
                        ))}
                      </div>
                    </>
                  )}

                  {/* Step 3: Prompt Configuration */}
                  {currentStep === 3 && (
                    <>
                      <h1 className="mb-6 text-3xl font-bold text-gray-800 dark:text-gray-100">
                        Prompt Configuration
                      </h1>

                      <div className="mb-8 space-y-6">
                        <div>
                          <label className="mb-3 block text-sm font-medium">
                            Do you need a system prompt?
                          </label>
                          <div className="space-y-3">
                            <RadioOption
                              id="prompt-yes"
                              name="needPrompt"
                              label="Yes, I need a system prompt"
                              description="Define behavior and capabilities with a system prompt"
                              checked={formData.needPrompt === true}
                              onChange={() =>
                                handleRadioChange("needPrompt", "true")
                              }
                            />
                            <RadioOption
                              id="prompt-no"
                              name="needPrompt"
                              label="No, I don't need a system prompt"
                              description="Use default model behavior without a custom prompt"
                              checked={formData.needPrompt === false}
                              onChange={() =>
                                handleRadioChange("needPrompt", "false")
                              }
                            />
                          </div>
                        </div>

                        {formData.needPrompt && (
                          <div>
                            <label
                              className="mb-1 block text-sm font-medium"
                              htmlFor="system-prompt"
                            >
                              System Prompt
                            </label>
                            <textarea
                              id="system-prompt"
                              name="systemPrompt"
                              className="form-input w-full rounded-lg border border-gray-300 p-2 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                              rows={5}
                              value={formData.systemPrompt}
                              onChange={handleChange}
                              placeholder="You are a helpful assistant..."
                            />
                          </div>
                        )}
                      </div>
                    </>
                  )}

                  {/* Step 4: LLM Selection */}
                  {currentStep === 4 && (
                    <>
                      <h1 className="mb-6 text-3xl font-bold text-gray-800 dark:text-gray-100">
                        Select LLM Type
                      </h1>

                      <div className="mb-8 space-y-3">
                        {llmTypes.map((type) => (
                          <RadioOption
                            key={type.id}
                            id={type.id}
                            name="llmType"
                            label={type.label}
                            description={type.description}
                            checked={formData.llmType === type.id}
                            onChange={() =>
                              handleRadioChange("llmType", type.id)
                            }
                          />
                        ))}
                      </div>
                    </>
                  )}

                  {/* Step 5: Output Type Selection */}
                  {currentStep === 5 && (
                    <>
                      <h1 className="text-3xl text-gray-800 dark:text-gray-100 font-bold mb-6">Select Output Type</h1>
                      
                      <div className="space-y-3 mb-8">
                        {outputTypes.map((type) => (
                          <RadioOption
                            key={type.id}
                            id={type.id}
                            name="outputType"
                            label={type.label}
                            description={type.description}
                            checked={formData.outputType === type.id}
                            onChange={() => handleRadioChange('outputType', type.id)}
                          />
                        ))}
                      </div>
                    </>
                  )}

                  {/* Step 6: Summary and Submit */}
                  {currentStep === 6 && (
                    <>
                      <h1 className="text-3xl text-gray-800 dark:text-gray-100 font-bold mb-6">Review and Submit</h1>
                      
                      <div className="space-y-6 mb-8">
                        <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">Flow Summary</h2>
                          <p className="mb-2"><strong>Name:</strong> {formData.flowName}</p>
                          <p className="mb-2"><strong>Description:</strong> {formData.flowDescription}</p>
                          <p className="mb-2"><strong>Project Type:</strong> {formData.projectType}</p>
                          <p className="mb-2"><strong>Input Type:</strong> {formData.inputType === 'chatInput' ? 'Chat Input' : 'Text Input'}</p>
                          <p className="mb-2"><strong>Using System Prompt:</strong> {formData.needPrompt ? 'Yes' : 'No'}</p>
                          {formData.needPrompt && <p className="mb-2"><strong>System Prompt:</strong> {formData.systemPrompt}</p>}
                          <p className="mb-2"><strong>LLM Type:</strong> {formData.llmType}</p>
                          <p className="mb-2"><strong>Output Type:</strong> {formData.outputType === 'chatOutput' ? 'Chat Output' : 'Text Output'}</p>
                        </div>
                      </div>
                    </>
                  )}

                  {/* Navigation Buttons */}
                  <div className="flex items-center justify-between mt-8">
                    {currentStep > 1 && (
                      <Button 
                        variant="secondary" 
                        onClick={prevStep}
                      >
                        &lt;- Previous
                      </Button>
                    )}
                    
                    {currentStep < totalSteps ? (
                      <Button 
                        variant="primary" 
                        className="ml-auto"
                        onClick={nextStep}
                        disabled={currentStep === 1 && (!formData.flowName || !formData.flowDescription || !formData.projectType)}
                      >
                        Next Step <ChevronRight className="ml-2 h-4 w-4 inline" />
                      </Button>
                    ) : (
                      <Button 
                        variant="primary" 
                        className="ml-auto bg-[#1b1b1b] hover:bg-[#252525] text-gray-300 border border-gray-800"
                        type="submit"
                      >
                        Create Flow <ChevronRight className="ml-2 h-4 w-4 inline" />
                      </Button>
                    )}
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>

        {/* Image */}
        <div
          className="hidden h-full overflow-hidden md:block md:w-1/4"
          aria-hidden="true"
        >
          <img
            className="h-full w-full object-cover object-center"
            src={OnboardingImage}
            alt="Onboarding"
          />
        </div>
      </div>
    </div>
  );
};

export default DynamicFlowStepper;
