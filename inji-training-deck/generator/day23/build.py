import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *   # noqa
import core

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'assets')
prs = init(os.path.join(A, 'base.pptx'), os.path.join(A, 'bg.png'), os.path.join(A, 'logo.png'))
core.prs = prs
BASE_N = len(prs.slides._sldIdLst)

K_SD  = "Day 3 · Module 8 · Selective disclosure"
K_VP  = "Day 3 · Module 8 · OpenID4VP"
K_W   = "Day 2 · Module 7 · Wallet internals"

# ============================================================ 1  SD-JWT ANATOMY
s = new_slide(); y = head(s, "What the holder actually sends", K_SD)
segs = ["Issuer-signed\nJWT", "given_name", "family_name", "birthdate", "nationality", "portrait"]
bw, gap = 1.16, 0.115
def strip(yy, keep, kb=False):
    for i, t in enumerate(segs):
        x = ML + i * (bw + gap)
        on = (i in keep)
        col = C['orange'] if i == 0 else (C['violet'] if on else C['dim'])
        if on:
            sh = rect(s, x, yy, bw, 0.46, fill=C['white'], alpha=9.0, line=col, lw=1.0)
        else:
            sh = rect(s, x, yy, bw, 0.46, fill=None, line=col, lw=0.75)
            ln = sh.line._get_or_add_ln()
            ln.append(ln.makeelement(qn('a:prstDash'), {'val': 'sysDash'}))
        _, tf = tb(s, x + 0.05, yy, bw - 0.10, 0.46, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, t, size=7.4, color=C['white'] if on else C['dim'], bold=on,
             align=PP_ALIGN.CENTER, first=True, font=MONO, line_spacing=1.08)
        if i < len(segs) - 1:
            _, tf = tb(s, x + bw, yy, gap, 0.46, wrap=False, anchor=MSO_ANCHOR.MIDDLE)
            para(tf, "~", size=11, color=C['orange'], bold=True,
                 align=PP_ALIGN.CENTER, first=True, font=MONO)
    if kb:
        x = ML + len(segs) * (bw + gap)
        rect(s, x, yy, 1.06, 0.46, fill=C['orange'], alpha=22.0, line=C['orange'], lw=1.0)
        _, tf = tb(s, x + 0.04, yy, 0.98, 0.46, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, "KB-JWT", size=7.4, color=C['orange'], bold=True,
             align=PP_ALIGN.CENTER, first=True, font=MONO)

_, tf = tb(s, ML, y - 0.02, CW, 0.18)
para(tf, "AS ISSUED — every disclosure travels with the credential", size=7.8,
     color=C['dim'], bold=True, first=True)
strip(y + 0.16, keep=set(range(6)))
_, tf = tb(s, ML, y + 0.70, CW, 0.18)
para(tf, "AS PRESENTED — the wallet drops the disclosures the verifier did not ask for",
     size=7.8, color=C['dim'], bold=True, first=True)
strip(y + 0.88, keep={0, 3}, kb=True)

yy = y + 1.72
codebox(s, ML, yy, 4.52, 1.42, [
 '{                                     // issuer-signed JWT payload',
 '  "iss": "https://issuer.example",',
 '  "vct": "IdentityCredential",',
 '  "_sd_alg": "sha-256",',
 '  "_sd": [ "X9Hk2...", "pQ7mZ...", "Lr3Nv...",',
 '           "Ty8Wc...", "Bd4Qs..." ],   // one digest per claim',
 '  "cnf": { "kid": "did:jwk:eyJrdHki..." }',
 '}',
], label="THE ISSUER SIGNS THIS — and only this", size=7.0, hl=[4, 5, 6])
card(s, ML + 4.68, yy, 4.08, 1.42, "Three parts, three jobs", [
 "**Issuer-signed JWT** — carries `_sd` digests, never the values",
 "**Disclosure** — `[salt, name, value]`, base64url, one per digest",
 "**KB-JWT** — the holder's signature over this presentation",
], C['violet'], tsize=9.6, isize=8.0)

callout(s, ML, yy + 1.56, CW,
        "Withholding is **deletion, not redaction**. The wallet simply does not append that disclosure. Nothing is rewritten, nothing is re-signed, and the issuer's signature still verifies over exactly the bytes it signed.",
        C['orange'], size=8.8)
notes(s, [
 "This is the slide that makes selective disclosure click, so do not rush it. Walk the two strips top to bottom.",
 "Top strip: the credential as issued. The issuer-signed JWT, then one disclosure per selectively-disclosable claim, all joined by tilde characters. That whole string is what sits in the wallet.",
 "Bottom strip: the same credential as presented when the verifier only asked for date of birth. Four disclosures are simply absent. The wallet did not rewrite the credential, did not ask the issuer for a new one, and did not re-sign anything. It concatenated fewer segments.",
 "Then the code box. The issuer signs a payload that contains digests, not values. _sd is an array of hashes. _sd_alg names the hash. cnf names the holder key that will sign the KB-JWT later. There is no given_name field anywhere in the signed payload.",
 "The KB-JWT appended at the end of the bottom strip is the holder binding proof, and it is the subject of the binding slide later in this module.",
 "The point to land: selective disclosure costs the issuer nothing at presentation time. The issuer is offline. The holder does all the work, and the maths still holds. The next slide explains why.",
], minutes="6 min")

# ============================================================ 2  SD-JWT TRUST
s = new_slide(); y = head(s, "Why the verifier still trusts what is shown", K_SD)
steps(s, y, [
 ("01 / RECEIVE", "Split on ~", "JWT · disclosures · KB-JWT", C['orange']),
 ("02 / VERIFY", "Issuer signature", "Covers `_sd`", C['mag2']),
 ("03 / HASH", "Each disclosure", "Using `_sd_alg`", C['violet']),
 ("04 / MATCH", "Digest in `_sd`", "No match → reject", C['violet2']),
 ("05 / ACCEPT", "Claim is genuine", "Only what arrived", C['orange2']),
])

yy = y + 1.32
codebox(s, ML, yy, 4.52, 1.50, [
 'disclosure  = ["s4lT_x9", "birthdate", "1987-04-12"]',
 '',
 'base64url(disclosure)  ->  "WyJzNGxUX3g5Iiw..."',
 'sha-256( that string ) ->  "Ty8Wc..."',
 '',
 '"Ty8Wc..."  IS IN  _sd  ->  claim accepted',
 '"Zz0Qq..."  NOT IN _sd  ->  presentation rejected',
], label="THE CHECK, IN FULL", size=7.0, hl=[5, 6])

card(s, ML + 4.68, yy, 4.08, 1.50, "What an attacker cannot do", [
 "**Add a claim** — its digest is not in `_sd`, and `_sd` is inside the signature",
 "**Change a value** — the digest changes and stops matching",
 "**Forge the omission** — a missing digest is unrevealed, never absent",
], C['red'], tsize=9.6, isize=8.0)

callout(s, ML, yy + 1.62, CW,
        "`inji-openid4vp` does **not** trim disclosures for you. `SdJwtVPTokenBuilder` passes the credential string through verbatim, and `limit_disclosure` from the presentation definition is parsed but never applied. Selecting which disclosures to send is the wallet app's job.",
        C['orange'], size=8.6, title="INTEGRATION NOTE — VERIFIED IN THE RELEASED LIBRARY")
notes(s, [
 "The question this slide answers is the one every verifier team asks: if the holder can delete parts of the credential, how is that not tampering?",
 "Because the digests live inside the issuer's signature. The issuer signed an array of hashes. Removing a disclosure removes a preimage; it does not touch the array. The signature still verifies. Adding a claim means presenting a disclosure whose hash is not in the array, and the verifier rejects it.",
 "So the trust boundary is: the issuer vouches for the set of possible claims. The holder chooses a subset. The verifier can prove the subset is authentic but learns nothing about what was withheld beyond the count of unmatched digests.",
 "Say that last part plainly, because it is the honest limitation: the verifier does see how many claims exist, since _sd has a fixed length. It does not see what they are. If even the count is sensitive, decoy digests are the spec's answer.",
 "The integration note is the practically important one and it is verified in the released code. The Inji library builds the KB-JWT and assembles the final token, but it hands back whatever SD-JWT string you gave it. If the wallet passes the full credential, the holder discloses everything while believing selective disclosure happened. Whoever writes the wallet owns that filtering step.",
], minutes="6 min")

# ============================================================ 3  SAME vs CROSS
s = new_slide(); y = head(s, "Same-device and cross-device presentation", K_VP)
colw = (CW - 0.18) / 2
flows = [
 ("SAME-DEVICE", C['orange'], [
   ("01", "Browser hands off", "Verifier page opens `openid4vp://authorize?...`"),
   ("02", "OS routes the link", "Deep link / app link wakes the wallet"),
   ("03", "Wallet presents", "Consent, then POST to `response_uri`"),
   ("04", "Browser resumes", "Verifier polls or is pushed the result"),
 ]),
 ("CROSS-DEVICE", C['violet'], [
   ("01", "Verifier renders a QR", "Request by value, or a `request_uri`"),
   ("02", "Phone scans it", "Wallet parses and authenticates the verifier"),
   ("03", "Wallet presents", "Consent, then POST to `response_uri`"),
   ("04", "Screen updates", "Verifier correlates on `state`"),
 ]),
]
for ci, (nm, col, rows) in enumerate(flows):
    x = ML + ci * (colw + 0.18)
    panel(s, x, y, colw, 2.06, col, 5.0)
    chip(s, x + 0.12, y - 0.10, 1.16, 0.22, nm, col, size=7.4)
    cy = y + 0.22
    for num, t, sub in rows:
        _, tf = tb(s, x + 0.14, cy, 0.26, 0.22)
        para(tf, num, size=7.6, color=col, bold=True, first=True, font=MONO)
        _, tf = tb(s, x + 0.44, cy - 0.02, colw - 0.60, 0.22)
        para(tf, t, size=9.0, color=C['white'], bold=True, first=True)
        _, tf = tb(s, x + 0.44, cy + 0.19, colw - 0.60, 0.22)
        md(tf, sub, size=7.6, color=C['body'], first=True)
        cy += 0.46

yy = y + 2.22
rowtable(s, ML, yy, CW, ["", "SAME-DEVICE", "CROSS-DEVICE"], [
 ["What carries the request", "A URL the OS resolves to the wallet", "A QR code the camera resolves"],
 ["Why the response is separate", "The browser is not the wallet — it cannot receive `vp_token`", "The two devices share no session at all"],
 ["What ties it back together", "`state`, plus `nonce` inside the signed presentation", "Identical — the protocol does not change"],
], col_w=[2.05, 3.30, 3.41], fsize=8.0, accent=C['mag'])
notes(s, [
 "The mechanics people expect to differ mostly do not, and that is the headline. Say it first: same-device and cross-device differ only in how the authorization request reaches the wallet. Everything after that is the same protocol.",
 "Same-device: the verifier's web page invokes a custom scheme or an app link. The OS routes it to the wallet. Cross-device: the verifier paints a QR and the wallet's camera reads it. In both cases the wallet ends up holding an authorization request.",
 "Now the part that surprises people. In neither flow does the response go back the way the request came. It is POSTed to response_uri. Even same-device, where a redirect back to the browser looks natural, the vp_token does not travel through the browser. direct_post exists precisely so the presentation never touches the user agent.",
 "That is why state matters so much. The verifier's front end has no idea the presentation happened; it correlates through state and then polls or gets pushed the result.",
 "For Brazil-style deployments the practical question is which one to build first. Cross-device is usually the safer default: it works when the credential holder and the relying party are not on the same machine, which is most counter and kiosk scenarios. Same-device needs app-link registration and per-platform testing.",
], minutes="6 min")

# ============================================================ 4  PAYLOADS
s = new_slide(); y = head(s, "The request and the response, annotated", K_VP)
yy = y + 0.10
codebox(s, ML, yy, 4.30, 3.02, [
 'GET  /authorize?',
 '  client_id            = did:web:verifier.example',
 '  client_id_scheme     = did',
 '  response_type        = vp_token',
 '  response_mode        = direct_post',
 '  response_uri         = https://verifier.example/cb',
 '  nonce                = n-0S6_WzA2Mj',
 '  state                = af0ifjsldkj',
 '  presentation_definition = { ... }',
 '',
 '// presentation_definition, trimmed:',
 '{ "id": "pd-1", "input_descriptors": [{',
 '    "id": "dob-only",',
 '    "format": { "vc+sd-jwt": { ... } },',
 '    "constraints": { "fields": [',
 '      { "path": ["$.birthdate"] } ] } }] }',
], label="AUTHORIZATION REQUEST", size=6.8, hl=[2, 4, 6, 7])
codebox(s, ML + 4.46, yy, 4.30, 3.02, [
 'POST https://verifier.example/cb',
 'Content-Type: application/x-www-form-urlencoded',
 '',
 'vp_token = eyJhbGci...~WyJzNGxUX3g5...~eyJ0eXAi...',
 '           |__issuer JWT__|__disclosure__|__KB-JWT__|',
 '',
 'presentation_submission = {',
 '  "id": "ps-1",',
 '  "definition_id": "pd-1",',
 '  "descriptor_map": [{',
 '    "id": "dob-only",',
 '    "format": "vc+sd-jwt",',
 '    "path": "$" }] }',
 '',
 'state = af0ifjsldkj',
 '',
 '// no redirect carries the vp_token.',
 '// direct_post keeps the presentation',
 '// out of the browser entirely.',
], label="AUTHORIZATION RESPONSE", size=6.8, hl=[3, 4])

callout(s, ML, yy + 3.16, CW,
        "`nonce` goes into the **signed** presentation; `state` stays **outside** it. `state` correlates the browser session and is not security-critical on its own — `nonce` is what makes the presentation unreplayable.",
        C['violet'], size=8.8)
notes(s, [
 "Reference slide. Do not read it aloud. Put it up, give the room twenty seconds, then point at four things.",
 "One: client_id and client_id_scheme travel together. The scheme tells the wallet how to authenticate the verifier's identity — resolve a DID, match a redirect URI, or look it up in a pre-registered list. Inji's released library supports exactly those three.",
 "Two: response_mode is direct_post, so response_uri is where the answer goes. There is no redirect carrying the vp_token.",
 "Three: the presentation_definition asks for one field. Look at the response: the vp_token carries the issuer JWT, exactly one disclosure, and the KB-JWT. That is selective disclosure, visible on the wire.",
 "Four: presentation_submission is the map from the request's input_descriptor ids to where each credential landed in the vp_token. When there is one credential the path is just dollar-sign. With several it becomes an array index, and getting that wrong is the single most common integration bug in this protocol.",
 "Flag the draft difference: this is the Presentation Exchange shape that the released Inji libraries implement. OpenID4VP 1.0 replaces presentation_definition with dcql_query and drops descriptor_map. Same idea, different field names.",
], minutes="7 min")

# ============================================================ 5  BINDING AT VP
s = new_slide(); y = head(s, "Proving holder binding at presentation time", K_VP)
rowtable(s, ML, y, CW,
 ["", "WHAT THE WALLET SIGNS", "WHAT THE VERIFIER CHECKS AGAINST"], [
 ["`ldp_vc`",
  "A Data Integrity `Proof` — `challenge` = nonce, `domain` = client_id, `proofPurpose` = authentication",
  "The `verificationMethod` in the proof, resolved to the holder key"],
 ["`vc+sd-jwt`",
  "A KB-JWT — `typ` = `kb+jwt`, claims `aud`, `nonce`, `iat`, `sd_hash`",
  "The `cnf` claim inside the issuer-signed JWT"],
 ["`mso_mdoc`",
  "A DeviceSignature over the session transcript `[clientIdHash, responseUriHash, nonce]`",
  "`deviceKeyInfo` inside the issuer-signed MSO"],
], col_w=[1.24, 3.86, 3.66], fsize=7.9, accent=C['violet'])

yy = y + 2.06
steps(s, yy, [
 ("AT ISSUANCE", "Wallet proves key K", "Issuer binds the credential to K", C['orange']),
 ("IN THE CREDENTIAL", "K is named by the issuer", "`cnf` · `deviceKeyInfo` · subject id", C['mag2']),
 ("AT PRESENTATION", "Wallet signs with K again", "Over this verifier's nonce", C['violet']),
 ("NON-REPUDIATION", "Same key, both ends", "Presenter = the bound subject", C['orange2']),
])

callout(s, ML, yy + 1.12, CW,
        "In the released Kotlin library, `UnsignedSdJwtVPTokenBuilder` supports **only** `cnf` with a `kid` — a `cnf` carrying a raw `jwk` throws. Worth confirming against your issuer's output before interop testing.",
        C['red'], size=8.6)
notes(s, [
 "Module 6 showed binding at issuance. This is the other half, and without it the first half proves nothing.",
 "Work the table by column, not by row. The middle column is what the wallet produces. The right column is where the verifier finds the key to check it against — and in every format that key came from inside the issuer's signature. That is the whole trick. The issuer says 'this credential belongs to key K'. The holder proves control of K, right now, against this verifier's nonce.",
 "For ldp_vc the proof carries challenge and domain. Challenge is the nonce, domain is the client id. Inji's Proof class sets proofPurpose to authentication.",
 "For SD-JWT it is the KB-JWT, and note sd_hash: it is a hash over the exact presented credential string, so the binding covers which disclosures were sent. You cannot lift a KB-JWT onto a different subset.",
 "For mdoc the session transcript hashes the client id, the response uri and the nonce together, which binds the presentation to the channel as well as the moment.",
 "Then the four-box chain at the bottom. That is the non-repudiation argument in one line: same key at both ends, so the presenter is demonstrably the subject the issuer bound the credential to. Without presentation-time binding, a stolen credential file would be enough.",
 "Close on the red caveat. It is verified in the released library and it will bite during interop if the other side emits cnf with an embedded jwk.",
], minutes="7 min")

# ============================================================ 6  BACKUP
s = new_slide(); y = head(s, "Backup and restore", K_W)
steps(s, y, [
 ("01 / COLLECT", "Read local store", "Credentials + issuer cache", C['orange']),
 ("02 / STRIP", "Drop binding data", "Keys are removed here", C['red']),
 ("03 / ENCRYPT", "Passphrase key", "Derived, then zipped", C['mag2']),
 ("04 / UPLOAD", "Drive or iCloud", "User's own cloud account", C['violet']),
 ("05 / RESTORE", "Download + decrypt", "Credentials return unbound", C['violet2']),
])

yy = y + 1.14
card(s, ML, yy, 4.30, 1.38, "What the backup contains", [
 "The credential documents themselves",
 "`myVCs` metadata — the index of what is held",
 "Cached issuer `.well-known` configuration",
], C['violet'], tsize=9.6, isize=8.2)
card(s, ML + 4.46, yy, 4.30, 1.38, "What it deliberately does not", [
 "`privateKey` — set to null before export",
 "`publicKey` and `walletBindingResponse` — also nulled",
 "Anything held in the hardware keystore",
], C['red'], tsize=9.6, isize=8.2)

callout(s, ML, yy + 1.52, CW,
        "This is not an oversight. A hardware-backed key is **non-exportable by design** — if the backup could carry it, the keystore guarantee would be worthless. `removeWalletBindingDataBeforeBackup` makes that explicit. Restored credentials come back **unbound and must be re-bound on the new device before they can be presented.** Budget for that in your support model.",
        C['orange'], size=8.6)
notes(s, [
 "Backup is where the security architecture and the user experience collide, so present it as a trade-off rather than a feature.",
 "Walk the five steps. Step two is the one that matters: before anything is written out, the wallet nulls the private key, the public key and the wallet binding response on every credential. That is a named function in the codebase.",
 "Why? Because the binding key lives in the platform keystore and is non-exportable. That is the guarantee the secure-storage slide makes. A backup that could extract it would break exactly the property the whole design rests on.",
 "So state the consequence plainly, because users will meet it: restore gives you your credentials back, but they arrive unbound. They will display. They cannot be presented until the holder re-binds on the new device, which means going back to the issuer for a fresh binding.",
 "That has real programme consequences. If a citizen loses a phone, restore alone does not put them back in business. Whatever re-binding path exists has to be as available as issuance was, and it needs to be in the support script.",
 "Also note where the backup goes: the user's own Drive or iCloud account, not programme infrastructure. That is good for data minimisation and it means the programme cannot restore on a user's behalf.",
], minutes="6 min")

# ============================================================ 7  QR LOGIN
s = new_slide(); y = head(s, "QR-code login is a different protocol", K_W)
rowtable(s, ML, y, CW, ["", "WHAT THE WALLET DOES", "WHICH PROTOCOL"], [
 ["`OPENID4VP://connect`", "Opens a Bluetooth channel to a nearby verifier", "OpenID4VP over BLE — Tuvali"],
 ["`openid4vp://authorize`", "Presents a credential online to a remote verifier", "OpenID4VP — inji-openid4vp"],
 ["`inji://…?linkCode=…`", "Authenticates a web session on the user's behalf", "eSignet linked authorization"],
], col_w=[2.10, 3.40, 3.26], fsize=8.0, accent=C['orange'])

yy = y + 1.94
steps(s, yy, [
 ("01 / SCAN", "Website shows a QR", "Carries `linkCode` + expiry", C['orange']),
 ("02 / LINK", "`link-transaction`", "Code → linked transaction id", C['mag2']),
 ("03 / AUTHENTICATE", "`authenticate`", "Wallet asserts the user", C['violet']),
 ("04 / CONSENT", "`consent`", "Scopes and claims approved", C['violet2']),
 ("05 / LOGGED IN", "Browser advances", "Site receives its tokens", C['orange2']),
])

callout(s, ML, yy + 1.12, CW,
        "No credential is presented and no `vp_token` exists in this flow. The wallet is acting as an **authenticator for a web login**, not as a holder proving a claim. Different endpoints, different trust model — do not let it get filed under OpenID4VP.",
        C['violet'], size=8.8)
notes(s, [
 "This slide exists to prevent a specific confusion. Three different things arrive at the wallet as a QR code, and teams routinely assume they are one feature.",
 "Walk the table. The wallet literally branches on the prefix — there is a guard for each of these three in the scan state machine. OPENID4VP://connect means Bluetooth. openid4vp://authorize means online presentation. A URL carrying a linkCode parameter means QR login.",
 "The third is not OpenID4VP at all. It is eSignet's linked-authorization API: link-transaction, then authenticate, then consent. The wallet is standing in for a password. The website gets its tokens from eSignet in the normal OIDC way.",
 "Make the distinction concrete: in QR login the relying party learns who you are because an identity provider vouches for you. In OpenID4VP the relying party learns a claim because an issuer vouched for it and you proved you hold it. Different trust model, different failure modes, different governance.",
 "There is also a same-device variant of this flow via deep link, so the wallet has a separate guard for QR-login-via-deep-link. Same protocol, no camera.",
 "Practical note for the room: if your programme only needs web login, you do not need credentials at all. Ask the question early, because it changes the scope enormously.",
], minutes="5 min")

# ============================================================ 8  SVG RENDERING
s = new_slide(); y = head(s, "Dynamic credential rendering", K_W)
steps(s, y, [
 ("01 / READ", "`renderMethod`", "From the credential", C['orange']),
 ("02 / CHECK", "`renderSuite`", "Must be `svg-mustache`", C['mag2']),
 ("03 / FETCH", "The template", "HTTP GET the SVG", C['violet']),
 ("04 / VERIFY", "`digestMultibase`", "SHA-256 over the SVG", C['red']),
 ("05 / FILL", "JSON Pointers", "`{{/path/to/claim}}`", C['violet2']),
 ("06 / DRAW", "Rendered SVG", "Plus an embedded QR", C['orange2']),
], tsize=8.6)

yy = y + 1.30
codebox(s, ML, yy, 4.52, 1.50, [
 '"renderMethod": [{',
 '  "type": "TemplateRenderMethod",',
 '  "renderSuite": "svg-mustache",',
 '  "template": "https://issuer.example/tmpl.svg",',
 '  "digestMultibase": "uZGVmYXVsdC1oYXNo..."',
 '}]',
 '',
 '<text>{{/credentialSubject/fullName}}</text>',
], label="IN THE CREDENTIAL", size=7.0, hl=[4, 7])
card(s, ML + 4.68, yy, 4.08, 1.50, "Design consequences", [
 "The issuer controls the look **without a wallet release**",
 "`digestMultibase` must start with `u` — base64url, no padding",
 "`{{/qrCodeImage}}` is substituted with a generated QR, with a fallback image",
], C['violet'], tsize=9.6, isize=8.0)

callout(s, ML, yy + 1.64, CW,
        "The template is fetched over the network, so plan for **offline**: cache the SVG at issuance, not at display time. A credential that cannot render in a basement is a credential that does not work.",
        C['orange'], size=8.8)
notes(s, [
 "Rendering looks cosmetic and is not. It is the only part of the credential the citizen actually sees, and it is issuer-controlled.",
 "The credential carries a renderMethod block pointing at an SVG template on the issuer's server, plus a digest of that template. The wallet fetches the SVG, hashes it, compares against digestMultibase, and refuses to render on a mismatch. So the issuer can change the design without shipping a wallet update, but cannot have the template swapped underneath them.",
 "Placeholders are JSON Pointers, not arbitrary expressions. Double brace, slash-separated path into the credential JSON. There is one special placeholder for the QR image, which the renderer generates from the credential and substitutes as a base64 PNG data URI, with a fallback image if generation fails.",
 "Two things to raise with whoever owns the issuer side. First, the template URL has to stay up as long as credentials referencing it are in circulation, and it has to be reachable from consumer networks. Second, changing the template means changing the digest, which means credentials already issued will fail the check — so template versioning is an issuance-time decision, not a design-time one.",
 "The offline point in the callout is the one to insist on. Cache the rendered output or at least the template when the credential is issued. Testing on office wifi will not surface this.",
], minutes="5 min")

# ============================================================ 9  BLE
s = new_slide(); y = head(s, "Offline sharing over Bluetooth", K_W)
steps(s, y, [
 ("01 / ADVERTISE", "Verifier starts", "Publishes a connect URI", C['orange']),
 ("02 / EXCHANGE", "QR carries the URI", "`name` + verifier public `key`", C['mag2']),
 ("03 / CONNECT", "Wallet scans, joins", "Keys exchanged, channel secured", C['violet']),
 ("04 / TRANSFER", "Encrypt & chunk", "Compressed, 512-byte writes", C['violet2']),
 ("05 / REPAIR", "Transfer report", "Missing chunks re-sent", C['orange2']),
])

yy = y + 1.14
card(s, ML, yy, 4.30, 1.42, "How the channel is bootstrapped", [
 "`OPENID4VP://connect?name=<NAME>&key=<PUBKEY>`",
 "The QR is the **out-of-band channel** — it carries the verifier's public key",
 "No network, no server, no shared session",
], C['violet'], tsize=9.6, isize=8.0)
card(s, ML + 4.46, yy, 4.30, 1.42, "How it survives a bad link", [
 "A Chunker splits; an Assembler rebuilds",
 "The receiver reports missing sequence numbers",
 "The sender replays only those chunks",
], C['orange2'], tsize=9.6, isize=8.0)

callout(s, ML, yy + 1.56, CW,
        "Scope check before you design around it: Tuvali is **pre-1.0**, its API is explicitly expected to change, and the current version transfers a credential **one way only** — wallet to verifier. The full OpenID4VP-over-BLE request/response exchange is not implemented yet.",
        C['red'], size=8.6)
notes(s, [
 "Offline sharing is the feature that sells the wallet in low-connectivity contexts, so be precise about what actually works today.",
 "The bootstrap is the interesting part. Bluetooth Low Energy has no trust model of its own, so the QR code does that job. The verifier advertises and encodes its name and public key into a connect URI. The wallet scans, extracts the key, and establishes an encrypted channel. The QR is functioning as the out-of-band channel that makes the pairing trustworthy.",
 "Then the transport reality. A BLE characteristic write is capped around 512 bytes, so a credential has to be split. Tuvali encrypts and compresses first, tells the receiver the resulting size, then streams chunks. The receiver reports which sequence numbers are missing or corrupt and the sender replays just those. That repair loop is why this works at all across a crowded room.",
 "Now the honest scoping, and do not soften it. The library's own README says it is under active development with no major version released and non-backward-compatible changes expected. And the implementation notes state that although the specification covers both request and response, the current version only transfers a credential from central to peripheral.",
 "So if your use case is a verifier handing a request to a wallet offline and receiving a signed presentation back, that is not what ships today. Plan accordingly, and raise it upstream if it is on your critical path.",
], minutes="5 min")

# ============================================================ save
out = os.path.join(HERE, 'out.pptx')
prs.save(out)
print("built %d new slides -> %s" % (len(prs.slides._sldIdLst) - BASE_N, out))
bad = bounds_report()
print("overflow issues:", len(bad))
for b in bad[:20]:
    print("   ", b)
