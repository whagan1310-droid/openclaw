import "./paths-BBP4yd-2.js";
import { a as logVerbose, c as shouldLogVerbose } from "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./thinking-Fqckw03T.js";
import "./agent-scope-C_RF521q.js";
import "./subsystem-D5pRlZe-.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DHGbafYr.js";
import "./exec-DruQEXPV.js";
import "./model-selection-BaeHlT6A.js";
import "./github-copilot-token-b6kJVrW-.js";
import "./boolean-BsqeuxE6.js";
import "./env-BCNBCy-T.js";
import "./host-env-security-DkAVVuaw.js";
import "./registry-CEJSZAKm.js";
import "./manifest-registry-Ds8wMsKE.js";
import "./dock-BI9_dwQi.js";
import "./message-channel-CSTlX5lG.js";
import "./plugins-DD42H5-v.js";
import "./sessions-DL9FheWJ.js";
import { d as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-C-D_ByVL.js";
import "./image-DYcaLiqA.js";
import "./models-config-C4_y2Zds.js";
import "./pi-embedded-helpers-BPB21Ua-.js";
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
import "./tool-images-Yi19DXNT.js";
import "./tool-display-UQpRiLW1.js";
import "./fetch-guard-Dgqgja8f.js";
import "./api-key-rotation-Du2GgzR5.js";
import "./local-roots-CpCrku7k.js";
import "./model-catalog-DhrOiZ6A.js";
import "./proxy-fetch-ltP1CUSR.js";

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