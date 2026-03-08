import "./run-with-concurrency-C_CE05l4.js";
import "./paths-C6TxBCvO.js";
import { p as shouldLogVerbose, u as logVerbose } from "./subsystem-W834z9Wa.js";
import "./workspace-pHGffow-.js";
import "./logger-D4RcXHR-.js";
import "./model-selection-BI58zgyw.js";
import "./github-copilot-token-D13V9YBz.js";
import "./legacy-names-Bkl4tjN-.js";
import "./thinking-DDO4j9rC.js";
import "./accounts-BH8pDk9r.js";
import "./plugins--L1Azplm.js";
import "./accounts-hTyc2FgV.js";
import "./image-ops-D3XDvn0o.js";
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
import { g as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-ByOzuB3E.js";
import "./fetch-DK5bYmSn.js";
import "./fetch-guard-DOq_LtZw.js";
import "./api-key-rotation-3XeDUVw_.js";
import "./proxy-fetch-ChfJDZwG.js";

//#region src/media-understanding/audio-preflight.ts
/**
* Transcribes the first audio attachment BEFORE mention checking.
* This allows voice notes to be processed in group chats with requireMention: true.
* Returns the transcript or undefined if transcription fails or no audio is found.
*/
async function transcribeFirstAudio(params) {
	const { ctx, cfg } = params;
	const audioConfig = cfg.tools?.media?.audio;
	if (!audioConfig || audioConfig.enabled === false) return;
	const attachments = normalizeMediaAttachments(ctx);
	if (!attachments || attachments.length === 0) return;
	const firstAudio = attachments.find((att) => att && isAudioAttachment(att) && !att.alreadyTranscribed);
	if (!firstAudio) return;
	if (shouldLogVerbose()) logVerbose(`audio-preflight: transcribing attachment ${firstAudio.index} for mention check`);
	try {
		const { transcript } = await runAudioTranscription({
			ctx,
			cfg,
			attachments,
			agentDir: params.agentDir,
			providers: params.providers,
			activeModel: params.activeModel,
			localPathRoots: resolveMediaAttachmentLocalRoots({
				cfg,
				ctx
			})
		});
		if (!transcript) return;
		firstAudio.alreadyTranscribed = true;
		if (shouldLogVerbose()) logVerbose(`audio-preflight: transcribed ${transcript.length} chars from attachment ${firstAudio.index}`);
		return transcript;
	} catch (err) {
		if (shouldLogVerbose()) logVerbose(`audio-preflight: transcription failed: ${String(err)}`);
		return;
	}
}

//#endregion
export { transcribeFirstAudio };