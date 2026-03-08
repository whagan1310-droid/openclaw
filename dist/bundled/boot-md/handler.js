import { c as resolveAgentWorkspaceDir, r as listAgentIds } from "../../run-with-concurrency-C_CE05l4.js";
import "../../paths-C6TxBCvO.js";
import { i as defaultRuntime, t as createSubsystemLogger } from "../../subsystem-W834z9Wa.js";
import { B as resolveAgentIdFromSessionKey } from "../../workspace-pHGffow-.js";
import "../../logger-D4RcXHR-.js";
import "../../model-selection-BI58zgyw.js";
import "../../github-copilot-token-D13V9YBz.js";
import { a as isGatewayStartupEvent } from "../../legacy-names-Bkl4tjN-.js";
import "../../thinking-DDO4j9rC.js";
import { n as SILENT_REPLY_TOKEN } from "../../tokens-Cyi-NbsV.js";
import { o as agentCommand, s as createDefaultDeps } from "../../pi-embedded-CMULkb1z.js";
import "../../accounts-BH8pDk9r.js";
import "../../plugins--L1Azplm.js";
import "../../send-CnclbAbb.js";
import "../../send-CqUG6BWq.js";
import "../../deliver-l9gW0Mte.js";
import "../../diagnostic-C44YRSu5.js";
import "../../accounts-hTyc2FgV.js";
import "../../image-ops-D3XDvn0o.js";
import "../../send-CXdTj6tV.js";
import "../../pi-model-discovery-_Vup86TF.js";
import { Dt as resolveMainSessionKey, J as updateSessionStore, Tt as resolveAgentMainSessionKey, W as loadSessionStore } from "../../pi-embedded-helpers-7IJhENfI.js";
import "../../chrome-DoImAA91.js";
import "../../frontmatter-BFHzrAY7.js";
import "../../skills-DZa9e6P1.js";
import "../../path-alias-guards-CfWf2Gqa.js";
import "../../redact-DGz6yigq.js";
import "../../errors-DDrhcWHi.js";
import "../../fs-safe-CzzA6NyV.js";
import "../../proxy-env-xp3c1fK8.js";
import "../../store-Bv_njIFN.js";
import "../../accounts-BxrwQsJd.js";
import { s as resolveStorePath } from "../../paths-BCj7Axtv.js";
import "../../tool-images-BjtzgbP_.js";
import "../../image-DEVruB_i.js";
import "../../audio-transcription-runner-ByOzuB3E.js";
import "../../fetch-DK5bYmSn.js";
import "../../fetch-guard-DOq_LtZw.js";
import "../../api-key-rotation-3XeDUVw_.js";
import "../../proxy-fetch-ChfJDZwG.js";
import "../../ir-D58n8zRv.js";
import "../../render-DW7AcFdD.js";
import "../../target-errors-CMuHXQ8m.js";
import "../../commands-registry-K3bIVADD.js";
import "../../skill-commands-OPA3HiS0.js";
import "../../fetch-BfuG8uZ8.js";
import "../../channel-activity-kTQ1sZX5.js";
import "../../tables-BsEIvRch.js";
import "../../send-DmyWmehl.js";
import "../../outbound-attachment-CkdLiHjr.js";
import "../../send-BL1_TLli.js";
import "../../proxy-CecQTx_Z.js";
import "../../manager-BY9SmtIm.js";
import "../../query-expansion-BgrH0Hrf.js";
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

//#region src/gateway/boot.ts
function generateBootSessionId() {
	return `boot-${(/* @__PURE__ */ new Date()).toISOString().replace(/[:.]/g, "-").replace("T", "_").replace("Z", "")}-${crypto.randomUUID().slice(0, 8)}`;
}
const log$1 = createSubsystemLogger("gateway/boot");
const BOOT_FILENAME = "BOOT.md";
function buildBootPrompt(content) {
	return [
		"You are running a boot check. Follow BOOT.md instructions exactly.",
		"",
		"BOOT.md:",
		content,
		"",
		"If BOOT.md asks you to send a message, use the message tool (action=send with channel + target).",
		"Use the `target` field (not `to`) for message tool destinations.",
		`After sending with the message tool, reply with ONLY: ${SILENT_REPLY_TOKEN}.`,
		`If nothing needs attention, reply with ONLY: ${SILENT_REPLY_TOKEN}.`
	].join("\n");
}
async function loadBootFile(workspaceDir) {
	const bootPath = path.join(workspaceDir, BOOT_FILENAME);
	try {
		const trimmed = (await fs.readFile(bootPath, "utf-8")).trim();
		if (!trimmed) return { status: "empty" };
		return {
			status: "ok",
			content: trimmed
		};
	} catch (err) {
		if (err.code === "ENOENT") return { status: "missing" };
		throw err;
	}
}
function snapshotMainSessionMapping(params) {
	const agentId = resolveAgentIdFromSessionKey(params.sessionKey);
	const storePath = resolveStorePath(params.cfg.session?.store, { agentId });
	try {
		const entry = loadSessionStore(storePath, { skipCache: true })[params.sessionKey];
		if (!entry) return {
			storePath,
			sessionKey: params.sessionKey,
			canRestore: true,
			hadEntry: false
		};
		return {
			storePath,
			sessionKey: params.sessionKey,
			canRestore: true,
			hadEntry: true,
			entry: structuredClone(entry)
		};
	} catch (err) {
		log$1.debug("boot: could not snapshot main session mapping", {
			sessionKey: params.sessionKey,
			error: String(err)
		});
		return {
			storePath,
			sessionKey: params.sessionKey,
			canRestore: false,
			hadEntry: false
		};
	}
}
async function restoreMainSessionMapping(snapshot) {
	if (!snapshot.canRestore) return;
	try {
		await updateSessionStore(snapshot.storePath, (store) => {
			if (snapshot.hadEntry && snapshot.entry) {
				store[snapshot.sessionKey] = snapshot.entry;
				return;
			}
			delete store[snapshot.sessionKey];
		}, { activeSessionKey: snapshot.sessionKey });
		return;
	} catch (err) {
		return err instanceof Error ? err.message : String(err);
	}
}
async function runBootOnce(params) {
	const bootRuntime = {
		log: () => {},
		error: (message) => log$1.error(String(message)),
		exit: defaultRuntime.exit
	};
	let result;
	try {
		result = await loadBootFile(params.workspaceDir);
	} catch (err) {
		const message = err instanceof Error ? err.message : String(err);
		log$1.error(`boot: failed to read ${BOOT_FILENAME}: ${message}`);
		return {
			status: "failed",
			reason: message
		};
	}
	if (result.status === "missing" || result.status === "empty") return {
		status: "skipped",
		reason: result.status
	};
	const sessionKey = params.agentId ? resolveAgentMainSessionKey({
		cfg: params.cfg,
		agentId: params.agentId
	}) : resolveMainSessionKey(params.cfg);
	const message = buildBootPrompt(result.content ?? "");
	const sessionId = generateBootSessionId();
	const mappingSnapshot = snapshotMainSessionMapping({
		cfg: params.cfg,
		sessionKey
	});
	let agentFailure;
	try {
		await agentCommand({
			message,
			sessionKey,
			sessionId,
			deliver: false,
			senderIsOwner: true
		}, bootRuntime, params.deps);
	} catch (err) {
		agentFailure = err instanceof Error ? err.message : String(err);
		log$1.error(`boot: agent run failed: ${agentFailure}`);
	}
	const mappingRestoreFailure = await restoreMainSessionMapping(mappingSnapshot);
	if (mappingRestoreFailure) log$1.error(`boot: failed to restore main session mapping: ${mappingRestoreFailure}`);
	if (!agentFailure && !mappingRestoreFailure) return { status: "ran" };
	return {
		status: "failed",
		reason: [agentFailure ? `agent run failed: ${agentFailure}` : void 0, mappingRestoreFailure ? `mapping restore failed: ${mappingRestoreFailure}` : void 0].filter((part) => Boolean(part)).join("; ")
	};
}

//#endregion
//#region src/hooks/bundled/boot-md/handler.ts
const log = createSubsystemLogger("hooks/boot-md");
const runBootChecklist = async (event) => {
	if (!isGatewayStartupEvent(event)) return;
	if (!event.context.cfg) return;
	const cfg = event.context.cfg;
	const deps = event.context.deps ?? createDefaultDeps();
	const agentIds = listAgentIds(cfg);
	for (const agentId of agentIds) {
		const workspaceDir = resolveAgentWorkspaceDir(cfg, agentId);
		const result = await runBootOnce({
			cfg,
			deps,
			workspaceDir,
			agentId
		});
		if (result.status === "failed") {
			log.warn("boot-md failed for agent startup run", {
				agentId,
				workspaceDir,
				reason: result.reason
			});
			continue;
		}
		if (result.status === "skipped") log.debug("boot-md skipped for agent startup run", {
			agentId,
			workspaceDir,
			reason: result.reason
		});
	}
};

//#endregion
export { runBootChecklist as default };