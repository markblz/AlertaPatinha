# Naming: shortlist, availability and conflicts for the Brazilian stray/lost-pet civic platform

All lookups were run live on 2026-10-21 from this machine: registro.br RDAP, Verisign RDAP, an anonymous INPI pePI trademark search, the iTunes Search API, Google Play search and listing HTML, and plain HTTP fetches of the domains. Registrant and applicant names are given only for companies. Private individuals are anonymized on purpose, even though RDAP and INPI publish their names.

How to read the RDAP codes:
- **404** means no registration object exists, so the domain is likely available. A domain can still be reserved or frozen, so confirm at checkout.
- **200** means the domain is registered.
- I checked the method first: `google.com.br` returned 200 and the nonsense name `zzqxnotreal123.com.br` returned 404. None of the ~220 queries hit rate limiting (no 429s).

---

## Q1. Candidate generation (≥25 candidates across styles, including the owner's two)

### Takeaway
I generated and checked 38 candidates in six styles. They form three families:
- **"Pet" compounds**: almost all of them are already taken.
- **"Bicho" compounds**: almost all are free, but they carry spelling and connotation baggage.
- **"Patinha"/"Caramelo" compounds**: the plain words are crowded, but SOS/Alerta combinations of them are mostly free.

### Cited Findings
Each name's domain codes are linked in Q2. Its INPI and app-store evidence is in Q3.
- **Owner's suggestions:** CuidaPet, EncontraPet.
- **"Pet" compounds:** AcheiPet, AchaPet, AlertaPet, SOS Pet, ResgataPet, SocorroPet, VistoPet, RastroPet, PetPerdido, MapaPet.
- **Verbs (first person / imperative):** Achei, Avistei, Farejei, Vi um Bicho, Achei Bicho, Acha Bicho, Ajuda Bicho, Avisa Bicho, Salva Bicho, Cadê Bicho.
- **Animal words:** Patinha, Patinhas, Focinho, Faro, Caramelo, Vira-lata, Bichinho.
- **Help/alert:** SOS Bicho, Alerta Bicho, Socorro Bicho, SOS Patinha, Alerta Patinha, SOS Caramelo, Alerta Caramelo.
- **Situational:** Bicho na Rua, Bicho Achado, Bicho Perdido, Rede Bicho.
- **Coined:** BichoSOS (domain `bichosos`), BichoAí. BichoAí turned out to be an existing competitor (see Q3).
- **Defensive and misspelling variants checked:** `alertabichos`, `alertabixo`, `sosbichos`, `sosbixo`, `acheibixo`, `sospatinhas`, `alertapatinhas`, `viubicho`.

### Inferences
- **"Bicho" vs "pet":** The platform is about strays and ferals, and those animals are not anyone's "pet". "Pet" is an anglicism tied to owned animals and pet-shop culture. "Bicho" is the everyday word for any animal across classes and regions. This is my sociolinguistic judgment; I have no corpus source for it.
- **Coined words:** Short invented words (Mapet, Achô and similar) fail the low-literacy "say it, type it" test almost by definition. I kept only BichoSOS as a test case, and it scored poorly.

### Gaps
- I did not test any names with users. Every rating of how understandable or memorable a name is comes from my own analysis.

---

## Q2. Domain availability (.com.br / .org.br / .app.br via registro.br RDAP; .com via Verisign RDAP)

### Takeaway
Every "Pet" compound that sounds natural is already registered as a .com.br. That includes both of the owner's names, AcheiPet, AchaPet, AlertaPet, SOS Pet and RastroPet. Four of the top-5 names are free across all four TLDs, along with their plural and "bixo" misspellings: Alerta Bicho, Alerta Patinha, SOS Caramelo and SOS Bicho. For SOS Bicho only the singular is free; its plural is not. SOS Patinha is free in the singular, but sospatinhas.com.br is taken.

### Cited Findings
Source pattern for every cell:
- `https://rdap.registro.br/domain/<name>.<tld>` (example: [alertabicho.com.br](https://rdap.registro.br/domain/alertabicho.com.br))
- `https://rdap.verisign.com/com/v1/domain/<name>.com` (example: [alertabicho.com](https://rdap.verisign.com/com/v1/domain/alertabicho.com))

All queried on 2026-10-21. 404 means free; 200 means registered.

| name | .com.br | .org.br | .app.br | .com |
|---|---|---|---|---|
| cuidapet | 200 | 404 | 404 | 200 |
| encontrapet | 200 | 404 | 404 | 200 |
| acheipet | 200 | 404 | 200 | 200 |
| achapet | 200 | 404 | 404 | 200 |
| alertapet | 200 | 404 | 404 | 200 |
| sospet | 200 | 200 | 404 | 200 |
| resgatapet | 404 | 404 | 404 | 404 |
| socorropet | 404 | 404 | 404 | 200 |
| vistopet | 404 | 404 | 404 | 404 |
| avistapet | 404 | 404 | 404 | 404 |
| rastropet | 200 | 404 | 404 | 200 |
| petperdido | 200 | 404 | 404 | 200 |
| petachado | 200 | 404 | 404 | 404 |
| mapapet | 200 | 404 | 404 | 200 |
| caramelopet | 200 | 404 | 404 | 200 |
| salvapet | 200 | 404 | 200 | 200 |
| petaqui | 200 | 404 | 404 | 200 |
| cadeopet | 200 | 404 | 404 | 404 |
| patrulhapet | 200 | 404 | 404 | 404 |
| achei | 200 | 404 | 200 | 200 |
| avistei | 200 | 404 | 404 | 200 |
| farejei | 200 | 404 | 404 | 200 |
| **alertabicho** | **404** | **404** | **404** | **404** |
| alertabichos | 404 | 404 | 404 | 404 |
| alertabixo | 404 | 404 | 404 | 404 |
| **sosbicho** | **404** | **404** | **404** | **404** |
| sosbichos | 200 | 200 | 404 | 404 |
| sosbixo | 404 | 404 | 404 | 404 |
| bichosos | 404 | 404 | 404 | 404 |
| viumbicho | 404 | 404 | 404 | 404 |
| viubicho | 404 | 404 | 404 | 404 |
| acheibicho | 404 | 404 | 404 | 404 |
| acheibixo | 404 | 404 | 404 | 404 |
| achabicho | 200 | 404 | 404 | 200 |
| achaobicho | 404 | 404 | 404 | 404 |
| ajudabicho | 404 | 404 | 404 | 404 |
| avisabicho | 404 | 404 | 404 | 404 |
| salvabicho | 404 | 404 | 404 | 404 |
| socorrobicho | 404 | 404 | 404 | 404 |
| cadebicho | 404 | 404 | 404 | 404 |
| redebicho | 404 | 404 | 404 | 404 |
| bichonarua | 404 | 404 | 404 | 404 |
| bichoachado | 404 | 404 | 404 | 404 |
| bichoavistado | 404 | 404 | 404 | 404 |
| bichoperdido | 200 | 404 | 404 | 404 |
| bichoaqui | 200 | 404 | 404 | 404 |
| bichoai | 200 | 404 | 404 | 404 |
| bichinho | 200 | 404 | 200 | 200 |
| **sospatinha** | **404** | **404** | **404** | **404** |
| sospatinhas | 200 | 404 | 404 | 404 |
| **alertapatinha** | **404** | **404** | **404** | **404** |
| alertapatinhas | 404 | 404 | 404 | 404 |
| patinha | 200 | 404 | 404 | 200 |
| patinhas | 200 | 404 | 200 | 200 |
| patanarua | 200 | 404 | 404 | 404 |
| focinho | 200 | 404 | 200 | 200 |
| faro | 200 | 404 | 200 | 200 |
| caramelo | 200 | 200 | 200 | 200 |
| viralata | 200 | 200 | 200 | 200 |
| **soscaramelo** | **404** | **404** | **404** | **404** |
| alertacaramelo | 404 | 404 | 404 | 404 |

What is behind the key taken domains: RDAP registration date plus an HTTP fetch of the site.
- **cuidapet.com.br:** Registered 2022-09-21 by an individual and renewed through 2027-09-21. The server answers HTTP 406 to non-browser clients, so I could not see its content. — [RDAP](https://rdap.registro.br/domain/cuidapet.com.br)
- **encontrapet.com.br:** Registered 2026-07-04 by PHDEV LTDA. It is a live lost-pet platform titled *"Encontra Pet — encontre seu pet perdido. Vamos procurar juntos."* It has lost and found listings, a clinic directory and filters by dog/cat and date. Its taglines include "Milhares de reencontros começam com uma busca." — [RDAP](https://rdap.registro.br/domain/encontrapet.com.br); [site](https://encontrapet.com.br/)
- **acheipet.com.br:** Registered 2012-12-19 by an individual and renewed to 2028. The site redirects to a dead JSF app (HTTP 404). — [RDAP](https://rdap.registro.br/domain/acheipet.com.br)
- **acheipet.app.br:** Registered 2026-05-29. It is a live product: *"AcheiPet: a tag NFC e QR Code para a coleira do seu pet"*. — [RDAP](https://rdap.registro.br/domain/acheipet.app.br); [site](https://acheipet.app.br/)
- **acheipet.com:** Listed for sale on HugeDomains. — [site](https://acheipet.com/)
- **achapet.com.br:** Registered 2025-12-31 by an individual. It is a Hostinger parked page. — [RDAP](https://rdap.registro.br/domain/achapet.com.br)
- **alertapet.com.br:** Registered 2020-07-04 by an individual and renewed to 2027-07-04. No HTTP response, so the domain is held but apparently unused. — [RDAP](https://rdap.registro.br/domain/alertapet.com.br)
- **sospet.org.br:** Registered by "Instituto SOS PET Uberlândia", a live castration program for dogs and cats. sospet.com.br was registered 2025-07-16 by an individual. — [RDAP](https://rdap.registro.br/domain/sospet.org.br); [site](https://sospet.org.br/)
- **rastropet.com.br:** Registered 2026-07-30. It is live as *"RastroPET — Coleira GPS e monitoramento para pets"*. — [RDAP](https://rdap.registro.br/domain/rastropet.com.br); [site](https://rastropet.com.br/)
- **bichoperdido.com.br:** Registered 2026-01-19. The site is live and titled "Bicho Perdido", with no other content visible. — [RDAP](https://rdap.registro.br/domain/bichoperdido.com.br); [site](https://bichoperdido.com.br/)
- **avistei.com.br:** Registered 2009 by DITCOM INTERNET LTDA. The page says "Avistei - Domínio Premium à venda!" — [RDAP](https://rdap.registro.br/domain/avistei.com.br); [site](https://avistei.com.br/)
- **patinha.com.br:** Registered 2001 by "Nova Patinha Materiais de Construção". — [RDAP](https://rdap.registro.br/domain/patinha.com.br)
- **caramelo.com.br:** Registered 1996 by "CARAMELO ARQUITETOS ASSOCIADOS LTDA". — [RDAP](https://rdap.registro.br/domain/caramelo.com.br)
- **focinho.com.br:** Registered 2024 by "9Media Serviços Digitais Ltda". — [RDAP](https://rdap.registro.br/domain/focinho.com.br)
- **achabicho.com.br:** Registered 2012-10-04 by an individual. No HTTP response. — [RDAP](https://rdap.registro.br/domain/achabicho.com.br)

### Inferences
- **alertapet.com.br may be buyable:** It has been held since 2020 by an individual and serves nothing, so it may be acquirable. avistei.com.br is openly for sale. Both are options only if the owner is willing to pay.
- **Plural misspellings for SOS Patinha and SOS Bicho:** A voice note saying "SOS Patinha" will often be typed as "sospatinhas", and that .com.br is someone else's. sosbichos.com.br and sosbichos.org.br are also taken. This is a real leak risk for both SOS names.
- **Alerta Bicho is the cleanest set:** Every variant is free across all 4 TLDs: singular, plural (`alertabichos`) and the common misspelling (`alertabixo`). That lets the owner register all of them defensively and redirect them.

### Gaps
- I did not verify registro.br eligibility rules for .org.br and .app.br, for example whether a non-profit CNPJ is required for .org.br.
- A 404 is a strong signal, not a guarantee. Domains in release or freezing processes can still be blocked.
- I could not see what cuidapet.com.br hosts (HTTP 406), nor who controls the "EncontraPet" Play app compared with encontrapet.com.br.

---

## Q3. Conflicts: existing apps, businesses, Instagram, INPI

### Takeaway
- **Owner's names:**
  - **CuidaPet** is blocked at INPI. There are pending "cuidapet" applications in classes 09 (software) and 42 (IT services), exactly the classes this platform needs, plus a CUIDA PET LTDA application in class 44.
  - **EncontraPet** is taken in practice. There is a same-named Google Play app and a live lost-pet site, both from 2026.
- **AcheiPet and AchaPet** are taken by INPI registrations and/or same-concept apps.
- **Direct concept competitors** already exist under the names BichoAí, AchaPet, EncontraPet and Pets – Perdidos e Achados. All are tiny (10+ installs).
- **"Bicho" names** are INPI-clean, but app-store searches for them are flooded with jogo-do-bicho gambling apps and insect apps.

### Cited Findings

**INPI (pePI "Pesquisa Radical" by trademark name, anonymous session, 2026-10-21).**
Search page: [busca.inpi.gov.br pePI](https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_classe_basica.jsp). The results are session-bound, so I cite process numbers so that each can be re-checked.

- **CuidaPet: 9 processes.**
  - 938675621 (NCL 09) and 938675648 (NCL 42), mark "cuidapet". Filed 2025-04-08 by an individual. Status: "Aguardando exame de mérito".
  - 939715163, "CUIDA PET", NCL 44. Filed 2025-06-25 by **CUIDA PET LTDA**. Status: awaiting examination.
  - 936939672, "Cuida+Pet", NCL 35. Filed by P&R COMERCIO DE PRODUTOS VETERINARIOS LTDA. Status: awaiting examination.
  - 940683008, "CUIDA PET", NCL 05. Filed 2025-08-20. Status: awaiting examination.
  - Older filings were refused or archived: 912946636, 918428807, 931537207, 935392505.
- **EncontraPet / "Encontra Pet":** 0 processes. "Encontre Meu Pet" also returned 0.
- **AcheiPet: 5 processes.**
  - 906489989, "ACHEI PET", NCL 35. **Registration in force** since its 2013 filing. Holder: ACHEI PET DIVULGAÇÃO ON-LINE LTDA – EPP.
  - 945051689, 945051760, 945051905 and 945051999, "AcheiPet", NCL 18, 09, 42 and 35. Filed 2026-09-01 by an individual. Status: awaiting the opposition period. The owner of acheipet.app.br has the same name as this applicant.
- **AchaPet:** 928483541 (NCL 38) and 928483606 (NCL 42), "acha.pet". **Registrations in force.** Holder: ICODEL – IMPORTAÇÃO E COMÉRCIO DE DISPOSITIVOS ELETRONICOS LTDA.
- **SOS Bicho (13 hits on the radical search, most of them "NOSSOS BICHOS"):**
  - 925611751, "SOS BICHO URBANO", NCL 45. Filed 2022 by an individual. Listed as "Registro de marca em vigor", although the class field oddly reads "Deferida … Excluída".
  - 910384452, "Clínica Veterinária SOS Bichos", NCL 44. Status: "Aguardando fim de sobrestamento".
  - 905678150, "SOS BICHOS", NCL 43. Filed by SOS BICHOS – ASSOCIAÇÃO DE PROTEÇÃO ANIMAL. Status: definitively archived.
- **SOS Patinha:**
  - 902681753, "S.O.S. PATINHA", NCL 44. Registration **extinct**.
  - 928580741, "SOS PATINHAS", NCL 44. Definitively archived.
  - Of the 332 "patinha" processes, none other has an SOS, alert or rescue theme.
- **Caramelo:** 696 processes. None has an SOS, alert or rescue theme. "SOS Caramelo" returned 0.
- **Patinha:** 332 processes.
- **Rede Bicho:** 932125433, "REDE BICHOS", NCL 35. Definitively archived (2023).
- **Avista Pet:** The only matches are 937388300 and 937388351, "Bella Vista Pet". 937388351 (NCL 44) is a registration in force.
- **Zero hits:** Alerta Bicho, Alerta Pet, Achei Bicho, Vi um Bicho, Ajuda Bicho, Bicho Achado, Salva Bicho, Socorro Bicho, Avisa Bicho, Bicho na Rua, Resgata Pet, Socorro Pet, Bicho Aí, Alerta Animal.

**Google Play** (search pages fetched with hl=pt_BR, gl=BR, for example [search "encontrapet"](https://play.google.com/store/search?q=encontrapet&c=apps&hl=pt_BR&gl=BR)).
- **EncontraPet** ([listing](https://play.google.com/store/apps/details?id=com.wdmapps.encontrapet)), package `com.wdmapps.encontrapet`, developer "williamwdm". Its description reads: "O EncontraPet foi criado para ajudar pessoas a divulgarem animais perdidos, encontrados ou disponíveis para adoção…" It has 10+ downloads and was updated 25 Aug 2026.
- **AchaPet: encontre e ajude** ([listing](https://play.google.com/store/apps/details?id=br.com.doglost.app)), developer Valoryn Labs. It is the same concept as this platform: "Consulte alertas próximos no mapa, publique ocorrências com foto e localização e mobilize a comunidade quando um pet estiver perdido, for visto na rua ou precisar de ajuda." It has 10+ downloads and was updated 21 Sep 2026.
- **BichoAí** ([listing](https://play.google.com/store/apps/details?id=br.com.bichoai.bichoai_app)), from an individual developer. Its tagline is "Viu um bicho aí? Marque no mapa e ajude." and it calls itself "o Waze colaborativo da proteção animal". It registers "Animais em situação de rua, feridos, perdidos ou encontrados", adoption, water and food points, and vaccination and castration campaigns. It has 10+ downloads and was updated 5 Oct 2026. Its domain bichoai.com.br is also registered ([RDAP](https://rdap.registro.br/domain/bichoai.com.br)).
- **Alerta Animal** ([listing](https://play.google.com/store/apps/details?id=br.com.alerta.animal.rs)) is an academic wildlife and roadkill reporting app ("Viu um animal silvestre na estrada? Reporte em segundos…"). It has 100+ downloads and was updated 12 Oct 2026.
- **Pets – Perdidos e Achados** ([listing](https://play.google.com/store/apps/details?id=app.emergent.petreunion6e1d5ef9d)) was updated 30 Sep 2026.
- **"Bicho" search results are polluted by gambling and insect apps:**
  - [search "alerta bicho"](https://play.google.com/store/search?q=alerta%20bicho&c=apps&hl=pt_BR&gl=BR) returns "Alerta Animal", "Palpite do Bicho – Resultados", "O Jogo do Bicho Resultados" and "Identificador de Insetos".
  - [search "vi um bicho"](https://play.google.com/store/search?q=vi%20um%20bicho&c=apps&hl=pt_BR&gl=BR) returns "Jogo do Bicho" first.
  - [search "ajuda bicho"](https://play.google.com/store/search?q=ajuda%20bicho&c=apps&hl=pt_BR&gl=BR) returns three jogo-do-bicho apps.
  - [search "achei bicho"](https://play.google.com/store/search?q=achei%20bicho&c=apps&hl=pt_BR&gl=BR) returns only insect apps.
- **No same-named app found on Play:** [search "sos bicho"](https://play.google.com/store/search?q=sos%20bicho&c=apps&hl=pt_BR&gl=BR) returned only generic SOS and panic apps.

**Apple App Store** (iTunes Search API, country=br, for example [term "encontra pet"](https://itunes.apple.com/search?country=br&entity=software&limit=6&term=encontra%20pet)).
- **"encontra pet"** returns several similar apps: "Pets – Perdidos e Achados", "Localiza Pet APP", "**AchaPet: encontre e ajude**", "SociPet: Encontre e Ajude Pets" and "Encontre Meu Pet".
- **"alerta pet"** returns "Aurora: Pets Perdidos e Adoção" and "Pet Help: Achados e Perdidos". Neither is named Alerta Pet ([query](https://itunes.apple.com/search?country=br&entity=software&limit=6&term=alerta%20pet)).
- **"caramelo"** returns "Caramelos: Rede Social Pet" (KAHU TECHNOLOGY LTDA) and "**Caramelo Pet**", which is published by a pet funeral and crematorium company ([query](https://itunes.apple.com/search?country=br&entity=software&limit=6&term=caramelo)).
- **"patinha"** returns "Só Patinhas", "Patinha", "Patinhas APP – Controle de Pet" and "Patinha do amigo pet" ([query](https://itunes.apple.com/search?country=br&entity=software&limit=6&term=patinha)).
- **No same-named app on iOS:** cuidapet, encontrapet, acheipet, "achei bicho" and "vi um bicho" returned 0 results. "sos bicho", "alerta bicho" and "salva bicho" returned only unrelated apps.

**Businesses and NGOs** (web search).
- There is no single national "SOS Bicho". Local groups include "SOS Bichos da Vila", declared a state public-utility entity by Santa Catarina law, and SOS Animais Pelotas. — [ALESC](https://portalelegis.alesc.sc.gov.br/documentos/6Y1Yv); [UFPel](https://anais-siiepe.ufpel.edu.br/2017/XU_03557.pdf)
- No NGO named exactly "SOS Patinhas" turned up, but "Patinhas…" is a very common naming pattern for protection NGOs: Patinhas Carentes (ES), Patinhas Slz (MA), Patinhas em Apuros (RS) and SOS 4 Patas (PR). — [A Gazeta](https://www.agazeta.com.br/hz/pet/em-dificuldades-ong-do-es-que-cuida-de-mais-de-100-animais-busca-novo-espaco-0424); [O Imparcial](https://oimparcial.com.br/cidades/2019/12/5-ongs-para-adotar-animais-de-estimacao-em-sao-luis/5/); [Escoteiros](https://www.escoteiros.org.br/wp-content/uploads/2026/03/Patinhas-a-obra-65.RS-1.pdf); [Bem Paraná](https://www.bemparana.com.br/publicacao/blogs/simonebello/familia-madalosso-inaugura-espaco-exclusivo-para-pets-e-realiza-acao-solidaria-com-a-ong-sos-4-patas-2/amp/)
- Web search found no app called "CuidaPet". The nearest match is a Spanish pet-sitter app, "CuidaMiMascota". — [search context](https://www.diaridetarragona.com/tarragona/145710/mascotas-sus-cuidados-y-caprichos-en-un-solo-click-en-el-smartphone-20200603-0021-ehdt202006030021.html)
- Web search found no "Alerta Bicho", "Bicho Achado" or "Ajuda Bicho" service. — (web search, 2026-10-21; results were wildlife-rescue articles only, e.g. [O Liberal](https://www.oliberal.com/belem/o-que-fazer-ao-encontrar-um-animal-silvestre-veja-orientacoes-apos-casos-com-botos-em-belem-1.1102574))
- Older Brazilian lost-pet apps and projects exist, for example GoApp (GoMap) and the academic AniMaps (CEFET-MG). — [ABC da Comunicação](https://www.abcdacomunicacao.com.br/casal-cria-aplicativo-ideal-para-quem-e-apaixonado-por-pets/); [CEFET-MG](https://www.digddv.cefetmg.br/wp-content/uploads/sites/52/2018/02/AniMaps.pdf)

**Instagram:** Every handle probe returned HTTP 401, because Instagram requires a login (via `i.instagram.com/api/v1/users/web_profile_info/`). I could not verify any handle. See Gaps.

### Inferences
- **Clearly taken by existing pet apps or brands:**
  - EncontraPet: a Play app plus a live lost-pet site.
  - AchaPet: a same-concept app on both stores, plus INPI registrations in classes 38/42.
  - AcheiPet: an INPI registration in force plus an NFC-tag product with 2026 filings in classes 9/18/35/42.
  - RastroPet: a GPS collar brand.
  - BichoAí: a same-concept app. Its tagline also effectively kills "Vi um Bicho".
  - Caramelo Pet: a pet crematorium app.
  - SOS Pet: an Uberlândia castration NGO that owns the .org.br.
- **Risk of using CuidaPet:** Using it for a software platform would probably collide with the pending class 09/42 "cuidapet" applications if they are granted. Brazil's INPI is first-to-file. This is my reading of the records, not legal advice.
- **"Bicho" names are free because they are noisy:** The word is generic. It also means "bug/insect" and is the root of "jogo do bicho". Expect worse discoverability in app-store search, and pre-empt it with a store subtitle such as "animais perdidos e feridos".
- **Several near-identical products launched in 2026, all tiny (10+ installs):** AchaPet, BichoAí, EncontraPet and Pets – Perdidos e Achados. Expect name and positioning crowding to grow, so file an INPI application early (classes 09, 42 and probably 45) once a name is chosen.

### Gaps
- Instagram handles are unverified because of the login wall. Hashtag volumes (#alertabicho, #sospatinha and so on) are also unverified.
- INPI checks were done by radical name search only. I did not run a phonetic or figurative search, and I did not query reorderings such as "Bicho Alerta". I did not search INPI for Avistei, Cadê Bicho, Farejei or SOS Pet.
- I could not establish whether the EncontraPet Play developer and PHDEV LTDA (owner of encontrapet.com.br) are the same entity.

---

## Q4. Evaluation and scored table

### Takeaway
Once names whose domains or trademarks are taken are set aside, the best options come out in a near three-way tie:
- **Alerta Bicho**, **Alerta Patinha** and **SOS Patinha** each score 35/45.
- **SOS Caramelo** and **SOS Bicho** follow at 34/45.

The core tradeoff is between "bicho" and "patinha":
- **"Bicho"** covers every species and is the street word for animals, but carries ch/x spelling, insect and gambling noise.
- **"Patinha"** is spelled cleanly, warm and has no gambling noise, but the "Patinhas" naming space is crowded and it leans toward dogs and cats.

### Cited Findings
- I scored on a 1–5 scale per criterion. The scores are my judgment. Each availability (A) score rests on the cited evidence in Q2 and Q3.
- **Criteria:**
  - **ST** = say-it, type-it: can someone who hears it in a voice note type it correctly? Ambiguous ch/x/ç/ss, accents, English words and spacing all lower the score.
  - **M** = memorability.
  - **L** = length of the domain string: ≤7 characters = 5, 8–9 = 4, 10–11 = 3, 12–13 = 2.
  - **H** = how clean the hashtag would be.
  - **HF** = conveys both help/emergency and find/sighting.
  - **SN** = species-neutral.
  - **C** = free of negative, slang, gambling or insect connotations.
  - **W** = works as a WhatsApp contact name and in "posta no X".
  - **A** = availability across domains, INPI and apps.

| # | Name | Style | ST | M | L | H | HF | SN | C | W | A | Total /45 | Decisive note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AlertaPet | Pet+alert | 5 | 4 | 4 | 3 | 5 | 4 | 5 | 4 | 2 | 36 | .com.br and .com taken (dormant since 2020); INPI clean |
| 2 | **Alerta Bicho** | alert+bicho | 3 | 4 | 3 | 4 | 5 | 5 | 3 | 4 | 4 | **35** | All 4 TLDs plus `alertabichos`/`alertabixo` free; INPI 0; "Alerta Animal" (wildlife) app is similar |
| 3 | **Alerta Patinha** | alert+animal word | 4 | 4 | 2 | 4 | 5 | 4 | 5 | 3 | 4 | **35** | All 4 TLDs plus plural free; long (13 characters) |
| 4 | **SOS Patinha** | SOS+animal word | 4 | 5 | 3 | 4 | 3 | 4 | 5 | 4 | 3 | **35** | Singular free; `sospatinhas.com.br` taken; INPI only extinct or archived marks |
| 5 | **SOS Caramelo** | SOS+cultural icon | 5 | 5 | 3 | 4 | 3 | 2 | 4 | 4 | 4 | **34** | All free; INPI 0 for the phrase; reads as dog-only |
| 6 | **SOS Bicho** | SOS+bicho | 4 | 5 | 4 | 4 | 3 | 5 | 3 | 4 | 2 | **34** | Domains free but `sosbichos` .com.br/.org.br taken; INPI "SOS BICHO URBANO" (NCL 45) in force |
| 7 | SOS Pet | Pet+SOS | 5 | 5 | 5 | 2 | 3 | 4 | 5 | 4 | 1 | 34 | .com.br/.org.br/.com taken; Instituto SOS PET Uberlândia |
| 8 | Salva Bicho | verb+bicho | 3 | 4 | 3 | 4 | 3 | 5 | 3 | 3 | 5 | 33 | All free; INPI 0; Play search shows rescue games |
| 9 | ResgataPet | verb+Pet | 4 | 3 | 3 | 4 | 2 | 4 | 5 | 3 | 5 | 33 | All free; "resgate" implies the user must rescue |
| 10 | Avisa Bicho | verb+bicho | 3 | 3 | 3 | 4 | 4 | 5 | 2 | 3 | 5 | 32 | Can be heard as slang "avisa, bicho!" ("tell me, dude") |
| 11 | Achei Bicho | verb+bicho | 2 | 4 | 3 | 4 | 3 | 5 | 3 | 3 | 5 | 32 | Two ch/x traps ("axei bixo"); Play search gives insect apps |
| 12 | Bicho na Rua | situational | 3 | 4 | 3 | 3 | 3 | 5 | 3 | 3 | 5 | 32 | Strong for strays, weak for lost owned pets |
| 13 | AchaPet | verb+Pet | 3 | 4 | 5 | 2 | 4 | 4 | 5 | 4 | 1 | 32 | **Taken**: same-concept app on both stores plus INPI "acha.pet" |
| 14 | SocorroPet | help+Pet | 4 | 3 | 3 | 4 | 3 | 4 | 5 | 2 | 4 | 32 | .com taken; BR domains free; INPI 0 |
| 15 | Avistei | verb | 4 | 3 | 5 | 3 | 2 | 3 | 5 | 4 | 2 | 31 | .com.br for sale; "avistar" is formal; no animal cue |
| 16 | VistoPet | verb+Pet | 3 | 3 | 4 | 4 | 2 | 4 | 3 | 3 | 5 | 31 | "visto" also means a travel visa |
| 17 | Rede Bicho | coined | 3 | 3 | 4 | 3 | 2 | 5 | 3 | 4 | 4 | 31 | INPI "REDE BICHOS" archived |
| 18 | Cadê Bicho | verb+bicho | 2 | 4 | 4 | 3 | 3 | 5 | 3 | 3 | 4 | 31 | Accent (cadê/cade/kd); INPI not checked |
| 19 | Patinha | animal word | 5 | 5 | 5 | 1 | 1 | 4 | 4 | 5 | 1 | 31 | 332 INPI processes; .com.br owned by a construction-materials store |
| 20 | BichoSOS | coined | 2 | 3 | 4 | 3 | 3 | 5 | 2 | 3 | 5 | 30 | `bichosos` misparses visually |
| 21 | CuidaPet (owner) | verb+Pet | 4 | 4 | 4 | 2 | 2 | 4 | 5 | 4 | 1 | 30 | **Blocked**: INPI "cuidapet" pending in NCL 09/42; CUIDA PET LTDA (NCL 44) |
| 22 | AcheiPet | verb+Pet | 3 | 4 | 4 | 2 | 3 | 4 | 5 | 4 | 1 | 30 | **Taken**: INPI "ACHEI PET" in force since 2013 plus NFC-tag product filings in 2026 |
| 23 | Acha Bicho | verb+bicho | 2 | 4 | 4 | 3 | 3 | 5 | 3 | 4 | 2 | 30 | .com.br (since 2012) and .com taken |
| 24 | Ajuda Bicho | verb+bicho | 3 | 3 | 3 | 3 | 3 | 5 | 2 | 3 | 5 | 30 | Play search gives 3 jogo-do-bicho apps; can be heard as "ajuda, bicho!" |
| 25 | Bicho Achado | situational | 3 | 3 | 3 | 4 | 2 | 5 | 3 | 2 | 5 | 30 | Covers "found" only |
| 26 | Socorro Bicho | help+bicho | 3 | 3 | 2 | 3 | 3 | 5 | 3 | 2 | 5 | 29 | Long; emergency only |
| 27 | EncontraPet (owner) | verb+Pet | 4 | 3 | 3 | 2 | 3 | 4 | 5 | 3 | 1 | 28 | **Taken**: Play app "EncontraPet" plus live encontrapet.com.br |
| 28 | Achei | verb | 3 | 5 | 5 | 1 | 2 | 3 | 4 | 4 | 1 | 28 | achei.com.br registered since 1996; too generic |
| 29 | Vi um Bicho | verb phrase | 3 | 4 | 4 | 2 | 3 | 5 | 2 | 3 | 2 | 28 | Echoes BichoAí's tagline; Play search gives Jogo do Bicho first |
| 30 | Focinho | animal word | 4 | 4 | 5 | 2 | 1 | 3 | 4 | 4 | 1 | 28 | Often misspelled "fucinho"; domains taken |
| 31 | Faro | animal word | 4 | 4 | 5 | 1 | 2 | 3 | 4 | 4 | 1 | 28 | Faro is a city in Portugal; dog connotation |
| 32 | Caramelo | cultural icon | 5 | 5 | 4 | 1 | 1 | 2 | 4 | 5 | 1 | 28 | All TLDs taken; 696 INPI processes; a "Caramelo Pet" crematorium app exists |
| 33 | Farejei | coined verb | 3 | 3 | 5 | 4 | 2 | 2 | 4 | 3 | 2 | 28 | .com.br/.com taken; dog-only (sniffing) |
| 34 | MapaPet | coined | 4 | 3 | 5 | 2 | 2 | 4 | 4 | 3 | 1 | 28 | .com.br/.com taken |
| 35 | RastroPet | animal word+Pet | 4 | 3 | 4 | 2 | 2 | 4 | 4 | 3 | 1 | 27 | **Taken**: RastroPET GPS collar brand |
| 36 | PetPerdido | situational | 5 | 4 | 3 | 2 | 2 | 4 | 4 | 2 | 1 | 27 | .com.br taken since 2018 |
| 37 | Bicho Perdido | situational | 3 | 4 | 2 | 3 | 2 | 5 | 3 | 2 | 2 | 26 | Live bichoperdido.com.br (2026) |
| 38 | Vira-lata | cultural icon | 3 | 5 | 4 | 2 | 1 | 2 | 3 | 4 | 1 | 25 | Hyphen; all TLDs taken; dog-only |

### Inferences
- **Why HF favors "Alerta":** "Alerta" works for both use cases ("alerta: cachorro ferido na rua X" and "alerta: gato visto na praça"). "SOS" signals an emergency, so a passer-by may feel that a healthy stray they merely saw isn't worth an "SOS". The sightings-to-chains feature depends on low-stakes posting, so this matters.
- **Spelling traps:**
  - "bicho" is commonly written "bixo" in informal Brazilian Portuguese. "Bixo" is also university slang for a freshman.
  - "achei" can become "axei".
  - "focinho" can become "fucinho".
  - "cadê" carries an accent.
  - Names built only from a-l-e-r-t-a / s-o-s / p-a-t-i-n-h-a / c-a-r-a-m-e-l-o have no ch/x/ç/ss ambiguity at all.
  - These are my observations of common usage; I have no frequency source.
- **"Bicho" also works as slang:** It is a vocative meaning "dude/mate" ("pô, bicho!"). Imperative-verb combinations ("Avisa Bicho", "Ajuda Bicho", "Salva Bicho") can therefore be heard as "tell/help/save, dude!". "Alerta Bicho" and "SOS Bicho" are less exposed because they read as noun phrases. This is my judgment and is unsourced.
- **"Bicho" invites off-scope reports:** It also covers pests (snakes, scorpions, rats, insects). A civic map labeled "bicho" may attract off-scope reports such as "tem um bicho aqui" for a scorpion. That would need copy and moderation guardrails.
- **"Vira-lata" connotation:** It has historically carried a pejorative sense (Nelson Rodrigues' "complexo de vira-lata"), even though "vira-lata caramelo" is now affectionate. This is my judgment and is unsourced.

### Gaps
- None of the names has been tested with users, for example by dictating them in a voice note to low-literacy users and checking the spelling. This is the cheapest experiment to resolve the "bicho vs patinha" tie.
- No regional slang check by native speakers from the North and Northeast was possible.

---

## Q5. Ranked top 5 with rationale

### Takeaway
**1. Alerta Bicho, 2. Alerta Patinha, 3. SOS Patinha, 4. SOS Caramelo, 5. SOS Bicho.**

Both owner suggestions should be dropped:
- **CuidaPet:** INPI applications in software classes 09/42 are pending, and it says "care", not "find".
- **EncontraPet:** A same-named lost-pet app and website already launched in 2026.

AlertaPet would rank first on fit (36/45), but only if the dormant alertapet.com.br (held since 2020) can be bought.

### Cited Findings
1. **Alerta Bicho (35/45).** It is the only top name that covers both use cases (an emergency and a mere sighting) and every species. "Bicho" is the cross-class word for any animal, including strays and ferals that are nobody's "pet".
   - Availability is the cleanest of any candidate. alertabicho, alertabichos and alertabixo are all 404 on .com.br/.org.br/.app.br/.com ([RDAP](https://rdap.registro.br/domain/alertabicho.com.br), [Verisign](https://rdap.verisign.com/com/v1/domain/alertabicho.com)).
   - INPI returned 0 processes, and no app has this name.
   - Costs: the "bixo" misspelling (cheap to cover by registering `alertabixo`), jogo-do-bicho and insect noise in app-store search ([Play search](https://play.google.com/store/search?q=alerta%20bicho&c=apps&hl=pt_BR&gl=BR)), and a resemblance to the wildlife app "Alerta Animal" ([listing](https://play.google.com/store/apps/details?id=br.com.alerta.animal.rs)).
   - "Posta no Alerta Bicho" and "manda pro Alerta Bicho" work naturally on WhatsApp.
2. **Alerta Patinha (35/45).** It keeps the "Alerta" advantage for both use cases and swaps "bicho" for a word with zero spelling ambiguity and no gambling or insect connotations.
   - All 8 domain variants (singular and plural) are free ([RDAP](https://rdap.registro.br/domain/alertapatinha.com.br)).
   - None of the 332 INPI "patinha" processes is an alert or SOS mark.
   - Costs: at 13 characters it is the longest of the shortlist. "Patinha" leans toward dogs and cats (fine for about 95% of cases, weaker for horses and birds). It also sits in a crowded "Patinhas…" NGO naming space ([A Gazeta](https://www.agazeta.com.br/hz/pet/em-dificuldades-ong-do-es-que-cuida-de-mais-de-100-animais-busca-novo-espaco-0424); [O Imparcial](https://oimparcial.com.br/cidades/2019/12/5-ongs-para-adotar-animais-de-estimacao-em-sao-luis/5/)), so it may be read as "one more protection group" rather than a national civic platform.
3. **SOS Patinha (35/45).** It is the warmest and most memorable, and it passes the voice-note test except for singular vs plural. It is short as a contact name.
   - The INPI precedents are dead: "S.O.S. PATINHA" (902681753) is extinct and "SOS PATINHAS" (928580741) is archived.
   - Costs: sospatinhas.com.br is already registered ([RDAP](https://rdap.registro.br/domain/sospatinhas.com.br)), so plural typos leak traffic. "SOS" frames every post as an emergency, which works against casual sighting reports, the raw material for the "chains".
4. **SOS Caramelo (34/45).** It has the strongest cultural hook (the vira-lata caramelo icon) and perfect spelling: s-o-s c-a-r-a-m-e-l-o.
   - All domains are free ([RDAP](https://rdap.registro.br/domain/soscaramelo.com.br)), and INPI has no "SOS Caramelo" among 696 "caramelo" processes.
   - Costs: it reads as dog-only, leaving out cats, a core half of the problem. "Caramelo" is also a crowded mark, with apps such as "Caramelos: Rede Social Pet" and a "Caramelo Pet" pet crematorium ([iTunes query](https://itunes.apple.com/search?country=br&entity=software&limit=6&term=caramelo)).
   - Better used as a **mascot or campaign name** than as the platform name. That last point is my inference.
5. **SOS Bicho (34/45).** It is the punchiest and most species-neutral option, with all four singular domains free ([RDAP](https://rdap.registro.br/domain/sosbicho.com.br)).
   - It ranks last because of legal and leak friction: INPI 925611751 "SOS BICHO URBANO" is listed as in force in class 45, and 910384452 "Clínica Veterinária SOS Bichos" is pending in class 44. sosbichos.com.br and sosbichos.org.br are taken ([RDAP](https://rdap.registro.br/domain/sosbichos.com.br)), and local NGOs such as "SOS Bichos da Vila" (SC) already use the name ([ALESC](https://portalelegis.alesc.sc.gov.br/documentos/6Y1Yv)).
   - The same jogo-do-bicho and insect noise as Alerta Bicho applies.

**Honorable mentions:**
- **AlertaPet:** the best fit, but the domain must be acquired ([RDAP](https://rdap.registro.br/domain/alertapet.com.br)).
- **Salva Bicho:** all free, but "rescue" framing.

**Avoid:** CuidaPet, EncontraPet, AcheiPet, AchaPet, Vi um Bicho (echoes BichoAí's tagline), RastroPet, Caramelo and Patinha on their own.

### Inferences
- **The decision between #1 and #2 to #3 is a product-strategy call:**
  - "Bicho" maximizes inclusivity and matches stray/feral reality and street vocabulary, at the cost of spelling and connotation noise.
  - "Patinha" maximizes warmth and spelling safety, at the cost of distinctiveness and non-dog/cat coverage.
- **A hybrid worth considering:** **Alerta Bicho** as the platform name with **Caramelo** as the mascot. That captures the national icon without making the brand dog-only.
- **Defensive set for #1 (if chosen):**
  - alertabicho .com.br/.org.br/.app.br/.com
  - alertabichos.com.br
  - alertabixo.com.br
  - All were 404 on 2026-10-21. Then file at INPI in classes 09, 42 and 45 promptly, because several same-concept products launched in 2026.
- **Key invariant:** The name must survive being dictated in a WhatsApp voice note and typed by someone with low literacy. "Alerta", "SOS", "patinha" and "caramelo" survive that. "Bicho" survives only if the "bixo" variants are owned.
- **Main failure mode:** Picking a "Pet" compound. Nearly all are already registered, apps already exist under them, and they mis-signal "owned pets" to an audience reporting strays.

### Gaps
- Instagram handles and hashtag volumes are unverified (login wall).
- INPI checks used the radical search only. A trademark attorney's phonetic search and an assessment of the "SOS BICHO URBANO" scope are needed before committing to any SOS name.
- No user testing has been done (dictation, spelling and comprehension) to break the tie between Alerta Bicho, Alerta Patinha and SOS Patinha.
