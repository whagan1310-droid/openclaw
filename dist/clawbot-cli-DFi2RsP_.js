import "./paths-BBP4yd-2.js";
import { p as theme } from "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./agent-scope-C_RF521q.js";
import "./subsystem-D5pRlZe-.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DHGbafYr.js";
import "./exec-DruQEXPV.js";
import "./model-selection-BaeHlT6A.js";
import "./github-copilot-token-b6kJVrW-.js";
import "./boolean-BsqeuxE6.js";
import "./env-BCNBCy-T.js";
import "./host-env-security-DkAVVuaw.js";
import "./registry-CEJSZAKm.js";
import "./manifest-registry-Ds8wMsKE.js";
import "./message-channel-CSTlX5lG.js";
import "./tailnet-D1FN3bC3.js";
import "./ws-CtzAmMCA.js";
import "./client-DPuEGSE_.js";
import "./call-CqTAcmXH.js";
import "./pairing-token-Dz_8pP2A.js";
import "./runtime-config-collectors-CvVyFBgq.js";
import "./command-secret-targets-DcsK8ZYD.js";
import { t as formatDocsLink } from "./links-B0L7hhCO.js";
import { n as registerQrCli } from "./qr-cli-DxBEuEos.js";

//#region src/cli/clawbot-cli.ts
function registerClawbotCli(program) {
	registerQrCli(program.command("clawbot").description("Legacy clawbot command aliases").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/clawbot", "docs.openclaw.ai/cli/clawbot")}\n`));
}

//#endregion
export { registerClawbotCli };