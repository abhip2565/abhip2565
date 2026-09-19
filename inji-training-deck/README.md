# Inji Wallet & Inji Web — Technical Enablement Workshop (Brazil)

A presentation-ready PowerPoint deck for a 4–5 hour technical training session aimed at
implementers, architects, developers and integration engineers.

**File:** `Inji-Wallet-and-Inji-Web-Technical-Enablement-Brazil.pptx`
85 slides · 16:9 · full speaker notes on every slide (~14,000 words)

## What it covers

| Block | Time | Contents |
|---|---|---|
| 1. Introduction + ecosystem | 20 min | Roles, trust boundaries, the recurring architecture diagram, where OpenID4VCI/OpenID4VP sit |
| 2. End-to-end demo first | 20 min | Full issuance and full presentation, with what happens behind the glass |
| 3. OpenID4VCI + issuance | 35 min | Credential Offer, issuer & AS metadata, both grant flows, token/credential messages |
| 4. PKCE, DPoP, proofs, binding | 25 min | What each mechanism protects; proof type vs binding method vs holder binding vs key binding |
| 5. Credential formats | 30 min | SD-JWT VC, mDoc/MSO, W3C VC, JWT VC — data model, verification, disclosure, key resolution |
| 6. Inji Wallet architecture | 35 min | Layers, XState machines, native bridge, storage, keys, deep links, extension points |
| 7. Mimoto | 25 min | Why it exists, internals, API surface, issuer/verifier configuration, responsibility matrix |
| 8. OpenID4VP + presentation | 30 min | Authorization request, client_id schemes, matching, consent, VP token, verifier checklist |
| 9. Inji Web + device flows | 25 min | BFF architecture, guest/logged-in journeys, same-device, cross-device, handoff |
| 10. Security + key resolution | 25 min | Threat model, attack→mitigation, kid/JWKS/DID/x5c resolution failures |
| 11. Config, deployment, code | 30 min | Configuration surface, localisation (pt-BR), deployment, repo walkthrough |
| 12. Troubleshooting + interop | 30 min | Triage tree, two failure catalogues, draft-version skew |
| 13. Brazil decisions + recap | 30–45 min | Open questions (no assumptions), decision ordering, exercises, recap |

Plus **8 demo checkpoints** spread through the day and **9 hands-on exercises**.

## Design conventions

- One recurring architecture diagram (Issuer → Mimoto → Inji Wallet → Credential Store →
  OpenID4VP → Verifier, with Inji Web attached to Mimoto) reappears with the component under
  discussion highlighted.
- Sequence diagrams for the pre-authorized code flow, the authorization code flow with PKCE,
  and cross-device OpenID4VP.
- Speaker notes on every slide carry: what to explain, caveats, likely audience questions,
  and a recommended time.
- Slide text is kept short; the depth lives in the notes.

## Accuracy

Technical statements were checked against the public MOSIP/Inji repositories
(`inji-wallet`, `inji-web`, `mimoto`, `inji-vci-client`, `inji-openid4vp`, `vc-verifier`,
`pixelpass`, `inji-certify`) at the time of writing. Version-specific behaviour is flagged
on the slide. Notable verified points that are easy to get wrong:

- DPoP is **not** implemented in the Inji stack reviewed; access tokens are Bearer tokens.
- `vc-verifier` resolves SD-JWT VC issuer keys from an X.509 chain (`x5c`);
  JWT VC Issuer Metadata (`/.well-known/jwt-vc-issuer`) is not yet supported.
- Inji Certify does not issue `mso_mdoc` today.
- Inji Web's OpenID4VP presentation support is currently limited to `ldp_vc`.
- Ed25519 and secp256k1 keys are not hardware-keystore backed on Android/iOS.

Re-verify against the release you deploy before treating any of this as fixed.

## Regenerating the deck

```bash
pip install python-pptx
cd generator
python3 -c "exec(open('build.py').read()); from deck_core import prs; prs.save('../deck.pptx')"
python3 check.py      # reports any slide whose content overflows the canvas
```

`deck_core.py` holds the design system (colours, type, tables, code boxes, auto-fit),
`deck_blocks.py` the composite blocks (cards, the architecture spine, sequence diagrams,
demo checkpoints), and `build.py` the slide content.
