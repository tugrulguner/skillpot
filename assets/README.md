# SkillPot artwork

SkillPot uses the ModePot family's flask, dark lockup, divider, lowercase wordmark,
two-line subtitle, and accent rule. Its accent is coral (`#FF9A76`). Stacked playbook
cards and a check mark distinguish the interior glyph without changing the family flask.

## Assets

| Source | Rendering | Purpose |
| --- | --- | --- |
| [skillpot-lockup.svg](skillpot-lockup.svg) | [skillpot-lockup.png](skillpot-lockup.png) | 1200 × 900 hero, displayed at 600 px in the README |
| [skillpot-mark.svg](skillpot-mark.svg) | [skillpot-mark.png](skillpot-mark.png) | Transparent 512 × 512 standalone mark |
| [skillpot-workflow.svg](skillpot-workflow.svg) | [skillpot-workflow.png](skillpot-workflow.png) | 1600 × 760 planned-workflow overview, displayed at 960 px |

## Family reference

The initial lockup follows the current editable Dexpot, Intpot, and Summonpot family
sources: 1200 × 900 canvas; `#090C11` background; divider at x=456 from y=220 to 680;
flask group `translate(98 270) scale(2.75)`; resource heading at (520,286); wordmark
baseline y=444; subtitles at (520,526) and (520,572); accent rule from (520,626) to
(1090,626). The canonical flask outline is retained unchanged. Text sizing adapts to
the project name; the layout and family geometry do not.

References:
- [Dexpot source](https://github.com/tugrulguner/dexpot/blob/main/assets/dexpot-lockup.svg)
- [Intpot source](https://github.com/tugrulguner/intpot/blob/main/assets/intpot-lockup.svg)
- [Summonpot source](https://github.com/tugrulguner/summonpot/blob/main/assets/summonpot-lockup.svg)

## Editing and rendering

Edit the SVG source and regenerate the matching PNG at its declared native dimensions.
The initial PNGs were rendered in Chromium at device scale factor 1 after fonts loaded.
Use Arial/Helvetica-compatible fonts and inspect the pixels after rendering; a successful
conversion alone does not establish correct text layout or color.

Keep a transparent background for the standalone mark. Preserve the planned-status label
inside the workflow overview until its procedure actually ships. Do not add a website,
compatibility badge, performance result, or maturity claim to detached artwork unless
it is true independently of the README.

Check source/rendering dimensions, text overflow, small-size glyph clarity, the shared
flask geometry, and the README's 600 px hero width. Both SVG sources and PNGs are tracked
under the repository's [MIT License](../LICENSE).
