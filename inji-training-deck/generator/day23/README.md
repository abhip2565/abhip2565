# Day 2 / Day 3 deck — added slides

Nine slides appended to the existing Day 2 / Day 3 Inji training deck and then
reordered into place, matched to that deck's design system (10 × 5.625 in,
Montserrat, translucent panels over the Inji background).

## What was added

| Position | Slide | Module |
|---|---|---|
| 16 | Dynamic credential rendering | Day 2 · Module 7 |
| 17 | Offline sharing over Bluetooth | Day 2 · Module 7 |
| 18 | QR-code login is a different protocol | Day 2 · Module 7 |
| 19 | Backup and restore | Day 2 · Module 7 |
| 26 | Same-device and cross-device presentation | Day 3 · Module 8 |
| 27 | The request and the response, annotated | Day 3 · Module 8 |
| 29 | What the holder actually sends | Day 3 · Selective disclosure |
| 30 | Why the verifier still trusts what is shown | Day 3 · Selective disclosure |
| 32 | Proving holder binding at presentation time | Day 3 · Module 8 |

Every slide carries speaker notes with a suggested duration.

## Building

`assets/base.pptx` is the source deck and is not committed — drop the current
version in before building.

```
cd generator/day23
python3 build.py        # appends the 9 slides -> out.pptx
python3 reorder.py      # moves them into position -> Inji-Day2-Day3-Training-EXTENDED.pptx
```

`core.py` holds the design system extracted from the source deck: geometry,
the Montserrat scale, the colour set, translucent panel fills (python-pptx has
no alpha API, so `_solid_alpha` writes the XML directly), and the composite
blocks — `steps`, `card`, `codebox`, `callout`, `rowtable`.

`bounds_report()` checks every shape against the slide edges and a 5.30 in
bottom limit; the build prints it. Pre-existing slides report decorative
bleeds, which is expected — only the new slides need to come back clean.

## Sources

Content was verified against the repositories rather than written from memory:

- `inji-openid4vp` — `ClientIdScheme`, `ResponseMode`, `UnsignedSdJwtVPTokenBuilder`
  (KB-JWT construction, the `cnf`/`kid`-only limitation), `SdJwtVPTokenBuilder`
  (no disclosure trimming), `Proof`, `DeviceAuthentication`, `UnsignedMdocVPTokenBuilder`
  (session transcript)
- `inji-wallet` — `shared/backupUtils/backupData.ts` (`removeWalletBindingDataBeforeBackup`),
  `machines/bleShare/scan/scanGuards.ts` (the three QR types), `shared/api.ts`
  (eSignet linked-authorization endpoints)
- `inji-vc-renderer` — `InjiVcRenderer`, `TemplateHelper` (`digestMultibase`
  validation), `JsonPointerResolver`, `Constants`
- `tuvali` — `README.md` and `docs/tuvali-implementation.md`
