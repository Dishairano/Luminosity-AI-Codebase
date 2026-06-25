// Luminosity Setup — werkt zowel als website-mockup (gesimuleerd) als als de
// echte installer in de ISO (praat dan met de lokale install-server via /api).

(() => {
  // --- Lumo, de mascotte (inline SVG zodat we 'm kunnen animeren) ---
  function lumo(face = "smile") {
    const mouth = {
      smile: "M34 60 q14 14 28 0",
      work:  "M40 62 q8 6 16 0",
      happy: "M30 58 q18 20 36 0",
    }[face] || "M34 60 q14 14 28 0";
    return `<svg viewBox="0 0 96 96" width="100%" height="100%" aria-hidden="true">
      <g class="lumo-rays" stroke="var(--accent)" stroke-width="3" stroke-linecap="round">
        ${Array.from({length: 12}, (_, i) => {
          const a = (i * 30) * Math.PI / 180, x = 48 + Math.cos(a), y = 48 + Math.sin(a);
          const x1 = 48 + Math.cos(a) * 40, y1 = 48 + Math.sin(a) * 40;
          const x2 = 48 + Math.cos(a) * 46, y2 = 48 + Math.sin(a) * 46;
          return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"/>`;
        }).join("")}
      </g>
      <circle class="lumo-glow" cx="48" cy="48" r="34" fill="var(--accent)" opacity=".25"/>
      <circle cx="48" cy="48" r="28" fill="var(--accent)"/>
      <g fill="var(--accent-ink)">
        <circle cx="38" cy="44" r="3.4"/><circle cx="58" cy="44" r="3.4"/>
        <path d="${mouth}" fill="none" stroke="var(--accent-ink)" stroke-width="3.2" stroke-linecap="round"/>
      </g>
    </svg>`;
  }
  const put = (id, face) => { const el = document.getElementById(id); if (el) el.innerHTML = lumo(face); };
  ["brand-mascot", "mascot-hero"].forEach(id => put(id, "smile"));
  put("install-mascot", "work");
  put("done-mascot", "happy");

  // --- State ---
  const TOTAL = 10;
  let step = 0;
  let real = false;            // praten we met een echte install-server?
  let disks = [];
  const cfg = {
    lang: "nl", layout: "whole", disk: null,
    accent: "#ffd166", accentName: "Zon", dark: true, updates: true,
  };

  const $ = (s) => document.querySelector(s);
  const $$ = (s) => [...document.querySelectorAll(s)];
  const stepsEls = $$(".step");
  const railEls = $$("#steps li");
  const dots = $("#dots");
  const back = $("#back"), next = $("#next");

  for (let i = 0; i < TOTAL; i++) dots.appendChild(document.createElement("i"));
  const dotEls = [...dots.children];

  // --- Detecteer echte server ---
  async function detectMode() {
    try {
      const r = await fetch("api/disks", { cache: "no-store" });
      if (!r.ok) throw 0;
      const data = await r.json();
      disks = data.disks || [];
      real = true;
      $("#mode-badge").textContent = "live";
    } catch {
      real = false;
      disks = [
        { name: "sda", size: "256 GB", model: "Samsung SSD", note: "leeg" },
        { name: "nvme0n1", size: "1 TB", model: "WD NVMe", note: "bevat data" },
      ];
    }
    renderDisks();
  }

  function renderDisks() {
    const box = $("#disk-choices");
    box.innerHTML = "";
    if (!disks.length) {
      box.innerHTML = '<p class="warn">Geen schijven gevonden. Sluit een (virtuele) schijf aan en herstart de installer.</p>';
      cfg.disk = null;
      render();
      return;
    }
    disks.forEach((d, i) => {
      const el = document.createElement("div");
      el.className = "choice" + (i === 0 ? " sel" : "");
      el.dataset.pick = "disk";
      el.dataset.value = d.name;
      el.innerHTML = `<div class="ic">💽</div>
        <div><div class="t">/dev/${d.name} — ${d.size}</div>
        <div class="d">${d.model || "schijf"}${d.note ? " · " + d.note : ""}</div></div>
        <div class="chk">✓</div>`;
      box.appendChild(el);
    });
    if (disks[0]) { cfg.disk = disks[0].name; updateViz(); }
    bindChoiceGroup(box);
    render();   // knop-status bijwerken nu de schijvenlijst er is
  }

  function bindChoiceGroup(scope) {
    scope.querySelectorAll('[data-pick]').forEach(c => {
      c.onclick = () => {
        const group = c.dataset.pick;
        document.querySelectorAll(`[data-pick="${group}"]`).forEach(x => x.classList.remove("sel"));
        c.classList.add("sel");
        if (group === "lang") cfg.lang = c.dataset.value;
        if (group === "disk") { cfg.disk = c.dataset.value; updateViz(); }
        if (group === "layout") cfg.layout = c.dataset.value;
        refreshSummary();
      };
    });
  }
  bindChoiceGroup(document); // statische keuzes (lang, layout)

  function updateViz() {
    const d = disks.find(x => x.name === cfg.disk);
    $("#viz-root").textContent = d ? d.size : "—";
  }

  // --- Toggles ---
  const switches = { accept: false, updates: true, darkmode: true };
  $$(".switch").forEach(s => {
    s.onclick = () => {
      s.classList.toggle("on");
      const on = s.classList.contains("on");
      if (s.id === "accept") { switches.accept = on; render(); }
      if (s.id === "updates") { cfg.updates = on; }
      if (s.id === "darkmode") { cfg.dark = on; document.body.classList.toggle("light", !on); }
    };
  });

  // --- Accent-swatches (live thema) ---
  $$(".swatch").forEach(sw => {
    sw.onclick = () => {
      $$(".swatch").forEach(x => x.classList.remove("sel"));
      sw.classList.add("sel");
      cfg.accent = sw.dataset.accent;
      cfg.accentName = sw.title.split(" ")[0];
      document.documentElement.style.setProperty("--accent", cfg.accent);
      // donkere tekst op lichte accenten
      document.documentElement.style.setProperty("--accent-ink", "#241a06");
      refreshSummary();
    };
  });

  // --- Validatie ---
  function pwOk() {
    const a = $("#pw").value, b = $("#pw2").value;
    const match = a.length > 0 && a === b;
    $("#pw-warn").style.display = (b.length > 0 && !match) ? "block" : "none";
    return match;
  }
  // render() erbij: de Volgende-knop moet direct aan/uit gaan tijdens het typen.
  ["pw", "pw2"].forEach(id => $("#" + id).addEventListener("input", () => { pwOk(); render(); }));

  function canAdvance() {
    if (step === 1) return switches.accept;
    if (step === 2) return !!cfg.disk;   // zonder gekozen schijf niet verder
    if (step === 4) return $("#username").value.trim() && pwOk();
    return true;
  }

  function refreshSummary() {
    const langTxt = cfg.lang === "nl" ? "Nederlands" : "English";
    $("#s-lang").textContent = langTxt;
    $("#s-disk").textContent = cfg.disk ? "/dev/" + cfg.disk : "—";
    $("#s-layout").textContent = cfg.layout === "whole" ? "hele schijf" : "handmatig";
    $("#s-user").textContent = $("#username").value || "gebruiker";
    $("#s-host").textContent = $("#hostname").value || "luminosity-pc";
    $("#s-tz").textContent = $("#tz").value;
    $("#s-kb").textContent = $("#kb").selectedOptions[0].textContent;
    $("#s-accent").textContent = cfg.accentName;
  }

  function render() {
    stepsEls.forEach(s => s.classList.toggle("show", +s.dataset.step === step));
    railEls.forEach(li => { const n = +li.dataset.step; li.classList.toggle("active", n === step); li.classList.toggle("done", n < step); });
    dotEls.forEach((d, i) => d.classList.toggle("on", i === step));
    back.style.visibility = step === 0 ? "hidden" : "visible";
    next.disabled = !canAdvance();
    const hideNav = step >= 8;
    next.style.display = hideNav ? "none" : "";
    back.style.display = hideNav ? "none" : "";
    if (!hideNav) next.textContent = step === 7 ? "Installeren" : "Volgende";
    if (step === 7) refreshSummary();
  }

  back.onclick = () => { if (step > 0) { step--; render(); } };
  next.onclick = () => {
    if (!canAdvance()) return;
    if (step === 7) { step = 8; render(); startInstall(); return; }
    step++; render();
  };
  ["username", "hostname"].forEach(id => $("#" + id).addEventListener("input", () => { render(); }));

  // --- Installatie ---
  function buildConfig() {
    return {
      disk: cfg.disk, layout: cfg.layout, lang: cfg.lang,
      hostname: $("#hostname").value || "luminosity-pc",
      username: $("#username").value || "gebruiker",
      fullname: $("#fullname").value || "",
      password: $("#pw").value,
      timezone: $("#tz").value,
      keyboard: $("#kb").value,
      accent: cfg.accent, dark: cfg.dark, updates: cfg.updates,
    };
  }
  function logLine(msg) {
    const log = $("#log");
    const d = document.createElement("div");
    d.textContent = "» " + msg;
    log.appendChild(d); log.scrollTop = log.scrollHeight;
  }
  function setPct(p) {
    $("#ring").style.setProperty("--p", p);
    $("#ringpct").textContent = Math.round(p) + "%";
  }

  async function startInstall() {
    if (real) return realInstall();
    return simulateInstall();
  }

  async function realInstall() {
    try {
      const res = await fetch("api/install", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildConfig()),
      });
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let nl;
        while ((nl = buf.indexOf("\n")) >= 0) {
          const line = buf.slice(0, nl).trim(); buf = buf.slice(nl + 1);
          if (!line.startsWith("data:")) continue;
          let ev; try { ev = JSON.parse(line.slice(5).trim()); } catch { continue; }
          if (ev.type === "log") logLine(ev.msg);
          else if (ev.type === "progress") setPct(ev.pct);
          else if (ev.type === "done") { setPct(100); finish(); }
          else if (ev.type === "error") { logLine("FOUT: " + ev.msg); }
        }
      }
    } catch (e) {
      logLine("Kon de installatie niet starten: " + e);
    }
  }

  function simulateInstall() {
    const msgs = [
      "Schijf /dev/" + cfg.disk + " voorbereiden…",
      "Partities maken (EFI + root)…",
      "Bestandssystemen formatteren…",
      "Basissysteem (Arch Linux) kopiëren…",
      "Kernel en drivers installeren…",
      "Hyprland (grafische laag) instellen…",
      "Quickshell-schil installeren…",
      "Offline taal-engine plaatsen…",
      "Je account aanmaken…",
      "Opstartlader schrijven…",
      "Laatste instellingen toepassen…",
    ];
    let i = 0, p = 0;
    const tick = () => {
      if (i < msgs.length) { logLine(msgs[i]); i++; }
      const target = Math.round((i / msgs.length) * 100);
      const grow = setInterval(() => { if (p >= target) { clearInterval(grow); return; } p++; setPct(p); }, 16);
      if (i < msgs.length) setTimeout(tick, 620);
      else setTimeout(finish, 1300);
    };
    tick();
  }

  function finish() { step = 9; render(); }

  $("#btn-restart").onclick = async () => {
    if (real) { try { await fetch("api/reboot", { method: "POST" }); } catch {} }
    document.querySelector(".setup").style.transition = "opacity .6s";
    document.querySelector(".setup").style.opacity = "0";
  };

  // --- Init ---
  detectMode();
  render();
})();
