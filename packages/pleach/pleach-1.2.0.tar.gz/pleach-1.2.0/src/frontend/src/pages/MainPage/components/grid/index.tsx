// import ForwardedIconComponent from "@/components/common/genericIconComponent";
// import useDragStart from "@/components/core/cardComponent/hooks/use-on-drag-start";
// import { Button } from "@/components/ui/button";
// import { Card } from "@/components/ui/card";
// import {
//   DropdownMenu,
//   DropdownMenuContent,
//   DropdownMenuTrigger,
// } from "@/components/ui/dropdown-menu";
// import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
// import useDeleteFlow from "@/hooks/flows/use-delete-flow";
// import DeleteConfirmationModal from "@/modals/deleteConfirmationModal";
// import FlowSettingsModal from "@/modals/flowSettingsModal";
// import useAlertStore from "@/stores/alertStore";
// import useFlowsManagerStore from "@/stores/flowsManagerStore";
// import { FlowType } from "@/types/flow";
// import { swatchColors } from "@/utils/styleUtils";
// import { cn, getNumberFromString } from "@/utils/utils";
// import { useState } from "react";
// import { useParams } from "react-router-dom";
// import useDescriptionModal from "../../hooks/use-description-modal";
// import { useGetTemplateStyle } from "../../utils/get-template-style";
// import { timeElapsed } from "../../utils/time-elapse";
// import DropdownComponent from "../dropdown";

// const GridComponent = ({ flowData }: { flowData: FlowType }) => {
//   const navigate = useCustomNavigate();

//   const [openDelete, setOpenDelete] = useState(false);
//   const [openSettings, setOpenSettings] = useState(false);
//   const setSuccessData = useAlertStore((state) => state.setSuccessData);
//   const { deleteFlow } = useDeleteFlow();

//   const setErrorData = useAlertStore((state) => state.setErrorData);
//   const { folderId } = useParams();
//   const isComponent = flowData.is_component ?? false;
//   const setFlowToCanvas = useFlowsManagerStore(
//     (state) => state.setFlowToCanvas,
//   );

//   const { getIcon } = useGetTemplateStyle(flowData);

//   const editFlowLink = `/flow/${flowData.id}${folderId ? `/folder/${folderId}` : ""}`;

//   const handleClick = async () => {
//     if (!isComponent) {
//       await setFlowToCanvas(flowData);
//       navigate(editFlowLink);
//     }
//   };

//   const handleDelete = () => {
//     deleteFlow({ id: [flowData.id] })
//       .then(() => {
//         setSuccessData({
//           title: "Selected items deleted successfully",
//         });
//       })
//       .catch(() => {
//         setErrorData({
//           title: "Error deleting items",
//           list: ["Please try again"],
//         });
//       });
//   };

//   const descriptionModal = useDescriptionModal(
//     [flowData?.id],
//     flowData.is_component ? "component" : "flow",
//   );

//   const { onDragStart } = useDragStart(flowData);

//   const swatchIndex =
//     (flowData.gradient && !isNaN(parseInt(flowData.gradient))
//       ? parseInt(flowData.gradient)
//       : getNumberFromString(flowData.gradient ?? flowData.id)) %
//     swatchColors.length;

//   return (
//     <>
//       <Card
//         key={flowData.id}
//         draggable
//         onDragStart={onDragStart}
//         onClick={handleClick}
//         className={`my-1 flex flex-col rounded-lg border border-border bg-background p-4 hover:border-placeholder-foreground hover:shadow-sm ${
//           isComponent ? "cursor-default" : "cursor-pointer"
//         }`}
//       >
//         <div className="flex w-full items-center gap-4">
//           <div className={cn(`flex rounded-lg p-3`, swatchColors[swatchIndex])}>
//             <ForwardedIconComponent
//               name={getIcon()}
//               aria-hidden="true"
//               className="h-5 w-5"
//             />
//           </div>
//           <div className="flex w-full min-w-0 items-center justify-between">
//             <div className="flex min-w-0 flex-col">
//               <div className="text-md truncate font-semibold">
//                 {flowData.name}
//               </div>
//               <div className="truncate text-xs text-muted-foreground">
//                 Edited {timeElapsed(flowData.updated_at)} ago
//               </div>
//             </div>
//             <DropdownMenu>
//               <DropdownMenuTrigger asChild>
//                 <Button
//                   variant="ghost"
//                   data-testid="home-dropdown-menu"
//                   size="iconMd"
//                   className="group"
//                 >
//                   <ForwardedIconComponent
//                     name="Ellipsis"
//                     aria-hidden="true"
//                     className="h-5 w-5 text-muted-foreground group-hover:text-foreground"
//                   />
//                 </Button>
//               </DropdownMenuTrigger>
//               <DropdownMenuContent
//                 className="w-[185px]"
//                 sideOffset={5}
//                 side="bottom"
//               >
//                 <DropdownComponent
//                   flowData={flowData}
//                   setOpenDelete={setOpenDelete}
//                   handleEdit={() => {
//                     setOpenSettings(true);
//                   }}
//                 />
//               </DropdownMenuContent>
//             </DropdownMenu>
//           </div>
//         </div>

//         <div className="line-clamp-2 h-full pt-5 text-sm text-primary">
//           {flowData.description}
//         </div>
//       </Card>

//       {openDelete && (
//         <DeleteConfirmationModal
//           open={openDelete}
//           setOpen={setOpenDelete}
//           onConfirm={handleDelete}
//           description={descriptionModal}
//           note={
//             !flowData.is_component
//               ? "Deleting the selected flow will remove all associated messages."
//               : ""
//           }
//         >
//           <></>
//         </DeleteConfirmationModal>
//       )}
//       <FlowSettingsModal
//         open={openSettings}
//         setOpen={setOpenSettings}
//         flowData={flowData}
//         details
//       />
//     </>
//   );
// };

// export default GridComponent;


import ForwardedIconComponent from "@/components/common/genericIconComponent";
import useDragStart from "@/components/core/cardComponent/hooks/use-on-drag-start";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import useDeleteFlow from "@/hooks/flows/use-delete-flow";
import DeleteConfirmationModal from "@/modals/deleteConfirmationModal";
import FlowSettingsModal from "@/modals/flowSettingsModal";
import useAlertStore from "@/stores/alertStore";
import useFlowsManagerStore from "@/stores/flowsManagerStore";
import { FlowType } from "@/types/flow";
import { swatchColors } from "@/utils/styleUtils";
import { cn, getNumberFromString } from "@/utils/utils";
import { useState } from "react";
import { useParams } from "react-router-dom";
import useDescriptionModal from "../../hooks/use-description-modal";
import { useGetTemplateStyle } from "../../utils/get-template-style";
import { timeElapsed } from "../../utils/time-elapse";
import DropdownComponent from "../dropdown";

const GridComponent = ({ flowData }: { flowData: FlowType }) => {
  const navigate = useCustomNavigate();

  const [openDelete, setOpenDelete] = useState(false);
  const [openSettings, setOpenSettings] = useState(false);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const { deleteFlow } = useDeleteFlow();

  const setErrorData = useAlertStore((state) => state.setErrorData);
  const { folderId } = useParams();
  const isComponent = flowData.is_component ?? false;
  const setFlowToCanvas = useFlowsManagerStore(
    (state) => state.setFlowToCanvas,
  );

  const { getIcon } = useGetTemplateStyle(flowData);

  const editFlowLink = `/flow/${flowData.id}${folderId ? `/folder/${folderId}` : ""}`;

  const handleClick = async () => {
    if (!isComponent) {
      await setFlowToCanvas(flowData);
      navigate(editFlowLink);
    }
  };

  const handleDelete = () => {
    deleteFlow({ id: [flowData.id] })
      .then(() => {
        setSuccessData({
          title: "Selected items deleted successfully",
        });
      })
      .catch(() => {
        setErrorData({
          title: "Error deleting items",
          list: ["Please try again"],
        });
      });
  };

  const descriptionModal = useDescriptionModal(
    [flowData?.id],
    flowData.is_component ? "component" : "flow",
  );

  const { onDragStart } = useDragStart(flowData);

  const swatchIndex =
    (flowData.gradient && !isNaN(parseInt(flowData.gradient))
      ? parseInt(flowData.gradient)
      : getNumberFromString(flowData.gradient ?? flowData.id)) %
    swatchColors.length;

  return (
    <>
      <Card
        key={flowData.id}
        draggable
        onDragStart={onDragStart}
        className="flex flex-col h-full bg-white dark:bg-gray-800 shadow-xs rounded-xl border border-gray-200 dark:border-gray-700/60 transition-all duration-200 hover:border-violet-300 dark:hover:border-violet-600 hover:shadow-md hover:translate-y-[-2px]"
      >
        <div className="flex flex-col h-full">
          {/* Card top */}
          <div className="grow p-5">
            {/* Menu button */}
            <div className="relative">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    data-testid="home-dropdown-menu"
                    size="iconMd"
                    className="absolute top-0 right-0 inline-flex hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    <ForwardedIconComponent
                      name="Ellipsis"
                      aria-hidden="true"
                      className="h-5 w-5 text-muted-foreground group-hover:text-foreground"
                    />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  className="w-[185px]"
                  sideOffset={5}
                  side="bottom"
                >
                  <DropdownComponent
                    flowData={flowData}
                    setOpenDelete={setOpenDelete}
                    handleEdit={() => {
                      setOpenSettings(true);
                    }}
                  />
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
            
            {/* Image + name */}
            <header>
              <div className="flex justify-center mb-5">
                <div 
                  className="relative inline-flex items-start cursor-pointer transform transition-transform duration-200 hover:scale-110"
                  onClick={handleClick}
                >
                  <div className={cn(`flex rounded-full p-2`, swatchColors[swatchIndex])}>
                    <ForwardedIconComponent
                      name={getIcon()}
                      aria-hidden="true"
                      className="h-8 w-8"
                    />
                  </div>
                </div>
              </div>
              <div className="text-center">
                <div 
                  className="inline-flex text-gray-800 dark:text-gray-100 hover:text-violet-600 dark:hover:text-violet-400 cursor-pointer transition-colors duration-200"
                  onClick={handleClick}
                >
                  <h4 className="text-xl leading-snug justify-center font-semibold">{flowData.name}</h4>
                </div>
              </div>
              <div className="flex justify-center items-center text-sm text-gray-500">
                <span>Edited {timeElapsed(flowData.updated_at)} ago</span>
              </div>
            </header>
            
            {/* Description */}
            <div className="text-center mt-2">
              <div className="text-sm line-clamp-2 text-gray-600 dark:text-gray-400">
                {flowData.description}
              </div>
            </div>
          </div>
          
          {/* Card footer */}
          <div className="border-t border-gray-100 dark:border-gray-700/60">
            <div 
              className="block text-center text-sm text-violet-500 hover:text-violet-600 dark:hover:text-violet-400 font-medium px-3 py-4 cursor-pointer transition-colors duration-200 hover:bg-violet-50 dark:hover:bg-violet-900/20"
              onClick={handleClick}
            >
              <div className="flex items-center justify-center">
                <ForwardedIconComponent
                  name="ArrowRight"
                  aria-hidden="true"
                  className="shrink-0 mr-2 h-4 w-4"
                />
                <span>Open Flow</span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {openDelete && (
        <DeleteConfirmationModal
          open={openDelete}
          setOpen={setOpenDelete}
          onConfirm={handleDelete}
          description={descriptionModal}
          note={
            !flowData.is_component
              ? "Deleting the selected flow will remove all associated messages."
              : ""
          }
        >
          <></>
        </DeleteConfirmationModal>
      )}
      <FlowSettingsModal
        open={openSettings}
        setOpen={setOpenSettings}
        flowData={flowData}
        details
      />
    </>
  );
};

export default GridComponent;