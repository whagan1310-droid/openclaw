import "./paths-BBP4yd-2.js";
import { L as shouldMigrateStateFromPath, d as colorize, f as isRich, p as theme } from "./globals-DyWRcjQY.js";
import { S as shortenHomePath } from "./utils-xFiJOAuL.js";
import "./agent-scope-C_RF521q.js";
import "./subsystem-D5pRlZe-.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DHGbafYr.js";
import "./exec-DruQEXPV.js";
import { tn as readConfigFileSnapshot } from "./model-selection-BaeHlT6A.js";
import "./github-copilot-token-b6kJVrW-.js";
import { t as formatCliCommand } from "./command-format-Gp1OUMPH.js";
import "./boolean-BsqeuxE6.js";
import "./env-BCNBCy-T.js";
import "./host-env-security-DkAVVuaw.js";
import "./registry-CEJSZAKm.js";
import "./manifest-registry-Ds8wMsKE.js";
import "./dock-BI9_dwQi.js";
import "./message-channel-CSTlX5lG.js";
import "./plugins-DD42H5-v.js";
import "./sessions-DL9FheWJ.js";
import "./tailnet-D1FN3bC3.js";
import "./ws-CtzAmMCA.js";
import "./accounts-fZUHTzqA.js";
import "./accounts-Bso9KOTU.js";
import "./logging-xYH6GmRT.js";
import "./accounts-OddzPdQ6.js";
import "./paths-BoNnI0IY.js";
import "./chat-envelope-C9vncoSN.js";
import "./client-DPuEGSE_.js";
import "./call-CqTAcmXH.js";
import "./pairing-token-Dz_8pP2A.js";
import "./exec-approvals-allowlist-DdSRN6ci.js";
import "./exec-safe-bin-runtime-policy-DbyyuUj-.js";
import "./plugin-auto-enable-jZIG-i4G.js";
import "./pairing-store-B_ho1sqi.js";
import "./runtime-config-collectors-CvVyFBgq.js";
import "./command-secret-targets-DcsK8ZYD.js";
import "./prompt-style-BgFv5fyL.js";
import "./note-k8AbeMaN.js";
import { n as formatConfigIssueLines } from "./issue-format-DH2qIw2f.js";
import { t as loadAndMaybeMigrateDoctorConfig } from "./doctor-config-flow-CBdcVxGS.js";

//#region src/cli/program/config-guard.ts
const ALLOWED_INVALID_COMMANDS = new Set([
	"doctor",
	"logs",
	"health",
	"help",
	"status"
]);
const ALLOWED_INVALID_GATEWAY_SUBCOMMANDS = new Set([
	"status",
	"probe",
	"health",
	"discover",
	"call",
	"install",
	"uninstall",
	"start",
	"stop",
	"restart"
]);
let didRunDoctorConfigFlow = false;
let configSnapshotPromise = null;
function resetConfigGuardStateForTests() {
	didRunDoctorConfigFlow = false;
	configSnapshotPromise = null;
}
async function getConfigSnapshot() {
	if (process.env.VITEST === "true") return readConfigFileSnapshot();
	configSnapshotPromise ??= readConfigFileSnapshot();
	return configSnapshotPromise;
}
async function ensureConfigReady(params) {
	const commandPath = params.commandPath ?? [];
	if (!didRunDoctorConfigFlow && shouldMigrateStateFromPath(commandPath)) {
		didRunDoctorConfigFlow = true;
		const runDoctorConfigFlow = async () => loadAndMaybeMigrateDoctorConfig({
			options: { nonInteractive: true },
			confirm: async () => false
		});
		if (!params.suppressDoctorStdout) await runDoctorConfigFlow();
		else {
			const originalStdoutWrite = process.stdout.write.bind(process.stdout);
			const originalSuppressNotes = process.env.OPENCLAW_SUPPRESS_NOTES;
			process.stdout.write = (() => true);
			process.env.OPENCLAW_SUPPRESS_NOTES = "1";
			try {
				await runDoctorConfigFlow();
			} finally {
				process.stdout.write = originalStdoutWrite;
				if (originalSuppressNotes === void 0) delete process.env.OPENCLAW_SUPPRESS_NOTES;
				else process.env.OPENCLAW_SUPPRESS_NOTES = originalSuppressNotes;
			}
		}
	}
	const snapshot = await getConfigSnapshot();
	const commandName = commandPath[0];
	const subcommandName = commandPath[1];
	const allowInvalid = commandName ? ALLOWED_INVALID_COMMANDS.has(commandName) || commandName === "gateway" && subcommandName && ALLOWED_INVALID_GATEWAY_SUBCOMMANDS.has(subcommandName) : false;
	const issues = snapshot.exists && !snapshot.valid ? formatConfigIssueLines(snapshot.issues, "-", { normalizeRoot: true }) : [];
	const legacyIssues = snapshot.legacyIssues.length > 0 ? formatConfigIssueLines(snapshot.legacyIssues, "-") : [];
	if (!(snapshot.exists && !snapshot.valid)) return;
	const rich = isRich();
	const muted = (value) => colorize(rich, theme.muted, value);
	const error = (value) => colorize(rich, theme.error, value);
	const heading = (value) => colorize(rich, theme.heading, value);
	const commandText = (value) => colorize(rich, theme.command, value);
	params.runtime.error(heading("Config invalid"));
	params.runtime.error(`${muted("File:")} ${muted(shortenHomePath(snapshot.path))}`);
	if (issues.length > 0) {
		params.runtime.error(muted("Problem:"));
		params.runtime.error(issues.map((issue) => `  ${error(issue)}`).join("\n"));
	}
	if (legacyIssues.length > 0) {
		params.runtime.error(muted("Legacy config keys detected:"));
		params.runtime.error(legacyIssues.map((issue) => `  ${error(issue)}`).join("\n"));
	}
	params.runtime.error("");
	params.runtime.error(`${muted("Run:")} ${commandText(formatCliCommand("openclaw doctor --fix"))}`);
	if (!allowInvalid) params.runtime.exit(1);
}
const __test__ = { resetConfigGuardStateForTests };

//#endregion
export { __test__, ensureConfigReady };