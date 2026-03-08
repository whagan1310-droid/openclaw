import { a as resolveAgentDir, c as resolveAgentWorkspaceDir, l as resolveDefaultAgentId, o as resolveAgentEffectiveModelPrimary } from "./run-with-concurrency-C_CE05l4.js";
import "./paths-C6TxBCvO.js";
import { t as createSubsystemLogger } from "./subsystem-W834z9Wa.js";
import "./workspace-pHGffow-.js";
import "./logger-D4RcXHR-.js";
import { Tr as DEFAULT_PROVIDER, l as parseModelRef, wr as DEFAULT_MODEL } from "./model-selection-BI58zgyw.js";
import "./github-copilot-token-D13V9YBz.js";
import "./legacy-names-Bkl4tjN-.js";
import "./thinking-DDO4j9rC.js";
import "./tokens-Cyi-NbsV.js";
import { t as runEmbeddedPiAgent } from "./pi-embedded-CMULkb1z.js";
import "./accounts-BH8pDk9r.js";
import "./plugins--L1Azplm.js";
import "./send-CnclbAbb.js";
import "./send-CqUG6BWq.js";
import "./deliver-l9gW0Mte.js";
import "./diagnostic-C44YRSu5.js";
import "./accounts-hTyc2FgV.js";
import "./image-ops-D3XDvn0o.js";
import "./send-CXdTj6tV.js";
import "./pi-model-discovery-_Vup86TF.js";
import "./pi-embedded-helpers-7IJhENfI.js";
import "./chrome-DoImAA91.js";
import "./frontmatter-BFHzrAY7.js";
import "./skills-DZa9e6P1.js";
import "./path-alias-guards-CfWf2Gqa.js";
import "./redact-DGz6yigq.js";
import "./errors-DDrhcWHi.js";
import "./fs-safe-CzzA6NyV.js";
import "./proxy-env-xp3c1fK8.js";
import "./store-Bv_njIFN.js";
import "./accounts-BxrwQsJd.js";
import "./paths-BCj7Axtv.js";
import "./tool-images-BjtzgbP_.js";
import "./image-DEVruB_i.js";
import "./audio-transcription-runner-ByOzuB3E.js";
import "./fetch-DK5bYmSn.js";
import "./fetch-guard-DOq_LtZw.js";
import "./api-key-rotation-3XeDUVw_.js";
import "./proxy-fetch-ChfJDZwG.js";
import "./ir-D58n8zRv.js";
import "./render-DW7AcFdD.js";
import "./target-errors-CMuHXQ8m.js";
import "./commands-registry-K3bIVADD.js";
import "./skill-commands-OPA3HiS0.js";
import "./fetch-BfuG8uZ8.js";
import "./channel-activity-kTQ1sZX5.js";
import "./tables-BsEIvRch.js";
import "./send-DmyWmehl.js";
import "./outbound-attachment-CkdLiHjr.js";
import "./send-BL1_TLli.js";
import "./proxy-CecQTx_Z.js";
import "./manager-BY9SmtIm.js";
import "./query-expansion-BgrH0Hrf.js";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

//#region src/hooks/llm-slug-generator.ts
/**
* LLM-based slug generator for session memory filenames
*/
const log = createSubsystemLogger("llm-slug-generator");
/**
* Generate a short 1-2 word filename slug from session content using LLM
*/
async function generateSlugViaLLM(params) {
	let tempSessionFile = null;
	try {
		const agentId = resolveDefaultAgentId(params.cfg);
		const workspaceDir = resolveAgentWorkspaceDir(params.cfg, agentId);
		const agentDir = resolveAgentDir(params.cfg, agentId);
		const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "openclaw-slug-"));
		tempSessionFile = path.join(tempDir, "session.jsonl");
		const prompt = `Based on this conversation, generate a short 1-2 word filename slug (lowercase, hyphen-separated, no file extension).

Conversation summary:
${params.sessionContent.slice(0, 2e3)}

Reply with ONLY the slug, nothing else. Examples: "vendor-pitch", "api-design", "bug-fix"`;
		const modelRef = resolveAgentEffectiveModelPrimary(params.cfg, agentId);
		const parsed = modelRef ? parseModelRef(modelRef, DEFAULT_PROVIDER) : null;
		const provider = parsed?.provider ?? DEFAULT_PROVIDER;
		const model = parsed?.model ?? DEFAULT_MODEL;
		const result = await runEmbeddedPiAgent({
			sessionId: `slug-generator-${Date.now()}`,
			sessionKey: "temp:slug-generator",
			agentId,
			sessionFile: tempSessionFile,
			workspaceDir,
			agentDir,
			config: params.cfg,
			prompt,
			provider,
			model,
			timeoutMs: 15e3,
			runId: `slug-gen-${Date.now()}`
		});
		if (result.payloads && result.payloads.length > 0) {
			const text = result.payloads[0]?.text;
			if (text) return text.trim().toLowerCase().replace(/[^a-z0-9-]/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "").slice(0, 30) || null;
		}
		return null;
	} catch (err) {
		const message = err instanceof Error ? err.stack ?? err.message : String(err);
		log.error(`Failed to generate slug: ${message}`);
		return null;
	} finally {
		if (tempSessionFile) try {
			await fs.rm(path.dirname(tempSessionFile), {
				recursive: true,
				force: true
			});
		} catch {}
	}
}

//#endregion
export { generateSlugViaLLM };