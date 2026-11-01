import json, io, os
# Nuove categorie (nicchie con disponibilita' a pagare) + 2 app ciascuna. Idempotente. Poi: python automation/allinea_hash.py en
C = [
("fatture-business","Fatture e business","🧾","Invoicing and business","invoicing-and-business"),
("finanza-personale","Budget e finanza","💶","Budget and finance","budget-and-finance"),
("scuola-studio","Scuola e studio","🎓","School and study","school-and-study"),
("sviluppo-web","Sviluppo e web","💻","Development and web","development-and-web"),
]
PC = ["windows","mac","linux"]
N = [
("fatturapida","FattuRapida","fatture-business",3999,"🧾",PC,
 "Crea fatture e preventivi in pochi clic, con anagrafica clienti.",
 "FattuRapida ti fa preparare fatture, preventivi e note di credito da modelli pronti, tenendo clienti e prodotti in un'unica anagrafica. I dati restano sul tuo computer.",
 ["Fatture, preventivi e note di credito da modelli personalizzabili","Anagrafica clienti e prodotti con ricerca veloce","Numerazione automatica e promemoria dei pagamenti scaduti","Esportazione in PDF e in XML da consegnare al tuo intermediario","Archivio sul tuo computer: nessun cloud obbligatorio"],
 "Professionisti e piccole attività che vogliono emettere documenti senza un gestionale complicato. Gli obblighi fiscali restano a tuo carico: verifica con il tuo commercialista.",
 "Create invoices and quotes in a few clicks, with a client database.",
 "FattuRapida lets you prepare invoices, quotes and credit notes from ready templates, keeping clients and products in a single database. Your data stays on your computer.",
 ["Invoices, quotes and credit notes from customizable templates","Client and product database with fast search","Automatic numbering and reminders for overdue payments","Export to PDF and XML to hand to your intermediary","Archive on your computer: no cloud required"],
 "Freelancers and small businesses who want to issue documents without a complicated management system. Tax obligations remain yours: check with your accountant."),
("stockbox","StockBox","fatture-business",2999,"📦",PC,
 "Tieni sotto controllo magazzino, scorte e fornitori.",
 "StockBox registra carichi e scarichi, ti avvisa quando un prodotto sta finendo e ti mostra a colpo d'occhio cosa riordinare e da chi.",
 ["Giacenze con soglia minima e avvisi di riordino","Carichi e scarichi anche con lettore di codici a barre","Inventario con esportazione in foglio di calcolo","Storico dei movimenti per ogni prodotto","Elenco fornitori con prezzi e tempi di consegna"],
 "Negozi, artigiani e piccoli e-commerce con un magazzino da tenere in ordine.",
 "Keep stock, supplies and suppliers under control.",
 "StockBox records stock in and out, warns you when a product is running low and shows at a glance what to reorder and from whom.",
 ["Stock levels with minimum threshold and reorder alerts","Stock in and out, also with a barcode reader","Inventory with spreadsheet export","Movement history for every product","Supplier list with prices and delivery times"],
 "Shops, craftspeople and small online stores with a warehouse to keep in order."),
("budgetcasa","BudgetCasa","finanza-personale",999,"💶",PC,
 "Tieni sotto controllo entrate, spese e risparmi di casa.",
 "BudgetCasa ti mostra dove vanno i soldi ogni mese: importi le spese, le assegni a una categoria e vedi subito quanto ti resta. Nessun collegamento alla banca, i dati restano sul tuo computer.",
 ["Categorie di spesa con regole automatiche","Budget mensili con avviso quando stai per superarli","Obiettivi di risparmio con barra di avanzamento","Grafici per mese e per categoria","Importazione dei movimenti da file CSV della banca"],
 "Famiglie e single che vogliono capire e ridurre le spese senza fogli di calcolo.",
 "Keep income, spending and savings at home under control.",
 "BudgetCasa shows where the money goes each month: import your expenses, assign a category and see at once what is left. No bank connection, your data stays on your computer.",
 ["Spending categories with automatic rules","Monthly budgets with an alert before you exceed them","Savings goals with a progress bar","Charts by month and by category","Import transactions from your bank's CSV file"],
 "Families and singles who want to understand and cut spending without spreadsheets."),
("speseinsieme","SpeseInsieme","finanza-personale",799,"🤝",PC+["android"],
 "Dividi le spese con coinquilini, famiglia e amici.",
 "SpeseInsieme tiene il conto di chi ha pagato cosa e calcola chi deve quanto a chi, con il minor numero possibile di pagamenti.",
 ["Gruppi per casa, viaggio o evento","Divisione in parti uguali o personalizzata","Saldo semplificato: chi deve dare e a chi","Spese in valute diverse per i viaggi","Esportazione del riepilogo da condividere"],
 "Coinquilini, coppie, famiglie e gruppi di amici in vacanza.",
 "Split expenses with flatmates, family and friends.",
 "SpeseInsieme keeps track of who paid what and works out who owes whom, with the fewest possible payments.",
 ["Groups for a home, a trip or an event","Equal or custom split","Simplified balance: who pays whom","Expenses in different currencies for trips","Export the summary to share"],
 "Flatmates, couples, families and groups of friends on holiday."),
]
N += [
("studydeck","StudyDeck","scuola-studio",899,"🎓",PC+["android"],
 "Flashcard con ripasso a intervalli per ricordare di più.",
 "StudyDeck ti ripropone ogni scheda al momento giusto, appena prima di dimenticarla, così studi meno tempo e ricordi più a lungo.",
 ["Ripasso a intervalli che si adatta alle tue risposte","Mazzi con immagini, formule e audio","Importazione di schede da file CSV","Statistiche di studio e serie di giorni consecutivi"],
 "Studenti di scuola e università e chi prepara concorsi ed esami.",
 "Flashcards with spaced repetition to remember more.",
 "StudyDeck shows each card again at the right moment, just before you forget it, so you study less and remember longer.",
 ["Spaced repetition that adapts to your answers","Decks with images, formulas and audio","Import cards from CSV files","Study statistics and daily streaks"],
 "School and university students and anyone preparing for exams."),
("dispensa-ai","DispensaAI","scuola-studio",1299,"📝",PC,
 "Trasforma appunti e dispense in riassunti e schemi.",
 "DispensaAI legge PDF e testi e prepara un riassunto a punti, uno schema e domande di ripasso. Funziona sul tuo computer con modelli locali, quindi serve un PC abbastanza potente.",
 ["Riassunto di PDF, slide e appunti","Schemi a punti e mappe dei concetti","Domande di ripasso generate dal testo","Elaborazione offline: i tuoi file non escono dal computer"],
 "Studenti e ricercatori con molto materiale da leggere. Controlla sempre il risultato: un riassunto automatico può contenere errori.",
 "Turn notes and handouts into summaries and outlines.",
 "DispensaAI reads PDFs and texts and prepares a bullet summary, an outline and review questions. It runs on your computer with local models, so a reasonably powerful PC is needed.",
 ["Summaries of PDFs, slides and notes","Bullet outlines and concept maps","Review questions generated from the text","Offline processing: your files never leave your computer"],
 "Students and researchers with a lot of material to read. Always check the result: an automatic summary can contain mistakes."),
("apilab","ApiLab","sviluppo-web",1999,"🧪",PC,
 "Prova e documenta le API senza scrivere codice.",
 "ApiLab ti fa inviare richieste a qualsiasi servizio web, controllare le risposte e salvare tutto in collezioni da riusare e condividere con il team.",
 ["Richieste REST con cronologia e collezioni","Variabili di ambiente per test, sviluppo e produzione","Controlli automatici sulle risposte","Esportazione della documentazione in HTML e Markdown"],
 "Sviluppatori e tester che lavorano con servizi web.",
 "Test and document APIs without writing code.",
 "ApiLab lets you send requests to any web service, check the responses and save everything in collections to reuse and share with your team.",
 ["REST requests with history and collections","Environment variables for test, development and production","Automatic checks on responses","Export documentation to HTML and Markdown"],
 "Developers and testers who work with web services."),
("sitesync","SiteSync","sviluppo-web",1499,"🔄",PC,
 "Carica il tuo sito sul server con un clic.",
 "SiteSync confronta la cartella del sito sul tuo computer con quella sul server e carica solo i file cambiati, via FTP o SFTP, con una copia di sicurezza prima di sovrascrivere.",
 ["Collegamenti FTP e SFTP con profili per più siti","Confronto tra cartella locale e server","Caricamento dei soli file modificati","Copia di sicurezza prima di ogni sovrascrittura"],
 "Chi gestisce siti web su hosting tradizionale.",
 "Upload your website to the server in one click.",
 "SiteSync compares the site folder on your computer with the one on the server and uploads only changed files, via FTP or SFTP, with a safety copy before overwriting.",
 ["FTP and SFTP connections with profiles for several sites","Comparison between local folder and server","Upload of changed files only","Safety copy before every overwrite"],
 "People who manage websites on traditional hosting."),
]
def md(i, f, w, hf, hw): return i + "\n\n## " + hf + "\n\n" + "\n".join("- " + x for x in f) + "\n\n## " + hw + "\n\n" + w
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
fn = '_data/catalogo.json'
d = json.load(io.open(fn, encoding='utf-8'))
cids = {c['id'] for c in d['categorie']}
for c in C:
    if c[0] not in cids:
        d['categorie'].append({"nome": c[1], "id": c[0], "icona": c[2], "tr": {"en": {"nome": c[3]}}})
    wr('_negozio/categoria-%s.md' % c[0], '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "%s"\nref: shop-cat-%s\n---\n' % (c[1], c[0], c[0], c[1], c[0]))
    wr('en/negozio/categoria/%s.md' % c[0], '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-cat-%s\ntr: tradotto\n---\n' % (c[3], c[0], c[4], c[3], c[0]))
ids = {p['id'] for p in d['prodotti']}
for x in N:
    if x[0] in ids: continue
    d['prodotti'].append({"tipo":"digitale","app":True,"id":x[0],"nome":x[1],"categoria":x[2],"prezzo_centesimi":x[3],
      "descrizione":x[6],"descrizione_completa":md(x[7],x[8],x[9],"Cosa puoi fare","Per chi è"),"immagine":"","icona":x[4],"visibile":True,
      "tr":{"en":{"nome":x[1],"descrizione":x[10],"descrizione_completa":md(x[11],x[12],x[13],"What you can do","Who it's for")}},"piattaforme":x[5]})
    wr('_negozio/%s.md' % x[0], '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s"\nref: shop-prod-%s\n---\n' % (x[1], x[0], x[0], x[6], x[0]))
    wr('en/negozio/%s.md' % x[0], '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-prod-%s\ntr: tradotto\n---\n' % (x[1], x[0], x[0], x[10], x[0]))
io.open(fn, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))
print('ok', len(d['categorie']), 'cat', len(d['prodotti']), 'prod')
