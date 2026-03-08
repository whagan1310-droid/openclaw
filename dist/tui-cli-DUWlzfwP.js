import "./paths-BBP4yd-2.js";
import { p as theme } from "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./thinking-Fqckw03T.js";
import "./agent-scope-C_RF521q.js";
import { d as defaultRuntime } from "./subsystem-D5pRlZe-.js";
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
import "./dock-BI9_dwQi.js";
import "./message-channel-CSTlX5lG.js";
import "./plugins-DD42H5-v.js";
import "./sessions-DL9FheWJ.js";
import "./pi-embedded-helpers-BPB21Ua-.js";
import "./sandbox-OEaNk7q1.js";
import "./tool-catalog-D3ArwgWP.js";
import "./chrome-B6q8Do1b.js";
import "./tailscale-D2B0lekn.js";
import "./tailnet-D1FN3bC3.js";
import "./ws-CtzAmMCA.js";
import "./auth-B6-DZzxb.js";
import "./server-context-XEXonK4C.js";
import "./frontmatter-C4-qX3Fu.js";
import "./env-overrides-BAmcNe_6.js";
import "./path-alias-guards-DDVRklJy.js";
import "./skills-CaeMRjIS.js";
import "./paths-DbMRQrAf.js";
import "./redact-Cl6kEomM.js";
import "./errors-BmWNPXkt.js";
import "./fs-safe-Bb0BVco4.js";
import "./proxy-env-pxZ2eJjo.js";
import "./image-ops-D8PauZdF.js";
import "./store-C3L_zXwi.js";
import "./ports-BOicksP0.js";
import "./trash-9-gyJvGZ.js";
import "./server-middleware-C3BRst0X.js";
import "./accounts-fZUHTzqA.js";
import "./accounts-Bso9KOTU.js";
import "./logging-xYH6GmRT.js";
import "./accounts-OddzPdQ6.js";
import "./paths-BoNnI0IY.js";
import "./chat-envelope-C9vncoSN.js";
import "./tool-images-Yi19DXNT.js";
import "./tool-display-UQpRiLW1.js";
import "./commands-PPn4IGbA.js";
import "./commands-registry-BHnndXec.js";
import "./client-DPuEGSE_.js";
import "./call-CqTAcmXH.js";
import "./pairing-token-Dz_8pP2A.js";
import { t as formatDocsLink } from "./links-B0L7hhCO.js";
import { t as parseTimeoutMs } from "./parse-timeout-zNJBr1fY.js";
import "./resolve-configured-secret-input-string-CNG-K_Kw.js";
import { t as runTui } from "./tui--MicXcfv.js";

//#region src/cli/tui-cli.ts
function registerTuiCli(program) {
	program.command("tui").description("Open a terminal UI connected to the Gateway").option("--url <url>", "Gateway WebSocket URL (defaults to gateway.remote.url when configured)").option("--token <token>", "Gateway token (if required)").option("--password <password>", "Gateway password (if required)").option("--session <key>", "Session key (default: \"main\", or \"global\" when scope is global)").option("--deliver", "Deliver assistant replies", false).option("--thinking <level>", "Thinking level override").option("--message <text>", "Send an initial message after connecting").option("--timeout-ms <ms>", "Agent timeout in ms (defaults to agents.defaults.timeoutSeconds)").option("--history-limit <n>", "History entries to load", "200").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/tui", "docs.openclaw.ai/cli/tui")}\n`).action(async (opts) => {
		try {
			const timeoutMs = parseTimeoutMs(opts.timeoutMs);
			if (opts.timeoutMs !== void 0 && timeoutMs === void 0) defaultRuntime.error(`warning: invalid --timeout-ms "${String(opts.timeoutMs)}"; ignoring`);
			const historyLimit = Number.parseInt(String(opts.historyLimit ?? "200"), 10);
			await runTui({
				url: opts.url,
				token: opts.token,
				password: opts.password,
				session: opts.session,
				deliver: Boolean(opts.deliver),
				thinking: opts.thinking,
				message: opts.message,
				timeoutMs,
				historyLimit: Number.isNaN(historyLimit) ? void 0 : historyLimit
			});
		} catch (err) {
			defaultRuntime.error(String(err));
			defaultRuntime.exit(1);
		}
	});
}

//#endregion
export { registerTuiCli };