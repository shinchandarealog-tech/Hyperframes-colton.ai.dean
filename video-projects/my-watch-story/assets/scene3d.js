/* My Watch Story — real-3D layer (three.js r147, deterministic).
 * Everything is a pure function of composition time `t`: render(t) poses every
 * object, then draws once. Driven by the HyperFrames three adapter (hf-seek)
 * and by the root GSAP timeline's onUpdate. Assets load through
 * THREE.DefaultLoadingManager so the renderer waits for them.
 *
 * Coordinates: the canvas covers the 16:9 shot (canvas y 656–1264). px(cx, cy)
 * maps a 1080x1920 canvas pixel to world space so 1 world unit = 1 px at z = 0.
 */
(function () {
  const W = 1080, H = 608, TOP = 656;
  const canvas = document.getElementById("gl");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.setClearColor(0x000000, 0);
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;

  const scene = new THREE.Scene();
  const FOV = 30;
  const DIST = (H / 2) / Math.tan((FOV / 2) * Math.PI / 180);
  const camera = new THREE.PerspectiveCamera(FOV, W / H, 10, 5000);
  camera.position.set(0, 0, DIST);

  const key = new THREE.DirectionalLight(0xffffff, 1.1);
  key.position.set(-300, 500, 900);
  scene.add(key);
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));

  const px = (cx, cy, z = 0) => new THREE.Vector3(cx - W / 2, (TOP + H / 2) - cy, z);

  /* ---------- easing + timing ---------- */
  const cl = (x) => Math.min(1, Math.max(0, x));
  const P = (t, a, d) => cl((t - a) / d);
  const E = {
    out3: (p) => 1 - Math.pow(1 - p, 3),
    out2: (p) => 1 - (1 - p) * (1 - p),
    in2: (p) => p * p,
    expo: (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p)),
    sine: (p) => -(Math.cos(Math.PI * p) - 1) / 2,
    back: (p, s = 2.2) => 1 + (s + 1) * Math.pow(p - 1, 3) + s * Math.pow(p - 1, 2),
  };
  const lerp = (a, b, p) => a + (b - a) * p;
  // keyframes: [[time, value, ease?], ...] — ease applies to the segment ending at that key
  function kf(t, keys) {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [t1, v1, ez] = keys[i];
      const [t0, v0] = keys[i - 1];
      if (t <= t1) return lerp(v0, v1, (ez || E.out3)((t - t0) / (t1 - t0)));
    }
    return keys[keys.length - 1][1];
  }
  const F = (n) => n / 60;

  /* ---------- materials ---------- */
  const M = {
    rose: new THREE.MeshStandardMaterial({ color: 0xd8957a, metalness: 1, roughness: 0.26, envMapIntensity: 0.75 }),
    roseGlow: new THREE.MeshStandardMaterial({ color: 0xd8957a, metalness: 0.9, roughness: 0.3, emissive: 0x6a3a2c, envMapIntensity: 0.7, transparent: true }),
    steel: new THREE.MeshStandardMaterial({ color: 0xdfe3e8, metalness: 1, roughness: 0.16 }),
    brushed: new THREE.MeshStandardMaterial({ color: 0xcfd3d8, metalness: 1, roughness: 0.38 }),
    dialCream: new THREE.MeshStandardMaterial({ color: 0xefe7d6, metalness: 0, roughness: 0.6 }),
    dialSilver: new THREE.MeshStandardMaterial({ color: 0xc9cdd3, metalness: 0.55, roughness: 0.32 }),
    dialBlack: new THREE.MeshStandardMaterial({ color: 0x2a2725, metalness: 0.2, roughness: 0.45 }),
    hand: new THREE.MeshStandardMaterial({ color: 0x1b1b1d, metalness: 0.4, roughness: 0.4 }),
    handLight: new THREE.MeshStandardMaterial({ color: 0xf2f2f2, metalness: 0.6, roughness: 0.25 }),
    white: new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0, roughness: 0.32, emissive: 0x6a6a6a }),
    planeWhite: new THREE.MeshStandardMaterial({ color: 0xf6f6f6, metalness: 0.15, roughness: 0.22, emissive: 0x2a2a2a }),
    tagFace: new THREE.MeshStandardMaterial({ color: 0x0e0c0e, metalness: 0, roughness: 0.7, envMapIntensity: 0.25 }),
    shadow: new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.4, depthWrite: false }),
    leather: new THREE.MeshStandardMaterial({ color: 0x8a5a3c, metalness: 0, roughness: 0.75 }),
  };

  /* ---------- loaders (tracked by DefaultLoadingManager) ---------- */
  const pmrem = new THREE.PMREMGenerator(renderer);
  new THREE.RGBELoader().load("assets/3d/studio_small_09_1k.hdr", (tex) => {
    scene.environment = pmrem.fromEquirectangular(tex).texture;
    tex.dispose();
    redraw();
  });
  const tl = new THREE.TextureLoader();
  tl.load("assets/3d/leather_Diffuse.jpg", (t) => { t.encoding = THREE.sRGBEncoding; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(0.6, 1.4); M.leather.map = t; M.leather.color.set(0xb98a6a); M.leather.needsUpdate = true; redraw(); });
  tl.load("assets/3d/leather_nor_gl.jpg", (t) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(0.6, 1.4); M.leather.normalMap = t; M.leather.needsUpdate = true; redraw(); });

  /* ---------- builders ---------- */
  function box(w, h, d, mat) { return new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); }
  function cylZ(r, h, mat, seg = 64) { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat); m.rotation.x = Math.PI / 2; return m; }

  // A wristwatch facing +z. kind: "timex" | "rolex" | "mini"
  function makeWatch(kind, opts = {}) {
    const g = new THREE.Group();
    const r = kind === "mini" ? 13 : kind === "rolex" ? 25 : 24;
    const caseMat = opts.caseMat || (kind === "timex" ? M.brushed : M.steel);
    const dialMat = opts.dialMat || (kind === "timex" ? M.dialCream : kind === "rolex" ? M.dialSilver : M.dialSilver);
    const handMat = opts.handMat || (dialMat === M.dialBlack ? M.handLight : M.hand);
    const c = cylZ(r, kind === "mini" ? 5 : 8, caseMat); g.add(c);
    if (kind === "rolex") {
      // fluted bezel: ring of facets
      const base = new THREE.Mesh(new THREE.TorusGeometry(r - 1.6, 2.4, 12, 72), M.steel); base.position.z = 4.2; g.add(base);
      for (let i = 0; i < 48; i++) {
        const a = (i / 48) * Math.PI * 2;
        const f = box(1.5, 3.8, 2.2, M.steel);
        f.position.set(Math.cos(a) * (r - 1.6), Math.sin(a) * (r - 1.6), 5.4);
        f.rotation.z = a; f.rotation.y = 0.35; g.add(f);
      }
    } else {
      const bez = new THREE.Mesh(new THREE.TorusGeometry(r - 1.2, kind === "mini" ? 1.4 : 2, 12, 64), caseMat);
      bez.position.z = kind === "mini" ? 2.6 : 4.1; g.add(bez);
    }
    const dial = new THREE.Mesh(new THREE.CircleGeometry(r - 3, 64), dialMat);
    dial.position.z = kind === "mini" ? 2.6 : 4.15; g.add(dial);
    const zTop = dial.position.z + 0.3;
    if (kind !== "mini") {
      for (let i = 0; i < 12; i++) {
        const a = (i / 12) * Math.PI * 2;
        const long = i % 3 === 0;
        const m = box(long ? 2.2 : 1.4, long ? 6 : 3.6, 0.8, kind === "rolex" ? M.steel : M.hand);
        const rr = r - (long ? 7.5 : 6.5);
        m.position.set(Math.sin(a) * rr, Math.cos(a) * rr, zTop);
        m.rotation.z = -a; g.add(m);
      }
      const crown = cylZ(2.6, 4, caseMat, 20); crown.rotation.set(0, 0, Math.PI / 2); crown.position.set(r + 2, 0, 0); g.add(crown);
      for (const sx of [-1, 1]) for (const sy of [-1, 1]) { const lug = box(5, 8, 5, caseMat); lug.position.set(sx * 9.5, sy * (r + 2), -0.5); g.add(lug); }
    }
    // hands at 10:10
    const hh = box(kind === "mini" ? 1.6 : 2.4, kind === "mini" ? 6 : 11, 0.7, handMat);
    hh.geometry.translate(0, (kind === "mini" ? 6 : 11) / 2, 0); hh.rotation.z = 2.1; hh.position.z = zTop + 0.6; g.add(hh);
    const mh = box(kind === "mini" ? 1.2 : 1.6, kind === "mini" ? 9 : 17, 0.7, handMat);
    mh.geometry.translate(0, (kind === "mini" ? 9 : 17) / 2, 0); mh.rotation.z = -1.0; mh.position.z = zTop + 1.2; g.add(mh);
    const pin = cylZ(kind === "mini" ? 1.2 : 1.8, 2, M.rose, 16); pin.position.z = zTop + 1.4; g.add(pin);
    if (kind === "timex") {
      for (const s of [-1, 1]) {
        const strap = new THREE.Mesh(new THREE.RoundedBoxGeometry(17, 34, 3.2, 3, 1.2), M.leather);
        strap.position.set(0, s * (r + 19), -1); g.add(strap);
      }
    } else if (kind === "rolex") {
      for (const s of [-1, 1]) for (let k = 0; k < 4; k++) {
        const y = s * (r + 6 + k * 8.2);
        const mid = box(6.2, 7, 3, M.steel); mid.position.set(0, y, -1); g.add(mid);
        for (const sx of [-1, 1]) { const o = box(4.6, 7.4, 2.6, M.brushed); o.position.set(sx * 5.8, y, -1.2); g.add(o); }
      }
    }
    return g;
  }

  // Tube that "draws" via drawRange
  function drawTube(curve, radius, mat, segs = 220) {
    const geo = new THREE.TubeGeometry(curve, segs, radius, 10, false);
    const m = new THREE.Mesh(geo, mat);
    m.userData.full = geo.index.count;
    m.userData.setP = (p) => geo.setDrawRange(0, Math.floor(m.userData.full * cl(p) / 6) * 6);
    m.userData.setP(0);
    return m;
  }
  const circleCurve = (rx, ry) => new THREE.EllipseCurve(0, 0, rx, ry, -Math.PI / 2, Math.PI * 1.5, false, 0);
  function curve3(c2) { const pts = c2.getPoints(200).map((p) => new THREE.Vector3(p.x, p.y, 0)); return new THREE.CatmullRomCurve3(pts, false); }

  /* ---------- scene objects ---------- */
  const O = {};

  // B03 Timex — sits in the Timex card's watch slot
  O.timex = makeWatch("timex"); O.timex.scale.setScalar(0.8); O.timex.position.copy(px(94.5, 769.5, 20)); scene.add(O.timex);
  // B06 Rolex — Rolex card slot
  O.rolex = makeWatch("rolex"); O.rolex.scale.setScalar(0.78); O.rolex.position.copy(px(672.5, 769.5, 20)); scene.add(O.rolex);

  // B07 ten mini watches under the counter
  O.minis = [];
  const miniLooks = [
    { caseMat: M.steel, dialMat: M.dialSilver }, { caseMat: M.rose, dialMat: M.dialBlack },
    { caseMat: M.brushed, dialMat: M.dialCream }, { caseMat: M.steel, dialMat: M.dialBlack },
    { caseMat: M.rose, dialMat: M.dialCream },
  ];
  for (let i = 0; i < 10; i++) {
    const w = makeWatch("mini", miniLooks[(i * 3) % 5]);
    w.position.copy(px(62 + (i % 5) * 46, 880 + Math.floor(i / 5) * 46, 10));
    scene.add(w); O.minis.push(w);
  }

  // B02 plane + dotted trail on a 3D curve
  O.flyCurve = new THREE.QuadraticBezierCurve3(px(52, 1010, -140), px(150, 690, 40), px(418, 752, 70));
  O.trail = [];
  for (let i = 0; i <= 44; i++) {
    const d = new THREE.Mesh(new THREE.SphereGeometry(2.3, 10, 8), M.roseGlow);
    d.position.copy(O.flyCurve.getPoint(i / 44)); d.userData.u = i / 44; scene.add(d); O.trail.push(d);
  }
  O.plane = new THREE.Group();
  {
    const body = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 3, 38, 20), M.planeWhite); body.rotation.z = -Math.PI / 2; O.plane.add(body);
    const nose = new THREE.Mesh(new THREE.SphereGeometry(4.2, 20, 14), M.planeWhite); nose.position.x = 19; nose.scale.set(1.6, 1, 1); O.plane.add(nose);
    const wing = new THREE.Mesh(new THREE.BoxGeometry(11, 50, 1.6), M.planeWhite); wing.position.x = 3; wing.geometry.translate(0, 0, 0); O.plane.add(wing);
    const tail = new THREE.Mesh(new THREE.BoxGeometry(6, 19, 1.4), M.planeWhite); tail.position.x = -16; O.plane.add(tail);
    const fin = new THREE.Mesh(new THREE.BoxGeometry(7, 1.4, 10), M.planeWhite); fin.position.set(-16, 0, 5); O.plane.add(fin);
    for (const s of [-1, 1]) { const eng = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.2, 7, 14), M.rose); eng.rotation.z = -Math.PI / 2; eng.position.set(5, s * 12, -2.5); O.plane.add(eng); }
  }
  scene.add(O.plane);

  // B02 3D ring round the watch roll
  O.rollRing = drawTube(curve3(circleCurve(110, 110)), 3.2, M.rose);
  O.rollRingG = new THREE.Group(); O.rollRingG.add(O.rollRing);
  O.rollRingG.position.copy(px(368, 1158, 0)); O.rollRingG.rotation.set(0.97, 0, -0.14); scene.add(O.rollRingG);

  // B08 ring round the lifted 5711R
  O.pkRing = drawTube(curve3(circleCurve(74, 74)), 3, M.roseGlow);
  O.pkRingG = new THREE.Group(); O.pkRingG.add(O.pkRing); scene.add(O.pkRingG);

  // B04 price tag hanging from a pin
  O.tag = new THREE.Group(); O.tag.position.copy(px(850, 686, 10)); scene.add(O.tag);
  O.tagSwing = new THREE.Group(); O.tag.add(O.tagSwing);
  {
    const nail = new THREE.Mesh(new THREE.SphereGeometry(5, 18, 12), M.rose); O.tag.add(nail);
    const str = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 44, 8), M.rose); str.position.y = -22; O.tagSwing.add(str);
    const s = new THREE.Shape();
    s.moveTo(0, -40); s.lineTo(52, -66); s.lineTo(52, -160); s.quadraticCurveTo(52, -168, 44, -168);
    s.lineTo(-44, -168); s.quadraticCurveTo(-52, -168, -52, -160); s.lineTo(-52, -66); s.lineTo(0, -40);
    const hole = new THREE.Path(); hole.absarc(0, -62, 6, 0, Math.PI * 2, true); s.holes.push(hole);
    const tg = new THREE.ExtrudeGeometry(s, { depth: 6, bevelEnabled: true, bevelThickness: 1.6, bevelSize: 1.6, bevelSegments: 3, curveSegments: 16 });
    tg.translate(0, 0, -3);
    O.tagSwing.add(new THREE.Mesh(tg, [M.tagFace, M.rose]));
    const eyelet = new THREE.Mesh(new THREE.TorusGeometry(6.5, 1.4, 10, 32), M.rose); eyelet.position.set(0, -62, 4.8); O.tagSwing.add(eyelet);
  }

  // B04 map pin (lathe) + soft shadow
  O.pin = new THREE.Group(); O.pin.position.copy(px(150, 834, 20)); O.pinScale = 1.35; scene.add(O.pin);
  O.pinBody = new THREE.Group(); O.pin.add(O.pinBody);
  {
    const prof = [[0, 0], [2.5, 7], [7, 19], [12.5, 33], [16, 45], [16.8, 53], [14.5, 61.5], [9.5, 67.5], [4, 70.2], [0, 70.8]].map(([x, y]) => new THREE.Vector2(x, y));
    const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 56), M.rose); O.pinBody.add(body);
    const dot = new THREE.Mesh(new THREE.SphereGeometry(6.8, 24, 16), M.white); dot.position.set(0, 52, 14.5); dot.scale.z = 0.5; O.pinBody.add(dot);
  }
  O.pinShadow = new THREE.Mesh(new THREE.CircleGeometry(20, 32), M.shadow); O.pinShadow.scale.set(1, 0.28, 1); O.pinShadow.position.set(0, -3, -4); O.pin.add(O.pinShadow);

  // Text meshes (built once the typeface loads)
  O.counts = []; O.plus = null; O.one = null; O.price = null;
  const textMats = [M.white, M.rose];
  function textGeo(font, str, size, depth, center) {
    const g = new THREE.TextGeometry(str, { font, size, height: depth, curveSegments: 10, bevelEnabled: true, bevelThickness: Math.max(1, depth * 0.08), bevelSize: Math.max(0.8, size * 0.012), bevelSegments: 3 });
    g.computeBoundingBox();
    if (center) { const b = g.boundingBox; g.translate(-(b.min.x + b.max.x) / 2, -(b.min.y + b.max.y) / 2, -depth / 2); }
    return g;
  }
  O.countG = new THREE.Group(); O.countG.position.copy(px(46, 820, 0)); scene.add(O.countG);
  O.oneG = new THREE.Group(); O.oneG.position.copy(px(160, 772, 30)); scene.add(O.oneG);
  new THREE.FontLoader().load("assets/3d/playfair-bold.typeface.json", (font) => {
    for (let n = 0; n <= 50; n++) {
      const m = new THREE.Mesh(textGeo(font, String(n), 118, 26, false), textMats);
      m.visible = false; O.countG.add(m); O.counts.push(m);
    }
    const w50 = O.counts[50].geometry.boundingBox.max.x;
    O.plus = new THREE.Mesh(textGeo(font, "+", 118, 26, true), textMats);
    O.plus.position.set(w50 + 52, 46, 0); O.countG.add(O.plus);
    O.one = new THREE.Mesh(textGeo(font, "1", 176, 40, true), textMats); O.oneG.add(O.one);
    O.price = new THREE.Mesh(textGeo(font, "£15", 34, 5, true), [M.white, M.rose]);
    O.price.position.set(0, -118, 6.5); O.tagSwing.add(O.price);
    redraw();
  });

  /* ---------- per-frame pose ---------- */
  const CUT = [2.333, 12.767, 22.133, 26.433];
  function pose(t) {
    // Timex (11.95 → cut 12.767): spins in to face camera, then idles
    {
      const on = t >= 11.95 && t < CUT[1];
      O.timex.visible = on;
      if (on) {
        const p = P(t, 11.95, 0.5);
        O.timex.rotation.set(0.25 * (1 - p) + 0.05 * Math.sin(t * 2), lerp(-Math.PI * 1.5, 0, E.out3(p)) + 0.22 * Math.sin((t - 11.95) * 2.4) * p, 0.06);
        O.timex.scale.setScalar(0.8 * lerp(0.4, 1, E.out3(P(t, 11.95, 0.3))));
      }
    }
    // Rolex (21.38 → cut 22.133)
    {
      const on = t >= 21.38 && t < CUT[2];
      O.rolex.visible = on;
      if (on) {
        const p = P(t, 21.38, 0.45);
        O.rolex.rotation.set(-0.2 * (1 - p) + 0.05 * Math.sin(t * 2.2), lerp(Math.PI * 1.5, 0, E.out3(p)) - 0.2 * Math.sin((t - 21.38) * 2.6) * p, -0.05);
        O.rolex.scale.setScalar(0.78 * lerp(0.4, 1, E.out3(P(t, 21.38, 0.28))));
      }
    }
    // Minis (22.3 + i*0.255, out at cut 26.433)
    O.minis.forEach((w, i) => {
      const t0 = 22.3 + i * 0.255;
      const on = t >= t0 && t < CUT[3];
      w.visible = on;
      if (on) {
        const p = P(t, t0, F(14));
        w.scale.setScalar(lerp(0.3, 1, E.out3(p)));
        w.rotation.set(0.3 * Math.sin(t * 1.3 + i), lerp(Math.PI, 0, E.out3(p)) + 0.35 * Math.sin(t * 1.7 + i * 0.9), 0);
      }
    });
    // Counter 0 → 50 (22.2 → 24.95), + snaps at 24.95, out at cut
    {
      const on = t >= 22.15 && t < CUT[3];
      O.countG.visible = on;
      if (on) {
        const pr = P(t, 22.2, 24.95 - 22.2);
        const v = Math.floor(50 * E.out2(pr) + 1e-6);
        O.counts.forEach((m, n) => (m.visible = n === v));
        const pe = E.out3(P(t, 22.15, F(14)));
        O.countG.rotation.set(lerp(-1.2, 0.1, pe), -0.32 + 0.1 * Math.sin((t - 22) * 1.1), 0);
        O.countG.position.copy(px(46, lerp(850, 820, pe), lerp(-80, 0, pe)));
        if (O.plus) {
          O.plus.visible = t >= 24.95;
          const pp = P(t, 24.95, F(9));
          O.plus.scale.setScalar(lerp(1.7, 1, E.expo(pp)));
          O.plus.rotation.y = lerp(1.4, 0, E.expo(pp));
        }
      }
    }
    // Plane + trail (3.05 → 4.2), fade 5.2–5.43
    {
      const on = t >= 3.02 && t < 5.45;
      const u = E.sine(P(t, 3.05, 1.15));
      const fade = 1 - P(t, 5.2, F(14));
      M.roseGlow.opacity = 1;
      O.trail.forEach((d) => { d.visible = on && d.userData.u <= u - 0.02; d.scale.setScalar(fade); });
      O.plane.visible = on;
      if (on) {
        const pos = O.flyCurve.getPoint(Math.max(0.001, u));
        const tan = O.flyCurve.getTangent(Math.max(0.001, u));
        O.plane.position.copy(pos);
        O.plane.rotation.set(0.35 * Math.sin(u * Math.PI) + 0.25, -0.25, Math.atan2(tan.y, tan.x));
        O.plane.scale.setScalar(lerp(0.9, 1.5, u) * fade);
      }
    }
    // Watch-roll ring (5.58 draw → 6.62 glide out)
    {
      const on = t >= 5.58 && t < 6.86;
      O.rollRingG.visible = on;
      if (on) {
        O.rollRing.userData.setP(E.out2(P(t, 5.58, F(16))));
        const out = 1 - E.in2(P(t, 6.62, F(14)));
        O.rollRingG.scale.setScalar(out);
        O.rollRing.rotation.z = (t - 5.58) * 0.6;
      }
    }
    // Price tag (12.98 swing in → 16.3 out)
    {
      const on = t >= 12.98 && t < 16.52;
      O.tag.visible = on;
      if (on) {
        O.tagSwing.rotation.z = kf(t, [[12.98, -1.08], [13.24, 0.16, E.out2], [13.48, -0.07, E.sine], [13.7, 0.026, E.sine], [13.9, 0, E.sine]]) + 0.012 * Math.sin((t - 13.9) * 2.2) * P(t, 13.9, 0.5);
        O.tagSwing.rotation.y = kf(t, [[12.98, 1.2], [13.5, -0.25, E.out3], [14.1, 0.12, E.sine]]) + 0.1 * Math.sin((t - 14.1) * 1.4) * P(t, 14.1, 0.6);
        const s = lerp(0.55, 1, E.out3(P(t, 12.98, 0.26))) * (1 - E.in2(P(t, 16.3, F(12))));
        O.tag.scale.setScalar(s);
      }
    }
    // Map pin (14.58 drop with one bounce → 16.32 out)
    {
      const on = t >= 14.58 && t < 16.5;
      O.pin.visible = on;
      if (on) {
        const y = kf(t, [[14.58, 160], [14.58 + F(11), 0, E.in2], [14.58 + F(17), 20, E.out2], [14.58 + F(23), 0, E.in2]]);
        O.pinBody.position.y = y;
        O.pinBody.rotation.y = lerp(Math.PI * 2, 0, E.out3(P(t, 14.58, 0.55))) + 0.3 * Math.sin((t - 14.6) * 1.6);
        O.pinShadow.scale.set(lerp(0.3, 1, cl(1 - y / 160)), 0.28 * lerp(0.3, 1, cl(1 - y / 160)), 1);
        O.pin.scale.setScalar(O.pinScale * (1 - E.in2(P(t, 16.32, F(10)))));
      }
    }
    // 5711R ring follows the lifted watch (27.3 → fade 28.12)
    {
      const on = t >= 27.3 && t < 28.34;
      O.pkRingG.visible = on;
      if (on) {
        O.pkRing.userData.setP(E.out2(P(t, 27.3, F(14))));
        // measured from the rendered footage at 125%
        const x = kf(t, [[27.3, 515], [27.5, 505, E.sine], [27.65, 465, E.sine], [27.8, 415, E.sine], [27.95, 392, E.sine], [28.1, 395, E.sine]]);
        const y = kf(t, [[27.3, 925], [27.5, 932, E.sine], [27.65, 872, E.sine], [27.8, 842, E.sine], [27.95, 832, E.sine], [28.1, 832, E.sine]]);
        O.pkRingG.position.copy(px(x, y, 0));
        O.pkRingG.rotation.set(0.45, -0.3, (t - 27.3) * 1.4);
        const fade = 1 - E.in2(P(t, 28.12, F(12)));
        O.pkRingG.scale.setScalar(lerp(0.85, 1, E.out3(P(t, 27.3, F(14)))) * fade);
      }
    }
    // The "1" (33.38 slam → end)
    {
      const on = t >= 33.38 && !!O.one;
      O.oneG.visible = on;
      if (on) {
        const p = P(t, 33.38, F(12));
        O.oneG.scale.setScalar(lerp(2.0, 1, E.expo(p)));
        O.oneG.rotation.set(0.06, lerp(-1.5, 0, E.expo(p)) + 0.2 * Math.sin((t - 33.6) * 1.5) * P(t, 33.5, 0.4), 0);
      }
    }
  }

  let lastT = 0;
  function render(t) {
    lastT = t;
    pose(t);
    renderer.render(scene, camera);
  }
  function redraw() { render(lastT); }

  window.addEventListener("hf-seek", (e) => render(Number(e.detail && e.detail.time) || 0));
  const root = window.__timelines && window.__timelines["main"];
  if (root) root.eventCallback("onUpdate", () => render(root.time()));
  window.__ws3d = { render };
  render(0);
})();
