import { u as getPairingAdapter } from "./pairing-store-B_ho1sqi.js";

//#region src/pairing/pairing-labels.ts
function resolvePairingIdLabel(channel) {
	return getPairingAdapter(channel)?.idLabel ?? "userId";
}

//#endregion
export { resolvePairingIdLabel as t };