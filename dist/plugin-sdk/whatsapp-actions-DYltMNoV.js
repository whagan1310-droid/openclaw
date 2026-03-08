import "./run-with-concurrency-ab1joTSj.js";
import "./config--DRASumq.js";
import "./logger-Bl138Nx7.js";
import "./paths-0d8fBoC4.js";
import { i as resolveWhatsAppAccount } from "./accounts-szhBTLZx.js";
import "./plugins-B07F4eF-.js";
import { f as readStringParam, l as readReactionParams, o as jsonResult, r as createActionGate, t as ToolAuthorizationError } from "./common-LT9u-caA.js";
import { t as resolveWhatsAppOutboundTarget } from "./resolve-outbound-target-Cc0R6amY.js";
import "./image-ops-C39TxwvE.js";
import "./github-copilot-token-CKKBybuX.js";
import "./path-alias-guards-BBXtPn2S.js";
import "./fs-safe-t5kQgXVc.js";
import "./proxy-env-0Kn4CclB.js";
import "./tool-images-DuFJbsyV.js";
import "./fetch-guard-CXhp1JB4.js";
import "./local-roots-DHZXwbEC.js";
import "./ir-DFO4p139.js";
import "./render-CF8xRF8z.js";
import "./tables-qg1bxLst.js";
import { r as sendReactionWhatsApp } from "./outbound-D9o0IwPQ.js";

//#region src/agents/tools/whatsapp-target-auth.ts
function resolveAuthorizedWhatsAppOutboundTarget(params) {
	const account = resolveWhatsAppAccount({
		cfg: params.cfg,
		accountId: params.accountId
	});
	const resolution = resolveWhatsAppOutboundTarget({
		to: params.chatJid,
		allowFrom: account.allowFrom ?? [],
		mode: "implicit"
	});
	if (!resolution.ok) throw new ToolAuthorizationError(`WhatsApp ${params.actionLabel} blocked: chatJid "${params.chatJid}" is not in the configured allowFrom list for account "${account.accountId}".`);
	return {
		to: resolution.to,
		accountId: account.accountId
	};
}

//#endregion
//#region src/agents/tools/whatsapp-actions.ts
async function handleWhatsAppAction(params, cfg) {
	const action = readStringParam(params, "action", { required: true });
	const isActionEnabled = createActionGate(cfg.channels?.whatsapp?.actions);
	if (action === "react") {
		if (!isActionEnabled("reactions")) throw new Error("WhatsApp reactions are disabled.");
		const chatJid = readStringParam(params, "chatJid", { required: true });
		const messageId = readStringParam(params, "messageId", { required: true });
		const { emoji, remove, isEmpty } = readReactionParams(params, { removeErrorMessage: "Emoji is required to remove a WhatsApp reaction." });
		const participant = readStringParam(params, "participant");
		const accountId = readStringParam(params, "accountId");
		const fromMeRaw = params.fromMe;
		const fromMe = typeof fromMeRaw === "boolean" ? fromMeRaw : void 0;
		const resolved = resolveAuthorizedWhatsAppOutboundTarget({
			cfg,
			chatJid,
			accountId,
			actionLabel: "reaction"
		});
		const resolvedEmoji = remove ? "" : emoji;
		await sendReactionWhatsApp(resolved.to, messageId, resolvedEmoji, {
			verbose: false,
			fromMe,
			participant: participant ?? void 0,
			accountId: resolved.accountId
		});
		if (!remove && !isEmpty) return jsonResult({
			ok: true,
			added: emoji
		});
		return jsonResult({
			ok: true,
			removed: true
		});
	}
	throw new Error(`Unsupported WhatsApp action: ${action}`);
}

//#endregion
export { handleWhatsAppAction };