**Source ID**: SRC-SLACK-17

# Slack Thread: Offline Auth Mock and Rotation Block
**Channel**: #cipherdoc
**Thread opened**: 2026-08-04
**Last activity**: 2026-08-05

---

**[2026-08-04 09:14] Bob**: Building the local auth mock for air-gap testing so we can exercise Diana's key-rotation design without a real deployment.

**[2026-08-04 09:16] Bob**: Mock is up. It runs the rotation flow with the network disabled, same as a real air-gapped site would see.

**[2026-08-04 10:27] Diana**: Good, that's exactly what I need to validate the design against.

**[2026-08-05 08:36] Alice**: How'd it go?

**[2026-08-05 08:45] Bob**: Not great. Key rotation just can't complete with the network down — the flow we designed assumes at least a brief connection to finish the handshake.

**[2026-08-05 08:48] Alice**: Ugh.

**[2026-08-05 09:13] Diana**: So we're blocked. There's no resolution yet on how to rotate without any network at all.

**[2026-08-05 09:33] Alice**: Offline auth stays blocked. Let's regroup on whether the design needs to change or whether we relax the offline requirement.
