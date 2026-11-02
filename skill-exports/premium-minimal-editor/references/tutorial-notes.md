# Source notes — "Viral minimal talking-head edit using only Claude"

Source: 21-min YouTube tutorial by Joseph (Ultimate Editors), Studied via full Whisper transcript (5,076 words) + 251 frames sampled at 1 frame / 5s. The video itself is not stored in the repo.

Note: about 25% of the video is a sales pitch for a paid course ("Ultimate Editors 2.0", "AI Editing Fundamentals"). That part has no technique and was skipped. The tutorial's own skill files were not shared — everything here is reconstructed from what was shown and said.

## Structure of the tutorial

| Time | Section |
|---|---|
| 0:00–1:00 | Intro, what the style is ("premium educational", "$100 per short") |
| 1:00–5:50 | Chapter 1 — the 10 principles of the minimal style |
| 6:00–7:45 | Why you must understand the style yourself + course ad |
| 7:45–11:30 | Chapter 2 — how to train Claude on a style |
| 11:30–17:45 | Chapter 3 — creating the full edit (plan → build → revise → sound) |
| 17:45–19:00 | Final result |
| 19:00–21:00 | Cost/time breakdown + course ad |

## Key quotes

- "If you simply don't know how to create good videos, you're only gonna be using AI to create bad videos."
- "Lazy inputs with AI gets you lazy results."
- "If you let AI do the planning on its own, it's actually not creative enough to do a great job right off the bat."
- "Without a high-quality edit plan, the animations just won't come together into an amazing edit."
- "The first draft is going to be 60 to 70% of the way there."
- "The reference videos are how Claude learns the logic behind the animations, and the Figma board is how Claude learns the design."

## The training prompt used (paraphrased exactly as shown)

> I want to teach you a new editing style. Analyze this clean premium minimal editing style using the 20 reference videos. Start by creating a word-by-word transcript and a frame-by-frame breakdown of every single video to study three main things. First, where the animations are placed in correlation with the script. Second, how the design is composed and what elements make it up. And third, the animation logic — how long the animations are and what they feel like so you can recreate them. Then use the Figma board as a reference that breaks down the elements of the style and master the style using both so that I could prompt you to recreate it.

Output: a skill covering sizing, layout, textures, shapes, colors, plus 225 extracted animations, each in its own folder with reference design + keyframe sheet + notes.

## The edit prompt used

> I want you to use the [style] skill to edit this short-form clip in his premium clean style. Start by creating a word-by-word transcript at the millisecond level and cut out all silences leaving 30 milliseconds of padding. On top of that, hand me a document with the script of my raw video on the right side and text boxes on the left with recommended designs pulled from the [style] reference folder so that I can plan out and decide what needs to be built for each scene.

Then after planning: paste the plan → "Build all the animations and create the edit. If it needs any assets, use the Chrome browser or files, and prompt me if there's anything you can't find."

## Worked example — "Four career patterns" (57.4s, 15 beats)

| Beat | Line | Chosen design | Why |
|---|---|---|---|
| 1 | "There's four career patterns, psychologically." | A-roll + captions (hero: **four**, ***psychologically***) | meet the face first |
| 2 | "There's linears who just go up and up and up…" | Graph: line climbs one step per "up" | first visual = hook |
| 3 | "There are transitories who skip around all over the place." | A-roll + captions | new type announced → face |
| 4 | "I'm gonna be a barista… girl in San Diego." | Two paintings (Chardin "Lady Taking Tea", Hayez "The Kiss") + text | describing → show it |
| 5 | "There are what's called expert… slow and steady." | A-roll first half → graph: long flat line | new type, then show |
| 6 | "My dad had the same job for 42 years." | Character callout (blue side illustration + "same job") | a person described |
| 7 | "…because it was secure, low stress" | Center illustration (blue figure, "secure", "low") | |
| 8 | "A lot of people… are spirals, every 7 to 12 years" | Center illustration: blue spiral, "for every 7 to 12" | |
| 9 | "Take their career down to the studs and start again." | B-roll + text | easy to feel |
| 10 | "First turn is hardest… French horn → scientist, brutal." | Object callout with real photos of him | personal story |
| 11 | "Going back and getting a PhD… really hard" | B-roll + text | |
| 12 | "Maybe in 10 years I'll be a circus clown or firefighter" | Center illustration of him, circle cycling through options | list of options |
| 13 | "…pursuing your calling… agility and courage" | Line + text, line runs through **calling / agility / courage** | big thesis |
| 14–15 | "…in the business of life." | Text-centric, quotation marks, blue bg, ***life*** | ending |

Pattern: **announce = face, describe = visual.**

Revisions given on draft 1: (1) first scene's text weak — put "psychologically" on screen; (2) rough cut between graph and next shot — hold graph text to 0:06; (3) paint texture too heavy and static — half strength, move with camera; (4) bad cut at 0:24; (5) spiral held longer through "for every 7 to 12 years"; (6) add quotation marks on the final text scene.

Sound pass: cinematic music track, clicks for text, highlighters for graphs, whooshes for transitions — 74 SFX placed, matched against the references.

Time: cuts + plan doc 15 min · human planning 15 min · build 60 min · revisions 10 min · sound 15 min ≈ 2 h.

## Building it

The tutorial built in Remotion through Claude. Any editor works: see `animation-library.md` for tool-agnostic build notes.
