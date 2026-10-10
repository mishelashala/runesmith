# RuneSmith

RuneSmith Mono and a VS Code extension for modern English written phonemically with Anglo-Saxon runes. Version 0.1.0.

## Install

1. Install `RuneSmithMono-Regular.ttf` using your operating system's font installer.
2. In VS Code, run **Extensions: Install from VSIX** and select `runesmith-0.1.0.vsix`.
3. Add this to VS Code settings:

```json
{
  "editor.fontFamily": "'RuneSmith Mono', 'Menlo', 'Consolas', monospace",
  "editor.fontLigatures": false
}
```

The font covers runes, two custom characters, runic punctuation, and spaces. Latin text and other punctuation use your fallback font. Restart VS Code after installing the font if necessary.

## Use

- Hover over runic words for **all matching English words**, American pronunciations in IPA, and dictionary-style respelling. Hover also identifies the rune or sound sequence under the pointer.
- Unknown words receive an informational underline. Use **Quick Fix** for ranked suggestions or to add a spelling to your personal dictionary. No automatic replacement occurs.
- **RuneSmith: Insert English Word as Runes** looks up an English word and inserts a selected pronunciation as runes.
- **RuneSmith: Insert Custom Rune** inserts V or voiced TH without requiring a special keyboard.
- **RuneSmith: Open Font for Installation** opens the bundled font.

Everything runs offline. No requests, telemetry, API keys, or credentials are used.

## Mapping decisions

Modern English only; American pronunciation from CMUdict; rune.school-inspired mapping; monospaced; no bind runes or ligature substitutions. Traditional shapes have modern sound assignments, not claims of historical orthography.

| Custom sound | Character | Design |
|---|---|---|
| /v/ | U+E000 | Feoh with two opposite-side branches (tree shape) |
| /ð/ | U+E001 | Thorn with a crossbar |

These Private Use characters require RuneSmith to render. /f/ uses ᚠ and /θ/ uses ᚦ. A sequence such as ᛋᚳ remains **two characters and two cells**.

Canonical vowels: KIT ᛁ, DRESS ᛖ, TRAP ᚫ, PALM/LOT /ɑ/ ᚪ, THOUGHT /ɔ/ ᚩᚩ, FOOT ᚣ, STRUT ᚢ, schwa ᛟ, FLEECE ᛇ, GOOSE ᚣᚹ, FACE ᛖᛡ, GOAT ᚩᚹ, PRICE ᚫᛡ, MOUTH ᚫᚹ, CHOICE ᚩᛡ, NURSE ᚢᚱ, unstressed /ɚ/ ᛟᚱ. Stress affects schwa mapping but is not printed in runic text.

Accepted compatibility spellings: ᛁᛡ → ᛇ, ᚫᚫ → ᚪ, ᛄ → ᛇ, ᛥ → ᛋᛏ, ᛢ → ᛣᚹ. The old shared F/V and TH spellings are not automatically converted: RuneSmith preserves the chosen phonemic contrasts.

## Current limits

- CMUdict has pronunciations, not definitions; short definitions are not bundled yet.
- Respelling is inspired by familiar dictionary notation, **not official Merriam-Webster data**. Stress marks currently precede vowel phonemes rather than being fully syllabified.
- This is a dictionary-driven prototype, not a grammar checker. Names and new words may need personal dictionary entries. CMUdict includes multiple American variants rather than one rigid accent.
- Historical rune.school near/air shortcuts (ᛠᚱ, ᛁᛁᚱ, ᛖᛖᚱ) are not normalized yet. Standard phonemic forms generated from the dictionary work.
- Suggestions rank rune edit distance, then deterministically by spelling; no usage-frequency ranking yet.
- Font outlines are original geometric artwork. Small-size proofing has been performed, but the font is unhinted and should be reviewed on your actual display.
- Automated provider tests use a VS Code API harness; an interactive installed-extension smoke test remains necessary.

## Develop

Node 20+ and Python 3.12+. Runtime extension code has no third-party JavaScript dependencies.

```sh
npm test
pip install -r requirements.txt
npm run build:font
npm run build:dictionary
npm run package
```

`core.js` owns the mapping and dictionary index; `extension.js` integrates hover, diagnostics, Quick Fixes, and insertion commands. `build_font.py` builds reproducible TrueType outlines. `build_dictionary.py` bundles 125,938 CMUdict word entries and preserves its license.

Sources: https://rune.school/learn/ and https://github.com/cmusphinx/cmudict . CMUdict redistribution notice is included in `CMUDICT-LICENSE.txt`.

## License

RuneSmith code and original font outlines are licensed under the [MIT License](LICENSE). The bundled CMUdict data retains its separate redistribution terms in [CMUDICT-LICENSE.txt](CMUDICT-LICENSE.txt).

## Notebook spacing

The font uses tighter 500-unit monospace cells and stronger 60-unit strokes on an 800-unit em. Use a period (`.`) between words, as in handwritten notes; its dot is drawn near the baseline. Middle dot (`·`) and runic punctuation are also supported. Dots already split words for hover and spell checking. Ordinary spaces remain blank. The preview defaults to dot-separated samples.
