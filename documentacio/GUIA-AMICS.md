# Amics de Cal Gendre · Guia de posada en marxa

**Model:** quotes de **5, 10 o 20 €/mes** (pagament mensual, trimestral o anual) per **domiciliació bancària**.
De cada quota, el **80 % és saldo** per gastar en **llibres** i el **20 % és suport** a la llibreria.
**5 % de descompte en llibres.** El saldo **no caduca**, ni amb la baixa.

| Quota | Saldo | Suport | Saldo l'any |
|---|---|---|---|
| 5 €/mes | 4 € | 1 € | 48 € |
| 10 €/mes | 8 € | 2 € | 96 € |
| 20 €/mes | 16 € | 4 € | 192 € |

Com funciona:

```
QR del flyer / web  →  socis.html (formulari)  →  Formulari de Google  →  Full de càlcul "Amics"
                                                                              │
                         cada mes: remesa de rebuts SEPA al banc  ◄───────────┤
                         cada mes: sumar el 80 % al saldo a Galatea ◄─────────┘
```

---

## 1. Crear el Formulari de Google (15 minuts, abans del 28/11)

La pàgina `socis.html` té el seu propi formulari bonic; per darrere envia les respostes a un
Formulari de Google, que les desa en un full de càlcul. La gent **no veu mai** el Formulari de Google.

1. Amb el compte de Google de la llibreria, ves a **forms.google.com → Formulari en blanc**.
   Títol: *Altes Amics de Cal Gendre*.
2. Crea **12 preguntes de tipus "Resposta curta"**, en aquest ordre, **sense marcar-ne cap com a obligatòria**
   (la web ja comprova que estiguin omplertes):
   `Quota` · `Periodicitat` · `Nom i cognoms` · `DNI` · `Telèfon` · `Correu` · `Adreça` ·
   `Codi postal` · `Població` · `IBAN` · `Titular del compte` · `Autoritza domiciliació`
3. **Configuració**: desmarca *Recopila adreces electròniques* i *Limita a 1 resposta*
   (no ha de demanar iniciar sessió a Google).
4. **Respostes → Enllaça amb Fulls de càlcul → Crea un full nou**. Activa també
   *⋮ → Rep notificacions per correu de les noves respostes*: us arribarà un correu a cada alta.
5. **Obtenir els identificadors de cada pregunta:**
   - Botó **⋮ → Obtén l'enllaç emplenat prèviament**.
   - Escriu qualsevol cosa a cada pregunta (p. ex. `a`, `b`, `c`…) i prem **Obtén l'enllaç → Copia l'enllaç**.
   - L'enllaç té aquesta forma:
     `https://docs.google.com/forms/d/e/1FAIpQL.../viewform?usp=pp_url&entry.1111=a&entry.2222=b&...`
   - Cada `entry.NNNN` és una pregunta, en el mateix ordre.
6. Obre `socis.html` i, a dalt del `<script>`, omple:

```js
const FORMULARI_GOOGLE = "https://docs.google.com/forms/d/e/1FAIpQL.../formResponse"; // ⚠ formResponse, no viewform
const CAMPS = {
  quota:"entry.1111", periode:"entry.2222", nom:"entry.3333", dni:"entry.4444",
  tel:"entry.5555", mail:"entry.6666", adreca:"entry.7777", cp:"entry.8888",
  poblacio:"entry.9999", iban:"entry.1010", titular:"entry.1212",
  mandat:"entry.1313"
};
```

7. **Prova-ho**: fes una alta de prova des del mòbil (pots fer servir l'IBAN d'exemple
   `ES91 2100 0418 4502 0005 1332`) i comprova que apareix al full de càlcul. Després esborra la fila.

> Mentre `FORMULARI_GOOGLE` estigui buit, el botó obre un correu adreçat a llibreria@calgendre.cat amb totes les dades.
> Funciona, però és molt millor tenir el formulari de Google configurat abans de la inauguració.

**Seguretat de les dades:** el full conté IBANs i DNIs. Que només hi tingui accés la llibreria
(no el comparteixis amb enllaç públic) i que el compte de Google tingui la verificació en dos passos activada.

---

## 2. Domiciliacions al banc (remeses SEPA)

1. Parla amb el **banc de la llibreria** per activar el servei de **remeses de rebuts SEPA (adeudos directos SEPA, CORE)**.
   Et donaran un **identificador de creditor** (comença per `ES` + DNI). Pregunta:
   - quina **comissió** cobren per rebut emès i per rebut retornat;
   - si accepten el **mandat signat electrònicament** (la casella "Autoritzo la domiciliació" del formulari,
     amb data i hora al full de càlcul). Si el banc demana signatura, imprimiu el mandat i feu-lo signar
     a la llibreria el primer cop que vingui cada amic/ga.
2. **Cada mes** (p. ex. el dia 1):
   - Al full de càlcul, mira qui toca cobrar aquest mes (mensuals: tots; trimestrals: gener, abril, juliol i octubre;
     anuals: el mes de l'alta).
   - Puja la remesa a la banca en línia (la majoria de bancs deixen importar un Excel o entrar els rebuts a mà).
     **Galatea** potser també pot generar remeses de rebuts: pregunta-ho a Defontsoft.
3. Si un rebut **es retorna**, avisa la persona. Les despeses de la devolució es descompten del saldo (és a les condicions).

## 3. Saldo i descompte a la botiga (Galatea)

Pregunta a Defontsoft:
1. Com posar a la **fitxa de client** un **5 % de descompte només en llibres**.
2. Com portar un **saldo a compte** per client (val, moneder o similar) que es pugui fer servir com a forma de pagament.

**Cada mes**, després que el banc hagi cobrat: suma el **80 %** de cada quota cobrada al saldo del client
(4 € / 8 € / 16 € per mes; ×3 si és trimestral, ×12 si és anual).

## 4. Baixes i canvis

- Les baixes arriben per correu, WhatsApp o a la llibreria. Si arriben **abans del dia 25**, ja no s'emet el rebut següent.
- Marca la baixa al full de càlcul (afegeix una columna `Estat`: *Actiu / Baixa*). **El saldo es conserva.**

---

## ⚠ Coses a confirmar amb la gestoria

- **IVA i tributació del 20 % de suport**: com que la llibreria no és una associació ni una cooperativa,
  aquesta part és un ingrés del negoci. Cal saber com es factura (i amb quin IVA).
- **IVA del 80 % de saldo**: normalment tributa quan es gasta en llibres (4 %), com una targeta regal.
- Si el saldo es pot **retornar en diners** en algun cas (ara les condicions no en diuen res).
