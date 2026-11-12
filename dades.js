/* ============================================================
   DADES DE CAL GENDRE (les fan servir index.html i agenda.html)
   ============================================================ */

/* ===== AGENDA: edita aquesta llista per afegir o treure activitats =====
   data: "AAAA-MM-DD". Les activitats passades s'amaguen soles.
   inscripcio (opcional):
     - un enllaç (Google Forms, Tally, Entradium...) -> botó "Inscriu-t'hi"
     - "whatsapp" -> obre WhatsApp amb un missatge ja escrit
     - sense camp -> entrada lliure, sense botó
   places (opcional): text curt, p. ex. "Places limitades" o "12 places · 15 €"
   destacat: true -> es pinta en lila (inauguració, actes especials) */
const WHATSAPP = "34930968669";   // <- número de la llibreria, sense + ni espais

const AGENDA = [
  { data:"2026-11-28", hora:"11–21 h", tipus:"Inauguració", destacat:true,
    titol:"Festa d'inauguració de Cal Gendre",
    text:"Llibreria oberta i brindis, recital d'Anna Gual i Jaume C. Pons Alorda, lectura en veu alta d'EVA354 i concert acústic d'Amulet.",
    places:"Entrada lliure" }
  /* Exemples per copiar quan hi hagi activitats:
  { data:"2026-12-12", hora:"11 h", tipus:"Taller", titol:"Nom del taller",
    text:"Descripció curta.", inscripcio:"whatsapp", places:"12 places" },
  { data:"2026-12-18", hora:"19:30 h", tipus:"Club de lectura", titol:"Club de lectura",
    text:"Descripció curta.", inscripcio:"https://forms.gle/...", places:"Places limitades" },
  */
];
