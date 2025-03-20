import ForwardedIconComponent from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import IOModal from "@/modals/IOModal/new-modal";

const PlaygroundButton = ({ hasIO, open, setOpen, canvasOpen }) => {
  const PlayIcon = () => (
    <ForwardedIconComponent name="bot-message-square" className="h-5 w-5 transition-all" />
  );

  const ButtonLabel = () => <span className="hidden md:block">Playground</span>;

  const ActiveButton = () => (
    <div
      data-testid="playground-btn-flow-io"
      className="playground-btn-flow-toolbar hover:bg-accent px-2 py-3 rounded-full flex items-center gap-2 text-base font-medium shadow-lg"
    >
      <PlayIcon />
    {/* <ButtonLabel /> */}
    </div>
  );

  const DisabledButton = () => (
    <div
      className="playground-btn-flow-toolbar cursor-not-allowed text-muted-foreground duration-150 px-4 py-3 rounded-full flex items-center gap-2 text-base font-medium shadow-sm"
      data-testid="playground-btn-flow"
    >
      <PlayIcon />
      {/* <ButtonLabel /> */}
    </div>
  );

  return hasIO ? (
    <IOModal
      open={open}
      setOpen={setOpen}
      disable={!hasIO}
      canvasOpen={canvasOpen}
    >
      <ActiveButton />
    </IOModal>
  ) : (
    <ShadTooltip content="Add a Chat Input or Chat Output to use the playground">
      <div>
        <DisabledButton />
      </div>
    </ShadTooltip>
  );
};

export default PlaygroundButton;