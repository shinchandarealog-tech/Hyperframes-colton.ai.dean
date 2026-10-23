// Beat script — the ONLY content file for this clip. Components are generic;
// everything topic-specific (words, timings, which component) lives here.
// Times are seconds in the delivered footage, anchored to transcript words.
// Per-aspect overrides go under `landscape: {}` / `portrait: {}`.
window.MS_CLIPS = window.MS_CLIPS || {};
window.MS_CLIPS["home-buying"] = {
  // Portrait layout over time. SPLIT (native-res speaker + graphic stage) is the
  // default; FULL (1.78× upscaled face crop) is used once, for a direct-address beat.
  layout: {
    portrait: [
      { at: 0, mode: "split" },
      { at: 9.82, mode: "full" },  // "Let's break it down step by step…"
      { at: 12.66, mode: "split" },
    ],
  },

  beats: [
    {
      id: "b1-hook", // "Are you thinking about buying a new home in the next 10 years?"
      component: "headline",
      start: 0.06,
      end: 2.72,
      suppressCaptions: true, // the headline carries these words
      lines: [
        { text: "Thinking about", at: 0.28 },  // "thinking"
        { text: "buying a home", at: 0.9 },    // "buying"
        { text: "in the next", at: 1.68, tone: "dim" },
        { text: "{{10 years?|mono}}", at: 2.13, tone: "dim" }, // "10"
      ],
    },
    {
      id: "b2-audience", // "If you're in your late 20s right now,"
      component: "anchoredLabel",
      start: 2.95,
      end: 4.55,
      title: { text: "Late 20s", at: 3.62 }, // "20s"
      note: { text: "Right now", at: 4.11 }, // "now"
    },
    // B3 promise / B4 roadmap / B5 context: captions only in this phase
    // (timeline diagram, section marker and pull quote come next — DESIGN.md §5).
    {
      id: "b6-tension", // "…it's gotten pretty pricey."
      component: "headline",
      start: 17.06,
      end: 18.67,
      exit: false, // clip ends on this line
      suppressCaptions: true,
      lines: [
        { text: "It's gotten", at: 17.06 },
        { text: "pretty {{pricey.|warn@18.03}}", at: 17.67 },
      ],
    },
  ],
};
