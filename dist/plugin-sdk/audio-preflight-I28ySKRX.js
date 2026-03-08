import "./run-with-concurrency-ab1joTSj.js";
import "./config--DRASumq.js";
import { L as logVerbose, z as shouldLogVerbose } from "./logger-Bl138Nx7.js";
import "./paths-0d8fBoC4.js";
import "./accounts-szhBTLZx.js";
import "./plugins-B07F4eF-.js";
import "./thinking-D9WAhjRI.js";
import "./accounts-BsWYNBoC.js";
import "./image-ops-C39TxwvE.js";
import "./pi-embedded-helpers-BHC5cQK1.js";
import "./accounts-BvOaO8tB.js";
import "./github-copilot-token-CKKBybuX.js";
import "./paths-DmMK7U5L.js";
import { i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, p as isAudioAttachment, t as runAudioTranscription } from "./audio-transcription-runner-DFP3PKLT.js";
import "./image-D4hgcNif.js";
import "./chrome-Pd5FxDO3.js";
import "./skills-ZOrsklaM.js";
import "./path-alias-guards-BBXtPn2S.js";
import "./redact-C3rEm8A0.js";
import "./errors-B2jpHiod.js";
import "./fs-safe-t5kQgXVc.js";
import "./proxy-env-0Kn4CclB.js";
import "./store-Bai6Vi8P.js";
import "./tool-images-DuFJbsyV.js";
import "./fetch-guard-CXhp1JB4.js";
import "./api-key-rotation-1UdeCVj2.js";
import "./local-roots-DHZXwbEC.js";
import "./proxy-fetch-C-fXKPD2.js";

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