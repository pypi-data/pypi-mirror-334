import { convertTestName } from "@/components/common/storeCardComponent/utils/convert-test-name";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import useDeleteFlow from "@/hooks/flows/use-delete-flow";
import { useAddComponent } from "@/hooks/useAddComponent";
import { DragEventHandler, forwardRef, useRef, useState } from "react";
import IconComponent, {
  ForwardedIconComponent,
} from "../../../../../../components/common/genericIconComponent";
import ShadTooltip from "../../../../../../components/common/shadTooltipComponent";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
} from "../../../../../../components/ui/select-custom";
import { useDarkStore } from "../../../../../../stores/darkStore";
import useFlowsManagerStore from "../../../../../../stores/flowsManagerStore";
import { APIClassType } from "../../../../../../types/api";
import {
  createFlowComponent,
  downloadNode,
  getNodeId,
} from "../../../../../../utils/reactflowUtils";
import { cn, removeCountFromString } from "../../../../../../utils/utils";

export const SidebarDraggableComponent = forwardRef(
  (
    {
      sectionName,
      display_name,
      icon,
      itemName,
      error,
      color,
      onDragStart,
      apiClass,
      official,
      beta,
      legacy,
      disabled,
      disabledTooltip,
    }: {
      sectionName: string;
      apiClass: APIClassType;
      icon: string;
      display_name: string;
      itemName: string;
      error: boolean;
      color: string;
      onDragStart: DragEventHandler<HTMLDivElement>;
      official: boolean;
      beta: boolean;
      legacy: boolean;
      disabled?: boolean;
      disabledTooltip?: string;
    },
    ref,
  ) => {
    const [open, setOpen] = useState(false);
    const { deleteFlow } = useDeleteFlow();
    const flows = useFlowsManagerStore((state) => state.flows);
    const addComponent = useAddComponent();

    const version = useDarkStore((state) => state.version);
    const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });
    const popoverRef = useRef<HTMLDivElement>(null);

    const handlePointerDown = (e) => {
      if (!open) {
        const rect = popoverRef.current?.getBoundingClientRect() ?? {
          left: 0,
          top: 0,
        };
        setCursorPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
      }
    };

    function handleSelectChange(value: string) {
      switch (value) {
        case "download":
          const type = removeCountFromString(itemName);
          downloadNode(
            createFlowComponent(
              { id: getNodeId(type), type, node: apiClass },
              version,
            ),
          );
          break;
        case "delete":
          const flowId = flows?.find((f) => f.name === display_name);
          if (flowId) deleteFlow({ id: flowId.id });
          break;
      }
    }

    const handleKeyDown = (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        addComponent(apiClass, itemName);
      }
    };

    return (
      <Select
        onValueChange={handleSelectChange}
        onOpenChange={(change) => setOpen(change)}
        open={open}
        key={itemName}
      >
        <ShadTooltip
          content={disabled ? disabledTooltip : null}
          styleClasses="z-50"
        >
          <div
            onPointerDown={handlePointerDown}
            onContextMenuCapture={(e) => {
              e.preventDefault();
              setOpen(true);
            }}
            key={itemName}
            data-tooltip-id={itemName}
            tabIndex={0}
            onKeyDown={handleKeyDown}
            className="m-0.5 w-[calc(50%-4px)] rounded-md px-1 py-1 outline-none ring-ring focus-visible:ring-1"
          >
            <div
              data-testid={sectionName + display_name}
              id={sectionName + display_name}
              className={cn(
                "group/draggable flex cursor-grab flex-col rounded-md bg-secondary/20 p-1 transition-colors duration-100 hover:bg-secondary/70",
                error && "cursor-not-allowed select-none",
                disabled
                  ? "pointer-events-none bg-accent text-placeholder-foreground"
                  : "text-foreground",
              )}
              draggable={!error}
              // style={{
              //   borderTop: `1px solid ${color}`,
              // }}
              onDragStart={onDragStart}
              onDragEnd={() => {
                if (
                  document.getElementsByClassName("cursor-grabbing").length > 0
                ) {
                  document.body.removeChild(
                    document.getElementsByClassName("cursor-grabbing")[0],
                  );
                }
              }}
            >
              {/* Centered larger icon */}
              <div className="mb-2 mt-2 flex justify-center">
                <ForwardedIconComponent
                  name={icon}
                  className="h-6 w-6 text-primary"
                />
              </div>

              {/* Card content */}
              <div className="flex w-full items-center overflow-hidden">
                <div className="flex-1 overflow-hidden">
                  <ShadTooltip content={display_name} styleClasses="z-50">
                    <span className="mb-2 block truncate text-center text-xs font-medium">
                      {display_name}
                    </span>
                  </ShadTooltip>
                  {/* <div className="mt-0.5 flex justify-center">
                    {beta && (
                      <Badge
                        variant="pinkStatic"
                        size="xq"
                        className="mx-0.5 shrink-0"
                      >
                        Beta
                      </Badge>
                    )}
                    {legacy && (
                      <Badge
                        variant="secondaryStatic"
                        size="xq"
                        className="mx-0.5 shrink-0"
                      >
                        Legacy
                      </Badge>
                    )}
                  </div> */}
                </div>
              </div>

              {/* Action buttons */}
              {/* <div className="mt-1 flex items-center justify-between border-t border-border pt-0.5">
                {!disabled && (
                  <Button
                    data-testid={`add-component-button-${convertTestName(
                      display_name,
                    )}`}
                    variant="ghost"
                    size="icon"
                    tabIndex={-1}
                    className="text-primary"
                    onClick={() => addComponent(apiClass, itemName)}
                  >
                    <ForwardedIconComponent
                      name="Plus"
                      className="h-4 w-4 shrink-0 transition-all group-hover/draggable:opacity-100 group-focus/draggable:opacity-100 sm:opacity-0"
                    />
                  </Button>
                )}
                <div ref={popoverRef} className="ml-auto">
                  <ForwardedIconComponent
                    name="GripVertical"
                    className="h-4 w-4 shrink-0 text-muted-foreground group-hover/draggable:text-primary"
                  />
                  <SelectTrigger tabIndex={-1}></SelectTrigger>
                  <SelectContent
                    position="popper"
                    side="bottom"
                    sideOffset={-25}
                    style={{
                      position: "absolute",
                      left: cursorPos.x,
                      top: cursorPos.y,
                    }}
                  >
                    <SelectItem value={"download"}>
                      <div className="flex">
                        <IconComponent
                          name="Download"
                          className="relative top-0.5 mr-2 h-4 w-4"
                        />{" "}
                        Download{" "}
                      </div>{" "}
                    </SelectItem>
                    {!official && (
                      <SelectItem value={"delete"}>
                        <div className="flex">
                          <IconComponent
                            name="Trash2"
                            className="relative top-0.5 mr-2 h-4 w-4"
                          />{" "}
                          Delete{" "}
                        </div>{" "}
                      </SelectItem>
                    )}
                  </SelectContent>
                </div>
              </div> */}
            </div>
          </div>
        </ShadTooltip>
      </Select>
    );
  },
);

export default SidebarDraggableComponent;
