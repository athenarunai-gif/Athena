"""German text for the deck, keyed by the exact English run.

Only the copy changes — geometry, colours and font sizes stay as built, so the
German deck is the same deck in another language. Translations are kept at or
below the English length wherever a box is tight; where German cannot be that
short, the layout was checked by rendering, not by hope.
"""

# Numbers, product names and third-party names that stay as they are.
KEEP = {
    "AthenaRun", "Devin, Copilot", "Reflex, Bubble", "Palantir, MightyBot",
    "NVIDIA Inception", "ACCELERATOR · KARLSRUHE", "TEAM", "GO-TO-MARKET",
    "PIPELINE", "Q1 – Q2 2027", "TAM", "SAM", "SOM", "CEO", "CTO",
    "Patrick Knapp", "Michael Altermann", "Design", "Integration", "Compliance",
    "Designer", "Business Analyst", "Release",
    "61", "%", "01", "02", "03", "04", "05", "06", "07", "08", "–",
    "01  ", "02  ", "03  ", "04  ", "05  ", "06  ",
    "[Kunde oder Branche]", "[was gebaut wurde]", "[Ergebnis in einer Zeile]",
    "[Name · E-Mail · Telefon]", "Excel",
    "Ich lasse Ihnen eine Frage da, keinen Prospekt.",
    "Welcher Prozess bei Ihnen läuft heute in ",
    " und sollte es seit einem Jahr nicht mehr?",
    "Wenn Ihnen dazu gerade etwas eingefallen ist — sprechen Sie mich an. "
    "Wir machen daraus eine Anwendung. Und wenn Ihnen zwanzig einfallen, "
    "reden wir über die Plattform statt über die Anwendung.",
}

DE = {
    # ---- slide 1: opener ------------------------------------------------
    "We build the chain, not the generator.":
        "Wir bauen die Kette, nicht den Generator.",

    # ---- slide 2: the problem -------------------------------------------
    "Still manual.": "Immer noch manuell.",
    " And that is where the money goes.": " Dort geht das Geld verloren.",
    "THE PROBLEM": "DAS PROBLEM",
    "STILL MANUAL": "IMMER NOCH MANUELL",
    "Requirements": "Anforderungen",
    "Feasibility": "Machbarkeit",
    "Approval": "Freigabe",
    "Operations": "Betrieb",
    "Five steps around the code. Every one of them a handoff, a document, a wait.":
        "Fünf Schritte rund um den Code. Jeder davon eine Übergabe, "
        "ein Dokument, eine Wartezeit.",
    "THEY BOUGHT THE GENERATOR — THE CHAIN AROUND IT IS STILL MANUAL":
        "DER GENERATOR IST GEKAUFT — DIE KETTE DRUMHERUM LÄUFT MANUELL",
    "of organizations see no EBIT impact from AI":
        "der Unternehmen sehen keinen EBIT-Effekt durch KI",
    "The expensive failures happen before a line of code.":
        "Die teuren Fehler passieren vor der ersten Zeile Code.",
    " That’s the part we automate.": " Genau diesen Teil automatisieren wir.",
    "Source: McKinsey, The State of AI in 2025 — 39% attribute any EBIT impact to AI":
        "Quelle: McKinsey, The State of AI in 2025 — 39 % führen einen "
        "EBIT-Effekt auf KI zurück",

    # ---- slide 3: the illusion ------------------------------------------
    "Complex Software.": "Komplexe Software.",
    " Is it possible with AI tools?": " Geht das mit KI-Tools?",
    "THE ILLUSION": "DIE ILLUSION",
    "Starting has never been cheaper: an AI IDE, a chat, a prompt, and something "
    "runs. That ease is what makes the engineering behind it easy to underestimate.":
        "Der Einstieg war nie billiger: eine KI-IDE, ein Chat, ein Prompt — und "
        "etwas läuft. Genau diese Leichtigkeit lässt das Engineering dahinter "
        "unterschätzen.",
    "DAY ONE": "TAG EINS",
    "EVERYTHING AFTER": "ALLES DANACH",
    "Prototype": "Prototyp",
    "in an afternoon": "in Stunden",
    "Fit": "Passung",
    "Solves the real process?": "Löst den echten Prozess?",
    "Lives in your estate?": "Läuft in Ihrer IT?",
    "Assurance": "Nachweis",
    "Someone can sign it?": "Kann jemand abnehmen?",
    "Operation": "Betrieb",
    "Survives year two?": "Übersteht Jahr zwei?",
    "WHAT THE GAP COSTS": "WAS DIE LÜCKE KOSTET",
    "Easy start": "Leichter Start",
    "Underestimated engineering": "Unterschätztes Engineering",
    "Hidden work": "Versteckte Arbeit",
    "Rework": "Nacharbeit",
    "Lost speed, higher cost": "Weniger Tempo, höhere Kosten",
    "Lost EBIT": "Verlorenes EBIT",
    "None of this is optional.": "Nichts davon ist optional.",
    "  It only gets discovered late.": "  Es fällt nur spät auf.",

    # ---- slide 4: idea to package ---------------------------------------
    "From idea to build-ready package.": "Von der Idee zum baureifen Paket.",
    "THE CHAIN": "DIE KETTE",
    "One line, a human gate at every step. AI agents support every stage, ":
        "Eine Linie, an jedem Schritt eine menschliche Freigabe. KI-Agenten "
        "unterstützen jede Stufe, ",
    "Discover through AI Memory": "von Erfassen bis KI-Gedächtnis",
    " — from first conversation to a build-ready package.":
        " — vom ersten Gespräch bis zum baureifen Paket.",
    "Discover": "Erfassen",
    "from conversation": "aus dem Gespräch",
    "Analyze": "Analysieren",
    "scope + fit": "Umfang + Passung",
    "Research": "Recherche",
    "cited, deep": "belegt, tief",
    "pre-build gate": "Gate vor dem Bau",
    "AI Memory": "KI-Gedächtnis",
    "patterns carried in": "Muster fließen ein",
    "human gate at every transition": "menschliche Freigabe an jedem Übergang",
    "IDEA TO BUILD-READY PACKAGE": "IDEE ZUM BAUREIFEN PAKET",

    # ---- slide 5: package to software -----------------------------------
    "From package to running software.": "Vom Paket zur laufenden Software.",
    "The package is approved. ": "Das Paket ist freigegeben. ",
    "Build through Operate": "von Bauen bis Betreiben",
    " — from approved package to software running in production. Every decision "
    "that matters stays with a person.":
        " — vom freigegebenen Paket zur Software im Produktivbetrieb. Jede "
        "wichtige Entscheidung bleibt beim Menschen.",
    "01–05 · build-ready package": "01–05 · baureifes Paket",
    "Build": "Bauen",
    "code + review": "Code + Review",
    "human approval": "Freigabe durch Menschen",
    "Operate": "Betreiben",
    "monitoring": "Monitoring",
    "LEARN": "LERNEN",
    "  ·  validated patterns from every build carry into the next":
        "  ·  validierte Muster aus jedem Build fließen in den nächsten",
    "PACKAGE TO RUNNING SOFTWARE": "PAKET ZU LAUFENDER SOFTWARE",

    # ---- slide 6: lifecycle ---------------------------------------------
    "The full lifecycle.": "Der Lebenszyklus.",
    " Every phase has multiple agents.": " Jede Phase hat mehrere Agenten.",
    "LIFECYCLE": "LEBENSZYKLUS",
    "Planning through maintenance — the classic software lifecycle, run end to "
    "end by agents, with a ":
        "Planung bis Wartung — der klassische Softwarelebenszyklus, durchgängig "
        "von Agenten betrieben, mit ",
    "human gate at every handover.": "menschlicher Freigabe an jeder Übergabe.",
    "Planning": "Planung",
    "Analysis": "Analyse",
    "Implementation": "Implementierung",
    "Testing": "Test",
    "Maintenance": "Wartung",
    "ALL SIX PHASES": "ALLE SECHS PHASEN",
    "agent-run": "agentenbetrieben",
    "MULTIPLE AGENTS PER PHASE": "MEHRERE AGENTEN PRO PHASE",
    "Planning agents": "Planungs-Agenten",
    "scope from first conversation, feasibility and fit":
        "Umfang aus dem Gespräch, Machbarkeit",
    "Analysis agents": "Analyse-Agenten",
    "cited, deep research into the requirements":
        "belegte, tiefe Recherche zu den Anforderungen",
    "Design agents": "Design-Agenten",
    "architecture, checked at the compliance gate":
        "Architektur, geprüft am Compliance-Gate",
    "Build agents": "Build-Agenten",
    "implementation with code review": "Implementierung mit Code-Review",
    "Test agents": "Test-Agenten",
    "verification before the release approval":
        "Verifikation vor der Release-Freigabe",
    "Operations agents": "Betriebs-Agenten",
    "monitoring, patterns back to the library":
        "Monitoring, Muster zurück in die Bibliothek",
    "human gate at every handover": "menschliche Freigabe an jeder Übergabe",

    # ---- slide 7: the payoff --------------------------------------------
    "The payoff.": "Der Effekt.",
    " Fewer people. A better starting point.":
        " Weniger Leute. Ein besserer Startpunkt.",
    "THE PAYOFF": "DER EFFEKT",
    "The chain does the work that used to need a team — every project starts on "
    "what the last one learned.":
        "Die Kette leistet die Arbeit eines Teams — jedes Projekt startet "
        "auf dem, was das letzte gelernt hat.",
    "A TYPICAL PROJECT TEAM": "EIN TYPISCHES PROJEKTTEAM",
    "Developer": "Entwickler",
    "WITH ATHENARUN": "MIT ATHENARUN",
    "One developer": "Ein Entwickler",
    "or a business user": "oder Fachanwender",
    "+ agents on all six lifecycle phases": "+ Agenten auf allen sechs Phasen",
    "Fewer roles per project": "Weniger Rollen je Projekt",
    "Eliminates or reduces business analyst, designer and developer headcount "
    "per project.":
        "Reduziert oder ersetzt Business Analyst, Designer und Entwickler "
        "pro Projekt.",
    "One developer, internally": "Ein Entwickler, intern",
    "AthenaRun runs its own projects with a single developer.":
        "AthenaRun liefert eigene Projekte mit einem einzigen Entwickler.",
    "A business user can run it": "Auch für Fachanwender",
    "The platform is operated by the business, not only by engineers.":
        "Die Plattform bedient der Fachbereich, nicht nur die Entwicklung.",
    "A head start on day one": "Vorsprung ab Tag eins",
    "Customers inherit best practices and documented failure learnings from the "
    "first build.":
        "Kunden erben Best Practices und dokumentierte Fehler ab dem ersten Build.",
    "Same scope, a fraction of the team.": "Gleicher Umfang, ein Bruchteil des Teams.",
    "  The library is what makes that safe.":
        "  Die Bibliothek macht das sicher.",

    # ---- slide 8: the moat ----------------------------------------------
    "Our moat.": "Unser Vorsprung.",
    " Every build makes the next one safer.":
        " Jeder Build hilft dem nächsten.",
    "THE MOAT": "DER VORSPRUNG",
    "Capture": "Erfassen",
    "Reuse": "Wiederverwenden",
    "Anyone can generate code. What compounds is what real production builds "
    "taught us — every project writes validated patterns and documented failures "
    "back into the library, and every next build queries it before a line of code "
    "is written.":
        "Code generieren kann jeder. Was sich aufaddiert, ist das, was echte "
        "Produktions-Builds gelehrt haben — jedes Projekt schreibt validierte "
        "Muster und dokumentierte Fehler in die Bibliothek zurück, und jeder "
        "nächste Build fragt sie ab, bevor eine Zeile Code entsteht.",
    "THE PATTERN LIBRARY": "DIE MUSTER-BIBLIOTHEK",
    "Hundreds": "Hunderte",
    "validated patterns": "validierte Muster",
    "Thousands": "Tausende",
    "documented anti-patterns": "dokumentierte Anti-Patterns",
    "The LEARN loop from the chain is what fills this library.":
        "Die LERNEN-Schleife aus der Kette füllt diese Bibliothek.",
    "WHY IT'S DEFENSIBLE": "WARUM ES VERTEIDIGBAR IST",
    "Earned, not bought.": "Erarbeitet, nicht gekauft.",
    "The library only grows by running real production builds.":
        "Die Bibliothek wächst nur durch echte Produktions-Builds.",
    "It compounds.": "Sie verzinst sich.",
    "Every project makes the next estimate, gate and build safer.":
        "Jedes Projekt macht Schätzung, Gate und Build des nächsten sicherer.",
    "Capital can’t copy it.": "Kapital kopiert sie nicht.",
    "A bigger round buys code, not failures already survived.":
        "Eine größere Runde kauft Code, keine überlebten Fehler.",

    # ---- slide 9: references --------------------------------------------
    "References.": "Referenzen.",
    " Three builds, three problems.": " Drei Projekte, drei Probleme.",
    "REFERENCES": "REFERENZEN",
    "Shipped software, not pilots. Each one replaced a process that was running "
    "manually.":
        "Ausgelieferte Software, keine Piloten. Jede hat einen manuellen "
        "Prozess ersetzt.",
    "CFO App": "CFO-App",
    "CLIENT / SECTOR": "KUNDE / BRANCHE",
    "WHAT WE BUILT": "WAS WIR GEBAUT HABEN",
    "RESULT": "ERGEBNIS",
    "Lead Generation": "Lead-Generierung",
    "Board Assistant": "Board-Assistent",
    "PLACEHOLDER — replace the three bracketed fields per tile before this deck "
    "goes to an investor.":
        "PLATZHALTER — die drei Klammerfelder pro Kachel ersetzen, bevor dieses "
        "Deck an Investoren geht.",

    # ---- slide 10 / 11 --------------------------------------------------
    "One question.": "Eine Frage.",
    "ONE QUESTION": "EINE FRAGE",
    "Further questions.": "Weitere Fragen.",
    "APPENDIX": "ANHANG",

    # ---- slide 12: market -----------------------------------------------
    "The market.": "Der Markt.",
    " Three cuts, each one narrower.": " Drei Schnitte, jeder enger.",
    "MARKET SIZE": "MARKTGRÖSSE",
    "Every number below carries its assumption.":
        "Jede Zahl unten nennt ihre Annahme.",
    "CUSTOM SOFTWARE DELIVERY, GLOBAL": "INDIVIDUALSOFTWARE, GLOBAL",
    "~$65B": "~65",
    " 2026": " Mrd. $ · 2026",
    "Analyst range $51–74B. 21% CAGR through 2030.":
        "Analystenspanne 51–74 Mrd. $. 21 % CAGR bis 2030.",
    "EUROPE  ·  REGULATED SECTORS": "EUROPA  ·  REGULIERTE BRANCHEN",
    "$15–20B": "15–20",
    " serviceable": " Mrd. $ · erreichbar",
    "Delivery requiring a compliance gate and an audit trail.":
        "Projekte mit Compliance-Gate und Audit-Trail.",
    "5 YEARS  ·  CUMULATIVE CONTRACT VALUE": "5 JAHRE  ·  KUMULIERTER VERTRAGSWERT",
    "$150M": "150",
    " TCV": " Mio. $ · TCV",
    "250 customers × $600k. Both assumptions.":
        "250 Kunden × 600 T$. Beides Annahmen.",
    "AMBITION": "ANSPRUCH",
    "1% of SAM": "1 % des SAM",
    " — open source as the adoption lever.": " — Open Source als Adoptionshebel.",

    # ---- slide 13: landscape --------------------------------------------
    "The landscape.": "Das Wettbewerbsfeld.",
    " Everyone owns a segment. We own the chain.":
        " Jeder hat ein Segment, wir die Kette.",
    "COMPETITIVE MAP": "WETTBEWERBSKARTE",
    "Coding agents write. App builders assemble. Regulated-agent platforms "
    "automate workflows. None run idea to running software end to end.":
        "Code-Agenten schreiben. App-Builder setzen zusammen. Agenten-"
        "Plattformen automatisieren Workflows. Keiner deckt die Kette ab.",
    "idea to operate": "Idee bis Betrieb",
    "Coding agents": "Code-Agenten",
    "App builders": "App-Builder",
    "Reg. agent platforms": "Reg. Plattformen",
    "Requirements from conversation": "Anforderungen aus dem Gespräch",
    "Compliance advisory before code": "Compliance-Prüfung vor dem Code",
    "Autonomous build + review": "Autonomer Build + Review",
    "Human gate at every release": "Menschliche Freigabe je Release",
    "Operate after go-live": "Betrieb nach dem Go-live",
    "Learning loop across projects": "Lernschleife über Projekte",
    "full": "voll",
    "partial": "teils",
    "none": "keine",
    "The others compete on one column.":
        "Die anderen besetzen eine Spalte.",
    " Our moat is the whole row — and the loop nobody else has.":
        " Unser Vorsprung ist die ganze Zeile — und die Lernschleife.",

    # ---- slide 14: team -------------------------------------------------
    "Built by people who’ve": "Gebaut von Leuten, die",
    " done both sides.": " beide Seiten kennen.",
    "One sold enterprise software. One built it. Together they’ve seen the pain "
    "from both sides.":
        "Einer hat Unternehmenssoftware verkauft. Einer hat sie gebaut. "
        "Zusammen kennen sie den Schmerz von beiden Seiten.",
    "PRODUCT & ENGINEERING": "PRODUKT & ENGINEERING",
    "10+ years in B2B sales & GTM across Seed–Series E startups":
        "10+ Jahre B2B-Vertrieb & GTM, Seed bis Series E",
    "Closed mid-market and enterprise deals at 6–7 figure ACVs":
        "Mittelstand- und Enterprise-Deals mit 6–7-stelligen ACVs",
    "Record €7M enterprise landing deal closed":
        "Größter Abschluss: Enterprise-Deal über 7 Mio. €",
    "Scaled business functions to 20+": "Unternehmensbereiche auf 20+ skaliert",
    "10+ years in product development and software engineering":
        "10+ Jahre Produktentwicklung und Software-Engineering",
    "Built and scaled a core logistics platform for daily operations":
        "Logistik-Kernplattform gebaut, skaliert und betrieben",
    "Scaled engineering teams to 20+": "Engineering-Teams auf 20+ skaliert",
    "Owns architecture and the autonomous build pipeline":
        "Verantwortet Architektur und die autonome Build-Pipeline",
    "+ Christian Lux, Co-Founder, Full-Stack Developer":
        "+ Christian Lux, Co-Founder, Full-Stack-Entwickler",
    " — highly experienced in AI development and security.":
        " — sehr erfahren in KI-Entwicklung und Sicherheit.",

    # ---- slide 15: traction & roadmap -----------------------------------
    "Traction & roadmap.": "Traction & Roadmap.",
    " Demand before launch.": " Nachfrage vor dem Launch.",
    "TRACTION": "TRACTION",
    "Signed intent, a bank contract in signing and a Q4 closing pipeline — then "
    "ninety days to convert it.":
        "Ein Bankvertrag im Signing, eine Q4-Pipeline im Abschluss — dann "
        "neunzig Tage zur Umsetzung.",
    "International bank": "Internationale Bank",
    "contract in signing": "Vertrag im Signing",
    "per deal · several deals": "pro Deal · mehrere Deals",
    "closing in Q4 2026": "Abschluss in Q4 2026",
    "signed LOI pipeline": "unterschriebene LOI-Pipeline",
    "7 letters of intent": "7 Absichtserklärungen",
    "BACKED & DISTRIBUTED": "PARTNER & PROGRAMME",
    "Channel partner": "Channel-Partner",
    "DISTRIBUTION": "VERTRIEB",
    "Hessen AI Cohort 2026": "Hessen AI Kohorte 2026",
    "STATE ACCELERATOR": "LANDES-ACCELERATOR",
    "Cyberlab Cohort 2026": "Cyberlab Kohorte 2026",
    "INFRASTRUCTURE": "INFRASTRUKTUR",
    "NEXT 90 DAYS  ·  Q4 2026": "NÄCHSTE 90 TAGE  ·  Q4 2026",
    "Prove & launch": "Beweisen & launchen",
    "Close the bank contract and the Q4 deals":
        "Bankvertrag und Q4-Deals abschließen",
    "Convert the signed LOIs into paying pilots":
        "Absichtserklärungen in zahlende Piloten wandeln",
    "Platform launch — go-to-market live": "Plattform-Launch — Go-to-Market live",
    "Integrate & scale": "Integrieren & skalieren",
    "Ship integrations across CRM, ERP and Slack":
        "Integrationen für CRM, ERP und Slack ausliefern",
    "Scale through the channel partner and accelerators":
        "Über Channel-Partner und Accelerators skalieren",
    "Open the app marketplace, enterprise partnerships":
        "App-Marktplatz und Enterprise-Partnerschaften öffnen",
    "The hard part is done.": "Der schwere Teil ist erledigt.",
    " Contracts in signing, engine shipped — what’s ahead is distribution, not "
    "invention.":
        " Verträge im Signing, Engine läuft — jetzt folgt Vertrieb, keine "
        "Erfindung.",
}

# Slide 1, rebuilt natively because the English title is baked into the picture.
TITLE_DE = ("Code generieren ist gelöst.", "Software ausliefern nicht.")
SUB_DE = ("Der Engpass hat sich verschoben — vom Schreiben des Codes auf "
          "alles drumherum.")
