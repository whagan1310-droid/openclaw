import { p as theme } from "./globals-d3aR1MYC.js";
import "./paths-BMo6kTge.js";
import { d as defaultRuntime } from "./subsystem-Cfn2Pryx.js";
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
import "./dock-sYVOKHlm.js";
import "./accounts-R3q-kjOQ.js";
import "./plugins-DRFogx00.js";
import "./logging-CY-Q5cwf.js";
import "./accounts-CKHrdz4J.js";
import "./image-ops-D7tZ0deS.js";
import "./message-channel-DTk937hY.js";
import "./pi-embedded-helpers-Bv8-njDx.js";
import "./sandbox-dCWvM5iw.js";
import "./tool-catalog-U5Hs0dNI.js";
import "./chrome-BRGJugRp.js";
import "./tailscale-Bm1Sl4zA.js";
import "./tailnet-BXLAgtlT.js";
import "./ws-Da560NJf.js";
import "./auth-vwV9EhNu.js";
import "./server-context-Os1yOTFa.js";
import "./frontmatter-DznzkPUb.js";
import "./env-overrides-ClebeSGi.js";
import "./path-alias-guards-B7T1EGZ9.js";
import "./skills-BCL68CAD.js";
import "./paths-4X-2N43i.js";
import "./redact-IU7JtJUp.js";
import "./errors-BPptd15U.js";
import "./fs-safe-DdGAi4U9.js";
import "./proxy-env-CTH3nMPY.js";
import "./store-OT87hlAd.js";
import "./ports-TdGFisXq.js";
import "./trash-DHeQIyU7.js";
import "./server-middleware-Bsz_1MtV.js";
import "./sessions-G4D58Ojj.js";
import "./accounts-viX3i-Kr.js";
import "./paths-CCvn4cNJ.js";
import "./chat-envelope-BBXhi7A0.js";
import "./tool-images-D8-CCKu5.js";
import "./thinking-DaklPihx.js";
import "./tool-display-DNMp8JVO.js";
import "./commands-i-ub-epr.js";
import "./commands-registry-UiH_wyVT.js";
import "./client-B9xXRY-r.js";
import "./call-C79Luiuk.js";
import "./pairing-token-CCWPBg5t.js";
import { t as parseTimeoutMs } from "./parse-timeout-widuTpq9.js";
import { t as formatDocsLink } from "./links-BVDZVrXu.js";
import "./resolve-configured-secret-input-string-D1i2aPBq.js";
import { t as runTui } from "./tui-B7W-qRRJ.js";

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