import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";
import { SidebarProvider } from "@/components/ui/sidebar";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { track } from "@/customization/utils/analytics";
import useAddFlow from "@/hooks/flows/use-add-flow";
import { Category } from "@/types/templates/types";
import { useState } from "react";
import { useParams } from "react-router-dom";
import { newFlowModalPropsType } from "../../types/components";
import BaseModal from "../baseModal";
import GetStartedComponent from "./components/GetStartedComponent";
import TemplateContentComponent from "./components/TemplateContentComponent";
import { Nav } from "./components/navComponent";
import { ChevronRight, ChevronLeft } from "lucide-react";

export default function TemplatesModal({
  open,
  setOpen,
}: newFlowModalPropsType): JSX.Element {
  const [currentTab, setCurrentTab] = useState("create-new-flow");
  const [stepperCurrentStep, setStepperCurrentStep] = useState(1);
  const addFlow = useAddFlow();
  const navigate = useCustomNavigate();
  const { folderId } = useParams();

  // Flow form data state
  const [formData, setFormData] = useState({
    flowName: '',
    flowDescription: '',
    projectType: '',
    inputType: 'chatInput',
    needPrompt: false,
    systemPrompt: '',
    llmType: 'bedrock',
    outputType: 'chatOutput',
    useMemory: false,
    useDatasource: false,
  });

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

  // Define categories and their items
  const categories: Category[] = [
    {
      title: "Create New",
      items: [
        { title: "Create New Flow", icon: "Plus", id: "create-new-flow" },
        { title: "Create New Agent", icon: "UserPlus", id: "create-new-agent" },
      ],
    },
    {
      title: "Templates",
      items: [
        // { title: "Get started", icon: "SquarePlay", id: "get-started" },
        { title: "All templates", icon: "LayoutPanelTop", id: "all-templates" },
      ],
    },
    {
      title: "Use Cases",
      items: [
        { title: "Assistants", icon: "BotMessageSquare", id: "assistants" },
        { title: "Classification", icon: "Tags", id: "classification" },
        { title: "Coding", icon: "TerminalIcon", id: "coding" },
        {
          title: "Content Generation",
          icon: "Newspaper",
          id: "content-generation",
        },
        { title: "Q&A", icon: "Database", id: "q-a" },
      ],
    },
    {
      title: "Methodology",
      items: [
        { title: "Prompting", icon: "MessagesSquare", id: "chatbots" },
        { title: "RAG", icon: "Database", id: "rag" },
        { title: "Agents", icon: "Bot", id: "agents" },
      ],
    }
    // New section

  ];

  const handleFormChange = (e) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? e.target.checked : undefined;
    
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleRadioChange = (name, value) => {
    setFormData({
      ...formData,
      [name]: value === 'true' ? true : value === 'false' ? false : value
    });
  };

  const totalSteps = 6;
  
  const nextStep = () => {
    setStepperCurrentStep(prev => prev + 1);
  };

  const prevStep = () => {
    setStepperCurrentStep(prev => prev - 1);
  };

  const handleCreateFlow = () => {
    // Create flow object based on formData
    console.log('Creating flow with:', formData);
    
    addFlow().then((id) => {
      navigate(`/flow/${id}${folderId ? `/folder/${folderId}` : ""}`);
      track("New Flow Created", { template: "Custom Flow", ...formData });
    });
  };

  // Radio option component for consistent styling
  const RadioOption = ({ 
    id, 
    name, 
    label, 
    description, 
    checked, 
    onChange 
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
          <svg className="w-6 h-6 shrink-0 fill-current mr-4" viewBox="0 0 24 24">
            <path className="text-violet-500" d="m12 10.856 9-5-8.514-4.73a1 1 0 0 0-.972 0L3 5.856l9 5Z" />
            <path className="text-violet-300" d="m11 12.588-9-5V18a1 1 0 0 0 .514.874L11 23.588v-11Z" />
            <path className="text-violet-200" d="M13 12.588v11l8.486-4.714A1 1 0 0 0 22 18V7.589l-9 4.999Z" />
          </svg>
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
    <BaseModal size="templates" open={open} setOpen={setOpen} className="p-0">
      <BaseModal.Content overflowHidden className="flex flex-col p-0">
        <div className="flex h-full">
          <SidebarProvider width="15rem" defaultOpen={false}>
            <Nav
              categories={categories}
              currentTab={currentTab}
              setCurrentTab={(tab) => {
                setCurrentTab(tab);
                if (tab === "create-new-flow") {
                  setStepperCurrentStep(1); // Reset stepper when navigating to it
                }
              }}
            />
            <main className="flex flex-1 flex-col gap-4 overflow-hidden p-6 md:gap-8">
              {currentTab === "get-started" ? (
                <GetStartedComponent />
              ) : currentTab === "create-new-flow" ? (
                <div className="flex flex-col h-full">
                  {/* Step indicator */}
                  <div className="px-4 pb-6 pt-4">
                    <div className="mx-auto w-full">
                      <div className="relative">
                        <div
                          className="absolute left-0 top-1/2 -mt-px h-0.5 w-full bg-gray-200 dark:bg-gray-700/60"
                          aria-hidden="true"
                        ></div>
                        <ul className="relative flex w-full justify-between">
                          {[1, 2, 3, 4, 5, 6].map((step) => (
                            <li key={step}>
                              <button
                                className={`flex items-center justify-center w-6 h-6 rounded-full text-xs font-semibold ${
                                  stepperCurrentStep >= step
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
                  
                  {/* Step content */}
                  <div className="flex-1 overflow-auto">
                    {/* Step 1: Flow Information */}
                    {stepperCurrentStep === 1 && (
                      <>
                        <h2 className="text-xl font-bold mb-4">Flow Information</h2>
                        <div className="space-y-4">
                          <div>
                            <label className="block text-sm font-medium mb-1">
                              Flow Name <span className="text-red-500">*</span>
                            </label>
                            <input
                              id="flow-name"
                              name="flowName"
                              className="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
                              type="text"
                              value={formData.flowName}
                              onChange={handleFormChange}
                              required
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium mb-1">
                              Flow Description <span className="text-red-500">*</span>
                            </label>
                            <textarea
                              id="flow-description"
                              name="flowDescription"
                              className="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
                              rows={3}
                              value={formData.flowDescription}
                              onChange={handleFormChange}
                              required
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium mb-1">
                              Project Type <span className="text-red-500">*</span>
                            </label>
                            <select
                              id="project-type"
                              name="projectType"
                              className="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
                              value={formData.projectType}
                              onChange={handleFormChange}
                              required
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
                    {stepperCurrentStep === 2 && (
                      <>
                        <h2 className="text-xl font-bold mb-4">Select Input Type</h2>
                        <div className="space-y-3">
                          {inputTypes.map((type) => (
                            <RadioOption
                              key={type.id}
                              id={type.id}
                              name="inputType"
                              label={type.label}
                              description={type.description}
                              checked={formData.inputType === type.id}
                              onChange={() => handleRadioChange("inputType", type.id)}
                            />
                          ))}
                        </div>
                      </>
                    )}

                    {/* Step 3: Prompt Configuration */}
                    {stepperCurrentStep === 3 && (
                      <>
                        <h2 className="text-xl font-bold mb-4">Prompt Configuration</h2>
                        <div className="space-y-6">
                          <div>
                            <label className="block text-sm font-medium mb-3">
                              Do you need a system prompt?
                            </label>
                            <div className="space-y-3">
                              <RadioOption
                                id="prompt-yes"
                                name="needPrompt"
                                label="Yes, I need a system prompt"
                                description="Define behavior and capabilities with a system prompt"
                                checked={formData.needPrompt === true}
                                onChange={() => handleRadioChange("needPrompt", "true")}
                              />
                              <RadioOption
                                id="prompt-no"
                                name="needPrompt"
                                label="No, I don't need a system prompt"
                                description="Use default model behavior without a custom prompt"
                                checked={formData.needPrompt === false}
                                onChange={() => handleRadioChange("needPrompt", "false")}
                              />
                            </div>
                          </div>

                          {formData.needPrompt && (
                            <div>
                              <label className="block text-sm font-medium mb-1">
                                System Prompt
                              </label>
                              <textarea
                                id="system-prompt"
                                name="systemPrompt"
                                className="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
                                rows={5}
                                value={formData.systemPrompt}
                                onChange={handleFormChange}
                                placeholder="You are a helpful assistant..."
                              />
                            </div>
                          )}
                        </div>
                      </>
                    )}

                    {/* Step 4: LLM Selection */}
                    {stepperCurrentStep === 4 && (
                      <>
                        <h2 className="text-xl font-bold mb-4">Select LLM Type</h2>
                        <div className="space-y-3">
                          {llmTypes.map((type) => (
                            <RadioOption
                              key={type.id}
                              id={type.id}
                              name="llmType"
                              label={type.label}
                              description={type.description}
                              checked={formData.llmType === type.id}
                              onChange={() => handleRadioChange("llmType", type.id)}
                            />
                          ))}
                        </div>
                      </>
                    )}

                    {/* Step 5: Output Type Selection */}
                    {stepperCurrentStep === 5 && (
                      <>
                        <h2 className="text-xl font-bold mb-4">Select Output Type</h2>
                        <div className="space-y-3">
                          {outputTypes.map((type) => (
                            <RadioOption
                              key={type.id}
                              id={type.id}
                              name="outputType"
                              label={type.label}
                              description={type.description}
                              checked={formData.outputType === type.id}
                              onChange={() => handleRadioChange("outputType", type.id)}
                            />
                          ))}
                        </div>
                      </>
                    )}

                    {/* Step 6: Review and Submit */}
                    {stepperCurrentStep === 6 && (
                      <>
                        <h2 className="text-xl font-bold mb-4">Review and Submit</h2>
                        <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                          <h3 className="text-lg font-semibold mb-4">Flow Summary</h3>
                          <p className="mb-2"><strong>Name:</strong> {formData.flowName}</p>
                          <p className="mb-2"><strong>Description:</strong> {formData.flowDescription}</p>
                          <p className="mb-2"><strong>Project Type:</strong> {formData.projectType}</p>
                          <p className="mb-2"><strong>Input Type:</strong> {formData.inputType === 'chatInput' ? 'Chat Input' : 'Text Input'}</p>
                          <p className="mb-2"><strong>Using System Prompt:</strong> {formData.needPrompt ? 'Yes' : 'No'}</p>
                          {formData.needPrompt && <p className="mb-2"><strong>System Prompt:</strong> {formData.systemPrompt}</p>}
                          <p className="mb-2"><strong>LLM Type:</strong> {llmTypes.find(type => type.id === formData.llmType)?.label || formData.llmType}</p>
                          <p className="mb-2"><strong>Output Type:</strong> {formData.outputType === 'chatOutput' ? 'Chat Output' : 'Text Output'}</p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              ) : currentTab === "create-new-agent" ? (
                <div>
                  <h2 className="text-xl font-bold mb-4">Create New Agent</h2>
                  <p className="text-muted-foreground mb-4">
                    Configure a new intelligent agent with custom capabilities and knowledge.
                  </p>
                  
                  <div className="space-y-6">
                    <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                      <h3 className="font-medium mb-2">Agent Templates</h3>
                      <p className="text-sm text-muted-foreground">
                        Choose a template to get started quickly with pre-configured capabilities.
                      </p>
                      
                      <div className="grid gap-4 mt-4 grid-cols-1 md:grid-cols-2">
                        <div className="border p-4 rounded-lg bg-white dark:bg-gray-700 hover:border-violet-500 cursor-pointer transition-colors">
                          <ForwardedIconComponent name="Bot" className="h-8 w-8 text-violet-500 mb-2" />
                          <h4 className="font-medium">Customer Support</h4>
                          <p className="text-sm text-muted-foreground">Assists with customer inquiries and problem-solving.</p>
                        </div>
                        
                        <div className="border p-4 rounded-lg bg-white dark:bg-gray-700 hover:border-violet-500 cursor-pointer transition-colors">
                          <ForwardedIconComponent name="Search" className="h-8 w-8 text-violet-500 mb-2" />
                          <h4 className="font-medium">Knowledge Assistant</h4>
                          <p className="text-sm text-muted-foreground">Answers questions from your knowledge base.</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                      <h3 className="font-medium mb-2">Agent Capabilities</h3>
                      <p className="text-sm text-muted-foreground">
                        Select which capabilities your agent will have.
                      </p>
                      
                      <div className="space-y-2 mt-4">
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span>Document processing</span>
                        </label>
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span>Web browsing</span>
                        </label>
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span>Code execution</span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <TemplateContentComponent
                  currentTab={currentTab}
                  categories={categories.flatMap((category) => category.items)}
                />
              )}
              
              <BaseModal.Footer>
                {currentTab === "create-new-flow" ? (
                  <div className="flex w-full justify-between items-center">
                    {stepperCurrentStep > 1 ? (
                      <Button
                        variant="outline"
                        onClick={prevStep}
                        className="flex items-center gap-1"
                      >
                        <ChevronLeft className="h-4 w-4" />
                        Previous
                      </Button>
                    ) : (
                      <div></div> /* Empty div for spacing */
                    )}
                    
                    {stepperCurrentStep < totalSteps ? (
                      <Button
                        onClick={nextStep}
                        disabled={stepperCurrentStep === 1 && (!formData.flowName || !formData.flowDescription || !formData.projectType)}
                        className="flex items-center gap-1 text-gray-400 border-gray-700 hover:bg-gray-800 hover:text-white"
                      >
                        Next
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    ) : (
                      <Button
                        onClick={handleCreateFlow}
                        className="flex items-center gap-1"
                      >
                        Create new
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ) : currentTab === "create-new-agent" ? (
                  <div className="flex w-full justify-end items-center">
                    <Button
                      onClick={() => {
                        // Handle agent creation
                        console.log("Creating new agent");
                        // Navigate to the appropriate page
                      }}
                      className="flex items-center gap-1"
                    >
                      Create new
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                ) : (
                  <div className="flex w-full flex-col justify-between gap-4 pb-4 sm:flex-row sm:items-center">
                    <div className="flex flex-col items-start justify-center">
                      <div className="font-semibold">Start from scratch</div>
                      <div className="text-sm text-muted-foreground">
                        Begin with a fresh flow to build from scratch.
                      </div>
                    </div>
                    <Button
                      onClick={() => {
                        addFlow().then((id) => {
                          navigate(
                            `/flow/${id}${folderId ? `/folder/${folderId}` : ""}`,
                          );
                        });
                        track("New Flow Created", { template: "Blank Flow" });
                      }}
                      size="sm"
                      data-testid="blank-flow"
                      className="shrink-0"
                    >
                      <ForwardedIconComponent
                        name="Plus"
                        className="h-4 w-4 shrink-0"
                      />
                      Blank Flow
                    </Button>
                  </div>
                )}
              </BaseModal.Footer>
            </main>
          </SidebarProvider>
        </div>
      </BaseModal.Content>
    </BaseModal>
  );
}