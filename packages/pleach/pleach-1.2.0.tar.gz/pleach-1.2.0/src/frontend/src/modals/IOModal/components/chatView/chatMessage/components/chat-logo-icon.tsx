import PleachLogo from "@/assets/pleach-logo.png";
import ChainLogo from "@/assets/logo.svg?react";
import { ENABLE_NEW_LOGO } from "@/customization/feature-flags";

export default function LogoIcon() {
  return (
    <div className="relative flex h-8 w-8 items-center justify-center rounded-md bg-muted">
      <div className="flex h-8 w-8 items-center justify-center">
      <img src={PleachLogo} className="h-6"  alt="Pleach Logo" />
      </div>
    </div>
  );
}
