// Footage map — clip-specific speaker geometry, in SOURCE pixels (1920×1080).
// Head samples come from scripts/measure-head.py (2 fps, skin-tone centroid) and
// were checked against an overlay contact sheet. Hand-edit freely: components
// only read this file, they never measure footage themselves.
window.MS_FOOTAGE = window.MS_FOOTAGE || {};
window.MS_FOOTAGE["home-buying"] = {
  source: { width: 1920, height: 1080, fps: 30, duration: 18.667 },
  head: {
    // [time s, face center x, face top y (forehead)]
    samples: [
      [0.0, 972, 174],
      [0.5, 960, 166],
      [1.0, 984, 166],
      [1.5, 1000, 154],
      [2.0, 960, 178],
      [2.5, 960, 166],
      [3.0, 904, 174],
      [3.5, 892, 174],
      [4.0, 900, 166],
      [4.5, 980, 158],
      [5.0, 1016, 166],
      [5.5, 996, 170],
      [6.0, 988, 178],
      [6.5, 1048, 182],
      [7.0, 1072, 178],
      [7.5, 1020, 162],
      [8.0, 956, 158],
      [8.5, 940, 198],
      [9.0, 956, 170],
      [9.5, 980, 182],
      [10.0, 984, 190],
      [10.5, 988, 190],
      [11.0, 984, 186],
      [11.5, 968, 170],
      [12.0, 968, 170],
      [12.5, 964, 158],
      [13.0, 956, 158],
      [13.5, 976, 170],
      [14.0, 988, 178],
      [14.5, 984, 186],
      [15.0, 1004, 202],
      [15.5, 952, 182],
      [16.0, 964, 226],
      [16.5, 976, 194],
      [17.0, 984, 178],
      [17.5, 992, 194],
      [18.0, 980, 186]
    ],
    width: 360,      // approx. head width incl. hair/ears
    hairAbove: 80,   // hair extends this far above the measured face top
    chinY: 600,      // chin line (constant for this locked-off shot)
  },
  // Hands entering from the bottom edge — graphics/captions keep out of these boxes.
  // From `measure-head.py --fps 4 --hands` (static set dressing filtered out).
  // Known miss: the right hand at 1.75–2.5 s overlaps the white pillow (x≈1700–1890)
  // and is filtered with it; captions are hidden during that beat anyway.
  gestures: [
    { start: 0, end: 0.25, rect: [348, 896, 628, 1080] },
    { start: 0, end: 0.75, rect: [1364, 888, 1624, 1080] },
    { start: 1.0, end: 1.5, rect: [704, 1032, 792, 1080] },
    { start: 1.0, end: 1.75, rect: [1384, 988, 1548, 1080] },
    { start: 1.5, end: 2.25, rect: [112, 880, 524, 1080] },
    { start: 2.5, end: 3.0, rect: [408, 980, 1040, 1080] },
    { start: 6.0, end: 7.0, rect: [996, 916, 1412, 1080] },
    { start: 7.5, end: 8.0, rect: [696, 1028, 776, 1080] },
    { start: 8.25, end: 8.75, rect: [376, 852, 720, 1080] },
    { start: 8.25, end: 9.0, rect: [1200, 796, 1552, 1080] },
    { start: 9.25, end: 11.25, rect: [232, 796, 800, 1080] },
    { start: 9.5, end: 11.0, rect: [1320, 832, 1652, 1080] },
    { start: 14.25, end: 14.75, rect: [800, 968, 956, 1080] },
    { start: 14.25, end: 14.75, rect: [1236, 952, 1356, 1080] },
    { start: 15.5, end: 16.25, rect: [368, 848, 840, 1080] },
    { start: 15.5, end: 17.0, rect: [876, 840, 1368, 1080] },
    { start: 17.0, end: 17.75, rect: [436, 920, 788, 1080] },
    { start: 17.0, end: 17.75, rect: [1100, 896, 1460, 1080] },
  ],
  // Areas where the accent blue would merge with the footage (blue hoodie).
  avoidAccent: [{ name: "wardrobe", rect: [460, 470, 1510, 1080] }],
  // Printed text in the footage — captions/labels must never sit on these.
  // Chest print "GALICI FINANCIAL", padded for body movement (hand-measured
  // from the frame review; not detected automatically).
  avoidText: [{ name: "chest-print", rect: [1000, 760, 1280, 920] }],
  // Side of the frame with clean, plain background (from the contrast notes).
  openSide: "left",
  notes: "Left third is clean mid-dark wall (#615850, warm white 6.2:1). Right third busy; lamp at x1740–1900 y180–450.",
};
