import "./run-with-concurrency-BdgPUUY-.js";
import "./accounts-BJiJ1olH.js";
import "./paths-MKyEVmEb.js";
import "./github-copilot-token-D5fdS6xD.js";
import "./config-Bq0-9IRt.js";
import { L as logVerbose, z as shouldLogVerbose } from "./logger-COmHOvdm.js";
import "./thinking-jqu0d5mh.js";
import "./image-ops-BeAUismH.js";
import "./pi-embedded-helpers-CUSmK7tU.js";
import "./plugins-NK3Kbpsu.js";
import "./accounts-CHStHsfX.js";
import "./accounts-BuBig3IR.js";
import "./paths-DR30B6cs.js";
import "./redact-DZTeCKgA.js";
import "./errors-x0EvNKYN.js";
import "./path-alias-guards-CtLu-sVZ.js";
import "./fs-safe-CmvP9IFC.js";
import "./ssrf-CZCOeNMj.js";
import "./fetch-guard-CdJjw74d.js";
import "./local-roots-CKYANN_u.js";
import "./tool-images-ByM5teJW.js";
import { f as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-BLg1Kk32.js";
import "./skills-CSkUhue3.js";
import "./chrome-cUWm_ik6.js";
import "./store-B2I8nuEV.js";
import "./image-Cbdwymb8.js";
import "./api-key-rotation-UU9-rkGf.js";
import "./proxy-fetch-BZAtM2fT.js";

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