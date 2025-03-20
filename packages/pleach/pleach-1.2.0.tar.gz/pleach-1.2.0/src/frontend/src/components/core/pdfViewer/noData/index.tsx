import { PDFErrorTitle, PDFLoadError } from "../../../../constants/constants";

export default function NoDataPdf(): JSX.Element {
  return (
    <div className="flex h-full w-full flex-col items-center justify-center bg-muted">
      <div className="chat-alert-box">
        <span>
          📄 <span className="pleach-chat-span">{PDFErrorTitle}</span>
        </span>
        <br />
        <div className="pleach-chat-desc">
          <span className="pleach-chat-desc-span">{PDFLoadError} </span>
        </div>
      </div>
    </div>
  );
}
