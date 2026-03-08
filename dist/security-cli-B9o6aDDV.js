import { g as resolveStateDir, m as resolveOAuthDir, o as resolveConfigPath } from "./paths-BBP4yd-2.js";
import { f as isRich, p as theme } from "./globals-DyWRcjQY.js";
import { S as shortenHomePath, x as shortenHomeInString } from "./utils-xFiJOAuL.js";
import { d as resolveDefaultAgentId } from "./agent-scope-C_RF521q.js";
import { d as defaultRuntime } from "./subsystem-D5pRlZe-.js";
import { c as normalizeAgentId, g as DEFAULT_ACCOUNT_ID } from "./session-key-CIXZm7v4.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DHGbafYr.js";
import { n as runExec } from "./exec-DruQEXPV.js";
import { $t as loadConfig, Jt as formatIcaclsResetCommand, Qt as createConfigIO, qt as createIcaclsResetCommand } from "./model-selection-BaeHlT6A.js";
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
import "./commands-PPn4IGbA.js";
import "./client-DPuEGSE_.js";
import "./call-CqTAcmXH.js";
import "./pairing-token-Dz_8pP2A.js";
import "./exec-approvals-allowlist-DdSRN6ci.js";
import "./exec-safe-bin-runtime-policy-DbyyuUj-.js";
import { i as readChannelAllowFromStore } from "./pairing-store-B_ho1sqi.js";
import "./read-only-account-inspect-qEo7wkha.js";
import "./workspace-dirs-FUjBTXbC.js";
import { t as formatDocsLink } from "./links-B0L7hhCO.js";
import { t as formatHelpExamples } from "./help-format-Dbqi5yWh.js";
import "./dangerous-tools-lwpZk6nY.js";
import "./skill-scanner-CP1gVl7O.js";
import "./probe-7M6jnKNV.js";
import "./node-command-policy-DzUXtbnH.js";
import { r as collectIncludePathsRecursive, t as runSecurityAudit } from "./audit-KQM1clYB.js";
import path from "node:path";
import fs from "node:fs/promises";

//#region src/security/fix.ts
async function safeChmod(params) {
	try {
		const st = await fs.lstat(params.path);
		if (st.isSymbolicLink()) return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: false,
			skipped: "symlink"
		};
		if (params.require === "dir" && !st.isDirectory()) return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: false,
			skipped: "not-a-directory"
		};
		if (params.require === "file" && !st.isFile()) return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: false,
			skipped: "not-a-file"
		};
		if ((st.mode & 511) === params.mode) return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: false,
			skipped: "already"
		};
		await fs.chmod(params.path, params.mode);
		return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: true
		};
	} catch (err) {
		if (err.code === "ENOENT") return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: false,
			skipped: "missing"
		};
		return {
			kind: "chmod",
			path: params.path,
			mode: params.mode,
			ok: false,
			error: String(err)
		};
	}
}
async function safeAclReset(params) {
	const display = formatIcaclsResetCommand(params.path, {
		isDir: params.require === "dir",
		env: params.env
	});
	try {
		const st = await fs.lstat(params.path);
		if (st.isSymbolicLink()) return {
			kind: "icacls",
			path: params.path,
			command: display,
			ok: false,
			skipped: "symlink"
		};
		if (params.require === "dir" && !st.isDirectory()) return {
			kind: "icacls",
			path: params.path,
			command: display,
			ok: false,
			skipped: "not-a-directory"
		};
		if (params.require === "file" && !st.isFile()) return {
			kind: "icacls",
			path: params.path,
			command: display,
			ok: false,
			skipped: "not-a-file"
		};
		const cmd = createIcaclsResetCommand(params.path, {
			isDir: st.isDirectory(),
			env: params.env
		});
		if (!cmd) return {
			kind: "icacls",
			path: params.path,
			command: display,
			ok: false,
			skipped: "missing-user"
		};
		await (params.exec ?? runExec)(cmd.command, cmd.args);
		return {
			kind: "icacls",
			path: params.path,
			command: cmd.display,
			ok: true
		};
	} catch (err) {
		if (err.code === "ENOENT") return {
			kind: "icacls",
			path: params.path,
			command: display,
			ok: false,
			skipped: "missing"
		};
		return {
			kind: "icacls",
			path: params.path,
			command: display,
			ok: false,
			error: String(err)
		};
	}
}
function setGroupPolicyAllowlist(params) {
	if (!params.cfg.channels) return;
	const section = params.cfg.channels[params.channel];
	if (!section || typeof section !== "object") return;
	if (section.groupPolicy === "open") {
		section.groupPolicy = "allowlist";
		params.changes.push(`channels.${params.channel}.groupPolicy=open -> allowlist`);
		params.policyFlips.add(`channels.${params.channel}.`);
	}
	const accounts = section.accounts;
	if (!accounts || typeof accounts !== "object") return;
	for (const [accountId, accountValue] of Object.entries(accounts)) {
		if (!accountId) continue;
		if (!accountValue || typeof accountValue !== "object") continue;
		const account = accountValue;
		if (account.groupPolicy === "open") {
			account.groupPolicy = "allowlist";
			params.changes.push(`channels.${params.channel}.accounts.${accountId}.groupPolicy=open -> allowlist`);
			params.policyFlips.add(`channels.${params.channel}.accounts.${accountId}.`);
		}
	}
}
function setWhatsAppGroupAllowFromFromStore(params) {
	const section = params.cfg.channels?.whatsapp;
	if (!section || typeof section !== "object") return;
	if (params.storeAllowFrom.length === 0) return;
	const maybeApply = (prefix, obj) => {
		if (!params.policyFlips.has(prefix)) return;
		const allowFrom = Array.isArray(obj.allowFrom) ? obj.allowFrom : [];
		const groupAllowFrom = Array.isArray(obj.groupAllowFrom) ? obj.groupAllowFrom : [];
		if (allowFrom.length > 0) return;
		if (groupAllowFrom.length > 0) return;
		obj.groupAllowFrom = params.storeAllowFrom;
		params.changes.push(`${prefix}groupAllowFrom=pairing-store`);
	};
	maybeApply("channels.whatsapp.", section);
	const accounts = section.accounts;
	if (!accounts || typeof accounts !== "object") return;
	for (const [accountId, accountValue] of Object.entries(accounts)) {
		if (!accountValue || typeof accountValue !== "object") continue;
		const account = accountValue;
		maybeApply(`channels.whatsapp.accounts.${accountId}.`, account);
	}
}
function applyConfigFixes(params) {
	const next = structuredClone(params.cfg ?? {});
	const changes = [];
	const policyFlips = /* @__PURE__ */ new Set();
	if (next.logging?.redactSensitive === "off") {
		next.logging = {
			...next.logging,
			redactSensitive: "tools"
		};
		changes.push("logging.redactSensitive=off -> \"tools\"");
	}
	for (const channel of [
		"telegram",
		"whatsapp",
		"discord",
		"signal",
		"imessage",
		"slack",
		"msteams"
	]) setGroupPolicyAllowlist({
		cfg: next,
		channel,
		changes,
		policyFlips
	});
	return {
		cfg: next,
		changes,
		policyFlips
	};
}
async function chmodCredentialsAndAgentState(params) {
	const credsDir = resolveOAuthDir(params.env, params.stateDir);
	params.actions.push(await safeChmod({
		path: credsDir,
		mode: 448,
		require: "dir"
	}));
	const credsEntries = await fs.readdir(credsDir, { withFileTypes: true }).catch(() => []);
	for (const entry of credsEntries) {
		if (!entry.isFile()) continue;
		if (!entry.name.endsWith(".json")) continue;
		const p = path.join(credsDir, entry.name);
		params.actions.push(await safeChmod({
			path: p,
			mode: 384,
			require: "file"
		}));
	}
	const ids = /* @__PURE__ */ new Set();
	ids.add(resolveDefaultAgentId(params.cfg));
	const list = Array.isArray(params.cfg.agents?.list) ? params.cfg.agents?.list : [];
	for (const agent of list ?? []) {
		if (!agent || typeof agent !== "object") continue;
		const id = typeof agent.id === "string" ? agent.id.trim() : "";
		if (id) ids.add(id);
	}
	for (const agentId of ids) {
		const normalizedAgentId = normalizeAgentId(agentId);
		const agentRoot = path.join(params.stateDir, "agents", normalizedAgentId);
		const agentDir = path.join(agentRoot, "agent");
		const sessionsDir = path.join(agentRoot, "sessions");
		params.actions.push(await safeChmod({
			path: agentRoot,
			mode: 448,
			require: "dir"
		}));
		params.actions.push(await params.applyPerms({
			path: agentDir,
			mode: 448,
			require: "dir"
		}));
		const authPath = path.join(agentDir, "auth-profiles.json");
		params.actions.push(await params.applyPerms({
			path: authPath,
			mode: 384,
			require: "file"
		}));
		params.actions.push(await params.applyPerms({
			path: sessionsDir,
			mode: 448,
			require: "dir"
		}));
		const storePath = path.join(sessionsDir, "sessions.json");
		params.actions.push(await params.applyPerms({
			path: storePath,
			mode: 384,
			require: "file"
		}));
		const sessionEntries = await fs.readdir(sessionsDir, { withFileTypes: true }).catch(() => []);
		for (const entry of sessionEntries) {
			if (!entry.isFile()) continue;
			if (!entry.name.endsWith(".jsonl")) continue;
			const p = path.join(sessionsDir, entry.name);
			params.actions.push(await params.applyPerms({
				path: p,
				mode: 384,
				require: "file"
			}));
		}
	}
}
async function fixSecurityFootguns(opts) {
	const env = opts?.env ?? process.env;
	const platform = opts?.platform ?? process.platform;
	const exec = opts?.exec ?? runExec;
	const isWindows = platform === "win32";
	const stateDir = opts?.stateDir ?? resolveStateDir(env);
	const configPath = opts?.configPath ?? resolveConfigPath(env, stateDir);
	const actions = [];
	const errors = [];
	const io = createConfigIO({
		env,
		configPath
	});
	const snap = await io.readConfigFileSnapshot();
	if (!snap.valid) errors.push(...snap.issues.map((i) => `${i.path}: ${i.message}`));
	let configWritten = false;
	let changes = [];
	if (snap.valid) {
		const fixed = applyConfigFixes({
			cfg: snap.config,
			env
		});
		changes = fixed.changes;
		const whatsappStoreAllowFrom = await readChannelAllowFromStore("whatsapp", env, DEFAULT_ACCOUNT_ID).catch(() => []);
		if (whatsappStoreAllowFrom.length > 0) setWhatsAppGroupAllowFromFromStore({
			cfg: fixed.cfg,
			storeAllowFrom: whatsappStoreAllowFrom,
			changes,
			policyFlips: fixed.policyFlips
		});
		if (changes.length > 0) try {
			await io.writeConfigFile(fixed.cfg);
			configWritten = true;
		} catch (err) {
			errors.push(`writeConfigFile failed: ${String(err)}`);
		}
	}
	const applyPerms = (params) => isWindows ? safeAclReset({
		path: params.path,
		require: params.require,
		env,
		exec
	}) : safeChmod({
		path: params.path,
		mode: params.mode,
		require: params.require
	});
	actions.push(await applyPerms({
		path: stateDir,
		mode: 448,
		require: "dir"
	}));
	actions.push(await applyPerms({
		path: configPath,
		mode: 384,
		require: "file"
	}));
	if (snap.exists) {
		const includePaths = await collectIncludePathsRecursive({
			configPath: snap.path,
			parsed: snap.parsed
		}).catch(() => []);
		for (const p of includePaths) actions.push(await applyPerms({
			path: p,
			mode: 384,
			require: "file"
		}));
	}
	await chmodCredentialsAndAgentState({
		env,
		stateDir,
		cfg: snap.config ?? {},
		actions,
		applyPerms
	}).catch((err) => {
		errors.push(`chmodCredentialsAndAgentState failed: ${String(err)}`);
	});
	return {
		ok: errors.length === 0,
		stateDir,
		configPath,
		configWritten,
		changes,
		actions,
		errors
	};
}

//#endregion
//#region src/cli/security-cli.ts
function formatSummary(summary) {
	const rich = isRich();
	const c = summary.critical;
	const w = summary.warn;
	const i = summary.info;
	const parts = [];
	parts.push(rich ? theme.error(`${c} critical`) : `${c} critical`);
	parts.push(rich ? theme.warn(`${w} warn`) : `${w} warn`);
	parts.push(rich ? theme.muted(`${i} info`) : `${i} info`);
	return parts.join(" · ");
}
function registerSecurityCli(program) {
	program.command("security").description("Audit local config and state for common security foot-guns").addHelpText("after", () => `\n${theme.heading("Examples:")}\n${formatHelpExamples([
		["openclaw security audit", "Run a local security audit."],
		["openclaw security audit --deep", "Include best-effort live Gateway probe checks."],
		["openclaw security audit --fix", "Apply safe remediations and file-permission fixes."],
		["openclaw security audit --json", "Output machine-readable JSON."]
	])}\n\n${theme.muted("Docs:")} ${formatDocsLink("/cli/security", "docs.openclaw.ai/cli/security")}\n`).command("audit").description("Audit config + local state for common security foot-guns").option("--deep", "Attempt live Gateway probe (best-effort)", false).option("--fix", "Apply safe fixes (tighten defaults + chmod state/config)", false).option("--json", "Print JSON", false).action(async (opts) => {
		const fixResult = opts.fix ? await fixSecurityFootguns().catch((_err) => null) : null;
		const report = await runSecurityAudit({
			config: loadConfig(),
			deep: Boolean(opts.deep),
			includeFilesystem: true,
			includeChannelSecurity: true
		});
		if (opts.json) {
			defaultRuntime.log(JSON.stringify(fixResult ? {
				fix: fixResult,
				report
			} : report, null, 2));
			return;
		}
		const rich = isRich();
		const heading = (text) => rich ? theme.heading(text) : text;
		const muted = (text) => rich ? theme.muted(text) : text;
		const lines = [];
		lines.push(heading("OpenClaw security audit"));
		lines.push(muted(`Summary: ${formatSummary(report.summary)}`));
		lines.push(muted(`Run deeper: ${formatCliCommand("openclaw security audit --deep")}`));
		if (opts.fix) {
			lines.push(muted(`Fix: ${formatCliCommand("openclaw security audit --fix")}`));
			if (!fixResult) lines.push(muted("Fixes: failed to apply (unexpected error)"));
			else if (fixResult.errors.length === 0 && fixResult.changes.length === 0 && fixResult.actions.every((a) => !a.ok)) lines.push(muted("Fixes: no changes applied"));
			else {
				lines.push("");
				lines.push(heading("FIX"));
				for (const change of fixResult.changes) lines.push(muted(`  ${shortenHomeInString(change)}`));
				for (const action of fixResult.actions) {
					if (action.kind === "chmod") {
						const mode = action.mode.toString(8).padStart(3, "0");
						if (action.ok) lines.push(muted(`  chmod ${mode} ${shortenHomePath(action.path)}`));
						else if (action.skipped) lines.push(muted(`  skip chmod ${mode} ${shortenHomePath(action.path)} (${action.skipped})`));
						else if (action.error) lines.push(muted(`  chmod ${mode} ${shortenHomePath(action.path)} failed: ${action.error}`));
						continue;
					}
					const command = shortenHomeInString(action.command);
					if (action.ok) lines.push(muted(`  ${command}`));
					else if (action.skipped) lines.push(muted(`  skip ${command} (${action.skipped})`));
					else if (action.error) lines.push(muted(`  ${command} failed: ${action.error}`));
				}
				if (fixResult.errors.length > 0) for (const err of fixResult.errors) lines.push(muted(`  error: ${shortenHomeInString(err)}`));
			}
		}
		const bySeverity = (sev) => report.findings.filter((f) => f.severity === sev);
		const render = (sev) => {
			const list = bySeverity(sev);
			if (list.length === 0) return;
			const label = sev === "critical" ? rich ? theme.error("CRITICAL") : "CRITICAL" : sev === "warn" ? rich ? theme.warn("WARN") : "WARN" : rich ? theme.muted("INFO") : "INFO";
			lines.push("");
			lines.push(heading(label));
			for (const f of list) {
				lines.push(`${theme.muted(f.checkId)} ${f.title}`);
				lines.push(`  ${f.detail}`);
				if (f.remediation?.trim()) lines.push(`  ${muted(`Fix: ${f.remediation.trim()}`)}`);
			}
		};
		render("critical");
		render("warn");
		render("info");
		defaultRuntime.log(lines.join("\n"));
	});
}

//#endregion
export { registerSecurityCli };