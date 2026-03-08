import "./paths-BBP4yd-2.js";
import "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
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
import "./tailscale-D2B0lekn.js";
import "./tailnet-D1FN3bC3.js";
import "./ws-CtzAmMCA.js";
import "./auth-B6-DZzxb.js";
import "./accounts-fZUHTzqA.js";
import "./accounts-Bso9KOTU.js";
import "./logging-xYH6GmRT.js";
import "./accounts-OddzPdQ6.js";
import "./paths-BoNnI0IY.js";
import "./chat-envelope-C9vncoSN.js";
import "./client-DPuEGSE_.js";
import "./call-CqTAcmXH.js";
import "./pairing-token-Dz_8pP2A.js";
import "./onboard-helpers-CKPkIyNp.js";
import "./prompt-style-BgFv5fyL.js";
import "./runtime-guard-B7OSlOCA.js";
import "./note-k8AbeMaN.js";
import { n as gatewayInstallErrorHint, t as buildGatewayInstallPlan } from "./daemon-install-helpers-DCJKVFCc.js";
import { r as isGatewayDaemonRuntime, t as DEFAULT_GATEWAY_DAEMON_RUNTIME } from "./daemon-runtime-Dp28yNwO.js";
import { t as resolveGatewayInstallToken } from "./gateway-install-token-B869pefO.js";
import { r as isSystemdUserServiceAvailable } from "./systemd-CwAmpVhn.js";
import { t as resolveGatewayService } from "./service-ieBgsBtq.js";
import { n as ensureSystemdUserLingerNonInteractive } from "./systemd-linger-rSYp9EtZ.js";

//#region src/commands/onboard-non-interactive/local/daemon-install.ts
async function installGatewayDaemonNonInteractive(params) {
	const { opts, runtime, port } = params;
	if (!opts.installDaemon) return;
	const daemonRuntimeRaw = opts.daemonRuntime ?? DEFAULT_GATEWAY_DAEMON_RUNTIME;
	const systemdAvailable = process.platform === "linux" ? await isSystemdUserServiceAvailable() : true;
	if (process.platform === "linux" && !systemdAvailable) {
		runtime.log("Systemd user services are unavailable; skipping service install.");
		return;
	}
	if (!isGatewayDaemonRuntime(daemonRuntimeRaw)) {
		runtime.error("Invalid --daemon-runtime (use node or bun)");
		runtime.exit(1);
		return;
	}
	const service = resolveGatewayService();
	const tokenResolution = await resolveGatewayInstallToken({
		config: params.nextConfig,
		env: process.env
	});
	for (const warning of tokenResolution.warnings) runtime.log(warning);
	if (tokenResolution.unavailableReason) {
		runtime.error([
			"Gateway install blocked:",
			tokenResolution.unavailableReason,
			"Fix gateway auth config/token input and rerun onboarding."
		].join(" "));
		runtime.exit(1);
		return;
	}
	const { programArguments, workingDirectory, environment } = await buildGatewayInstallPlan({
		env: process.env,
		port,
		token: tokenResolution.token,
		runtime: daemonRuntimeRaw,
		warn: (message) => runtime.log(message),
		config: params.nextConfig
	});
	try {
		await service.install({
			env: process.env,
			stdout: process.stdout,
			programArguments,
			workingDirectory,
			environment
		});
	} catch (err) {
		runtime.error(`Gateway service install failed: ${String(err)}`);
		runtime.log(gatewayInstallErrorHint());
		return;
	}
	await ensureSystemdUserLingerNonInteractive({ runtime });
}

//#endregion
export { installGatewayDaemonNonInteractive };