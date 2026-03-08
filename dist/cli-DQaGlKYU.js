import "./paths-BBP4yd-2.js";
import "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./thinking-Fqckw03T.js";
import { Ot as loadOpenClawPlugins } from "./reply-CCBexja_.js";
import { d as resolveDefaultAgentId, u as resolveAgentWorkspaceDir } from "./agent-scope-C_RF521q.js";
import { t as createSubsystemLogger } from "./subsystem-D5pRlZe-.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DHGbafYr.js";
import "./exec-DruQEXPV.js";
import { $t as loadConfig } from "./model-selection-BaeHlT6A.js";
import "./github-copilot-token-b6kJVrW-.js";
import "./boolean-BsqeuxE6.js";
import "./env-BCNBCy-T.js";
import "./host-env-security-DkAVVuaw.js";
import "./registry-CEJSZAKm.js";
import "./manifest-registry-Ds8wMsKE.js";
import "./dock-BI9_dwQi.js";
import "./message-channel-CSTlX5lG.js";
import "./send-CmOa-Ni1.js";
import "./plugins-DD42H5-v.js";
import "./sessions-DL9FheWJ.js";
import "./audio-transcription-runner-C-D_ByVL.js";
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
import "./send-CpuweJkl.js";
import "./paths-BoNnI0IY.js";
import "./chat-envelope-C9vncoSN.js";
import "./tool-images-Yi19DXNT.js";
import "./tool-display-UQpRiLW1.js";
import "./fetch-guard-Dgqgja8f.js";
import "./api-key-rotation-Du2GgzR5.js";
import "./local-roots-CpCrku7k.js";
import "./model-catalog-DhrOiZ6A.js";
import "./proxy-fetch-ltP1CUSR.js";
import "./tokens-BUhXwgty.js";
import "./deliver-s7VOqmJk.js";
import "./commands-PPn4IGbA.js";
import "./commands-registry-BHnndXec.js";
import "./client-DPuEGSE_.js";
import "./call-CqTAcmXH.js";
import "./pairing-token-Dz_8pP2A.js";
import "./with-timeout-Dd1NyOsy.js";
import "./diagnostic-DIe2z7or.js";
import "./send-DXHZEPNR.js";
import "./pi-model-discovery-zC2LVJRu.js";
import "./exec-approvals-allowlist-DdSRN6ci.js";
import "./exec-safe-bin-runtime-policy-DbyyuUj-.js";
import "./ir-Vta7AMmQ.js";
import "./render-BBWKrfmg.js";
import "./target-errors-CjB9ZnAm.js";
import "./channel-selection-CeO3RPS_.js";
import "./plugin-auto-enable-jZIG-i4G.js";
import "./send-BSTORW3n.js";
import "./outbound-attachment-0C6s1zey.js";
import "./fetch-CWxyv3dX.js";
import "./delivery-queue-C9pOHkVO.js";
import "./send-B-p5NEnA.js";
import "./pairing-store-B_ho1sqi.js";
import "./read-only-account-inspect-qEo7wkha.js";
import "./channel-activity-B_kO46sv.js";
import "./tables-CyoXYrlb.js";
import "./proxy-C-mS5IJD.js";
import "./timeouts-CjfVT9AB.js";
import "./skill-commands-DWIygbP0.js";
import "./workspace-dirs-FUjBTXbC.js";
import "./runtime-config-collectors-CvVyFBgq.js";
import "./command-secret-targets-DcsK8ZYD.js";
import "./session-cost-usage-D4slaGCr.js";
import "./onboard-helpers-CKPkIyNp.js";
import "./prompt-style-BgFv5fyL.js";
import "./pairing-labels-BMomJTRg.js";
import "./memory-cli-DjaudeXJ.js";
import "./manager-C6IdcHE5.js";
import "./query-expansion-BSREc1OE.js";
import "./links-B0L7hhCO.js";
import "./cli-utils-tNdOjVQI.js";
import "./help-format-Dbqi5yWh.js";
import "./progress-D-QR55qI.js";
import "./exec-approvals-D0z5V3f5.js";
import "./nodes-screen-Pqt7wIam.js";
import "./system-run-command-BnH4PenG.js";
import "./server-lifecycle-JeW7Cjd1.js";
import "./stagger-wClkZ9EC.js";

//#region src/plugins/cli.ts
const log = createSubsystemLogger("plugins");
function registerPluginCliCommands(program, cfg) {
	const config = cfg ?? loadConfig();
	const workspaceDir = resolveAgentWorkspaceDir(config, resolveDefaultAgentId(config));
	const logger = {
		info: (msg) => log.info(msg),
		warn: (msg) => log.warn(msg),
		error: (msg) => log.error(msg),
		debug: (msg) => log.debug(msg)
	};
	const registry = loadOpenClawPlugins({
		config,
		workspaceDir,
		logger
	});
	const existingCommands = new Set(program.commands.map((cmd) => cmd.name()));
	for (const entry of registry.cliRegistrars) {
		if (entry.commands.length > 0) {
			const overlaps = entry.commands.filter((command) => existingCommands.has(command));
			if (overlaps.length > 0) {
				log.debug(`plugin CLI register skipped (${entry.pluginId}): command already registered (${overlaps.join(", ")})`);
				continue;
			}
		}
		try {
			const result = entry.register({
				program,
				config,
				workspaceDir,
				logger
			});
			if (result && typeof result.then === "function") result.catch((err) => {
				log.warn(`plugin CLI register failed (${entry.pluginId}): ${String(err)}`);
			});
			for (const command of entry.commands) existingCommands.add(command);
		} catch (err) {
			log.warn(`plugin CLI register failed (${entry.pluginId}): ${String(err)}`);
		}
	}
}

//#endregion
export { registerPluginCliCommands };