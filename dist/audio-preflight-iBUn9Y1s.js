import { a as logVerbose, c as shouldLogVerbose } from "./globals-d3aR1MYC.js";
import "./paths-BMo6kTge.js";
import "./subsystem-Cfn2Pryx.js";
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
import "./models-config-_Eeii_hA.js";
import "./model-catalog-gOiarqwC.js";
import "./fetch-Bl3aVxxx.js";
import { _ as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-ayYbqJLy.js";
import "./fetch-guard-DWL1zn9K.js";
import "./image-DDi7eszA.js";
import "./tool-display-DNMp8JVO.js";
import "./api-key-rotation-CkaJoN8F.js";
import "./proxy-fetch-m6Pd-K6R.js";

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