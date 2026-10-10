# RuneSmith

A runic editor font and VS Code writing assistant for Futhark and Anglo-Saxon Futhorc.

**Status:** Planning. Created October 10, 2026.

## Motivation

The current appearance of Unicode runes in my editor is unsatisfactory. RuneSmith aims to make runic text comfortable to read, write, and check.

## 1. Editor font

Create attractive, legible Futhark glyphs mapped to existing Unicode runic characters.

- Consistent stroke weight, spacing, angles, and proportions.
- Distinct rune shapes at normal editor sizes.
- Editor-friendly metrics, ideally monospaced.
- Reliable alignment and line height without clipping.
- Preserve Unicode text so documents remain portable.

Choose the initial Futhark variant and include the Anglo-Saxon Futhorc characters needed by the extension.

## 2. VS Code rune assistant

Provide spell checking for English written with Anglo-Saxon runes.

- Recognize runic words.
- Flag likely spelling or rune-selection mistakes.
- Offer “Did you mean…?” correction suggestions.
- Hover over a word to see its English spelling and pronunciation using Merriam-Webster-style notation.

Example: hover over the runic equivalent of **show** to see **show** and its dictionary pronunciation.

## Open decisions

- Modern English written in Futhorc, historical Old English, or separate modes? Modern English is the initial working assumption.
- Which spelling or sound-to-rune conventions should be accepted?
- How should ambiguous sequences and multiple candidate words appear?
- Which dictionary and pronunciation source can be used, under what terms?
- Is monospacing required, or should there also be a proportional version?

## Font quality checks

Verify Unicode coverage, font-table validity, glyph metrics, spacing, clipping, and rendering at several sizes. Inspect real words and paragraphs for optical consistency and distinguishability. Review the final appearance in the actual editor.

## Initial checklist

- [ ] Choose the rune inventory and writing convention.
- [ ] Collect examples of current rendering problems.
- [ ] Design a contrasting set of glyphs and test real text.
- [ ] Build and validate an installable font.
- [ ] Prototype runic-word recognition and English-word hover.
- [ ] Add correction suggestions after the mapping works reliably.
