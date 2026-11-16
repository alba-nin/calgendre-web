/* =====================================================================
   Cal Gendre · carregador de continguts
   ---------------------------------------------------------------------
   Els TEXTOS de la web no s'editen aquí: són a la carpeta contingut/
     contingut/general.json  -> telèfon, correu, adreça, horaris...
     contingut/inici.json    -> textos de la pàgina d'inici i la carta
     contingut/agenda.json   -> activitats de l'agenda
   S'editen des de GitHub (llapis ✎ → Commit changes). Instruccions a COM-EDITAR.md.

   Format dels textos:  **negreta**   __subratllat__
   ===================================================================== */
(function () {
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const fmt = s => esc(s)
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/__(.+?)__/g, "<u>$1</u>")
    .replace(/\n/g, "<br>");
  const valor = (obj, cami) => cami.split(".").reduce((o, k) => (o == null ? o : o[k]), obj);

  const llegeix = n => fetch(`contingut/${n}.json`, { cache: "no-store" })
    .then(r => (r.ok ? r.json() : null)).catch(() => null);

  function aplica(CG) {
    const g = CG.general || {};
    /* textos simples: <p data-c="inici.llibreria.text"> */
    document.querySelectorAll("[data-c]").forEach(el => {
      const v = valor(CG, el.dataset.c);
      if (typeof v === "string" && v.trim()) el.innerHTML = fmt(v);
      else if (typeof v === "string") el.style.display = "none";
    });
    /* llistes de text: <ol data-llista="inici.paquet.contingut"> */
    document.querySelectorAll("[data-llista]").forEach(el => {
      const v = valor(CG, el.dataset.llista);
      if (Array.isArray(v)) el.innerHTML = v.filter(Boolean).map(x => `<li>${fmt(x)}</li>`).join("");
    });
    /* horaris */
    document.querySelectorAll("[data-horaris]").forEach(el => {
      if (Array.isArray(g.horaris)) el.innerHTML = g.horaris.map(h => `<tr><td>${esc(h.dies)}</td><td>${esc(h.hores)}</td></tr>`).join("");
    });
    /* contacte */
    if (g.whatsapp) document.querySelectorAll("[data-wa]").forEach(a => {
      const t = a.dataset.wa; a.href = `https://wa.me/${g.whatsapp}` + (t ? `?text=${encodeURIComponent(t)}` : "");
    });
    if (g.telefon) document.querySelectorAll("[data-tel]").forEach(a => { a.href = "tel:+34" + g.telefon.replace(/\D/g, ""); a.textContent = g.telefon; });
    if (g.email) document.querySelectorAll("[data-mail]").forEach(a => { a.href = "mailto:" + g.email; a.textContent = g.email; });
    document.querySelectorAll("[data-adreca]").forEach(el => {
      if (g.adreca) el.innerHTML = el.dataset.adreca === "linies"
        ? `Cal Gendre 1879<br>${esc(g.adreca)}<br>${esc(g.poblacio || "")}`
        : `${esc(g.adreca)} · ${esc(g.poblacio || "")}`;
    });
    /* carta: graella de seccions i productes */
    const carta = CG.inici && CG.inici.carta;
    document.querySelectorAll("[data-carta]").forEach(el => {
      if (!carta || !Array.isArray(carta.seccions)) return;
      el.innerHTML = carta.seccions.map(s => `<div><h3>${esc(s.titol)}</h3><ul>${
        (s.productes || []).map(p => `<li><span>${esc(p.nom)}</span><span>${p.preu ? esc(String(p.preu).replace(/\s*€?$/, " €")) : "— €"}</span></li>`).join("")
      }</ul></div>`).join("");
      const sec = el.closest("section");
      if (sec) sec.classList.toggle("aviat", carta.proximament !== false);
    });
    /* catàleg en mode "pròximament" */
    if (document.body.dataset.pagina === "cataleg" && typeof g.cataleg_proximament === "boolean")
      document.body.classList.toggle("aviat", g.cataleg_proximament);
  }

  window.esc = esc;
  window.fmt = fmt;
  window.CONTINGUT = Promise.all(["general", "inici", "agenda"].map(llegeix)).then(([general, inici, agenda]) => {
    const CG = { general: general || {}, inici: inici || {}, agenda: Array.isArray(agenda) ? agenda : [] };
    /* dates: accepta "2026-11-28" o "2026-11-28T00:00..." */
    CG.agenda.forEach(a => { a.data = String(a.data || "").slice(0, 10); });
    window.CG = CG;
    const fet = () => aplica(CG);
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fet); else fet();
    return CG;
  });
})();
