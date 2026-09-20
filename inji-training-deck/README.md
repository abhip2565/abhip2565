# Inji training decks

Two presentation-ready PowerPoint decks built on a shared design system, plus the Python
generator that produces them.

| Deck | Slides | For |
|---|---|---|
| `Inji-Wallet-and-Inji-Web-Technical-Enablement-Brazil.pptx` | 85 | A 4–5 hour end-to-end technical enablement session for a Brazil implementation team |
| `Inji-Key-Manager-Deep-Dive.pptx` | 24 | A standalone 90-minute Key Manager deep dive. Programme-neutral, styled with the official Inji deck template |

Both are 16:9 with full speaker notes on every slide (what to explain, caveats, likely
audience questions, recommended time).

---

## Deck 2 — Key Manager deep dive

**File:** `Inji-Key-Manager-Deep-Dive.pptx` · 24 slides · 90 minutes · ~5,500 words of notes

Styled with the **official Inji deck template** (June 2026): the brand gradient background,
the Inji logo and watermark, the left accent rail, Montserrat, and `#F27D21` orange. Dense
technical content sits on a light panel over the gradient, which is how the template treats
its own content boxes.

Slide text is programme-neutral and declarative — no country, organisation or schedule
references, and no imperative instructions to the audience. Speaker notes keep their
coaching tone, since they are written for whoever is presenting.

Diagram-led, covering the eight topics in the session plan:

| # | Topic | Time | Key visuals |
|---|---|---|---|
| 1 | Why a dedicated Key Manager | 10 min | Before/after custody diagram; where it sits in the Inji stack (shared service vs. embedded library) |
| 2 | Key Manager architecture | 20 min | Three-tier key hierarchy; HSM vs. database custody; key-generation sequence; signing sequence; data model; API surface |
| 3 | Key lifecycle | 15 min | Five-state lifecycle; rotation timeline with the `pre_expire_days` overlap; what happens to credentials already issued |
| 4 | HSM integration | 12 min | Keystore-implementation diagram (PKCS11 / PKCS12 / Offline / JCE); software-vs-HSM trade-off table |
| 5 | Trust anchors | 12 min | Five stages from key to trust; `did.json` and `jwks.json` anatomy; safe-rotation runbook |
| 6 | Status list mechanics | 10 min | Bitstring diagram; issue→revoke→verify sequence; status list vs. key revocation |
| 7 | Multi-issuer / multi-tenant | 6 min | Key-isolation diagram; isolation-strength table; external-trust requirements |
| 8 | Key compromise | 5 min | Incident timeline; rotate-vs-repudiate blast radius |

### Findings worth knowing before you present

Verified against `mosip/keymanager` and `mosip/inji-certify`:

- **Inji Certify embeds the key manager library** rather than calling a separate service —
  `mosip.kernel.keymanager.hsm.*` are Certify's own properties. There is no Key Manager pod
  in the Inji stack.
- **Three tiers, not two:** ROOT → module/master key (in the HSM) → base/reference key
  (generated in software, private key wrapped with the module public key, stored in
  `keymgr.key_store`). "All private keys are in the HSM" is an over-claim.
- **`PUT /revokeKey` does not destroy anything.** It sets `key_expire_dtimes` to one minute
  ago, which forces an early rotation. Credentials already signed stay valid.
- **Nothing is ever deleted.** `getAllCertificates` returns every certificate an alias has
  ever had, and that is what `jwks.json` is built from — the reason rotation doesn't break
  old credentials.
- **Rotation is lazy.** No scheduler; the first signing request past the
  `key_expire_dtimes − pre_expire_days` boundary generates the successor.
- **Status list credentials are themselves signed VCs** (default `Ed25519Signature2020`,
  key ref `ED25519_SIGN`), so the revocation mechanism has a key dependency of its own.
- Shipped `key_policy_def` seed: ROOT 2920 days / 1125 pre-expire, BASE 730 / 30,
  module app ids 1095 / 60.

---

## Deck 1 — Inji Wallet & Inji Web technical enablement (Brazil)

### What it covers

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

### Design conventions

- One recurring architecture diagram (Issuer → Mimoto → Inji Wallet → Credential Store →
  OpenID4VP → Verifier, with Inji Web attached to Mimoto) reappears with the component under
  discussion highlighted.
- Sequence diagrams for the pre-authorized code flow, the authorization code flow with PKCE,
  and cross-device OpenID4VP.
- Speaker notes on every slide carry: what to explain, caveats, likely audience questions,
  and a recommended time.
- Slide text is kept short; the depth lives in the notes.

### Accuracy

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

---

## Regenerating either deck

```bash
pip install python-pptx
cd generator

# Brazil enablement deck
python3 -c "exec(open('build.py').read()); from deck_core import prs; prs.save('../deck1.pptx')"

# Key Manager deep dive (applies the Inji brand theme)
python3 -c "exec(open('build_km.py').read()); from deck_core import prs; prs.save('../deck2.pptx')"
```

`deck_core.THEME` drives the branding. It is empty by default, so deck 1 renders on white;
`theme_inji.apply()` fills it in and deck 2 renders on the Inji gradient. Nothing else in
the slide content changes between the two.

| File | Role |
|---|---|
| `deck_core.py` | Design system: colours, type, tables, code boxes with syntax highlighting, auto-fit pass |
| `deck_blocks.py` | Composite blocks: bullets, cards, callouts, the recurring architecture spine, sequence diagrams, demo checkpoints |
| `deck_km.py` | Extra primitives for the Key Manager deck: nodes, labelled arrows, trust zones, lifecycle strips, rotation timelines |
| `theme_inji.py` | The Inji brand theme — palette, fonts and the `assets/` background, logo, rail and watermark. Applied by deck 2 only; deck 1 keeps the neutral light theme |
| `build.py` | Slide content for deck 1 |
| `build_km.py` | Slide content for deck 2 |
| `check.py` | Reports any slide whose content overflows the canvas |

Both builds end with `fit_all()`, which shrinks any slide whose content would run past the
bottom margin, so content changes will not silently overflow.
