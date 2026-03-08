import { p as theme } from "./globals-d3aR1MYC.js";
import "./paths-BMo6kTge.js";
import "./subsystem-Cfn2Pryx.js";
import "./boolean-DtWR5bt3.js";
import "./auth-profiles-XSsJj4N1.js";
import "./agent-scope-Bfb1NlQ6.js";
import "./utils-cwpAMi-t.js";
import "./openclaw-root-BFfBQ6FD.js";
import "./logger-DB-PHqB2.js";
import "./exec-DKveyX0v.js";
import "./github-copilot-token-Byc_YVYE.js";
import "./host-env-security-lcjXF83D.js";
import "./version-DdJhsIqk.js";
import "./registry-CUSs0-4j.js";
import "./manifest-registry-Dkqj8xGu.js";
import "./message-channel-DTk937hY.js";
import "./tailnet-BXLAgtlT.js";
import "./ws-Da560NJf.js";
import "./client-B9xXRY-r.js";
import "./call-C79Luiuk.js";
import "./pairing-token-CCWPBg5t.js";
import "./runtime-config-collectors-Dv1HEdRX.js";
import "./command-secret-targets-BLNsV-9B.js";
import { t as formatDocsLink } from "./links-BVDZVrXu.js";
import { n as registerQrCli } from "./qr-cli-C_xb0wNi.js";

//#region src/cli/clawbot-cli.ts
function registerClawbotCli(program) {
	registerQrCli(program.command("clawbot").description("Legacy clawbot command aliases").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/clawbot", "docs.openclaw.ai/cli/clawbot")}\n`));
}

//#endregion
export { registerClawbotCli };