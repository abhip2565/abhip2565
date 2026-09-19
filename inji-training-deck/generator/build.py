# -*- coding: utf-8 -*-
"""Inji Wallet & Inji Web — Technical Enablement Workshop (Brazil).
Builds the PPTX. Facts verified against MOSIP/Inji repositories, Sept 2026."""
import sys
from deck_blocks import *   # noqa

# =================================================================== 1. TITLE
s = new_slide(dark=True)
STATE['section'] = "Inji technical enablement"
rect(s, 0, 0, W, H, fill=C['dark'])
rect(s, 0, 0, W, 0.10, fill=C['accent'])
rect(s, 8.55, 0.10, 4.78, H - 0.10, fill=C['dark2'])
rect(s, 8.55, 0.10, 0.045, H - 0.10, fill=RGBColor(0x1E, 0x3F, 0x5C))
_, tf = tb(s, 0.95, 1.55, 7.3, 0.4)
para(tf, "TECHNICAL ENABLEMENT WORKSHOP", size=12, color=C['accent'], bold=True, first=True)
_, tf = tb(s, 0.95, 2.05, 7.4, 1.9)
para(tf, "Inji Wallet & Inji Web", size=44, color=C['white'], bold=True, first=True,
     line_spacing=1.02)
para(tf, "End to end, for the people who have to build it", size=19,
     color=RGBColor(0x8F, 0xAE, 0xC8), space_before=8)
line(s, 0.95, 4.35, 5.2, 4.35, C['accent'], 2.5)
_, tf = tb(s, 0.95, 4.60, 7.3, 1.2)
para(tf, "Brazil implementation team  •  architects, developers, integration engineers",
     size=13, color=RGBColor(0xC6, 0xD6, 0xE4), first=True)
para(tf, "4–5 hours  •  ~3h15m teaching  •  ~1h15m demos, exercises, discussion",
     size=13, color=RGBColor(0x8F, 0xAE, 0xC8), space_before=5)
for i, (lab, val) in enumerate([("Wallet", "React Native"), ("Web", "React + BFF"),
                                ("Backend", "Mimoto (Spring)"), ("Protocols", "OpenID4VC")]):
    x = 8.98 + (i % 2) * 2.10
    yy = 2.72 + (i // 2) * 1.02
    rect(s, x, yy, 1.92, 0.86, fill=C['dark2'], line=RGBColor(0x1E, 0x3F, 0x5C), lw=1,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
    _, t2 = tb(s, x + 0.10, yy + 0.15, 1.72, 0.25)
    para(t2, lab, size=8.5, color=C['accent'], bold=True, align=PP_ALIGN.CENTER, first=True)
    _, t3 = tb(s, x + 0.08, yy + 0.44, 1.76, 0.3)
    para(t3, val, size=10, color=C['white'], bold=True, align=PP_ALIGN.CENTER, first=True)
_, tf = tb(s, 0.95, 6.62, 7.4, 0.5)
para(tf, "Built on the public MOSIP / Inji repositories. Where behaviour is version-specific it is called out on the slide.",
     size=9.5, color=RGBColor(0x62, 0x80, 0x9B), italic=True, first=True)
_, tf = tb(s, 8.98, 2.20, 4.1, 0.3)
para(tf, "THE STACK IN ONE GLANCE", size=8.5, color=C['accent'], bold=True, first=True)
_, tf = tb(s, 8.98, 4.95, 4.05, 1.6)
para(tf, "Repositories you will meet today:", size=9.5, color=RGBColor(0x8F,0xAE,0xC8), bold=True, first=True)
for rp in ["mosip/inji-wallet", "mosip/inji-web", "mosip/mimoto", "mosip/inji-vci-client",
           "mosip/inji-openid4vp", "mosip/vc-verifier"]:
    para(tf, rp, size=9, color=RGBColor(0x7D,0xD3,0xC8), font=F_MONO, space_before=2)
notes(s, ["Welcome. Set the tone: this is an engineering session, not a product pitch. Nobody has to buy anything today.",
          "Say plainly what success looks like: at the end, every person in the room can draw the Inji architecture on a whiteboard and say which component owns which failure.",
          "Ask for a quick round of introductions: name, role, and which component they expect to touch first (issuer, wallet, web, verifier, infra). Write the counts down — you will use them to decide how deep to go in sections 8-11.",
          "Confirm logistics: breaks, language, whether people can run code during the session."],
      caveats=["Everything in this deck was checked against the public Inji repositories. Versions move fast; re-verify before you commit to a design.",
               "Brazil's architecture is not decided in this deck. Section 18 is deliberately a set of questions."],
      questions=["Is this the same as MOSIP? — Inji is the credential layer of the MOSIP ecosystem, but it works with any OpenID4VC-compliant issuer, MOSIP or not."],
      minutes="5 min (welcome + introductions)")
footer(s, dark=True)

# =================================================================== 2. OBJECTIVES
s, y = slide("What you will be able to do by 5 pm",
             kicker="Learning objectives",
             sub="Six concrete outcomes. If any of these is still fuzzy at the end, stop the session and ask.")
objs = [
 ("Draw the architecture", "Sketch Issuer → Mimoto → Wallet → Credential Store → OpenID4VP → Verifier from memory, and place Inji Web correctly.", C['primary']),
 ("Read a protocol trace", "Follow an OpenID4VCI issuance and an OpenID4VP presentation message by message, and say what each field is for.", C['accent']),
 ("Tell the layers apart", "Distinguish PKCE from DPoP, proof type from key-binding method, and bound from unbound credentials.", C['violet']),
 ("Choose a format", "Explain what changes for you if Brazil picks SD-JWT VC versus mDoc versus JSON-LD — data model, verification, disclosure, binding.", C['amber']),
 ("Configure the stack", "Register an issuer and a verifier, set deep links and callbacks, and know what is config versus what is code.", C['green']),
 ("Own a failure", "Take any error message and say within a minute whether it belongs to the Issuer, Mimoto, Wallet, Web or Verifier.", C['red']),
]
for i, (t, d, col) in enumerate(objs):
    x = ML + (i % 3) * (CW / 3 + 0.02) - (i % 3) * 0.02
    x = ML + (i % 3) * ((CW + 0.22) / 3)
    yy = y + (i // 3) * 2.42
    wid = (CW - 0.44) / 3
    rect(s, x, yy, wid, 2.20, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.055)
    rect(s, x, yy, wid, 0.075, fill=col)
    b = rect(s, x + 0.22, yy + 0.30, 0.42, 0.42, fill=col, shape=MSO_SHAPE.OVAL)
    tf2 = b.text_frame; tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf2.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(i + 1); r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = C['white']; r.font.name = F_SANS
    _, t2 = tb(s, x + 0.22, yy + 0.86, wid - 0.44, 0.34)
    para(t2, t, size=13.5, color=C['ink'], bold=True, first=True)
    _, t3 = tb(s, x + 0.22, yy + 1.22, wid - 0.44, 0.9)
    para(t3, d, size=10.2, color=C['muted'], first=True, line_spacing=1.25)
notes(s, ["Read the six outcomes out loud. They are the contract for the session.",
          "Point out that objective 6 — owning a failure — is the one that saves the most time in a real integration. Most lost days in VC projects come from a team debugging a component that was never at fault.",
          "Tell people to write down which objective matters most to their own role; you will come back to it in the recap."],
      caveats=["Do not promise that the session makes anyone production-ready on day one. It makes them able to read the system and ask the right questions."],
      questions=["Will we get the slides? — Yes, with speaker notes; the notes carry the detail that is not on the slides."],
      minutes="3 min")
footer(s)

# =================================================================== 3. WHAT IS INJI
s, y = slide("Inji Wallet and Inji Web, in plain words",
             kicker="Orientation",
             sub="Two holder applications, one backend, one set of protocols.")
card(s, ML, y, 3.85, 2.55, "Inji Wallet", [
    "A mobile app (Android and iOS) that a person installs.",
    "Built with React Native; heavy lifting sits in native Kotlin/Swift libraries.",
    "Holds credentials **on the device**, encrypted, with keys in platform hardware where the platform allows it.",
    "Can work offline once a credential is downloaded.",
], accent=C['primary'], tint=C['primary_l'], size=10.2)
card(s, ML + 4.19, y, 3.85, 2.55, "Inji Web", [
    "A browser wallet. No app install, works on a laptop or a shared device.",
    "React frontend; it keeps **no** credential in the browser.",
    "Credentials live in Mimoto's database, encrypted with a key derived from the user's PIN.",
    "For people without a smartphone, and for desktop journeys.",
], accent=C['accent'], tint=C['accent_l'], size=10.2)
card(s, ML + 8.38, y, 3.85, 2.55, "Mimoto", [
    "The shared backend for both. One Spring Boot service.",
    "Knows the list of issuers and trusted verifiers.",
    "Does token exchange, credential storage for Web, PDF rendering, session handling.",
    "It is a **backend-for-frontend**, not an issuer and not a verifier.",
], accent=C['violet'], tint=C['violet_l'], size=10.2)
yy = y + 2.78
callout(s, ML, yy, CW, "Inji is not an identity system. It does not decide who you are — the **Issuer** does that. Inji moves a credential the issuer already decided to give you, stores it safely, and hands a provable copy of part of it to a **Verifier** when you consent.", kind='tip', size=11)
yy += 0.78
_, tf = tb(s, ML, yy, CW, 0.3)
para(tf, "WHAT THEY ARE NOT", size=9, color=C['red'], bold=True, first=True)
row = [("Not an issuer", "Inji never mints a credential."),
       ("Not a verifier", "Inji never decides whether to let someone through a gate."),
       ("Not an IdP", "Authentication is done by eSignet, Keycloak, gov.br — whatever you plug in."),
       ("Not a database of people", "Mimoto stores credentials for Web users, not an identity registry.")]
for i, (t, d) in enumerate(row):
    x = ML + i * (CW / 4)
    _, t2 = tb(s, x, yy + 0.30, CW / 4 - 0.18, 0.7)
    rich(t2, [(t + " — ", C['red'], True), (d, C['muted'], False)], size=9.5, first=True,
         line_spacing=1.2)
notes(s, ["This slide exists to stop three recurring misunderstandings before they start.",
          "Wallet holds credentials on the device. Inji Web does not — the credential sits in Mimoto's Postgres, encrypted with an AES-256-GCM key that is itself wrapped with a PBKDF2 key derived from the user's wallet PIN. That is a real architectural difference with real privacy consequences, and Brazil has to decide whether it is acceptable.",
          "Say clearly: Mimoto is a BFF. Every time somebody proposes putting issuer logic or verifier logic into Mimoto, this slide is the answer."],
      caveats=["Inji Web's OpenID4VP presentation support is currently limited to ldp_vc; SD-JWT VC presentation from Web is on the roadmap, not shipped. Check the current release before promising it.",
               "'Offline' for Wallet means presenting a credential you already hold without a network. It does not mean downloading a credential offline."],
      questions=["If Mimoto stores credentials for Web users, is that a data residency problem? — Yes, and it is on the Brazil discussion list in section 18.",
                 "Can we run Wallet without Mimoto? — Partly. Issuer discovery and token exchange currently route through Mimoto in the standard configuration."],
      minutes="6 min")
footer(s)

# =================================================================== 4. AGENDA
s, y = slide("How the session runs", kicker="Agenda and timing",
             sub="Twelve teaching blocks, eight demo checkpoints, nine exercises. Timings are targets — the facilitator will re-balance live.")
rows = [
 ["1", "Introduction + Inji ecosystem", "20 min", "Architecture, roles, trust boundaries, where the protocols sit", "—"],
 ["2", "End-to-end demo first", "20 min", "One full issuance and one full presentation, then we explain it", "**Demo 1**"],
 ["3", "OpenID4VCI and issuance", "35 min", "Offer, metadata, both grant flows, token, credential request", "**Demo 2**"],
 ["4", "PKCE, DPoP, proofs and binding", "25 min", "What each mechanism actually protects, and how they differ", "Exercise 3"],
 ["5", "Credential formats", "30 min", "SD-JWT VC, mDoc, JSON-LD — data model to verification", "**Demo 3**"],
 ["6", "Inji Wallet architecture", "35 min", "Modules, native bridge, storage, keys, deep links, config", "**Demo 4**"],
 ["7", "Mimoto", "25 min", "Responsibilities, API surface, issuer and verifier configuration", "**Demo 7**"],
 ["8", "OpenID4VP and presentation", "30 min", "Request, matching, consent, VP token, verifier validation", "**Demo 5**"],
 ["9", "Inji Web + device flows", "25 min", "Same-device, cross-device, QR, handoff", "**Demo 6**"],
 ["10", "Security + key resolution", "25 min", "Threat model, kid/JWKS, mitigations", "Exercise 9"],
 ["11", "Config, deployment, dev walkthrough", "30 min", "Repos, builds, tracing a request through code", "—"],
 ["12", "Troubleshooting + interoperability", "30 min", "Failure catalogue and triage", "**Demo 8**"],
 ["13", "Brazil discussion, exercises, Q&A", "30–45 min", "Open technical decisions for Brazil", "—"],
]
_tb_bottom = table(s, ML, y, CW, ["#", "Block", "Time", "What it covers", "Checkpoint"], rows,
      col_w=[0.5, 3.1, 1.0, 6.3, 1.5], fsize=9.3, hsize=9.5, row_h=0.325, head_h=0.34)
yy = _tb_bottom + 0.18
callout(s, ML, yy, CW, "Total teaching ≈ 3 h 10 m. Demos, exercises and discussion ≈ 1 h 15 m. Plus two breaks of 10 minutes — take them, this is dense material.", kind='note', size=10.5)
notes(s, ["Walk the agenda quickly — 90 seconds, not five minutes.",
          "Explain the shape deliberately: we do the full demo second, before any protocol theory. People retain protocol detail far better when they have already watched the thing work.",
          "Point out the demo checkpoints are spread through the day on purpose. Nobody learns from a 45-minute demo block at 5 pm.",
          "Agree the break times with the room now so nobody is guessing."],
      caveats=["If the room is more architect-heavy than developer-heavy, compress section 11 (developer walkthrough) and give the time to sections 10 and 18.",
               "If the room is developer-heavy, do the opposite."],
      minutes="2 min")
footer(s)

# =================================================================== 5. SECTION 1
section("Inji ecosystem overview", "20 min",
        "Before any protocol detail: who the actors are, what each one is allowed to do, and where the trust boundaries fall.",
        ["The recurring architecture diagram",
         "Issuer, Holder, Verifier",
         "Mimoto, Wallet, Web, libraries",
         "Trust boundaries",
         "Online and offline",
         "Where OpenID4VCI and OpenID4VP sit"], num="1")
notes(prs.slides[-1], ["This is the map the whole day hangs off. Spend the time.",
                       "Tell the room that the diagram on the next slide will reappear in the corner of many later slides with the current component highlighted — that is their 'you are here' marker."],
      minutes="20 min for the section")

# =================================================================== 6. THE SPINE
s, y = slide("The one diagram to remember", kicker="Reference architecture",
             sub="Everything else today is a zoom-in on one of these boxes or one of these arrows.")
spine(s, y=1.95, highlight=(), big=True)
yy = 4.55
labels = [
 ("Issuer", "Decides the person deserves the credential, signs it. Inji Certify, or Brazil's own system.", C['primary']),
 ("Mimoto", "Wallet backend. Issuer list, token exchange, storage for Web. Never signs credentials.", C['violet']),
 ("Inji Wallet / Web", "The holder. Requests, stores, chooses what to disclose, presents.", C['accent']),
 ("Credential Store", "Encrypted at rest. On device for Wallet; in Mimoto's DB for Web.", C['amber']),
 ("Verifier", "Asks for specific claims, checks the signatures, decides. Inji Verify or a third party.", C['green']),
]
n = len(labels); gap = 0.24
bw = (CW - gap * (n - 1)) / n
for i, (t, d, col) in enumerate(labels):
    x = ML + i * (bw + gap)
    rect(s, x, yy, bw, 0.055, fill=col)
    _, t2 = tb(s, x, yy + 0.14, bw, 0.28)
    para(t2, t, size=10.5, color=col, bold=True, first=True)
    _, t3 = tb(s, x, yy + 0.44, bw, 1.1)
    para(t3, d, size=9.3, color=C['muted'], first=True, line_spacing=1.25)
callout(s, ML, 6.18, CW, "Read the arrows as **protocols, not as network hops**. OpenID4VCI is how a credential is obtained. OpenID4VP is how one is shown. Everything else — Mimoto's REST API, the native bridge inside the Wallet — is implementation, and can be changed without breaking interoperability.", kind='tip', size=10.5)
notes(s, ["Draw this on the whiteboard as you talk, do not just read the slide. People remember what they watched being drawn.",
          "Left to right is the life of a credential: it is created on the left, held in the middle, consumed on the right.",
          "Stress the distinction in the callout. The two OpenID4VC protocols are the interoperability contract with the outside world. Mimoto's own REST API is internal to Inji and you are free to change it. Teams that confuse the two either over-standardise internals or accidentally break interop.",
          "Note that the Credential Store is drawn as its own box on purpose: it behaves very differently between Wallet (on device) and Web (in Mimoto)."],
      caveats=["The arrow Issuer→Mimoto is not the whole truth: the Wallet talks to the issuer's credential endpoint directly for the credential request. Mimoto brokers discovery and token exchange. We correct this precisely in section 3 — flag it now so nobody builds the wrong mental model.",
               "Do not let anyone leave thinking Mimoto is a mandatory part of OpenID4VCI. It is an Inji design choice."],
      questions=["Why is there a backend at all if the wallet is the holder? — Client secrets, issuer catalogue management, and the browser wallet. Covered in section 7.",
                 "Can the Verifier talk to the Issuer? — Only to fetch issuer keys. It never asks the issuer about the person; that is the point of the model."],
      minutes="7 min")
footer(s)

# =================================================================== 7. ROLES
s, y = slide("Three roles, and only three", kicker="The trust triangle",
             sub="Every VC system in the world is this triangle. Inji is an implementation of the middle corner.")
# triangle diagram
cxI, cxV, cxH = 2.9, 10.4, 6.65
rect(s, cxI - 1.45, y + 0.10, 2.9, 1.05, fill=C['primary'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
_, tf = tb(s, cxI - 1.35, y + 0.28, 2.7, 0.7, anchor=MSO_ANCHOR.MIDDLE)
para(tf, "ISSUER", size=13, color=C['white'], bold=True, align=PP_ALIGN.CENTER, first=True)
para(tf, "signs the credential", size=9, color=C['primary_l'], align=PP_ALIGN.CENTER)
rect(s, cxV - 1.45, y + 0.10, 2.9, 1.05, fill=C['green'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
_, tf = tb(s, cxV - 1.35, y + 0.28, 2.7, 0.7, anchor=MSO_ANCHOR.MIDDLE)
para(tf, "VERIFIER", size=13, color=C['white'], bold=True, align=PP_ALIGN.CENTER, first=True)
para(tf, "checks and decides", size=9, color=C['green_l'], align=PP_ALIGN.CENTER)
rect(s, cxH - 1.75, y + 1.92, 3.5, 1.05, fill=C['accent'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
_, tf = tb(s, cxH - 1.65, y + 2.06, 3.3, 0.78, anchor=MSO_ANCHOR.MIDDLE)
para(tf, "HOLDER  —  Inji Wallet / Inji Web", size=12.5, color=C['white'], bold=True,
     align=PP_ALIGN.CENTER, first=True)
para(tf, "stores, chooses, consents, presents", size=9, color=C['accent_l'], align=PP_ALIGN.CENTER)
c = line(s, cxI + 0.15, y + 1.20, cxH - 1.35, y + 1.95, C['primary'], 1.6); arrowhead(c)
c = line(s, cxH + 1.35, y + 1.95, cxV - 0.15, y + 1.20, C['green'], 1.6); arrowhead(c)
c = line(s, cxI + 1.55, y + 0.62, cxV - 1.55, y + 0.62, C['muted'], 1.3, dash=2); arrowhead(c)
_, tf = tb(s, cxI + 1.6, y - 0.14, 5.9, 0.3)
para(tf, "verifier fetches issuer keys only — never asks the issuer about the person",
     size=8.8, color=C['muted'], italic=True, align=PP_ALIGN.CENTER, first=True)
_, tf = tb(s, 2.9, y + 1.36, 2.7, 0.3)
para(tf, "OpenID4VCI", size=9.5, color=C['primary'], bold=True, first=True)
_, tf = tb(s, 8.1, y + 1.36, 2.7, 0.3)
para(tf, "OpenID4VP", size=9.5, color=C['green'], bold=True, align=PP_ALIGN.RIGHT, first=True)
yy = y + 3.30
rows = [
 ["**Issuer**", "Authenticates the person, decides eligibility, signs the credential, publishes its metadata and public keys.",
  "Decide who the holder may show it to. Track where it is used."],
 ["**Holder** (Wallet / Web)", "Requests, stores, protects the private key, shows the user what is being asked, gets consent, builds the presentation.",
  "Alter claims. Vouch for the issuer's decision. Verify on the verifier's behalf."],
 ["**Verifier**", "Builds the request, checks the issuer signature, checks holder binding, checks freshness, applies its own policy.",
  "See claims it did not ask for. Assume the wallet is honest."],
]
table(s, ML, yy, CW, ["Role", "Must do", "Must not do"], rows,
      col_w=[2.1, 5.6, 4.5], fsize=9.5, row_h=0.55, head_h=0.32)
notes(s, ["Slow down here. Most integration arguments later in a project are really disagreements about this table.",
          "The dashed arrow across the top is important: the verifier contacts the issuer **only** to resolve keys. It never phones home to ask 'is this person still valid?' during a normal presentation. That is what makes the model privacy-preserving and offline-capable.",
          "Consent lives with the holder. In Inji that is a real screen in the Wallet that lists the requested claims before anything is sent. Show it in Demo 5.",
          "Point out that status/revocation is the one place where the verifier may go back to a status list — and that Inji Wallet does not currently do revocation checking for any format."],
      caveats=["Real deployments blur the triangle: an organisation can be both issuer and verifier. Keep the roles separate in the design even when the boxes run on the same cluster.",
               "'Must not do' for the holder is enforced by cryptography, not by policy. If the wallet alters a claim, the issuer signature fails."],
      questions=["Who is responsible if a verifier accepts a revoked credential? — A policy question, not a protocol one. Put it on the Brazil list."],
      minutes="5 min")
footer(s)

# =================================================================== 8. COMPONENTS
s, y = slide("The component inventory", kicker="What actually runs",
             sub="Repository, language, where it runs, and who owns it operationally. Memorise the middle column.")
rows = [
 ["`inji-wallet`", "Inji Wallet (mobile)", "React Native 0.74 / Expo 51, Kotlin, Swift", "User's phone", "Holder app"],
 ["`inji-web`", "Inji Web (browser)", "React + TypeScript, Tailwind", "Your cluster / CDN", "Holder app"],
 ["`mimoto`", "Wallet backend (BFF)", "Java 21, Spring Boot, Postgres, Redis", "Your cluster", "Backend"],
 ["`inji-certify`", "Issuer (reference)", "Java, Spring Boot, plugin-based", "Issuer's cluster", "Issuer"],
 ["`inji-verify`", "Verifier (reference)", "React + Java", "Verifier's cluster", "Verifier"],
 ["`inji-vci-client`", "OpenID4VCI client library", "Kotlin (AAR) + Swift", "Inside Wallet", "Library"],
 ["`inji-openid4vp`", "OpenID4VP library", "Kotlin Multiplatform (AAR/JAR) + Swift", "Inside Wallet, Mimoto", "Library"],
 ["`vc-verifier`", "Credential verification", "Kotlin/Java (AAR/JAR)", "Inside Wallet, Mimoto", "Library"],
 ["`pixelpass`", "QR encode/decode, CBOR→JSON", "Kotlin/JS", "Inside Wallet, Web", "Library"],
 ["`secure-keystore`", "Android/iOS key storage", "Kotlin / Swift", "Inside Wallet", "Library"],
 ["`inji-vc-renderer`", "SVG / display rendering", "Kotlin/JS", "Inside Wallet, Web", "Library"],
 ["`tuvali`", "BLE offline sharing transport", "Kotlin / Swift", "Inside Wallet", "Library"],
]
_tb_bottom = table(s, ML, y, CW, ["Repository", "What it is", "Built with", "Runs on", "Class"], rows,
      col_w=[2.3, 3.0, 3.9, 2.0, 1.1], fsize=9.2, row_h=0.325, head_h=0.34)
yy = _tb_bottom + 0.14
callout(s, ML, yy, CW, "The Wallet is a **thin React Native shell over native libraries**. The protocol logic is not in JavaScript — it is in Kotlin and Swift, shipped as versioned artefacts. That is why a wallet bug is often a library bug, and why you must track library versions, not just the app version.", kind='tip', size=10.3)
notes(s, ["This is a reference slide; do not read every row. Point at the three groups: two holder apps, one backend, and a set of shared libraries.",
          "The big idea is the callout: Inji deliberately pushed protocol work into cross-platform native libraries so Android, iOS and server-side Java can share one implementation. inji-openid4vp is Kotlin Multiplatform and ships as both AAR and JAR — the same library runs in the phone and inside Mimoto.",
          "Tell people to write down the library versions their build pins. In the wallet these are declared in android/app/build.gradle.",
          "Certify and Verify are reference implementations. Brazil may replace either with its own system and still be fully interoperable — that is the point of the standards."],
      caveats=["Library versions in this deck were read from the wallet's build file at the time of writing; treat them as illustrative and check your own branch.",
               "Not every library exists in every language yet. iOS parity lags Android on some features — verify before promising an iOS date."],
      questions=["Do we have to use Inji Certify as the issuer? — No. Any OpenID4VCI-compliant issuer works. Section 18.",
                 "Is there a JS OpenID4VP library for Inji Web? — Web's presentation path goes through Mimoto, which uses the JAR."],
      minutes="5 min")
footer(s)

# =================================================================== 9. TRUST BOUNDARIES
s, y = slide("Trust boundaries — who can hurt you, and how", kicker="Security framing",
             sub="Draw the boxes you control. Everything crossing a boundary line is attacker-reachable input.")
zones = [
 ("Issuer domain", "Issuer service, signing keys, JWKS or DID document, issuer metadata endpoint.",
  "You trust the signature, not the connection.", C['primary'], C['primary_l']),
 ("Your domain", "Mimoto, Inji Web, issuer catalogue, trusted-verifier list, Postgres, Redis.",
  "You own patching, TLS, data residency, logs.", C['violet'], C['violet_l']),
 ("User's device", "Inji Wallet, OS keystore, encrypted credential store, camera, browser.",
  "Assume it can be rooted. Keys in hardware where possible.", C['accent'], C['accent_l']),
 ("Verifier domain", "Verifier app, its response_uri, its client metadata and keys.",
  "Any QR can claim to be a verifier. Validate before you send.", C['green'], C['green_l']),
]
bw = (CW - 3 * 0.22) / 4
for i, (t, d, risk, col, tint) in enumerate(zones):
    x = ML + i * (bw + 0.22)
    rect(s, x, y, bw, 2.55, fill=tint, line=col, lw=1.4, dash=2,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    _, t2 = tb(s, x + 0.18, y + 0.18, bw - 0.36, 0.3)
    para(t2, t.upper(), size=10, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.18, y + 0.56, bw - 0.36, 1.1)
    para(t3, d, size=9.6, color=C['ink2'], first=True, line_spacing=1.28)
    line(s, x + 0.18, y + 1.76, x + bw - 0.18, y + 1.76, col, 1.0, dash=2)
    _, t4 = tb(s, x + 0.18, y + 1.88, bw - 0.36, 0.6)
    para(t4, risk, size=9.2, color=col, bold=True, first=True, line_spacing=1.25)
yy = y + 2.80
_, tf = tb(s, ML, yy, CW, 0.3)
para(tf, "FOUR THINGS THAT CROSS A BOUNDARY — AND THEREFORE NEED VALIDATION", size=9.5,
     color=C['red'], bold=True, first=True)
items = [
 ("A scanned QR code", "Could encode any URL. Never auto-open, never auto-submit."),
 ("Issuer metadata + keys", "Fetched over the network. Pin the host; check the signature covers what you think it covers."),
 ("An authorization request", "A verifier you have never met. Check client_id scheme, signature and registered response_uri."),
 ("A deep link into the app", "Any installed app or web page can fire it. Treat parameters as hostile."),
]
for i, (t, d) in enumerate(items):
    x = ML + i * (CW / 4)
    rect(s, x, yy + 0.34, 0.05, 0.72, fill=C['red'])
    _, t2 = tb(s, x + 0.16, yy + 0.34, CW / 4 - 0.34, 0.28)
    para(t2, t, size=10, color=C['ink'], bold=True, first=True)
    _, t3 = tb(s, x + 0.16, yy + 0.62, CW / 4 - 0.34, 0.7)
    para(t3, d, size=9.2, color=C['muted'], first=True, line_spacing=1.22)
notes(s, ["Frame the day's security thinking now, so that later sections can just point back here.",
          "The four boxes are the only four places code runs. Ask the room which boxes Brazil will own — the answer decides a lot of the deployment section.",
          "The bottom strip is the practical takeaway: four untrusted inputs. Every security incident in a wallet project comes through one of them.",
          "Emphasise the device box: a rooted phone is not a theoretical concern for a national wallet. That is why key material goes to the platform keystore and why key attestation exists."],
      caveats=["TLS protects the channel, not the content. A credential is trustworthy because it is signed, not because it arrived over HTTPS. Say this sentence twice.",
               "The Wallet cannot fully defend a rooted device. Design so a compromised device costs one user, not the system."],
      questions=["Can we detect rooted devices? — Partially; Play Integrity / SafetyNet style attestation. Mimoto exposes attestation verification endpoints. It is a signal, not a guarantee."],
      minutes="6 min")
footer(s)

# =================================================================== 10. PROTOCOL MAP
s, y = slide("Where OpenID4VCI and OpenID4VP actually sit", kicker="Protocol map",
             sub="Two protocols, two directions, one holder in the middle. Learn which questions belong to which.")
lx = ML
rect(s, lx, y, 5.95, 2.95, fill=C['primary_l'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
_, tf = tb(s, lx + 0.28, y + 0.20, 5.4, 0.36)
para(tf, "OpenID4VCI — getting a credential", size=14, color=C['primary'], bold=True, first=True)
_, tf = tb(s, lx + 0.28, y + 0.58, 5.4, 0.3)
para(tf, "OpenID for Verifiable Credential Issuance", size=9.5, color=C['muted'], italic=True, first=True)
bullets(s, lx + 0.28, y + 0.95, 5.4, [
    "Built on **OAuth 2.0**. Same grammar: authorization endpoint, token endpoint, scopes.",
    "Adds: a credential endpoint, issuer metadata, credential offers, and a **proof** that the wallet holds a key.",
    "Inji supports **draft 11 and draft 13** via `inji-vci-client`.",
    "Grants: `authorization_code` and `urn:ietf:params:oauth:grant-type:pre-authorized_code`.",
], size=10.3, bullet_col=C['primary'])
rx = ML + 6.28
rect(s, rx, y, 5.95, 2.95, fill=C['green_l'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
_, tf = tb(s, rx + 0.28, y + 0.20, 5.4, 0.36)
para(tf, "OpenID4VP — showing a credential", size=14, color=C['green'], bold=True, first=True)
_, tf = tb(s, rx + 0.28, y + 0.58, 5.4, 0.3)
para(tf, "OpenID for Verifiable Presentations", size=9.5, color=C['muted'], italic=True, first=True)
bullets(s, rx + 0.28, y + 0.95, 5.4, [
    "Also OAuth-shaped, but there is no access token for the verifier — the **credential is the response**.",
    "Verifier sends an authorization request; wallet returns a `vp_token`.",
    "Inji supports **draft 21 and draft 23** via `inji-openid4vp`.",
    "Response modes: `direct_post`, `direct_post.jwt` (encrypted), plus `iar-post` variants.",
], size=10.3, bullet_col=C['green'])
yy = y + 3.20
rows = [
 ["Who starts it?", "Either the wallet (pick an issuer) or the issuer (credential offer QR)", "Always the verifier"],
 ["What is transported?", "A credential, signed by the issuer", "A presentation, signed by the holder, containing credentials"],
 ["Who authenticates the user?", "The issuer's authorization server (eSignet, Keycloak, gov.br…)", "Nobody — consent in the wallet is the gate"],
 ["What stops replay?", "PKCE + one-time codes + `c_nonce` inside the proof", "`nonce` + `state` from the verifier, echoed in the response"],
 ["Typical failure owner", "Issuer metadata, auth server config, proof format", "Client-id scheme, matching, response_uri, encryption keys"],
]
table(s, ML, yy, CW, ["Question", "OpenID4VCI", "OpenID4VP"], rows,
      col_w=[2.6, 4.8, 4.8], fsize=9.4, row_h=0.42, head_h=0.34)
notes(s, ["The comparison table is the slide. People who internalise it stop mixing up the two protocols for the rest of their careers.",
          "Row 3 is the one that surprises people: in OpenID4VP nobody authenticates the user. There is no login. Possession of the credential plus the holder's key, plus consent in the wallet, is the whole story. That is deliberate — it is what makes presentation work offline and across organisations.",
          "Row 4 is the security skeleton. Come back to it in section 4 and again in section 10.",
          "Mention draft versions now: Inji supports VCI draft 11 and 13, VP draft 21 and 23. Draft skew is the single most common interoperability problem with external parties."],
      caveats=["'Draft' is not a warning label here — these drafts are what the whole ecosystem ships against. But two parties on different drafts will fail in confusing ways. Agree the draft in writing with every external partner.",
               "OpenID4VP draft 23 removes client_id_scheme as a separate parameter; the library infers the draft from whether that parameter is present."],
      questions=["Is there a final version? — The specs continue to move. Plan for version negotiation, not a one-time integration."],
      minutes="6 min")
footer(s, )

# =================================================================== 11. ONLINE/OFFLINE
s, y = slide("Online and offline: what needs a network, and when", kicker="Connectivity",
             sub="A common planning mistake is assuming the whole journey is online, or that everything works offline.")
rows = [
 ["Discover issuers", "Wallet → Mimoto → issuer well-known", "!!Network required", "Cached in Mimoto (Caffeine/Redis, configurable TTL)"],
 ["Authenticate the user", "Wallet → authorization server (browser)", "!!Network required", "No offline equivalent"],
 ["Download the credential", "Wallet → issuer credential endpoint", "!!Network required", "Retry with backoff; Mimoto has a poll/retry setting"],
 ["Verify at download", "`vc-verifier` in the wallet", "!!Usually network", "Needs issuer key — may hit JWKS/DID; cache keys"],
 ["View a stored credential", "Local store only", "++Fully offline", "Rendering uses cached issuer metadata"],
 ["Show a QR of the credential", "PixelPass or Claim 169 QR", "++Fully offline", "Issuer-provided Claim 169 QR is preferred when present"],
 ["Present over OpenID4VP", "Wallet → verifier `response_uri`", "!!Network required", "`direct_post` is an HTTP POST to the verifier"],
 ["Present over BLE (proximity)", "`tuvali` transport", "++Fully offline", "Device-to-device; separate from OpenID4VP"],
]
_tb_bottom = table(s, ML, y, CW, ["Step", "Path", "Connectivity", "Notes"], rows,
      col_w=[2.6, 3.5, 2.0, 4.2], fsize=9.4, row_h=0.42, head_h=0.34)
yy = _tb_bottom + 0.16
c1 = callout(s, ML, yy, 5.95, "**Issuance is an online act.** Plan connectivity at the point where citizens obtain credentials — a kiosk, an office, an assisted-enrolment point.", kind='warn', size=10.3)
callout(s, ML + 6.28, yy, 5.95, "**Presentation can be offline** only if you choose an offline-capable channel: a QR the verifier scans, or BLE. OpenID4VP itself always needs a network.", kind='good', size=10.3)
notes(s, ["This slide prevents an expensive misunderstanding. Teams often promise 'offline wallet' and mean different things.",
          "Walk the rows. The clean rule: obtaining is online, holding and displaying are offline, presenting depends entirely on the channel you choose.",
          "The BLE row matters for Brazil if proximity use cases (transport, border, events) are in scope. Tuvali is Inji's own BLE transport and is not the same thing as ISO 18013-5 device retrieval — be precise about that if somebody asks for 'mDL offline'.",
          "The Claim 169 QR row is a MOSIP-specific optimisation: the issuer can embed a pre-signed CBOR QR in the credential, and the wallet displays that rather than generating its own."],
      caveats=["Verification at download time may need the issuer's key, which may be a network fetch. If that call fails the credential download can fail even though the credential itself arrived. That is a real and confusing failure — it appears again in troubleshooting.",
               "Offline presentation via QR means the verifier trusts a static artefact; freshness/replay protection is weaker than OpenID4VP with a nonce. Say so explicitly."],
      questions=["Can the wallet queue an issuance request and complete it later? — Not in the standard flow; the authorization code and c_nonce are short-lived."],
      minutes="5 min")
footer(s, )

# =================================================================== SECTION 2
section("End-to-end demo, first", "20 min",
        "We run the whole thing before we explain any of it. Watch the screen, not the slides. Questions are welcome — answers may be deferred to the matching section.",
        ["Obtain and download a credential",
         "Inspect what was stored",
         "Present it to a verifier",
         "Consent and selective disclosure",
         "The same journey on the web",
         "What was happening behind the glass"], highlight=('issuer', 'mimoto', 'wallet', 'store', 'verifier'), num="2")
notes(prs.slides[-1],
      ["Say why the demo is first: protocol slides land much better once people have seen the artefact move.",
       "Ask people to note down every moment they did not understand. You will collect those at the end of the demo and map each one to the section that answers it — that turns confusion into an agenda."],
      caveats=["Have a recorded fallback. A live demo that fails at 09:40 costs you the room's attention for an hour.",
               "Use a pre-provisioned test identity. Do not do live enrolment on stage."],
      minutes="20 min for the section")

# ------------------------------------------------- demo 1
demo_slide(1, "Obtain a credential — the full issuance journey", "8 minutes",
  ["A running issuer (Inji Certify or your own) with at least one credential configuration.",
   "Mimoto up, with the issuer present in `mimoto-issuers-config.json` and `enabled: true`.",
   "Wallet build pointing at your `MIMOTO_HOST`.",
   "A test identity that the issuer's authorization server will accept."],
  ["User opens the Wallet and taps **Add credential**.",
   "A list of issuers appears, each with logo and description.",
   "User picks one, and picks which credential type to download.",
   "A browser opens for login — OTP, biometric, whatever the AS is configured for.",
   "The browser closes, the app spins, the card appears."],
  ["Wallet asked Mimoto for the issuer list (`GET /v2/issuers`).",
   "Wallet fetched `/.well-known/openid-credential-issuer` for metadata.",
   "It discovered the authorization server and built an authorization URL **with PKCE**.",
   "The code came back on the wallet's `oauthredirect` deep link.",
   "Token exchange, then a **proof JWT** signed by a key the wallet just created, then the credential request."],
  fail="The two usual suspects are (a) the redirect URI registered at the authorization server does not match the one the wallet sends, and (b) the issuer's well-known endpoint is unreachable from the phone's network. Have both ready to show.")
notes(prs.slides[-1],
      ["Narrate the user journey first with no jargon at all — 'pick an issuer, log in, get a card'. Then do the same journey again pointing at the third column.",
       "Pause on the browser step. That browser is the authorization server, not Inji. Whatever Brazil uses for citizen login goes there, and it is the single biggest external dependency in issuance.",
       "Call out the moment the key is created: before the credential request, the wallet generates a key pair and signs a proof JWT proving it holds the private key. That is what binds the credential to this device. We pull it apart in section 4.",
       "If you have a proxy or charles/mitm set up, show the actual HTTP calls. Nothing beats seeing the real traffic."],
      caveats=["Do not claim the wallet talks to the issuer for everything. Discovery and token exchange are brokered by Mimoto in the standard Inji configuration; the credential request goes to the issuer directly.",
               "Downloads can be slow; Mimoto has a configurable download timeout (mosip.inji.openId4VCIDownloadVCTimeout) — mention it rather than standing in awkward silence."],
      questions=["Why does a browser open instead of an in-app form? — Because the wallet must never see the user's credentials for the authorization server. That is the whole point of the authorization code flow.",
                 "Could we skip the login? — Yes, with the pre-authorized code flow. Section 3."],
      minutes="8 min")

# ------------------------------------------------- demo 1b presentation
demo_slide(2, "Present a credential — the full verification journey", "8 minutes",
  ["A verifier (Inji Verify or your own) that can render an OpenID4VP QR.",
   "The verifier registered in `mimoto-trusted-verifiers.json` with its `client_id` and `response_uri`.",
   "The credential from Demo 1 already in the wallet.",
   "A second screen so the room sees both the verifier and the phone."],
  ["Verifier shows a QR code and says what it wants.",
   "User scans it with the Wallet.",
   "Wallet shows: **who is asking**, and **exactly which claims**.",
   "User picks a credential and taps share.",
   "Verifier screen flips to success, showing only the claims it asked for."],
  ["The QR carried an OpenID4VP authorization request (or a `request_uri` pointing to one).",
   "`inji-openid4vp` validated the request against the `client_id` scheme and the trusted-verifier list.",
   "Wallet matched stored credentials against the `presentation_definition` constraints.",
   "It built an **unsigned VP token**, the wallet signed it, the library POSTed it to `response_uri`.",
   "The verifier checked the issuer signature, the holder binding, and its own `nonce`."],
  fail="If the verifier is not in the trusted list, the wallet refuses before showing anything. That is correct behaviour, and it is worth failing on purpose once — see Demo 8.")
notes(prs.slides[-1],
      ["The moment that matters is the consent screen. Freeze on it. Point out it names the verifier and lists the claims. Everything in OpenID4VP exists to make that screen honest.",
       "Point out what the verifier screen does NOT show: any claim it did not request. If the credential format supports selective disclosure, the undisclosed claims never left the phone.",
       "Mention the direction of travel: the wallet POSTs to the verifier. The verifier never connects to the phone. That is why cross-device works without any inbound connectivity to the handset.",
       "Collect the room's 'I did not understand X' notes now and map them to sections."],
      caveats=["With ldp_vc the whole credential goes across — selective disclosure is a property of SD-JWT VC and mDoc, not of OpenID4VP. Be careful not to over-promise on this slide.",
               "Inji Wallet may ask for face verification before sharing if the selected credential contains a face image; that is an Inji product behaviour, not part of OpenID4VP."],
      questions=["Can the verifier replay what it received? — It can re-present the VP token, which is why the nonce and the verifier's own audience checks matter. Section 8.",
                 "What if the user has two matching credentials? — The wallet shows both and the user chooses."],
      minutes="8 min")

# =================================================================== SECTION 3
section("Credential issuance with OpenID4VCI", "35 min",
        "From 'I want a credential' to 'it is stored'. Every message, in order, with the fields that actually matter when something breaks.",
        ["Credential Offer",
         "Issuer + authorization server metadata",
         "Pre-authorized code flow",
         "Authorization code flow + PKCE",
         "Token request and response",
         "Credential request, proof, response"],
        highlight=('issuer', 'mimoto', 'wallet', 'store'), num="3")
notes(prs.slides[-1],
      ["This is the densest section of the morning. Warn people, and promise the payoff: after this, issuance logs stop being mysterious.",
       "Keep referring back to Demo 1. Every slide here is a zoom-in on something they already watched happen."],
      minutes="35 min for the section")

# ------------------------------------------------- VCI endpoints
s, y = slide("OpenID4VCI: five endpoints and one new idea", kicker="The shape of the protocol",
             sub="If you know OAuth 2.0, you already know 80% of this. The new part is the credential endpoint and the proof.")
rows = [
 ["`/.well-known/openid-credential-issuer`", "Credential Issuer", "GET", "What credentials exist, in what formats, at which endpoint, with what display labels"],
 ["`/.well-known/oauth-authorization-server`", "Authorization Server", "GET", "Where to authorize, where to get tokens, which grants and response types are supported"],
 ["`authorization_endpoint`", "Authorization Server", "GET (browser)", "Authenticate the user and issue a one-time authorization code"],
 ["`token_endpoint`", "Authorization Server", "POST", "Exchange the code (or pre-authorized code) for an access token and a `c_nonce`"],
 ["`credential_endpoint`", "Credential Issuer", "POST", "The new one. Send a proof, get a credential back."],
]
_tb_bottom = table(s, ML, y, CW, ["Endpoint", "Who hosts it", "Method", "What it gives you"], rows,
      col_w=[4.0, 2.2, 1.6, 4.4], fsize=9.5, row_h=0.50, head_h=0.34)
yy = _tb_bottom + 0.22
card(s, ML, yy, 5.95, 2.05, "Two ways a journey starts", [
    "**Wallet-initiated** (trusted issuer): the user browses a list of issuers the wallet already knows and picks one.",
    "**Issuer-initiated** (credential offer): the issuer produces a QR or a link; scanning it starts the journey.",
    "Inji supports both. `inji-vci-client` exposes them as `requestCredentialFromTrustedIssuer` and `fetchCredentialUsingCredentialOffer`.",
], accent=C['primary'], tint=C['primary_l'], size=10.2)
card(s, ML + 6.28, yy, 5.95, 2.05, "Two grant types", [
    "**Authorization code** — the user logs in at the authorization server. Always with PKCE from a mobile wallet.",
    "**Pre-authorized code** — the issuer already authenticated the user out-of-band, so no login happens in the wallet. Optionally protected by a `tx_code`.",
    "Which one you use is the issuer's decision, announced in the credential offer.",
], accent=C['accent'], tint=C['accent_l'], size=10.2)
notes(s, ["Anchor on the OAuth similarity — it lowers the anxiety in the room immediately.",
          "The only genuinely new endpoint is the credential endpoint, and the only genuinely new concept is the proof: a JWT signed by a key the wallet controls, sent with the credential request, so the issuer can bind the credential to that key.",
          "Explain the two starting points with concrete Brazilian examples: wallet-initiated is 'I open my wallet and want my vaccination record'; issuer-initiated is 'the clinic prints a QR on my discharge paper'.",
          "Note that the issuer decides the grant type, not the wallet. The wallet reads it out of the credential offer or the metadata."],
      caveats=["Metadata path detail: the well-known path is inserted between host and path components per RFC 8414 conventions. Issuers that host the credential issuer at a sub-path frequently get this wrong, and the wallet then 404s. This is a top-three integration bug.",
               "Draft 11 and draft 13 differ in the metadata shape (credentials_supported vs credential_configurations_supported). inji-vci-client handles both; your issuer must pick one and be consistent."],
      questions=["Does the wallet need a client secret? — No. A mobile wallet is a public client; that is exactly why PKCE is mandatory."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- credential offer
s, y = slide("The Credential Offer", kicker="Message 1",
             sub="A small JSON object, delivered by QR or deep link, that says: this issuer, this credential, this grant.")
codebox(s, ML, y, 6.05, 2.95, [
 '{',
 '  "credential_issuer": "https://certify.example.gov.br",',
 '  "credential_configuration_ids": [',
 '    "CPFCredentialSdJwt"',
 '  ],',
 '  "grants": {',
 '    "urn:ietf:params:oauth:grant-type:pre-authorized_code": {',
 '      "pre-authorized_code": "412350404962811318869516",',
 '      "tx_code": { "input_mode": "numeric", "length": 6 },',
 '      "authorization_server": "https://as.example.gov.br"',
 '    }',
 '  }',
 '}',
], label="CREDENTIAL OFFER — BY VALUE", size=9.4, hl=[1, 3, 7])
codebox(s, ML + 6.35, y, 5.88, 1.20, [
 'openid-credential-offer://?credential_offer_uri=',
 '  https%3A%2F%2Fcertify.example.gov.br%2Foffer%2Fabc123',
], label="CREDENTIAL OFFER — BY REFERENCE", size=9.4)
yy = y + 1.52
bullets(s, ML + 6.35, yy, 5.88, [
 "`credential_issuer` is the **identity** of the issuer. Everything else is derived from it by fetching metadata.",
 "`credential_configuration_ids` must match keys in the issuer's metadata. A typo here produces an unhelpful error.",
 "`grants` tells the wallet which flow to run. Absent grants means: fall back to authorization code.",
 "`tx_code` is a short code the issuer gives the user separately (SMS, printed slip). It stops a stolen QR from being redeemed.",
 "By reference keeps the QR small and keeps the pre-authorized code off the printed page.",
], size=10.2)
callout(s, ML, y + 3.20, 6.05, "Inji Wallet scans this, hands it straight to `inji-vci-client`, and the library decides the flow. The app does not parse the offer itself.", kind='tip', size=10.2)
notes(s, ["Read the JSON aloud field by field. It is short and every field earns its place.",
          "Stress that credential_issuer is an identifier AND a base URL. The wallet appends /.well-known/openid-credential-issuer to it. If Brazil's issuer sits behind a path prefix or a reverse proxy that rewrites paths, this is where it breaks.",
          "tx_code is the anti-theft measure for printed offers. Explain the scenario: a QR printed on a discharge slip left on a table. Without tx_code, whoever picks it up gets the credential.",
          "Mention that inji-vci-client caches the fetched issuer metadata for the duration of the flow — so a metadata endpoint that is slow costs you once, not five times."],
      caveats=["credential_configuration_ids is an array, but Inji does not support batch credential download. One credential per journey.",
               "The offer has no signature. Its trustworthiness comes from the issuer metadata fetch that follows, over TLS, plus the optional tx_code. Do not treat the offer itself as authenticated."],
      questions=["Can the offer expire? — The pre-authorized code does. The offer object itself carries no expiry field; the issuer enforces it server-side.",
                 "What if we want the user to confirm the issuer first? — inji-vci-client has an onCheckIssuerTrust callback for exactly that."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- metadata
s, y = slide("Issuer metadata and authorization server metadata", kicker="Discovery",
             sub="Two GETs that decide whether the rest of the flow is even possible. Most 'the wallet does not work' tickets end here.")
codebox(s, ML, y, 6.05, 3.55, [
 'GET https://certify.example.gov.br',
 '      /.well-known/openid-credential-issuer',
 '',
 '{',
 '  "credential_issuer": "https://certify.example.gov.br",',
 '  "credential_endpoint": ".../credential",',
 '  "authorization_servers": ["https://as.example.gov.br"],',
 '  "credential_configurations_supported": {',
 '    "CPFCredentialSdJwt": {',
 '      "format": "vc+sd-jwt",',
 '      "vct": "CPFCredential",',
 '      "scope": "cpf_vc_ldp",',
 '      "proof_types_supported": {',
 '        "jwt": { "proof_signing_alg_values_supported":',
 '                 ["RS256", "ES256"] } },',
 '      "claims": { "nome": {"display":[{"name":"Nome"}]} },',
 '      "display": [{ "name": "CPF", "locale": "pt-BR" }]',
 '    }',
 '  }',
 '}',
], label="CREDENTIAL ISSUER METADATA", size=8.9, hl=[6, 9, 12])
codebox(s, ML + 6.35, y, 5.88, 1.90, [
 'GET https://as.example.gov.br',
 '      /.well-known/oauth-authorization-server',
 '',
 '{ "issuer": "https://as.example.gov.br",',
 '  "authorization_endpoint": ".../authorize",',
 '  "token_endpoint": ".../token",',
 '  "grant_types_supported": ["authorization_code"],',
 '  "response_types_supported": ["code"] }',
], label="AUTHORIZATION SERVER METADATA", size=8.9)
yy = y + 2.18
bullets(s, ML + 6.35, yy, 5.88, [
 "The wallet reads `authorization_servers` from the issuer metadata and takes the **first entry**. Multiple-server negotiation is not implemented.",
 "It then checks `grant_types_supported` contains a grant it can run — today, `authorization_code`. If not, it stops with a clear error.",
 "`display` and `claims[].display` drive the labels and field order on the card. If your card looks wrong, fix the metadata, not the app.",
 "Mimoto caches both documents (`cache.credential-issuer.wellknown.expiry-time-in-min`). After changing metadata, **expect a stale window**.",
], size=10.0)
notes(s, ["This slide answers more support tickets than any other in the deck.",
          "Point at the highlighted lines: authorization_servers, format, proof_types_supported. Those three drive everything downstream.",
          "The display metadata point is worth labouring. Teams routinely try to hard-code Portuguese labels into the wallet. Do not. Put pt-BR display entries in the issuer metadata and the wallet renders them. Field ORDER also comes from metadata in draft 13.",
          "The caching point saves an afternoon: after an issuer metadata change, Mimoto will keep serving the old copy until the TTL expires. Either wait, restart, or lower the TTL in non-production."],
      caveats=["Inji takes only the first entry of authorization_servers. If Brazil plans several authorization servers per issuer, that is a gap to raise upstream.",
               "The well-known document must be reachable from the phone, not just from your laptop. Split-horizon DNS and internal-only hostnames cause 'works on my machine' failures here.",
               "Draft 11 issuers publish credentials_supported as an array; draft 13 publishes credential_configurations_supported as an object. Mixing them silently produces an empty credential list."],
      questions=["Can we serve different metadata per locale? — Use the display array with locale entries rather than different documents."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- seq: pre-auth
s, y = slide("Pre-authorized code flow, step by step", kicker="Sequence — issuer-initiated",
             sub="No login inside the wallet. The issuer already knows who the user is.")
sequence(s, ["User", "Inji Wallet", "inji-vci-client", "Authorization Server", "Credential Issuer"],
 [(4, 0, "Issuer shows a Credential Offer QR", 'resp'),
  (0, 1, "Scan the QR"),
  (1, 2, "`fetchCredentialUsingCredentialOffer(offer)`"),
  (2, 4, "`GET /.well-known/openid-credential-issuer`"),
  (4, 2, "issuer metadata (cached)", 'resp'),
  (2, 3, "`GET /.well-known/oauth-authorization-server`"),
  (3, 2, "token endpoint, grants supported", 'resp'),
  (2, 1, "`getTxCode()` — only if the offer asks", 'resp'),
  (0, 1, "User types the 6-digit tx_code"),
  (2, 1, "`getTokenResponse(tokenRequest)` callback", 'resp'),
  (1, 3, "`POST /token` pre-authorized_code + tx_code"),
  (3, 1, "`access_token` + `c_nonce`", 'resp'),
  (2, 1, "`getProofJwt(issuer, c_nonce, algs)` callback", 'resp'),
  (1, 1, "Generate key, sign proof JWT in keystore", 'self'),
  (2, 4, "`POST /credential` + Bearer + proof"),
  (4, 2, "credential", 'resp'),
  (2, 1, "`CredentialResponse` → verify → store", 'resp'),
 ], top=1.42, height=5.20)
notes(s, ["Walk it slowly with a laser pointer. Fifteen minutes of this slide is not wasted time.",
          "The shape to notice: the library orchestrates, but the WALLET performs every action that needs a key, a screen, or the network stack. inji-vci-client calls back into the app for tx_code, for the token request, and for the proof JWT. That is a deliberate design: the library never touches private keys.",
          "Step 11: the token request carries the pre-authorized code and the tx_code. There is no browser, no redirect, no PKCE — PKCE belongs to the authorization code flow only.",
          "Step 12: c_nonce is the issuer's freshness challenge. It goes inside the proof JWT at step 14. Without it, an attacker could replay an old proof.",
          "Step 17: the wallet verifies the credential with vc-verifier before storing it. A credential that fails verification is not saved."],
      caveats=["tx_code is optional. If the offer does not ask for one, steps 8 and 9 disappear — and so does the protection against a stolen offer.",
               "Some issuers return c_nonce from the credential endpoint on a 'nonce required' error rather than from the token endpoint. Handle both.",
               "Note there is no PKCE here at all. People often assume PKCE is everywhere; it is not."],
      questions=["Who generates the pre-authorized code? — The issuer, at the moment it creates the offer, bound to a specific user.",
                 "Can the same offer be redeemed twice? — It must not be. Single-use enforcement is the issuer's job."],
      minutes="9 min")
footer(s)

# ------------------------------------------------- seq: auth code
s, y = slide("Authorization code flow with PKCE, step by step", kicker="Sequence — wallet-initiated",
             sub="The user logs in at the authorization server, in a real browser, not inside the app's UI.")
sequence(s, ["User", "Inji Wallet", "inji-vci-client", "Authorization Server", "Credential Issuer"],
 [(1, 2, "`requestCredentialFromTrustedIssuer(issuer, configId)`"),
  (2, 4, "`GET /.well-known/openid-credential-issuer`"),
  (2, 3, "`GET /.well-known/oauth-authorization-server`"),
  (2, 2, "PKCE session: verifier, challenge=S256, state", 'self'),
  (2, 1, "`authorizeUser(authorizationUrl)` callback", 'resp'),
  (1, 3, "System browser → `/authorize` + `code_challenge`"),
  (0, 3, "User authenticates (OTP / biometric)"),
  (3, 1, "302 → `…inji://oauthredirect?code=…`", 'resp'),
  (1, 2, "`sendAuthCode(code)`"),
  (2, 1, "`getTokenResponse()` — carries `code_verifier`", 'resp'),
  (1, 3, "`POST /token` code + code_verifier + client_id"),
  (3, 1, "`access_token` (Bearer) + `c_nonce`", 'resp'),
  (2, 1, "`getProofJwt(issuer, c_nonce, algs)`", 'resp'),
  (1, 1, "Sign proof JWT with device-held key", 'self'),
  (2, 4, "`POST /credential` format + proof + Bearer"),
  (4, 2, "credential (JSON / JWT / base64url CBOR)", 'resp'),
  (2, 1, "verify with `vc-verifier` → encrypted store", 'resp'),
 ], top=1.42, height=5.20)
notes(s, ["Compare directly with the previous slide. The delta is steps 4 to 11: PKCE session, browser, user login, code, code_verifier.",
          "Step 6 — the SYSTEM browser, not a WebView. This matters: a WebView controlled by the app could read the user's password. Using the system browser is a security requirement, and it is also why the deep-link configuration has to be right.",
          "Step 8 — the redirect comes back on a custom scheme registered by the app. In Inji Wallet that is io.mosip.residentapp.inji://oauthredirect, declared in AndroidManifest.xml and in the issuer configuration in Mimoto. These two values must match exactly, including trailing slashes.",
          "Step 11 — the code_verifier proves the same app that started the flow is finishing it. Detail on the next section.",
          "Note that in Inji's standard deployment the token exchange is brokered through Mimoto (get-token/{issuer}) so that any client secret stays server-side. The library's callback gives the app the freedom to route it that way."],
      caveats=["The redirect_uri must be registered identically at the authorization server, in mimoto-issuers-config.json, and in the app manifest. Three places, one value. Most first-day failures are here.",
               "Custom URI schemes are first-come-first-served on Android. Two apps registering the same scheme is a real hijack risk — prefer App Links / Universal Links where you can.",
               "state is not optional in practice: it is how the wallet knows the response belongs to the request it started."],
      questions=["Why not use an in-app WebView, it looks nicer? — Because it breaks the security model and many authorization servers refuse it.",
                 "Can we do silent re-issuance? — Only if the authorization server supports refresh tokens for this client; Inji's flow assumes a fresh authorization."],
      minutes="9 min")
footer(s)

# ------------------------------------------------- token + credential messages
s, y = slide("Token request, credential request, credential response", kicker="Messages 2, 3 and 4",
             sub="Three HTTP exchanges. Learn the field names — they are what appears in your logs.")
codebox(s, ML, y, 5.95, 1.62, [
 'POST /token   Content-Type: application/x-www-form-urlencoded',
 '',
 'grant_type=authorization_code',
 '&code=SplxlOBeZQQYbYS6WxSbIA',
 '&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk',
 '&client_id=inji-wallet&redirect_uri=io.mosip…://oauthredirect',
], label="TOKEN REQUEST", size=8.7, hl=[4])
codebox(s, ML, y + 1.92, 5.95, 1.40, [
 '{ "access_token": "eyJhbGciOi…",',
 '  "token_type": "Bearer",',
 '  "expires_in": 3600,',
 '  "c_nonce": "tZignsnFbp",',
 '  "c_nonce_expires_in": 86400 }',
], label="TOKEN RESPONSE", size=8.7, hl=[3])
codebox(s, ML + 6.28, y, 5.95, 2.20, [
 'POST /credential   Authorization: Bearer eyJhbGciOi…',
 '',
 '{ "format": "vc+sd-jwt",',
 '  "vct": "CPFCredential",',
 '  "proof": {',
 '    "proof_type": "jwt",',
 '    "jwt": "eyJ0eXAiOiJvcGVuaWQ0dmNpLXByb29mK2p3dCI…"',
 '  } }',
], label="CREDENTIAL REQUEST", size=8.7, hl=[4, 5, 6])
codebox(s, ML + 6.28, y + 2.50, 5.95, 1.24, [
 '{ "credential": "eyJraWQiOiJ…~WyJzYWx0Iiwibm9tZS…~" }',
 '',
 '// ldp_vc  -> a JSON-LD object',
 '// vc+sd-jwt -> compact JWT + "~" separated disclosures',
 '// mso_mdoc -> base64url-encoded CBOR',
], label="CREDENTIAL RESPONSE", size=8.7)
yy = y + 3.50
callout(s, ML, yy, 5.95, "`code_verifier` is the PKCE secret. `c_nonce` is the issuer's freshness challenge and must be echoed inside the proof JWT.", kind='note', size=10.2)
callout(s, ML + 6.28, y + 3.86, 5.95, "The **shape of the credential depends entirely on the format.** Your storage, rendering and verification code all branch here.", kind='warn', size=10.2)
notes(s, ["Four boxes, four minutes. Do not lecture; point at the highlighted fields.",
          "token_type is Bearer here. That is the current Inji behaviour — the access token is a bearer token, which means anyone who steals it in transit can use it. We discuss the alternative (DPoP) on the next slides, and whether Brazil should ask for it.",
          "c_nonce is the hinge between the token step and the credential step. It ties the proof to this issuance, right now. If your issuer does not return c_nonce, the proof cannot be replay-protected and many issuers will reject it.",
          "The credential response is deliberately format-agnostic in the protocol and completely format-specific in your code. That asymmetry is the main reason format choice is an architecture decision, not a detail."],
      caveats=["expires_in on the access token is usually short. A slow credential endpoint plus a short token lifetime equals intermittent 401s in production.",
               "Draft 13 allows the credential endpoint to respond asynchronously with a transaction_id and an acceptance token. Inji's wallet flow assumes the synchronous response; check what your issuer does.",
               "The proof JWT typ is openid4vci-proof+jwt. Issuers that do not check it are being lenient; do not rely on that."],
      questions=["Can we get several credentials in one call? — Batch issuance is out of scope for the Inji wallet today."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- where inji does what
s, y = slide("Who does what, in Inji's implementation", kicker="Mapping protocol to code",
             sub="The library orchestrates the protocol. The application owns keys, screens and the network. That split is deliberate.")
rows = [
 ["Read the credential offer", "`inji-vci-client`", "—", "—", "Library parses by value or by `credential_offer_uri`"],
 ["Fetch issuer metadata", "`inji-vci-client`", "caches copy for Web", "hosts it", "Wallet may also read it via Mimoto for the issuer list"],
 ["Discover the auth server", "`inji-vci-client`", "caches", "—", "First entry of `authorization_servers` only"],
 ["Build the PKCE session", "`inji-vci-client`", "—", "—", "`PKCESessionManager`, SHA-256, `S256`"],
 ["Open the browser", "**Wallet app**", "—", "—", "System browser via `authorizeUser` callback"],
 ["Exchange code for token", "**Wallet app**", "`POST /get-token/{issuer}`", "validates", "Routed via Mimoto so secrets stay server-side"],
 ["Create the key pair", "**Wallet app**", "—", "—", "`secure-keystore`, Android Keystore / iOS Keychain"],
 ["Sign the proof JWT", "**Wallet app**", "—", "—", "`getProofJwt` callback; library never sees the key"],
 ["Send the credential request", "`inji-vci-client`", "—", "issues", "Format-specific request builder"],
 ["Verify the credential", "`vc-verifier`", "same library", "—", "Signature, and for SD-JWT the disclosure digests"],
 ["Store it", "**Wallet app**", "Postgres for Web", "—", "MMKV + encryption on device; AES-GCM in DB for Web"],
]
_tb_bottom = table(s, ML, y, CW, ["Step", "Wallet side", "Mimoto", "Issuer", "Notes"], rows,
      col_w=[2.7, 2.2, 2.0, 1.3, 4.0], fsize=9.2, row_h=0.355, head_h=0.34)
yy = _tb_bottom + 0.16
callout(s, ML, yy, CW, "Read the bold rows: **every operation that touches a private key or a user-facing screen is in the application, not the library.** When you port Inji to a new platform, that is the boundary you re-implement.", kind='tip', size=10.3)
notes(s, ["This is the slide developers photograph. Give them a moment.",
          "The callback architecture is the important idea. inji-vci-client is a state machine that says 'I need a tx_code', 'I need a token', 'I need a proof' — and the wallet answers. The library is deliberately incapable of signing anything.",
          "Row 6 is an Inji design decision worth discussing with Brazil: Mimoto brokers the token exchange so that any client authentication material stays on the server. If Brazil's authorization server uses a public client with PKCE only, this hop could in principle be removed — but it also gives you a central place for logging and policy.",
          "Row 10: the wallet verifies at download. A credential that fails verification is never stored. Some teams want to store-and-warn instead; that is a product decision."],
      caveats=["Mimoto's /get-token/{issuer} endpoint is Inji-specific, not part of OpenID4VCI. Do not describe it to external partners as a standard endpoint.",
               "The iOS library surface mirrors the Kotlin one, but verify feature parity on the version you pin."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- demo 2
demo_slide(3, "Inspect what was actually stored", "5 minutes",
  ["A credential downloaded in Demo 1.",
   "Android: `adb logcat` filtered on the app, or Flipper (the repo ships an `inji.flipper` config).",
   "For Inji Web: access to Mimoto's Postgres, or the `GET /wallets/{id}/credentials` response.",
   "A JWT decoder and a CBOR decoder open in a browser tab."],
  ["Open the credential detail view in the wallet.",
   "Field labels are in the issuer's language, in the issuer's order.",
   "A QR code appears on the card.",
   "Delete and re-download to show the whole cycle is repeatable."],
  ["Labels and order came from `credential_configurations_supported[..].claims[..].display` and the `order` property — **not** from app code.",
   "The stored blob is encrypted with a key held in the OS keystore; MMKV holds the ciphertext.",
   "The QR is the issuer's Claim 169 QR if the credential carries one, otherwise generated by `pixelpass`.",
   "For mDoc the wallet keeps the decoded JSON only in memory, never on disk."],
  fail="If the labels appear as raw claim names, the issuer metadata is missing display entries — or Mimoto is serving a cached copy from before you fixed them.")
notes(prs.slides[-1],
      ["This demo converts an abstract slide into a visible fact: the wallet is a renderer of issuer metadata.",
       "Show the display/order behaviour by changing one label in the issuer metadata and re-downloading. If Mimoto's cache is in the way, that itself is a useful lesson — show the TTL property.",
       "For Portuguese: this is the moment to show that credential field labels are localised by the ISSUER, while the app chrome is localised by the app's own locale files. Two different localisation surfaces. Brazil must plan both."],
      caveats=["Do not show a real person's credential. Use test data.",
               "Decrypting the on-device store live is not practical in a workshop; describe it rather than attempting it."],
      minutes="5 min")

# =================================================================== SECTION 4
section("PKCE, DPoP, proofs and binding", "25 min",
        "Four mechanisms that all involve signing something. They protect completely different things, and mixing them up leads to bad architecture decisions.",
        ["Why PKCE exists, and what it does not do",
         "Why DPoP exists — and Inji's current position",
         "Bearer vs sender-constrained tokens",
         "Proof type vs cryptographic binding method",
         "Holder binding vs key binding",
         "Key attestation, and what it does not replace"], highlight=('wallet',), num="4")
notes(prs.slides[-1], ["Set expectations: this section is conceptual, and it is the one where precision pays off later.",
                       "Promise a single comparison table at the end that they can keep."],
      minutes="25 min for the section")

# ------------------------------------------------- PKCE
s, y = slide("PKCE — proving the app that finished is the app that started",
             kicker="RFC 7636", sub="Proof Key for Code Exchange. It protects the authorization code, and nothing else.")
codebox(s, ML, y, 5.95, 1.70, [
 '// 1. before opening the browser',
 'code_verifier  = random 43-128 char string',
 'code_challenge = BASE64URL(SHA-256(code_verifier))',
 '',
 '// 2. in the authorization URL',
 '?code_challenge=E9Melhoa…&code_challenge_method=S256',
], label="WHAT THE WALLET DOES", size=8.9)
codebox(s, ML, y + 2.02, 5.95, 1.20, [
 '// 3. in the token request, the original secret',
 'code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk',
 '',
 '// the AS recomputes the hash and compares',
], label="AND THEN", size=8.9)
card(s, ML + 6.28, y, 5.95, 1.78, "The attack it stops", [
 "A malicious app on the same phone registers the same custom URI scheme and intercepts the redirect.",
 "It now holds a valid authorization **code**.",
 "Without PKCE it can exchange that code for an access token. With PKCE it cannot — it never had the `code_verifier`.",
], accent=C['red'], tint=C['red_l'], size=10.2)
card(s, ML + 6.28, y + 2.02, 5.95, 2.45, "What PKCE does NOT do", [
 "It does not protect the **access token** after it is issued. A stolen bearer token is still usable.",
 "It does not authenticate the user, the app, or the device.",
 "It does not apply to the pre-authorized code flow — there is no authorization code there.",
 "It is not a substitute for `state`: `state` correlates the response to the request; PKCE binds the code to the client.",
], accent=C['amber'], tint=C['amber_l'], size=10.2)
callout(s, ML, y + 3.52, 5.95, "In Inji, PKCE is handled **inside** `inji-vci-client` (`PKCESessionManager`, SHA-256, method `S256`). The app never has to implement it.", kind='good', size=10.2)
notes(s, ["Tell the story before the mechanics: on a phone, the redirect back from the browser lands on a custom URI scheme, and on Android any app can claim a scheme. So the code can be stolen. PKCE makes a stolen code worthless.",
          "The analogy that works: you hand the cloakroom a padlocked box (the challenge) when you check your coat, and the key (the verifier) when you collect it. Somebody who steals the ticket still cannot open the box.",
          "Labour the 'what it does NOT do' card. This is where teams over-claim. PKCE is about the code, not the token.",
          "Inji uses S256 only — plain is not offered, which is correct."],
      caveats=["PKCE is mandatory for public clients in OAuth 2.1 and in OpenID4VCI practice. Do not let an authorization server vendor tell you it is optional.",
               "If the authorization server does not advertise code_challenge_methods_supported, test it explicitly — silent ignoring of the challenge is a real and dangerous vendor bug."],
      questions=["Do we still need a client secret? — No, and a mobile app cannot keep one anyway.",
                 "Does Inji Web use PKCE? — Its issuance path runs through Mimoto, which is a confidential client; the trade-offs differ."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- DPoP
s, y = slide("DPoP — making a stolen token useless", kicker="RFC 9449",
             sub="Demonstrating Proof-of-Possession. It protects the access token, which is exactly what PKCE does not.")
codebox(s, ML, y, 6.35, 2.55, [
 'POST /credential',
 'Authorization: DPoP eyJhbGciOi…            // note: not "Bearer"',
 'DPoP: eyJ0eXAiOiJkcG9wK2p3dCIsImFsZyI6IkVTMjU2IiwiandrIjp7…',
 '',
 '// decoded DPoP proof header',
 '{ "typ": "dpop+jwt", "alg": "ES256", "jwk": { public key } }',
 '// decoded DPoP proof payload',
 '{ "jti": "e1j3V_bK", "htm": "POST",',
 '  "htu": "https://issuer.example/credential",',
 '  "iat": 1770000000,',
 '  "ath": "fUHyO2r2Z3DZ53EsNrWBb0xWXoaNy59IiKCAqksmQEo",',
 '  "nonce": "eyJ7S_zG…" }',
], label="A DPoP-BOUND REQUEST", size=8.8, hl=[1, 2, 10])
rows = [
 ["`jwk`", "Header", "The public key. Its thumbprint is the token's binding identity."],
 ["`jkt`", "In the token", "SHA-256 thumbprint of that JWK, placed in the access token's `cnf` claim by the AS."],
 ["`htm` / `htu`", "Payload", "HTTP method and URL this proof is valid for. Stops a proof being reused on another endpoint."],
 ["`ath`", "Payload", "Hash of the access token. Ties this proof to that exact token."],
 ["`jti` + `iat`", "Payload", "One-time id and timestamp. The server keeps a short replay cache."],
 ["`nonce`", "Payload", "Server-supplied freshness value, when the server demands one."],
]
table(s, ML + 6.60, y, 5.68, ["Field", "Where", "What it is for"], rows,
      col_w=[1.3, 1.1, 3.6], fsize=9.0, row_h=0.52, head_h=0.32)
yy = y + 2.80
callout(s, ML, yy, 6.35, "**Inji today uses Bearer access tokens.** DPoP is not implemented in `inji-vci-client`, `inji-openid4vp` or Mimoto in the versions reviewed for this workshop. Treat DPoP as a design option to raise, not a feature to assume.", kind='bad', size=10.3)
notes(s, ["Be scrupulously honest on this slide. DPoP is in the spec ecosystem and it is the right direction, but it is not in the Inji code today. Saying otherwise will cost you credibility the first time somebody greps the repo.",
          "Explain the mechanism simply: with a bearer token, possession is authorisation — steal the string, use the token. With DPoP, the token carries a fingerprint (jkt) of a key, and every request must be accompanied by a fresh signature from that key. Stealing the token alone gets you nothing.",
          "ath is the subtle one. Without it, a DPoP proof captured on one request could be paired with a different stolen token. ath nails the proof to one specific token.",
          "For Brazil: if the threat model includes token theft at the network layer or a compromised intermediary, DPoP is the mitigation to ask for upstream. Log it as a requirement, not an assumption."],
      caveats=["Do not confuse the DPoP proof with the OpenID4VCI credential request proof. Same word, completely different job. Next slide fixes this.",
               "DPoP requires support on BOTH the authorization server and the resource server (the credential endpoint). Half a deployment is worse than none."],
      questions=["Can we add DPoP ourselves? — It is a library change in inji-vci-client plus AS and issuer support. Raise it with the Inji community rather than forking.",
                 "Is mTLS an alternative? — Yes, RFC 8705 certificate-bound tokens achieve the same goal; heavier to operate on mobile."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- PKCE vs DPoP
s, y = slide("PKCE is not DPoP, and neither is the credential proof", kicker="The distinction that matters",
             sub="Three mechanisms, three different things being protected. Keep this table.")
rows = [
 ["**What is protected**", "The authorization **code**", "The access **token**", "The **credential** being issued"],
 ["**Specification**", "RFC 7636", "RFC 9449", "OpenID4VCI"],
 ["**Who verifies it**", "Authorization server, at `/token`", "Any server that accepts the token", "The credential issuer, at `/credential`"],
 ["**Key involved**", "None — a hash of a random string", "A key pair held by the client", "The key the credential will be **bound to**"],
 ["**When it is sent**", "Challenge at `/authorize`, verifier at `/token`", "A fresh proof on **every** protected request", "Once, inside the credential request body"],
 ["**Freshness source**", "The code is single-use", "`jti`, `iat`, optional server `nonce`", "`c_nonce` from the token response"],
 ["**If it is missing**", "A stolen code becomes a token", "A stolen token can be replayed anywhere", "The credential cannot be bound to a device key"],
 ["**In Inji today**", "++Implemented in `inji-vci-client`", "!!Not implemented", "++Implemented — `getProofJwt` callback"],
]
_tb_bottom = table(s, ML, y, CW, ["", "PKCE", "DPoP", "Credential request proof"], rows,
      col_w=[2.5, 3.2, 3.3, 3.3], fsize=9.4, row_h=0.54, head_h=0.38)
yy = _tb_bottom + 0.18
callout(s, ML, yy, CW, "One sentence to remember: **PKCE protects the hand-off, DPoP protects the ticket, the credential proof protects the binding.** They are complements, never substitutes.", kind='tip', size=11)
notes(s, ["Put this on screen and stop talking for twenty seconds. Let people read it.",
          "Then take questions. This is the slide where the room's misconceptions surface, and it is much cheaper to fix them here than in section 12.",
          "Note the bottom row is a status row, not a specification row. It will change as Inji evolves — date it when you present.",
          "If someone argues 'we have PKCE so we do not need DPoP', use row 1: different asset, different attack."],
      caveats=["The 'credential request proof' column is specifically the proof in the credential request body. The word 'proof' also appears in ldp_vc credentials (the linked-data proof) and in VP tokens. Three more uses of the same word. Context is everything."],
      minutes="5 min")
footer(s)

# ------------------------------------------------- proof vs binding
s, y = slide("Proof type, binding method, holder binding, key binding", kicker="Four words, four meanings",
             sub="These get used interchangeably in meetings. They are not interchangeable. Fix the vocabulary now.")
defs = [
 ("Proof type", "How the **credential request** proves possession of a key.",
  "`proof_type: \"jwt\"` — a signed JWT with typ `openid4vci-proof+jwt`. CWT proof exists in the spec; Inji Certify does not support it.",
  "Lives in: the credential request, at issuance time.", C['primary']),
 ("Cryptographic binding method", "How the issuer **identifies** the key inside the issued credential.",
  "`did:jwk`, `did:key`, a raw `jwk`, or an X.509 reference. Announced in metadata as `cryptographic_binding_methods_supported`.",
  "Lives in: issuer metadata, and the issued credential.", C['violet']),
 ("Holder binding", "The credential names **who** holds it, and the holder can prove it at presentation.",
  "SD-JWT VC: the `cnf` claim. ldp_vc: `credentialSubject.id` matched against the VP `holder`. mDoc: the device key in the MSO.",
  "Lives in: the credential, checked by the verifier.", C['accent']),
 ("Key binding", "The specific act of **signing at presentation time** with the bound key.",
  "SD-JWT VC: the KB-JWT appended after the disclosures. mDoc: `DeviceSignature` / device authentication. ldp_vc: the VP proof.",
  "Lives in: the presentation, produced on demand.", C['green']),
]
bw = (CW - 3 * 0.20) / 4
for i, (t, one, detail, where, col) in enumerate(defs):
    x = ML + i * (bw + 0.20)
    rect(s, x, y, bw, 3.30, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.045)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.24, bw - 0.40, 0.55)
    para(t2, t, size=12.5, color=col, bold=True, first=True, line_spacing=1.05)
    _, t3 = tb(s, x + 0.20, y + 0.90, bw - 0.40, 0.7)
    parts = re.split(r'(\*\*[^*]+\*\*)', one)
    rich(t3, [((pt[2:-2], C['ink'], True) if pt.startswith('**') else (pt, C['ink2'], False))
              for pt in parts if pt], size=10.2, first=True, line_spacing=1.25)
    line(s, x + 0.20, y + 1.72, x + bw - 0.20, y + 1.72, C['line'], 1.0)
    _, t4 = tb(s, x + 0.20, y + 1.82, bw - 0.40, 1.0)
    parts = re.split(r'(`[^`]+`)', detail)
    rich(t4, [((pt[1:-1], C['primary'], False, False, F_MONO) if pt.startswith('`') else (pt, C['muted'], False))
              for pt in parts if pt], size=9.3, first=True, line_spacing=1.28)
    _, t5 = tb(s, x + 0.20, y + 2.86, bw - 0.40, 0.4)
    para(t5, where, size=9, color=col, bold=True, first=True, line_spacing=1.2)
yy = y + 3.55
callout(s, ML, yy, CW, "The trap: **proof type is about the request, binding method is about the identifier, holder binding is about the credential, key binding is about the presentation.** A team that says 'we support holder binding' has told you almost nothing until you ask which of these four they mean.", kind='warn', size=10.5)
notes(s, ["Slow, deliberate delivery. Read each card, then give one concrete example that walks across all four.",
          "The walk-through example: at issuance the wallet sends a JWT proof (proof type). The issuer puts a did:jwk identifier into the credential (binding method). The credential therefore names a holder key (holder binding). At presentation the wallet signs a KB-JWT with that key (key binding). One key, four vocabulary slots.",
          "Ask the room to say which one a verifier checks. Answer: holder binding, by validating the key binding artefact. The verifier never sees the issuance proof.",
          "This slide is the antidote to a very common architecture mistake: assuming that because issuance used a proof, presentations are automatically bound. They are not — the credential must carry the binding, and the format must support it."],
      caveats=["Inji Wallet supports holder binding for SD-JWT VC only via a cnf claim containing a kid, with ES256 and EdDSA. For ldp_vc it is supported for Ed25519Signature2020. Those are real constraints — check them against Brazil's format choice.",
               "An SD-JWT VC without a cnf claim gets no KB-JWT. inji-openid4vp skips it rather than failing — so an unbound credential presents successfully with weaker guarantees. Verifiers must check for themselves."],
      questions=["Can one credential be bound to two devices? — Not with a single cnf key. You would issue twice, once per device key."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- proof jwt + attestation
s, y = slide("The proof JWT, and where key attestation fits", kicker="Anatomy",
             sub="What the wallet actually signs at issuance — and why a strong attestation does not remove the need for it.")
codebox(s, ML, y, 6.10, 2.55, [
 '// header',
 '{ "typ": "openid4vci-proof+jwt",',
 '  "alg": "ES256",',
 '  "jwk": { "kty":"EC", "crv":"P-256", "x":"…", "y":"…" } }',
 '',
 '// payload',
 '{ "iss":  "inji-wallet",            // the client_id',
 '  "aud":  "https://certify.example.gov.br",',
 '  "iat":  1770000000,',
 '  "nonce": "tZignsnFbp"             // the c_nonce',
 '}',
 '',
 '// signature made by the private key in the device keystore',
], label="CREDENTIAL REQUEST PROOF JWT", size=8.8, hl=[1, 3, 9])
bullets(s, ML + 6.42, y, 5.81, [
 "`jwk` (or `kid`) is the public key the credential will be bound to. The issuer copies it into the credential.",
 "`aud` must be the credential issuer. This stops a proof harvested by one issuer being replayed at another.",
 "`nonce` is the `c_nonce` from the token response — the freshness tie.",
 "The private key never leaves the keystore. `inji-vci-client` asks for a signature through `getProofJwt`; it never sees key material.",
 "The algorithm must be one of `proof_signing_alg_values_supported` from the issuer metadata. Inji supports `RS256`, `ES256`, `ES256K`, `Ed25519`.",
], size=10.4)
yy = y + 2.85
card(s, ML, yy, 6.10, 2.25, "Key attestation — what it adds", [
 "A statement from the **platform** (Android Key Attestation, Play Integrity, iOS App Attest) that a key was generated inside real hardware on a genuine device.",
 "It answers: *is this key protected?* and *is this a real app on a real device?*",
 "Mimoto exposes endpoints for attestation verification (`/safetynet/online/verify`, `/safetynet/offline/verify`).",
], accent=C['green'], tint=C['green_l'], size=10.2)
card(s, ML + 6.42, yy, 5.81, 2.25, "Why it does not replace the proof", [
 "Attestation says *a key exists and is well protected*. The credential request proof says *I control this key, right now, for this issuer, with this nonce*.",
 "Attestation has no `aud` and no `c_nonce` binding to this issuance.",
 "OpenID4VCI requires the proof when the issuer asks for one. Attestation is an **additional** signal the issuer may demand on top.",
], accent=C['amber'], tint=C['amber_l'], size=10.2)
notes(s, ["Decode a real proof JWT live if you can — jwt.io on a test token makes this concrete in fifteen seconds.",
          "The aud field is the security-critical one people skip. Without it, an issuer you do not trust can collect proofs and replay them at an issuer you do trust.",
          "Key attestation: explain the difference in one line — attestation is about the key's container, the proof is about this transaction. A bank vault certificate does not prove you are making a withdrawal today.",
          "Brazil angle: if the trust framework requires hardware-backed keys, attestation is how you enforce it. That is an issuer-side policy decision, and it constrains which devices can hold credentials — which is a real inclusion trade-off."],
      caveats=["Ed25519 and secp256k1 keys are NOT supported by Android's hardware keystore. Inji stores those in EncryptedSharedPreferences wrapped by a hardware key instead, and signs in software. If you require hardware attestation, you are effectively restricted to RSA-2048 and EC P-256.",
               "Play Integrity replaced SafetyNet; the Mimoto endpoint names still say safetynet. Do not read the endpoint name as a statement about which API is in use."],
      questions=["Does the issuer have to check attestation? — Only if its policy says so; the protocol does not require it.",
                 "What about iOS? — App Attest and Secure Enclave give an equivalent signal with a different API surface."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- bound vs unbound + exercise
s, y = slide("Bound and unbound credentials — and an exercise", kicker="Consequences",
             sub="Whether a credential is bound to a key changes what a verifier can conclude from it.")
rows = [
 ["Contains a holder key reference", "++Yes — `cnf`, device key, or subject id", "!!No"],
 ["Wallet signs at presentation", "++Yes — KB-JWT / DeviceSignature / VP proof", "!!No signature from the holder"],
 ["A copied credential is useful to a thief", "++No — they lack the private key", "!!Yes — it is a bearer document"],
 ["Verifier can prove 'presenter == holder'", "++Yes", "!!No — only 'this is a valid credential'"],
 ["Works for anonymous / low-assurance use", "Overkill", "Fine — e.g. a public transport concession"],
 ["Cost", "Key management, hardware constraints, device loss handling", "Almost none"],
]
table(s, ML, y, 7.30, ["Property", "Bound credential", "Unbound credential"], rows,
      col_w=[3.0, 2.4, 1.9], fsize=9.4, row_h=0.50, head_h=0.34)
card(s, ML + 7.62, y, 4.61, 3.34, "Exercise 3 — inspect a proof", [
 "Take the proof JWT from a real issuance (logs or a proxy).",
 "Decode it. Find `typ`, `alg`, `jwk`, `aud`, `nonce`.",
 "Answer: which issuer is this proof valid for, and which single issuance?",
 "Now change `aud` to another issuer and replay it. What should happen, and what actually happens?",
 "Write down which component rejected it — that is the skill we are building.",
], accent=C['violet'], tint=C['violet_l'], size=10.2)
yy = y + 3.60
callout(s, ML, yy, CW, "Brazil decision point: **which credential types must be bound?** A tax identity almost certainly. A library card almost certainly not. Binding everything costs device-management complexity you may not need; binding nothing makes credentials transferable.", kind='spec', size=10.6)
notes(s, ["Run the exercise as a real five-minute activity if the room has laptops and access to logs. If not, do it as a thought exercise out loud.",
          "The last row of the table is the one architects care about: binding is not free. It brings key lifecycle, device loss, device change, and re-issuance flows with it. Ask the room what happens today when a citizen changes phone.",
          "Push the room to answer the Brazil question with examples from their own programme. Do not answer it for them."],
      caveats=["Unbound does not mean insecure — it means the credential is a bearer artefact. For low-assurance use that can be the right choice.",
               "A bound credential that the verifier does not check the binding on is effectively unbound. Binding requires both sides."],
      minutes="6 min")
footer(s)

# =================================================================== SECTION 5
section("Credential formats", "30 min",
        "The single most consequential architecture decision Brazil will make. It changes the data model, the verification code, what can be selectively disclosed, and how keys are resolved.",
        ["The format landscape",
         "SD-JWT VC end to end",
         "Disclosures, digests, _sd_alg, cnf",
         "Issuer key resolution for SD-JWT",
         "mDoc: MSO, namespaces, device auth",
         "A decision matrix for Brazil"], highlight=('issuer', 'store'), num="5")
notes(prs.slides[-1], ["Open by saying this bluntly: of everything today, format choice is the decision that is hardest to reverse.",
                       "Encourage the room to take notes against their own use cases as you go."],
      minutes="30 min for the section")

# ------------------------------------------------- format landscape
s, y = slide("Four formats, and what each one costs you", kicker="Landscape",
             sub="Inji Wallet can download and present all four. That does not mean all four are equally good for a national programme.")
rows = [
 ["**Data model**", "JSON-LD graph, `@context` driven", "Plain JSON claims + `vct` type", "CBOR, ISO namespaces", "JSON claims in a JWT"],
 ["**Signature**", "Linked Data Proof (Ed25519Signature2020, RSA…)", "Compact JWS over the issuer-signed JWT", "COSE_Sign1 over the MSO", "JWS"],
 ["**Selective disclosure**", "!!None natively", "++Native — per-claim disclosures", "++Native — per-element in namespaces", "!!None natively"],
 ["**Holder binding**", "`credentialSubject.id` + VP proof", "`cnf` claim + KB-JWT", "Device key in the MSO + `DeviceSignature`", "`cnf` claim"],
 ["**Issuer key resolution**", "`did:web`, `did:key`, `did:jwk`, HTTPS", "~~Today in Inji: X.509 (`x5c`)", "IACA / document signer certificate chain", "Embedded JWK, `jku`, `kid`, DID"],
 ["**Size**", "Large — context processing needed", "Compact", "Compact (binary)", "Compact"],
 ["**Offline friendliness**", "Context fetching is a hazard", "Good", "Excellent — built for proximity", "Good"],
 ["**Inji Wallet support**", "Download + present", "Download + present", "Download + present", "Verify only"],
 ["**Inji Web support**", "Download + present", "Download; ~~present not yet", "Not yet", "—"],
 ["**Inji Certify issues it**", "++Yes", "++Yes (`vc+sd-jwt`)", "!!No", "—"],
]
table(s, ML, y, CW, ["", "W3C VC  `ldp_vc`", "SD-JWT VC  `vc+sd-jwt` / `dc+sd-jwt`", "mDoc  `mso_mdoc`", "JWT VC  `jwt_vc_json`"], rows,
      col_w=[2.4, 2.6, 3.0, 2.4, 1.9], fsize=8.9, hsize=9.0, row_h=0.425, head_h=0.46)
notes(s, ["Do not read the table. Pick four cells and talk about them.",
          "Row 3 is the headline. If selective disclosure matters — and for a national identity credential it almost always does — ldp_vc and plain JWT VC are off the table without extra machinery.",
          "Row 5 is the honest caveat that teams discover late: Inji's vc-verifier currently resolves SD-JWT VC issuer keys from an X.509 certificate in the header, and JWT VC Issuer Metadata (the /.well-known/jwt-vc-issuer document) is not yet supported. If Brazil's issuer plans to publish keys that way, that is a gap to plan around or contribute upstream.",
          "Row 10 matters for sequencing: Inji Certify does not issue mDoc today. If Brazil wants mDL, the issuer side is not the reference implementation.",
          "Note vc+sd-jwt versus dc+sd-jwt: the media type was renamed as the IETF draft progressed. Inji supports both strings. Agree which one with every partner, in writing."],
      caveats=["Support matrices move. Re-check against the release you will deploy, not against this slide.",
               "'Download + present' for mDoc in the wallet does not mean end-to-end mDL: ISO 18013-5 proximity has its own transport requirements beyond OpenID4VP."],
      questions=["Can one wallet hold several formats at once? — Yes, and it will. The store is format-tagged.",
                 "Which format do most European programmes use? — The EUDI reference is SD-JWT VC and mDoc; plan for both."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- SD-JWT anatomy
s, y = slide("SD-JWT VC, taken apart", kicker="Format deep dive",
             sub="One string, separated by tildes. Everything about selective disclosure follows from this structure.")
seg = [("Issuer-signed JWT", C['primary'], 4.1), ("~", C['muted'], 0.28),
       ("Disclosure 1", C['accent'], 2.1), ("~", C['muted'], 0.28),
       ("Disclosure 2", C['accent'], 2.1), ("~", C['muted'], 0.28),
       ("KB-JWT", C['green'], 2.2)]
xx = ML
for t, col, wd in seg:
    sh = rect(s, xx, y, wd, 0.54, fill=col if t != "~" else C['white'],
              shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.12)
    tf = sh.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t
    r.font.size = Pt(11 if t != "~" else 14); r.font.bold = True; r.font.name = F_SANS
    r.font.color.rgb = C['white'] if t != "~" else C['muted']
    xx += wd + 0.10
_, tf = tb(s, ML, y + 0.60, 4.1, 0.3)
para(tf, "signed by the ISSUER", size=8.5, color=C['primary'], bold=True, align=PP_ALIGN.CENTER, first=True)
_, tf = tb(s, ML + 4.48, y + 0.60, 4.86, 0.3)
para(tf, "plain salted values — the wallet chooses which to send", size=8.5, color=C['accent'],
     bold=True, align=PP_ALIGN.CENTER, first=True)
_, tf = tb(s, ML + 9.72, y + 0.60, 2.5, 0.3)
para(tf, "signed by the HOLDER", size=8.5, color=C['green'], bold=True, align=PP_ALIGN.CENTER, first=True)
yy = y + 1.05
codebox(s, ML, yy, 6.10, 2.85, [
 '// issuer-signed JWT payload',
 '{ "iss": "https://certify.example.gov.br",',
 '  "vct": "CPFCredential",',
 '  "iat": 1770000000, "exp": 1801536000,',
 '  "_sd_alg": "sha-256",',
 '  "_sd": [ "9gjVuXtM…", "Tk5rX2ZN…", "aB3kQp1y…" ],',
 '  "cnf": { "jwk": { "kty":"EC", "crv":"P-256", … } }',
 '}',
 '',
 '// one disclosure, base64url of a 3-element array',
 '["_26bc4LT-ac6q2KI6cBW5es", "nome", "Ana Silva"]',
 '//  ^ salt                    ^ claim   ^ value',
 '//  SHA-256(disclosure) must equal one entry in _sd',
], label="WHAT IS INSIDE", size=8.7, hl=[4, 5, 6, 12])
bullets(s, ML + 6.42, yy, 5.81, [
 "The issuer replaces each selectively-disclosable claim with a **digest** in `_sd`, and hands the wallet the matching disclosures.",
 "`_sd_alg` names the hash. Inji supports `sha-256`, `sha-384`, `sha-512`; a mismatch throws.",
 "To disclose a claim, the wallet **includes its disclosure**. To hide it, it simply omits it — the digest stays, the value is unrecoverable.",
 "`cnf` carries the holder key. Inji's OpenID4VP library supports `cnf` with a `kid` in `did:jwk` form, using `ES256` or `EdDSA`.",
 "The **KB-JWT** is added only at presentation. It signs over `sd_hash` (a hash of everything being presented), the verifier's `nonce` and `aud`.",
 "No `cnf` means no KB-JWT: `inji-openid4vp` skips signing and presents it unbound.",
], size=10.2)
notes(s, ["Draw the tildes on the whiteboard. It is genuinely this simple, and simplicity is the format's main virtue.",
          "The insight people need: the issuer signs the DIGESTS, not the values. So the wallet can drop any disclosure it likes and the issuer signature still verifies. Selective disclosure with no re-signing and no issuer involvement at presentation time.",
          "The salt matters: without a per-claim random salt, a verifier could brute-force a low-entropy claim like a birth year from its digest. Never let an issuer skip salts.",
          "sd_hash inside the KB-JWT binds the key-binding signature to exactly the set of disclosures being sent. Without it, a middleman could strip disclosures after the holder signed.",
          "Point out the last bullet as a real behaviour to design around: an SD-JWT VC without cnf presents fine but proves nothing about who presented it."],
      caveats=["Unsupported or mismatched _sd_alg raises an exception in inji-openid4vp. Test your issuer's choice against the wallet before go-live.",
               "Nested and array disclosures exist in the spec and add complexity. Keep the first Brazilian credential flat if you can.",
               "Disclosures are plaintext to anyone who gets the full credential — the protection is against the VERIFIER seeing undisclosed claims, not against device compromise."],
      questions=["Can the verifier ask for a claim that is not disclosable? — Only if the issuer left it outside _sd, in which case it is always visible.",
                 "Does hiding a claim change the credential's signature? — No, and that is the whole trick."],
      minutes="9 min")
footer(s)

# ------------------------------------------------- SD-JWT key resolution
s, y = slide("SD-JWT VC: how the verifier finds the issuer's key", kicker="Key resolution",
             sub="A correct credential with an unresolvable key is a failed verification. This is where a lot of integration time goes.")
paths = [
 ("x5c  — X.509 chain in the header", "The issuer embeds its certificate chain in the JWS header. The verifier validates the chain to a trusted root.",
  "This is what Inji's `vc-verifier` uses for `vc+sd-jwt` and `dc+sd-jwt` today.", C['green'], True),
 ("/.well-known/jwt-vc-issuer", "Take `iss`, insert the well-known path, fetch the JWT VC Issuer Metadata, follow `jwks` or `jwks_uri`, select by `kid`.",
  "Defined by the SD-JWT VC draft. **Not supported by Inji's vc-verifier at the time of writing.**", C['amber'], False),
 ("DID-based", "`iss` is a DID. Resolve the DID document, find the verification method named by `kid`, take the public key.",
  "`vc-verifier` resolves `did:web`, `did:key`, `did:jwk` — used heavily for `ldp_vc`.", C['primary'], True),
]
for i, (t, how, status, col, ok) in enumerate(paths):
    yy = y + i * 1.13
    rect(s, ML, yy, 7.35, 1.02, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
    rect(s, ML, yy, 0.055, 1.02, fill=col)
    _, t2 = tb(s, ML + 0.22, yy + 0.12, 7.0, 0.28)
    para(t2, t, size=11.5, color=col, bold=True, first=True)
    _, t3 = tb(s, ML + 0.22, yy + 0.42, 7.0, 0.55)
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', how + "  " + status)
    ch = []
    for pt in parts:
        if not pt:
            continue
        if pt.startswith('`'):
            ch.append((pt[1:-1], C['primary'], False, False, F_MONO))
        elif pt.startswith('**'):
            ch.append((pt[2:-2], C['red'], True))
        else:
            ch.append((pt, C['muted'], False))
    rich(t3, ch, size=9.4, first=True, line_spacing=1.24)
codebox(s, ML + 7.66, y, 4.57, 2.25, [
 '// JWS header — pick ONE resolution path',
 '{ "alg": "ES256",',
 '  "typ": "vc+sd-jwt",',
 '  "kid": "did:web:gov.br#key-1",',
 '  "x5c": [ "MIIC…", "MIIB…" ] }',
 '',
 '// and iss in the payload',
 '"iss": "https://certify.example.gov.br"',
], label="WHERE THE HINTS LIVE", size=8.6)
callout(s, ML + 7.66, y + 2.45, 4.57, "Rule of thumb: **`kid` selects, `iss` locates.** `kid` says which key; `iss` (or `x5c`) says where to get it.", kind='tip', size=10.0)
yy = y + 3.55
rows = [
 ["`kid` missing", "Verifier cannot choose among several keys", "Always set `kid`, even with one key"],
 ["`kid` does not match any published key", "Verification fails after a successful fetch", "Publish old keys during rotation; overlap by at least one credential lifetime"],
 ["JWKS unreachable or behind a redirect", "Intermittent failures; hard to reproduce", "No redirects on key endpoints; monitor them like a production API"],
 ["`alg` in header not accepted by the verifier", "Rejected before any network call", "Agree the algorithm set in the interface contract"],
]
table(s, ML, yy, CW, ["Failure", "What you see", "What to do"], rows,
      col_w=[3.2, 4.2, 4.8], fsize=9.3, row_h=0.42, head_h=0.32)
notes(s, ["Be explicit and honest about the middle row: the well-known jwt-vc-issuer path is the direction the SD-JWT VC spec points, and Inji's verifier does not implement it yet. Brazil needs to know that before designing its key publication strategy.",
          "The practical consequence: if Brazil issues SD-JWT VC today and expects Inji Wallet to verify it, the issuer must put an X.509 chain in the header and the wallet must trust the root. That is a PKI decision, not just a code decision.",
          "The 'kid selects, iss locates' line is worth writing on the whiteboard.",
          "The failure table is a preview of section 12 — tell people it will come back."],
      caveats=["Key rotation is the failure nobody plans for. A credential signed in March must still verify in December, so the March key has to stay published. Overlap windows are a policy decision with a hard technical deadline.",
               "Certificate chain validation for document signers in mDoc is a related but separate problem — see the mDoc slide."],
      questions=["Can we use both x5c and a well-known document? — Yes, and publishing both maximises interoperability with wallets other than Inji."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- mDoc
s, y = slide("mDoc / mso_mdoc, taken apart", kicker="Format deep dive",
             sub="ISO/IEC 18013-5. A binary, CBOR-based format designed for a driving licence held up at a roadside.")
codebox(s, ML, y, 6.10, 3.10, [
 'IssuerSigned = {',
 '  "nameSpaces": {',
 '    "org.iso.18013.5.1": [',
 '      IssuerSignedItem(digestID: 1, random: h\'A3…\',',
 '        elementIdentifier: "family_name",',
 '        elementValue: "Silva"),',
 '      IssuerSignedItem(digestID: 2, …, "birth_date", …)',
 '    ]',
 '  },',
 '  "issuerAuth": COSE_Sign1(                 // issuer signature',
 '     payload: MobileSecurityObject {',
 '       digestAlgorithm: "SHA-256",',
 '       valueDigests: { "org.iso.18013.5.1": {1: h\'…\', 2: h\'…\'} },',
 '       deviceKeyInfo: { deviceKey: COSE_Key },   // holder binding',
 '       docType: "org.iso.18013.5.1.mDL",',
 '       validityInfo: { signed, validFrom, validUntil } })',
 '}',
], label="STRUCTURE (CBOR, SHOWN AS DIAGNOSTIC NOTATION)", size=8.5, hl=[9, 13])
bullets(s, ML + 6.42, y, 5.81, [
 "**Namespaces** group elements. `org.iso.18013.5.1` is the ISO mDL namespace; countries add their own, e.g. `org.iso.18013.5.1.BR`.",
 "**Issuer authentication**: `issuerAuth` is a COSE_Sign1 over the Mobile Security Object. The MSO holds a **digest per element**, so selective disclosure works the same way as SD-JWT — send the element, the verifier re-hashes it.",
 "**Device authentication**: `deviceKeyInfo.deviceKey` inside the MSO is the holder's public key. At presentation the device produces a `DeviceSignature` (or a MAC) over the session transcript.",
 "**Two signatures, two purposes**: issuerAuth proves the data; DeviceSignature proves who is presenting it.",
 "The document signer's certificate chains to a country IACA root. That PKI is the trust anchor — there is no DID and no JWKS.",
], size=10.1)
yy = y + 3.35
rows = [
 ["**Online (OpenID4VP)**", "mDoc inside a `vp_token`", "Must use `response_mode=direct_post.jwt` — ISO 18013-7 requires the response to be encrypted", "Inji: supported by `inji-openid4vp`"],
 ["**Proximity (18013-5)**", "NFC/BLE device retrieval, session encryption, session transcript", "A different transport and a different security model entirely", "Inji has BLE sharing via `tuvali`, which is not ISO device retrieval"],
]
table(s, ML, yy, CW, ["Mode", "How the mDoc travels", "What it demands", "Inji position"], rows,
      col_w=[2.0, 2.8, 4.6, 2.8], fsize=9.3, row_h=0.62, head_h=0.34)
notes(s, ["Start with the shape: mDoc is CBOR, so you cannot eyeball it. Have a CBOR decoder ready — that alone changes how a team debugs mDoc.",
          "The conceptual parallel with SD-JWT VC is worth drawing explicitly: both put per-claim digests under one issuer signature, and both let the holder omit values. The difference is encoding, key resolution, and the extra device authentication step.",
          "Device authentication is stronger than SD-JWT key binding in one respect: it signs over a session transcript that includes the reader's identity and the session keys, which makes relay attacks much harder in proximity mode.",
          "The bottom table matters for planning. If Brazil wants mDL online, direct_post.jwt with response encryption is not optional — ISO 18013-7 requires it, and inji-openid4vp enforces it.",
          "Say plainly: Inji Certify does not issue mDoc today, and tuvali is not ISO device retrieval. If proximity mDL is a Brazilian requirement, that is a gap with real cost."],
      caveats=["vc-verifier validates the mDoc signature, issuing country, doc type and validity window. Document signer certificate chain validation was not implemented at the time of writing — verify the current state before relying on it.",
               "PixelPass is used to turn the base64url CBOR into JSON for rendering only. That decoded JSON is kept in memory, never persisted."],
      questions=["Can we mix an mDoc and an SD-JWT VC in one presentation? — The protocol allows multiple credentials in a vp_token; test it, do not assume it.",
                 "Do we need our own IACA? — If Brazil issues mDLs, yes, and that is a national PKI programme in its own right."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- format decision
s, y = slide("Choosing a format: what actually changes", kicker="Decision matrix",
             sub="Ask these questions in order. The answers narrow the choice faster than a feature comparison does.")
qs = [
 ("1. Must the holder be able to hide claims?", "Yes → SD-JWT VC or mDoc. No → any format works.",
  "A CPF credential shown to a bar to prove age should not reveal the CPF number.", C['primary']),
 ("2. Is proximity / offline presentation in scope?", "Yes → mDoc, and plan for the 18013-5 transport stack.",
  "Roadside checks, transport gates, border control.", C['accent']),
 ("3. Who will verify it, and with what software?", "European or ISO-aligned verifiers → SD-JWT VC and mDoc. MOSIP-ecosystem verifiers → ldp_vc is well trodden.",
  "Interoperability is a property of the ecosystem, not of the format.", C['violet']),
 ("4. How will issuer keys be published?", "X.509 chain → works with Inji today for SD-JWT. DID or JWKS → best trodden path is ldp_vc.",
  "This is a PKI decision with a long lead time.", C['amber']),
 ("5. Is the issuer already built?", "Inji Certify issues ldp_vc and `vc+sd-jwt`, not mDoc. A custom issuer can do anything.",
  "Do not let the format choice silently create a new issuer programme.", C['green']),
 ("6. What is the credential's assurance level?", "High → bound, selectively disclosable, hardware-backed key. Low → unbound is fine.",
  "Not every credential deserves the same machinery.", C['red']),
]
for i, (q, a, ex, col) in enumerate(qs):
    x = ML + (i % 2) * (CW / 2 + 0.10)
    yy = y + (i // 2) * 1.52
    wid = CW / 2 - 0.10
    rect(s, x, yy, wid, 1.36, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
    rect(s, x, yy, 0.055, 1.36, fill=col)
    _, t2 = tb(s, x + 0.22, yy + 0.12, wid - 0.42, 0.28)
    para(t2, q, size=11.2, color=C['ink'], bold=True, first=True)
    _, t3 = tb(s, x + 0.22, yy + 0.44, wid - 0.42, 0.56)
    parts = re.split(r'(`[^`]+`)', a)
    rich(t3, [((pt[1:-1], C['primary'], False, False, F_MONO) if pt.startswith('`') else (pt, col, True))
              for pt in parts if pt], size=9.8, first=True, line_spacing=1.24)
    _, t4 = tb(s, x + 0.22, yy + 1.00, wid - 0.42, 0.32)
    para(t4, ex, size=9.0, color=C['muted'], italic=True, first=True, line_spacing=1.2)
notes(s, ["Turn this into a live conversation. Ask the room each question and write the answers on a flipchart — those answers feed straight into section 18.",
          "Question 3 is the one teams underrate. A format is only useful if the verifiers you need can read it. Survey the intended verifier population before choosing.",
          "Question 5 is a scheduling point: choosing mDoc today means building or buying an mDoc issuer, because Inji Certify does not issue it.",
          "Question 6 gives permission to use different formats for different credentials. That is normal and healthy, as long as the wallet and the verifiers can handle the set."],
      caveats=["Do not let 'we might need it one day' drive the choice. Every format you support is verification code, test surface and support burden in every verifier.",
               "Supporting two formats is a reasonable strategy; supporting four is usually a symptom of an unmade decision."],
      minutes="5 min")
footer(s)

# ------------------------------------------------- demo 3
demo_slide(4, "Selective disclosure with SD-JWT VC", "6 minutes",
  ["An SD-JWT VC in the wallet with at least four disclosable claims.",
   "A verifier request that asks for **one** of them.",
   "A JWT decoder and a base64url decoder to hand.",
   "Ideally: a proxy so the room can see the `vp_token` that leaves the phone."],
  ["The wallet shows the credential with every claim visible to the user.",
   "The verifier asks for one claim.",
   "The consent screen names that one claim.",
   "The verifier receives it — and nothing else."],
  ["The wallet sent the issuer-signed JWT plus **only the matching disclosure**.",
   "The other digests are still in `_sd`, but their values were never transmitted.",
   "A KB-JWT was appended, signed with the key in `cnf`, covering `sd_hash`, `nonce` and `aud`.",
   "The issuer was not contacted at any point."],
  fail="Show the raw `vp_token` and count the tildes. One issuer JWT, one disclosure, one KB-JWT. That count is the proof that selective disclosure worked.")
notes(prs.slides[-1],
      ["This is the demo that sells the architecture to non-technical stakeholders too. Keep it in your pocket for executive audiences.",
       "Counting tildes is the single best teaching trick in this deck. Do it on screen.",
       "Emphasise the last bullet: the issuer was offline for the whole exchange. Privacy by architecture, not by policy."],
      caveats=["If the credential has no cnf claim there will be no KB-JWT and only two tildes. That is a useful failure to show deliberately.",
               "If your verifier logs the full vp_token, redact before screenshotting."],
      minutes="6 min")

# =================================================================== SECTION 6
section("Inji Wallet architecture", "35 min",
        "What the code actually looks like. Layers, state machines, the native bridge, storage, keys, deep links, and the seams where you extend it.",
        ["React Native shell over native libraries",
         "XState machines for issuance and presentation",
         "The native bridge, module by module",
         "Credential store and secure storage",
         "Key generation and platform limits",
         "Deep links, QR, configuration, extension points"], highlight=('wallet', 'store'), num="6")
notes(prs.slides[-1], ["Tell developers this is their section; tell architects to focus on the layering and the extension points slide.",
                       "If the room is architect-heavy, compress the module map and spend the time on the responsibilities and key management slides."],
      minutes="35 min for the section")

# ------------------------------------------------- wallet layers
s, y = slide("Inji Wallet in layers", kicker="Architecture",
             sub="A React Native presentation layer, an XState orchestration layer, and native Kotlin/Swift libraries doing the cryptography.")
layers = [
 ("Screens and components", "`screens/`, `components/`, `routes/`", "React Native + Expo. i18next for language. Theming via app config.", C['accent'], C['accent_l']),
 ("Orchestration — state machines", "`machines/`", "XState. One machine per journey: `VCItemMachine`, `VCMetaMachine`, `openID4VP`, `Issuers`, `bleShare`, `QrLogin`, `backupAndRestore`.", C['violet'], C['violet_l']),
 ("Domain services and adapters", "`shared/`", "`vciClient/`, `openID4VP/`, `vcVerifier/`, `keystore/`, `cryptoutil/`, `storage.ts`, `api.ts`, `telemetry/`.", C['primary'], C['primary_l']),
 ("Native bridge", "`android/app/src/main/java/io/mosip/residentapp/`, `ios/`", "`InjiVciClientModule`, `InjiOpenID4VPModule`, `RNVCVerifierModule`, `RNSecureKeystoreModule`.", C['amber'], C['amber_l']),
 ("Native libraries (versioned artefacts)", "Maven Central / CocoaPods", "`inji-vci-client`, `inji-openid4vp`, `vcverifier`, `pixelpass`, `secure-keystore`, `injivcrenderer`, `tuvali`.", C['green'], C['green_l']),
]
lh = 0.88
for i, (t, where, what, col, tint) in enumerate(layers):
    yy = y + i * (lh + 0.10)
    rect(s, ML, yy, 8.80, lh, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
    rect(s, ML, yy, 0.06, lh, fill=col)
    _, t2 = tb(s, ML + 0.22, yy + 0.11, 3.0, 0.28)
    para(t2, t, size=11.2, color=col, bold=True, first=True)
    _, t3 = tb(s, ML + 0.22, yy + 0.42, 3.0, 0.42)
    parts = re.split(r'(`[^`]+`)', where)
    rich(t3, [((pt[1:-1], C['muted'], False, False, F_MONO) if pt.startswith('`') else (pt, C['muted'], False))
              for pt in parts if pt], size=8.4, first=True, line_spacing=1.18)
    _, t4 = tb(s, ML + 3.35, yy + 0.16, 5.35, 0.66)
    parts = re.split(r'(`[^`]+`)', what)
    rich(t4, [((pt[1:-1], C['primary'], False, False, F_MONO) if pt.startswith('`') else (pt, C['ink2'], False))
              for pt in parts if pt], size=9.3, first=True, line_spacing=1.24)
card(s, 9.22, y, 3.01, 2.60, "Where the seams are", [
    "Anything **above** the bridge is JavaScript you can change quickly.",
    "Anything **below** is a versioned artefact — change it upstream, not by patching.",
    "`patches/` in the repo exists for third-party fixes. Read it before you debug odd behaviour.",
], accent=C['ink'], tint=C['surf'], size=9.5)
card(s, 9.22, y + 2.74, 3.01, 1.81, "The rule", [
    "Protocol logic lives in native libraries **so Android, iOS and Mimoto share one implementation**.",
    "If you find protocol logic in TypeScript, treat it as a smell.",
], accent=C['red'], tint=C['red_l'], size=9.5)
notes(s, ["Work bottom-up. The native libraries are the stable core; everything above is presentation and orchestration.",
          "Explain why XState is there: issuance and presentation are genuinely stateful, long-running, and interruptible (the user backgrounds the app mid-browser-redirect). A state machine makes those transitions explicit and testable. The .typegen.ts files are generated — do not hand-edit them.",
          "The bridge layer is thin on purpose. It converts JS calls into native calls and pushes events back via NativeEventEmitter. Look at shared/vciClient/VciClient.ts to see the pattern: the app registers listeners for onRequestProof, onRequestAuthCode, onRequestTxCode and answers them.",
          "The patches/ directory point saves real time — patch-package is in use, so some third-party behaviour differs from upstream."],
      caveats=["Because protocol logic is native, a protocol bug is usually fixed by bumping a library version and testing, not by editing the app. Plan your release process around that.",
               "iOS uses the Swift equivalents of the same libraries. Do not assume identical APIs — check the Swift package."],
      questions=["Can we reuse the wallet's code in our own app? — The libraries, yes, they are published artefacts. The app is a reference implementation."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- modules table
s, y = slide("The module map", kicker="Repo orientation",
             sub="Where to look first when you are handed a bug report. Paths are from the root of `mosip/inji-wallet`.")
rows = [
 ["`machines/Issuers/`", "Issuer list, selection, the download journey", "Start here for 'credential will not download'"],
 ["`machines/VerifiableCredential/VCItemMachine/`", "One credential: load, render, share, delete", "Rendering and per-credential actions"],
 ["`machines/VerifiableCredential/VCMetaMachine/`", "The collection: what is stored, ordering, metadata", "'My credential disappeared'"],
 ["`machines/openID4VP/`", "Online presentation: request → match → consent → send", "Start here for 'sharing failed'"],
 ["`machines/bleShare/`", "Offline BLE sharing (scan and request sides)", "Proximity sharing issues"],
 ["`machines/QrLogin/`", "QR-based login to a relying party", "Login-with-wallet journeys"],
 ["`shared/vciClient/VciClient.ts`", "Bridge to `inji-vci-client`, callback wiring", "Every issuance callback passes through here"],
 ["`shared/openID4VP/`", "Bridge to `inji-openid4vp`, plus `walletMetadata.ts`", "What the wallet advertises it can do"],
 ["`shared/vcVerifier/VcVerifier.ts`", "Bridge to `vc-verifier`, verification + status", "Verification result and error codes"],
 ["`shared/keystore/SecureKeystore.ts`", "Bridge to `secure-keystore`", "Key generation and signing"],
 ["`shared/cryptoutil/`", "Key types, encryption helpers, signature format conversion", "`KeyTypes.ts` lists supported algorithms"],
 ["`shared/storage.ts`", "MMKV-backed encrypted store, HMAC integrity checks", "Storage and tamper detection"],
 ["`locales/`, `i18n.ts`", "App language files", "Portuguese UI strings go here"],
 ["`android/`, `ios/`", "Native modules, manifests, entitlements, deep links", "Intent filters and URL schemes"],
]
table(s, ML, y, CW, ["Path", "What it owns", "Go here when…"], rows,
      col_w=[4.3, 4.5, 3.4], fsize=9.2, row_h=0.325, head_h=0.34)
notes(s, ["Reference slide. Do not read it. Instead, pick two rows and open the actual files on screen.",
          "The most useful sentence for a new developer: 'machines/ tells you what the app is doing, shared/ tells you how it talks to the outside world, android/ and ios/ tell you how the OS reaches the app'.",
          "Point at locales/ and android/ together when you talk about Brazil: Portuguese strings in one place, deep-link schemes in the other, and both need a decision."],
      caveats=["Machine files come with generated .typegen.ts companions. Regenerate rather than edit.",
               "The repo's package name is still mosip-resident-app and the Android application id is io.mosip.residentapp for the base build — flavours override it."],
      minutes="5 min")
footer(s)

# ------------------------------------------------- storage & keys
s, y = slide("Credential storage and secure key management", kicker="On the device",
             sub="Two separate problems: keeping the credential confidential, and keeping the signing key unextractable.")
card(s, ML, y, 5.95, 2.30, "Credential storage", [
 "MMKV key-value store holds **ciphertext**, never plaintext credentials.",
 "The encryption key itself lives in the OS keystore, unlocked by device authentication.",
 "An **HMAC per credential** is stored and re-checked on read — tamper detection, not just confidentiality.",
 "mDoc credentials are kept as the original base64url CBOR; the decoded JSON exists only in the state machine's memory.",
 "Inji Web is different: credentials sit in Mimoto's Postgres, AES-256-GCM, key wrapped with a PBKDF2 key derived from the user's PIN.",
], accent=C['primary'], tint=C['primary_l'], size=10.0)
card(s, ML + 6.28, y, 5.95, 2.30, "Key management", [
 "Keys are generated **on the device**, at first use, and never leave it.",
 "`secure-keystore` abstracts Android Keystore and iOS Keychain/Secure Enclave behind one interface.",
 "Signing happens inside the platform, not in JavaScript — the app receives a signature, not a key.",
 "Device authentication (PIN, biometric) gates access to the key.",
 "The same key is used for the issuance proof and for presentation key binding.",
], accent=C['accent'], tint=C['accent_l'], size=10.0)
yy = y + 2.55
rows = [
 ["`RSA-2048`", "++Hardware keystore", "Generated and stored in Keychain, wrapped via Secure Enclave", "`RS256` proofs", "Hardware-backed on both platforms"],
 ["`EC P-256` (R1)", "++Hardware keystore", "Keychain + Secure Enclave wrapping", "`ES256` — SD-JWT key binding, mDoc device key", "The default choice for new work"],
 ["`EC secp256k1` (K1)", "~~EncryptedSharedPreferences", "Keychain, key wrapping", "`ES256K`", "Not supported by hardware keystore — signing happens in software"],
 ["`Ed25519`", "~~EncryptedSharedPreferences", "Keychain, key wrapping", "`EdDSA` — `Ed25519Signature2020` for ldp_vc", "Not supported by hardware keystore — signing happens in software"],
]
_tb_bottom = table(s, ML, yy, CW, ["Key type", "Android", "iOS", "Used for", "Consequence"], rows,
      col_w=[2.0, 2.5, 3.0, 2.8, 2.8], fsize=9.0, row_h=0.55, head_h=0.34)
yy2 = _tb_bottom + 0.14
callout(s, ML, yy2, CW, "The consequence column is the planning point: **if Brazil's trust framework demands hardware-backed keys, the practical choices are RSA-2048 and EC P-256.** Choosing Ed25519 for elegance quietly gives up hardware protection on both platforms.", kind='warn', size=10.4)
notes(s, ["Separate the two problems out loud. Confidentiality of the credential is one job; unextractability of the key is a different one. Teams conflate them and then design badly.",
          "The HMAC detail is worth a moment: the wallet does not only encrypt, it also detects modification of the stored blob. That defends against an attacker with file-system access who cannot decrypt but could corrupt.",
          "The key type table is the most practically useful thing in this section. Android's hardware keystore supports RSA and EC P-256 natively; secp256k1 and Ed25519 are not supported, so Inji generates them in software and stores them in EncryptedSharedPreferences wrapped by a hardware key. The key is protected at rest but the signing operation happens outside the secure hardware.",
          "For iOS, Inji uses key wrapping to hold keys in the Keychain with Secure Enclave protection, then brings them out to sign for the non-native curves.",
          "Tie this back to section 4: hardware protection is what makes key attestation meaningful. No hardware, no meaningful attestation."],
      caveats=["'Hardware-backed' varies by device. A low-cost Android handset may have a weaker TEE than a flagship. If assurance matters, attestation tells you what you actually got.",
               "Device loss and device change are product problems with no protocol answer. Decide the re-issuance path early; Inji has backup and restore machinery but it is a separate design conversation.",
               "Biometric changes on the device can invalidate keys bound to biometric authentication. The repo carries react-native-biometrics-changed for exactly that reason."],
      questions=["Can we export the key to a new phone? — Not if it is hardware-backed, by design. Re-issue instead.",
                 "Is one key used for every credential? — Check the version; treat per-credential keys as a design question for Brazil."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- deep links & QR
s, y = slide("Deep links, QR codes and how things get into the app", kicker="Entry points",
             sub="Four ways the outside world reaches Inji Wallet. Each one is an attack surface and a configuration item.")
rows = [
 ["OAuth redirect", "`io.mosip.residentapp.inji://oauthredirect`", "Custom URI scheme, declared in `AndroidManifest.xml` and in the issuer config in Mimoto", "Returning from the authorization server with a `code`"],
 ["OpenID4VP deep link", "`openid4vp://authorize?…`", "Intent filter on scheme `openid4vp`, host `authorize`", "Same-device presentation from a mobile browser"],
 ["Wallet-linked auth", "`io.mosip.residentapp.inji://wla-auth`", "Intent filter, host `wla-auth`", "Wallet-linked authentication callbacks"],
 ["QR scan (OpenID4VP)", "`OPENID4VP://…` or an authorization request", "Camera → `scanGuards` classify the payload", "Cross-device presentation"],
 ["QR scan (credential offer)", "`openid-credential-offer://?credential_offer_uri=…`", "Camera → `inji-vci-client` parses it", "Issuer-initiated issuance"],
 ["QR scan (QR login)", "a URL carrying `linkCode`", "Camera → `QrLogin` machine", "Log in to a relying party with the wallet"],
]
_tb_bottom = table(s, ML, y, CW, ["Entry point", "URI / payload shape", "Where it is configured", "Used for"], rows,
      col_w=[2.4, 3.7, 3.6, 2.8], fsize=9.2, row_h=0.50, head_h=0.34)
yy = _tb_bottom + 0.20
card(s, ML, yy, 5.95, 2.10, "What must line up", [
 "The redirect URI is configured in **three** places: the authorization server's client registration, `mimoto-issuers-config.json`, and the app manifest. All three must be byte-identical.",
 "Android: `intent-filter` with `action.VIEW`, categories `DEFAULT` and `BROWSABLE`.",
 "iOS: `CFBundleURLSchemes` in `Info.plist`; associated domains if you use Universal Links.",
], accent=C['primary'], tint=C['surf'], size=10.0)
card(s, ML + 6.28, yy, 5.95, 2.10, "Why this is a security surface", [
 "**Custom schemes are not exclusive.** Any app can register `openid4vp://`. On Android the user may be shown a chooser; a malicious app may win.",
 "Prefer **App Links (Android) / Universal Links (iOS)** where you can — they are domain-verified and cannot be hijacked.",
 "Every parameter arriving on a deep link is attacker-controlled. Validate before acting; never auto-submit.",
], accent=C['red'], tint=C['red_l'], size=10.0)
notes(s, ["Have the AndroidManifest.xml open on screen. Showing the actual intent-filter takes ten seconds and removes all ambiguity.",
          "The 'three places' rule is the single most common first-week failure. Write it on the flipchart.",
          "The security point deserves weight: custom URI schemes are first-come-first-served. PKCE is what saves you when a scheme is hijacked — which is the concrete reason PKCE exists, tying back to section 4.",
          "For Brazil: decide now whether to use App Links with a gov.br-owned domain. It is a better security posture and it needs DNS and hosting work, so it has lead time."],
      caveats=["Changing the URI scheme means re-registering redirect URIs at every authorization server. Decide the scheme before you onboard issuers, not after.",
               "iOS treats unknown schemes silently; a mistyped scheme fails with no error, which is painful to debug. Test on a real device early."],
      questions=["Can two Inji-based wallets coexist on one phone? — Only with distinct schemes and application ids. The repo already defines several product flavours."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- config & extension points
s, y = slide("Configuration, error handling and extension points", kicker="Where you plug in",
             sub="What you can change with a config file, what needs code, and where the code is designed to be extended.")
card(s, ML, y, 3.90, 4.35, "Configuration (no code change)", [
 "`.env` / `.env.local`: `MIMOTO_HOST`, `ESIGNET_HOST`, `OBSRV_HOST`, `APPLICATION_THEME`.",
 "`app.config.ts` and product flavours in `android/app/build.gradle` (application id, name, icons).",
 "`locales/*.json` for UI language — add `pt-BR` here.",
 "Issuer list and trusted verifiers: not in the app at all — they come from **Mimoto**.",
 "Credential labels and field order: not in the app — they come from **issuer metadata**.",
], accent=C['green'], tint=C['green_l'], size=9.8)
card(s, ML + 4.15, y, 3.90, 4.35, "Error handling", [
 "Library errors arrive with structured codes: `VCI-001` … `VCI-011` from `inji-vci-client`.",
 "`shared/error/` centralises mapping from error code to user-facing message.",
 "The state machines have explicit error states — a failure is a transition, not an exception thrown into the void.",
 "Telemetry goes to the configured Obsrv endpoint via `shared/telemetry/`.",
 "Rule: **never show a raw library error to a citizen**, and never hide it from the log.",
], accent=C['amber'], tint=C['amber_l'], size=9.8)
card(s, ML + 8.32, y, 3.91, 4.35, "Extension points", [
 "**New credential format**: add a handler in the native libraries, then rendering support. Not an app-only change.",
 "**New issuer**: configuration in Mimoto. Zero app changes if the metadata is well formed.",
 "**New language**: add a locale file; ask the issuer for matching `display` entries.",
 "**Theming**: `APPLICATION_THEME` plus asset replacement.",
 "**New transport**: the bridge pattern — a native module plus a `shared/` adapter plus a machine.",
], accent=C['violet'], tint=C['violet_l'], size=9.8)
yy = y + 4.60
callout(s, ML, yy, CW, "The test for 'is this configuration or customisation?': **if adding a second country would need the same change again, it is configuration and belongs in a file. If it only ever applies to Brazil, it is customisation and belongs in a fork you have to maintain.**", kind='tip', size=10.6)
notes(s, ["The three cards map to three different teams: ops owns the left, developers own the middle, architects own the right.",
          "Hammer the left card's last two bullets. A remarkable amount of 'app work' requested in VC projects is actually issuer metadata work or Mimoto configuration. Sorting that out early saves mobile release cycles, which are the slowest thing in the programme.",
          "The error code point is practical: VCI-001 through VCI-011 are documented in inji-vci-client. Teach support staff to capture the code, not the screenshot.",
          "The callout is the sentence to repeat in every design review. Customisation is a maintenance liability; configuration is not."],
      caveats=["Adding a credential format really is a library change. Budget for upstream contribution, not a local patch, or you will carry a fork forever.",
               "Mobile release cycles include app store review. Anything that can be moved out of the app and into Mimoto or issuer metadata should be."],
      questions=["Can we change the issuer list without a new app release? — Yes, that is exactly why it lives in Mimoto."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- demo 4
demo_slide(5, "Trace one issuance through the running app", "6 minutes",
  ["`adb logcat` attached, or Flipper with the repo's `inji.flipper` config.",
   "React Native debugger open on the running build.",
   "The `machines/Issuers/` source open in an editor.",
   "A network proxy if your environment allows it."],
  ["Start a credential download.",
   "Watch the state machine transition: issuer selected → metadata → authorize → token → proof → download → verify → store.",
   "Each transition appears in the log.",
   "The card appears at the end."],
  ["Every transition is an XState state change you can name.",
   "The callbacks from `inji-vci-client` surface as native events: `onRequestAuthCode`, `onRequestProof`, `onRequestTxCode`.",
   "The proof JWT is created in `RNSecureKeystoreModule` and handed back through `VciClient.sendProof()`.",
   "`vc-verifier` runs before the store write."],
  fail="If nothing is logged after the browser closes, the redirect never reached the app — go straight to the deep-link configuration, not to the protocol.")
notes(prs.slides[-1],
      ["This demo teaches the debugging reflex we want people to leave with: name the state you are in, and the failure localises itself.",
       "The 'nothing logged after the browser closes' heuristic is worth repeating. It separates a protocol problem from an OS-integration problem in five seconds.",
       "If the room is not developer-heavy, run this as a narrated screen recording instead of live."],
      caveats=["Do not do this against a production environment or real citizen data.",
               "Proxying TLS on a modern Android build requires a user CA and network security config — set it up beforehand, not on stage."],
      minutes="6 min")

# =================================================================== SECTION 7
section("Mimoto — the wallet backend", "25 min",
        "Why there is a backend at all, what belongs in it, and — just as important — what must never be put in it.",
        ["Why Mimoto exists",
         "Internal architecture",
         "The API surface",
         "Issuer and verifier configuration",
         "Format handlers and verification",
         "Responsibility matrix"], highlight=('mimoto',), num="7")
notes(prs.slides[-1], ["Warn the room that this section contains the most frequently violated design rule in the whole stack: putting issuer or verifier logic into Mimoto.",
                       "Ask early who will operate Mimoto in Brazil — the answer shapes the deployment discussion later."],
      minutes="25 min for the section")

# ------------------------------------------------- mimoto why + arch
s, y = slide("Why Mimoto exists", kicker="Rationale",
             sub="Four problems that a pure client-side wallet cannot solve cleanly.")
probs = [
 ("A browser cannot be a wallet on its own", "Inji Web has no secure key storage and no persistent local store you would trust. Someone has to hold the credential and the key. That someone is Mimoto.", C['accent']),
 ("Somebody must curate the issuer list", "Citizens should not type issuer URLs. Mimoto serves a governed catalogue, with logos, descriptions and per-issuer configuration, updatable without an app release.", C['primary']),
 ("Client secrets cannot live in an app", "Token exchange with an authorization server may need client authentication. Mimoto does it server-side so nothing sensitive ships in the APK.", C['violet']),
 ("Shared services belong in one place", "Caching of metadata, PDF rendering of credentials, the trusted-verifier list, telemetry and session handling — all needed by both Wallet and Web.", C['green']),
]
for i, (t, d, col) in enumerate(probs):
    x = ML + (i % 2) * (CW / 2 + 0.12)
    yy = y + (i // 2) * 1.48
    wid = CW / 2 - 0.12
    rect(s, x, yy, wid, 1.30, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
    rect(s, x, yy, 0.055, 1.30, fill=col)
    _, t2 = tb(s, x + 0.22, yy + 0.14, wid - 0.42, 0.30)
    para(t2, t, size=12, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.22, yy + 0.48, wid - 0.42, 0.74)
    para(t3, d, size=9.8, color=C['ink2'], first=True, line_spacing=1.26)
yy = y + 3.05
card(s, ML, yy, 5.95, 1.90, "Mimoto must NOT", [
 "Sign credentials. That is the issuer's monopoly.",
 "Decide whether a presentation is acceptable. That is the verifier's job.",
 "Become an identity registry. It stores credentials for Web users, not a population database.",
 "Hold the Wallet's private keys. Those never leave the device.",
], accent=C['red'], tint=C['red_l'], size=10.0)
card(s, ML + 6.28, yy, 5.95, 1.90, "The test to apply", [
 "Ask: *would an external, standards-compliant wallet need this?*",
 "If no — it is Inji-internal convenience, and Mimoto is the right home.",
 "If yes — it belongs in the protocol or in the issuer, and putting it in Mimoto breaks interoperability.",
], accent=C['accent'], tint=C['accent_l'], size=10.0)
notes(s, ["The four reasons are worth stating in order, because they are the ones that come back as challenges in design reviews.",
          "Reason 1 is the strongest. Once you decide to support a browser-based holder, a server-side credential store is almost unavoidable — and that brings the data residency question with it.",
          "The 'must not' card is the one to photograph. Every one of those four has been proposed in real projects.",
          "The test on the right is a practical tie-breaker. Mimoto is a convenience layer for Inji's own clients. The moment its behaviour becomes load-bearing for an external wallet, you have accidentally invented a proprietary protocol."],
      caveats=["Mimoto is an Inji component, not an OpenID4VC component. Never describe a Mimoto endpoint to an external partner as if it were standard.",
               "A single Mimoto holding credentials for millions of Web users is a high-value target. Treat it as such in the security review."],
      questions=["Could Brazil run Wallet without Mimoto? — Technically much of the mobile flow could be direct, but you lose the governed issuer catalogue and Inji Web entirely.",
                 "Can Mimoto be multi-tenant? — Configuration is per-deployment today; plan a deployment per programme."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- mimoto internals
s, y = slide("Inside Mimoto", kicker="Architecture",
             sub="Spring Boot, Java 21. Controllers at the edge, services in the middle, Postgres and Redis behind.")
# columns diagram
colw = 2.55
cols = [
 ("Clients", [("Inji Wallet", C['accent']), ("Inji Web", C['accent'])], C['accent'], C['accent_l']),
 ("Controllers", [("IssuersV2Controller", None), ("WalletsController", None),
                  ("WalletCredentialsController", None), ("WalletPresentationsController", None), ("VerifiersController", None), ("IdpController / TokenAuth", None),
                  ("CredentialsController (PDF)", None), ("AttestationServiceController", None)], C['primary'], C['primary_l']),
 ("Services", [("IssuersService", None), ("CredentialService", None),
               ("CredentialRequestService", None), ("CredentialFormatHandlerFactory", None),
               ("CredentialVerifierService", None), ("PresentationService / OpenID4VPService", None),
               ("CredentialMatchingService", None), ("WalletService / Unlock / Lock", None),
               ("DataProtectionService", None), ("TrustedVerifierService", None)], C['violet'], C['violet_l']),
 ("State and config", [("Postgres — wallets, credentials", None), ("Redis or Caffeine — cache, sessions", None),
                       ("mimoto-issuers-config.json", None), ("mimoto-trusted-verifiers.json", None),
                       ("mimoto-default.properties", None)], C['green'], C['green_l']),
 ("Outbound", [("Issuer well-known", None), ("Authorization server token endpoint", None),
               ("Credential endpoint", None), ("Verifier response_uri", None),
               ("Google / OIDC login", None)], C['amber'], C['amber_l']),
]
gapx = 0.12
cw2 = (CW - gapx * 4) / 5
for i, (title, items, col, tint) in enumerate(cols):
    x = ML + i * (cw2 + gapx)
    rect(s, x, y, cw2, 4.32, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.045)
    rect(s, x, y, cw2, 0.07, fill=col)
    _, t2 = tb(s, x + 0.14, y + 0.20, cw2 - 0.28, 0.3)
    para(t2, title.upper(), size=9.5, color=col, bold=True, first=True)
    cy = y + 0.55
    for nm, _c in items:
        rect(s, x + 0.11, cy, cw2 - 0.22, 0.325, fill=C['white'], line=C['surf2'], lw=0.8,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.16)
        _, t3 = tb(s, x + 0.17, cy, cw2 - 0.34, 0.325, anchor=MSO_ANCHOR.MIDDLE)
        para(t3, nm, size=8.1, color=C['ink2'], font=F_MONO if i in (1, 2) else F_SANS,
             first=True, line_spacing=0.98)
        cy += 0.372
    if i < 4:
        c = line(s, x + cw2 + 0.005, y + 2.1, x + cw2 + gapx - 0.01, y + 2.1, C['muted'], 1.2)
        arrowhead(c, tail=True, size='sm')
yy = y + 4.52
callout(s, ML, yy, CW, "Notice `CredentialFormatHandlerFactory` and its `LdpVcCredentialFormatHandler`, `VcSdJwtCredentialFormatHandler`, `DcSdJwtCredentialFormatHandler`. **Format support in Mimoto is a strategy pattern** — adding a format means adding a handler, not editing controllers.", kind='tip', size=10.4)
notes(s, ["Read the columns left to right as a request's journey.",
          "The controller list tells you the API surface at a glance. Two families: the older issuer/credential endpoints used by the mobile wallet, and the newer /wallets/** family that powers Inji Web's logged-in experience.",
          "The services column is where the real work is. CredentialFormatHandlerFactory is the extension seam worth naming explicitly — it is how a new credential format enters Mimoto.",
          "State column: Postgres for durable wallet and credential data, Redis (or Caffeine for single-instance) for caching and sessions. The README is explicit that Caffeine is fine for one instance and Redis is required for a load-balanced deployment. That is an operational footgun worth flagging to whoever runs the cluster.",
          "Outbound column: these are the calls that fail in production. Every one of them needs egress rules, timeouts and monitoring."],
      caveats=["Running several Mimoto replicas with Caffeine gives each replica its own cache and inconsistent behaviour. Use Redis in any clustered deployment.",
               "Sessions: Mimoto's HTTP session holds the unlocked wallet key for Inji Web users. server.servlet.session.timeout defaults to 30 minutes and is a real security parameter."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- mimoto API + config
s, y = slide("Mimoto's API surface and configuration files", kicker="What you will call and edit",
             sub="Base path `/v1/mimoto`. Two groups: catalogue endpoints, and the stateful wallet endpoints used by Inji Web.")
rows = [
 ["`GET /v2/issuers`", "The governed issuer catalogue", "Wallet, Web"],
 ["`GET /issuers/{id}/configuration`", "Issuer well-known + auth server well-known, merged and cached", "Web"],
 ["`GET /issuers/{id}/well-known-proxy`", "Proxy to the issuer's well-known document", "Wallet"],
 ["`POST /get-token/{issuer}`", "Broker the authorization-code → access-token exchange", "Wallet"],
 ["`GET /verifiers`", "The trusted verifier list", "Wallet"],
 ["`POST /wallets`  ·  `POST /wallets/{id}/unlock`", "Create a Web wallet with a PIN; unlock it for a session", "Web"],
 ["`POST /wallets/{id}/credentials`", "Download a credential into the Web wallet", "Web"],
 ["`GET /wallets/{id}/credentials`", "List stored credentials; `/{credentialId}` fetches or downloads one", "Web"],
 ["`POST /wallets/{id}/presentations`", "Start an OpenID4VP presentation for a Web session", "Web"],
 ["`GET /wallets/{id}/presentations/{pid}/credentials`", "Which stored credentials match this request", "Web"],
 ["`POST /credentials/download`", "Render a credential as a PDF", "Wallet, Web"],
 ["`POST /safetynet/{online|offline}/verify`", "Device attestation verification", "Wallet"],
]
table(s, ML, y, 7.55, ["Endpoint", "What it does", "Caller"], rows,
      col_w=[3.5, 3.4, 1.0], fsize=8.9, row_h=0.325, head_h=0.32)
codebox(s, ML + 7.86, y, 4.37, 2.35, [
 '// mimoto-issuers-config.json',
 '{ "issuers": [{',
 '  "issuer_id": "GovBR",',
 '  "display": [{ "name":"gov.br",',
 '                "language":"pt" }],',
 '  "protocol": "OpenId4VCI",',
 '  "client_id": "inji-wallet",',
 '  "credential_issuer_host": "https://…",',
 '  "wellknown_endpoint": "https://…",',
 '  "redirect_uri": "io.mosip…://oauthredirect",',
 '  "token_endpoint": "https://…/get-token/GovBR",',
 '  "enabled": "true" }] }',
], label="ADDING AN ISSUER", size=8.3, hl=[9])
codebox(s, ML + 7.86, y + 2.58, 4.37, 1.62, [
 '// mimoto-trusted-verifiers.json',
 '{ "verifiers": [{',
 '  "client_id": "verify.gov.br",',
 '  "redirect_uris": ["https://verify.gov.br/"],',
 '  "response_uris": ["https://verify.gov.br/vp"],',
 '  "jwks_uri": "https://verify.gov.br/.well-known/jwks.json",',
 '  "allow_unsigned_request": false }] }',
], label="ADDING A VERIFIER", size=8.3, hl=[6])
notes(s, ["Point at the two JSON files. Between them they carry most of the day-two operational work: onboarding issuers and onboarding verifiers.",
          "The highlighted line in the issuer config is redirect_uri — the third of the 'three places' from the deep-links slide.",
          "The highlighted line in the verifier config is allow_unsigned_request. Set it to false for any verifier you actually care about: it forces signed authorization requests and makes verifier impersonation much harder. The sample shipped in the repo has it true, which is convenient for demos and wrong for production.",
          "jwks_uri is how the wallet validates a signed request from that verifier. No jwks_uri means no signature validation is possible.",
          "Mention that the /wallets/** family is what makes Inji Web work; the mobile wallet does not use it."],
      caveats=["These files are configuration, but they are security configuration. Treat changes to them as you would firewall rules: reviewed, versioned, audited.",
               "Caching means a change here is not instant. Know your TTLs."],
      questions=["Can the issuer list differ per user segment? — Not out of the box; it is a deployment-wide catalogue.",
                 "How do we onboard a verifier we do not control? — You still need their client_id, response_uri and JWKS. There is no way around exchanging that information."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- responsibility matrix
s, y = slide("Responsibility matrix — the slide to settle arguments", kicker="Who owns what",
             sub="Print this. Put it on the wall of the integration room.")
callout(s, ML, y, CW, "Read the key/credential rows across: for **Inji Wallet** they are on the device; for **Inji Web** they are in Mimoto. Same protocol, very different privacy and data-residency profile — the most important architectural difference between the two products.", kind='warn', size=10.4)
rows = [
 ["Authenticate the citizen", "", "", "", "++OWNS (via its AS)", ""],
 ["Decide eligibility, mint and sign the credential", "", "", "", "++OWNS", ""],
 ["Publish issuer metadata and public keys", "", "", "", "++OWNS", ""],
 ["Curate which issuers appear in the app", "", "", "++OWNS", "", ""],
 ["Run the OpenID4VCI client state machine", "++OWNS", "via Mimoto", "++for Web", "", ""],
 ["Generate/protect the holder key and sign the issuance proof", "++OWNS", "", "++OWNS (for Web)", "", ""],
 ["Store the credential", "++OWNS (device)", "", "++OWNS (Postgres)", "", ""],
 ["Show the consent screen", "++OWNS", "++OWNS", "", "", ""],
 ["Match credentials, build and sign the VP token", "++OWNS", "", "++OWNS (for Web)", "", ""],
 ["Validate the verifier before responding", "++OWNS", "", "++OWNS", "", ""],
 ["Verify the issuer signature and decide whether to grant access", "", "", "", "", "++OWNS"],
]
table(s, ML, y + 0.72, CW, ["Responsibility", "Inji Wallet", "Inji Web", "Mimoto", "Issuer", "Verifier"], rows,
      col_w=[4.8, 1.6, 1.4, 1.7, 1.5, 1.3], fsize=8.9, hsize=9.2, row_h=0.30, head_h=0.34,
      align=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER])
notes(s, ["Give the room a minute to read it, then draw attention to the Wallet/Web asymmetry in the key, proof and storage rows.",
          "For a regulator or a privacy officer, that asymmetry is the headline: with the mobile wallet, the state does not hold the citizen's credentials; with the web wallet, it does. Brazil must decide deliberately, not by accident of which product gets deployed first.",
          "The last row belongs to the verifier alone. If anyone proposes Mimoto 'helping' with verification decisions, point here.",
          "Use this matrix as the answer key for Exercise 2 later in the day."],
      caveats=["Mimoto does verify credentials in some flows (CredentialVerifierService) — that is integrity verification at download for the Web wallet, not an access decision. Keep the distinction crisp.",
               "This matrix reflects the current reference implementation. A Brazilian variant may shift boxes; if so, document it explicitly."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- demo 7
demo_slide(6, "Watch Mimoto handle a request", "5 minutes",
  ["Mimoto running locally (`docker-compose` in the repo brings up Mimoto, Postgres and Redis).",
   "Its logs on screen, at INFO or DEBUG.",
   "Swagger / the Stoplight API docs open.",
   "`curl` or Postman ready — the repo ships Postman collections in `docs/postman-collections/`."],
  ["Call `GET /v2/issuers` and see the catalogue.",
   "Call `GET /issuers/{id}/configuration` twice.",
   "The second call is dramatically faster.",
   "Change an issuer's display name, call again — nothing changes yet."],
  ["The first configuration call fetched **two** well-known documents and merged them.",
   "The second was served from the Caffeine cache.",
   "The unchanged display name is the cache TTL, `cache.credential-issuer.wellknown.expiry-time-in-min`.",
   "This is the same cache that will make you think your issuer metadata fix did not work."],
  fail="Deliberately stop the issuer and call the configuration endpoint again. Note the error Mimoto returns and how it differs from a cache hit — that difference is your first triage signal.")
notes(prs.slides[-1],
      ["This demo exists to teach one lesson: the cache is real, and it will waste your afternoon if you do not know about it.",
       "Show the TTL property in mimoto-default.properties and lower it live if you can.",
       "The failure variant is the useful part — knowing what Mimoto says when the issuer is down is worth more than knowing what it says when everything works."],
      caveats=["Do not run this against a shared environment; you will be changing configuration.",
               "Redis versus Caffeine changes the behaviour you will see. Say which one you are running."],
      minutes="5 min")

# ------------------------------------------------- libraries
s, y = slide("The Inji libraries — what to use and what not to rewrite", kicker="SDKs",
             sub="Each library owns one problem. If your application code is solving one of these problems, stop and use the library.")
rows = [
 ["`inji-vci-client`", "Running OpenID4VCI correctly (drafts 11 and 13), both flows, PKCE internally",
  "Credential offer or issuer + config id, client metadata, a set of callbacks",
  "`CredentialResponse`: credential, `credentialConfigurationId`, `credentialIssuer`",
  "!!PKCE, metadata discovery, request construction, error taxonomy"],
 ["`inji-openid4vp`", "Running OpenID4VP (drafts 21 and 23) — request validation through response delivery",
  "Encoded authorization request, trusted verifiers, selected credentials, signatures",
  "Validated request; unsigned VP token to sign; response POSTed to the verifier",
  "!!client_id scheme rules, presentation submission, response encryption"],
 ["`vc-verifier`", "Deciding whether a credential is authentic and well-formed",
  "Credential + format string", "`verificationStatus`, message, error code, credential status",
  "!!Signature verification, key resolution, SD-JWT digest checks, mDoc validation"],
 ["`secure-keystore`", "Platform key storage and signing",
  "Key alias, algorithm, data to sign", "A signature — never a private key",
  "!!Anything touching Android Keystore or iOS Keychain directly"],
 ["`pixelpass`", "QR encoding/decoding and CBOR ↔ JSON",
  "CBOR bytes or a data payload", "JSON for rendering, or a compact QR payload",
  "!!CBOR parsing, QR compression"],
 ["`inji-vc-renderer`", "Turning a credential into a visual representation",
  "Credential + template", "Rendered output for display",
  "!!Bespoke per-credential rendering code"],
 ["`tuvali`", "BLE transport for offline device-to-device sharing",
  "Payload + peer connection", "Delivered payload",
  "!!BLE state machines and chunking"],
]
_tb_bottom = table(s, ML, y, CW, ["Library", "Problem it solves", "Input", "Output", "Do NOT reimplement"], rows,
      col_w=[1.9, 3.1, 2.6, 2.6, 2.6], fsize=8.7, hsize=9.0, row_h=0.62, head_h=0.34)
yy = _tb_bottom + 0.14
callout(s, ML, yy, CW, "Integration point to remember: the libraries are **callback-driven**. They ask the application for a tx code, a token, a proof, a signature — and the application answers. Nothing that can sign is ever inside a library.", kind='tip', size=10.4)
notes(s, ["Frame the last column as a governance statement, not just advice. Reimplementing any of those is how a deployment quietly becomes non-interoperable.",
          "inji-openid4vp is Kotlin Multiplatform and ships as both AAR and JAR — the same code runs inside the phone and inside Mimoto. That is why Wallet and Web behave consistently.",
          "vc-verifier deserves a special mention: it is the component that decides trust, and it is shared by the wallet and by Mimoto. Its key resolver support (did:web, did:key, did:jwk, HTTPS, X.509) is effectively your trust infrastructure.",
          "The callback point is the integration lesson. When you port to a new platform, you implement the callbacks, not the protocol."],
      caveats=["Library versions must be compatible with each other; the wallet's build file excludes transitive copies of vcverifier and openid4vp to avoid duplicate classes. Expect to do the same in any host app.",
               "Check Swift parity before committing to an iOS date for any feature you see in the Kotlin README."],
      minutes="6 min")
footer(s)

# =================================================================== SECTION 8
section("Credential presentation with OpenID4VP", "30 min",
        "The verifier asks; the wallet decides what to send. Request validation, credential matching, consent, the VP token, and what the verifier must check.",
        ["The authorization request, field by field",
         "client_id schemes and why they matter",
         "Matching and consent",
         "The VP token and presentation submission",
         "direct_post and direct_post.jwt",
         "Verifier-side validation checklist"], highlight=('wallet', 'store', 'verifier'), num="8")
notes(prs.slides[-1], ["Remind the room of Demo 2 — this section explains what they already watched.",
                       "Flag that the verifier-side checklist at the end is the slide verifier developers should take away."],
      minutes="30 min for the section")

# ------------------------------------------------- OVP request
s, y = slide("The OpenID4VP authorization request", kicker="Message 1",
             sub="Everything the wallet needs to decide whether to talk to this verifier at all, and what it is being asked for.")
codebox(s, ML, y, 6.15, 2.95, [
 'openid4vp://authorize?',
 '  client_id=verify.gov.br',
 '  &client_id_scheme=pre-registered      // draft 21 only',
 '  &response_type=vp_token',
 '  &response_mode=direct_post',
 '  &response_uri=https://verify.gov.br/vp',
 '  &nonce=n-0S6_WzA2Mj',
 '  &state=af0ifjsldkj',
 '  &presentation_definition={…}          // or …_uri',
 '  &client_metadata={…}',
 '',
 '// or, by reference — keeps the QR small:',
 '  ?client_id=verify.gov.br&request_uri=https://…/req',
 '   &request_uri_method=post',
], label="AUTHORIZATION REQUEST", size=8.7, hl=[1, 5, 6, 7])
rows = [
 ["`client_id`", "Who is asking. Meaning depends on the scheme."],
 ["`client_id_scheme`", "How to authenticate that claim. Present → draft 21. Absent → draft 23 rules."],
 ["`response_type`", "Always `vp_token` here."],
 ["`response_mode`", "`direct_post` or `direct_post.jwt` (encrypted). Inji also supports `iar-post` variants."],
 ["`response_uri`", "Where the wallet POSTs the answer. Must match the registered value."],
 ["`nonce`", "Freshness. Goes into the holder's signature so the verifier knows the presentation is for this request."],
 ["`state`", "The verifier's own correlation handle. Echoed back untouched."],
 ["`presentation_definition`", "What is being asked for: input descriptors, fields, constraints, format filters."],
 ["`client_metadata`", "The verifier's own metadata — including the public key used to encrypt the response."],
]
table(s, ML + 6.46, y, 5.77, ["Parameter", "What it is for"], rows,
      col_w=[1.9, 3.9], fsize=8.9, row_h=0.33, head_h=0.32)
yy = y + 3.20
card(s, ML, yy, 6.15, 1.95, "client_id schemes Inji supports", [
 "`pre-registered` — the verifier is in the wallet's trusted list. Signed requests validated against its `jwks_uri`. Unsigned allowed only if `allow_unsigned_request` is true.",
 "`redirect_uri` — the `client_id` **is** the response URI. The request must be unsigned.",
 "`did` — `client_id` is a DID; the request must be signed and the key resolved from the DID document via `kid`.",
], accent=C['primary'], tint=C['primary_l'], size=9.6)
card(s, ML + 6.46, yy, 5.77, 1.95, "Why this is the security hinge", [
 "The scheme decides **how the wallet knows the verifier is who it claims to be.**",
 "`pre-registered` with `shouldValidateClient = true` is the strongest posture — and it defaults to true from release 0.4.x onwards.",
 "Turning validation off makes demos easy and makes verifier impersonation trivial. Do not ship it.",
], accent=C['red'], tint=C['red_l'], size=9.6)
notes(s, ["Go through the highlighted parameters only: client_id, response_mode, response_uri, nonce.",
          "nonce is the anti-replay mechanism on this side of the protocol, mirroring c_nonce on the issuance side. Draw the parallel explicitly — it helps people remember both.",
          "state is not a security control; it is correlation. People confuse the two constantly. nonce is signed by the holder; state is not.",
          "The client_id scheme discussion is the heart of the slide. Explain that draft 21 carried client_id_scheme as its own parameter, and draft 23 folded it into the client_id value. inji-openid4vp infers which draft you are speaking by whether that parameter is present — an elegant trick worth knowing when you debug.",
          "Request by reference (request_uri) is how real verifiers keep QR codes scannable. Note that Inji can POST wallet metadata to the request_uri when request_uri_method=post, which lets the verifier tailor the request to the wallet's capabilities."],
      caveats=["shouldValidateClient defaulting to true is a breaking change from earlier releases. If an integration that used to work stops working, check this first.",
               "A request by reference must be a signed JWT. Unsigned by-reference requests are not accepted.",
               "presentation_definition_uri means another network call — one more thing that can fail in a shop with bad wifi."],
      questions=["Can a verifier ask for two credentials at once? — Yes, with multiple input descriptors.",
                 "What if the wallet does not trust the verifier? — It stops before showing the user anything. That is correct."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- OVP sequence
s, y = slide("Cross-device presentation, step by step", kicker="Sequence — OpenID4VP",
             sub="`direct_post`. The wallet is the client; the verifier never connects to the phone.")
sequence(s, ["User", "Verifier", "Inji Wallet", "inji-openid4vp", "Credential Store"],
 [(1, 1, "Create request, store nonce + state against a session", 'self'),
  (1, 0, "Show QR (request by value, or `request_uri`)", 'resp'),
  (0, 2, "Scan the QR"),
  (2, 3, "`authenticateVerifier(request, trustedVerifiers, true)`"),
  (3, 1, "`GET`/`POST request_uri` — only if by reference"),
  (1, 3, "signed Authorization Request Object (JWT)", 'resp'),
  (3, 3, "Validate client_id scheme, signature, required fields", 'self'),
  (3, 2, "validated `AuthorizationRequest`", 'resp'),
  (2, 4, "Find credentials matching the `presentation_definition`"),
  (4, 2, "candidate credentials", 'resp'),
  (2, 0, "Show verifier identity + requested claims — consent", 'resp'),
  (0, 2, "User selects credential(s) and approves"),
  (2, 3, "`constructUnsignedVPToken(selected, holderId, alg)`"),
  (3, 2, "unsigned VP token per format (KB-JWT header+payload)", 'resp'),
  (2, 2, "Sign with the bound key in the secure keystore", 'self'),
  (2, 3, "`shareVerifiablePresentation(signingResult)`"),
  (3, 1, "`POST response_uri`  vp_token + presentation_submission + state"),
  (1, 1, "Verify issuer signature, holder binding, nonce, then decide", 'self'),
 ], top=1.42, height=5.20)
notes(s, ["This is the mirror image of the issuance sequence. Point that out — the symmetry helps.",
          "Step 7 is where a hostile verifier is stopped. Everything before it is untrusted input.",
          "Step 9: matching happens against the presentation_definition's input descriptors and field constraints. The wallet is filtering locally — no network, no issuer involvement.",
          "Step 11 is the consent screen. It is the only place a human decides anything in this entire protocol.",
          "Steps 13 to 16 are the two-phase signing dance: the library builds the unsigned token, the app signs it with a key the library cannot see, the library assembles and sends. Same pattern as issuance.",
          "Step 18 is the verifier's whole job, and it is expanded on the checklist slide."],
      caveats=["There is no redirect back to a browser in cross-device. The verifier's screen must learn of success through its own session — polling or server-sent events. Verifier teams miss this repeatedly.",
               "If an mso_mdoc credential is in the response, direct_post.jwt is mandatory per ISO 18013-7 and the library enforces it.",
               "If the selected SD-JWT VC has no cnf, steps 14 and 15 produce nothing to sign and the presentation goes out unbound."],
      questions=["Who chooses when several credentials match? — The user, on the consent screen.",
                 "Can the wallet refuse part of a request? — It can present a subset; the verifier decides whether that is enough."],
      minutes="9 min")
footer(s)

# ------------------------------------------------- VP token
s, y = slide("The response: vp_token, presentation submission, and encryption", kicker="Message 2",
             sub="What actually gets POSTed, and the difference between direct_post and direct_post.jwt.")
codebox(s, ML, y, 6.15, 2.30, [
 'POST /vp   Content-Type: application/x-www-form-urlencoded',
 '',
 'vp_token = "eyJraWQi…~WyJzYWx0Iiwibm9tZSIsIkFuYSJd~eyJ0eXAi…"',
 '           //  issuer JWT  ~   disclosure(s)   ~   KB-JWT',
 '&presentation_submission = {',
 '   "id": "sub-1", "definition_id": "def-1",',
 '   "descriptor_map": [{ "id": "cpf", "format": "vc+sd-jwt",',
 '                        "path": "$" }] }',
 '&state = af0ifjsldkj',
], label="direct_post — UNENCRYPTED", size=8.6, hl=[2, 3])
codebox(s, ML, y + 2.56, 6.15, 1.55, [
 'POST /vp',
 'response = <JWE>',
 '',
 '// JWE header: alg=ECDH-ES, enc=A256GCM',
 '//   apu = wallet-generated nonce (16 bytes of entropy)',
 '//   apv = the verifier nonce from the request',
 '// encrypted to the key in client_metadata',
], label="direct_post.jwt — ENCRYPTED", size=8.6, hl=[1])
rows = [
 ["`vp_token`", "The presentation itself. Shape depends on format: SD-JWT string, CBOR for mDoc, JSON-LD VP for ldp_vc."],
 ["`presentation_submission`", "A map telling the verifier which input descriptor each credential answers, and where to find it."],
 ["`state`", "Echoed so the verifier can find its session."],
 ["`response` (JWE)", "In `direct_post.jwt`, everything above is encrypted into one JWE."],
]
table(s, ML + 6.46, y, 5.77, ["Field", "What it carries"], rows,
      col_w=[2.0, 3.8], fsize=9.0, row_h=0.62, head_h=0.32)
yy = y + 2.90
card(s, ML + 6.46, yy, 5.77, 2.20, "When to insist on direct_post.jwt", [
 "Whenever the claims are sensitive and the `response_uri` terminates TLS somewhere you do not control (CDN, WAF, load balancer).",
 "**Always** for mDoc — ISO 18013-7 requires it and `inji-openid4vp` enforces it.",
 "Inji supports `ECDH-ES` key agreement with `A256GCM` content encryption.",
 "`apu`/`apv` bind the encryption to this wallet and this request, so a captured JWE cannot be re-used.",
], accent=C['accent'], tint=C['accent_l'], size=9.8)
notes(s, ["Show the tildes again in the vp_token. Continuity with the SD-JWT slide pays off here.",
          "presentation_submission is the piece verifier developers forget. Without it the verifier has to guess which credential answers which descriptor. Read it, do not ignore it.",
          "The encryption discussion is practical, not academic: in most real deployments TLS terminates at a load balancer or a WAF, so the plaintext presentation exists, briefly, on infrastructure that is not the verifier's application. direct_post.jwt closes that gap end to end.",
          "apu and apv are the ephemeral-binding values. Mention them as the reason a captured JWE is not replayable to another session."],
      caveats=["Presentation Exchange (the presentation_definition / presentation_submission pair) is being superseded by the Digital Credentials Query Language in later OpenID4VP drafts. Inji is on drafts 21 and 23 and uses Presentation Exchange. Expect this to change; do not build deep dependencies on the submission format.",
               "An encrypted response is unsigned at the JWE layer — authenticity comes from the credential signatures inside, not from the envelope."],
      questions=["Does encryption replace holder binding? — No. Encryption protects the channel; binding proves who presented."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- verifier checklist
s, y = slide("What a verifier must check — the checklist", kicker="Verifier side",
             sub="Hand this to whoever builds Brazil's verifiers. A verifier that skips any of these is not a verifier.")
groups = [
 ("Before you trust the envelope", [
   "`state` matches a session you opened, and that session is not already used.",
   "The response arrived at the `response_uri` you published, over TLS you control.",
   "`presentation_submission` maps every input descriptor you asked for.",
 ], C['primary']),
 ("The credential itself", [
   "Issuer signature verifies against a key you resolved from a **trusted** source.",
   "The issuer is one you accept for this claim — a valid signature from the wrong issuer is worthless.",
   "`iat` / `exp` / `validityInfo` are within range.",
   "For SD-JWT: each disclosure's digest is present in `_sd`, using the declared `_sd_alg`.",
   "For mDoc: `issuerAuth` COSE signature valid, element digests match the MSO, doc type and issuing country expected.",
 ], C['accent']),
 ("The holder", [
   "A key-binding artefact is present: KB-JWT, `DeviceSignature`, or VP proof.",
   "It is signed by the key named in the credential (`cnf`, `deviceKey`, or `credentialSubject.id`).",
   "It covers **your** `nonce` and names **you** in `aud`.",
   "For SD-JWT: `sd_hash` matches exactly the disclosures you received.",
 ], C['violet']),
 ("Your own policy", [
   "Did you receive only the claims you asked for — and did you need all of them?",
   "Is this credential type acceptable for this decision?",
   "Revocation / status: do you check it, and can you tolerate the privacy cost of doing so?",
   "Log the decision, not the credential.",
 ], C['green']),
]
bw = (CW - 3 * 0.20) / 4
for i, (t, items, col) in enumerate(groups):
    x = ML + i * (bw + 0.20)
    rect(s, x, y, bw, 4.60, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    rect(s, x, y, bw, 0.065, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.22, bw - 0.40, 0.5)
    para(t2, t, size=11.5, color=col, bold=True, first=True, line_spacing=1.08)
    cy = y + 0.82
    for it in items:
        rect(s, x + 0.20, cy + 0.045, 0.14, 0.14, fill=None, line=col, lw=1.2)
        _, t3 = tb(s, x + 0.44, cy, bw - 0.66, 0.9)
        parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', it)
        ch = []
        for pt in parts:
            if not pt:
                continue
            if pt.startswith('`'):
                ch.append((pt[1:-1], C['primary'], False, False, F_MONO))
            elif pt.startswith('**'):
                ch.append((pt[2:-2], C['ink'], True))
            else:
                ch.append((pt, C['ink2'], False))
        rich(t3, ch, size=9.3, first=True, line_spacing=1.25)
        nl = max(1, -(-len(re.sub(r'[`*]', '', it)) // 34))
        cy += 0.16 + nl * 0.155
notes(s, ["This is a takeaway slide. Say so, and pause on it.",
          "The second bullet in 'The credential itself' is the one that is most often missed: verifying a signature only tells you the data is unaltered. It says nothing about whether that issuer is allowed to assert this claim. Trust policy is separate from cryptography.",
          "In 'The holder', the aud and nonce checks are what stop a presentation captured at verifier A being replayed at verifier B. If your verifier does not check them, holder binding gives you nothing.",
          "'Log the decision, not the credential' is a data-protection point with teeth. Verifier logs full of presented claims are a breach waiting to happen.",
          "Note Inji Wallet does not perform revocation checking for any format today — so if revocation matters in Brazil, the verifier side must own it."],
      caveats=["Status list checking leaks to the issuer that a verification is happening, unless you use a privacy-preserving mechanism. That is a genuine design trade-off, not an oversight.",
               "vc-verifier has a PresentationVerifier with holder-binding validation for did:key and did:jwk holders; unsupported DID methods are skipped rather than failed. Know what your verifier actually enforces."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- demo 5
demo_slide(7, "Cross-device and same-device, back to back", "6 minutes",
  ["Verifier reachable from both the phone's network and the laptop's.",
   "The verifier registered in `mimoto-trusted-verifiers.json` with the exact `response_uri`.",
   "A mobile browser on the same phone as the wallet, for the same-device run.",
   "A network trace if possible."],
  ["**Cross-device**: QR on the laptop, scan with the phone, laptop flips to success without the user touching it.",
   "**Same-device**: open the verifier in the phone's browser, tap the button, the wallet opens directly, then the browser returns.",
   "The consent screen is identical in both."],
  ["Cross-device: the phone POSTs to `response_uri`; the laptop learns of success from **its own** backend.",
   "Same-device: the browser fired an `openid4vp://authorize` deep link; after posting, the wallet sends the user back.",
   "The protocol messages are the same in both runs — only the delivery channel and the return path differ."],
  fail="If the same-device run opens a browser page saying 'no app can handle this link', the intent filter or URL scheme is wrong. That is an OS configuration problem, not a protocol problem.")
notes(prs.slides[-1],
      ["Running both in succession is what makes the concept stick. Do not skip one for time.",
       "The 'laptop learns from its own backend' point is the lesson for verifier developers in the room.",
       "Ask the room to predict what changes in the HTTP trace between the two runs. Answer: almost nothing."],
      caveats=["Same-device needs the verifier's web page to be reachable on the phone, which trips up localhost-only demo setups.",
               "If several wallets are installed, Android may show a chooser — good material for the security discussion."],
      minutes="6 min")

# =================================================================== SECTION 9
section("Inji Web and device flows", "25 min",
        "The browser wallet: why it exists, how it differs from the mobile wallet, and how the four device journeys actually work.",
        ["Why a browser wallet",
         "Frontend architecture and the BFF pattern",
         "Guest and logged-in journeys",
         "Same-device, cross-device, handoff",
         "What Web does that Wallet does not",
         "Theming, localisation, deployment"], highlight=('web', 'mimoto'), num="9")
notes(prs.slides[-1], ["Frame the inclusion argument up front: not every citizen has a smartphone, and a national programme cannot require one.",
                       "Warn that the privacy trade-off is real and will come up."],
      minutes="25 min for the section")

# ------------------------------------------------- inji web arch
s, y = slide("Inji Web architecture", kicker="Backend-for-frontend",
             sub="A React frontend that is deliberately stateless, with Mimoto doing everything that needs a secret or a key.")
# diagram
bx = [ML, ML + 4.35, ML + 8.70]
names = [("Browser — Inji Web", ["React + TypeScript", "Tailwind, i18next", "Redux for UI state",
                                 "pages/, components/, hooks/", "env.config.js at runtime",
                                 "Holds NO credential, NO key"], C['accent'], C['accent_l']),
         ("Mimoto — the BFF", ["Session per logged-in user", "Wallet created with a PIN",
                               "AES-256-GCM credential store", "Runs OpenID4VCI and OpenID4VP",
                               "Issuer catalogue + trusted verifiers", "PDF rendering"], C['violet'], C['violet_l']),
         ("Outside world", ["Issuer well-known + credential endpoint", "Authorization server (eSignet, OIDC, Google)",
                            "Verifier response_uri", "Postgres (durable)", "Redis (sessions, cache)"], C['primary'], C['primary_l'])]
for i, (t, items, col, tint) in enumerate(names):
    w2 = 4.10 if i < 2 else 3.53
    rect(s, bx[i], y, w2, 3.20, fill=tint, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.055)
    rect(s, bx[i], y, w2, 0.07, fill=col)
    _, t2 = tb(s, bx[i] + 0.22, y + 0.24, w2 - 0.44, 0.32)
    para(t2, t, size=12.5, color=col, bold=True, first=True)
    bullets(s, bx[i] + 0.22, y + 0.66, w2 - 0.44, items, size=9.8, gap=0.06, bullet_col=col)
    if i < 2:
        c = line(s, bx[i] + w2 + 0.04, y + 1.6, bx[i + 1] - 0.04, y + 1.6, C['ink2'], 1.5)
        arrowhead(c, tail=True)
_, tf = tb(s, ML + 4.05, y + 1.20, 0.6, 0.3)
para(tf, "HTTPS\nsession cookie", size=7.8, color=C['muted'], align=PP_ALIGN.CENTER, first=True)
yy = y + 3.45
rows = [
 ["Guest journey", "Browse issuers, download a credential, receive it as a **PDF or a file**", "Nothing persisted server-side for the user", "Quick, anonymous, one-off"],
 ["Logged-in journey", "Create a wallet with a **PIN**, download credentials into it, present them", "Credentials stored in Mimoto, encrypted with a PIN-derived key", "Repeat use, presentation support"],
]
table(s, ML, yy, CW, ["Journey", "What the user does", "What is stored", "Why it exists"], rows,
      col_w=[1.8, 4.4, 3.8, 2.2], fsize=9.4, row_h=0.62, head_h=0.34)
notes(s, ["Start with the inclusion rationale, then the architecture.",
          "The BFF pattern is the key idea: the browser is a rendering surface, and every operation that needs a secret, a key or durable state happens in Mimoto. That is why Inji Web can be stateless and still support presentation.",
          "The PIN mechanism deserves detail: on wallet creation Mimoto generates a 256-bit AES key, derives a key from the user's PIN with PBKDF2-HMAC-SHA512 and a random salt, encrypts the AES key with it, and stores salt+IV+ciphertext. On unlock, the PIN reconstructs the key and it lives in the HTTP session — default 30-minute timeout. The raw PIN and the raw AES key are never stored.",
          "Say the consequence plainly: if the user forgets the PIN, the credentials are unrecoverable by design. That is a product and support decision Brazil must plan for.",
          "env.config.js is read at runtime, not build time — so one container image can be deployed to several environments. Useful operational detail."],
      caveats=["Inji Web's OpenID4VP presentation support is currently limited to ldp_vc. SD-JWT VC presentation from the web wallet is on the roadmap.",
               "A 30-minute session holding an unlocked key is a security parameter. Review it against Brazilian requirements rather than accepting the default.",
               "Multiple Mimoto replicas need Redis-backed sessions, or users will appear to be logged out at random."],
      questions=["Can a user move credentials between Wallet and Web? — Not as a supported flow; they are separate holders.",
                 "Can we skip the PIN? — Then Mimoto would hold keys unprotected. No."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- device flows
s, y = slide("The four device journeys in detail", kicker="Same-device, cross-device, handoff",
             sub="Who holds the credential, where the request comes from, and how the user gets back to where they started.")
flows = [
 ("Cross-device", "Verifier on a screen • Wallet on a phone",
  ["Verifier renders a QR containing the request or a `request_uri`.",
   "User scans with Inji Wallet.",
   "Wallet POSTs the `vp_token` to `response_uri`.",
   "**No return redirect** — the verifier's page updates from its own backend."], C['primary']),
 ("Same-device", "Verifier website and Wallet on the same phone",
  ["The web page fires `openid4vp://authorize?…`.",
   "Android intent filter / iOS URL scheme opens the Wallet.",
   "Wallet POSTs the response.",
   "Wallet can then return the user to the browser."], C['accent']),
 ("Web holder", "Inji Web is the wallet, on a laptop",
  ["User is logged in and has unlocked their Mimoto wallet.",
   "The request reaches Inji Web (link or paste).",
   "Mimoto matches credentials and builds the VP.",
   "Currently `ldp_vc` only."], C['violet']),
 ("Web-to-mobile handoff", "Journey starts on the web, finishes on the phone",
  ["Inji Web (or any site) renders a QR.",
   "Inji Wallet scans it and completes the exchange.",
   "Useful when the credential is on the phone but the journey began on a shared PC.",
   "Same protocol as cross-device."], C['green']),
]
bw = (CW - 3 * 0.20) / 4
for i, (t, sub_, steps, col) in enumerate(flows):
    x = ML + i * (bw + 0.20)
    rect(s, x, y, bw, 3.15, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    rect(s, x, y, bw, 0.065, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.22, bw - 0.40, 0.3)
    para(t2, t, size=12.5, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.20, y + 0.55, bw - 0.40, 0.4)
    para(t3, sub_, size=8.8, color=C['muted'], italic=True, first=True, line_spacing=1.2)
    cy = y + 1.00
    for j, stp in enumerate(steps):
        b = rect(s, x + 0.20, cy + 0.02, 0.22, 0.22, fill=col, shape=MSO_SHAPE.OVAL)
        tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
        pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
        rb = pb.add_run(); rb.text = str(j + 1); rb.font.size = Pt(7.5)
        rb.font.bold = True; rb.font.color.rgb = C['white']; rb.font.name = F_SANS
        _, t4 = tb(s, x + 0.50, cy, bw - 0.72, 0.8)
        parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', stp)
        ch = []
        for pt in parts:
            if not pt:
                continue
            if pt.startswith('`'):
                ch.append((pt[1:-1], C['primary'], False, False, F_MONO))
            elif pt.startswith('**'):
                ch.append((pt[2:-2], C['red'], True))
            else:
                ch.append((pt, C['ink2'], False))
        rich(t4, ch, size=9.2, first=True, line_spacing=1.24)
        nl = max(1, -(-len(re.sub(r'[`*]', '', stp)) // 32))
        cy += 0.14 + nl * 0.152
yy = y + 3.40
rows = [
 ["Where the credential lives", "Phone", "Phone", "Mimoto", "Phone"],
 ["How the request arrives", "Camera", "Deep link", "Browser session", "Camera"],
 ["Return path for the user", "!!None — verifier polls", "++Deep link back to browser", "++Same page", "!!None"],
 ["Main configuration risk", "Verifier not in trusted list", "Intent filter / URL scheme", "CORS and session cookies", "QR payload size"],
]
table(s, ML, yy, CW, ["", "Cross-device", "Same-device", "Web holder", "Handoff"], rows,
      col_w=[3.0, 2.4, 2.4, 2.2, 2.2], fsize=9.3, row_h=0.36, head_h=0.34)
notes(s, ["The bottom table is the summary people will photograph.",
          "Row 3 is the operational surprise: in two of the four journeys there is no way to send the user back, so the verifier must drive its own UI update. Verifier teams that assume a redirect will build something that hangs forever.",
          "Row 4 gives each journey its own first-suspect when something fails. Use it in the troubleshooting section.",
          "For Brazil: decide which journeys are in scope for phase one. Supporting all four at launch multiplies the test matrix by four."],
      caveats=["QR payload size is a real limit in the handoff journey. Use request_uri rather than embedding a large request by value.",
               "CORS and cookie SameSite settings are the classic Inji Web failure. Covered in troubleshooting."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- demo 6
demo_slide(8, "The Inji Web journey, end to end", "6 minutes",
  ["Inji Web and Mimoto running (`docker-compose` brings up the full stack).",
   "`env.config.js` pointing `MIMOTO_URL` at your Mimoto.",
   "An OIDC login configured, or Google login credentials.",
   "Browser devtools open on the network tab."],
  ["Home page in Portuguese if you switch the language.",
   "Guest: pick an issuer, authenticate, receive the credential as a file.",
   "Logged in: create a wallet with a PIN, download into it, list it, open it.",
   "Lock the session and unlock it again with the PIN."],
  ["Every action is a call to Mimoto: `/v2/issuers`, `/issuers/{id}/configuration`, `/wallets`, `/wallets/{id}/unlock`, `/wallets/{id}/credentials`.",
   "The browser never sees a private key or a plaintext credential store.",
   "Unlock derives the AES key from the PIN and puts it in the HTTP session.",
   "The Portuguese strings come from `src/locales/pt.json` — already in the repo."],
  fail="If login works but credential listing 401s, look at cookies: `credentials: 'include'` on the frontend, and `SameSite` / domain settings on Mimoto's session cookie.")
notes(prs.slides[-1],
      ["Show the network tab throughout. It makes the BFF pattern self-evident.",
       "Switch the language to Portuguese live — pt.json already ships in the repo with a full translation. That is a genuinely encouraging fact for the Brazil team and worth showing rather than telling.",
       "Demonstrate lock/unlock so people understand the session-bound key."],
      caveats=["Do not use a real PIN you use elsewhere, even in a demo.",
               "Guest journey and logged-in journey have different data footprints; say which one you are demonstrating."],
      minutes="6 min")

# =================================================================== SECTION 10
section("Security architecture and key resolution", "25 min",
        "The threat model, the attacks that actually happen, the mitigations that actually work — and the key-resolution failures that eat integration weeks.",
        ["Threat model and assets",
         "Attack → mitigation table",
         "Malicious QR, token theft, replay",
         "Compromised verifier and issuer endpoints",
         "kid, JWKS, DID and metadata resolution",
         "What happens when resolution fails"], highlight=('issuer', 'wallet', 'verifier'), num="10")
notes(prs.slides[-1], ["Tell the room this section is deliberately adversarial. Invite them to attack the design out loud.",
                       "If there is a security team in the organisation, this is the section to invite them to."],
      minutes="25 min for the section")

# ------------------------------------------------- threat model
s, y = slide("Threat model: what is worth stealing", kicker="Assets and adversaries",
             sub="Start from the assets. The mitigations follow from what you are protecting and from whom.")
assets = [
 ("The holder's private key", "Lets an attacker present as the citizen, forever.",
  "Hardware keystore, device authentication, attestation. Never exportable.", C['red']),
 ("Stored credentials", "Personal data at rest — on the phone, or in Mimoto's database for Web users.",
  "Encryption at rest, HMAC integrity check, PIN-derived key wrapping, short sessions.", C['amber']),
 ("Access tokens in flight", "A stolen bearer token can fetch a credential in the citizen's name.",
  "TLS, short lifetimes, single-use codes. **DPoP would bind them — not implemented today.**", C['violet']),
 ("The issuer's signing key", "Total compromise: an attacker can mint credentials.",
  "HSM, separation of duties, key rotation with overlap, certificate transparency of a sort.", C['primary']),
 ("The citizen's attention", "Most practical attacks are social: a QR that looks official, a page that looks like gov.br.",
  "Honest consent screens, verifier identity shown clearly, trusted-verifier lists.", C['accent']),
]
for i, (a, why, mit, col) in enumerate(assets):
    yy = y + i * 0.92
    rect(s, ML, yy, CW, 0.82, fill=C['surf'] if i % 2 == 0 else C['white'],
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
    rect(s, ML, yy, 0.055, 0.82, fill=col)
    _, t2 = tb(s, ML + 0.22, yy + 0.10, 2.9, 0.6)
    para(t2, a, size=11, color=col, bold=True, first=True, line_spacing=1.12)
    _, t3 = tb(s, ML + 3.25, yy + 0.10, 4.1, 0.65)
    para(t3, why, size=9.4, color=C['ink2'], first=True, line_spacing=1.24)
    _, t4 = tb(s, ML + 7.55, yy + 0.10, CW - 7.75, 0.65)
    parts = re.split(r'(\*\*[^*]+\*\*)', mit)
    rich(t4, [((pt[2:-2], C['red'], True) if pt.startswith('**') else (pt, C['muted'], False))
              for pt in parts if pt], size=9.4, first=True, line_spacing=1.24)
_, tf = tb(s, ML + 3.25, y - 0.26, 4.1, 0.24)
para(tf, "WHY AN ATTACKER WANTS IT", size=8.2, color=C['muted'], bold=True, first=True)
_, tf = tb(s, ML + 7.55, y - 0.26, 4.0, 0.24)
para(tf, "WHAT ACTUALLY PROTECTS IT", size=8.2, color=C['muted'], bold=True, first=True)
_, tf = tb(s, ML + 0.22, y - 0.26, 2.9, 0.24)
para(tf, "ASSET", size=8.2, color=C['muted'], bold=True, first=True)
yy = y + 4.75
callout(s, ML, yy, CW, "Note the last row. In deployed wallet systems the most successful attacks are **not cryptographic**. They are a convincing QR code in a public place and a consent screen the user does not read. Design the consent screen as a security control, because it is one.", kind='warn', size=10.5)
notes(s, ["Work down the asset list and ask the room who owns the mitigation for each. The answers reveal gaps in the delivery plan.",
          "Row 3 is where the DPoP conversation from section 4 pays off. Be precise: today the tokens are bearer tokens, so TLS and short lifetimes are the whole defence in transit.",
          "Row 4 belongs to the issuer programme, not to the wallet team, but the wallet team suffers the consequences. Make sure someone in Brazil owns issuer key management explicitly.",
          "Spend real time on row 5. Show the consent screen again if you can. Ask whether a citizen reading it would understand who is asking and for what."],
      caveats=["Threat modelling is not a one-off. Redo it when the format changes, when a new journey is added, and before go-live.",
               "Device loss is not on this list because it is a recovery problem, not an attack — but it needs an owner too."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- attacks
s, y = slide("Attacks and mitigations", kicker="Concrete scenarios",
             sub="Each row is something that has happened, somewhere, to somebody. The middle column is what goes wrong; the right column is what you do about it.")
rows = [
 ["**Malicious QR code**", "A poster in a bus station encodes a verifier request from an attacker, asking for everything.",
  "Trusted-verifier list with `shouldValidateClient = true`; show verifier identity on the consent screen; never auto-submit a scan."],
 ["**Deep-link hijack**", "A malicious app registers `openid4vp://` or the OAuth redirect scheme and intercepts the callback.",
  "PKCE makes a stolen authorization code useless. Prefer App Links / Universal Links, which are domain-verified."],
 ["**Token theft**", "An access token is captured at a TLS-terminating proxy and replayed to the credential endpoint.",
  "Short token lifetimes, TLS everywhere, minimise hops. DPoP is the structural fix — raise it as a requirement."],
 ["**Presentation replay**", "A `vp_token` captured at verifier A is replayed at verifier B.",
  "The holder signs over the verifier's `nonce` and `aud`. Verifiers MUST check both — a verifier that skips this defeats the design."],
 ["**Compromised verifier**", "A legitimate verifier is breached and starts over-asking for claims.",
  "Selective disclosure limits the blast radius; consent screens expose over-asking; audit which verifiers ask for what."],
 ["**Rogue issuer endpoint**", "DNS is poisoned and issuer metadata is served by an attacker.",
  "The credential must still carry a valid signature from a key you trust. Metadata over TLS; pin roots; monitor key endpoints."],
 ["**Stolen or lost device**", "The handset is taken with credentials on it.",
  "Device authentication gates key use; credentials encrypted at rest; plan a revoke-and-reissue path."],
 ["**Metadata / key endpoint outage**", "JWKS is down, so verification fails and users cannot download or present.",
  "Cache keys aggressively; publish through resilient infrastructure; monitor as a production dependency, not a static file."],
 ["**Over-collection by design**", "A `presentation_definition` asks for the full credential when one claim would do.",
  "Governance, not code: review verifier requests. Format choice matters — only SD-JWT VC and mDoc can actually withhold."],
]
table(s, ML, y, CW, ["Attack", "What goes wrong", "Mitigation"], rows,
      col_w=[2.2, 4.6, 5.4], fsize=9.2, row_h=0.55, head_h=0.34)
notes(s, ["Do not read all nine. Pick three the room will actually face and go deep.",
          "The malicious QR row is the one to dwell on for Brazil — public QR codes are everywhere and citizens are trained to scan them. The trusted-verifier list is a real control, and the default in the shipped sample config (allow_unsigned_request: true) is the wrong setting for production.",
          "The presentation replay row is where you can test whether the room absorbed section 8. Ask them which two fields matter. Answer: nonce and aud.",
          "The last row is a governance point. No amount of protocol prevents a verifier asking for too much — only a format that supports withholding, plus a review process, does."],
      caveats=["Mitigations here assume both ends behave. A verifier you do not control may skip checks; you cannot fix that from the wallet.",
               "Revocation is listed as a mitigation for device loss, but Inji Wallet does not perform revocation checking today — the verifier side must."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- key resolution
s, y = slide("Issuer key resolution — the integration time-sink", kicker="kid, JWKS, DID, metadata",
             sub="A perfectly valid credential whose key cannot be found is indistinguishable from a forgery. Plan key publication like a product.")
# resolution paths, compact
_, tf = tb(s, ML, y, CW, 0.26)
para(tf, "THE CREDENTIAL ARRIVES  →  vc-verifier PICKS A RESOLVER FROM THE HEADER  →  KEY  →  SIGNATURE CHECK", size=8.6, color=C['muted'], bold=True, first=True)
resolvers = [
 ("did:web", "Derive an HTTPS URL from the DID, fetch the DID document, pick the method named by `kid`.", C['primary']),
 ("did:key / did:jwk", "The key is encoded **inside** the identifier. No network call, no outage risk.", C['accent']),
 ("HTTPS / JWKS", "Fetch the verification-method URL or a JWKS document and select by `kid`.", C['violet']),
 ("x5c (X.509)", "Validate the certificate chain in the JWS header up to a trusted root. **Inji's path for SD-JWT VC today.**", C['green']),
]
rw = (CW - 3 * 0.18) / 4
for i, (t, d, col) in enumerate(resolvers):
    x = ML + i * (rw + 0.18)
    rect(s, x, y + 0.34, rw, 1.32, fill=C['surf'], line=col, lw=1.2,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.07)
    _, t2 = tb(s, x + 0.18, y + 0.48, rw - 0.36, 0.28)
    para(t2, t, size=11, color=col, bold=True, font=F_MONO, first=True)
    _, t3 = tb(s, x + 0.18, y + 0.80, rw - 0.36, 0.8)
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', d)
    ch = []
    for pt in parts:
        if not pt:
            continue
        if pt.startswith('`'):
            ch.append((pt[1:-1], col, False, False, F_MONO))
        elif pt.startswith('**'):
            ch.append((pt[2:-2], C['ink'], True))
        else:
            ch.append((pt, C['muted'], False))
    rich(t3, ch, size=9.2, first=True, line_spacing=1.25)
yy = y + 2.00
rows = [
 ["No `kid` in the header", "The resolver cannot choose among several published keys", "Verification fails or picks wrong", "Always publish and always send `kid`"],
 ["`kid` not found at the source", "Key rotated and the old one was removed", "Every credential signed before rotation breaks", "Keep retired keys published for at least one credential lifetime"],
 ["DID document unreachable", "`did:web` host down, DNS, or a redirect the resolver will not follow", "Intermittent, environment-specific failures", "Treat the DID document as a production endpoint with SLA and monitoring"],
 ["JWKS behind a redirect or WAF", "Resolver gets HTML or a 403 instead of JSON", "Confusing parse errors", "Serve key material from a path with no redirects and no bot protection"],
 ["`alg` mismatch", "Issuer signs with an algorithm the verifier does not accept", "Rejected before any network call", "Agree the algorithm set in the interface contract, in writing"],
 ["SD-JWT with no `x5c` and no supported metadata path", "Inji's `vc-verifier` resolves `vc+sd-jwt` issuer keys from X.509 today; JWT VC Issuer Metadata is not yet supported", "Cannot verify at all", "Publish an X.509 chain for SD-JWT VC, and publish the well-known document too for other wallets"],
]
table(s, ML, yy, CW, ["Failure", "Root cause", "What you see", "What to do"], rows,
      col_w=[2.6, 4.0, 2.8, 2.8], fsize=8.9, row_h=0.43, head_h=0.32)
notes(s, ["The four resolver paths at the top are the whole mechanism; the table below is where the time goes.",
          "Row 2 is the one that bites eighteen months into a programme, long after the launch team has moved on. Key rotation without overlap breaks every credential ever issued with the old key. Write the overlap policy down now.",
          "Row 4 is comically common: a well-meaning ops team puts the JWKS behind a WAF that challenges non-browser clients, and every wallet in the country fails to verify.",
          "Row 6 is the Inji-specific one, and it is the most important planning item on this slide for Brazil. If you go SD-JWT VC, plan an X.509 publication path for Inji, and publish the well-known jwt-vc-issuer document as well so other wallets can interoperate. Doing both costs little and buys a lot.",
          "Point out that vc-verifier supports did:web, did:key, did:jwk and HTTPS resolvers — which is the well-trodden path for ldp_vc."],
      caveats=["Key resolution happens at download time in the wallet and again at presentation time in the verifier. Both need to work, from different networks.",
               "Caching keys improves resilience but delays rotation. Decide the cache TTL deliberately."],
      questions=["How long should the overlap be? — At least the maximum credential validity period, plus a margin."],
      minutes="8 min")
footer(s)

# =================================================================== SECTION 11
section("Configuration, deployment and the code", "30 min",
        "Everything between a working demo and a running service: what to configure, how to deploy it, and how to find your way around the repositories.",
        ["Configuration versus customisation",
         "The configuration surface, component by component",
         "Localisation, branding, pt-BR",
         "Deployment topology and build pipelines",
         "Repository walkthrough",
         "Tracing a request through the code"], highlight=('mimoto', 'wallet', 'web'), num="11")
notes(prs.slides[-1], ["This section is for the people who will operate the system. If the room is mostly protocol people, move faster here.",
                       "The configuration-versus-customisation slide is the one that protects the programme's long-term cost."],
      minutes="30 min for the section")

# ------------------------------------------------- config surface
s, y = slide("The configuration surface", kicker="What you set, and where",
             sub="If you can change it here, you do not need a code change — and you do not need an app store release.")
rows = [
 ["**Inji Wallet**", "`.env` / `.env.local`", "`MIMOTO_HOST`, `ESIGNET_HOST`, `OBSRV_HOST`, `APPLICATION_THEME`", "Rebuild required"],
 ["", "`android/app/build.gradle` flavours", "Application id, app name, icons, redirect scheme", "Rebuild required"],
 ["", "`AndroidManifest.xml` / `Info.plist`", "Intent filters, URL schemes, permissions, associated domains", "Rebuild required"],
 ["", "`locales/*.json`", "UI language strings — add `pt-BR`", "Rebuild required"],
 ["**Inji Web**", "`public/env.config.js`", "`MIMOTO_URL`, `DEFAULT_LANG`, `DEFAULT_THEME`, `DEFAULT_TITLE`, `IGNORED_ISSUER_IDS`", "++Runtime — no rebuild"],
 ["", "`src/locales/*.json`", "UI strings; `pt.json` already ships in the repository", "Rebuild required"],
 ["", "Tailwind theme + assets", "Colours, fonts, logos", "Rebuild required"],
 ["**Mimoto**", "`mimoto-issuers-config.json`", "Which issuers exist, their hosts, client ids, redirect URIs, display", "++Restart or cache TTL"],
 ["", "`mimoto-trusted-verifiers.json`", "Which verifiers the wallet will talk to, their JWKS and response URIs", "++Restart or cache TTL"],
 ["", "`mimoto-default.properties`", "Datasource, cache TTLs, session timeout, download timeouts, partner keys", "Restart"],
 ["**Issuer**", "Credential issuer metadata", "Formats, claims, **display labels and field order, per locale**", "++Live, subject to Mimoto's cache"],
]
_tb_bottom = table(s, ML, y, CW, ["Component", "Where", "What you control", "Takes effect"], rows,
      col_w=[1.8, 3.4, 5.4, 2.4], fsize=9.1, row_h=0.375, head_h=0.34)
yy = _tb_bottom + 0.16
callout(s, ML, yy, CW, "Read the right-hand column as a **release-speed map**. Anything that says 'rebuild required' for the Wallet means an app store cycle. Push as much as you can into issuer metadata, Mimoto configuration and `env.config.js` — those change in minutes, not weeks.", kind='tip', size=10.4)
notes(s, ["The right-hand column is the strategic content. In a national programme, mobile release cadence is the constraint that hurts most.",
          "The last row is the one teams forget: credential labels, ordering and localisation live in issuer metadata and can change without touching any Inji component. Design for that from day one.",
          "IGNORED_ISSUER_IDS in env.config.js is a useful operational lever — it lets you hide an issuer from Inji Web without changing Mimoto's catalogue.",
          "Point out that pt.json already exists in inji-web. Brazil starts from a translated base, not from zero."],
      caveats=["'Runtime, no rebuild' for env.config.js assumes your deployment mounts or rewrites that file. Confirm your container pipeline actually does so.",
               "Cache TTLs mean issuer metadata changes are not instant. Know the number before you promise a turnaround time."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- localisation / branding
s, y = slide("Localisation, branding and Portuguese", kicker="pt-BR",
             sub="Three separate localisation surfaces. Missing one of them produces a half-translated app.")
surfaces = [
 ("1 — Application chrome", "Buttons, menus, errors, onboarding.",
  ["Inji Web: `src/locales/pt.json` — **already present and complete** in the repository.",
   "Inji Wallet: `locales/` plus `i18n.ts`; `expo-localization` picks the device language.",
   "Owned by: the Inji delivery team."], C['accent']),
 ("2 — Credential content", "Field labels, credential name, the order fields appear in.",
  ["Comes from the **issuer's** metadata: `display[{name, locale}]` and the `order` property.",
   "Set `locale: \"pt-BR\"` entries alongside any others.",
   "Owned by: whoever operates the issuer."], C['primary']),
 ("3 — Brand and theme", "Colours, logos, fonts, app name, icons.",
  ["Wallet: `APPLICATION_THEME`, product flavours in Gradle, asset replacement.",
   "Web: Tailwind theme, `DEFAULT_TITLE`, `DEFAULT_FAVICON`, `DEFAULT_FONT_URL`.",
   "Owned by: the programme's design authority."], C['violet']),
]
for i, (t, d, items, col) in enumerate(surfaces):
    x = ML + i * (CW / 3 + 0.08)
    wid = CW / 3 - 0.11
    rect(s, x, y, wid, 3.05, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    rect(s, x, y, wid, 0.065, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.22, wid - 0.40, 0.3)
    para(t2, t, size=12, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.20, y + 0.56, wid - 0.40, 0.3)
    para(t3, d, size=9.2, color=C['muted'], italic=True, first=True)
    bullets(s, x + 0.20, y + 0.92, wid - 0.40, items, size=9.7, gap=0.07, bullet_col=col)
yy = y + 3.30
c1 = callout(s, ML, yy, 5.95, "Other languages already in `inji-web`: `en`, `pt`, `fr`, `ar`, `hi`, `kn`, `ta`. Portuguese is not a port — it is a starting point you refine.", kind='good', size=10.3)
callout(s, ML + 6.28, yy, 5.95, "The half-translated trap: app chrome in Portuguese, credential fields in English, because nobody told the issuer team about surface 2.", kind='warn', size=10.3)
notes(s, ["Make the three-surface point explicitly. It is the single most useful thing on this slide, because the failure it prevents is embarrassing and very visible.",
          "Surface 2 is owned by a different team than surface 1 in almost every programme. Name the owner in the room today.",
          "Portuguese in inji-web is already a full translation, done by the community. Show it in the demo. It changes the tone of the localisation conversation from 'a big task' to 'a review task'.",
          "Brazilian Portuguese versus European Portuguese: the existing pt.json will need review. Decide whether to use pt or pt-BR as the locale code and be consistent across all three surfaces."],
      caveats=["Right-to-left is already handled for Arabic; if Brazil ever adds another script, the plumbing exists.",
               "Date, number and name formatting are separate from string translation. Check them explicitly."],
      minutes="5 min")
footer(s)

# ------------------------------------------------- deployment
s, y = slide("Deployment topology and build pipelines", kicker="Running it for real",
             sub="Four deliverables with four very different release cadences. Plan around the slowest one.")
rows = [
 ["**Inji Wallet — Android**", "Gradle, Java 17, min SDK 24, target SDK 35; product flavours give you distinct app ids",
  "Play Store review", "Signing keys in a controlled pipeline; flavour per environment; never ship a debug build"],
 ["**Inji Wallet — iOS**", "Xcode 15+, deployment target 14.0, CocoaPods",
  "App Store review", "Provisioning profiles, associated domains if you use Universal Links"],
 ["**Inji Web**", "Node 18, React build, Docker image; `env.config.js` read at runtime",
  "++Minutes", "One image, many environments; Helm chart in the repo"],
 ["**Mimoto**", "Java 21, Spring Boot, Docker; Postgres + Redis; Helm chart in the repo",
  "++Minutes", "Redis is required for more than one replica; DB migration scripts in `db_scripts/`"],
]
_tb_bottom = table(s, ML, y, CW, ["Deliverable", "Build", "Release latency", "What to get right"], rows,
      col_w=[2.2, 4.6, 1.8, 3.6], fsize=9.2, row_h=0.62, head_h=0.34)
yy = _tb_bottom + 0.22
card(s, ML, yy, 3.90, 2.45, "Environment separation", [
 "One Mimoto, one Postgres, one Redis **per environment**. Configuration is deployment-wide.",
 "Wallet flavours give you a dev, QA and production app side by side on one device.",
 "Issuer and verifier catalogues differ per environment — keep them in version control.",
], accent=C['primary'], tint=C['primary_l'], size=9.8)
card(s, ML + 4.15, yy, 3.90, 2.45, "Network, certificates, domains", [
 "Egress from Mimoto to: issuer well-known, token endpoint, credential endpoint, verifier `response_uri`.",
 "The **phone** must also reach the issuer directly — not just your cluster.",
 "Public TLS everywhere; no self-signed certificates on anything a phone touches.",
 "Stable domains for issuer metadata and key endpoints. Changing them invalidates trust.",
], accent=C['amber'], tint=C['amber_l'], size=9.8)
card(s, ML + 8.32, yy, 3.91, 2.45, "Observability", [
 "Correlate with the `traceabilityId` that `inji-vci-client` and `inji-openid4vp` are constructed with.",
 "Log the structured error codes (`VCI-00x`), never the credential contents.",
 "Telemetry from the Wallet goes to the configured Obsrv endpoint.",
 "Alert on: issuer well-known availability, key endpoint availability, token endpoint latency.",
], accent=C['green'], tint=C['green_l'], size=9.8)
notes(s, ["The release-latency column is the planning message. A wallet bug is a two-week fix at best because of store review; a Mimoto or issuer-metadata change is minutes. Architect accordingly — this is the operational justification for the configuration-surface slide.",
          "The 'phone must reach the issuer directly' point catches teams whose network design assumes everything goes through the cluster. The credential request is a direct call from the handset.",
          "traceabilityId is genuinely useful: both libraries take one at construction, so you can correlate a user's journey across the wallet, Mimoto and the issuer if everyone logs it. Agree the propagation convention early.",
          "Alerting on the issuer's key endpoint is unusual but essential — it is a hard dependency for verification and it is usually owned by a team that does not know that."],
      caveats=["Helm charts exist for Inji Web and Mimoto in their repositories; treat them as a starting point, not a production-hardened deployment.",
               "Database migration scripts live in mimoto/db_scripts and db_upgrade_script. Version upgrades are not always drop-in.",
               "Do not ship a wallet build with a test issuer catalogue baked into its MIMOTO_HOST."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- dev walkthrough
s, y = slide("Developer walkthrough: getting it running", kicker="Hands on the code",
             sub="The fastest path from a clean laptop to a working stack, plus where to put a breakpoint.")
codebox(s, ML, y, 3.95, 2.60, [
 '# Mimoto + Postgres + Redis + Web',
 'git clone \\',
 '  github.com/mosip/inji-web',
 'cd inji-web/docker-compose',
 'docker-compose up',
 '',
 '# Inji Web alone (Node 18)',
 'cd inji-web/inji-web',
 'npm install && npm start',
 '#  -> http://localhost:3004',
], label="RUN THE BACKEND AND WEB", size=8.6)
codebox(s, ML + 4.20, y, 3.95, 2.60, [
 '# Inji Wallet (Node 18, RN 0.74, Expo 51)',
 'git clone \\',
 '  github.com/mosip/inji-wallet',
 'cd inji-wallet',
 'cp .env .env.local      # set MIMOTO_HOST',
 'npm install',
 '',
 'npx react-native run-android',
 '#  iOS: cd ios && pod install, then run-ios',
], label="RUN THE WALLET", size=8.6)
codebox(s, ML + 8.40, y, 3.83, 2.60, [
 '# Mimoto from source (JDK 21)',
 'git clone github.com/mosip/mimoto',
 'cd mimoto',
 'mvn clean install -DskipTests',
 '',
 '# then set, in application-local.properties:',
 '#   spring.datasource.*',
 '#   mimoto-issuers-config.json',
 '#   mimoto-trusted-verifiers.json',
], label="RUN MIMOTO", size=8.6)
yy = y + 2.90
rows = [
 ["Trace an **issuance** request", "`machines/Issuers/` → `shared/vciClient/VciClient.ts` → `InjiVciClientModule` (native) → `inji-vci-client`",
  "Breakpoint on the `getProofJwt` callback: you see the `c_nonce` and the algorithms the issuer will accept"],
 ["Trace a **presentation** request", "`machines/openID4VP/openID4VPServices.ts` → `shared/openID4VP/OpenID4VP.ts` → `InjiOpenID4VPModule` → `inji-openid4vp`",
  "Breakpoint on `constructUnsignedVPToken`: you see exactly what will be signed"],
 ["Add or modify an **issuer**", "`mimoto/src/main/resources/mimoto-issuers-config.json`, then restart or wait out the cache",
  "Check `GET /v2/issuers` before blaming the app"],
 ["Change one **configuration** item", "`inji-web/public/env.config.js` for Web; `.env.local` for Wallet; `mimoto-default.properties` for Mimoto",
  "Web takes effect on reload; Wallet needs a rebuild"],
 ["Debug a **failed** request", "Wallet: logcat / Flipper. Mimoto: application log + the structured error. Issuer: its own log.",
  "Start by deciding which of the three owns the failure — that is the triage tree on the next slide"],
]
table(s, ML, yy, CW, ["Task", "Path through the code", "Where to put the breakpoint"], rows,
      col_w=[2.5, 5.6, 4.3], fsize=9.0, row_h=0.50, head_h=0.32)
notes(s, ["If there are developers in the room with laptops, have them start docker-compose now — it takes several minutes and they can follow the rest of the section while it pulls.",
          "The two trace rows are the most valuable thing on this slide. The pattern is identical for both protocols: machine → shared adapter → native module → library. Once you know that shape you can find anything.",
          "The breakpoint suggestions are chosen deliberately: getProofJwt and constructUnsignedVPToken are the two moments where the app is about to sign something, so they are where the interesting state is.",
          "Row 3's advice — check GET /v2/issuers before blaming the app — saves a whole class of wasted debugging."],
      caveats=["Node 18 specifically. Newer Node versions break the React Native 0.74 toolchain in ways that are hard to diagnose.",
               "iOS requires a Mac with Xcode 15+; plan for that in the team's equipment.",
               "docker-compose brings up a demo configuration, not a secure one. Never expose it."],
      minutes="8 min")
footer(s)

# =================================================================== SECTION 12
section("Troubleshooting and interoperability", "30 min",
        "The failure catalogue, the triage tree, and what it takes to work with issuers and verifiers you did not build.",
        ["Triage: which component owns this?",
         "Issuance failures",
         "Crypto and format failures",
         "Presentation and platform failures",
         "What to log and what to look at",
         "Interoperability and draft versions"], highlight=('issuer', 'mimoto', 'wallet', 'web', 'verifier'), num="12")
notes(prs.slides[-1], ["Tell the room this is the section they will come back to. The tables are reference material, not lecture material.",
                       "Invite people to add their own failures to the catalogue during the session."],
      minutes="30 min for the section")

# ------------------------------------------------- triage tree
s, y = slide("Triage: who owns this failure?", kicker="Decision tree",
             sub="Four questions, asked in order. Most failures are localised within two minutes.")
qs = [
 ("Did anything reach the network at all?",
  "No → the failure is **inside the app**: deep link not registered, QR not parsed, permission denied, or a crash. Look at logcat / the browser console.",
  "Yes → go to question 2.", C['primary']),
 ("Did the issuer or verifier answer?",
  "No → **connectivity or DNS**: the phone's network, egress rules, a certificate the device does not trust, or a host that only resolves inside your cluster.",
  "Yes, with an HTTP error → read the body; the error usually names the party at fault. Go to question 3.", C['accent']),
 ("Is the message well formed for the version in use?",
  "No → **contract mismatch**: draft 11 versus 13, draft 21 versus 23, `vc+sd-jwt` versus `dc+sd-jwt`, a missing `kid`, an unexpected `alg`.",
  "Yes → go to question 4.", C['violet']),
 ("Does the cryptography check out?",
  "No → **key resolution or signature**: key not found, wrong `kid`, rotated key removed, chain not trusted, digest mismatch.",
  "Yes, and it still fails → **policy**: the verifier does not accept this issuer or this credential type. Not a bug.", C['amber']),
]
for i, (q, a1, a2, col) in enumerate(qs):
    yy = y + i * 1.18
    b = rect(s, ML, yy, 0.44, 0.44, fill=col, shape=MSO_SHAPE.OVAL)
    tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run(); rb.text = str(i + 1); rb.font.size = Pt(14); rb.font.bold = True
    rb.font.color.rgb = C['white']; rb.font.name = F_SANS
    _, t2 = tb(s, ML + 0.62, yy + 0.04, 3.55, 0.8)
    para(t2, q, size=12, color=C['ink'], bold=True, first=True, line_spacing=1.15)
    for j, a in enumerate((a1, a2)):
        x = ML + 4.35 + j * 4.05
        rect(s, x, yy - 0.02, 3.85, 1.00, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.09)
        _, t3 = tb(s, x + 0.18, yy + 0.08, 3.50, 0.85)
        parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', a)
        ch = []
        for pt in parts:
            if not pt:
                continue
            if pt.startswith('`'):
                ch.append((pt[1:-1], C['primary'], False, False, F_MONO))
            elif pt.startswith('**'):
                ch.append((pt[2:-2], col, True))
            else:
                ch.append((pt, C['ink2'], False))
        rich(t3, ch, size=9.3, first=True, line_spacing=1.25)
    if i < 3:
        line(s, ML + 0.22, yy + 0.46, ML + 0.22, yy + 1.16, C['line'], 1.2, dash=2)
yy = y + 4.85
callout(s, ML, yy, CW, "The discipline this builds: **name the owner before you debug.** A developer who spends an hour in the wallet on a problem the issuer caused has lost the hour and learned nothing.", kind='tip', size=10.6)
notes(s, ["Teach this as a habit, not a diagram. Walk through one real failure with the room using the four questions.",
          "Question 1 is startlingly effective. 'Did anything leave the phone?' separates OS integration problems from protocol problems instantly, and OS integration problems are the majority in the first weeks.",
          "Question 3 is where draft skew shows up. Keep a written record of which draft every partner is on.",
          "Question 4's second branch matters: a policy rejection is not a bug. Teams burn days trying to 'fix' a verifier that is correctly refusing an issuer it does not trust."],
      caveats=["Some failures span two owners — for example, a metadata document that is valid but cached stale. The tree still helps: it tells you where to look first.",
               "Always capture the traceabilityId. Without it, cross-component correlation is guesswork."],
      minutes="6 min")
footer(s)

# ------------------------------------------------- failures 1
s, y = slide("Failure catalogue 1 — issuance", kicker="Troubleshooting",
             sub="Symptom, most likely cause, who owns it, and where to look.")
rows = [
 ["Credential Offer QR does nothing", "Scheme not registered, or the payload is not a recognised offer", "Wallet", "Device logs; confirm the scheme in `AndroidManifest.xml` / `Info.plist`"],
 ["Invalid Credential Offer", "`credential_configuration_ids` does not match the issuer metadata", "Issuer", "Compare the offer against `credential_configurations_supported`"],
 ["Issuer metadata unavailable", "Wrong well-known path, host unreachable from the phone, or a redirect", "Issuer / network", "`curl` the well-known URL from a device network; check Mimoto's cache"],
 ["Empty credential list", "Draft 11 vs 13 metadata shape mismatch", "Issuer", "Look for `credentials_supported` vs `credential_configurations_supported`"],
 ["Authorization redirect fails", "Redirect URI not registered at the AS, or mismatched by one character", "Issuer / config", "Compare all three copies: AS registration, Mimoto issuer config, app manifest"],
 ["Browser closes, nothing happens", "The deep link did not reach the app", "Wallet / OS config", "Test the URI with `adb shell am start -a android.intent.action.VIEW -d …`"],
 ["PKCE mismatch at `/token`", "`code_verifier` lost — a new PKCE session was created mid-flow", "Wallet / library", "Check for process death and re-entry into the flow"],
 ["Token request fails", "Client id or secret wrong, grant type unsupported, or code already used", "AS / Mimoto", "Mimoto's `/get-token/{issuer}` log plus the AS log"],
 ["Bearer vs DPoP mismatch", "The issuer demands `DPoP` but the wallet sends `Bearer`", "Issuer", "Inji sends Bearer today — the issuer must accept it"],
 ["`c_nonce` / nonce failure", "The proof was built with a stale or missing `c_nonce`", "Wallet / issuer", "Confirm `c_nonce` is returned by the token endpoint and echoed in the proof"],
 ["Credential request proof rejected", "Wrong `alg`, missing `aud`, wrong `typ`, or an unsupported binding method", "Wallet / issuer", "Decode the proof JWT; compare against `proof_types_supported`"],
 ["Unsupported credential format", "The wallet does not support the format the issuer returned", "Issuer / wallet", "Compare `format` in the credential request and in issuer metadata"],
 ["Download times out", "Slow credential endpoint versus the configured timeout", "Issuer / config", "`mosip.inji.openId4VCIDownloadVCTimeout`; library `downloadTimeoutInMillis`"],
]
table(s, ML, y, CW, ["Symptom", "Most likely cause", "Owner", "Where to look"], rows,
      col_w=[3.0, 3.9, 1.5, 4.4], fsize=8.7, row_h=0.35, head_h=0.32)
notes(s, ["Reference material. Do not read it. Ask the room which symptoms they have already seen and discuss those.",
          "Row 5 and row 6 together account for a large share of first-week failures. The adb command in row 6 is the fastest way to prove whether a deep link is registered — teach it explicitly.",
          "Row 9 is the honest DPoP note again: if a partner issuer requires DPoP, Inji cannot currently satisfy it. That is a conversation to have before integration starts, not during.",
          "Row 4 is subtle and wastes a lot of time: a draft-11 issuer talking to draft-13 expectations produces an empty list rather than an error."],
      caveats=["Owner column is 'most likely', not 'always'. Use the triage tree to confirm.",
               "Several of these produce the same user-visible message. The error code is what distinguishes them — capture it."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- failures 2
s, y = slide("Failure catalogue 2 — crypto, formats, presentation and platform", kicker="Troubleshooting",
             sub="The second half. These appear later in a project and take longer to diagnose.")
rows = [
 ["Issuer `kid` not found", "Key rotated and removed, or `kid` never published", "Issuer", "Fetch the DID document / JWKS and list the key ids"],
 ["JWKS resolution failure", "Redirect, WAF challenge, or wrong content type", "Issuer / ops", "`curl -v` the JWKS URL from outside your network"],
 ["Credential signature verification fails", "Wrong key, wrong `alg`, or the payload was altered in transit", "Issuer", "`vc-verifier` error code; re-verify the raw credential offline"],
 ["SD-JWT disclosure failure", "Digest not present in `_sd`, or `_sd_alg` unsupported / mismatched", "Issuer", "Recompute the digest of each disclosure and compare to `_sd`"],
 ["mDoc parsing failure", "Malformed CBOR or an unexpected structure", "Issuer", "Decode the CBOR independently; check namespaces and `docType`"],
 ["mDoc issuer authentication fails", "`issuerAuth` COSE signature invalid, or the chain does not reach a trusted root", "Issuer / PKI", "Validate the document signer certificate separately"],
 ["Device authentication fails", "The device key in the MSO does not match the key that signed", "Wallet", "Confirm which key was used; check the keystore alias"],
 ["QR parsing failure", "Unexpected scheme, truncated payload, or a QR too dense to scan", "Verifier", "Decode the QR to text and inspect it; prefer `request_uri`"],
 ["OpenID4VP request validation fails", "client_id scheme mismatch, unsigned request where signing is required, verifier not in the trusted list", "Verifier / config", "`mimoto-trusted-verifiers.json`; `shouldValidateClient`; `allow_unsigned_request`"],
 ["VP generation fails", "No matching credential, or no `cnf` so no key binding is possible", "Wallet", "Check the `presentation_definition` constraints against what is stored"],
 ["Verifier rejects the presentation", "`nonce`/`aud` mismatch, unacceptable issuer, or policy", "Verifier", "Verifier log; confirm it is checking the right `nonce`"],
 ["Web: 401 after login", "Cookies not sent — `credentials: 'include'`, `SameSite`, or a domain mismatch", "Web / Mimoto", "Browser network tab; Mimoto session configuration"],
 ["Web: CORS error", "Origin not allowed by Mimoto, or a preflight failing", "Mimoto", "Response headers on the preflight `OPTIONS`"],
 ["Android-specific failure", "Scheme hijack by another app, network security config blocking a CA, or Keystore constraints", "Wallet / OS", "logcat; check for a chooser dialog; review `network_security_config`"],
 ["iOS-specific failure", "URL scheme not declared, associated domain not verified, Keychain access group wrong", "Wallet / OS", "Console.app; confirm `Info.plist` entries"],
]
table(s, ML, y, CW, ["Symptom", "Most likely cause", "Owner", "Where to look"], rows,
      col_w=[3.2, 4.2, 1.4, 4.0], fsize=8.5, row_h=0.325, head_h=0.32)
notes(s, ["Again: reference material. Pick three and go deep.",
          "The SD-JWT disclosure row is worth demonstrating — recomputing a digest by hand once makes the format permanently clear.",
          "The two Web rows (401 and CORS) cover most Inji Web integration pain. They are boring and they are the truth.",
          "The Android row about a chooser dialog is a security lesson disguised as a bug report: if a chooser appears, another app claims your scheme."],
      caveats=["Do not paste real credentials into online decoders while debugging. Use local tools.",
               "Some of these failures are silent on one platform and loud on the other. Test both."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- interoperability
s, y = slide("Interoperability: working with systems you did not build", kicker="External issuers and verifiers",
             sub="Interoperability is a negotiated agreement, not a property you get for free by using a standard.")
card(s, ML, y, 3.90, 3.05, "Agree these in writing, first", [
 "**Draft versions**: OpenID4VCI 11 or 13; OpenID4VP 21 or 23.",
 "**Format string**: `vc+sd-jwt` or `dc+sd-jwt`; `ldp_vc`; `mso_mdoc`.",
 "**Algorithms**: signing algs for credentials, proofs and key binding.",
 "**Key publication**: `x5c`, JWKS, DID method — and the rotation policy.",
 "**client_id scheme** and whether requests are signed.",
 "**Response mode**: `direct_post` or `direct_post.jwt`, and the encryption algorithms.",
], accent=C['primary'], tint=C['primary_l'], size=9.7)
card(s, ML + 4.15, y, 3.90, 3.05, "Where skew actually bites", [
 "Draft 11 publishes `credentials_supported`; draft 13 publishes `credential_configurations_supported`. A mismatch shows as an **empty list**, not an error.",
 "OpenID4VP draft 21 uses a separate `client_id_scheme`; draft 23 folds it into `client_id`. `inji-openid4vp` infers the draft from its presence.",
 "`vc+sd-jwt` and `dc+sd-jwt` are the same format at different points in the IETF draft's life. Both are supported; agree on one.",
 "Presentation Exchange is being replaced by DCQL in later OpenID4VP drafts. Do not build deep dependencies on the submission shape.",
], accent=C['amber'], tint=C['amber_l'], size=9.7)
card(s, ML + 8.32, y, 3.91, 3.05, "How to test it", [
 "Build a **conformance checklist** from the agreed list and run it before every release on both sides.",
 "Keep a reference issuer and a reference verifier you control, for bisecting failures.",
 "Test with a **second wallet** that is not Inji. If only Inji can read your credentials, you have not achieved interoperability.",
 "Use the OpenID Foundation conformance suites where they cover your profile.",
 "Test key rotation as a scheduled exercise, not as an incident.",
], accent=C['green'], tint=C['green_l'], size=9.7)
yy = y + 3.30
rows = [
 ["Graceful failure", "An unknown format, algorithm or draft should produce a **clear, specific** error — never a crash and never a silent empty screen"],
 ["Capability advertisement", "Inji publishes `walletMetadata`: supported `vp_formats`, `client_id_schemes`, request signing algs, response encryption algs. Verifiers can read it when the request is fetched by reference with `request_uri_method=post`"],
 ["Version negotiation", "There is none in the protocol. It is a deployment agreement, which is why the left-hand card exists"],
]
table(s, ML, yy, CW, ["Principle", "What it means in practice"], rows,
      col_w=[2.4, 9.8], fsize=9.4, row_h=0.52, head_h=0.32)
notes(s, ["Open with the headline: standards make interoperability possible, they do not make it automatic. Every successful integration in this space starts with a written profile agreement.",
          "The empty-list failure in card two is worth a story. It is the most misleading failure mode in OpenID4VCI because nothing is obviously wrong — the wallet just shows no credentials.",
          "The 'test with a second wallet' advice in card three is the single best interoperability investment. It catches assumptions no amount of internal testing will.",
          "walletMetadata in the wallet repo is a real, readable file. Show it: it is the machine-readable version of the left card."],
      caveats=["DCQL will land in later drafts and will change the request shape. Plan for a migration rather than assuming stability.",
               "Conformance suites cover profiles, not your specific credential design. Passing them is necessary, not sufficient."],
      minutes="7 min")
footer(s)

# ------------------------------------------------- demo 8
demo_slide(9, "Break one configuration on purpose, then find it", "8 minutes",
  ["A working end-to-end setup.",
   "Logs visible for Wallet, Mimoto and the issuer at the same time.",
   "The triage tree slide on a second screen.",
   "A volunteer from the room who has not seen the change."],
  ["The facilitator changes **one** thing without telling the room.",
   "The journey fails.",
   "The room works the triage tree out loud: did anything leave the phone? did the server answer? is the message well formed? does the crypto check out?",
   "Someone names the owner, then the field."],
  ["Good things to break, in rising order of difficulty:",
   "1. Change `redirect_uri` in `mimoto-issuers-config.json` by one character.",
   "2. Set the issuer's `enabled` to `false`.",
   "3. Remove the verifier from `mimoto-trusted-verifiers.json`.",
   "4. Point `wellknown_endpoint` at a URL that returns HTML.",
   "5. Change the issuer's signing `kid` without publishing the new key."],
  fail="Break number 5 last. It is the one that teaches the most, because everything looks healthy until the very final verification step — exactly like a real key-rotation incident.")
notes(prs.slides[-1],
      ["This is the most valuable exercise in the day. Protect the time for it.",
       "Do not reveal the change. Let the room drive. Your job is to keep them on the triage tree rather than letting them guess.",
       "After each round, ask: which question in the tree would have got us here fastest? That is the reflection that makes the skill stick.",
       "Break number 5 mirrors a real production incident pattern — rotation without overlap. Land that point explicitly."],
      caveats=["Reset the configuration between rounds or failures will compound and confuse.",
               "Keep rounds short — five minutes each, maximum. Three good rounds beat one long one."],
      minutes="8 min")

# =================================================================== SECTION 13 BRAZIL
section("Brazil: the open technical decisions", "20 min + discussion",
        "This section deliberately contains no answers. These are the decisions that have to be made, the order to make them in, and what each one constrains downstream.",
        ["Credential types and formats",
         "Issuer and authentication systems",
         "Claims, disclosure and binding",
         "Trust framework and key publication",
         "Verifier ecosystem and offline needs",
         "Residency, deployment, customisation"], highlight=('issuer', 'mimoto', 'wallet', 'web', 'verifier'), num="13")
notes(prs.slides[-1],
      ["Say explicitly: this deck makes no assumptions about Brazil's architecture, and the next three slides are questions, not proposals.",
       "Set up the format: capture every answer, and every 'we do not know yet', on a flipchart or a shared document. The unknowns are as valuable as the answers.",
       "Assign an owner to each open question before the session ends. A question with no owner is not a decision, it is a delay."],
      minutes="20 min plus open discussion")

# ------------------------------------------------- brazil Qs 1
s, y = slide("Brazil discussion — credentials, issuers, claims", kicker="Open questions, part 1",
             sub="Work top to bottom. Each answer narrows the next question. Capture owners and dates, not just opinions.")
groups = [
 ("Credentials and formats", [
   "Which credential types will Brazil issue first? Second?",
   "Which format for each — SD-JWT VC, mDoc, JSON-LD, or a mix?",
   "Is one format per credential type acceptable, or must the wallet support several from day one?",
   "Does any credential need to be an mDL conforming to ISO 18013-5?",
 ], C['primary']),
 ("Issuers and authentication", [
   "Which issuer systems already exist, and which will be built?",
   "Will Inji Certify be used, or an existing national issuing platform?",
   "What authenticates the citizen at issuance — gov.br, eSignet, something else?",
   "Which grant type: authorization code, pre-authorized code, or both?",
   "Where will citizens obtain credentials, and will connectivity be reliable there?",
 ], C['accent']),
 ("Claims and disclosure", [
   "Which claims are mandatory in each credential?",
   "Which claims must support selective disclosure?",
   "Which claims must NEVER be disclosed together (a privacy requirement, not a technical one)?",
   "What are the credential validity periods, and what is the re-issuance trigger?",
 ], C['violet']),
]
bw = (CW - 2 * 0.24) / 3
for i, (t, items, col) in enumerate(groups):
    x = ML + i * (bw + 0.24)
    rect(s, x, y, bw, 4.55, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.22, y + 0.24, bw - 0.44, 0.34)
    para(t2, t, size=13, color=col, bold=True, first=True)
    cy = y + 0.78
    for it in items:
        rect(s, x + 0.22, cy + 0.055, 0.16, 0.16, fill=None, line=col, lw=1.3)
        _, t3 = tb(s, x + 0.48, cy, bw - 0.70, 1.0)
        para(t3, it, size=9.9, color=C['ink2'], first=True, line_spacing=1.26)
        nl = max(1, -(-len(it) // 40))
        cy += 0.18 + nl * 0.165
notes(s, ["Facilitate, do not present. Read each question, pause, and let the room argue.",
          "The format question depends on the answers in the third column, not the other way round. If people jump straight to 'SD-JWT or mDoc', redirect them: first say which claims must be withholdable, then the format follows.",
          "The 'never disclosed together' question is one that privacy regulators ask and engineers rarely anticipate. Raise it even if nobody has an answer.",
          "The connectivity question is the one that decides whether the programme works outside major cities. Do not let it be skipped."],
      caveats=["Resist giving your own recommendation too early. The room's own reasoning is what will survive the session.",
               "If a question genuinely cannot be answered today, write down who will answer it and by when."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- brazil Qs 2
s, y = slide("Brazil discussion — trust, verifiers, deployment", kicker="Open questions, part 2",
             sub="These decisions have long lead times. Starting them late is the most common cause of a delayed launch.")
groups = [
 ("Trust and keys", [
   "What trust framework governs who may issue and who may verify?",
   "How will issuer keys be published — X.509 chain, JWKS, DID? (Note what Inji's verifier supports today.)",
   "What is the key rotation policy, and what is the overlap window?",
   "What holder-binding level is required per credential type? Hardware-backed?",
   "Who operates the root of trust, and what is the incident process if it is compromised?",
 ], C['primary']),
 ("Verifiers and journeys", [
   "What verifier ecosystem exists today, and who will build the first verifiers?",
   "Are offline presentations required? Proximity use cases?",
   "Is the browser Digital Credentials API (DC API) needed? (Not supported in the versions reviewed.)",
   "Which web journeys are in scope: same-device, cross-device, Inji Web as holder, handoff?",
   "How will verifiers be onboarded, reviewed and revoked?",
 ], C['accent']),
 ("Deployment and customisation", [
   "What data residency constraints apply — especially to Mimoto's credential store for Inji Web users?",
   "What infrastructure is available: Kubernetes, managed Postgres, managed Redis?",
   "Which components will Brazil customise, and which stay standard?",
   "What localisation and branding are required, and who owns each of the three surfaces?",
   "How will changes be contributed upstream rather than forked?",
 ], C['violet']),
]
bw = (CW - 2 * 0.24) / 3
for i, (t, items, col) in enumerate(groups):
    x = ML + i * (bw + 0.24)
    rect(s, x, y, bw, 4.55, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.22, y + 0.24, bw - 0.44, 0.34)
    para(t2, t, size=13, color=col, bold=True, first=True)
    cy = y + 0.78
    for it in items:
        rect(s, x + 0.22, cy + 0.055, 0.16, 0.16, fill=None, line=col, lw=1.3)
        _, t3 = tb(s, x + 0.48, cy, bw - 0.70, 1.0)
        para(t3, it, size=9.9, color=C['ink2'], first=True, line_spacing=1.26)
        nl = max(1, -(-len(it) // 40))
        cy += 0.18 + nl * 0.165
notes(s, ["The first column has the longest lead time. National PKI decisions take months and block everything downstream.",
          "The residency question in the third column is the one that can change the product choice entirely. If credentials for Inji Web users cannot be held centrally, the browser wallet may not be viable in its current form. That is a big finding, and better discovered today than in month nine.",
          "The DC API question is forward-looking: browsers are adding a native credential-presentation API. It is not supported in the Inji versions reviewed here. If Brazil expects browser-native flows, that is a roadmap conversation with the Inji community.",
          "The last bullet — contributing upstream rather than forking — is a cost decision disguised as a philosophy question. A fork is a permanent tax."],
      caveats=["Do not let 'we will customise it later' pass without a name attached. Customisation debt compounds.",
               "Several of these questions belong to people who are not in the room. Identify them and schedule the conversation."],
      minutes="8 min")
footer(s)

# ------------------------------------------------- brazil decision order
s, y = slide("The order to decide things in", kicker="Sequencing",
             sub="Each decision constrains the ones to its right. Making them out of order causes rework.")
steps = [
 ("1  Use cases and claims", "Which credentials, which claims, which must be withholdable", C['primary']),
 ("2  Format per credential", "Follows directly from disclosure and offline needs", C['accent']),
 ("3  Binding and assurance", "Bound or unbound; hardware-backed or not; which key types", C['violet']),
 ("4  Trust framework and key publication", "Who may issue, who may verify, how keys are published and rotated", C['amber']),
 ("5  Issuer platform and auth", "Certify or bespoke; which authorization server; which grant", C['green']),
 ("6  Journeys and verifiers", "Same-device, cross-device, web, offline; who builds verifiers", C['red']),
 ("7  Deployment and residency", "Where Mimoto runs, what it stores, which environments", C['primary_d']),
]
n = len(steps)
bw = (CW - (n - 1) * 0.16) / n
for i, (t, d, col) in enumerate(steps):
    x = ML + i * (bw + 0.16)
    rect(s, x, y + 0.30, bw, 2.35, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.055)
    rect(s, x, y + 0.30, bw, 0.075, fill=col)
    _, t2 = tb(s, x + 0.14, y + 0.52, bw - 0.28, 0.75)
    para(t2, t, size=10.8, color=col, bold=True, first=True, line_spacing=1.12)
    _, t3 = tb(s, x + 0.14, y + 1.32, bw - 0.28, 1.2)
    para(t3, d, size=9.0, color=C['muted'], first=True, line_spacing=1.26)
    if i < n - 1:
        c = line(s, x + bw + 0.02, y + 1.45, x + bw + 0.14, y + 1.45, C['ink2'], 1.4)
        arrowhead(c, tail=True, size='sm')
yy = y + 3.00
card(s, ML, yy, 5.95, 2.05, "What can start in parallel today", [
 "Standing up a development environment (docker-compose brings the stack up in minutes).",
 "Reviewing and refining the existing `pt.json` translation.",
 "Building a throwaway issuer and verifier to learn against.",
 "Identifying who owns the national key infrastructure conversation.",
], accent=C['green'], tint=C['green_l'], size=10.0)
card(s, ML + 6.28, yy, 5.95, 2.05, "What must not start before its turn", [
 "Branding and UI customisation before the journeys are decided.",
 "Verifier onboarding before the trust framework exists.",
 "Production PKI before the format and binding decisions are made.",
 "Any fork of an Inji repository, ever, before trying configuration first.",
], accent=C['red'], tint=C['red_l'], size=10.0)
notes(s, ["This is the slide the programme manager in the room needs.",
          "Explain the dependency logic: format follows from claims; binding follows from assurance; key publication follows from format; everything else follows from those.",
          "The 'start in parallel' card matters for morale — there is real, useful work available on day one that does not block on any decision.",
          "The last bullet on the right is deliberate. Forking is almost always premature, and it is the decision teams regret most."],
      caveats=["Real programmes never decide in a clean order. The point is to know which decision you are pre-empting when you go out of order, and to record it.",
               "Revisit this ordering after the first pilot — assumptions will have changed."],
      minutes="5 min")
footer(s)

# =================================================================== EXERCISES
STATE['section'] = "Exercises"
s, y = slide("Hands-on exercises", kicker="Do these, in pairs",
             sub="Nine short exercises. Pick the ones that match your role; do exercise 2 and 9 whatever your role.")
ex = [
 ("1", "Identify the components in an issuance flow", "Given a network trace from Demo 1, label every request with the component that served it and the protocol step it belongs to.", "10 min", C['primary']),
 ("2", "Whose failure is this?", "Ten error messages on cards. Sort them into Issuer, Mimoto, Wallet, Web, Verifier. Use the triage tree. **Everyone does this one.**", "10 min", C['red']),
 ("3", "Inspect a DPoP-style proof", "Decode a credential-request proof JWT. Identify `typ`, `alg`, `jwk`, `aud`, `nonce`. Say what each one stops.", "8 min", C['violet']),
 ("4", "Modify an issuer configuration", "Add a new issuer to `mimoto-issuers-config.json`, restart, and see it appear in `GET /v2/issuers` and in the app.", "12 min", C['accent']),
 ("5", "Trace an OpenID4VCI flow in code", "From `machines/Issuers/` to `inji-vci-client`. Put a breakpoint on `getProofJwt` and read the `c_nonce`.", "12 min", C['primary']),
 ("6", "Inspect SD-JWT disclosures", "Split a credential on `~`. Base64url-decode one disclosure. Recompute its SHA-256 and find it in `_sd`.", "10 min", C['green']),
 ("7", "Inspect an mDoc structure", "Decode the base64url CBOR. Find the namespaces, the element digests, the `deviceKey` and the `validityInfo`.", "12 min", C['amber']),
 ("8", "Trace an OpenID4VP request", "From the QR to the POST at `response_uri`. Identify `nonce`, `state`, `client_id_scheme` and the response mode.", "12 min", C['accent']),
 ("9", "Diagnose a kid-resolution failure", "Given a credential whose `kid` is not published, produce the exact error and name the one change that fixes it. **Everyone does this one.**", "10 min", C['red']),
]
bw = (CW - 2 * 0.20) / 3
for i, (n, t, d, tm, col) in enumerate(ex):
    x = ML + (i % 3) * (bw + 0.20)
    yy = y + (i // 3) * 1.62
    rect(s, x, yy, bw, 1.48, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.055)
    rect(s, x, yy, 0.055, 1.48, fill=col)
    b = rect(s, x + 0.20, yy + 0.16, 0.34, 0.34, fill=col, shape=MSO_SHAPE.OVAL)
    tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run(); rb.text = n; rb.font.size = Pt(11); rb.font.bold = True
    rb.font.color.rgb = C['white']; rb.font.name = F_SANS
    _, t2 = tb(s, x + 0.62, yy + 0.18, bw - 1.30, 0.3)
    para(t2, t, size=10.8, color=C['ink'], bold=True, first=True)
    _, t5 = tb(s, x + bw - 0.78, yy + 0.20, 0.62, 0.26)
    para(t5, tm, size=8.4, color=col, bold=True, align=PP_ALIGN.RIGHT, first=True)
    _, t3 = tb(s, x + 0.22, yy + 0.58, bw - 0.44, 0.84)
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', d)
    ch = []
    for pt in parts:
        if not pt:
            continue
        if pt.startswith('`'):
            ch.append((pt[1:-1], C['primary'], False, False, F_MONO))
        elif pt.startswith('**'):
            ch.append((pt[2:-2], col, True))
        else:
            ch.append((pt, C['ink2'], False))
    rich(t3, ch, size=9.3, first=True, line_spacing=1.26)
notes(s, ["Do not try to run all nine. Pick three or four based on who is in the room, and let people choose within that.",
          "Exercises 2 and 9 are the ones that produce the capability we most want: correct attribution of a failure, and comfort with key resolution.",
          "Exercise 6 is the one that makes SD-JWT click permanently. If you only have time for one technical exercise, make it this.",
          "Run them in pairs, not alone — the explaining is where the learning happens. Reconvene after each and take one answer from each pair."],
      caveats=["Prepare the materials in advance: the error cards for exercise 2, a sample credential for 6 and 7, a trace for 1 and 8.",
               "Have a written answer key. Do not improvise the answers in front of the room."],
      minutes="30–45 min, run as a block or spread through the day")
footer(s)

# =================================================================== RECAP
STATE['section'] = "Recap and next steps"
s, y = slide("Recap: the architecture and who owns what", kicker="Final recap, part 1",
             sub="If you remember one slide from today, make it this one.")
spine(s, y=y + 0.10, highlight=('issuer', 'mimoto', 'wallet', 'store', 'verifier'), big=True)
yy = y + 2.60
owners = [
 ("Issuer", ["Authenticates the citizen", "Decides eligibility", "Signs the credential",
             "Publishes metadata and keys", "Owns key rotation"], C['primary']),
 ("Mimoto", ["Issuer catalogue", "Trusted verifier list", "Token exchange brokering",
             "Credential store for Inji Web", "Caching, sessions, PDF"], C['violet']),
 ("Inji Wallet", ["Holds credentials on device", "Generates and protects keys",
                  "Signs proofs and presentations", "Shows consent", "Works offline for display"], C['accent']),
 ("Inji Web", ["Browser holder", "No local key, no local store",
               "Mimoto is its backend", "Guest and logged-in journeys", "For people without a phone"], C['amber']),
 ("Verifier", ["Builds the request", "Validates issuer signature",
               "Validates holder binding", "Checks nonce and audience", "Makes the decision"], C['green']),
]
bw = (CW - 4 * 0.20) / 5
for i, (t, items, col) in enumerate(owners):
    x = ML + i * (bw + 0.20)
    rect(s, x, yy, bw, 2.05, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.055)
    rect(s, x, yy, bw, 0.065, fill=col)
    _, t2 = tb(s, x + 0.18, yy + 0.20, bw - 0.36, 0.3)
    para(t2, t, size=11.5, color=col, bold=True, first=True)
    cy = yy + 0.58
    for it in items:
        rect(s, x + 0.20, cy + 0.055, 0.07, 0.07, fill=col, shape=MSO_SHAPE.OVAL)
        _, t3 = tb(s, x + 0.36, cy, bw - 0.54, 0.4)
        para(t3, it, size=9.0, color=C['ink2'], first=True, line_spacing=1.2)
        nl = max(1, -(-len(it) // 26))
        cy += 0.04 + nl * 0.155
notes(s, ["Close the loop with the diagram you opened with. Ask someone in the room to narrate it rather than doing it yourself.",
          "Point at the Wallet and Web columns together one last time — same protocol, different custody model. It is the thing most likely to be misremembered.",
          "Ask: which column does your team sit in? Which column will you have to argue with most? That framing helps people plan their next conversations."],
      minutes="4 min")
footer(s)

# ------------------------------------------------- recap 2
s, y = slide("Recap: protocols, security and the lessons", kicker="Final recap, part 2",
             sub="The eight sentences worth carrying out of the room.")
lessons = [
 ("OpenID4VCI gets a credential; OpenID4VP shows one.", "Two protocols, two directions. Everything else is implementation.", C['primary']),
 ("PKCE protects the code. DPoP protects the token. The credential proof protects the binding.", "Three mechanisms, three assets. Inji implements the first and third today.", C['violet']),
 ("Proof type, binding method, holder binding, key binding are four different things.", "Ask which one someone means before agreeing to anything.", C['accent']),
 ("Format choice decides selective disclosure, verification and key resolution.", "It follows from your claims, not from fashion. It is the hardest decision to reverse.", C['amber']),
 ("Signature verification is not trust.", "A valid signature from an issuer you do not accept is worthless. Trust policy is separate from cryptography.", C['green']),
 ("The consent screen is a security control.", "Most real attacks are social. Design it as carefully as you design the crypto.", C['red']),
 ("Key rotation without overlap breaks every credential you ever issued.", "Publish retired keys for at least one full credential lifetime.", C['primary_d']),
 ("Configuration beats customisation, every time.", "Push change into issuer metadata and Mimoto config. App-store cycles are the slowest thing you own.", C['violet']),
]
for i, (t, d, col) in enumerate(lessons):
    x = ML + (i % 2) * (CW / 2 + 0.12)
    yy = y + (i // 2) * 1.28
    wid = CW / 2 - 0.12
    rect(s, x, yy, wid, 1.12, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.07)
    rect(s, x, yy, 0.055, 1.12, fill=col)
    b = rect(s, x + 0.20, yy + 0.16, 0.30, 0.30, fill=col, shape=MSO_SHAPE.OVAL)
    tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run(); rb.text = str(i + 1); rb.font.size = Pt(10); rb.font.bold = True
    rb.font.color.rgb = C['white']; rb.font.name = F_SANS
    _, t2 = tb(s, x + 0.60, yy + 0.14, wid - 0.82, 0.5)
    para(t2, t, size=10.8, color=C['ink'], bold=True, first=True, line_spacing=1.15)
    _, t3 = tb(s, x + 0.60, yy + 0.66, wid - 0.82, 0.42)
    para(t3, d, size=9.3, color=C['muted'], first=True, line_spacing=1.22)
notes(s, ["Read all eight out loud, slowly. This is the last thing people hear.",
          "Ask the room which one they disagree with. If nobody disagrees, ask which one they think their organisation will find hardest to act on — that surfaces the real risks.",
          "Lesson 5 and lesson 7 are the two that cause the most expensive incidents in deployed systems. Give them an extra beat."],
      minutes="4 min")
footer(s)

# ------------------------------------------------- next steps
s, y = slide("Next steps for the Brazil implementation", kicker="What happens after today",
             sub="Concrete, owned, and dated. A workshop that ends without owners ends without effect.")
phases = [
 ("This week", [
   "Stand up a full local stack (`docker-compose` in `inji-web`).",
   "Build a throwaway issuer and verifier to experiment against.",
   "Assign an owner to every open question from section 13.",
   "Review the existing `pt.json` translation for Brazilian Portuguese.",
 ], C['accent']),
 ("This month", [
   "Decide claims and disclosure requirements per credential type.",
   "Decide the format per credential type, with the reasoning written down.",
   "Agree the binding and assurance level per credential type.",
   "Start the trust framework and key publication conversation — it has the longest lead time.",
 ], C['primary']),
 ("This quarter", [
   "Agree the interoperability profile in writing with the first external issuer and verifier.",
   "Run a pilot with real citizens in one region, including a low-connectivity site.",
   "Test key rotation as a planned exercise.",
   "Decide the deployment and data residency model for Mimoto.",
 ], C['violet']),
 ("Ongoing", [
   "Contribute fixes and gaps upstream rather than forking.",
   "Track draft versions — OpenID4VCI 13+, OpenID4VP 23+, SD-JWT VC, and the DCQL transition.",
   "Keep a conformance checklist and run it every release.",
   "Re-run this workshop for each new team that joins.",
 ], C['green']),
]
bw = (CW - 3 * 0.20) / 4
for i, (t, items, col) in enumerate(phases):
    x = ML + i * (bw + 0.20)
    rect(s, x, y, bw, 3.30, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.24, bw - 0.40, 0.32)
    para(t2, t.upper(), size=11.5, color=col, bold=True, first=True)
    bullets(s, x + 0.20, y + 0.72, bw - 0.40, items, size=9.7, gap=0.09, bullet_col=col)
yy = y + 3.58
_, tf = tb(s, ML, yy, CW, 0.32)
para(tf, "REFERENCES — read these, not blog posts", size=9, color=C['accent'], bold=True, first=True)
refs = [
 ["OpenID4VCI", "openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "Inji supports drafts 11 and 13"],
 ["OpenID4VP", "openid.net/specs/openid-4-verifiable-presentations-1_0-23.html", "Inji supports drafts 21 and 23"],
 ["SD-JWT VC", "datatracker.ietf.org — draft-ietf-oauth-sd-jwt-vc", "and draft-ietf-oauth-selective-disclosure-jwt"],
 ["PKCE / DPoP", "RFC 7636  ·  RFC 9449", "and RFC 8414 for AS metadata"],
 ["mDoc / mDL", "ISO/IEC 18013-5  ·  ISO/IEC TS 18013-7", "proximity and online presentation"],
 ["Inji", "docs.inji.io  ·  github.com/mosip", "inji-wallet, inji-web, mimoto, inji-vci-client, inji-openid4vp, vc-verifier"],
]
table(s, ML, yy + 0.34, CW, ["Topic", "Where", "Note"], refs,
      col_w=[1.8, 5.2, 5.2], fsize=8.8, row_h=0.28, head_h=0.28)
notes(s, ["Close by making it concrete. Name people against the 'this week' column before anyone leaves the room.",
          "The 'this month' column contains the decisions that unblock everything else. If only one column gets attention, make it that one.",
          "The references table is deliberately short and authoritative. Encourage people to read the specifications — in this field the primary sources are unusually readable, and blog posts age badly.",
          "Offer to reconvene in four weeks to review the section 13 answers. A follow-up session converts a workshop into a programme."],
      caveats=["Draft URLs move as versions advance. Check the OpenID Foundation and IETF datatracker for the current draft rather than trusting a bookmarked link.",
               "Verify every version claim in this deck against the release you deploy."],
      minutes="5 min")
footer(s)

# ------------------------------------------------- closing
s = new_slide(dark=True)
rect(s, 0, 0, W, H, fill=C['dark'])
rect(s, 0, 0, W, 0.10, fill=C['accent'])
_, tf = tb(s, 1.4, 2.35, 8.6, 1.5)
para(tf, "Obrigado — questions, arguments,\nand disagreements welcome.", size=32, color=C['white'],
     bold=True, first=True, line_spacing=1.1)
line(s, 1.4, 4.20, 5.0, 4.20, C['accent'], 2.5)
_, tf = tb(s, 1.4, 4.45, 9.0, 1.4)
para(tf, "The best outcome of today is a list of things we could not answer, each with a name against it.",
     size=14, color=RGBColor(0x9E, 0xB8, 0xCE), first=True, line_spacing=1.3)
para(tf, "Slides include full speaker notes. Every version-specific statement should be re-checked against the release you deploy.",
     size=11.5, color=RGBColor(0x62, 0x80, 0x9B), space_before=10, line_spacing=1.3)
notes(s, ["Do not end on a summary. End on the open questions.",
          "Read out the unanswered list from section 13 and confirm each owner by name.",
          "Agree the date of the follow-up session before people leave."],
      minutes="Remaining time — open Q&A")
footer(s, dark=True)

# =================================================================== auto-fit pass
_fitted = fit_all()
