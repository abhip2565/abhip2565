# -*- coding: utf-8 -*-
"""Inji Key Manager deep dive — trust & key management (90 min).
Facts verified against mosip/keymanager and mosip/inji-certify."""
from deck_km import *   # noqa
import theme_inji
theme_inji.apply()
F_SANS = theme_inji.SANS   # this module's own binding from the star-import

# =================================================================== 1 TITLE
s = new_slide(dark=True, chrome=False)
STATE['section'] = "Key Manager — trust & key management"
s.shapes.add_picture(theme_inji.ASSETS + '/inji_mark.png', Inches(7.40), Inches(4.16),
                     Inches(6.13), Inches(3.10))
s.shapes.add_picture(theme_inji.ASSETS + '/inji_logo.png', Inches(0.95), Inches(0.62),
                     Inches(1.28), Inches(0.65))
_, tf = tb(s, 0.95, 1.62, 7.3, 0.4)
para(tf, "INJI DEEP-DIVE  ·  KEY MANAGER", size=11.5,
     color=C['accent'], bold=True, first=True)
_, tf = tb(s, 0.95, 2.10, 7.4, 2.0)
para(tf, "Key Manager", size=46, color=C['white'], bold=True, italic=True,
     first=True, line_spacing=1.0)
para(tf, "Trust and key management,\nfrom the core idea to production detail", size=18,
     color=theme_inji.ON_DARK, space_before=8, line_spacing=1.2)
line(s, 0.95, 4.72, 4.30, 4.72, C['accent'], 2.5)
_, tf = tb(s, 0.95, 4.96, 7.3, 1.5)
para(tf, "90 minutes  ·  8 topics  ·  17 architecture and flow diagrams", size=13,
     color=theme_inji.ON_DARK, first=True)
para(tf, "Verified against mosip/keymanager and mosip/inji-certify. Version-specific behaviour is flagged where it matters.",
     size=10.5, color=theme_inji.ON_DARK_DIM, space_before=8, line_spacing=1.3)
_, tf = tb(s, 8.62, 1.20, 4.3, 0.3)
para(tf, "THE EIGHT QUESTIONS THIS SESSION ANSWERS", size=8.5, color=C['accent'],
     bold=True, first=True)
qs = ["Why a dedicated Key Manager at all?",
      "What is the key hierarchy, really?",
      "How does Certify sign without holding a key?",
      "What happens at rotation, expiry, revocation?",
      "Software keystore or HSM — and why?",
      "How does a key become a trust anchor?",
      "How do status lists and keys interact?",
      "What happens if a key is compromised?"]
cy = 1.62
for i, q in enumerate(qs):
    b = rect(s, 8.62, cy + 0.02, 0.28, 0.28, fill=C['accent'], shape=MSO_SHAPE.OVAL)
    tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run(); rb.text = str(i + 1); rb.font.size = Pt(8.5); rb.font.bold = True
    rb.font.color.rgb = C['white']; rb.font.name = F_SANS
    _, t3 = tb(s, 9.00, cy, 3.9, 0.6)
    para(t3, q, size=10, color=theme_inji.ON_DARK, first=True, line_spacing=1.2)
    cy += 0.62
notes(s, ["Open by naming the stakes: everything the issuance side does — every credential, every DID document, every status list — is only worth something because a private key stayed private. This session is about the component that makes that true.",
          "Tell the room the shape of the 90 minutes: 8 topics, roughly 10 minutes each, diagram-led. Questions welcome throughout; anything needing the hands-on environment gets parked for the lab.",
          "Ask up front: who here has run an HSM in production? Who has done a key rotation on a live service? The answers tell you how deep to go in topics 4 and 5."],
      caveats=["This is the MOSIP Key Manager (mosip/keymanager, kernel-keymanager-service). Inji Certify embeds the same library rather than calling it over HTTP — that distinction comes up in topic 2 and matters for deployment.",
               "Numbers on these slides (validity days, pre-expire days) come from the shipped key_policy_def seed data. Every deployment sets its own."],
      minutes="2 min")
footer(s, dark=True)

# =================================================================== 2 AGENDA
s, y = slide("How the 90 minutes runs", kicker="Session map",
             sub="Eight topics. The first three build the model; the rest are consequences of it.")
rows = [
 ["1", "**Why a Key Manager at all**", "10 min", "Ad-hoc key handling vs. centralised custody, policy and audit", "2 diagrams"],
 ["2", "**Key Manager architecture**", "20 min", "Three-tier hierarchy, HSM vs database, signing without key access, data model, APIs", "6 diagrams"],
 ["3", "**Key lifecycle in detail**", "15 min", "Generate, activate, rotate, expire, revoke — and what happens to credentials already issued", "3 diagrams"],
 ["4", "**HSM integration**", "12 min", "PKCS#11, PKCS12, Offline, JCE; SoftHSM vs a real HSM; production trade-offs", "2 diagrams"],
 ["5", "**Trust anchors**", "12 min", "How a public key becomes something a verifier trusts; `did.json`, `jwks.json`, safe rotation", "2 diagrams"],
 ["6", "**Status list mechanics**", "10 min", "Revocation and suspension, and how status lists interact with key rotation", "2 diagrams"],
 ["7", "**Multi-issuer and multi-tenant trust**", "6 min", "Key isolation on one Key Manager; being trusted outside your own deployment", "1 diagram"],
 ["8", "**Incident: key compromise**", "5 min", "What to do in the first hour, and how fast trust can actually be withdrawn", "1 diagram"],
]
_tb = table(s, ML, y, CW, ["#", "Topic", "Time", "What it covers", "Visuals"], rows,
            col_w=[0.5, 3.3, 0.9, 6.5, 1.1], fsize=9.5, row_h=0.46, head_h=0.34)
yy = _tb + 0.24
callout(s, ML, yy, CW, "Two ideas carry the whole session. **One:** private keys live in exactly one place and never move. **Two:** a key is never deleted — it is superseded, and the old one stays published so yesterday's credentials still verify. Almost every design decision in the Key Manager follows from those two.", kind='tip', size=11)
notes(s, ["Keep this to ninety seconds. The room is technical and impatient.",
          "Do flag the shape: topics 1–3 are the model, topics 4–8 are consequences. If we run long, topic 7 compresses and topic 8 does not — incident response is the one people remember.",
          "The callout is the thesis of the session. Say it now, and say it again in the recap."],
      minutes="2 min")
footer(s)

# =================================================================== 3 WHY — BEFORE/AFTER
s, y = slide("Why not just keep keys in the application?", kicker="Topic 1 — the core idea",
             sub="The honest version of what happens when each service handles its own key material.")
zone(s, ML, y, 5.95, 3.55, "WITHOUT A KEY MANAGER", C['red'], C['red_l'])
svc = [("Certify", 0), ("eSignet", 1), ("IDA", 2)]
for nm, i in svc:
    x = ML + 0.35 + i * 1.78
    node(s, x, y + 0.55, 1.58, 0.72, nm, fill=C['white'], border=C['red'], tsize=10.5)
    node(s, x, y + 1.52, 1.58, 0.62, "key.p12", "on local disk", fill=C['red_l'],
         border=C['red'], fg=C['red'], tsize=9.5, ssize=7.5, mono=True)
    line(s, x + 0.79, y + 1.27, x + 0.79, y + 1.52, C['red'], 1.2)
_, tf = tb(s, ML + 0.35, y + 2.36, 5.25, 1.0)
for t in ["Three copies of the trust problem, three rotation schedules.",
          "Key material sits in config, in backups, in container images.",
          "No single answer to 'which key signed this credential, and when?'",
          "Policy lives in three codebases and drifts."]:
    rich(tf, [("•  ", C['red'], True), (t, C['ink2'], False)], size=9.6,
         first=(t.startswith("Three")), space_before=3, line_spacing=1.2)
zone(s, ML + 6.28, y, 5.95, 3.55, "WITH A KEY MANAGER", C['green'], C['green_l'])
for nm, i in svc:
    x = ML + 6.60 + i * 1.78
    node(s, x, y + 0.55, 1.58, 0.72, nm, fill=C['white'], border=C['green'], tsize=10.5)
    arrow(s, x + 0.79, y + 1.27, ML + 9.26, y + 1.72, C['green'], 1.2)
node(s, ML + 7.45, y + 1.75, 3.62, 0.72, "Key Manager", "one custody point, one policy set",
     fill=C['green'], fg=C['white'], tsize=12, ssize=8)
node(s, ML + 8.30, y + 2.72, 1.92, 0.56, "HSM", "keys never leave", fill=C['ink'],
     fg=C['white'], tsize=10, ssize=7.5)
line(s, ML + 9.26, y + 2.47, ML + 9.26, y + 2.72, C['green'], 1.2)
yy = y + 3.80
cards = [("Centralised custody", "One place holds private keys, one place to harden, one place to audit access.", C['primary']),
         ("Consistent policy", "Validity, rotation cadence and algorithm are data in `key_policy_def`, not code in three services.", C['accent']),
         ("One audit trail", "Every signing operation goes through one service, so 'which key signed what' has a single answer.", C['violet'])]
bw = (CW - 2 * 0.22) / 3
for i, (t, d, col) in enumerate(cards):
    x = ML + i * (bw + 0.22)
    rect(s, x, yy, bw, 1.32, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
    rect(s, x, yy, 0.055, 1.32, fill=col)
    _, t2 = tb(s, x + 0.22, yy + 0.14, bw - 0.42, 0.3)
    para(t2, t, size=11.5, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.22, yy + 0.48, bw - 0.42, 0.75)
    parts = re.split(r'(`[^`]+`)', d)
    rich(t3, [((p[1:-1], C['primary'], False, False, F_MONO) if p.startswith('`') else (p, C['muted'], False))
              for p in parts if p], size=9.5, first=True, line_spacing=1.25)
notes(s, ["Do not present this as theory. Ask the room how key material is handled in the systems they operate today, and let the left-hand box be uncomfortable.",
          "The strongest of the three benefits for a national issuer is the audit trail. When a credential is disputed years later, 'which key signed this and was it valid at the time' has to have one answer, from one system.",
          "The policy point is concrete in MOSIP: key_policy_def is a database table with app_id, key_validity_duration and pre_expire_days. Changing rotation cadence is a data change, not a release.",
          "Note that 'Key Manager' here is a library as much as a service — Certify embeds it. We come back to that on the next slide."],
      caveats=["Centralisation is also concentration of risk. One Key Manager compromised is worse than one service compromised. That is precisely why the HSM and the role model matter, and why topic 8 exists.",
               "Do not oversell: a Key Manager does not remove the need for network segmentation, secrets management or least-privilege service accounts."],
      questions=["Isn't this a single point of failure? — For availability, yes; design for HA. For confidentiality it is the opposite: one hardened point beats three soft ones."],
      minutes="8 min")
footer(s)

# =================================================================== 4 WHERE IT SITS
s, y = slide("Where the Key Manager sits in the Inji stack", kicker="Topic 1 — placement",
             sub="Two deployment shapes, and Inji Certify uses the second one.")
zone(s, ML, y, 5.95, 3.90, "SHAPE A — SHARED SERVICE", C['primary'], C['primary_l'])
node(s, ML + 0.40, y + 0.50, 1.60, 0.62, "Certify", fill=C['white'], border=C['primary'], tsize=10)
node(s, ML + 2.20, y + 0.50, 1.55, 0.62, "eSignet", fill=C['white'], border=C['primary'], tsize=10)
node(s, ML + 3.95, y + 0.50, 1.55, 0.62, "IDA / others", fill=C['white'], border=C['primary'], tsize=9.5)
node(s, ML + 1.30, y + 1.72, 3.35, 0.78, "kernel-keymanager-service",
     "REST · /v1/keymanager", fill=C['primary'], fg=C['white'], tsize=11, ssize=8, mono=False)
for i in range(3):
    x = ML + 0.40 + i * 1.78 + 0.78
    arrow(s, x, y + 1.12, ML + 2.98, y + 1.72, C['primary'], 1.1)
node(s, ML + 0.45, y + 2.86, 2.35, 0.62, "HSM", "PKCS#11", fill=C['ink'], fg=C['white'], tsize=10, ssize=7.5)
node(s, ML + 3.15, y + 2.86, 2.35, 0.62, "Postgres", "mosip_keymgr", fill=C['ink2'], fg=C['white'], tsize=10, ssize=7.5)
line(s, ML + 2.20, y + 2.50, ML + 1.62, y + 2.86, C['primary'], 1.1)
line(s, ML + 3.60, y + 2.50, ML + 4.32, y + 2.86, C['primary'], 1.1)
zone(s, ML + 6.28, y, 5.95, 3.90, "SHAPE B — EMBEDDED LIBRARY  (Inji Certify today)", C['accent'], C['accent_l'])
rect(s, ML + 6.68, y + 0.50, 5.15, 2.00, fill=C['white'], line=C['accent'], lw=1.4,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
_, tf = tb(s, ML + 6.85, y + 0.62, 4.8, 0.28)
para(tf, "Inji Certify process", size=10.5, color=C['accent'], bold=True, first=True)
node(s, ML + 6.90, y + 1.00, 2.30, 0.60, "Certify services", "VC issuance", fill=C['accent_l'],
     border=C['accent'], fg=C['accent'], tsize=9.5, ssize=7.5)
node(s, ML + 9.35, y + 1.00, 2.30, 0.60, "keymanager lib", "kernel-keymanager", fill=C['accent'],
     fg=C['white'], tsize=9.5, ssize=7.5)
arrow(s, ML + 9.22, y + 1.30, ML + 9.33, y + 1.30, C['accent'], 1.3)
_, tf = tb(s, ML + 6.90, y + 1.72, 4.75, 0.62)
para(tf, "In-process method call. No network hop, no token, no separate service to operate.",
     size=9.2, color=C['muted'], italic=True, first=True, line_spacing=1.22)
node(s, ML + 6.73, y + 2.86, 2.35, 0.62, "HSM / PKCS12", "keystore", fill=C['ink'], fg=C['white'], tsize=10, ssize=7.5)
node(s, ML + 9.43, y + 2.86, 2.35, 0.62, "Postgres", "certify schema", fill=C['ink2'], fg=C['white'], tsize=10, ssize=7.5)
line(s, ML + 8.30, y + 2.50, ML + 7.90, y + 2.86, C['accent'], 1.1)
line(s, ML + 10.20, y + 2.50, ML + 10.60, y + 2.86, C['accent'], 1.1)
yy = y + 4.16
codebox(s, ML, yy, 5.95, 1.10, [
 '# in certify-default.properties — Certify owns a keystore directly',
 'mosip.kernel.keymanager.hsm.keystore-type = PKCS12',
 'mosip.kernel.keymanager.hsm.config-path  = CERTIFY_PKCS12/local.p12',
 '# production: switch to PKCS11 + an HSM config file',
], size=8.6, hl=[1])
callout(s, ML + 6.28, yy, 5.95, "Because Certify **embeds** the key manager, `mosip.kernel.keymanager.*` properties are Certify's own configuration. There is no separate Key Manager pod to point at in the Inji stack — a frequent source of confusion when people come from a full MOSIP deployment.", kind='warn', size=10.2)
notes(s, ["This slide prevents a real deployment misunderstanding. In a full MOSIP platform the Key Manager is a shared REST service. In the Inji stack, Certify links the same library in-process and owns its own keystore and key tables.",
          "The evidence is in certify-default.properties: mosip.kernel.keymanager.hsm.keystore-type, config-path and keystore-pass are set on Certify itself. Show that file in the hands-on if people doubt it.",
          "Consequences to state explicitly: no network hop for signing (good for latency), no shared custody across services (good for isolation), but also no single audit point across Certify and eSignet — each has its own.",
          "Which shape you want is a real architecture decision. If several services in your estate will sign credentials, Shape A gives you one custody point; Shape B gives you simpler operations per service."],
      caveats=["Shape B means every Certify replica needs access to the keystore. With PKCS11 that means every pod needs the HSM client library and credentials — this is a real operational constraint we return to in topic 4.",
               "Do not assume the local PKCS12 file in the default config is acceptable anywhere but a laptop."],
      questions=["Can we run Certify against a separate Key Manager service? — Not out of the box in the current code path; it links the library. Treat it as a change to propose upstream, not a config flag."],
      minutes="6 min")
footer(s)

# =================================================================== 5 HIERARCHY
s, y = slide("The three-tier key hierarchy", kicker="Topic 2 — architecture",
             sub="The single most important diagram in this session. Everything else is a consequence of it.")
# tier boxes
tiers = [
 ("ROOT key", "self-signed root certificate  ·  app_id = ROOT",
  "Lives in the HSM. Never used to sign a credential — only to sign module keys.",
  C['ink'], 2.6, 0.0),
 ("Module / master key", "one per app_id, e.g. CERTIFY_VC_SIGN_RSA  ·  cert signed by ROOT",
  "Lives in the HSM. Signs base-key certificates and wraps base private keys.",
  C['primary'], 4.4, 0.0),
 ("Base / reference key", "app_id + ref_id, e.g. CERTIFY_VC_SIGN_ED25519 + ED25519_SIGN",
  "Generated in software. Private key encrypted with the module public key, stored in Postgres.",
  C['accent'], 6.2, 0.0),
]
bx, bw = ML + 0.25, 6.05
for i, (t, sub_, note, col, wfac, _) in enumerate(tiers):
    yy = y + i * 1.22
    inset = i * 0.30
    node(s, bx + inset, yy, bw - inset * 2, 0.92, t, sub_, fill=col, fg=C['white'],
         tsize=13, ssize=8.4)
    _, t3 = tb(s, bx + bw + 0.30, yy + 0.10, 5.4, 0.75)
    para(t3, note, size=9.8, color=C['ink2'], first=True, line_spacing=1.25)
    if i < 2:
        arrow(s, bx + bw / 2, yy + 0.92, bx + bw / 2, yy + 1.22, C['ink2'], 1.5,
              label="signs the certificate below", lw_box=2.5, lside='on', lsize=7.8)
yy = y + 3.72
zone(s, ML, yy, 5.95, 1.55, "STAYS IN THE HSM", C['ink'], C['surf'])
_, tf = tb(s, ML + 0.28, yy + 0.30, 5.4, 1.15)
for i, t in enumerate(["**ROOT** private key — signs module certificates only.",
                       "**Module/master** private keys — sign base certificates, and unwrap base private keys.",
                       "Neither ever leaves the device. The Key Manager asks the HSM to sign; it never reads the key."]):
    parts = re.split(r'(\*\*[^*]+\*\*)', t)
    rich(tf, [((p[2:-2], C['ink'], True) if p.startswith('**') else (p, C['muted'], False))
              for p in parts if p], size=9.6, first=(i == 0), space_before=4, line_spacing=1.22)
zone(s, ML + 6.28, yy, 5.95, 1.55, "STORED IN POSTGRES", C['accent'], C['accent_l'])
_, tf = tb(s, ML + 6.56, yy + 0.30, 5.4, 1.15)
for i, t in enumerate(["`key_store` — the base private key, **encrypted with the module public key**, plus its PEM certificate.",
                       "`key_alias` — metadata: app_id, ref_id, generation and expiry time, thumbprint.",
                       "Stolen database rows alone are useless: unwrapping needs the module private key in the HSM."]):
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', t)
    ch = []
    for p in parts:
        if not p: continue
        if p.startswith('`'): ch.append((p[1:-1], C['accent'], False, False, F_MONO))
        elif p.startswith('**'): ch.append((p[2:-2], C['ink'], True))
        else: ch.append((p, C['muted'], False))
    rich(tf, ch, size=9.6, first=(i == 0), space_before=4, line_spacing=1.22)
notes(s, ["Draw this on the whiteboard as you talk. Three tiers, and the relationship between them is 'signs the certificate of'.",
          "Tier 1, ROOT: app_id ROOT in key_policy_def, 2920 days validity in the shipped seed data. It signs module certificates and nothing else. If you ever see a credential signed directly by ROOT, something is wrong.",
          "Tier 2, module or master key: one per app_id. In Certify these are CERTIFY_VC_SIGN_RSA, CERTIFY_VC_SIGN_ED25519, CERTIFY_VC_SIGN_EC_R1, CERTIFY_VC_SIGN_EC_K1 — one per signature algorithm. Its certificate is signed by ROOT. It lives in the HSM.",
          "Tier 3, base or reference key: identified by app_id PLUS ref_id. This is the key that actually signs a credential. Here is the part people miss: it is generated in software, its private key is then encrypted with the module public key and stored as a row in key_store, and its certificate is signed by the module private key inside the HSM.",
          "So the honest security statement is: module and root private keys never exist outside the HSM. Base private keys do exist in process memory while in use, but at rest they are wrapped by a key that only the HSM can unwrap."],
      caveats=["That last point matters and is often over-claimed. Do not tell an auditor 'all private keys are in the HSM' — say 'root and module keys are in the HSM; operational signing keys are wrapped by them and unwrapped in memory on use'.",
               "The wrapping is done with the module PUBLIC key at generation time (keymanagerUtil.encryptKey) and unwrapped with the module private key from the HSM (PrivateKeyDecryptorHelper). Reading those two classes is the fastest way to convince a sceptic.",
               "Some reference ids are handled as HSM keys directly rather than DB-stored — the signing refs such as ED25519_SIGN, EC_SECP256R1_SIGN, EC_SECP256K1_SIGN go to the HSM path in getAllCertificates. Check the branch for the key you care about."],
      questions=["Why not keep every key in the HSM? — Cost and throughput. HSM key slots and operations are finite and expensive; this design puts the crown jewels in hardware and scales the rest.",
                 "Can we force VC signing keys into the HSM? — For the Ed25519/EC sign reference ids the code already takes the HSM path. Verify for your chosen algorithm in the lab."],
      minutes="10 min")
footer(s)

# =================================================================== 6 HSM vs DB
s, y = slide("What lives where — and why a stolen database is not enough", kicker="Topic 2 — custody",
             sub="Follow one base key from generation to storage. The wrap is the whole security argument.")
sequence(s, ["Caller (Certify)", "Key Manager", "Key generator", "HSM", "Postgres"],
 [(0, 1, "Need a signing key for `CERTIFY_VC_SIGN_ED25519` / `ED25519_SIGN`"),
  (1, 4, "Look for a current `key_alias` row for this app_id + ref_id"),
  (4, 1, "none found (first use, or the previous one aged out)", 'resp'),
  (1, 2, "Generate a fresh key pair (BouncyCastle)"),
  (2, 1, "public + private key, in memory", 'resp'),
  (1, 3, "Fetch the **module** certificate for this app_id"),
  (3, 1, "module certificate (public key + alias)", 'resp'),
  (1, 1, "Encrypt the new private key with the module **public** key", 'self'),
  (1, 3, "Sign the new X.509 certificate  (CN = appId-refId)"),
  (3, 1, "certificate signed by the module private key — which never left", 'resp'),
  (1, 4, "INSERT `key_store` (id, master_key, encrypted private key, cert PEM)"),
  (1, 4, "INSERT `key_alias` (app_id, ref_id, gen/expiry, thumbprint, uni_ident)"),
  (1, 0, "certificate + key id — never the private key", 'resp'),
 ], top=1.42, height=4.30)
yy = 6.00
callout(s, ML, yy, CW, "Steps 8 and 11 together are the whole point. The row in `key_store` holds a private key that **only the HSM can unwrap**. An attacker with a full database dump, and no HSM access, has a pile of ciphertext.", kind='good', size=10.6)
notes(s, ["Walk this slowly; it is the mechanism behind the previous slide's claim.",
          "Step 4: the key pair is generated in software by the BouncyCastle key generator — getAsymmetricKey(), or getEd25519KeyPair() for the Ed25519 signing reference.",
          "Step 8: keymanagerUtil.encryptKey(privateKey, masterPublicKey). The private key is wrapped with the MODULE PUBLIC key, so wrapping needs no HSM secret — only unwrapping does.",
          "Step 9: CertificateUtility.generateX509Certificate is called with the module private key entry obtained from the HSM keystore. The signature happens inside the HSM provider; the Key Manager holds a handle, not bytes.",
          "Step 12: uni_ident is appId_refId_timestamp and carries a unique constraint — that is what stops two 'current' keys existing for the same app_id and ref_id.",
          "Ask the room: where would you attack this? The honest answers are the HSM credentials, the process memory while a base key is unwrapped, and the operator with permission to call the signing API. That leads directly into topic 4 and topic 8."],
      caveats=["The unwrap path (PrivateKeyDecryptorHelper) explicitly refuses to decrypt with a master key, and refuses when the alias equals the master alias or the stored private key is the 'NA' marker used for other-domain certificates. Those guards exist to stop the module key being used as an ordinary key.",
               "Certificate CN is set to appId-refId. That is convenient for debugging and it means your certificates are self-describing — do not treat it as a security control."],
      minutes="8 min")
footer(s)

# =================================================================== 7 SIGNING
s, y = slide("Signing without ever holding a key", kicker="Topic 2 — the signing path",
             sub="What actually happens when Certify signs a Verifiable Credential.")
sequence(s, ["Certify VC service", "key-alias mapper", "Key Manager", "HSM", "Postgres"],
 [(0, 1, "Credential is ready; signature algorithm is `EdDSA`"),
  (1, 0, "app_id `CERTIFY_VC_SIGN_ED25519`, ref_id `ED25519_SIGN`", 'resp'),
  (0, 2, "sign(payload, app_id, ref_id)"),
  (2, 4, "Fetch the current `key_alias` + `key_store` row"),
  (4, 2, "wrapped private key + certificate", 'resp'),
  (2, 3, "Unwrap: decrypt with the module private key"),
  (3, 2, "base private key, in memory only", 'resp'),
  (2, 2, "Produce the signature (JWS / Linked Data Proof)", 'self'),
  (2, 0, "signature + key id (`kid`) + certificate", 'resp'),
  (0, 0, "Attach proof to the credential and return it", 'self'),
 ], top=1.42, height=3.70)
yy = 5.42
codebox(s, ML, yy, 6.15, 1.42, [
 '# certify-default.properties — algorithm to Key Manager alias',
 'mosip.certify.signature-algo.key-alias-mapper = {                    \\',
 "  'RS256' : {{'CERTIFY_VC_SIGN_RSA',     ''                }}, \\",
 "  'EdDSA' : {{'CERTIFY_VC_SIGN_ED25519', 'ED25519_SIGN'    }}, \\",
 "  'ES256' : {{'CERTIFY_VC_SIGN_EC_R1',   'EC_SECP256R1_SIGN'}}, \\",
 "  'ES256K': {{'CERTIFY_VC_SIGN_EC_K1',   'EC_SECP256K1_SIGN'}}  }",
], size=8.3, hl=[3])
bullets(s, ML + 6.46, yy - 0.10, 5.77, [
 "The application never asks for *a key*. It asks for *a signature*, by algorithm.",
 "The mapping from algorithm to `app_id` / `ref_id` is **configuration**, so changing the signing algorithm for a credential type is a property change, not code.",
 "The returned `kid` is what a verifier will use to find the right public key in `jwks.json` or the DID document.",
 "If no current key exists for that alias, one is generated on the spot — first signature of the day can be slower.",
], size=10.0)
notes(s, ["This is the answer to 'how does Certify sign without touching key material'. It calls a signing API with an identifier, and gets a signature back.",
          "Show the key-alias-mapper property on screen. It is the seam between 'which algorithm does this credential type use' and 'which key in the Key Manager'. This is the line that changes when a deployment chooses an algorithm.",
          "Step 6 and 7 are the nuance from the previous slide: the base private key is unwrapped into process memory to sign. For the Ed25519 and EC signing reference ids the code path goes to the HSM directly instead — worth verifying for whichever algorithm you pick.",
          "Point at the last bullet as an operational gotcha: lazy generation means the very first credential after a rotation boundary pays the cost of generating a key pair and writing two rows."],
      caveats=["kid continuity is critical. If you change the algorithm for a credential type, you change the key, so you change the kid — and every already-issued credential still references the old one. That is fine, because old certificates stay published, but only if you do not prune them.",
               "Signing throughput with a real HSM is bounded by the HSM, not by your pods. Load-test it before you promise a rate."],
      questions=["Can two credential types use different algorithms? — Yes; the mapper is per algorithm and the credential configuration chooses the algorithm."],
      minutes="7 min")
footer(s)

# =================================================================== 8 DATA MODEL
s, y = slide("The data model — three tables you will read a lot", kicker="Topic 2 — schema",
             sub="Schema `keymgr` in Postgres. Learn these three and most Key Manager questions answer themselves.")
codebox(s, ML, y, 6.15, 1.62, [
 'keymgr.key_policy_def          -- the rules',
 '  app_id                  PK   -- ROOT, BASE, CERTIFY_VC_SIGN_RSA …',
 '  key_validity_duration        -- days the key is valid',
 '  pre_expire_days              -- stop using it this many days early',
 '  is_active',
], label="POLICY", size=8.5, hl=[3])
codebox(s, ML, y + 1.92, 6.15, 1.92, [
 'keymgr.key_alias               -- one row per key, ever',
 '  id                      PK   -- UUID; also the alias inside the HSM',
 '  app_id, ref_id               -- which key this is',
 '  key_gen_dtimes               -- when it was created',
 '  key_expire_dtimes            -- when it stops being valid',
 '  cert_thumbprint              -- ties a credential back to this key',
 '  uni_ident               UQ   -- appId_refId_timestamp',
], label="METADATA", size=8.5, hl=[4, 6])
codebox(s, ML + 6.46, y, 5.77, 1.62, [
 'keymgr.key_store               -- the wrapped material',
 '  id                      PK   -- = key_alias.id',
 '  master_key                   -- alias of the module key that wrapped it',
 '  private_key                  -- base64url, encrypted',
 '  certificate_data             -- PEM',
], label="MATERIAL", size=8.5, hl=[2, 3])
yy = y + 1.92
_, tf = tb(s, ML + 6.46, yy - 0.24, 5.77, 0.24)
para(tf, "SEED POLICY SHIPPED WITH THE PRODUCT", size=9, color=C['muted'], bold=True, first=True)
rows = [
 ["`ROOT`", "2920  (8 years)", "1125", "Signs module certificates only"],
 ["`BASE`", "730  (2 years)", "30", "Default for base/reference keys"],
 ["Module app ids", "1095  (3 years)", "60", "e.g. `KERNEL`, `PMS`, `RESIDENT`"],
]
table(s, ML + 6.46, yy, 5.77, ["app_id", "validity (days)", "pre-expire", "Role"], rows,
      col_w=[1.5, 1.6, 1.0, 1.7], fsize=9.0, row_h=0.42, head_h=0.32)
yy2 = y + 3.98
callout(s, ML + 6.46, yy2 - 0.52, 5.77, "`pre_expire_days` is the rotation lever. A key stops being handed out for **new** signatures that many days before it actually expires — which creates the overlap window on the next slide.", kind='tip', size=10.0)
callout(s, ML, yy2, 6.15, "There is **no delete**. `key_alias` accumulates every key the system has ever had, and that is deliberate — it is what lets a three-year-old credential still verify.", kind='warn', size=10.0)
notes(s, ["Put the three code boxes on screen and let people read. Then make three points.",
          "One: key_alias is append-only in practice. Nothing removes rows. That is how history is preserved.",
          "Two: key_store.master_key is a foreign-key-ish pointer to the key_alias id of the module key that wrapped this private key. That is the link that makes unwrapping possible and the link that makes a database dump useless on its own.",
          "Three: uni_ident carries a unique constraint on appId_refId_timestamp. If you ever see a 'no unique alias' error in the logs, this is the constraint the code is defending — it means two current keys were found for one app_id/ref_id, which should be impossible.",
          "The policy table is where a real decision gets made: how long should a VC signing key live, and how much overlap do you want? Those two numbers drive everything in topic 3."],
      caveats=["The seed numbers are MOSIP defaults, not recommendations for any particular deployment. A two-year signing key with a 30-day overlap is a policy choice you should make deliberately.",
               "cert_thumbprint is how a credential is traced back to the key that signed it. Keep it in your logs; it is far more useful than a key id in an incident.",
               "There are more tables — ca_cert_store, partner_cert_store, data_encrypt_keystore — but these three carry the signing story."],
      minutes="6 min")
footer(s)

# =================================================================== 9 API SURFACE
s, y = slide("The API surface", kicker="Topic 2 — interfaces",
             sub="Base path `/v1/keymanager`. Grouped by what you would actually use them for.")
rows = [
 ["**Key lifecycle**", "`POST /generateMasterKey/{objectType}`", "Create a module/master key in the keystore", "Bootstrap, new app_id"],
 ["", "`POST /generateECSignKey/{objectType}`", "Create an EC signing key", "EC-based credential signing"],
 ["", "`PUT /revokeKey`", "Expire the current key for an app_id + ref_id", "Suspected compromise — see topic 8"],
 ["**Certificates**", "`GET /getCertificate`", "Current certificate for an app_id + ref_id", "Publishing, debugging"],
 ["", "`GET /getAllCertificates`", "**Every** certificate ever issued for that alias", "Building `jwks.json` — this is the rotation-safe one"],
 ["", "`GET /getCertificateChain`", "Certificate chain up to ROOT", "Chain validation by a relying party"],
 ["", "`POST /generateCSR`  ·  `POST /uploadCertificate`", "Get a CSR signed by an external CA and load it back", "Bringing in an externally anchored trust chain"],
 ["**Signing**", "`POST /sign`  ·  `/signV2`  ·  `/jwtSign`  ·  `/jwsSign`", "Produce a signature over data", "VC signing, response signing"],
 ["", "`POST /coseSign1`  ·  `/cwtSign`", "COSE / CWT signatures", "mDoc and CBOR credentials"],
 ["", "`POST /jwtVerify`  ·  `/csverifysign`", "Verify a signature", "Verifier-side and internal checks"],
 ["**Crypto**", "`POST /encrypt`  ·  `/decrypt`  ·  `/encryptWithPin`", "Data encryption using managed keys", "Protecting data at rest"],
 ["**Trust store**", "`POST /uploadCACertificate`", "Register a CA or sub-CA certificate", "Building the trust store"],
 ["", "`POST /uploadPartnerCertificate`  ·  `/verifyCertificateTrust`", "Partner certificates and trust-path validation", "Onboarding external parties"],
]
table(s, ML, y, CW, ["Group", "Endpoint", "What it does", "When you reach for it"], rows,
      col_w=[1.7, 4.3, 3.4, 3.4], fsize=8.8, row_h=0.33, head_h=0.32)
notes(s, ["Reference slide — do not read it out. Point at three rows.",
          "getAllCertificates versus getCertificate is the single most important distinction on this slide. getCertificate gives you today's key. getAllCertificates gives you every key that alias has ever had. Certify's jwks.json is built from getAllCertificates, and that is exactly why rotation does not break old credentials.",
          "revokeKey does something much less dramatic than the name suggests — we cover it in topic 3. Flag it now so nobody leaves thinking it destroys anything.",
          "generateCSR plus uploadCertificate is the path if the trust chain must come from an external or national CA rather than the self-signed ROOT. That is a likely requirement for a government issuer and worth flagging to whoever owns PKI."],
      caveats=["All of these are protected by role-based authorisation (mosip.role.keymanager.*). In the embedded-in-Certify shape, most are not exposed at all — Certify calls the library directly.",
               "Do not expose the Key Manager API to anything but trusted internal callers. There is no scenario where a wallet or a verifier should reach it."],
      minutes="4 min")
footer(s)

# =================================================================== 10 LIFECYCLE STATES
s, y = slide("The life of one key", kicker="Topic 3 — lifecycle",
             sub="Five states. Only one of them is 'being used to sign', and none of them is 'deleted'.")
lifecycle(s, y + 0.30, [
 ("GENERATED", "key pair created,\nwrapped, stored", C['muted']),
 ("CURRENT", "the one handed out\nfor new signatures", C['green']),
 ("SUPERSEDED", "pre-expire reached;\nstill valid for verifying", C['amber']),
 ("EXPIRED", "past key_expire_dtimes;\nverification should fail", C['red']),
 ("RETAINED", "row stays forever,\ncertificate stays published", C['ink']),
], h=0.95, gap=0.30)
yy = y + 1.62
rows = [
 ["**GENERATED**", "On first use of an `app_id` + `ref_id`, or when no current key exists", "Row written to `key_alias` and `key_store`", "Lazy — no scheduler triggers it"],
 ["**CURRENT**", "`now` is before `key_expire_dtimes − pre_expire_days`", "Returned by `getCertificate`; used for every new signature", "Exactly one per app_id + ref_id"],
 ["**SUPERSEDED**", "`now` has passed the pre-expire boundary", "No longer used for new signatures. A new key is generated on the next request", "**Still verifies** — this is the overlap window"],
 ["**EXPIRED**", "`now` is past `key_expire_dtimes`", "Verifiers should reject signatures dated after this", "Certificate `notAfter` carries the same date"],
 ["**RETAINED**", "Always", "Still returned by `getAllCertificates`; still published in `jwks.json`", "These rows are never deleted"],
]
table(s, ML, yy, CW, ["State", "Entered when", "What it means operationally", "The catch"], rows,
      col_w=[1.6, 3.5, 4.5, 3.2], fsize=9.0, row_h=0.50, head_h=0.32)
notes(s, ["The state that surprises people is SUPERSEDED. A key stops being used for new signatures before it expires, and the gap between those two moments is the whole point.",
          "The mechanism is one line in KeymanagerUtil.isValidTimestamp: a key counts as current only while now is before keyExpiryTime minus preExpireDays. Once that boundary passes, the key is filtered out of the 'current' list, and the next signing request generates a fresh one.",
          "Note that generation is lazy. Nothing schedules a rotation. The first signing request after the boundary pays the cost. If your issuance volume is bursty, that first request can be noticeably slower — worth knowing before someone opens a latency ticket.",
          "RETAINED is a policy statement more than a state: nothing in the code deletes key_alias or key_store rows, and nothing should."],
      caveats=["'Verifiers should reject' for EXPIRED is about what a correct verifier does with the certificate's notAfter. The Key Manager does not reach out and stop anything.",
               "If you ever need to prune the database for size, understand that you are deciding which historical credentials stop verifying. That is a policy decision with a legal dimension, not a housekeeping task."],
      minutes="6 min")
footer(s)

# =================================================================== 11 ROTATION TIMELINE
s, y = slide("Rotation: what the overlap window actually buys you", kicker="Topic 3 — rotation",
             sub="Using the shipped BASE policy: 730 days validity, 30 days pre-expire.")
timeline(s, ML, y + 0.34, 7.95, [
 ("Key A — used for new signatures", 0.0, 0.48, C['green'], "700 days", 0),
 ("overlap", 0.48, 0.52, C['amber'], "30 days: verify only", 0),
 ("Key B — used for new signatures", 0.52, 1.0, C['primary'], "generated lazily at the boundary", 1),
], years=4, hrow=0.56, vgap=0.78)
_, tf = tb(s, ML + 8.30, y + 0.16, 3.93, 2.6)
para(tf, "WHAT HAPPENS AT THE BOUNDARY", size=9, color=C['accent'], bold=True, first=True)
for t in ["Key A is filtered out of the `current` list.",
          "The next signing request finds no current key and **generates Key B**.",
          "Key A is still valid: its certificate has not reached `notAfter`.",
          "Credentials signed with Key A keep verifying — for 30 more days by validity, and **indefinitely** as long as the certificate stays published."]:
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', t)
    ch = []
    for p in parts:
        if not p: continue
        if p.startswith('`'): ch.append((p[1:-1], C['primary'], False, False, F_MONO))
        elif p.startswith('**'): ch.append((p[2:-2], C['ink'], True))
        else: ch.append((p, C['ink2'], False))
    rich(tf, ch, size=9.4, space_before=7, line_spacing=1.24)
yy = y + 2.86
c1 = callout(s, ML, yy, 5.95, "**The trap.** A credential is valid for as long as its own `exp` says — often years. Your signing key rotates in two. So the certificate that verifies it **must outlive the key's signing life by the full credential lifetime.** That is why nothing is deleted.", kind='bad', size=10.3)
callout(s, ML + 6.28, yy, 5.95, "**The lever.** Shorten `key_validity_duration` and you rotate more often, limiting the blast radius of a compromise. Lengthen `pre_expire_days` and you widen the overlap, reducing the risk of a gap during an outage.", kind='good', size=10.3)
yy2 = yy + 1.30
rows = [
 ["Short validity, short overlap", "Small blast radius", "More rotations; a publication failure is felt quickly", "High-value, short-lived credentials"],
 ["Long validity, long overlap", "Fewer moving parts", "A compromised key is in play for longer", "Long-lived credentials, stable infrastructure"],
 ["Long validity, short overlap", "!!Worst of both", "Rare rotations, and little slack when one goes wrong", "!!Not recommended"],
]
table(s, ML, yy2, CW, ["Policy shape", "Gains you", "Costs you", "Fits"], rows,
      col_w=[2.8, 2.6, 4.4, 2.4], fsize=9.2, row_h=0.42, head_h=0.32)
notes(s, ["This slide is the heart of topic 3. Let the timeline sit on screen while you talk.",
          "The arithmetic with shipped defaults: 730 days validity, 30 days pre-expire, so a key is used for new signatures for 700 days and then remains valid for verification for 30 more.",
          "Now pose the question that matters: if an issued credential is valid for five years, and the signing key rotates every two, how does a verifier check a four-year-old credential? The answer is that the old certificate is still published in jwks.json and the DID document, because getAllCertificates returns every certificate the alias has ever had. Publication lifetime is driven by credential lifetime, not key lifetime.",
          "Then the policy table. Ask the room which row their deployment is in today and which row it should be in.",
          "If anyone asks about automated rotation: there is no scheduler. Rotation happens because the next signing request finds no current key. That is simple and robust, but it also means rotation is invisible until it happens — so monitor key_alias for new rows."],
      caveats=["Overlap does not protect you from a publication failure. If jwks.json or the DID document is stale or unreachable at the moment a verifier checks, the overlap window is irrelevant. Monitor those endpoints as production dependencies.",
               "Changing key_validity_duration affects only keys generated after the change. Existing keys keep the expiry they were born with."],
      questions=["Can we force a rotation early? — revokeKey expires the current key immediately, which triggers generation of a new one. See topic 8.",
                 "Do we need to re-sign old credentials after rotation? — No, and you must not; that would change them."],
      minutes="9 min")
footer(s)

# =================================================================== 12 ALREADY ISSUED
s, y = slide("What happens to credentials already issued?", kicker="Topic 3 — the question everyone asks",
             sub="Four events, four different answers. Getting these confused is how programmes lose trust.")
ev = [
 ("Key rotated\n(normal, scheduled)", "Nothing. Old credentials keep verifying.",
  ["The old certificate stays in `key_alias` and stays published.", "`kid` in the old credential still resolves.", "No re-issuance, no action for holders."],
  C['green'], "++NO IMPACT"),
 ("Key expired\n(past notAfter)", "Verification of anything signed by it should now fail.",
  ["A correct verifier checks the certificate's validity window.", "Credentials outliving their signing certificate become unverifiable.", "**Publication lifetime has to be planned around credential lifetime.**"],
  C['amber'], "~~PLAN FOR IT"),
 ("Key revoked\n(`PUT /revokeKey`)", "In MOSIP this *expires* the key — it does not destroy anything.",
  ["`key_expire_dtimes` is set to one minute ago.", "A new key is generated on the next request.", "**Already-issued credentials are NOT invalidated.**"],
  C['violet'], "!!NOT WHAT YOU THINK"),
 ("Credential revoked\n(status list)", "That single credential stops being accepted.",
  ["A bit is flipped in the status list credential.", "Verifiers that check status reject it.", "The signing key is untouched."],
  C['red'], "++THE RIGHT TOOL"),
]
bw = (CW - 3 * 0.20) / 4
for i, (t, headline, pts, col, badge) in enumerate(ev):
    x = ML + i * (bw + 0.20)
    rect(s, x, y, bw, 3.95, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.24, bw - 0.40, 0.62)
    parts = re.split(r'(`[^`]+`)', t)
    rich(t2, [((p[1:-1], col, True, False, F_MONO) if p.startswith('`') else (p, col, True))
              for p in parts if p], size=11.5, first=True, line_spacing=1.12)
    bl = badge[2:]
    bcol = C['green'] if badge.startswith('++') else (C['red'] if badge.startswith('!!') else C['amber'])
    chip(s, x + 0.20, y + 0.94, min(bw - 0.40, 0.30 + len(bl) * 0.085), 0.28, bl,
         bcol, C['white'], size=8.2)
    _, t3 = tb(s, x + 0.20, y + 1.34, bw - 0.40, 0.75)
    para(t3, headline, size=9.8, color=C['ink'], bold=True, first=True, line_spacing=1.24)
    cy = y + 2.18
    for p_ in pts:
        rect(s, x + 0.22, cy + 0.05, 0.07, 0.07, fill=col, shape=MSO_SHAPE.OVAL)
        _, t4 = tb(s, x + 0.40, cy, bw - 0.62, 0.8)
        parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', p_)
        ch = []
        for q in parts:
            if not q: continue
            if q.startswith('`'): ch.append((q[1:-1], col, False, False, F_MONO))
            elif q.startswith('**'): ch.append((q[2:-2], C['ink'], True))
            else: ch.append((q, C['muted'], False))
        rich(t4, ch, size=9.2, first=True, line_spacing=1.24)
        cy += 0.16 + max(1, -(-len(re.sub(r'[`*]', '', p_)) // 30)) * 0.152
yy = y + 4.20
callout(s, ML, yy, CW, "The distinction that matters in every design review: **revoking a key is not revoking a credential.** `revokeKey` rotates your signing key early. To stop a specific credential being accepted you flip its bit in the status list. Two mechanisms, two blast radii — and only one of them helps when a single citizen's credential must be withdrawn.", kind='bad', size=10.8)
notes(s, ["This is the slide to slow down on. The revokeKey behaviour genuinely surprises experienced people.",
          "Read the implementation with them if there is any doubt: revokeKey computes expireTime as now minus one minute and calls storeKeyInAlias with it. That is the entire effect. No row is deleted, no certificate is withdrawn, no credential is touched.",
          "So the practical rule: revokeKey is an emergency rotation, useful when you believe a key is compromised and you want to stop signing NEW things with it. It does nothing about what was already signed.",
          "To withdraw something already issued you need the status list — topic 6 — or, if the key itself is compromised and you must repudiate everything it signed, you have to stop publishing its certificate, which invalidates every credential it ever signed. That is the nuclear option in topic 8.",
          "Ask the room: for their own credential, which of these four events is most likely in the first year of operation? Usually the answer is rotation, and usually nobody has tested it."],
      caveats=["KERNEL/SIGN is explicitly not revocable — the code refuses. Know which aliases are protected before you plan an incident response.",
               "The 'key expired' column depends on the verifier actually checking the certificate validity window. Not every verifier does. Do not rely on expiry as an access control."],
      questions=["Can we invalidate every credential signed by one key? — Only by removing that certificate from publication, which is drastic and irreversible for holders. Status lists are the surgical tool."],
      minutes="8 min")
footer(s)

# =================================================================== 13 HSM ARCH
s, y = slide("HSM integration — how the keystore is actually reached", kicker="Topic 4 — HSM",
             sub="One interface, four implementations. Changing from a file to real hardware is a configuration change, not a code change.")
node(s, ML + 3.55, y, 5.10, 0.76, "Key Manager", "asks for a signature, never for a key",
     fill=C['primary'], fg=C['white'], tsize=12, ssize=8.4)
node(s, ML + 3.55, y + 1.12, 5.10, 0.66, "ECKeyStore  /  KeyStoreImpl",
     "one interface; implementation chosen by mosip.kernel.keymanager.hsm.keystore-type",
     fill=C['ink2'], fg=C['white'], tsize=11, ssize=8, mono=False)
arrow(s, ML + 6.10, y + 0.76, ML + 6.10, y + 1.12, C['ink2'], 1.4)
impls = [
 ("PKCS11", "SunPKCS11 provider\n+ HSM config file", "Real HSM, or SoftHSM locally", C['green'], True),
 ("PKCS12", "a `.p12` file on disk", "Local development only", C['amber'], False),
 ("Offline", "no keystore access", "Verification-only deployments", C['muted'], False),
 ("JCE", "vendor JCE provider\n(e.g. CloudHSM)", "Cloud HSM services", C['primary'], False),
]
bw = (CW - 3 * 0.22) / 4
for i, (t, how, when, col, rec) in enumerate(impls):
    x = ML + i * (bw + 0.22)
    yy = y + 2.14
    rect(s, x, yy, bw, 1.62, fill=C['surf'], line=col, lw=1.3 if rec else 1.0,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
    rect(s, x, yy, bw, 0.065, fill=col)
    _, t2 = tb(s, x + 0.18, yy + 0.20, bw - 0.36, 0.28)
    para(t2, t, size=12, color=col, bold=True, font=F_MONO, first=True)
    _, t3 = tb(s, x + 0.18, yy + 0.56, bw - 0.36, 0.55)
    parts = re.split(r'(`[^`]+`)', how)
    rich(t3, [((p[1:-1], col, False, False, F_MONO) if p.startswith('`') else (p, C['ink2'], False))
              for p in parts if p], size=9.4, first=True, line_spacing=1.22)
    _, t4 = tb(s, x + 0.18, yy + 1.16, bw - 0.36, 0.38)
    para(t4, when, size=8.8, color=C['muted'], italic=True, first=True, line_spacing=1.2)
    arrow(s, ML + 6.10, y + 1.78, x + bw / 2, yy - 0.02, C['faint'], 1.0)
    if rec:
        chip(s, x + bw - 1.08, yy - 0.15, 1.00, 0.26, "PRODUCTION", col, C['white'], size=7.6)
yy = y + 4.00
node(s, ML + 1.20, yy, 2.40, 0.62, "SoftHSM", "software, dev", fill=C['amber_l'],
     border=C['amber'], fg=C['amber'], tsize=10.5, ssize=8)
node(s, ML + 4.20, yy, 2.40, 0.62, "Network HSM", "e.g. Luna, nShield", fill=C['green_l'],
     border=C['green'], fg=C['green'], tsize=10.5, ssize=8)
node(s, ML + 7.20, yy, 2.40, 0.62, "Cloud HSM", "AWS / Azure managed", fill=C['primary_l'],
     border=C['primary'], fg=C['primary'], tsize=10.5, ssize=8)
_, tf = tb(s, ML, yy - 0.21, CW, 0.22)
para(tf, "WHAT SITS BEHIND PKCS#11 / JCE", size=9, color=C['muted'], bold=True, first=True)
codebox(s, ML + 10.18, yy - 0.02, 2.05, 0.92, [
 'keystore-type = PKCS11',
 'config-path   = hsm.cfg',
 'keystore-pass = ••••',
], size=7.6)
notes(s, ["The architectural point is that the Key Manager talks to one interface, ECKeyStore, and the implementation is selected by a property. Moving from a p12 file to a network HSM is a configuration and operations exercise, not a development one.",
          "PKCS11 is the path you want in production. It uses the JDK's SunPKCS11 provider with a config file that points at the vendor's shared library and a slot. SoftHSM implements the same interface in software, which is why you can develop against PKCS11 locally and deploy against real hardware with the same code path — a genuinely good design decision.",
          "PKCS12 is what the shipped Certify configuration uses for local development: CERTIFY_PKCS12/local.p12 with password 'local'. That is fine on a laptop and unacceptable anywhere else. Say that plainly.",
          "Offline exists for deployments that only verify and never sign. JCE covers vendor providers such as CloudHSM.",
          "The decision to force is: which of these three boxes at the bottom, and who operates it. That has procurement lead time, so it should be decided early."],
      caveats=["With the embedded shape from topic 1, every Certify pod needs the HSM client library, the config file and the credentials. That is a real constraint on container images and on secret distribution — plan it with whoever runs the cluster.",
               "SoftHSM is not a security control. Its key material is a file on disk protected by a PIN in configuration. Use it to prove the PKCS11 path works, never to protect anything real."],
      questions=["Can different environments use different keystore types? — Yes, and they should: PKCS12 locally, PKCS11 everywhere else.",
                 "Does the HSM become a throughput bottleneck? — It can. Signing rate is an HSM specification; get numbers before you size."],
      minutes="7 min")
footer(s)

# =================================================================== 14 HSM TRADEOFFS
s, y = slide("Software keystore or HSM — the honest trade-off", kicker="Topic 4 — production decision",
             sub="For an issuer whose signatures carry legal weight, this is not really a close call. But know what you are buying.")
rows = [
 ["**Where the private key is**", "A file on a disk you manage", "Inside tamper-resistant hardware", "The whole argument"],
 ["**Can an operator copy it?**", "!!Yes — read the file", "++No — it is non-exportable by design", "This is what an auditor asks"],
 ["**Compromise of a host**", "!!Key is gone; assume total compromise", "Attacker can *use* the key while they have access, but cannot *keep* it", "Changes incident response completely"],
 ["**Cost**", "++None", "Hardware or managed service, plus operations", "Budget and procurement lead time"],
 ["**Throughput**", "CPU-bound; scales with pods", "!!Bounded by the device; a hard ceiling", "Load-test before sizing"],
 ["**Availability**", "Same as the pod", "Extra dependency — needs HA, and a tested failover", "New single point of failure"],
 ["**Key ceremony / audit**", "Ad hoc", "++Formal, witnessed, evidenced", "Often a compliance requirement"],
 ["**Backup and recovery**", "Copy the file", "!!Vendor-specific; must be rehearsed", "The step teams skip and regret"],
 ["**Fits**", "Local development, CI", "Production issuance for a national credential", ""],
]
_tb = table(s, ML, y, CW, ["", "Software keystore (PKCS12)", "HSM (PKCS11 / JCE)", "Why it matters"], rows,
            col_w=[2.5, 3.4, 3.9, 3.4], fsize=9.3, row_h=0.46, head_h=0.34)
yy = _tb + 0.22
callout(s, ML, yy, CW, "The row that decides it is the third one. With a file-based keystore, a host compromise means the key is **copied** and you can never again prove that a signature came from you. With an HSM, the same compromise means the attacker could **use** the key while they were inside — bad, but bounded, and revocable. That difference is the entire value proposition.", kind='spec', size=10.6)
notes(s, ["Frame this as a risk conversation rather than a technology preference, and let the room argue.",
          "Row 3 is the one to dwell on. Exfiltration versus use. A stolen file is forever; misuse of an HSM-held key ends when access ends. For a national issuer that distinction is the difference between rotating a key and repudiating years of credentials.",
          "Be balanced about the costs. An HSM is a new hard dependency with its own availability story, its own failover drill and its own backup procedure — and backup is genuinely hard and vendor-specific. Teams buy the hardware and never rehearse recovery.",
          "The throughput row matters wherever issuance volume is high, the HSM signing rate is a design input, not an afterthought.",
          "Land the ask: whoever owns infrastructure needs to start the HSM conversation now, because procurement and key ceremony take months, not sprints."],
      caveats=["A managed cloud HSM removes some operational burden and adds a data-residency question — which is a live question for any government issuer.",
               "HSM does not protect against an authorised caller misusing the signing API. Role-based access and monitoring still matter; the hardware only stops exfiltration."],
      minutes="5 min")
footer(s)

# =================================================================== 15 TRUST ANCHOR
s, y = slide("How a public key becomes a trust anchor", kicker="Topic 5 — trust anchors",
             sub="A key is only useful to a verifier if the verifier can find it and has a reason to believe it.")
stages = [
 ("1  Key exists", "`key_alias` + `key_store`,\ncertificate signed by\nthe module key", C['ink']),
 ("2  Certificate exported", "`getAllCertificates(appId, refId)`\nreturns every certificate\nthis alias has ever had", C['primary']),
 ("3  Published", "Certify serves\n`/.well-known/jwks.json`\nand `/.well-known/did.json`", C['accent']),
 ("4  Discovered", "Verifier resolves the `kid`\nor the DID, and fetches\nthe public key", C['violet']),
 ("5  Trusted", "Verifier's **policy** says\nthis issuer is acceptable\nfor this claim", C['green']),
]
n = len(stages); gap = 0.22
bw = (CW - gap * (n - 1)) / n
for i, (t, d, col) in enumerate(stages):
    x = ML + i * (bw + gap)
    rect(s, x, y, bw, 1.95, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.055)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.18, y + 0.24, bw - 0.36, 0.3)
    para(t2, t, size=11.5, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.18, y + 0.62, bw - 0.36, 1.2)
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', d)
    ch = []
    for p in parts:
        if not p: continue
        if p.startswith('`'): ch.append((p[1:-1], col, False, False, F_MONO))
        elif p.startswith('**'): ch.append((p[2:-2], C['ink'], True))
        else: ch.append((p, C['muted'], False))
    rich(t3, ch, size=8.8, first=True, line_spacing=1.28)
    if i < n - 1:
        arrow(s, x + bw + 0.02, y + 1.0, x + bw + gap - 0.02, y + 1.0, C['ink2'], 1.3)
yy = y + 2.25
callout(s, ML, yy, CW, "Steps 1 to 4 are engineering. **Step 5 is governance** — and nothing in the Key Manager can produce it. A perfectly resolvable key from an issuer nobody has agreed to trust is still worthless. Someone has to maintain the trust list, and verifiers outside the deployment have to learn about it.", kind='warn', size=10.6)
yy = yy + 0.92
codebox(s, ML, yy, 6.15, 2.05, [
 'GET /.well-known/did.json',
 '{',
 '  "@context": ["https://www.w3.org/ns/did/v1"],',
 '  "id": "did:web:certify.example.org",',
 '  "assertionMethod": ["did:web:certify.example.org"],',
 '  "verificationMethod": [{',
 '    "id": "did:web:certify.example.org#key-0",',
 '    "type": "Ed25519VerificationKey2020",',
 '    "controller": "did:web:certify.example.org",',
 '    "publicKeyMultibase": "z6Mk…"       // base58btc',
 '  }]',
 '}',
], label="DID DOCUMENT — SERVED BY CERTIFY", size=8.4, hl=[4, 9])
codebox(s, ML + 6.46, yy, 5.77, 2.05, [
 'GET /.well-known/jwks.json',
 '{ "keys": [',
 '  { "kid": "…", "kty": "RSA", "alg": "RS256",',
 '    "use": "sig", "x5c": ["MIIC…"],',
 '    "exp": 1861920000 },        // current key',
 '  { "kid": "…", "kty": "RSA", "alg": "RS256",',
 '    "use": "sig", "x5c": ["MIIB…"],',
 '    "exp": 1798848000 }         // LAST YEAR\'S key',
 '] }',
], label="JWKS — BUILT FROM getAllCertificates", size=8.4, hl=[7])
notes(s, ["Walk the five stages, then land on the callout: the first four are code, the fifth is a decision made by humans in a trust framework.",
          "The DID document is generated by Certify's DIDDocumentUtil from the configured did-url and the certificates in the Key Manager. Ed25519 keys are published as Ed25519VerificationKey2020 with a base58btc publicKeyMultibase; others go out as JsonWebKey2020.",
          "The jwks.json endpoint is built by iterating the key-alias-mapper and calling getAllCertificates for each. That is why the highlighted second entry — last year's key — is there, and that is the mechanism that makes rotation non-breaking. Show this to anyone who doubts the retention argument from topic 3.",
          "did:web is worth explaining in one line: the DID resolves to an HTTPS URL on the domain in the identifier, so the security of the anchor is the security of that domain and its TLS. Whoever controls DNS for that host controls the trust anchor.",
          "The domain chosen here is a long-term commitment. Changing it later invalidates every credential that references it."],
      caveats=["did:web trust is domain trust. Protect DNS, protect TLS certificate issuance for that host, and monitor the endpoint. A takeover of that hostname is a takeover of the issuer's identity.",
               "Certify serves did.json and jwks.json under /.well-known/. If a CDN, WAF or reverse proxy caches or challenges those paths, verifiers fail in ways that look like credential errors. This is a genuinely common production failure."],
      questions=["Should we use did:web or an X.509 chain from a national CA? — Both are legitimate; a government issuer often needs the CA chain for legal recognition. generateCSR plus uploadCertificate is the path."],
      minutes="8 min")
footer(s)

# =================================================================== 16 ROTATING ANCHOR
s, y = slide("Rotating a trust anchor without breaking anyone", kicker="Topic 5 — safe rotation",
             sub="The order of operations matters — done in the wrong order, every verifier fails at once.")
steps = [
 ("Publication precedes signing", "The new key is generated and its certificate appears in `jwks.json` / `did.json` **before** anything is signed with it.",
  "Verifiers that cache the document have time to pick it up.", C['green']),
 ("The old certificate stays published", "The previous certificate remains in the document. `getAllCertificates` does this for you — do not filter it out.",
  "Everything signed last year keeps verifying.", C['primary']),
 ("Overlap exceeds cache TTLs", "Verifiers and CDNs cache these documents. The overlap window has to be longer than the longest cache TTL in the chain.",
  "A 30-day overlap and a 24-hour cache is comfortable. A 1-hour overlap is not.", C['amber']),
 ("A `kid` is never reused", "A new key gets a new key id. Reusing one makes old credentials resolve to the wrong public key.",
  "Silent, confusing verification failures.", C['red']),
 ("The endpoints are monitored", "`/.well-known/jwks.json` and `did.json` are production dependencies with an availability target.",
  "If they are down, verification is down — everywhere, for everyone.", C['violet']),
]
cy = y
for i, (t, d, why, col) in enumerate(steps):
    rect(s, ML, cy, CW, 0.80, fill=C['surf'] if i % 2 == 0 else C['white'],
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
    rect(s, ML, cy, 0.055, 0.80, fill=col)
    b = rect(s, ML + 0.22, cy + 0.22, 0.36, 0.36, fill=col, shape=MSO_SHAPE.OVAL)
    tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run(); rb.text = str(i + 1); rb.font.size = Pt(11); rb.font.bold = True
    rb.font.color.rgb = C['white']; rb.font.name = F_SANS
    _, t2 = tb(s, ML + 0.72, cy + 0.10, 2.55, 0.62, anchor=MSO_ANCHOR.MIDDLE)
    parts = re.split(r'(`[^`]+`)', t)
    rich(t2, [((p[1:-1], col, True, False, F_MONO) if p.startswith('`') else (p, col, True))
              for p in parts if p], size=11, first=True, line_spacing=1.14)
    _, t3 = tb(s, ML + 3.40, cy + 0.08, 5.15, 0.66, anchor=MSO_ANCHOR.MIDDLE)
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', d)
    ch = []
    for p in parts:
        if not p: continue
        if p.startswith('`'): ch.append((p[1:-1], C['primary'], False, False, F_MONO))
        elif p.startswith('**'): ch.append((p[2:-2], C['ink'], True))
        else: ch.append((p, C['ink2'], False))
    rich(t3, ch, size=9.4, first=True, line_spacing=1.24)
    _, t4 = tb(s, ML + 8.75, cy + 0.08, 3.40, 0.66, anchor=MSO_ANCHOR.MIDDLE)
    para(t4, why, size=9.0, color=C['muted'], italic=True, first=True, line_spacing=1.24)
    cy += 0.92
_, tf = tb(s, ML + 3.40, y - 0.26, 5.15, 0.24)
para(tf, "THE RULE", size=8.6, color=C['muted'], bold=True, first=True)
_, tf = tb(s, ML + 8.75, y - 0.26, 3.40, 0.24)
para(tf, "IF YOU GET IT WRONG", size=8.6, color=C['muted'], bold=True, first=True)
notes(s, ["This is a runbook, not a concept. Suggest the team turns it into an actual checklist.",
          "Rule 3 is the one that catches people. Overlap must exceed the longest cache TTL anywhere in the chain — verifier caches, CDN caches, and the Mimoto-style caches on the wallet side. If an overlap of 30 days sounds generous, remember that a badly configured CDN can serve a stale document for a week.",
          "Rule 4 deserves emphasis: kid is how a credential points at the key that signed it. Reuse breaks that pointer silently, and the resulting failures look like tampering rather than misconfiguration.",
          "Rule 5 is an availability ask, not a security one. Put jwks.json and did.json on the same monitoring and alerting as the credential endpoint. Most teams do not, and then spend a day debugging 'random verification failures'.",
          "Ask: who owns these two URLs today? Frequently the answer is nobody, which is the finding."],
      caveats=["Because rotation is lazy — triggered by the first signing request after the boundary — 'publish first, sign later' is not automatic. If you need a controlled rotation, generate the key deliberately and confirm it appears in the published documents before traffic reaches it.",
               "Where an external CA chain is used rather than the self-signed ROOT, rotation also involves the CA's timelines. Add those to the plan."],
      minutes="6 min")
footer(s)

# =================================================================== 17 STATUS LIST
s, y = slide("Status list mechanics", kicker="Topic 6 — revocation and suspension",
             sub="How one credential out of a million is withdrawn, without telling the verifier who asked.")
# bitstring visual
_, tf = tb(s, ML, y, 6.15, 0.26)
para(tf, "A STATUS LIST CREDENTIAL IS A BITSTRING, COMPRESSED AND SIGNED", size=9,
     color=C['muted'], bold=True, first=True)
cellw = 0.31
for i in range(18):
    x = ML + i * (cellw + 0.035)
    on = i in (4, 11)
    rect(s, x, y + 0.36, cellw, 0.42, fill=C['red'] if on else C['surf2'],
         line=C['line'], lw=0.8)
    _, t2 = tb(s, x, y + 0.36, cellw, 0.42, wrap=False, anchor=MSO_ANCHOR.MIDDLE)
    para(t2, "1" if on else "0", size=9.5, color=C['white'] if on else C['faint'],
         bold=True, align=PP_ALIGN.CENTER, font=F_MONO, first=True)
    if on:
        _, t3 = tb(s, x - 0.35, y + 0.82, 1.0, 0.24, wrap=False)
        para(t3, "idx %d" % i, size=7.6, color=C['red'], bold=True,
             align=PP_ALIGN.CENTER, first=True)
_, tf = tb(s, ML, y + 1.08, 6.15, 0.62)
para(tf, "Every credential of a type gets an index at issuance. Bit 0 = valid, bit 1 = revoked. The verifier downloads the whole list, so the issuer never learns which credential was checked.",
     size=9.4, color=C['ink2'], first=True, line_spacing=1.24)
codebox(s, ML + 6.46, y, 5.77, 1.92, [
 '// inside the issued credential',
 '"credentialStatus": {',
 '  "type": "BitstringStatusListEntry",',
 '  "statusPurpose": "revocation",',
 '  "statusListIndex": "11",',
 '  "statusListCredential":',
 '     "https://certify.example.org/status/ab12"',
 '}',
], label="THE POINTER THE VERIFIER FOLLOWS", size=8.4, hl=[4, 6])
yy = y + 2.02
sequence(s, ["Holder", "Certify", "Status list store", "Verifier"],
 [(1, 2, "At issuance: claim the next free index"),
  (2, 1, "`statusListCredentialId` + `statusListIndex`", 'resp'),
  (1, 0, "Credential, carrying `credentialStatus`", 'resp'),
  (1, 2, "Administrator revokes — set the bit at that index"),
  (2, 2, "Re-encode the bitstring, re-sign the status list VC", 'self'),
  (3, 2, "`GET` the status list credential URL"),
  (2, 3, "signed status list VC", 'resp'),
  (3, 3, "Verify signature, decompress, read the bit", 'self'),
 ], top=yy, height=2.86)
notes(s, ["Start with the bitstring picture. It is the simplest possible idea: one bit per credential, and a URL that says where the bitstring lives.",
          "The privacy property is the reason this design exists. The verifier downloads the entire list, so the issuer's server sees a request for a list, not a request about a person. Contrast that with OCSP-style per-credential lookups, which leak exactly who is being checked and when. For a national credential that difference is material.",
          "In Certify, status list credentials are rows in the database with a vc_document column, served by id. The default size is 16 KB of bitstring, and indices are handed out by a database index provider. Allowed status purposes are configured — the shipped configuration allows 'revocation'.",
          "Draw attention to step 5: the status list is itself a Verifiable Credential and it is re-signed every time a bit changes. That is the hook into the next slide.",
          "Ask: who will have authority to flip a bit, and through what interface? Revocation authority is a governance question that usually has no owner on day one."],
      caveats=["The verifier must actually check status. Nothing forces it. If your verifiers skip the check, revocation does nothing — and note that Inji Wallet does not perform revocation checking today, so this lands on the verifier side.",
               "Downloading a full list costs bandwidth. 16 KB is small, but at national scale you will have many lists; plan caching and CDN behaviour, and remember caching delays revocation."],
      minutes="6 min")
footer(s)

# =================================================================== 18 STATUS vs KEYS
s, y = slide("Status lists and key rotation — where they touch", kicker="Topic 6 — the interaction",
             sub="Two independent mechanisms, with exactly one dependency between them. Miss it and revocation silently stops working.")
card(s, ML, y, 5.95, 2.25, "The dependency", [
 "The status list credential is **itself a signed VC**.",
 "Certify signs it with its own configured key: `mosip.certify.status-list.signature-crypto-suite` (default `Ed25519Signature2020`), key reference `ED25519_SIGN`.",
 "So when that key rotates, **newly published status lists are signed by the new key** — and verifiers must be able to resolve it.",
 "If the new key is not yet published, status checks fail even though the credentials themselves are fine.",
], accent=C['red'], tint=C['red_l'], size=10.0)
card(s, ML + 6.28, y, 5.95, 2.25, "What that means in practice", [
 "The status list signing key is on the **same publication path** as the credential signing key — `jwks.json` and the DID document.",
 "Rotating it is subject to the same order of operations from topic 5.",
 "A failure here looks like 'the credential is revoked' or 'status unavailable' to the verifier, not like a key problem.",
 "Monitor status list URLs alongside the well-known endpoints.",
], accent=C['accent'], tint=C['accent_l'], size=10.0)
yy = y + 2.50
rows = [
 ["**What it withdraws**", "One credential", "Nothing already issued — only future signatures"],
 ["**Blast radius**", "A single holder", "Every future credential from that alias"],
 ["**Who acts**", "An administrator with revocation authority", "An operator with Key Manager access"],
 ["**Verifier sees**", "`statusListIndex` bit set to 1", "A new `kid` on newly issued credentials"],
 ["**Reversible?**", "++Yes — clear the bit", "!!No — the old key is not reinstated as current"],
 ["**Applies when**", "A credential was issued in error, or the holder's entitlement ended", "A key is suspected compromised, or a scheduled rotation is due"],
 ["**Does NOT do**", "!!Stop a verifier that never checks status", "!!Invalidate anything already signed"],
]
table(s, ML, yy, CW, ["", "Status list revocation", "Key revocation (`PUT /revokeKey`)"], rows,
      col_w=[2.6, 4.8, 4.8], fsize=9.4, row_h=0.46, head_h=0.34)
notes(s, ["The left card is the non-obvious dependency and the reason this slide exists. Nobody expects the revocation mechanism to have a key dependency, and then one day status checks start failing after a routine rotation.",
          "Read the property names out: mosip.certify.status-list.signature-crypto-suite defaults to Ed25519Signature2020 and mosip.certify.status-list.key-manager-ref-id defaults to ED25519_SIGN. Those are real defaults in the shipped configuration.",
          "The comparison table is the takeaway. Print it. The 'Reversible?' row is worth pausing on — status list revocation is reversible by clearing a bit; key revocation is not reversible in the sense people expect, because the old key does not become current again.",
          "The last row is the honest one. Neither mechanism does the thing people most often assume: status lists do nothing if verifiers skip the check, and key revocation does nothing about already-issued credentials."],
      caveats=["Suspension versus revocation: the status purpose is configurable, and the shipped configuration allows only 'revocation'. Where suspension is needed — temporary withdrawal — that is a configuration change plus a verifier-side behaviour to agree.",
               "Re-signing a status list on every bit change means status list updates are signing operations. At high revocation volume that is HSM load; batch if you can."],
      questions=["If a signing key is compromised, do we revoke every credential it signed via status lists? — That is exactly the question in topic 8, and usually the answer is yes, in batches."],
      minutes="5 min")
footer(s)

# =================================================================== 19 MULTI-TENANT
s, y = slide("Multi-issuer and multi-tenant key isolation", kicker="Topic 7 — sharing one Key Manager",
             sub="Isolation is by `app_id` and `ref_id`. Understand exactly how strong that is before you rely on it.")
# isolation diagram
node(s, ML + 3.40, y, 5.45, 0.70, "One Key Manager instance", fill=C['primary'],
     fg=C['white'], tsize=12)
tenants = [("Tenant A", "CERTIFY_A_VC_SIGN_RSA", C['accent']),
           ("Tenant B", "CERTIFY_B_VC_SIGN_RSA", C['violet']),
           ("Tenant C", "CERTIFY_C_VC_SIGN_ED25519", C['amber'])]
bw = 3.55
for i, (t, alias, col) in enumerate(tenants):
    x = ML + i * (bw + 0.70)
    yy = y + 1.25
    zone(s, x, yy, bw, 1.85, t, col, None)
    node(s, x + 0.22, yy + 0.42, bw - 0.44, 0.52, alias, fill=col, fg=C['white'],
         tsize=8.8, mono=True)
    _, t2 = tb(s, x + 0.22, yy + 1.06, bw - 0.44, 0.65)
    para(t2, "own app_id → own module key,\nown policy row, own certificates",
         size=8.8, color=C['muted'], align=PP_ALIGN.CENTER, first=True, line_spacing=1.24)
    arrow(s, ML + 6.12, y + 0.70, x + bw / 2, yy - 0.02, C['faint'], 1.0)
yy = y + 3.35
rows = [
 ["Separate key material", "++Strong", "Different `app_id` means a different module key in the keystore, and different rows in `key_store`"],
 ["Separate policy", "++Strong", "`key_policy_def` is keyed on `app_id` — different validity and rotation per tenant"],
 ["Separate certificates and `kid`s", "++Strong", "Each tenant publishes its own certificates; a verifier can pin one tenant"],
 ["Separate API authorisation", "~~Depends on you", "Role-based access is configured, not automatic. A caller with the signing role can ask for another tenant's alias unless you restrict it"],
 ["Separate HSM partition", "~~Depends on the HSM", "One keystore configuration per Key Manager instance. True partition isolation usually means a separate instance"],
 ["Separate database", "!!No", "One `keymgr` schema holds all tenants' aliases and wrapped keys"],
 ["Separate blast radius on compromise", "!!No", "Compromise of the HSM credentials or the host reaches every tenant on that instance"],
]
table(s, ML, yy, CW, ["Isolation dimension", "How strong", "Why"], rows,
      col_w=[3.4, 2.0, 6.8], fsize=9.2, row_h=0.42, head_h=0.32)
notes(s, ["Be precise here, because 'multi-tenant' means different things to different people and the honest answer is 'logically isolated, physically shared'.",
          "The top three rows are genuinely strong: different app_id gives you different module keys, different policy and different published certificates. A verifier can pin exactly one tenant's key and ignore the rest.",
          "The bottom three rows are the caveats. One database, one keystore configuration, one host. If the threat model includes 'one tenant's operator should not be able to reach another tenant's keys', logical separation on a shared instance is not enough — you need separate Key Manager instances, and probably separate HSM partitions.",
          "The question is concrete: will different agencies issue through one Certify deployment or several? If several agencies with different legal accountability share one instance, expect that to be challenged in a security review."],
      caveats=["Being trusted outside the deployment is a separate question from isolation — it is on the next slide.",
               "Role configuration (mosip.role.keymanager.*) is a list of role names per endpoint. It does not express 'this caller may only use these aliases'. If you need that, it is additional work."],
      minutes="5 min")
footer(s)

# =================================================================== 20 EXTERNAL TRUST
s, y = slide("Being trusted outside your own deployment", kicker="Topic 7 — external trust",
             sub="Everything so far makes a credential verifiable. This is what makes it *accepted*.")
cards = [
 ("Resolvable keys", ["A stable, monitored `did:web` domain or JWKS URL.",
                      "Every historical certificate still published.",
                      "No redirects, no WAF challenge, no bot protection on those paths."], C['primary']),
 ("A recognised chain", ["Self-signed ROOT is fine inside your own trust boundary.",
                         "Outside it, verifiers usually need a chain to a CA they already trust.",
                         "`POST /generateCSR` → external CA signs → `POST /uploadCertificate`."], C['accent']),
 ("A published profile", ["Which formats, which algorithms, which `kid` resolution path.",
                          "Credential types and their claim definitions.",
                          "Rotation cadence and overlap, so verifiers can size their caches."], C['violet']),
 ("A governance answer", ["Who may issue on behalf of the programme, and who says so.",
                          "How a verifier learns the list and how it is updated.",
                          "What happens, contractually, when a key is compromised."], C['green']),
]
bw = (CW - 3 * 0.20) / 4
for i, (t, pts, col) in enumerate(cards):
    x = ML + i * (bw + 0.20)
    rect(s, x, y, bw, 2.85, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.20, y + 0.24, bw - 0.40, 0.32)
    para(t2, t, size=12, color=col, bold=True, first=True)
    cy = y + 0.70
    for p_ in pts:
        rect(s, x + 0.22, cy + 0.05, 0.07, 0.07, fill=col, shape=MSO_SHAPE.OVAL)
        _, t3 = tb(s, x + 0.40, cy, bw - 0.62, 0.9)
        parts = re.split(r'(`[^`]+`)', p_)
        rich(t3, [((q[1:-1], col, False, False, F_MONO) if q.startswith('`') else (q, C['ink2'], False))
                  for q in parts if q], size=9.3, first=True, line_spacing=1.26)
        cy += 0.16 + max(1, -(-len(re.sub(r'[`*]', '', p_)) // 30)) * 0.155
yy = y + 3.10
callout(s, ML, yy, CW, "Three of these four are engineering work you can start this month. The fourth — governance — is the one that takes a year and blocks the others from mattering, and it needs a named owner.", kind='spec', size=10.8)
yy += 0.85
_, tf = tb(s, ML, yy, CW, 0.28)
para(tf, "DISCUSSION — FOR YOUR OWN DEPLOYMENT", size=9, color=C['accent'], bold=True, first=True)
qs = ["Self-signed ROOT, or a chain to a nationally recognised CA?",
      "Which domain hosts the DID document, and who controls its DNS?",
      "One Key Manager for all issuers, or one per agency?",
      "Who is authorised to revoke, and through which interface?"]
for i, q in enumerate(qs):
    x = ML + (i % 2) * (CW / 2 + 0.10)
    yy2 = yy + 0.32 + (i // 2) * 0.42
    rect(s, x, yy2 + 0.06, 0.16, 0.16, fill=None, line=C['accent'], lw=1.3)
    _, t2 = tb(s, x + 0.34, yy2, CW / 2 - 0.50, 0.36)
    para(t2, q, size=10, color=C['ink2'], first=True)
notes(s, ["Close topic 7 by widening the frame: everything in this session makes credentials verifiable, and verifiability is necessary but not sufficient. Acceptance is a governance product.",
          "The 'recognised chain' card is where a government issuer usually differs from a pilot. A self-signed root is fine while one organisation is both issuer and verifier. The moment a bank, an airline or another country has to accept the credential, they will ask whose CA signed it. generateCSR plus uploadCertificate is the mechanism; the CA relationship is the work.",
          "Run the four discussion questions as an actual discussion. Capture answers and owners on a flipchart — they feed straight into Day 3's security hardening session.",
          "If the room does not know which CA applies, that is itself the most useful output of the session."],
      caveats=["Do not let 'we will decide the CA later' pass quietly. CA onboarding has months of lead time and it constrains the key algorithms you may use.",
               "The published profile is cheap to write and saves enormous time with every external partner. Offer to draft it."],
      minutes="5 min")
footer(s)

# =================================================================== 21 INCIDENT
s, y = slide("A signing key is suspected compromised", kicker="Topic 8 — incident response",
             sub="What you do, in what order, and what each step actually achieves.")
timeline(s, ML, y + 0.30, 7.60, [
 ("Contain", 0.0, 0.20, C['red'], "minutes", 0),
 ("Signing stops", 0.20, 0.40, C['amber'], "PUT /revokeKey", 0),
 ("Assess", 0.40, 0.66, C['violet'], "what did it sign?", 1),
 ("Decide", 0.66, 0.84, C['primary'], "rotate, or repudiate?", 1),
 ("Publish", 0.84, 1.0, C['green'], "verifiers, holders", 2),
], years=5, hrow=0.54, vgap=0.74, xlabel="T+%d")
_, tf = tb(s, ML + 7.95, y + 0.26, 4.28, 2.8)
para(tf, "WHAT EACH STEP BUYS YOU", size=9, color=C['accent'], bold=True, first=True)
for t, d in [("Contain", "HSM access is cut, the HSM PIN rotated, and the service credentials that could call the signing API revoked."),
             ("Signing stops", "`revokeKey` expires the key now. The next request generates a new one. **Already-issued credentials are untouched.**"),
             ("Assess", "`cert_thumbprint` plus the issuance logs give the list of every credential signed by that key."),
             ("Decide", "Rotate only, or withdraw what the key signed. See the next slide."),
             ("Publish", "The new certificate goes into `jwks.json` / `did.json`, and verifiers are told what changed and when.")]:
    parts = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', d)
    ch = [(t + " — ", C['ink'], True)]
    for p in parts:
        if not p: continue
        if p.startswith('`'): ch.append((p[1:-1], C['primary'], False, False, F_MONO))
        elif p.startswith('**'): ch.append((p[2:-2], C['red'], True))
        else: ch.append((p, C['muted'], False))
    rich(tf, ch, size=9.0, space_before=6, line_spacing=1.24)
yy = y + 3.10
callout(s, ML, yy, CW, "The uncomfortable truth to say out loud in the drill: **revokeKey stops the bleeding, it does not heal the wound.** It prevents further signatures with the compromised key. Everything that key already signed is still cryptographically valid, and will stay valid as long as its certificate is published.", kind='bad', size=10.6)
yy += 0.92
rows = [
 ["Was the key in an HSM?", "The attacker could **use** it while they had access, but not take a copy. Scope is the access window.",
  "Rotate, audit signatures inside the window, keep publishing the old certificate"],
 ["Was it a file-based keystore?", "!!Assume the private key was **copied**. The attacker can sign forever, anywhere.",
  "Repudiate: stop publishing that certificate and re-issue affected credentials"],
]
table(s, ML, yy, CW, ["First question to answer", "What it means", "What it usually leads to"], rows,
      col_w=[3.0, 5.2, 4.0], fsize=9.4, row_h=0.62, head_h=0.34)
notes(s, ["Run this as a drill, not a lecture. Give the room the scenario — 'a Certify pod was compromised, we do not know for how long' — and let them walk the timeline.",
          "Step order matters. Containment comes before revocation: if the attacker still has HSM access, generating a new key just gives them a second key.",
          "The Assess step is where preparation pays. If you are not recording cert_thumbprint against every issued credential, you cannot answer 'what did this key sign', and every subsequent decision becomes guesswork. Make that a logging requirement today.",
          "The bottom table is the fork in the road, and it is decided by a choice made months earlier: HSM or file. That is the strongest practical argument for the HSM, stronger than any compliance checkbox.",
          "Land the ask: this is worth rehearsing once, in a non-production environment, before go-live. A drill takes an afternoon and finds the gaps."],
      caveats=["KERNEL/SIGN cannot be revoked through the API — the code refuses. Know which aliases are protected before the incident, not during it.",
               "Revocation is not reversible in the way people expect: the old key does not come back as current. If you revoke by mistake you get an unplanned rotation, which is survivable but noisy."],
      questions=["How fast can trust actually be withdrawn? — Stopping new signatures is immediate. Withdrawing already-issued credentials is bounded by verifier cache TTLs, so hours to days. Plan for days."],
      minutes="6 min")
footer(s)

# =================================================================== 22 BLAST RADIUS
s, y = slide("Rotate or repudiate — and what it costs holders", kicker="Topic 8 — the hard call",
             sub="Three responses, three very different impacts on citizens who did nothing wrong.")
opts = [
 ("Rotate only", "The key stops being used. Its certificate stays published.",
  ["++No holder is affected", "++No re-issuance", "!!Anything the attacker signed stays valid",
   "Applies when: the key was HSM-held and the access window is known and empty"], C['green']),
 ("Rotate + status-list the suspects", "The key stops being used, and the specific credentials believed fraudulent are revoked.",
  ["++Only affected holders are impacted", "~~Needs a reliable list of what to revoke",
   "~~Only works if verifiers check status", "Applies when: the fraudulent credentials can be identified"], C['amber']),
 ("Repudiate the key", "Its certificate stops being published entirely.",
  ["!!**Every** credential it ever signed stops verifying", "!!Mass re-issuance; citizens are locked out meanwhile",
   "++The only option that truly withdraws the attacker's signatures",
   "Applies when: the private key was copied"], C['red']),
]
bw = (CW - 2 * 0.24) / 3
for i, (t, d, pts, col) in enumerate(opts):
    x = ML + i * (bw + 0.24)
    rect(s, x, y, bw, 3.55, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.045)
    rect(s, x, y, bw, 0.07, fill=col)
    _, t2 = tb(s, x + 0.22, y + 0.26, bw - 0.44, 0.34)
    para(t2, t, size=13.5, color=col, bold=True, first=True)
    _, t3 = tb(s, x + 0.22, y + 0.68, bw - 0.44, 0.70)
    para(t3, d, size=9.8, color=C['ink2'], first=True, line_spacing=1.26)
    cy = y + 1.52
    for p_ in pts:
        pc, txt = C['ink2'], p_
        if txt.startswith('++'): pc, txt = C['green'], txt[2:]
        elif txt.startswith('!!'): pc, txt = C['red'], txt[2:]
        elif txt.startswith('~~'): pc, txt = C['amber'], txt[2:]
        rect(s, x + 0.22, cy + 0.05, 0.08, 0.08, fill=pc, shape=MSO_SHAPE.OVAL)
        _, t4 = tb(s, x + 0.42, cy, bw - 0.64, 0.9)
        parts = re.split(r'(\*\*[^*]+\*\*)', txt)
        rich(t4, [((q[2:-2], pc, True) if q.startswith('**') else (q, pc if pc is not C['ink2'] else C['muted'], False))
                  for q in parts if q], size=9.3, first=True, line_spacing=1.26)
        cy += 0.16 + max(1, -(-len(re.sub(r'[*]', '', txt)) // 28)) * 0.155
yy = y + 3.80
callout(s, ML, yy, CW, "Notice who pays. Rotating costs you an afternoon. Repudiating costs **every citizen holding a credential signed by that key** their access, until re-issuance completes. That asymmetry is why the HSM decision in topic 4 is a citizen-impact decision, not an infrastructure one.", kind='spec', size=10.8)
notes(s, ["This is the slide that connects the whole session together. Make the connection explicit.",
          "Walk the three options in order of increasing pain. The middle one — rotate plus targeted status-list revocation — is where you want to be, and it is only available if two things are true: you can identify the fraudulent credentials, and your verifiers actually check status.",
          "The third option is the one nobody plans for. Un-publishing a certificate breaks every credential it signed, including millions issued legitimately. For a national credential that is a front-page event.",
          "Now tie it back: whether you ever face option three is decided by the keystore choice made in topic 4, and whether option two is available is decided by the status list design in topic 6 and by verifier behaviour. Every earlier topic converges here.",
          "Close topic 8 by asking the room to estimate, for their planned volume, how long a mass re-issuance would take. The number is usually sobering and it makes the HSM business case by itself."],
      caveats=["Option two depends on verifiers checking status. If a significant share of verifiers do not, option two degrades towards option one and you are relying on the attacker not using what they stole.",
               "Do not treat option three as theoretical. Write the runbook for it, including holder communications, before you need it."],
      minutes="5 min")
footer(s)

# =================================================================== 23 RECAP
s, y = slide("The model in one slide", kicker="Recap",
             sub="If the room remembers six things from these 90 minutes, make it these.")
items = [
 ("Three tiers, one direction", "ROOT signs module keys; module keys sign base keys and wrap their private keys; base keys sign credentials.", C['primary']),
 ("The application asks for a signature, never for a key", "Certify maps an algorithm to an `app_id` + `ref_id` and calls the Key Manager. Key material never crosses that boundary.", C['accent']),
 ("Nothing is ever deleted", "`key_alias` and `key_store` are append-only, and `getAllCertificates` publishes the history. That is what lets a three-year-old credential still verify.", C['violet']),
 ("Rotation is lazy and overlapping", "`pre_expire_days` takes a key out of service before it expires. The next signing request creates its successor. Publication lifetime must exceed credential lifetime.", C['amber']),
 ("Revoking a key is not revoking a credential", "`revokeKey` is an emergency rotation. Withdrawing one credential is a status-list bit — and the status list is itself a signed VC with its own key.", C['red']),
 ("HSM or file decides your worst day", "HSM-held keys can be misused but not copied. File-based keys can be copied, and that is the difference between rotating and repudiating.", C['green']),
]
for i, (t, d, col) in enumerate(items):
    x = ML + (i % 2) * (CW / 2 + 0.12)
    yy = y + (i // 2) * 1.42
    wid = CW / 2 - 0.12
    rect(s, x, yy, wid, 1.26, fill=C['surf'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.065)
    rect(s, x, yy, 0.055, 1.26, fill=col)
    b = rect(s, x + 0.22, yy + 0.18, 0.32, 0.32, fill=col, shape=MSO_SHAPE.OVAL)
    tfb = b.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]; pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run(); rb.text = str(i + 1); rb.font.size = Pt(10.5); rb.font.bold = True
    rb.font.color.rgb = C['white']; rb.font.name = F_SANS
    _, t2 = tb(s, x + 0.64, yy + 0.16, wid - 0.86, 0.36)
    para(t2, t, size=11.5, color=C['ink'], bold=True, first=True, line_spacing=1.14)
    _, t3 = tb(s, x + 0.64, yy + 0.56, wid - 0.86, 0.62)
    parts = re.split(r'(`[^`]+`)', d)
    rich(t3, [((p[1:-1], col, False, False, F_MONO) if p.startswith('`') else (p, C['muted'], False))
              for p in parts if p], size=9.4, first=True, line_spacing=1.24)
notes(s, ["Read all six aloud, slowly. This is the last thing the room hears before lunch.",
          "Then ask which one surprised them most. In most rooms it is number five, and that is a good sign — it means the distinction landed.",
          "Point out that numbers three and four together are the reason the design looks odd at first: an append-only key table and a lazy rotation are exactly what you need when the artefacts you sign outlive your keys.",
          "Hand over to lunch with the discussion questions from the next slide on screen."],
      minutes="3 min")
footer(s)

# =================================================================== 24 NEXT
s, y = slide("What to do with this — lab, decisions, references", kicker="Close",
             sub="Three things worth trying hands-on, four decisions to start, and where to read further.")
card(s, ML, y, 3.90, 3.30, "Worth trying hands-on", [
 "Finding the `key_alias` and `key_store` rows behind an issued credential, and matching `cert_thumbprint` to the `kid` in the credential.",
 "Fetching `/.well-known/jwks.json` and `/.well-known/did.json` from a Certify instance to identify which key signed what.",
 "Calling `PUT /revokeKey` on a throwaway alias, then issuing again — a new key appears and **the old credential still verifies**.",
], accent=C['accent'], tint=C['accent_l'], size=9.8)
card(s, ML + 4.15, y, 3.90, 3.30, "Decisions to start now", [
 "HSM or software keystore for production — and who procures and operates it.",
 "Key validity and `pre_expire_days` per credential type, driven by how long credentials live.",
 "Self-signed ROOT or a chain to a recognised CA; which domain hosts the DID document.",
 "Who holds revocation authority, and through which interface.",
], accent=C['primary'], tint=C['primary_l'], size=9.8)
card(s, ML + 8.32, y, 3.91, 3.30, "The source, not the wiki", [
 "`mosip/keymanager` — the service impl, the DB helper and the private-key decryptor.",
 "Its `db_scripts` DDL — three tables, each column commented.",
 "`mosip/inji-certify` — the DID document util, the JWKS service, the status list service.",
 "docs.mosip.io — Key Manager module documentation.",
], accent=C['violet'], tint=C['violet_l'], size=9.6)
yy = y + 3.55
_, tf = tb(s, ML, yy, CW, 0.28)
para(tf, "PARKED QUESTIONS", size=9,
     color=C['accent'], bold=True, first=True)
qs = ["Rotation cadence per credential type", "HSM procurement and key ceremony",
      "CA chain and the recognised CA", "Incident drill before go-live"]
for i, q in enumerate(qs):
    x = ML + i * (CW / 4)
    rect(s, x, yy + 0.38, 0.16, 0.16, fill=None, line=C['accent'], lw=1.3)
    _, t2 = tb(s, x + 0.34, yy + 0.32, CW / 4 - 0.50, 0.4)
    para(t2, q, size=9.8, color=C['ink2'], first=True, line_spacing=1.2)
notes(s, ["Close by making the session actionable rather than interesting.",
          "The third lab item is the best one: revoke a key, issue again, and confirm the previously issued credential still verifies. Five minutes of hands-on makes the revokeKey point permanent in a way no slide can.",
          "The four decisions have different lead times. HSM procurement is the longest — start it this week even if the rest is undecided.",
          "Carry the parked questions forward to Day 3's security hardening block so the thread is not dropped. Assign a name to each before people leave for lunch.",
          "If there is time before lunch, take open questions. If not, note them and open Day 2's recap with them."],
      minutes="3 min")
footer(s)

# =================================================================== auto-fit
_fitted = fit_all()
