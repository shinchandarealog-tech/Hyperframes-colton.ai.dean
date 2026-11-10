/* BK — shared Three.js kit for "Before the Doorbell".
   Everything is deterministic: scenes are pure functions of time t (seconds). */
(function () {
  const T = THREE;
  const C = {
    yellow: "#f8cb46", yellowDeep: "#e9b52c", green: "#0c831f", greenDeep: "#0a6f1a",
    ink: "#1c1a12", cream: "#fff7e2", creamDeep: "#f1e3bd", cold: "#cfe3f5", white: "#ffffff",
    skin: "#efc9a0", clay: "#f6f0e2",
  };

  // ---------- math / easing ----------
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const lerp = (a, b, u) => a + (b - a) * u;
  const E = {
    lin: (u) => u,
    inC: (u) => u * u * u,
    outC: (u) => 1 - Math.pow(1 - u, 3),
    inOutS: (u) => -(Math.cos(Math.PI * u) - 1) / 2,
    inOutC: (u) => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2),
    outExpo: (u) => (u >= 1 ? 1 : 1 - Math.pow(2, -10 * u)),
    inQ: (u) => u * u,
    outBack: (u, s = 1.70158) => 1 + (s + 1) * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2),
    outElastic: (u) => (u === 0 || u === 1 ? u : Math.pow(2, -10 * u) * Math.sin((u * 10 - 0.75) * ((2 * Math.PI) / 3)) + 1),
    outBounce: (u) => {
      const n = 7.5625, d = 2.75;
      if (u < 1 / d) return n * u * u;
      if (u < 2 / d) return n * (u -= 1.5 / d) * u + 0.75;
      if (u < 2.5 / d) return n * (u -= 2.25 / d) * u + 0.9375;
      return n * (u -= 2.625 / d) * u + 0.984375;
    },
  };
  function rng(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ---------- fonts for canvas textures ----------
  const FONTS = { ok: false, specs: ['800 40px "Bricolage Grotesque"', '800 40px "Plus Jakarta Sans"', '700 40px "Plus Jakarta Sans"', '600 40px "Plus Jakarta Sans"', '700 40px "Caveat"'] };
  try { FONTS.specs.forEach((s) => document.fonts.load(s)); } catch (e) {}
  function refreshFonts() {
    if (FONTS.ok) return;
    try { FONTS.ok = FONTS.specs.every((s) => document.fonts.check(s)); } catch (e) { FONTS.ok = true; }
  }

  // ---------- renderer / stage ----------
  function roomEnv(renderer) {
    const room = new T.Scene();
    const box = new T.Mesh(new T.BoxGeometry(10, 10, 10), new T.MeshBasicMaterial({ color: "#d9d2c3", side: T.BackSide }));
    room.add(box);
    const panel = (w, h, x, y, z, ry, rx, intensity) => {
      const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: new T.Color(intensity, intensity, intensity) }));
      m.position.set(x, y, z); m.rotation.set(rx || 0, ry || 0, 0); room.add(m);
    };
    panel(6, 2.2, 0, 4.9, 0, 0, Math.PI / 2, 3.2);   // big softbox overhead
    panel(2.5, 4, -4.9, 1, 1, Math.PI / 2, 0, 2.2);  // key strip left
    panel(2.5, 4, 4.9, 0.5, -1, -Math.PI / 2, 0, 1.3); // fill right
    panel(5, 2, 0, 1, 4.9, Math.PI, 0, 1.0);         // front fill
    const pm = new T.PMREMGenerator(renderer);
    const tex = pm.fromScene(room, 0.04).texture;
    pm.dispose();
    return tex;
  }

  function stage(canvas, opts = {}) {
    const renderer = new T.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: "high-performance" });
    renderer.setPixelRatio(1);
    renderer.setSize(1080, 1920, false);
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.LinearToneMapping;
    renderer.toneMappingExposure = opts.exposure || 0.92;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = T.VSMShadowMap;
    const scene = new T.Scene();
    scene.background = new T.Color(opts.bg || C.cream);
    scene.environment = roomEnv(renderer);
    const camera = new T.PerspectiveCamera(opts.fov || 32, 1080 / 1920, 0.05, 100);
    const hemi = new T.HemisphereLight("#ffffff", opts.ground || "#e9dcbd", opts.hemi ?? 0.55);
    scene.add(hemi);
    const key = new T.DirectionalLight("#fffaf0", opts.key ?? 2.2);
    key.position.set(...(opts.keyPos || [3, 6, 4]));
    key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024);
    key.shadow.radius = opts.shadowRadius ?? 10;
    key.shadow.blurSamples = 16;
    key.shadow.bias = -0.0006;
    const s = opts.shadowSize || 4;
    Object.assign(key.shadow.camera, { left: -s, right: s, top: s, bottom: -s, near: 0.1, far: 30 });
    scene.add(key);
    scene.add(key.target);
    // Depth of field: scene -> multisampled target with depth, then a disc-blur pass whose
    // radius grows with distance from the focus plane (like a real lens).
    const dof = { enabled: !!opts.dof, focus: 5, range: 2.5, maxBlur: opts.dof?.maxBlur ?? 14 };
    let rt, post, postCam, postMat;
    if (dof.enabled) {
      rt = new T.WebGLRenderTarget(1080, 1920, { samples: 4, type: T.HalfFloatType });
      rt.depthTexture = new T.DepthTexture(1080, 1920);
      postMat = new T.ShaderMaterial({
        uniforms: { tColor: { value: rt.texture }, tDepth: { value: rt.depthTexture }, focus: { value: 5 }, range: { value: 2.5 },
          maxBlur: { value: dof.maxBlur }, near: { value: camera.near }, far: { value: camera.far }, res: { value: new T.Vector2(1080, 1920) } },
        vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
        fragmentShader: `
          uniform sampler2D tColor; uniform sampler2D tDepth; uniform float focus, range, maxBlur, near, far; uniform vec2 res; varying vec2 vUv;
          float lin(float d){ float z = d * 2.0 - 1.0; return 2.0 * near * far / (far + near - z * (far - near)); }
          float coc(vec2 uv){ return clamp(abs(lin(texture2D(tDepth, uv).x) - focus) / range, 0.0, 1.0) * maxBlur; }
          void main(){
            float c0 = coc(vUv); vec4 acc = texture2D(tColor, vUv); float w = 1.0;
            for (int i = 1; i < 32; i++) {
              float a = float(i) * 2.39996; float r = sqrt(float(i) / 31.0);
              vec2 uv = vUv + vec2(cos(a), sin(a)) * r * c0 / res;
              float ci = coc(uv);
              float wi = smoothstep(0.0, 1.0, ci / max(c0, 0.001) + 0.15);   // keep sharp foreground edges from bleeding
              acc += texture2D(tColor, uv) * wi; w += wi;
            }
            gl_FragColor = acc / w;
            #include <tonemapping_fragment>
            #include <colorspace_fragment>
          }`,
        depthTest: false, depthWrite: false, toneMapped: true,
      });
      post = new T.Scene(); post.add(new T.Mesh(new T.PlaneGeometry(2, 2), postMat));
      postCam = new T.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    }
    return {
      renderer, scene, camera, key, hemi, dof,
      render() {
        refreshFonts();
        if (!dof.enabled) { renderer.render(scene, camera); return; }
        postMat.uniforms.focus.value = dof.focus; postMat.uniforms.range.value = dof.range; postMat.uniforms.maxBlur.value = dof.maxBlur;
        postMat.uniforms.near.value = camera.near; postMat.uniforms.far.value = camera.far;
        renderer.setRenderTarget(rt); renderer.render(scene, camera);
        renderer.setRenderTarget(null); renderer.render(post, postCam);
      },
    };
  }

  // ---------- materials ----------
  const M = {
    clay: (c, r = 0.82) => new T.MeshStandardMaterial({ color: c, roughness: r, metalness: 0, envMapIntensity: 0.45 }),
    plastic: (c, r = 0.32, cc = 0.6) => new T.MeshPhysicalMaterial({ color: c, roughness: r, metalness: 0, clearcoat: cc, clearcoatRoughness: 0.25, envMapIntensity: 0.55 }),
    gloss: (c) => new T.MeshPhysicalMaterial({ color: c, roughness: 0.2, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 0.7 }),
    glass: (c = "#ffffff", o = 0.35) => new T.MeshPhysicalMaterial({ color: c, roughness: 0.08, metalness: 0, transparent: true, opacity: o, clearcoat: 1 }),
    paper: (c) => new T.MeshStandardMaterial({ color: c, roughness: 0.92, metalness: 0, envMapIntensity: 0.4 }),
    basic: (c) => new T.MeshBasicMaterial({ color: c }),
    tex: (tex, r = 0.4, transparent = true) => new T.MeshStandardMaterial({ map: tex, roughness: r, metalness: 0, transparent, envMapIntensity: 0.4 }),
  };

  // ---------- geometry ----------
  function roundedShape(w, h, r) {
    const s = new T.Shape(), x = -w / 2, y = -h / 2;
    r = Math.min(r, w / 2, h / 2);
    s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
    s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
    s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
    return s;
  }
  // rounded, bevelled slab centred on origin (x=w, y=h, z=d)
  function rbox(w, h, d, r, bevel) {
    const b = bevel ?? Math.min(d * 0.35, r * 0.6);
    const g = new T.ExtrudeGeometry(roundedShape(w - 2 * b, h - 2 * b, Math.max(0.001, r - b)), {
      depth: Math.max(0.001, d - 2 * b), bevelEnabled: true, bevelThickness: b, bevelSize: b, bevelSegments: 5, curveSegments: 10,
    });
    g.translate(0, 0, -(d - 2 * b) / 2);
    g.computeVertexNormals();
    return g;
  }
  function mesh(geo, mat, cast = true, receive = true) {
    const m = new T.Mesh(geo, mat); m.castShadow = cast; m.receiveShadow = receive; return m;
  }
  // a textured card face on the front of an rbox
  function face(w, h, tex, z, r = 0.45) {
    const m = new T.Mesh(new T.ShapeGeometry(roundedShape(w, h, Math.min(w, h) * 0.12), 6), M.tex(tex, r));
    // UVs for ShapeGeometry are in shape units; remap to 0..1
    const uv = m.geometry.attributes.uv, pos = m.geometry.attributes.position;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / w + 0.5, pos.getY(i) / h + 0.5);
    m.position.z = z; m.receiveShadow = true;
    return m;
  }

  // ---------- canvas text textures ----------
  const TEXS = [];
  function canvasTex(w, h, draw) {
    const c = document.createElement("canvas"); c.width = w; c.height = h;
    const ctx = c.getContext("2d");
    const tex = new T.CanvasTexture(c);
    tex.colorSpace = T.SRGBColorSpace; tex.anisotropy = 8;
    const o = {
      tex, ctx, w, h, state: undefined, fonts: null,
      set(state) {
        refreshFonts();
        if (state === o.state && o.fonts === FONTS.ok) return;
        o.state = state; o.fonts = FONTS.ok;
        ctx.clearRect(0, 0, w, h); draw(ctx, state, w, h); tex.needsUpdate = true;
      },
    };
    o.set(null); TEXS.push(o);
    return o;
  }
  function rr(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function wordmark(ctx, x, y, size, align = "center") {
    ctx.font = `800 ${size}px "Bricolage Grotesque", "Plus Jakarta Sans", sans-serif`;
    ctx.textBaseline = "middle";
    const a = ctx.measureText("blink").width, b = ctx.measureText("it").width, tot = a + b - size * 0.04;
    let sx = align === "center" ? x - tot / 2 : x;
    ctx.fillStyle = C.ink; ctx.textAlign = "left"; ctx.fillText("blink", sx, y);
    ctx.fillStyle = C.green; ctx.fillText("it", sx + a - size * 0.04, y);
  }

  // soft contact shadow (grounding) — radial gradient decal
  let _blob = null;
  function blob(w, d, opacity = 0.35) {
    if (!_blob) {
      const c = document.createElement("canvas"); c.width = c.height = 128;
      const g = c.getContext("2d"), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
      gr.addColorStop(0, "rgba(40,32,10,1)"); gr.addColorStop(0.45, "rgba(40,32,10,0.45)"); gr.addColorStop(1, "rgba(40,32,10,0)");
      g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
      _blob = new T.CanvasTexture(c);
    }
    const m = new T.Mesh(new T.PlaneGeometry(w, d), new T.MeshBasicMaterial({ map: _blob, transparent: true, opacity, depthWrite: false }));
    m.rotation.x = -Math.PI / 2; m.renderOrder = 1;
    return m;
  }

  // ---------- models (all ~1 unit tall, origin at bottom centre) ----------
  function milk() {
    const g = new T.Group();
    const body = mesh(new T.BoxGeometry(0.5, 0.72, 0.5), M.plastic(C.white, 0.45, 0.3)); body.position.y = 0.36; g.add(body);
    const lab = canvasTex(256, 256, (x) => {
      x.fillStyle = C.cold; x.fillRect(0, 70, 256, 120);
      x.fillStyle = C.ink; x.font = '800 62px "Plus Jakarta Sans", sans-serif'; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText("MILK", 128, 132);
    });
    const lm = new T.Mesh(new T.PlaneGeometry(0.5, 0.5), new T.MeshStandardMaterial({ map: lab.tex, transparent: true, roughness: 0.5 }));
    lm.position.set(0, 0.38, 0.252); g.add(lm);
    const roofShape = new T.Shape(); roofShape.moveTo(-0.25, 0); roofShape.lineTo(0.25, 0); roofShape.lineTo(0, 0.24); roofShape.closePath();
    const roof = mesh(new T.ExtrudeGeometry(roofShape, { depth: 0.5, bevelEnabled: false }), M.plastic(C.white, 0.45, 0.3));
    roof.position.set(0, 0.72, -0.25); g.add(roof);
    const fin = mesh(new T.BoxGeometry(0.06, 0.1, 0.5), M.plastic(C.white, 0.45, 0.3)); fin.position.set(0, 0.99, 0); g.add(fin);
    const cap = mesh(new T.CylinderGeometry(0.06, 0.06, 0.06, 24), M.plastic(C.green, 0.3)); cap.position.set(0.12, 0.86, 0.12); cap.rotation.z = -0.78; g.add(cap);
    return g;
  }
  function chips() {
    const g = new T.Group();
    const geo = new T.SphereGeometry(0.5, 40, 24); geo.scale(0.95, 1.0, 0.32);
    const p = geo.attributes.position; // flatten top & bottom edges into crimped seams
    for (let i = 0; i < p.count; i++) { const y = p.getY(i); if (Math.abs(y) > 0.36) { p.setZ(i, p.getZ(i) * 0.25); } }
    geo.computeVertexNormals();
    const bag = mesh(geo, M.gloss(C.yellow)); bag.position.y = 0.5; g.add(bag);
    const lab = canvasTex(256, 256, (x) => {
      x.fillStyle = C.cream; x.beginPath(); x.arc(128, 112, 56, 0, Math.PI * 2); x.fill();
      x.fillStyle = "#e9a93a"; x.beginPath(); x.ellipse(128, 112, 36, 30, 0.3, 0, Math.PI * 2); x.fill();
      x.fillStyle = C.green; x.font = '800 46px "Plus Jakarta Sans", sans-serif'; x.textAlign = "center"; x.fillText("CHIPS", 128, 214);
    });
    const lm = new T.Mesh(new T.PlaneGeometry(0.62, 0.62), new T.MeshStandardMaterial({ map: lab.tex, transparent: true, roughness: 0.3 }));
    lm.position.set(0, 0.5, 0.165); g.add(lm);
    return g;
  }
  function ice() {
    const g = new T.Group();
    const geo = new T.CylinderGeometry(0.32, 0.4, 0.78, 32, 1, false); const bag = mesh(geo, M.plastic("#a9cdee", 0.25, 1)); bag.position.y = 0.39; g.add(bag);
    const tie = mesh(new T.ConeGeometry(0.12, 0.22, 20), M.glass("#dcecf9", 0.7)); tie.position.y = 0.88; g.add(tie);
    const knot = mesh(new T.TorusGeometry(0.06, 0.025, 10, 20), M.plastic(C.green, 0.3)); knot.position.y = 0.79; knot.rotation.x = Math.PI / 2; g.add(knot);
    const r = rng(9), cubeM = M.gloss("#e8f3fc"), cg = rbox(0.17, 0.17, 0.17, 0.04, 0.02);
    for (let i = 0; i < 9; i++) { const c = mesh(cg, cubeM); const ang = r() * 2.4 - 1.2; c.position.set(Math.sin(ang) * 0.36, 0.14 + r() * 0.5, Math.cos(ang) * 0.36); c.rotation.set(r() * 3, r() * 3, r() * 3); g.add(c); }
    return g;
  }
  function cake() {
    const g = new T.Group();
    const base = mesh(new T.CylinderGeometry(0.46, 0.46, 0.2, 48), M.clay(C.cream, 0.6)); base.position.y = 0.1; g.add(base);
    const mid = mesh(new T.CylinderGeometry(0.46, 0.46, 0.08, 48), M.clay(C.yellow, 0.55)); mid.position.y = 0.24; g.add(mid);
    const top = mesh(new T.CylinderGeometry(0.46, 0.46, 0.2, 48), M.clay(C.cream, 0.6)); top.position.y = 0.38; g.add(top);
    const glaze = mesh(new T.CylinderGeometry(0.48, 0.48, 0.07, 48), M.gloss("#3a2a1c")); glaze.position.y = 0.5; g.add(glaze);
    const candle = mesh(new T.CylinderGeometry(0.035, 0.035, 0.24, 16), M.plastic(C.green)); candle.position.y = 0.66; g.add(candle);
    const flame = mesh(new T.SphereGeometry(0.045, 16, 12), new T.MeshBasicMaterial({ color: "#ffd25a" })); flame.scale.y = 1.6; flame.position.y = 0.83; g.add(flame);
    return g;
  }
  const PRODUCT = { milk, chips, ice, cake };

  // open-top paper bag (origin bottom centre), front printed with the wordmark
  function bag(w = 1.0, h = 1.0, d = 0.66) {
    const g = new T.Group(), th = 0.025, pm = M.paper(C.yellow), inner = M.paper("#d9a827");
    const front = canvasTex(512, 512, (x) => { x.fillStyle = C.yellow; x.fillRect(0, 0, 512, 512); wordmark(x, 256, 300, 128); });
    const fm = [pm, pm, pm, pm, new T.MeshStandardMaterial({ map: front.tex, roughness: 0.9 }), inner];
    const add = (geo, mats, x, y, z) => { const m = mesh(geo, mats); m.position.set(x, y, z); g.add(m); return m; };
    add(new T.BoxGeometry(w, h, th), fm, 0, h / 2, d / 2);
    add(new T.BoxGeometry(w, h, th), [pm, pm, pm, pm, inner, pm], 0, h / 2, -d / 2);
    add(new T.BoxGeometry(th, h, d), [pm, inner, pm, pm, pm, pm], w / 2, h / 2, 0);
    add(new T.BoxGeometry(th, h, d), [inner, pm, pm, pm, pm, pm], -w / 2, h / 2, 0);
    add(new T.BoxGeometry(w, th, d), inner, 0, th / 2, 0);
    const rim = M.paper(C.yellowDeep);
    add(new T.BoxGeometry(w + 0.03, 0.09, th * 1.6), rim, 0, h - 0.045, d / 2 + 0.01);
    add(new T.BoxGeometry(w + 0.03, 0.09, th * 1.6), rim, 0, h - 0.045, -d / 2 - 0.01);
    const dark = mesh(new T.PlaneGeometry(w - 0.04, d - 0.04), new T.MeshBasicMaterial({ color: "#3a2f12" }), false, false);
    dark.rotation.x = -Math.PI / 2; dark.position.y = h * 0.55; g.add(dark);
    g.userData.dark = dark;
    return g;
  }

  function thumb() {
    const g = new T.Group();
    const f = mesh(new T.CapsuleGeometry(0.11, 0.7, 10, 24), M.clay(C.skin, 0.55)); f.position.y = -0.46; g.add(f);
    const nail = mesh(new T.SphereGeometry(0.075, 20, 14), M.plastic("#f7dcc2", 0.3, 0.5)); nail.scale.set(1, 1.25, 0.35); nail.position.set(0, -0.12, 0.095); g.add(nail);
    return g; // tip at origin, finger extends down -y
  }

  function appIcon(size = 1, depth = 0.2) {
    const g = new T.Group();
    const body = mesh(rbox(size, size, depth, size * 0.24), M.gloss(C.yellow)); g.add(body);
    const tx = canvasTex(512, 512, (x) => { wordmark(x, 256, 262, 150); });
    const f = face(size * 0.94, size * 0.94, tx.tex, depth / 2 + 0.002, 0.3); f.material.transparent = true; g.add(f); g.userData.face = f;
    return g;
  }

  function scooter() {
    const g = new T.Group();
    const body = mesh(new T.CapsuleGeometry(0.06, 0.16, 8, 16), M.gloss(C.yellow)); body.rotation.z = Math.PI / 2; body.position.y = 0.09; g.add(body);
    const box = mesh(rbox(0.13, 0.12, 0.13, 0.03), M.gloss(C.yellow)); box.position.set(-0.08, 0.2, 0); g.add(box);
    const wM = M.plastic(C.ink, 0.5, 0.2), wG = new T.TorusGeometry(0.045, 0.02, 10, 20);
    [-0.1, 0.11].forEach((x) => { const w = mesh(wG, wM); w.position.set(x, 0.045, 0); g.add(w); });
    const rider = mesh(new T.CapsuleGeometry(0.045, 0.09, 8, 14), M.clay(C.green, 0.5)); rider.position.set(0.03, 0.22, 0); g.add(rider);
    const head = mesh(new T.SphereGeometry(0.05, 20, 14), M.gloss(C.green)); head.position.set(0.04, 0.33, 0); g.add(head);
    return g; // faces +x
  }

  function pin(color = C.ink) {
    const g = new T.Group();
    const head = mesh(new T.SphereGeometry(0.16, 32, 20), M.gloss(color)); head.position.y = 0.42; g.add(head);
    const cone = mesh(new T.ConeGeometry(0.11, 0.3, 32), M.gloss(color)); cone.rotation.x = Math.PI; cone.position.y = 0.2; g.add(cone);
    const home = mesh(rbox(0.12, 0.09, 0.05, 0.015), M.clay(C.cream, 0.5)); home.position.set(0, 0.41, 0.15); g.add(home);
    const roofS = new T.Shape(); roofS.moveTo(-0.09, 0); roofS.lineTo(0.09, 0); roofS.lineTo(0, 0.07); roofS.closePath();
    const roof = mesh(new T.ExtrudeGeometry(roofS, { depth: 0.04, bevelEnabled: false }), M.clay(C.cream, 0.5)); roof.position.set(0, 0.45, 0.13); g.add(roof);
    return g;
  }

  function star(r = 0.3, depth = 0.1, color = C.cream) {
    const s = new T.Shape();
    for (let i = 0; i < 10; i++) { const a = (i / 10) * Math.PI * 2 + Math.PI / 2, rr2 = i % 2 ? r * 0.45 : r; const x = Math.cos(a) * rr2, y = Math.sin(a) * rr2; i ? s.lineTo(x, y) : s.moveTo(x, y); }
    s.closePath();
    const g = new T.ExtrudeGeometry(s, { depth, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 4 });
    g.translate(0, 0, -depth / 2); g.computeVertexNormals();
    return mesh(g, M.gloss(color));
  }

  window.BK = { T, C, E, clamp, seg, lerp, rng, stage, M, rbox, roundedShape, mesh, face, canvasTex, rr, wordmark, blob,
    PRODUCT, milk, chips, ice, cake, bag, thumb, appIcon, scooter, pin, star, FONTS, refreshFonts };
})();
