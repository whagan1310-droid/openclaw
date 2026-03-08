import "./globals-d3aR1MYC.js";
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
import "./message-channel-DTk937hY.js";
import "./tailscale-Bm1Sl4zA.js";
import "./tailnet-BXLAgtlT.js";
import "./ws-Da560NJf.js";
import "./auth-vwV9EhNu.js";
import "./sessions-G4D58Ojj.js";
import "./accounts-viX3i-Kr.js";
import "./paths-CCvn4cNJ.js";
import "./chat-envelope-BBXhi7A0.js";
import "./client-B9xXRY-r.js";
import "./call-C79Luiuk.js";
import "./pairing-token-CCWPBg5t.js";
import "./onboard-helpers-BSbYkxLh.js";
import "./prompt-style-4wb3GpM-.js";
import "./note-D-3vxUal.js";
import { n as gatewayInstallErrorHint, t as buildGatewayInstallPlan } from "./daemon-install-helpers-De2rRniV.js";
import "./runtime-guard-DgCE52lk.js";
import { r as isGatewayDaemonRuntime, t as DEFAULT_GATEWAY_DAEMON_RUNTIME } from "./daemon-runtime-D8xmnSd2.js";
import { t as resolveGatewayInstallToken } from "./gateway-install-token-BdYvQouH.js";
import { r as isSystemdUserServiceAvailable } from "./systemd-D5gNH924.js";
import { t as resolveGatewayService } from "./service-DAmsCq52.js";
import { n as ensureSystemdUserLingerNonInteractive } from "./systemd-linger-BI9FOuxq.js";

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