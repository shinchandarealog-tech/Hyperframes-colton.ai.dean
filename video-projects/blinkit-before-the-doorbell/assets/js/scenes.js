/* The 9 beats as Three.js scenes. Each builder returns draw(t) where t is GLOBAL time. */
(function () {
  const { T, C, E, seg, lerp, clamp, rng, stage, M, rbox, mesh, face, canvasTex, rr, wordmark, blob } = BK;
  const S = {};
  const V = (x, y, z) => new T.Vector3(x, y, z);
  const wob = (t, a, b, amp, freq) => (t < a ? 0 : amp * Math.exp(-(t - a) * b) * Math.sin((t - a) * freq));

  // ============ B1 · inside the fridge (0–1.5) ============
  S.fridge = function (cv) {
    const st = stage(cv, { bg: "#9fbfdd", ground: "#8fb0d0", hemi: 0.45, key: 1.3, keyPos: [0.8, 4, 4.5], fov: 44, shadowSize: 2.5, exposure: 1.1 });
    const { scene, camera } = st;
    const inside = mesh(new T.BoxGeometry(2.0, 3.8, 2.3), new T.MeshStandardMaterial({ color: "#d5e6f6", roughness: 0.5, side: T.BackSide, envMapIntensity: 0.3 }), false, true);
    inside.position.set(0, 0.05, -0.2); scene.add(inside);
    const cool = new T.PointLight("#e6f2ff", 5, 6, 1.4); cool.position.set(0, 1.55, 0.1); scene.add(cool);
    const strip = mesh(new T.BoxGeometry(1.3, 0.05, 0.12), new T.MeshBasicMaterial({ color: "#ffffff" }), false, false); strip.position.set(0, 1.9, 0.45); scene.add(strip);
    const glass = M.glass("#f4f9ff", 0.28), edge = M.plastic("#ffffff", 0.2, 1);
    [0.8, -0.25, -1.2].forEach((y) => {
      const s = mesh(new T.BoxGeometry(1.96, 0.035, 2.05), glass, false, true); s.position.set(0, y, -0.2); scene.add(s);
      const e = mesh(new T.BoxGeometry(1.96, 0.05, 0.04), edge); e.position.set(0, y, 0.82); scene.add(e);
    });
    // top shelf
    const jar = new T.Group(); jar.add(mesh(new T.CylinderGeometry(0.17, 0.17, 0.34, 40), M.plastic(C.white, 0.35)));
    const lid = mesh(new T.CylinderGeometry(0.18, 0.18, 0.08, 40), M.gloss(C.yellow)); lid.position.y = 0.2; jar.add(lid);
    jar.position.set(-0.58, 0.8 + 0.19, -0.35); scene.add(jar);
    const jar2 = new T.Group(); jar2.add(mesh(new T.CylinderGeometry(0.13, 0.13, 0.26, 40), M.glass("#cfe3f5", 0.75)));
    const lid2 = mesh(new T.CylinderGeometry(0.135, 0.135, 0.07, 40), M.gloss(C.green)); lid2.position.y = 0.16; jar2.add(lid2);
    jar2.position.set(-0.2, 0.8 + 0.15, -0.55); scene.add(jar2);
    const prof = [V(0, 0, 0), V(0.14, 0, 0), V(0.15, 0.3, 0), V(0.12, 0.42, 0), V(0.06, 0.5, 0), V(0.06, 0.6, 0), V(0, 0.6, 0)].map((v) => new T.Vector2(v.x, v.y));
    const bottle = mesh(new T.LatheGeometry(prof, 40), M.plastic(C.white, 0.3)); bottle.position.set(0.58, 0.82, -0.45); scene.add(bottle);
    const band = mesh(new T.CylinderGeometry(0.152, 0.152, 0.12, 40, 1, true), M.clay(C.yellow, 0.5)); band.position.set(0.58, 0.82 + 0.18, -0.45); scene.add(band);
    // middle shelf — the EMPTY carton, tipped over
    const carton = BK.milk(); carton.scale.setScalar(0.62); scene.add(carton);
    const puddle = mesh(new T.CylinderGeometry(0.15, 0.15, 0.006, 40), M.gloss("#ffffff")); puddle.scale.x = 1.6; puddle.position.set(-0.5, -0.23, 0.15); scene.add(puddle);
    // bottom shelf — egg tray, two eggs
    const tray = mesh(rbox(0.74, 0.12, 0.36, 0.04), M.clay(C.creamDeep, 0.8)); tray.position.set(-0.05, -1.12, -0.2); scene.add(tray);
    [-0.25, -0.02].forEach((x) => { const e = mesh(new T.SphereGeometry(0.1, 32, 20), M.plastic("#fbf6ee", 0.4, 0.2)); e.scale.y = 1.28; e.position.set(x, -0.96, -0.2); scene.add(e); });
    const butter = mesh(rbox(0.36, 0.14, 0.24, 0.03), M.plastic(C.yellow, 0.4)); butter.position.set(0.55, -1.11, -0.3); scene.add(butter);
    // sticky note on the back wall
    const nt = canvasTex(512, 512, (x) => {
      x.fillStyle = C.yellow; x.fillRect(0, 0, 512, 512);
      x.fillStyle = "rgba(255,255,255,0.55)"; x.fillRect(170, 0, 170, 46);
      x.fillStyle = C.ink; x.textAlign = "center"; x.textBaseline = "middle"; x.font = '700 132px "Caveat", cursive';
      x.fillText("Guests", 256, 210); x.fillText("8:00!", 256, 350);
    });
    const note = mesh(new T.PlaneGeometry(0.52, 0.52), new T.MeshStandardMaterial({ map: nt.tex, roughness: 0.85 }), true, false);
    note.position.set(0.48, 0.45, -1.33); note.rotation.z = -0.06; note.scale.setScalar(0.85); scene.add(note);
    // door on a hinge (left edge)
    const hinge = new T.Group(); hinge.position.set(-1.0, 0.05, 0.98); scene.add(hinge);
    const door = mesh(rbox(2.05, 3.85, 0.16, 0.12), M.plastic("#f3f6f9", 0.45, 0.3)); door.position.set(1.025, 0, 0); hinge.add(door);
    [0.75, -0.6].forEach((y) => { const b = mesh(rbox(1.6, 0.36, 0.3, 0.05), M.glass("#eaf3fb", 0.7)); b.position.set(1.03, y, -0.22); hinge.add(b); });
    const handle = mesh(rbox(0.07, 0.9, 0.08, 0.035), M.plastic("#c9d6e2", 0.3)); handle.position.set(1.85, 0, 0.12); hinge.add(handle);
    return function (t) {
      hinge.rotation.y = lerp(-1.3, -1.95, E.outC(seg(t, 0.0, 0.45)));
      const tip = wob(t, 0.45, 5, 0.12, 14);
      carton.rotation.set(0, 0.35, -Math.PI / 2 + 0.06 + tip);
      carton.position.set(0.12, -0.25 + 0.017 + 0.155, -0.15);
      const u = E.outC(seg(t, 0.12, 1.55));
      camera.position.set(lerp(-0.05, 0.06, u), lerp(0.05, -0.12, u), lerp(4.6, 3.35, u));
      camera.lookAt(lerp(0, 0.1, u), lerp(-0.12, -0.22, u), -0.4);
      st.render();
    };
  };

  // ============ B2 · phone + glossy icon (1.5–3.0) ============
  S.phone = function (cv) {
    const st = stage(cv, { bg: "#fbeec8", hemi: 0.65, key: 2.0, keyPos: [2.5, 4.5, 6], fov: 30, shadowSize: 2.5 });
    const { scene, camera } = st;
    const back = mesh(new T.PlaneGeometry(14, 14), M.clay("#fbeec8", 0.95), false, true); back.position.z = -0.7; scene.add(back);
    const phone = new T.Group(); scene.add(phone);
    phone.add(mesh(rbox(1.0, 2.05, 0.1, 0.17), M.gloss(C.ink)));
    const W = 540, H = 1140, k = 0.94 / W;
    const scr = canvasTex(W, H, (x) => {
      const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#fff7e2"); g.addColorStop(1, "#f1dfa6"); x.fillStyle = g; x.fillRect(0, 0, W, H);
      x.fillStyle = C.ink; x.font = '700 30px "Plus Jakarta Sans", sans-serif'; x.textBaseline = "middle";
      x.textAlign = "left"; x.fillText("7:50", 52, 50); x.textAlign = "right"; x.fillText("94%", W - 52, 50);
      rr(x, W / 2 - 62, 30, 124, 40, 20); x.fill();
      const cols = ["#cfe3f5", C.green, C.yellow, C.ink, "#e9d9a8", "#cfe3f5", C.ink, C.green, "#e9d9a8", C.yellow, "#cfe3f5", C.ink];
      for (let i = 0; i < 12; i++) {
        const cx = 70 + (i % 4) * 116, cy = 150 + Math.floor(i / 4) * 140;
        x.shadowColor = "rgba(60,40,0,0.18)"; x.shadowBlur = 14; x.shadowOffsetY = 6;
        x.fillStyle = cols[i]; rr(x, cx, cy, 84, 84, 22); x.fill();
        x.shadowColor = "transparent";
        x.strokeStyle = "rgba(255,255,255,0.85)"; x.lineWidth = 6; x.beginPath();
        if (i % 3 === 0) x.arc(cx + 42, cy + 42, 16, 0, 7); else rr(x, cx + 26, cy + 26, 32, 32, i % 3 === 1 ? 8 : 16); x.stroke();
      }
      x.fillStyle = "rgba(255,255,255,0.55)"; rr(x, 35, H - 160, W - 70, 120, 40); x.fill();
      const dock = [C.cold, null, C.green, C.ink];
      dock.forEach((c, i) => { if (!c) return; x.fillStyle = c; rr(x, 63 + i * 110, H - 142, 84, 84, 22); x.fill(); });
    });
    const sf = face(0.94, 1.99, scr.tex, 0.052, 0.25); sf.material.transparent = false; phone.add(sf);
    const icon = BK.appIcon(0.15, 0.05); scene.add(icon);
    const iconLocal = V((105 - 270 + 0) * k, (570 - (H - 100)) * k, 0.085);
    const th = BK.thumb(); th.scale.setScalar(0.62); phone.add(th);
    const tmp = new T.Vector3(), q0 = new T.Quaternion(), q1 = new T.Quaternion();
    camera.position.set(0, 0, 5.2); camera.lookAt(0, -0.05, 0);
    return function (t) {
      const u = E.inOutS(seg(t, 1.4, 3.05));
      phone.rotation.set(lerp(-0.3, -0.16, u), lerp(0.4, 0.2, u), lerp(0.05, 0.0, u));
      phone.position.set(0, lerp(-0.08, 0.02, u), 0);
      phone.updateMatrixWorld(true);
      // thumb: enter, press, release, leave
      const inn = E.outC(seg(t, 1.72, 2.06)), press = seg(t, 2.08, 2.15) - seg(t, 2.16, 2.3), out = E.inQ(seg(t, 2.47, 2.8));
      th.position.set(iconLocal.x + 0.03, iconLocal.y - 0.02 - (1 - inn) * 1.6 - out * 1.8, 0.12 - press * 0.04);
      th.rotation.set(-0.55, 0, 0.32);
      // icon: sits in the dock, squashes on press, then flies to fill the frame
      tmp.copy(iconLocal); tmp.z -= press * 0.02; phone.localToWorld(tmp);
      phone.getWorldQuaternion(q0);
      const f = E.inC(seg(t, 2.36, 2.78));
      icon.userData.face.material.opacity = 1 - seg(t, 2.46, 2.6);
      const pop = 1 - 0.1 * press + 0.08 * E.outBack(seg(t, 2.16, 2.36)) * (1 - f);
      icon.position.set(lerp(tmp.x, 0, f), lerp(tmp.y, -0.15, f), lerp(tmp.z, 4.96, f));
      icon.quaternion.copy(q0).slerp(q1, E.outC(seg(t, 2.36, 2.7)));
      icon.scale.setScalar(pop * lerp(1, 4, f));
      st.render();
    };
  };

  // ============ B3 · floating app UI with 3D products (3.0–5.0) ============
  const PRODUCTS = [
    { k: "milk", nm: "Toned Milk", wt: "500 ml", pr: "₹32" },
    { k: "chips", nm: "Masala Chips", wt: "52 g", pr: "₹20" },
    { k: "ice", nm: "Ice Cubes", wt: "1 kg", pr: "₹50" },
    { k: "cake", nm: "Chocolate Cake", wt: "500 g", pr: "₹384" },
  ];
  S.app = function (cv) {
    const st = stage(cv, { bg: C.cream, hemi: 0.6, key: 2.0, keyPos: [2.5, 4, 5.5], fov: 30, shadowSize: 2.6 });
    const { scene, camera } = st;
    const back = mesh(new T.PlaneGeometry(14, 14), M.clay(C.cream, 0.95), false, true); back.position.z = -0.42; scene.add(back);
    const ui = new T.Group(); scene.add(ui);
    const head = mesh(rbox(1.62, 0.66, 0.08, 0.08), M.plastic(C.yellow, 0.55, 0.08)); head.position.set(0, 1.2, 0); ui.add(head);
    const ht = canvasTex(1024, 418, (x) => {
      x.fillStyle = C.ink; x.textBaseline = "alphabetic"; x.textAlign = "left";
      x.font = '700 50px "Plus Jakarta Sans", sans-serif'; x.fillText("Delivery in", 60, 110);
      x.font = '800 150px "Bricolage Grotesque", sans-serif'; x.fillText("10 minutes", 52, 255);
      x.fillStyle = "#4a3f16"; x.font = '600 44px "Plus Jakarta Sans", sans-serif'; x.fillText("Home · Indiranagar, Bengaluru", 60, 345);
    });
    head.add(face(1.62, 0.66, ht.tex, 0.042, 0.4));
    const bar = mesh(rbox(1.52, 0.2, 0.08, 0.1), M.plastic(C.white, 0.35)); bar.position.set(0, 0.8, 0.09); ui.add(bar);
    const QUERY = "milk, chips, ice, cake…";
    const bt = canvasTex(1024, 135, (x, s) => {
      s = s || "0|1"; const [n, caret] = s.split("|").map(Number);
      x.strokeStyle = C.ink; x.lineWidth = 9; x.beginPath(); x.arc(70, 62, 22, 0, 7); x.stroke(); x.beginPath(); x.moveTo(86, 80); x.lineTo(104, 98); x.stroke();
      x.fillStyle = C.ink; x.font = '700 60px "Plus Jakarta Sans", sans-serif'; x.textBaseline = "middle"; x.textAlign = "left";
      const txt = QUERY.slice(0, n); x.fillText(txt, 135, 70);
      if (caret) { const w = x.measureText(txt).width; x.fillStyle = C.green; x.fillRect(140 + w, 34, 7, 72); }
    });
    bar.add(face(1.52, 0.2, bt.tex, 0.042, 0.4));
    const cards = PRODUCTS.map((p, i) => {
      const g = new T.Group();
      const c = mesh(rbox(0.76, 0.96, 0.06, 0.07), M.plastic(C.white, 0.38)); g.add(c);
      const tx = canvasTex(512, 646, (x, added) => {
        x.fillStyle = C.ink; x.textAlign = "left"; x.textBaseline = "alphabetic";
        x.font = '800 44px "Plus Jakarta Sans", sans-serif'; x.fillText(p.nm, 34, 430);
        x.fillStyle = "#6b6450"; x.font = '500 34px "Plus Jakarta Sans", sans-serif'; x.fillText(p.wt, 34, 478);
        x.fillStyle = C.ink; x.font = '800 64px "Bricolage Grotesque", sans-serif'; x.fillText(p.pr, 34, 590);
        x.lineWidth = 7; x.strokeStyle = C.green; rr(x, 290, 525, 190, 88, 24);
        if (added) { x.fillStyle = C.green; x.fill(); x.fillStyle = C.cream; } else { x.stroke(); x.fillStyle = C.green; }
        x.font = '800 38px "Plus Jakarta Sans", sans-serif'; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(added ? "ADDED" : "ADD", 385, 571);
      });
      g.add(face(0.76, 0.96, tx.tex, 0.032, 0.4));
      const prod = BK.PRODUCT[p.k](); prod.scale.setScalar(0.34); prod.position.set(0, 0.04, 0.16); g.add(prod);
      const pad = blob(0.5, 0.28, 0.25); pad.rotation.x = 0; pad.position.set(0, 0.06, 0.035); g.add(pad);
      g.position.set(i % 2 ? 0.405 : -0.405, i < 2 ? 0.08 : -0.97, 0);
      ui.add(g);
      return { g, prod, tx, base: g.position.clone() };
    });
    const at = [3.3, 3.55, 3.8, 4.1];
    camera.position.set(0, 0, 6.25); camera.lookAt(0, 0.05, 0);
    return function (t) {
      const u = E.outC(seg(t, 2.8, 5.15));
      ui.rotation.set(lerp(-0.26, -0.08, u), lerp(0.16, 0.04, u), 0);
      ui.position.set(0, 0, lerp(-0.3, 0, u));
      head.position.y = 1.2 + (1 - E.outBack(seg(t, 2.8, 3.15))) * 0.4;
      bar.scale.setScalar(Math.max(0.001, E.outBack(seg(t, 2.84, 3.2))));
      const n = Math.max(0, Math.min(QUERY.length, Math.floor((t - 3.15) / 0.046) + 1));
      const caret = t < 3.15 ? 1 : t < 4.35 ? 1 : (Math.floor((t - 4.35) / 0.2) % 2 ? 1 : 0);
      bt.set(n + "|" + caret);
      cards.forEach((c, i) => {
        const a = seg(t, at[i], at[i] + 0.42);
        c.g.scale.setScalar(Math.max(0.001, E.outBack(a, 1.4)));
        c.g.position.z = lerp(-0.5, 0, E.outC(a));
        c.prod.rotation.y = -0.5 + (t - at[i]) * 0.7;
        c.prod.position.z = 0.16 + 0.05 * E.outBack(seg(t, at[i] + 0.1, at[i] + 0.5));
        c.tx.set(t >= 4.45 + i * 0.1);
      });
      st.render();
    };
  };

  // ============ B4 · products drop into the bag (5.0–7.0) ============
  S.cart = function (cv) {
    const st = stage(cv, { bg: "#fbefcc", hemi: 0.6, key: 2.2, keyPos: [2.2, 5.5, 4.5], fov: 32, shadowSize: 3 });
    const { scene, camera } = st;
    const floor = mesh(new T.PlaneGeometry(20, 20), M.clay("#fbefcc", 0.95), false, true); floor.rotation.x = -Math.PI / 2; scene.add(floor);
    const b = BK.bag(1.05, 1.0, 0.7); scene.add(b);
    const items = ["milk", "chips", "ice", "cake"].map((k) => { const m = BK.PRODUCT[k](); m.scale.setScalar(0.5); scene.add(m); return m; });
    const rest = [[-0.3, 0.68, 0.05, -0.18], [-0.07, 0.72, -0.06, 0.12], [0.16, 0.66, 0.08, -0.08], [0.3, 0.72, -0.08, 0.16]];
    const btn = mesh(rbox(1.15, 0.22, 0.1, 0.11), M.gloss(C.green)); scene.add(btn);
    const btx = canvasTex(1024, 178, (x, done) => {
      x.fillStyle = C.cream; x.font = '800 80px "Plus Jakarta Sans", sans-serif'; x.textAlign = "center"; x.textBaseline = "middle";
      x.fillText(done ? "Order placed!" : "Place order", 512, 92);
    });
    btn.add(face(1.15, 0.22, btx.tex, 0.052, 0.4));
    btn.position.set(0, 0.25, 1.3); btn.rotation.x = -0.75;
    const th = BK.thumb(); th.scale.setScalar(0.62); scene.add(th);
    return function (t) {
      const o = E.inOutS(seg(t, 4.9, 7.15));
      camera.position.set(lerp(-0.45, 0.25, o), 3.3, 5.0); camera.lookAt(0, 0.62, 0.25);
      let squash = 0;
      items.forEach((m, i) => {
        const t0 = 5.2 + i * 0.25, a = seg(t, t0, t0 + 0.42), r = rest[i];
        m.position.set(r[0], lerp(3.4, r[1], E.outBounce(a)), r[2]);
        m.rotation.set(0.2 * (1 - a), r[3] + (1 - a) * 3.5 * (i % 2 ? 1 : -1), r[3] * 0.5);
        m.visible = t >= t0;
        squash = Math.max(squash, wob(t, t0 + 0.26, 12, 0.05, 30) * (t > t0 + 0.26 ? 1 : 0));
      });
      b.scale.set(1 + squash * 0.6, 1 - Math.abs(squash), 1 + squash * 0.6);
      b.position.y = 0; b.rotation.y = lerp(-0.15, 0.1, o);
      const bi = E.outBack(seg(t, 5.0, 5.4));
      b.scale.multiplyScalar(Math.max(0.001, bi));
      btn.position.y = 0.25 - (1 - E.outExpo(seg(t, 5.15, 5.6))) * 1.4;
      const press = seg(t, 6.5, 6.57) - seg(t, 6.58, 6.75);
      btn.scale.setScalar(1 - press * 0.05);
      btx.set(t >= 6.6);
      const inn = E.outC(seg(t, 6.2, 6.48)), out = E.inQ(seg(t, 6.89, 7.15));
      th.position.set(0.36, btn.position.y + 0.02 - (1 - inn) * 1.5 - out * 1.5, 1.4 - press * 0.05);
      th.rotation.set(-1.25, 0, 0.25);
      st.render();
    };
  };

  // ============ B5 · clay-3D city, scooter on the route (7.0–10.0) ============
  S.map = function (cv) {
    const st = stage(cv, { bg: "#f1e7cb", ground: "#e8dcb8", hemi: 0.62, key: 2.3, keyPos: [3, 7, 2.5], fov: 34, shadowSize: 4.5, shadowRadius: 6 });
    const { scene, camera, key } = st;
    key.shadow.mapSize.set(2048, 2048);
    const ground = mesh(new T.PlaneGeometry(30, 30), M.clay("#efe4c4", 0.95), false, true); ground.rotation.x = -Math.PI / 2; scene.add(ground);
    const XL = [-4.8, -3.6, -2.4, -1.2, 0.3, 1.2, 2.6, 3.8, 5.0], ZL = [5.2, 3.8, 2.4, 0.8, -0.6, -2.2, -3.6, -5.0, -6.4];
    const roadM = M.clay("#fbf8f0", 0.9);
    XL.forEach((x) => { const r = mesh(new T.PlaneGeometry(0.34, 30), roadM, false, true); r.rotation.x = -Math.PI / 2; r.position.set(x, 0.004, 0); scene.add(r); });
    ZL.forEach((z) => { const r = mesh(new T.PlaneGeometry(30, 0.34), roadM, false, true); r.rotation.x = -Math.PI / 2; r.position.set(0, 0.005, z); scene.add(r); });
    const R = rng(77), bM = [M.clay("#f8f4ea", 0.85), M.clay("#f3ecdc", 0.85), M.clay("#fbf3df", 0.85)], parkM = M.clay("#bfdcb3", 0.9);
    const treeM = M.clay("#7fbf6a", 0.7), trunkM = M.clay("#c9b28a", 0.8), winM = M.clay("#e2d6bb", 0.8);
    const tree = (x, z, s) => { const tr = mesh(new T.CylinderGeometry(0.02 * s, 0.025 * s, 0.12 * s, 8), trunkM); tr.position.set(x, 0.06 * s, z); scene.add(tr);
      const cr = mesh(new T.SphereGeometry(0.11 * s, 16, 12), treeM); cr.position.set(x, 0.18 * s, z); scene.add(cr); };
    for (let i = 0; i < XL.length - 1; i++) for (let j = 0; j < ZL.length - 1; j++) {
      const x0 = XL[i] + 0.3, x1 = XL[i + 1] - 0.3, z0 = ZL[j + 1] + 0.3, z1 = ZL[j] - 0.3;
      if ((i === 4 && j === 1) || (i === 1 && j === 4) || (i === 6 && j === 2)) {
        const p = mesh(new T.BoxGeometry(x1 - x0, 0.03, z1 - z0), parkM); p.position.set((x0 + x1) / 2, 0.015, (z0 + z1) / 2); scene.add(p);
        for (let k = 0; k < 7; k++) tree(lerp(x0 + 0.1, x1 - 0.1, R()), lerp(z0 + 0.1, z1 - 0.1, R()), 0.8 + R() * 0.6);
        continue;
      }
      const nx = x1 - x0 > 1.0 ? 2 : 1, nz = z1 - z0 > 1.0 ? 2 : 1;
      for (let a = 0; a < nx; a++) for (let c = 0; c < nz; c++) {
        const w = (x1 - x0) / nx - 0.08, d = (z1 - z0) / nz - 0.08, h = 0.18 + R() * 0.5;
        const bx = mesh(rbox(w, h, d, 0.03, 0.02), bM[Math.floor(R() * 3)]);
        bx.rotation.x = 0; bx.position.set(x0 + (a + 0.5) * (x1 - x0) / nx, h / 2, z0 + (c + 0.5) * (z1 - z0) / nz); scene.add(bx);
        const roofTop = mesh(new T.BoxGeometry(w * 0.4, 0.05, d * 0.3), winM); roofTop.position.set(bx.position.x + w * 0.15, h + 0.025, bx.position.z); scene.add(roofTop);
      }
      tree(x0 - 0.12, z0 + 0.2, 0.7); tree(x1 + 0.12, z1 - 0.25, 0.7);
    }
    const pts = [[-1.2, 2.4], [-1.2, 0.8], [0.3, 0.8], [0.3, -0.6], [1.2, -0.6], [1.2, -2.2]].map((p) => V(p[0], 0.03, p[1]));
    const path = new T.CurvePath();
    for (let i = 0; i < pts.length - 1; i++) path.add(new T.LineCurve3(pts[i], pts[i + 1]));
    const TUB = 600, RAD = 10;
    const tube = mesh(new T.TubeGeometry(path, TUB, 0.05, RAD, false), new T.MeshStandardMaterial({ color: C.green, roughness: 0.35, emissive: C.green, emissiveIntensity: 0.25 }), false, false);
    tube.scale.y = 0.4; scene.add(tube);
    const store = new T.Group(); scene.add(store); store.position.set(-1.2, 0, 2.4);
    store.add(mesh(new T.CylinderGeometry(0.2, 0.2, 0.08, 40), M.gloss(C.yellow)).translateY(0.04));
    const stx = canvasTex(256, 256, (x) => { x.fillStyle = C.ink; x.font = '800 190px "Bricolage Grotesque", sans-serif'; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText("b", 128, 120); });
    const sl = new T.Mesh(new T.CircleGeometry(0.16, 40), new T.MeshStandardMaterial({ map: stx.tex, transparent: true })); sl.rotation.x = -Math.PI / 2; sl.position.y = 0.083; store.add(sl);
    const home = BK.pin(); home.position.set(1.2, 0, -2.2); home.scale.setScalar(1.15); scene.add(home);
    const hb = blob(0.5, 0.5, 0.3); hb.position.set(1.2, 0.01, -2.2); scene.add(hb);
    const sc = BK.scooter(); sc.scale.setScalar(1.6); scene.add(sc);
    const p = new T.Vector3(), tg = new T.Vector3(), camP = new T.Vector3(), look = new T.Vector3();
    return function (t) {
      const g = E.outC(seg(t, 6.95, 7.45));
      tube.geometry.setDrawRange(0, Math.floor(g * TUB) * RAD * 6);
      store.scale.setScalar(Math.max(0.001, E.outBack(seg(t, 7.0, 7.3))));
      const hp = seg(t, 7.1, 7.5);
      home.position.y = (1 - E.outBounce(hp)) * 0.8 + 0.03 * Math.sin(t * 5);
      const u = E.inOutS(seg(t, 7.3, 9.7));
      path.getPointAt(u, p); path.getTangentAt(Math.min(0.999, u + 0.001), tg);
      sc.position.copy(p).setY(0.02);
      sc.rotation.y = Math.atan2(-tg.z, tg.x);
      sc.scale.setScalar(1.6 * Math.max(0.001, E.outBack(seg(t, 7.15, 7.4))));
      // camera: overview → chase → dive to the home pin
      const ov = V(-0.5, 6.0, 6.2), chase = V(p.x + 1.1, 2.7, p.z + 2.9), dive = V(1.35, 0.9, -1.35);
      const toChase = E.inOutS(seg(t, 7.0, 7.9)), toDive = E.inC(seg(t, 9.65, 10.15));
      camP.copy(ov).lerp(chase, toChase).lerp(dive, toDive);
      look.set(lerp(-0.6, p.x, toChase), 0, lerp(1.2, p.z - 0.7, toChase));
      look.lerp(V(1.2, 0.4, -2.2), toDive);
      camera.position.copy(camP); camera.lookAt(look);
      st.render();
    };
  };

  // ============ B6 · front door (10.0–11.5) ============
  S.door = function (cv) {
    const st = stage(cv, { bg: "#f6e8c4", hemi: 0.55, key: 1.9, keyPos: [-2.5, 4, 5], fov: 34, shadowSize: 3 });
    const { scene, camera } = st;
    const wallM = M.clay("#f6e8c4", 0.9), trimM = M.plastic(C.ink, 0.5, 0.2);
    const wall = (w, h, x, y) => { const m = mesh(new T.BoxGeometry(w, h, 0.2), wallM); m.position.set(x, y, 0); scene.add(m); };
    wall(3, 6, -0.62 - 1.5, 0.5); wall(3, 6, 0.62 + 1.5, 0.5); wall(1.24, 3, 0, 1.0 + 1.5);
    const floor = mesh(new T.PlaneGeometry(10, 10), M.clay("#e8d6a6", 0.9), false, true); floor.rotation.x = -Math.PI / 2; floor.position.y = -1.3; scene.add(floor);
    const trim = (w, h, x, y) => { const m = mesh(new T.BoxGeometry(w, h, 0.26), trimM); m.position.set(x, y, 0.02); scene.add(m); };
    trim(0.09, 2.38, -0.665, -0.11); trim(0.09, 2.38, 0.665, -0.11); trim(1.42, 0.09, 0, 1.04);
    const outside = mesh(new T.PlaneGeometry(6, 6), new T.MeshStandardMaterial({ color: "#2b2a22", roughness: 1 }), false, true); outside.position.set(0, 0, -2.2); scene.add(outside);
    const porch = new T.PointLight("#ffd9a0", 4, 4, 1.6); porch.position.set(0.5, 0.9, -1.0); scene.add(porch);
    const hinge = new T.Group(); hinge.position.set(-0.6, -0.16, 0.0); scene.add(hinge);
    const doorM = M.plastic(C.green, 0.45, 0.4), panelM = M.plastic(C.greenDeep, 0.5, 0.3);
    const dm = mesh(rbox(1.2, 2.28, 0.08, 0.03), doorM); dm.position.set(0.6, 0, 0); hinge.add(dm);
    [0.52, -0.52].forEach((y) => { const p = mesh(rbox(0.86, 0.86, 0.04, 0.04), panelM); p.position.set(0.6, y, 0.045); hinge.add(p); });
    const knob = mesh(new T.SphereGeometry(0.055, 24, 16), M.gloss(C.yellow)); knob.position.set(1.06, -0.05, 0.1); hinge.add(knob);
    // rider's sleeve + the yellow bag, outside the doorway
    const rider = new T.Group(); scene.add(rider);
    const rb = BK.bag(0.55, 0.52, 0.36); rb.position.set(0, -0.62, 0); rider.add(rb);
    const arm = mesh(new T.CapsuleGeometry(0.075, 0.7, 8, 16), M.clay(C.yellow, 0.7)); arm.rotation.z = Math.PI / 2 - 0.25; arm.position.set(0.55, 0.0, 0); rider.add(arm);
    const hand = mesh(new T.SphereGeometry(0.075, 20, 14), M.clay(C.skin, 0.55)); hand.position.set(0.16, -0.08, 0); rider.add(hand);
    const bell = mesh(rbox(0.15, 0.22, 0.05, 0.04), M.plastic(C.white, 0.35)); bell.position.set(0.82, -0.05, 0.13); scene.add(bell);
    const btn = mesh(new T.CylinderGeometry(0.035, 0.035, 0.03, 24), M.gloss(C.yellow)); btn.rotation.x = Math.PI / 2; btn.position.set(0.82, -0.03, 0.165); scene.add(btn);
    const rings = [0, 1].map(() => { const r = new T.Mesh(new T.TorusGeometry(0.1, 0.012, 10, 48), new T.MeshBasicMaterial({ color: C.green, transparent: true })); r.position.set(0.82, -0.03, 0.17); scene.add(r); return r; });
    return function (t) {
      const u = E.outC(seg(t, 9.8, 11.65));
      camera.position.set(lerp(0.12, 0.05, u), lerp(0.55, 0.45, u), lerp(6.3, 5.7, u)); camera.lookAt(0.05, 0.3, 0);
      hinge.rotation.y = lerp(0, -1.25, E.inOutC(seg(t, 10.12, 10.65)));
      rings.forEach((r, i) => { const a = seg(t, 10.0 + i * 0.45, 10.45 + i * 0.45); r.scale.setScalar(1 + a * 2.2); r.material.opacity = a > 0 && a < 1 ? 0.9 * (1 - a) : 0; });
      btn.position.z = 0.165 - 0.012 * (seg(t, 9.95, 10.0) - seg(t, 10.05, 10.15));
      const hand_in = E.outBack(seg(t, 10.4, 10.9), 1.2);
      rider.position.set(lerp(1.6, 0.18, hand_in), -0.1 + 0.02 * Math.sin(t * 6), -0.55);
      rider.rotation.z = lerp(0.12, 0, hand_in);
      st.render();
    };
  };

  // ============ B7 · blurred floating groceries behind the word stack (11.5–13.0) ============
  S.float = function (cv) {
    const st = stage(cv, { bg: C.green, ground: "#0a5e17", hemi: 0.7, key: 2.0, keyPos: [2, 5, 5], fov: 32 });
    const { scene, camera } = st;
    const R = rng(5), objs = [];
    ["milk", "chips", "ice", "cake", "milk", "chips"].forEach((k, i) => {
      const m = BK.PRODUCT[k](); m.scale.setScalar(0.55 + R() * 0.25);
      const a = (i / 6) * Math.PI * 2 + 0.4, rad = 1.0 + R() * 0.35;
      m.userData = { x: Math.cos(a) * rad * 0.7, y: Math.sin(a) * rad * 1.35, z: -0.6 - R() * 1.2, s: R() * 6 };
      scene.add(m); objs.push(m);
    });
    camera.position.set(0, 0, 5); camera.lookAt(0, 0, 0);
    return function (t) {
      objs.forEach((m, i) => { const d = m.userData; m.position.set(d.x, d.y + 0.08 * Math.sin(t * 1.6 + d.s), d.z); m.rotation.set(0.3 * Math.sin(t + d.s), t * 0.8 + d.s, 0.2 * Math.cos(t * 0.9 + d.s)); });
      st.render();
    };
  };

  // ============ B8 · groceries burst out behind the slogan (13.0–14.5) ============
  S.burst = function (cv) {
    const st = stage(cv, { bg: C.yellow, ground: "#d9a827", hemi: 0.7, key: 2.1, keyPos: [2, 5, 5], fov: 32 });
    const { scene, camera } = st;
    const R = rng(21), objs = [];
    const kinds = ["milk", "chips", "ice", "cake", "star", "star", "star", "milk"];
    kinds.forEach((k, i) => {
      const m = k === "star" ? BK.star(0.22, 0.1, [C.cream, C.green, C.ink][i % 3]) : BK.PRODUCT[k]();
      if (k !== "star") m.scale.setScalar(0.42);
      const a = (i / kinds.length) * Math.PI * 2 + 0.3;
      m.userData = { tx: Math.cos(a) * (0.95 + R() * 0.1), ty: Math.sin(a) * (1.5 + R() * 0.15), tz: -0.4 - R() * 0.6, sp: (R() - 0.5) * 4, d: R() * 0.08 };
      scene.add(m); objs.push(m);
    });
    camera.position.set(0, 0, 5); camera.lookAt(0, 0, 0);
    return function (t) {
      objs.forEach((m) => {
        const d = m.userData, a = E.outExpo(seg(t, 13.0 + d.d, 13.45 + d.d));
        m.position.set(d.tx * a, d.ty * a + 0.04 * Math.sin(t * 2 + d.sp), lerp(-2, d.tz, a));
        m.rotation.set(0.3 + d.sp * 0.1, d.sp * (t - 13) + (1 - a) * 4, 0.2);
        const s = m.userData.s0 || (m.userData.s0 = m.scale.x);
        m.scale.setScalar(Math.max(0.001, s * a));
      });
      st.render();
    };
  };

  // ============ B9 · the glossy 3D app icon lands (14.5–17.0) ============
  S.logo = function (cv) {
    const st = stage(cv, { bg: C.cream, hemi: 0.6, key: 2.2, keyPos: [-2, 4, 5], fov: 30, shadowSize: 2 });
    const { scene, camera } = st;
    const back = mesh(new T.PlaneGeometry(14, 14), M.clay(C.cream, 0.95), false, true); back.position.z = -0.45; scene.add(back);
    const icon = BK.appIcon(1.0, 0.24); scene.add(icon);
    camera.position.set(0, 0, 5.4); camera.lookAt(0, 0.05, 0);
    return function (t) {
      const a = seg(t, 14.45, 15.0);
      icon.rotation.set(lerp(0.5, 0, E.outC(a)), lerp(-2.6, 0, E.outBack(a, 1.2)), 0);
      icon.position.set(0, lerp(-0.6, 0.38, E.outBack(a, 1.3)), lerp(-1.5, 0, E.outC(a)));
      icon.scale.setScalar(Math.max(0.001, lerp(0.2, 0.9, E.outBack(a, 1.5))));
      st.render();
    };
  };

  window.SCENES = S;
})();
