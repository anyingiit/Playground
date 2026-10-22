Fixes #24.

The smaller font for Unix time was keyed to the `.epoch` class, which the template builds from the clock's name. This changes the selector to `.clock[data-timezone="EPOCH"] .time`, so the font now follows the timezone that actually switches a clock to Unix time:

- A clock named "Unix" (or anything else) with `timezone: EPOCH` gets the smaller font, so the auto-resizer no longer shrinks every clock to fit a full-size 10-digit number.
- A clock named "EPOCH" with a real timezone keeps the normal size.

The default configuration looks the same as before, since its "EPOCH" clock also has `timezone: EPOCH`. The template still adds the name-based class to each clock; it just no longer affects the font size.

### Testing

- `npm test`, `npm run lint` and `npm run build` pass.
- I built the site, added a "Unix" clock with `data-timezone="EPOCH"` and an "EPOCH" clock with `data-timezone="UTC"` to the built page, and checked the computed `.time` font size in headless Chromium. Before the change, the "Unix" clock rendered at 64px and the "EPOCH"/UTC clock at 40px. After it, they render at 40px and 64px, and the default clocks are unchanged.

### Motivation and disclosure

This is a `good first issue` with clear acceptance criteria. I prepared it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the checks above.
