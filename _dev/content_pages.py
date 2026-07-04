# -*- coding: utf-8 -*-
"""Main content blocks for every Tinkoder subpage, both languages."""

# ---------------------------------------------------------------- SERVICES FI
SERVICES_FI = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Palvelut</p>
        <h1>Mitä kaikkea teemme</h1>
        <p class="lead">Kuusi palvelualuetta, yksi periaate: ratkaisemme ongelmasi, emme myy sinulle tavaraa. Jokainen projekti alkaa maksuttomalla tarjouksella.</p>
      </div>
    </section>

    <section class="section" style="padding-top:1rem">
      <div class="container">

        <article class="service-detail" id="3d-tulostus">
          <div>
            <p class="eyebrow">01 · Valmistus</p>
            <h3>3D-tulostus, CAD-mallinnus ja varaosat</h3>
            <p>Mallinnamme ja tulostamme toiminnalliset osat mittojen, valokuvan tai rikkinäisen kappaleen perusteella. Käänteissuunnittelussa mittaamme alkuperäisen osan, korjaamme sen suunnitteluvirheet ja valitsemme materiaalin käyttökohteen mukaan — kuumaan, kylmään, ulos tai jatkuvaan rasitukseen.</p>
          </div>
          <div>
            <h4>Kenelle</h4>
            <ul>
              <li>Kotitaloudet, joiden kodinkoneesta hajosi osa, jota ei enää myydä</li>
              <li>Yritykset, jotka tarvitsevat jigin, kiinnikkeen tai piensarjan</li>
              <li>Harrastajat, joilla on malli valmiina mutta ei tulostinta</li>
            </ul>
            <h4>Esimerkkejä</h4>
            <ul>
              <li>Astianpesukoneen sarana, jota valmistaja ei enää toimita</li>
              <li>Mittatilauskotelo elektroniikkaprojektille</li>
              <li>50 kappaleen piensarja tuotetestausta varten</li>
            </ul>
            <div class="specs"><span class="spec">PLA · PETG · ASA · TPU</span><span class="spec">OpenSCAD · Fusion 360</span><span class="spec">Toimitus 3–7 pv</span></div>
          </div>
        </article>

        <article class="service-detail" id="elektroniikka">
          <div>
            <p class="eyebrow">02 · Elektroniikka</p>
            <h3>Elektroniikkaprototyypit ja sulautetut järjestelmät</h3>
            <p>Rakennamme toimivat prototyypit ESP32-, Arduino- ja Raspberry Pi -alustoille: anturit, ohjaukset, näytöt ja langattomat yhteydet. Toimitamme laitteen ohjelmakoodeineen ja kytkentäkaavioineen, jotta ratkaisu ei jää mustaksi laatikoksi.</p>
          </div>
          <div>
            <h4>Kenelle</h4>
            <ul>
              <li>Startupit, jotka haluavat testata laiteidean ennen isoja investointeja</li>
              <li>Teollisuus, joka tarvitsee mittausdataa nopeasti ja edullisesti</li>
              <li>Keksijät, joiden idea vaatii toimivan demon</li>
            </ul>
            <h4>Esimerkkejä</h4>
            <ul>
              <li>Lämpötila- ja kosteusseuranta tuotantotilaan</li>
              <li>Etäluettava anturi, joka raportoi suoraan Teamsiin tai sähköpostiin</li>
              <li>Servo-ohjattu mekaniikka omaan tuoteideaan</li>
            </ul>
            <div class="specs"><span class="spec">ESP32 · ESP8266</span><span class="spec">Arduino · Raspberry Pi</span><span class="spec">MQTT · Wi-Fi · Zigbee</span></div>
          </div>
        </article>

        <article class="service-detail" id="alykoti">
          <div>
            <p class="eyebrow">03 · Älykoti</p>
            <h3>Home Assistant ja älykotiratkaisut</h3>
            <p>Suunnittelemme ja asennamme paikallisesti toimivat älykotijärjestelmät: Home Assistant -asennukset, ESPHome-laitteet, älykaihtimet, WLED- ja tunnelmavalaistukset sekä integraatiot laitteisiin, joita mikään valmis järjestelmä ei tue. Etätyönä koko Suomeen, asennuskäynnit Pirkanmaalla.</p>
          </div>
          <div>
            <h4>Kenelle</h4>
            <ul>
              <li>Kotitaloudet, jotka haluavat älykodin ilman kuukausimaksuja</li>
              <li>Home Assistant -käyttäjät, jotka kaipaavat apua vaikeaan integraatioon</li>
              <li>Rakentajat ja remontoijat, jotka suunnittelevat valaistusta ja automaatiota</li>
            </ul>
            <h4>Esimerkkejä</h4>
            <ul>
              <li>Home Assistant -asennus ja peruskonfiguraatio avaimet käteen</li>
              <li>Moottoroidut rullakaihtimet auringonnousun mukaan</li>
              <li>WLED-tunnelmavalaistus olohuoneeseen tai terassille</li>
            </ul>
            <div class="specs"><span class="spec">Home Assistant</span><span class="spec">ESPHome · WLED</span><span class="spec">Paikallinen · ei pilvipakkoa</span></div>
          </div>
        </article>

        <article class="service-detail" id="tuotekehitys">
          <div>
            <p class="eyebrow">04 · Tuotekehitys</p>
            <h3>Tuotekehitys, prototypointi ja piensarjat</h3>
            <p>Viemme idean luonnoksesta myyntikelpoiseksi tuotteeksi: konseptointi, nopea prototypointi, iterointi käyttäjäpalautteen pohjalta ja lopulta piensarjatuotanto. Koska mekaniikka, elektroniikka ja ohjelmisto tehdään samassa pajassa, iteraatiokierros kestää päiviä eikä kuukausia.</p>
          </div>
          <div>
            <h4>Kenelle</h4>
            <ul>
              <li>Startupit ennen sopimusvalmistajan etsimistä</li>
              <li>Pk-yritykset, jotka haluavat testata uutta tuoteideaa pienellä riskillä</li>
              <li>Teollisuuden kehitysyksiköt, jotka tarvitsevat nopean kokeilun</li>
            </ul>
            <h4>Tyypillinen kulku</h4>
            <ul>
              <li>Viikko 1: konsepti ja ensimmäinen karkea prototyyppi</li>
              <li>Viikot 2–4: iterointi, testaus ja materiaalivalinnat</li>
              <li>Sen jälkeen: piensarja tai dokumentaatio jatkovalmistusta varten</li>
            </ul>
            <div class="specs"><span class="spec">1–500 kpl sarjat</span><span class="spec">Dokumentaatio mukana</span></div>
          </div>
        </article>

        <article class="service-detail" id="korjaukset">
          <div>
            <p class="eyebrow">05 · Korjaukset</p>
            <h3>Korjaukset ja käänteissuunnittelu</h3>
            <p>Ennen kuin heität laitteen pois, kysy meiltä. Mittaamme hajonneen osan työntömitalla ja tarvittaessa skannaamalla, mallinnamme sen uudelleen ja vahvistamme kohdat, joista alkuperäinen petti. Usein korjaus maksaa murto-osan uuden laitteen hinnasta — ja on ympäristöteko.</p>
          </div>
          <div>
            <h4>Kenelle</h4>
            <ul>
              <li>Kuka tahansa, jonka laitteen muoviosa on hajonnut</li>
              <li>Yritykset, joiden tuotantolaitteen varaosa on poistunut markkinoilta</li>
              <li>Keräilijät ja entisöijät, jotka tarvitsevat osan jota ei ole saanut vuosikymmeniin</li>
            </ul>
            <h4>Esimerkkejä</h4>
            <ul>
              <li>Pesukoneen luukun salpa</li>
              <li>Vanhan stereolaitteen nuppi ja pidike</li>
              <li>Tuotantolinjan ohjainrulla erikoismateriaalista</li>
            </ul>
            <div class="specs"><span class="spec">Mittaus ja mallinnus</span><span class="spec">Alkuperäistä kestävämpi</span></div>
          </div>
        </article>

        <article class="service-detail" id="konsultointi">
          <div>
            <p class="eyebrow">06 · Konsultointi</p>
            <h3>Tekninen konsultointi ja harrastajien tuki</h3>
            <p>Joskus ei tarvita valmista laitetta vaan osaavaa apua. Autamme tuntipohjaisesti niin yrityksiä kuin harrastajia: Home Assistant -pulmat, ESPHome-konfiguraatiot, 3D-mallinnuksen sparraus tai oman projektin suunnittelukatselmointi etäyhteydellä.</p>
          </div>
          <div>
            <h4>Kenelle</h4>
            <ul>
              <li>Harrastajat, joiden projekti on jumissa</li>
              <li>Yritykset, jotka arvioivat teknologiavalintaa ennen investointia</li>
              <li>IT-osastot, jotka tarvitsevat IoT-osaamista määräaikaisesti</li>
            </ul>
            <h4>Miten toimii</h4>
            <ul>
              <li>Varaa etäsessio — näyttöjako ja suora apu ongelmaan</li>
              <li>Ensimmäinen puoli tuntia kartoitusta veloituksetta</li>
              <li>Saat session jälkeen kirjalliset muistiinpanot ja jatkosuositukset</li>
            </ul>
            <div class="specs"><span class="spec">Tuntiveloitus</span><span class="spec">Etänä koko Suomeen</span></div>
          </div>
        </article>

        <div class="cta-band mt-2">
          <h2>Etkö löytänyt palvelua listalta?</h2>
          <p>Lista ei ole koskaan täydellinen — erikoisimmat projektit ovat usein parhaita. Kerro mitä tarvitset, niin katsotaan onnistuuko.</p>
          <p style="margin-top:1.6rem"><a class="btn btn--light" href="/yhteys.html">Kysy meiltä</a></p>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- SERVICES EN
SERVICES_EN = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Services</p>
        <h1>What we do</h1>
        <p class="lead">Six service areas, one principle: we solve your problem instead of selling you stuff. Every project starts with a free quote.</p>
      </div>
    </section>

    <section class="section" style="padding-top:1rem">
      <div class="container">

        <article class="service-detail" id="3d-printing">
          <div>
            <p class="eyebrow">01 · Fabrication</p>
            <h3>3D printing, CAD modelling &amp; replacement parts</h3>
            <p>We model and print functional parts from measurements, a photo or the broken piece itself. In reverse engineering we measure the original, fix its design flaws and choose a material to match the job — heat, cold, outdoors or constant load.</p>
          </div>
          <div>
            <h4>Who it's for</h4>
            <ul>
              <li>Households with an appliance part that's no longer sold</li>
              <li>Companies needing a jig, fixture or small production run</li>
              <li>Hobbyists with a finished model but no printer</li>
            </ul>
            <h4>Examples</h4>
            <ul>
              <li>A dishwasher hinge the manufacturer discontinued</li>
              <li>A custom enclosure for an electronics project</li>
              <li>A 50-piece batch for product testing</li>
            </ul>
            <div class="specs"><span class="spec">PLA · PETG · ASA · TPU</span><span class="spec">OpenSCAD · Fusion 360</span><span class="spec">Delivery 3–7 days</span></div>
          </div>
        </article>

        <article class="service-detail" id="electronics">
          <div>
            <p class="eyebrow">02 · Electronics</p>
            <h3>Electronics prototyping &amp; embedded systems</h3>
            <p>We build working prototypes on ESP32, Arduino and Raspberry Pi: sensors, controls, displays and wireless connectivity. Every device ships with its source code and wiring diagrams, so the solution never becomes a black box.</p>
          </div>
          <div>
            <h4>Who it's for</h4>
            <ul>
              <li>Startups validating a hardware idea before big investments</li>
              <li>Industry needing measurement data quickly and affordably</li>
              <li>Inventors whose idea needs a working demo</li>
            </ul>
            <h4>Examples</h4>
            <ul>
              <li>Temperature and humidity monitoring for a production space</li>
              <li>A remote sensor that reports straight to Teams or email</li>
              <li>Servo-driven mechanics for your own product idea</li>
            </ul>
            <div class="specs"><span class="spec">ESP32 · ESP8266</span><span class="spec">Arduino · Raspberry Pi</span><span class="spec">MQTT · Wi-Fi · Zigbee</span></div>
          </div>
        </article>

        <article class="service-detail" id="smart-home">
          <div>
            <p class="eyebrow">03 · Smart home</p>
            <h3>Home Assistant &amp; smart home solutions</h3>
            <p>We design and install local-first smart home systems: Home Assistant setups, ESPHome devices, smart blinds, WLED and ambient lighting, and integrations for devices no off-the-shelf system supports. Remotely across Finland, on-site in the Tampere region.</p>
          </div>
          <div>
            <h4>Who it's for</h4>
            <ul>
              <li>Households that want a smart home without subscription fees</li>
              <li>Home Assistant users stuck on a tricky integration</li>
              <li>Builders and renovators planning lighting and automation</li>
            </ul>
            <h4>Examples</h4>
            <ul>
              <li>Turnkey Home Assistant installation and base configuration</li>
              <li>Motorised roller blinds that follow the sunrise</li>
              <li>WLED ambient lighting for a living room or terrace</li>
            </ul>
            <div class="specs"><span class="spec">Home Assistant</span><span class="spec">ESPHome · WLED</span><span class="spec">Local-first · no cloud lock-in</span></div>
          </div>
        </article>

        <article class="service-detail" id="product-development">
          <div>
            <p class="eyebrow">04 · Product development</p>
            <h3>Product development, prototyping &amp; small runs</h3>
            <p>We take an idea from sketch to sellable product: concepting, rapid prototyping, iteration on user feedback, and finally small-batch production. Because mechanics, electronics and software happen in the same workshop, an iteration cycle takes days, not months.</p>
          </div>
          <div>
            <h4>Who it's for</h4>
            <ul>
              <li>Startups before they look for a contract manufacturer</li>
              <li>SMEs testing a new product idea with low risk</li>
              <li>Industrial R&amp;D units that need a fast experiment</li>
            </ul>
            <h4>Typical flow</h4>
            <ul>
              <li>Week 1: concept and a first rough prototype</li>
              <li>Weeks 2–4: iteration, testing and material choices</li>
              <li>After that: a small batch, or documentation for scaled manufacturing</li>
            </ul>
            <div class="specs"><span class="spec">Batches of 1–500</span><span class="spec">Documentation included</span></div>
          </div>
        </article>

        <article class="service-detail" id="repairs">
          <div>
            <p class="eyebrow">05 · Repairs</p>
            <h3>Repairs &amp; reverse engineering</h3>
            <p>Before you throw the appliance away, ask us. We measure the broken part with callipers — and scanning when needed — remodel it, and reinforce the spots where the original failed. A repair often costs a fraction of a new device, and it's the sustainable choice.</p>
          </div>
          <div>
            <h4>Who it's for</h4>
            <ul>
              <li>Anyone with a broken plastic part in an otherwise good device</li>
              <li>Companies whose production machine's spare part has left the market</li>
              <li>Collectors and restorers needing a part unavailable for decades</li>
            </ul>
            <h4>Examples</h4>
            <ul>
              <li>A washing machine door latch</li>
              <li>A knob and bracket for a vintage stereo</li>
              <li>A guide roller for a production line, in a special material</li>
            </ul>
            <div class="specs"><span class="spec">Measure &amp; remodel</span><span class="spec">Stronger than the original</span></div>
          </div>
        </article>

        <article class="service-detail" id="consulting">
          <div>
            <p class="eyebrow">06 · Consulting</p>
            <h3>Technical consulting &amp; hobbyist support</h3>
            <p>Sometimes you don't need a finished device — just capable help. We assist companies and hobbyists by the hour: Home Assistant problems, ESPHome configurations, 3D-modelling sparring or a remote design review of your own project.</p>
          </div>
          <div>
            <h4>Who it's for</h4>
            <ul>
              <li>Hobbyists whose project is stuck</li>
              <li>Companies evaluating a technology choice before investing</li>
              <li>IT departments needing IoT expertise for a fixed term</li>
            </ul>
            <h4>How it works</h4>
            <ul>
              <li>Book a remote session — screen share and hands-on help</li>
              <li>The first half hour of scoping is free of charge</li>
              <li>You get written notes and recommendations after the session</li>
            </ul>
            <div class="specs"><span class="spec">Hourly rate</span><span class="spec">Remote, anywhere in Finland</span></div>
          </div>
        </article>

        <div class="cta-band mt-2">
          <h2>Didn't find your service on the list?</h2>
          <p>The list is never complete — the strangest projects are often the best ones. Tell us what you need and we'll see what's possible.</p>
          <p style="margin-top:1.6rem"><a class="btn btn--light" href="/en/contact.html">Ask us</a></p>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- PORTFOLIO
def _project(img, title, problem, solution, tech, result):
    return f"""
          <article class="card project reveal">
            <div class="project__media">{img}</div>
            <div class="project__body">
              <h3>{title}</h3>
              <dl class="project__facts">
                <dt>{problem[0]}</dt><dd>{problem[1]}</dd>
                <dt>{solution[0]}</dt><dd>{solution[1]}</dd>
                <dt>{tech[0]}</dt><dd>{tech[1]}</dd>
                <dt>{result[0]}</dt><dd>{result[1]}</dd>
              </dl>
            </div>
          </article>"""

IMG_BLINDS = """<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><rect x="30" y="30" width="240" height="20" rx="10" stroke="var(--primary)" stroke-width="2.5"/><rect x="40" y="60" width="220" height="80" rx="6" stroke="var(--primary)" stroke-width="2" stroke-dasharray="6 5"/><circle cx="270" cy="40" r="14" stroke="var(--accent)" stroke-width="2.5"/><path d="M270 40 v100" stroke="var(--muted)" stroke-width="1.5"/></svg>"""
IMG_BUS = """<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><rect x="60" y="40" width="180" height="90" rx="10" stroke="var(--primary)" stroke-width="2.5"/><text x="82" y="80" fill="var(--primary)" font-family="Spline Sans Mono, monospace" font-size="16">71 → 3 min</text><text x="82" y="106" fill="var(--muted)" font-family="Spline Sans Mono, monospace" font-size="14">8 · 12 · 27 min</text></svg>"""
IMG_FILTER = """<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><path d="M60 140 h180 v-60 a20 20 0 0 0 -20 -20 h-140 a20 20 0 0 0 -20 20 Z" stroke="var(--primary)" stroke-width="2.5" stroke-linejoin="round"/><circle cx="150" cy="100" r="22" stroke="var(--primary)" stroke-width="2.5"/><path d="M150 78 v-8 M150 130 v-8 M128 100 h-8 M180 100 h-8" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round"/></svg>"""
IMG_WLED = """<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><path d="M40 130 h220" stroke="var(--primary)" stroke-width="2.5"/><circle cx="70" cy="130" r="7" fill="var(--accent)"/><circle cx="120" cy="130" r="7" stroke="var(--primary)" stroke-width="2"/><circle cx="170" cy="130" r="7" fill="var(--accent)"/><circle cx="220" cy="130" r="7" stroke="var(--primary)" stroke-width="2"/><path d="M70 122 q0 -40 40 -50 M170 122 q0 -55 55 -60" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/></svg>"""
IMG_ARM = """<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><rect x="120" y="140" width="60" height="14" rx="7" stroke="var(--primary)" stroke-width="2.5"/><path d="M150 140 L130 90 L170 55" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="130" cy="90" r="6" fill="var(--accent)"/><circle cx="170" cy="55" r="6" fill="var(--accent)"/><path d="M170 55 q30 -10 40 10" stroke="var(--muted)" stroke-width="2" stroke-dasharray="4 4"/></svg>"""
IMG_PART = """<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><path d="M80 60 h100 a16 16 0 0 1 16 16 v20 h40 v50 H80 Z" stroke="var(--primary)" stroke-width="2.5" stroke-linejoin="round"/><circle cx="110" cy="90" r="10" stroke="var(--primary)" stroke-width="2"/><circle cx="110" cy="122" r="10" stroke="var(--primary)" stroke-width="2"/><path d="M80 40 h100 M80 34 v12 M180 34 v12" stroke="var(--muted)" stroke-width="1"/><text x="112" y="36" fill="var(--muted)" font-family="Spline Sans Mono, monospace" font-size="11">58 mm</text></svg>"""

PORTFOLIO_FI = f"""
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Portfolio</p>
        <h1>Töitämme</h1>
        <p class="lead">Jokainen projekti alkoi jonkun ongelmasta. Kuvat ovat toistaiseksi teknisiä piirroksia — valokuvat oikeista toteutuksista lisätään sitä mukaa kun asiakkaat antavat luvan.</p>
      </div>
    </section>
    <section class="section" style="padding-top:1rem">
      <div class="container">
        <div class="grid">
{_project(IMG_BLINDS, "Älykaihtimet Home Assistantiin",
  ("Ongelma", "Kaupalliset moottorikaihtimet maksoivat satoja euroja ikkunaa kohden ja vaativat valmistajan sovelluksen."),
  ("Ratkaisu", "Askelmoottoriyksikkö 3D-tulostetussa kotelossa, ESPHome-ohjaus ja liukusäädin Home Assistantin käyttöliittymässä. Sama ohjain skaalautuu useaan ikkunaan."),
  ("Teknologiat", "ESP8266, NEMA 17, A4988, ESPHome, 3D-tulostettu mekaniikka"),
  ("Tulos", "Kaihtimet avautuvat auringon mukana. Kustannus noin kolmasosa kaupallisesta ratkaisusta."))}
{_project(IMG_BUS, "Nysse-bussinäyttö eteiseen",
  ("Ongelma", "Bussiaikataulun tarkistaminen puhelimesta joka aamu — kengät jalassa, kädet täynnä."),
  ("Ratkaisu", "OLED-näyttö, joka hakee seuraavat neljä lähtöä omalta pysäkiltä Nyssen rajapinnasta Home Assistantin kautta."),
  ("Teknologiat", "WeMos D1 Mini, SSD1306, Home Assistant, Nysse API"),
  ("Tulos", "Lähtöajat näkyvät yhdellä vilkaisulla ovensuussa. Ei enää turhaa juoksua pysäkille."))}
{_project(IMG_FILTER, "Kissanvessan älysuodatin",
  ("Ongelma", "Hajut ehtivät levitä asuntoon ennen laatikon siivousta."),
  ("Ratkaisu", "Seinään kiinnitettävä suodatinyksikkö, jonka PIR-tunnistin käynnistää puhaltimen kissan käynnin jälkeen. Aktiivihiilipatruuna vaihtuu napsauttamalla."),
  ("Teknologiat", "PIR-anturi, 40 mm puhallin, USB-C, parametrinen OpenSCAD-suunnittelu"),
  ("Tulos", "Hajuton eteinen ja patruunanvaihto kymmenessä sekunnissa. Kehitteillä piensarjatuotteeksi."))}
{_project(IMG_WLED, "WLED-tunnelmavalaistus",
  ("Ongelma", "Olohuoneen valaistus oli joko täysillä tai pimeänä — tunnelmaa ei syntynyt."),
  ("Ratkaisu", "Epäsuora LED-nauhavalaistus WLED-ohjaimella, valmiit tunnelmat Home Assistantin painikkeisiin ja elokuvatila, joka reagoi televisioon."),
  ("Teknologiat", "WLED, WS2812B, ESP32, Home Assistant -automaatiot"),
  ("Tulos", "Valaistus vaihtuu tilanteen mukaan automaattisesti. Naapuritkin kysyivät toteuttajaa."))}
{_project(IMG_ARM, "Robottikäsi kissan leikkikaveriksi",
  ("Ongelma", "Kissa kaipasi virikettä myös silloin, kun ketään ei ole kotona."),
  ("Ratkaisu", "Kompakti servokäytöinen robottikäsi, joka heiluttaa lelua satunnaisilla liikeradoilla. Käynnistys etänä tai aikataululla Home Assistantista."),
  ("Teknologiat", "ESP32, MG90-servot, 3D-tulostettu runko"),
  ("Tulos", "Kissa viihtyy, ja liikeradat ovat riittävän arvaamattomia pitämään mielenkiinnon yllä."))}
{_project(IMG_PART, "Poistuneen varaosan käänteissuunnittelu",
  ("Ongelma", "Laadukkaan kodinkoneen sarana hajosi, eikä valmistaja enää toimita osaa."),
  ("Ratkaisu", "Alkuperäinen osa mitattiin, mallinnettiin ja vahvistettiin murtumakohdasta. Materiaaliksi valittiin iskunkestävä PETG."),
  ("Teknologiat", "Työntömittamittaus, Fusion 360, PETG-tulostus"),
  ("Tulos", "Kone palasi käyttöön alle viikossa. Uusi osa on kestänyt alkuperäistä pidempään."))}
        </div>
        <div class="cta-band mt-2">
          <h2>Sinun projektisi tähän?</h2>
          <p>Kerro ideasi — lisäämme portfolioomme mieluiten juuri sellaisia töitä, joita kukaan muu ei tee.</p>
          <p style="margin-top:1.6rem"><a class="btn btn--light" href="/yhteys.html">Pyydä tarjous</a></p>
        </div>
      </div>
    </section>
"""

PORTFOLIO_EN = f"""
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Portfolio</p>
        <h1>Our work</h1>
        <p class="lead">Every project started as someone's problem. The images are technical drawings for now — photos of real builds will be added as clients give permission.</p>
      </div>
    </section>
    <section class="section" style="padding-top:1rem">
      <div class="container">
        <div class="grid">
{_project(IMG_BLINDS, "Smart blinds for Home Assistant",
  ("Problem", "Commercial motorised blinds cost hundreds of euros per window and required the manufacturer's app."),
  ("Solution", "A stepper motor unit in a 3D-printed housing, ESPHome control and a position slider in the Home Assistant UI. The same controller scales to multiple windows."),
  ("Technologies", "ESP8266, NEMA 17, A4988, ESPHome, 3D-printed mechanics"),
  ("Result", "The blinds follow the sun. Cost roughly a third of the commercial option."))}
{_project(IMG_BUS, "Hallway bus departure display",
  ("Problem", "Checking the bus schedule on a phone every morning — shoes on, hands full."),
  ("Solution", "An OLED display that fetches the next four departures from your own stop via the Tampere transit API through Home Assistant."),
  ("Technologies", "WeMos D1 Mini, SSD1306, Home Assistant, Nysse API"),
  ("Result", "Departure times at a glance by the door. No more sprinting to the stop for nothing."))}
{_project(IMG_FILTER, "Smart litter box air filter",
  ("Problem", "Odours spread through the flat before the box gets cleaned."),
  ("Solution", "A wall-mounted filter unit whose PIR sensor starts the fan right after the cat's visit. The activated-carbon cartridge swaps with a snap."),
  ("Technologies", "PIR sensor, 40 mm fan, USB-C, parametric OpenSCAD design"),
  ("Result", "An odour-free hallway and a ten-second cartridge change. In development as a small-batch product."))}
{_project(IMG_WLED, "WLED ambient lighting",
  ("Problem", "The living room lighting was either full-on or off — no atmosphere in between."),
  ("Solution", "Indirect LED strip lighting with a WLED controller, preset scenes on Home Assistant buttons and a movie mode that reacts to the TV."),
  ("Technologies", "WLED, WS2812B, ESP32, Home Assistant automations"),
  ("Result", "The lighting adapts to the situation automatically. Even the neighbours asked who built it."))}
{_project(IMG_ARM, "Robotic cat teaser arm",
  ("Problem", "The cat needed stimulation even when no one is home."),
  ("Solution", "A compact servo-driven arm that waves a toy in randomised patterns. Started remotely or on a schedule from Home Assistant."),
  ("Technologies", "ESP32, MG90 servos, 3D-printed frame"),
  ("Result", "A happy cat — and movement patterns unpredictable enough to stay interesting."))}
{_project(IMG_PART, "Reverse-engineered discontinued spare part",
  ("Problem", "A hinge broke on a quality appliance and the manufacturer no longer supplies the part."),
  ("Solution", "The original part was measured, remodelled and reinforced at the fracture point. Impact-resistant PETG was chosen as the material."),
  ("Technologies", "Calliper measurement, Fusion 360, PETG printing"),
  ("Result", "The appliance was back in use within a week. The new part has outlasted the original."))}
        </div>
        <div class="cta-band mt-2">
          <h2>Your project here?</h2>
          <p>Tell us your idea — the projects we most like to add to this page are the ones nobody else will take on.</p>
          <p style="margin-top:1.6rem"><a class="btn btn--light" href="/en/contact.html">Request a quote</a></p>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- ABOUT
ABOUT_FI = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Tietoa meistä</p>
        <h1>Paja, joka sanoo harvoin ei</h1>
        <p class="lead">Tinkoder syntyi yksinkertaisesta havainnosta: maailma on täynnä ongelmia, joihin ei ole valmista tuotetta — mutta joihin on ratkaisu.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="container prose">
        <p>Tinkoder on tamperelainen paja, joka yhdistää kolme asiaa, jotka yleensä pitää ostaa kolmesta eri paikasta: mekaniikkasuunnittelun, elektroniikan ja ohjelmiston. Kun sama tekijä hallitsee koko ketjun, ratkaisusta tulee eheämpi — ja projektista nopeampi.</p>
        <p>Taustamme on vuosien harrastuneisuudessa ja sadoissa rakennetuissa projekteissa: älykoteja, antureita, moottoroituja mekanismeja, varaosia ja laitteita, joita ei ollut olemassa ennen kuin joku tarvitsi niitä. Se sama uteliaisuus näkyy asiakastöissä. Meille mielenkiintoisin toimeksianto on se, josta muut kieltäytyvät liian erikoisena.</p>
        <h2>Miten työskentelemme</h2>
        <p>Uskomme paikallisiin ratkaisuihin, jotka eivät ole riippuvaisia yhdestä pilvipalvelusta. Dokumentoimme kaiken niin, että asiakas voi halutessaan jatkaa itse. Ja sanomme suoraan, jos jokin idea ei kannata — ennen kuin siihen on kulunut euroakaan.</p>
        <h2>Arvomme</h2>
        <ul>
          <li><strong>Korjaaminen ennen korvaamista.</strong> Yksi hyvin suunniteltu osa pelastaa usein koko laitteen.</li>
          <li><strong>Avoimuus.</strong> Saat lähdekoodit, mallit ja dokumentaation — ratkaisu on sinun, ei meidän.</li>
          <li><strong>Rehellisyys.</strong> Kiinteä hinta, realistinen aikataulu, ei yllätyksiä laskussa.</li>
        </ul>
        <p class="mt-2"><a class="btn btn--primary" href="/yhteys.html">Ota yhteyttä</a></p>
      </div>
    </section>
"""

ABOUT_EN = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">About us</p>
        <h1>The workshop that rarely says no</h1>
        <p class="lead">Tinkoder was born from a simple observation: the world is full of problems with no product to buy — but with a solution to build.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="container prose">
        <p>Tinkoder is a Tampere-based workshop that combines three things you usually have to buy from three different places: mechanical design, electronics and software. When one maker controls the whole chain, the solution comes out more coherent — and the project moves faster.</p>
        <p>Our background is years of hands-on building and hundreds of finished projects: smart homes, sensors, motorised mechanisms, replacement parts and devices that didn't exist until someone needed them. The same curiosity carries into client work. The most interesting commission, for us, is the one everybody else turned down as too weird.</p>
        <h2>How we work</h2>
        <p>We believe in local-first solutions that don't depend on any single cloud service. We document everything so the client can carry on independently if they want. And we say it out loud when an idea isn't worth building — before a single euro has been spent on it.</p>
        <h2>Our values</h2>
        <ul>
          <li><strong>Repair before replace.</strong> One well-designed part often saves the whole device.</li>
          <li><strong>Openness.</strong> You get the source code, the models and the documentation — the solution is yours, not ours.</li>
          <li><strong>Honesty.</strong> Fixed price, realistic timeline, no surprises on the invoice.</li>
        </ul>
        <p class="mt-2"><a class="btn btn--primary" href="/en/contact.html">Get in touch</a></p>
      </div>
    </section>
"""

# ---------------------------------------------------------------- CONTACT
CONTACT_FI = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Yhteystiedot</p>
        <h1>Kerro, mitä tarvitset</h1>
        <p class="lead">Kuva, luonnos tai pari lausetta riittää. Vastaamme arkisin yleensä saman päivän aikana — tarjous on aina maksuton.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="container">
        <div class="grid grid--2">
          <div class="card">
            <form class="form" id="contact-form" novalidate>
              <div>
                <label for="name">Nimi</label>
                <input type="text" id="name" name="name" autocomplete="name" required>
              </div>
              <div>
                <label for="email">Sähköposti</label>
                <input type="email" id="email" name="email" autocomplete="email" required>
              </div>
              <div>
                <label for="topic">Aihe</label>
                <select id="topic" name="topic">
                  <option>3D-tulostus tai varaosa</option>
                  <option>Elektroniikka tai prototyyppi</option>
                  <option>Älykoti tai Home Assistant</option>
                  <option>Tuotekehitys tai piensarja</option>
                  <option>Korjaus</option>
                  <option>Konsultointi</option>
                  <option>Jokin muu</option>
                </select>
              </div>
              <div>
                <label for="message">Viesti</label>
                <textarea id="message" name="message" rows="6" required placeholder="Kuvaile ongelma tai idea omin sanoin. Mitat ja kuvat voi lähettää myös sähköpostilla."></textarea>
                <p class="hint">Emme jaa tietojasi kenellekään. Lue <a href="/tietosuoja.html">tietosuojaseloste</a>.</p>
              </div>
              <button class="btn btn--primary" type="submit">Lähetä viesti</button>
              <p class="form__status" role="status" aria-live="polite" data-success="Kiitos viestistäsi! Palaamme asiaan mahdollisimman pian."></p>
            </form>
          </div>
          <div>
            <div class="card" style="margin-bottom:1.4rem">
              <h3>Suoraan sähköpostilla</h3>
              <p><a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a></p>
              <p style="color:var(--muted)">Liitä mukaan kuvat ja mitat, jos niitä on — se nopeuttaa tarjousta huomattavasti.</p>
            </div>
            <div class="card" style="margin-bottom:1.4rem">
              <h3>Sijainti ja aukiolo</h3>
              <p style="color:var(--muted)">Tampere, Suomi<br>Ma–Pe 9–17 (paikkamerkki)<br>Etätyöt koko Suomeen</p>
            </div>
            <div class="card">
              <h3>Sosiaalinen media</h3>
              <p style="color:var(--muted)"><a href="#">Instagram</a> · <a href="#">YouTube</a> · <a href="#">LinkedIn</a> <span class="spec">paikkamerkit</span></p>
            </div>
          </div>
        </div>
      </div>
    </section>
"""

CONTACT_EN = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Contact</p>
        <h1>Tell us what you need</h1>
        <p class="lead">A photo, a sketch or a couple of sentences is enough. We usually reply the same working day — and the quote is always free.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="container">
        <div class="grid grid--2">
          <div class="card">
            <form class="form" id="contact-form" novalidate>
              <div>
                <label for="name">Name</label>
                <input type="text" id="name" name="name" autocomplete="name" required>
              </div>
              <div>
                <label for="email">Email</label>
                <input type="email" id="email" name="email" autocomplete="email" required>
              </div>
              <div>
                <label for="topic">Topic</label>
                <select id="topic" name="topic">
                  <option>3D printing or a replacement part</option>
                  <option>Electronics or a prototype</option>
                  <option>Smart home or Home Assistant</option>
                  <option>Product development or a small run</option>
                  <option>Repair</option>
                  <option>Consulting</option>
                  <option>Something else</option>
                </select>
              </div>
              <div>
                <label for="message">Message</label>
                <textarea id="message" name="message" rows="6" required placeholder="Describe the problem or idea in your own words. Dimensions and photos can also be sent by email."></textarea>
                <p class="hint">We never share your details. Read the <a href="/en/privacy.html">privacy policy</a>.</p>
              </div>
              <button class="btn btn--primary" type="submit">Send message</button>
              <p class="form__status" role="status" aria-live="polite" data-success="Thanks for your message! We'll get back to you as soon as possible."></p>
            </form>
          </div>
          <div>
            <div class="card" style="margin-bottom:1.4rem">
              <h3>Straight to email</h3>
              <p><a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a></p>
              <p style="color:var(--muted)">Attach photos and measurements if you have them — it speeds up the quote considerably.</p>
            </div>
            <div class="card" style="margin-bottom:1.4rem">
              <h3>Location &amp; hours</h3>
              <p style="color:var(--muted)">Tampere, Finland<br>Mon–Fri 9–17 (placeholder)<br>Remote work across Finland</p>
            </div>
            <div class="card">
              <h3>Social media</h3>
              <p style="color:var(--muted)"><a href="#">Instagram</a> · <a href="#">YouTube</a> · <a href="#">LinkedIn</a> <span class="spec">placeholders</span></p>
            </div>
          </div>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- PRIVACY
PRIVACY_FI = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Tietosuoja</p>
        <h1>Tietosuojaseloste</h1>
        <p class="lead">Päivitetty: heinäkuu 2026. Tämä on selkokielinen kuvaus siitä, mitä tietoja keräämme ja miksi.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="container prose">
        <h2>Rekisterinpitäjä</h2>
        <p>Tinkoder (Y-tunnus 0000000-0), Tampere, Suomi. Yhteydenotot: <a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a>.</p>
        <h2>Mitä tietoja keräämme</h2>
        <ul>
          <li>Yhteydenottolomakkeen tiedot: nimi, sähköposti ja viestin sisältö.</li>
          <li>Asiakassuhteen aikana syntyvät tiedot: tarjoukset, tilaukset ja laskutustiedot.</li>
        </ul>
        <p>Emme käytä seurantaevästeitä emmekä kolmannen osapuolen analytiikkaa. Kieli- ja teemavalintasi tallennetaan vain omaan selaimeesi, eikä niitä lähetetä meille.</p>
        <h2>Miksi käsittelemme tietoja</h2>
        <p>Tietoja käytetään ainoastaan yhteydenottoihin vastaamiseen, tarjousten laatimiseen ja asiakassuhteen hoitamiseen. Emme myy emmekä luovuta tietoja kolmansille osapuolille markkinointiin.</p>
        <h2>Säilytysaika</h2>
        <p>Yhteydenotot säilytetään enintään kaksi vuotta. Kirjanpitolain edellyttämät tiedot säilytetään lain vaatiman ajan.</p>
        <h2>Oikeutesi</h2>
        <p>Sinulla on oikeus tarkastaa, oikaista ja poistaa tietosi sekä vastustaa käsittelyä. Pyynnöt osoitteeseen <a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a>. Sinulla on myös oikeus tehdä valitus tietosuojavaltuutetulle.</p>
      </div>
    </section>
"""

PRIVACY_EN = """
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Privacy</p>
        <h1>Privacy policy</h1>
        <p class="lead">Updated: July 2026. A plain-language description of what data we collect and why.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="container prose">
        <h2>Data controller</h2>
        <p>Tinkoder (Business ID 0000000-0), Tampere, Finland. Contact: <a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a>.</p>
        <h2>What we collect</h2>
        <ul>
          <li>Contact form data: name, email and the contents of your message.</li>
          <li>Data created during a client relationship: quotes, orders and invoicing details.</li>
        </ul>
        <p>We use no tracking cookies and no third-party analytics. Your language and theme choices are stored only in your own browser and never sent to us.</p>
        <h2>Why we process data</h2>
        <p>Data is used solely to answer enquiries, prepare quotes and manage the client relationship. We do not sell or hand over data to third parties for marketing.</p>
        <h2>Retention</h2>
        <p>Enquiries are kept for a maximum of two years. Records required by accounting law are kept for the legally mandated period.</p>
        <h2>Your rights</h2>
        <p>You have the right to access, correct and delete your data, and to object to processing. Send requests to <a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a>. You also have the right to lodge a complaint with the Finnish Data Protection Ombudsman.</p>
      </div>
    </section>
"""

# ---------------------------------------------------------------- 404
NOTFOUND = """
    <section class="section center">
      <div class="container" style="max-width:640px">
        <p class="eyebrow">404</p>
        <h1>Tätä osaa ei löytynyt varastosta</h1>
        <p class="lead">Sivu on poistettu, siirretty tai osoitteessa on kirjoitusvirhe. Mutta hyvä uutinen: puuttuvien osien valmistaminen on erikoisalaamme.</p>
        <p lang="en" style="color:var(--muted)">Page not found — but making missing parts is our speciality.</p>
        <p class="mt-2">
          <a class="btn btn--primary" href="/">Etusivulle</a>
          <a class="btn btn--ghost" href="/en/" data-lang-link="en">Home (English)</a>
        </p>
      </div>
    </section>
"""

PAGES = [
    dict(path="palvelut.html", lang="fi",
         title="Palvelut — 3D-tulostus, elektroniikka, älykoti ja tuotekehitys | Tinkoder",
         desc="Tinkoderin palvelut: 3D-tulostus ja varaosat, elektroniikkaprototyypit, Home Assistant -älykotiratkaisut, tuotekehitys, korjaukset ja tekninen konsultointi.",
         fi_url="/palvelut.html", en_url="/en/services.html", active="services", content=SERVICES_FI),
    dict(path="en/services.html", lang="en",
         title="Services — 3D Printing, Electronics, Smart Home & Product Development | Tinkoder",
         desc="Tinkoder's services: 3D printing and replacement parts, electronics prototyping, Home Assistant smart home solutions, product development, repairs and technical consulting.",
         fi_url="/palvelut.html", en_url="/en/services.html", active="services", content=SERVICES_EN),

    dict(path="portfolio.html", lang="fi",
         title="Portfolio — Toteutettuja projekteja | Tinkoder",
         desc="Katso Tinkoderin toteuttamia projekteja: älykaihtimet, Nysse-bussinäyttö, WLED-valaistukset, robotiikkaa ja käänteissuunniteltuja varaosia.",
         fi_url="/portfolio.html", en_url="/en/portfolio.html", active="portfolio", content=PORTFOLIO_FI),
    dict(path="en/portfolio.html", lang="en",
         title="Portfolio — Completed Projects | Tinkoder",
         desc="See Tinkoder's completed projects: smart blinds, a live bus departure display, WLED lighting, robotics and reverse-engineered replacement parts.",
         fi_url="/portfolio.html", en_url="/en/portfolio.html", active="portfolio", content=PORTFOLIO_EN),

    dict(path="tietoa.html", lang="fi",
         title="Tietoa meistä — Paja, joka sanoo harvoin ei | Tinkoder",
         desc="Tinkoder on tamperelainen paja, joka yhdistää mekaniikkasuunnittelun, elektroniikan ja ohjelmiston. Tutustu arvoihimme ja tapaamme työskennellä.",
         fi_url="/tietoa.html", en_url="/en/about.html", active="about", content=ABOUT_FI),
    dict(path="en/about.html", lang="en",
         title="About Us — The Workshop That Rarely Says No | Tinkoder",
         desc="Tinkoder is a Tampere-based workshop combining mechanical design, electronics and software. Learn about our values and how we work.",
         fi_url="/tietoa.html", en_url="/en/about.html", active="about", content=ABOUT_EN),

    dict(path="yhteys.html", lang="fi",
         title="Yhteystiedot — Pyydä maksuton tarjous | Tinkoder",
         desc="Ota yhteyttä Tinkoderiin: kuva, luonnos tai pari lausetta riittää. Vastaamme yleensä saman päivän aikana. Tarjous on aina maksuton.",
         fi_url="/yhteys.html", en_url="/en/contact.html", active="contact", content=CONTACT_FI),
    dict(path="en/contact.html", lang="en",
         title="Contact — Request a Free Quote | Tinkoder",
         desc="Contact Tinkoder: a photo, a sketch or a couple of sentences is enough. We usually reply the same day. The quote is always free.",
         fi_url="/yhteys.html", en_url="/en/contact.html", active="contact", content=CONTACT_EN),

    dict(path="tietosuoja.html", lang="fi",
         title="Tietosuojaseloste | Tinkoder",
         desc="Tinkoderin tietosuojaseloste: mitä tietoja keräämme, miksi ja kuinka kauan niitä säilytetään.",
         fi_url="/tietosuoja.html", en_url="/en/privacy.html", active=None, content=PRIVACY_FI),
    dict(path="en/privacy.html", lang="en",
         title="Privacy Policy | Tinkoder",
         desc="Tinkoder's privacy policy: what data we collect, why, and how long we keep it.",
         fi_url="/tietosuoja.html", en_url="/en/privacy.html", active=None, content=PRIVACY_EN),

    dict(path="404.html", lang="fi",
         title="404 — Sivua ei löytynyt | Tinkoder",
         desc="Sivua ei löytynyt. Palaa Tinkoderin etusivulle.",
         fi_url="/404.html", en_url="/404.html", active=None, content=NOTFOUND),
]
