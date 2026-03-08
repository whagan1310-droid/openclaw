import "./run-with-concurrency-4hV87dFz.js";
import "./paths-CaA28K0s.js";
import { L as logVerbose, z as shouldLogVerbose } from "./logger-03l-fZAz.js";
import "./model-selection-lwmr9t_l.js";
import "./github-copilot-token-BWXANsA6.js";
import "./thinking-BVC5l1Nc.js";
import "./accounts-BII343--.js";
import "./plugins-w_ygGzjR.js";
import "./accounts-DgQ-HDpf.js";
import "./image-ops-D5o85tBt.js";
import "./pi-embedded-helpers-Cs29J7Bb.js";
import "./chrome-CN7Tv4h2.js";
import "./skills-Cm6_G0q1.js";
import "./path-alias-guards-9z4t17It.js";
import "./redact-BYyl-Ec1.js";
import "./errors-LUTSBF6A.js";
import "./fs-safe-D0wIkojW.js";
import "./proxy-env-CyEJdzEs.js";
import "./store-w524DpCn.js";
import "./accounts-BFIJx-P9.js";
import "./paths-DN38TCtQ.js";
import "./tool-images-BW_l10SN.js";
import "./image-CqbPncBo.js";
import { g as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-C-yA9c1T.js";
import "./fetch-Bvs4eaAh.js";
import "./fetch-guard-BNfxuLyv.js";
import "./api-key-rotation-B7mT4FVY.js";
import "./proxy-fetch-ukJ5M9an.js";

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