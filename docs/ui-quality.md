# UI quality rules

This product has a command-line interface and no screen today (the optional static HTML view is out of the current batch, decision D6). The rules are binding for every user-facing string, for command output and for any HTML, CSS or interface a later ticket adds. The owner set rules 1 and 2; rules 3 to 10 were approved on 2026-11-22 and have the same standing. They keep the interface from showing the usual marks of generated UI.

1. No thick accent border on one side of a card, callout, alert, list item or quote (for example `border-left: 4px solid <accent>`). Use spacing, type weight, an icon or a full hairline border instead.
2. No soft tinted background with a thin border of the same hue as the default way to mark a status, tag, callout or card. One neutral surface and one clear signal (text, icon or a solid chip) is enough.
3. No gradient text and no purple-to-blue gradient as a default accent.
4. No blur or glass panels, and no drop shadow plus large radius on every card.
5. No emoji used as icons or bullets, and no sparkle marks.
6. No pill or badge on things that are not states. No all-caps, letter-spaced micro labels as section decoration.
7. No centred hero with a slogan in an application screen. Screens open on the user's task.
8. One accent colour, used for the primary action and the current selection. Status colours only for status.
9. Dense, aligned layouts on a consistent spacing scale. No card grid where a table or a list is the right form (the trial report is a table).
10. User-facing copy is plain and specific: no filler, no exclamation marks, and the same word for the same thing everywhere.

## How the rules are applied

- A ticket that adds a screen or a page starts with the `ui-ux-pro-max` skill (design-system search for the product type) and ends with a check of every changed screen against this file. Tickets that only change command output or documentation check rules 5 and 10 and the table form of rule 9.
- Command output states unknown or missing values in words, not by colour or symbol alone, and stays readable as plain text in a log.
- User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- Code Reviewer names this file in its checklist. Enforcement is by the review gate, not by a script. Rule 1 can be linted; rule 2 cannot be detected reliably from CSS.
