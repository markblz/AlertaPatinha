# Prior art (international + Brazilian) and Brazilian institutional, legal and usage context for a stray/lost-pet civic platform

Research date: 2026-10-21. All figures are dated where the source allows. "Inference" bullets are my reasoning, not sourced facts.

---

## 1. International prior art: models, scale, matching tech, business model, praise, criticism, failures

### Takeaway
The international market splits four ways: (a) free, nonprofit-funded aggregators with photo matching (Petco Love Lost, about 250k confirmed reunions by Apr 2026) that pull in posts from other networks (Nextdoor) and act as the official map for many US cities; (b) freemium alert networks that charge for "boosts" (PawBoost); (c) camera or surveillance networks (Ring Search Party, launched late 2025), which reach a lot of people quickly but drew a strong privacy backlash; (d) early facial-recognition apps (Finding Rover, about 2014–2016) that got press and then faded. Public-sector portals (Bogotá 2025) are usually simple bulletin boards with no verification. Scams that target owners of lost pets are a well-documented problem across the whole category.

### Cited Findings

**Petco Love Lost (US, nonprofit, free)**
- Database has reunited 250,000 lost pets (Apr 14, 2026 milestone) — [Pet Age](https://www.petage.com/?p=503153); repeated in [KDH News](https://kdhnews.com/online_features/health_and_wellness/250-000-lost-pets-reunited-lifesaving-national-nonprofit-helps-bring-lost-pets-and-their-families/article_a5bf2c78-2e5a-5f77-9291-20b350f6e451.html)
- Earlier milestones: 100,000th confirmed reunion — [AAHA](https://www.aaha.org/?p=33077); "more than 200,000 since 2021" — [Techstrong.ai](https://techstrong.ai/?p=44893)
- Petco Love's COO says a reunion counts only when the poster reports it manually, and estimates that only about one-third of reunions get confirmed. Real reunions are probably about 3× the reported figure, and the system has a feedback-loop problem. — [Techstrong.ai](https://techstrong.ai/?p=44893) / [AAHA](https://www.aaha.org/?p=33077) (via search summary)
- Photo matching reportedly uses up to 512 visual data points (fur pattern, facial structure, markings) and also matches on microchip ID. The shelter network is about 3,000 shelters. — [KDH News](https://kdhnews.com/online_features/health_and_wellness/250-000-lost-pets-reunited-lifesaving-national-nonprofit-helps-bring-lost-pets-and-their-families/article_a5bf2c78-2e5a-5f77-9291-20b350f6e451.html); [RH-SPCA / WHSV 2021](https://www.whsv.com/2021/04/23/rh-spca-adopts-petco-love-lost-facial-recognition-technology-to-help-reunite-lost-pets-with-their-owners/)
- Example of a long-tail success: a cat reunited after 103 days through AI photo matching — [CBS Texas](https://www.cbsnews.com/texas/video/ai-photo-matching-tool-reunites-north-texas-woman-with-her-cat-after-103-days)
- Shelters say it "does not replace microchipping" — [LifeLine Animal Project](https://lifelineanimal.org/petco-love-lost/)
- **Nextdoor integration (May 2024):** all pet-related Nextdoor posts are automatically included in Petco Love Lost search results — [Nextdoor blog](https://blog.nextdoor.com/2024/05/30/reunite-lost-pets-beyond-your-neighborhood-with-petco-love)
- City animal services adopt Petco Love Lost as their official lost/found map. Examples: Santa Barbara County (map integrated with Nextdoor) — [Edhat](https://www.edhat.com/news/county-healths-animal-services-debuts-new-lost-found-pet-map/); Sacramento (map integrated with Nextdoor and Ring) — [City of Sacramento](https://www.cityofsacramento.gov/community-development/animal-care/lost-and-found); Austin (scans public Nextdoor posts) — [Austin Animal Services](https://www.austintexas.gov/lost-a-pet); Midland TX — [NewsWest9](https://newswest9.com/article/news/local/midland-animal-services-partners-with-petco-love-lost-service-to-help-find-missing-pets/513-832b922a-b66f-4fd3-9c28-2529f0f43422)

**Ring "Search Party" (Amazon, US)**
- AI scans nearby outdoor Ring camera footage for dogs that match a lost-pet report (photo plus description). Each camera owner chooses whether to share a match. Rollout began in November (2025) in the US, with cats and other animals planned "at a later date". — [Tom's Guide](https://www.tomsguide.com/home/home-security/rings-new-search-party-feature-can-help-you-find-your-lost-dog-heres-how-it-works)
- Expanded on Feb 2, 2026 to all US users, including people with no Ring device — [Dataconomy](https://dataconomy.com/2026/02/03/ring-expands-ai-search-party-to-find-lost-dogs-nationwide/); [About Amazon](https://www.aboutamazon.com/news/devices/ring-search-party-for-dogs-united-states-missing-pets)
- Ring says it is reuniting "more than one lost dog a day" — [About Amazon](https://www.aboutamazon.com/news/devices/ring-search-party-for-dogs-united-states-missing-pets); 99 dogs as of about Feb 15, 2026 — [ChannelIAM (secondary)](https://en.channeliam.com/2026/02/15/amazon-ring-search-party-for-dogs-ai-feature/); see also [Ring blog](https://blog.ring.com/pets/how-search-party-for-dogs-is-reuniting-pets-with-their-owners/)
- Ring says more than 1 million lost/found pet reports were posted on its platform in the previous year — [Fox 5 NY](https://www.fox5ny.com/news/amazons-ring-ai-power-lost-dogs)
- **Backlash:** the Super Bowl 2026 ad (a lost dog found by a neighborhood network of AI cameras) was criticized as "sinister", with viewers asking whether the same system would track humans. Ring then ended its planned Flock Safety (law-enforcement footage) partnership. Ring's statement cited cost and did not mention the ad. — [ABC7](https://abc7news.com/post/ring-flock-partnership-amazon-scraps-surveillance-company-safety-super-bowl-commercial-backlash/18596207/); [Yahoo Tech](https://tech.yahoo.com/home/articles/amazon-ends-flock-partnership-backlash-172510856.html)
- Search Party is **enabled by default** (opt-out). EFF: "no one … will be safer in Ring's surveillance nightmare." — [Techdirt](https://www.techdirt.com/company/ring/)

**PawBoost (US, freemium)**
- Describes itself as an "AMBER Alert for lost pets". It claims more than 2 million pets reunited (unverified, self-reported). Trustpilot rates it about 4.9/5 on about 443 reviews. Praise centers on speed. Paid "boosts" are the main monetization users mention. It replies to 100% of negative reviews but often takes more than a month. — [Trustpilot](https://uk.trustpilot.com/review/pawboost.com?page=7); company profile [CB Insights](https://www.cbinsights.com/company/pawboost)

**Finding Rover (US, about 2014–2016)**
- Facial recognition from a frontal photo: 128 facial measurements. Claimed 15,000–18,000 reunions and more than 1M animals in its database (2015-era reports). Shelters adopted it, e.g. Chicago and Ventura County in 2020. — [ABC7](https://abc7.com/1082495); [WTTW Chicago](https://news.wttw.com/node/27331); [Ventura County Animal Services PDF, 2020](https://animalservices.venturacounty.gov/wp-content/uploads/2020/08/VCAS_Finding_Rover.pdf); [Star Tribune](https://m.startribune.com/phone-app-can-recognize-missing-dogs-faces/298624331/)

**Public-sector precedent (Latin America): Bogotá, Colombia**
- Launched by the Instituto Distrital de Protección y Bienestar Animal (IDPYBA), announced Aug 19, 2025, live Aug 22, 2025: "Perros y gatos buscan su hogar", a "digital bulletin board" of lost/found reports with photo, place/date, description and reporter contact. IDPYBA explicitly **does not verify** reports and **does not intermediate** contact. It has no map and no matching. Future plans: filters by locality, reunion reporting, links to vets/shelters. — [Infobae](https://www.infobae.com/colombia/2025/08/19/distrito-lanzo-portal-web-para-mascotas-perdidas-en-bogota-asi-funciona/)

**Cross-cutting failure mode: scams that target owners of lost pets**
- A widespread pattern: a fake "finder" asks the owner for a 6-digit code "to verify" them. The code is actually a Google Voice (or account-recovery/2FA) code used to hijack the number or accounts. Ransom or "reward" demands via gift cards, crypto, Venmo or CashApp are also common, and scammers impersonate shelters to request "surgery" payments. Advice from these sources: keep identifying marks out of public posts so real finders can be verified, use email instead of a phone number, ask for a photo or video call. — [BBB via News5 Cleveland](https://www.news5cleveland.com/money/consumer/cleveland-bbb-issue-warning-of-missing-pet-scam-using-google-voice); [KTNV](https://www.ktnv.com/news/las-vegas-pet-owners-targeted-by-lost-pet-recovery-scam); [CBS New York](https://www.cbsnews.com/amp/newyork/news/scammers-target-long-island-families-asking-for-help-finding-lost-pets-on-social-media); [Bitdefender (AI variant)](https://www.bitdefender.com/en-au/blog/hotforsecurity/missing-pet-ai-scam)

### Inferences
- The winning international pattern is to **aggregate and integrate**, not to build a standalone silo. Petco Love Lost grew by ingesting Nextdoor posts and becoming the cities' official map. A Brazilian equivalent would ingest from or interoperate with WhatsApp, Instagram and Facebook, SinPatinhas and CCZs.
- Reunion metrics are badly undercounted (about one-third confirmed), so a "close the chain" step that asks people to confirm the reunion (and rewards them for it) is needed both to measure impact and to keep stale reports off the map.
- Ring shows that "AI + crowd cameras + map" reaches a lot of people fast but is perceived as surveillance. Opt-out defaults and links to law enforcement were the flashpoints. A Brazilian civic platform that shows exact locations should make precision opt-in and explain itself carefully.
- Bogotá's no-verification, no-intermediation bulletin board is the minimum a government can launch. It leaves open everything about trust, fraud, staleness and matching, which is where a civic platform can add value.
- Scam resistance should be designed in from the start: in-platform contact relay (masked numbers), withholding of verification attributes, and warnings about "codes".

### Gaps
- Could not verify Finding Rover's current operating status (shutdown or acquisition). Coverage stops around 2016–2020.
- No reliable 2025–2026 data found for Pet FBI (status unknown), 24Petwatch (scale or business-model criticism; a 2025 PetPlace press release claiming a 58% July-4 spike and "only 45% of US pets microchipped / 60% of chips registered" surfaced in search, but I did not retrieve the primary URL), Petfinder's lost-and-found role, or the Citizen app's pet features.
- No independent accuracy benchmarks for Petco Love Lost or Ring matching. All accuracy claims come from vendors.
- No Ring Search Party reunion count after Feb 2026, and no confirmation that the cat expansion has happened.

---

## 2. Brazilian prior art: existing apps and sites, status, features, and why none became the default

### Takeaway
Brazil has many small lost-pet, adoption and rescue initiatives: startup apps (Pupz 2022, ILY 2023), newsroom- and NGO-run Instagram/WhatsApp efforts, municipal complaint apps, crisis tools built during the 2024 Rio Grande do Sul floods, and dozens of academic prototypes. **I found no national-scale, dominant lost/stray-pet platform.** The real "default" remains Facebook groups, Instagram and WhatsApp. The many TCC (undergraduate thesis) and student prototypes show that people keep having the idea, but almost none ship and last.

### Cited Findings

**Startup and private apps**
- **Pupz (2022):** free Android/iOS app from a pet-products company. Registration takes 6 face photos of the animal for AI facial recognition. The CEO claims >94% accuracy (company claim, not independently verified). It also sells GPS/QR collars and shows a lost-and-found list within a chosen radius. — [Mobile Time](https://www.mobiletime.com.br/?p=698265); [BNews 2022](https://www.bnews.com.br/noticias/bnews-pet/app-gratuito-ajuda-localizar-pets-perdidos-saiba-como-usar.html); [Agora RN](https://agorarn.com.br/ultimas/aplicativo-encontra-pets-perdidos-com-reconhecimento-facial-e-chips-em-coleiras/); [Correio Braziliense](https://blogs.correiobraziliense.com.br/maisbichos/app-faz-reconhecimento-facial-de-pets/amp/). Current status: unknown.
- **ILY – I Love You, Pet (Belo Horizonte, Jan 2023):** free. Owners profile their pets. When a pet goes missing, registered "protetores" in nearby CEPs (postal codes) get an alert, **delivered via WhatsApp**. Profiles are **validated by WhatsApp number** to deter fake accounts, and the platform says it does not share personal data between users. — [Estado de Minas](https://www.em.com.br/app/noticia/gerais/2023/01/24/interna_gerais,1448600/plataforma-mineira-ajuda-a-encontrar-pets-perdidos.shtml). Current status: unknown.
- **Adoption-focused:** Adota Pet GO (Brasília; geolocated listings) — [Correio Braziliense](https://blogs.correiobraziliense.com.br/maisbichos/app-de-brasilia-facilita-adocao/); PetPonto (NGO and adopter geolocation, celebrity ambassador) — [A Gazeta](https://www.agazeta.com.br/revista-ag/pet/quer-adotar-um-pet-estes-sites-e-aplicativos-podem-te-ajudar-0921); Vivo Valoriza (2021, adoption via the Meu Vivo app, 20+ partner NGOs, SP/RJ/BH only) — [Meio & Mensagem](https://www.meioemensagem.com.br/marketing/vivo-cria-movimento-para-adocao-de-pets)

**Crisis precedent: Rio Grande do Sul floods (May 2024)**
- A couple in Canoas built an AI tool that matches shelter animals with owners. It used Monday.com as the database and an AI model from Pix Force. Owners and shelters filled in separate forms with photos plus name, sex, color and size. The first match came within days. — [TecMundo](https://www.tecmundo.com.br/software/282908-rs-casal-lanca-sistema-ia-match-entre-pets-perdidos-tutores-veja.htm); [Olhar Digital](https://olhardigital.com.br/2024/05/16/pro/ia-ajuda-tutores-a-encontrar-animais-desaparecidos-apos-enchentes-no-rs/)
- Scale: about 10k animals rescued by mid-May — [Olhar Digital](https://olhardigital.com.br/2024/05/16/pro/ia-ajuda-tutores-a-encontrar-animais-desaparecidos-apos-enchentes-no-rs/); "RS has 20k animals in shelters", with castration and microchipping announced — [Diário de Pernambuco](https://www.diariodepernambuco.com.br/noticia/brasil/2024/05/rs-tem-20-mil-animais-em-abrigos-e-anuncia-castracao-e-microchipagem.html)
- Parallel efforts: the state launched a "Plano Estadual de Ação de Resposta à Fauna" on May 31, 2024, alongside a volunteer-built map of sheltered animals filterable by address — [Agência Brasil](https://agenciabrasil.ebc.com.br/geral/noticia/2024-05/rio-grande-do-sul-lanca-plano-de-ajuda-animais); São Paulo city hall built its own registry for about 2k animals housed in Canoas — [Prefeitura SP](https://prefeitura.sp.gov.br/w/prefeitura-cria-plataforma-para-cadastrar-animais-resgatados-nas-enchentes-do-rs); the NGO Pets RS ran a site with search by neighborhood or name, plus Instagram — [Canaltech](https://canaltech.com.br/redes-sociais/chuvas-no-rs-redes-sociais-ajudam-a-encontrar-animais-perdidos-288373/)

**Media, NGO and government channels**
- "Cadê meu pet?" by the newspaper Folha Vitória (ES) spreads cases through Instagram and the paper's WhatsApp news communities — [Folha Vitória](https://www.folhavitoria.com.br/geral/cade-meu-pet-voce-viu-o-tutor-cao-foi-encontrado-perdido-na-serra/)
- Jundiaí (SP) municipal app (2018) takes anonymous mistreatment complaints with photo and **exact location**, routed to the city's animal-welfare department — [Prefeitura de Jundiaí](https://jundiai.sp.gov.br/noticias/2018/12/19/app-da-prefeitura-ajuda-a-denunciar-maus-tratos-contra-animais/)
- Colab (a civic-tech platform used by municipalities): photo-based zeladoria (urban-maintenance) requests with public lookup by address, e.g. Santo André — [DGABC](https://www.dgabc.com.br/Noticia/2915516/sto-andre-lanca-aplicativo-de-zeladoria); Serra (ES) — [ES Hoje](https://eshoje.com.br/?p=877058). I could not confirm a dedicated animal-abandonment category.
- DF "Cadastro Mais Protetor" (Sepan-DF ordinance, June 2025) maps volunteer protectors and civil-society groups to inform policy. It is a registry, not a public app. — [Jornal de Brasília](https://jornaldebrasilia.com.br/estilo-de-vida/noticiaanimal/cadastro-mais-protetor-vai-mapear-atuacao-de-protetores-de-caes-e-gatos-no-df/)
- Porto Alegre created a **Cadastro de Animal Comunitário** (Feb 2026) to map community dogs for health and vaccination care — [Prefeitura de Porto Alegre](https://prefeitura.poa.br/smgg/noticias/prefeitura-fortalece-politica-de-protecao-caes-comunitarios-por-meio-de-cadastro)
- "SINA-PET", a citizen legislative idea for a national unified Gov.br platform registering animals held by NGOs and zoonoses centers, closed without enough support — [Senado e-Cidadania](https://www12.senado.leg.br/ecidadania/visualizacaoideia?id=211019)

**Academic prototypes (evidence of recurring, rarely shipped ideas)**
- Many TCC and student apps for lost, found, stray or adoption: Snoutsee (2022), a localization and adoption system (2024), Aumigos (2025), Animals Life (2025), Pet Hood, an IFS Sergipe project (2025), Adog (CEFET-MG), IPet (connects NGOs and donors) — [CPS/Snoutsee](https://ric.cps.sp.gov.br/bitstream/123456789/12878/1/tecnico_desenvolvimento_sistemas_2022_2_gabriela_leal_tavares_snoutsee.pdf); [CPS/Aumigos](https://ric.cps.sp.gov.br/bitstream/123456789/44332/1/etimdesenvolvimentodesistemas_2025_2_agathalopes_aumigos.pdf); [CPS/Animals Life](https://ric.cps.sp.gov.br/bitstream/123456789/44148/1/informatica_2025_2_beatrizespindolabarbosa_animalslifeprojetodeunifica%c3%a7%c3%a3o.pdf); [Uniube/Pet Hood](https://repositorio.uniube.br/bitstream/123456789/1808/1/Pet%20Hood%20%e2%80%93%20A%20rede%20social%20voltada%20para%20pets.pdf); [IF Goiano/IPet](https://repositorio.ifgoiano.edu.br/bitstream/prefix/2277/1/ARTIGO_IPET_ROBERTO_VALTENIS.pdf)

### Inferences (why nothing became the default)
- **Cold start is local, and so are the network effects:** a lost-pet tool is useful only if enough nearby people are already watching. Facebook groups and WhatsApp already have that audience. Standalone apps (Pupz, ILY) had to win it neighborhood by neighborhood.
- **Install friction against WhatsApp-native behavior:** ILY's choice to deliver alerts and validate users through WhatsApp suggests that builders already saw that people won't open an extra app. With 92% of internet users on instant messaging (see §4), intake and alerts belong in WhatsApp.
- **No sustainable model:** the private apps were tied to selling hardware (Pupz collars) or had no visible revenue. Adoption platforms leaned on corporate CSR (Vivo). None had the endowment-style funding that Petco Love provides.
- **No institutional anchor:** none were integrated with CCZs or SinPatinhas, so they never became the "official" channel (unlike the US cities that adopted Petco Love Lost).
- **Crisis tools appear and vanish:** the RS 2024 flood tools were built in days on generic SaaS. The demand was proven, but there was no persistent infrastructure to reuse. A standing platform with a "crisis mode" would fill that gap.

### Gaps
- No app-store download counts, ratings or current status (active or dead) were retrievable for Pupz, ILY, PetPonto or Adota Pet GO. They need manual Play Store and App Store checks.
- I could not identify the biggest Brazilian adoption portal (e.g., any Petlove, Petz or Cobasi adoption programs). Not covered by these searches.
- A Bem Paraná article on a "real-time alerts" lost-pet platform surfaced but was not read — [Bem Paraná](https://www.bemparana.com.br/animais/plataforma-ajuda-na-busca-por-animais-perdidos-com-alertas-em-tempo-real/amp/)

---

## 3. SinPatinhas (federal registry) and state and municipal registration and castration programs

### Takeaway
SinPatinhas (MMA, launched April 2025) is a free, voluntary, Gov.br-authenticated national registry. It issues an "RG Animal" with a QR code, optionally stores a microchip number, supports electronic transfer of responsibility, and lets the government "negativar" (blacklist) people responsible for mistreatment. It grew from about 620k animals (May 2025) to 1.31M at one year (Apr 2026) and about 1.8M (data to Sep 10, 2026). That is still only about 2% of Brazil's roughly 93M owned dogs and cats. **I found no public API or open-data release.** It is effectively mandatory where federal castration or microchipping money is used (via ProPatinhas).

### Cited Findings
- Launched by the federal government in April 2025 — [O Hoje, 23/04/2025](https://ohoje.com/2025/04/23/governo-federal-lanca-sinpatinhas-sistema-nacional-de-registro-de-animais/)
- Access: free, voluntary, through sinpatinhas.mma.gov.br with a Gov.br login (silver or gold level, CPF required) — [CNN Brasil](https://www.cnnbrasil.com.br/politica/sinpatinhas-como-cadastrar-caes-e-gatos-no-programa-de-rg-para-pets/)
- **RG Animal:** a unique national ID number with a QR code for the collar. Anyone who finds the animal can scan it to reach the owner's authorized contact. — [Congresso em Foco](https://congressoemfoco.com.br/noticia/107835/sinpatinhas-entenda-o-novo-rg-animal-lancado-pelo-governo-federal); [CNN Brasil](https://www.cnnbrasil.com.br/politica/rg-dos-pets-como-fazer-e-para-que-serve/)
- **Data fields:** owner identity, CPF, address. Animal origin and characteristics, breed, sex, real or presumed age, vaccines, diseases and treatments. Microchip number is **optional** ("poderá ser incluído"). — [Congresso em Foco](https://congressoemfoco.com.br/noticia/107835/sinpatinhas-entenda-o-novo-rg-animal-lancado-pelo-governo-federal). Conflict: a 2026 column says registration "exige foto dos animais e cadastro de microchip" — [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1). Most sources say the microchip is optional and a photo is expected.
- **Features listed:** RG Animal, a national health card, QR-code ID, **lookup by microchip**, **electronic transfer of responsibility**, and **"negativação" of people responsible for mistreatment**. Described as a "base pública e unificada" integrating ID, health and management data. — [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1)
- Owners must report a sale, donation or death of the animal — [Congresso em Foco](https://congressoemfoco.com.br/noticia/107835/sinpatinhas-entenda-o-novo-rg-animal-lancado-pelo-governo-federal)
- MMA director Vanessa Negrini: the microchip only identifies and does not track — [CNN Brasil](https://www.cnnbrasil.com.br/politica/rg-dos-pets-como-fazer-e-para-que-serve/) (via search summary)
- **Mandatory for anyone receiving public funds** for castration or microchipping (municipalities and NGOs funded by parliamentary amendments) — [CNN Brasil](https://www.cnnbrasil.com.br/politica/rg-dos-pets-como-fazer-e-para-que-serve/); [Congresso em Foco](https://congressoemfoco.com.br/noticia/107835/sinpatinhas-entenda-o-novo-rg-animal-lancado-pelo-governo-federal)
- **ProPatinhas** ("Programa Nacional de Proteção e Manejo Populacional Ético de Cães e Gatos"): voluntary federal financial and technical support to states and municipalities for sterilization, microchipping and registration — [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1)
- **Adoption numbers over time:**
  - About 620k animals (end of May 2025) — [O Cafezinho](https://www.ocafezinho.com/2025/05/29/mais-de-620-mil-animais-ja-tem-rg-veja-como-cadastrar-seu-pet-no-sinpatinhas/amp/)
  - First anniversary (MMA, Apr 2026): **1,305,529 animals** (795,859 dogs, 61%; 509,670 cats, 39%), **1,044,385 tutors** (individuals and legal entities), close to 1,000 civil-society organizations, 2,697 vets, present in **98.3% of municipalities** — [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1)
  - **About 1.8M animals** (federal data to Sep 10, 2026): more than 1M dogs and 743,367 cats. SP leads with 538,059, then RJ and PR. — [Portal de Prefeitura (13/10/2026)](https://portaldeprefeitura.com.br/pernambuco/pernambuco-animais-cadastrados-sinpatinhas-castracao-microchipagem/634008/); [A Crítica MS](https://acritica.net/cidades/ms-animais-cadastrados-sinpatinhas/) (press reports, not an MMA primary source)
  - State examples: Pernambuco 51,984 animals and 42,214 tutors — [Portal de Prefeitura](https://portaldeprefeitura.com.br/pernambuco/pernambuco-animais-cadastrados-sinpatinhas-castracao-microchipagem/634008/); Ceará about 48k (57% dogs) — [O Povo, 18/04/2026](https://www.opovo.com.br/noticias/ceara/2026/04/18/amp/de-mel-a-simba-os-nomes-favoritos-dos-pets-no-ceara.html); Minas Gerais 93,550 at one year — [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1)
- **Municipal integration example:** Campinas castration drive (Apr 2026) requires SinPatinhas registration first, then scheduling on a separate municipal system (castrapet.com.br). Eligible: dogs and cats aged 6 months to 8 years. — [Correio da Manhã](https://www.correiodamanha.com.br/nacional/sao-paulo/campinas/2026/04/amp/281693-mutirao-de-castracao-em-campinas-utiliza-sistema-federal-sinpatinhas-para-cadastro-de-pets.html)
- Juiz de Fora joined at launch and plans phase 2 (castration and zoonoses projects). Its municipal Censo Municipal de Animais Domésticos law (Lei 14.295/2021) has produced no published results. — [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1)
- Porto Alegre Cadastro de Animal Comunitário (Feb 2026) — [Prefeitura POA](https://prefeitura.poa.br/smgg/noticias/prefeitura-fortalece-politica-de-protecao-caes-comunitarios-por-meio-de-cadastro); DF Cadastro Mais Protetor (June 2025) — [Jornal de Brasília](https://jornaldebrasilia.com.br/estilo-de-vida/noticiaanimal/cadastro-mais-protetor-vai-mapear-atuacao-de-protetores-de-caes-e-gatos-no-df/)

### Inferences
- Coverage is about 1.8M out of about 93M owned dogs and cats (62.2M + 30.8M, Abinpet/IPB, §4), so about 2%. Most found animals will **not** be in SinPatinhas, and photo re-ID plus crowd sightings remain necessary.
- SinPatinhas registers *owned* animals and their tutors. Strays and community animals fall mostly outside it, except where NGOs or municipalities register them to get ProPatinhas funds. That leaves room for a complementary "unowned / community animal" layer, which could later link to SinPatinhas IDs (QR / RG Animal / microchip lookup).
- Integration hooks to explore: (1) scan the RG Animal QR code or enter the number on a found animal to route to the owner; (2) a "registered in SinPatinhas?" field on reports; (3) nudge reunited owners to register; (4) feed castration-campaign info by location. All of these depend on MMA offering an API or agreement, which I did not find.
- The "negativação" list of abusers is sensitive: a civic platform should never try to mirror or publish it (LGPD and defamation risk, see §5).

### Gaps
- **No public API, open-data set, dashboard or data-sharing agreement** for SinPatinhas was found. Ask MMA directly (Lei de Acesso à Informação requests or dados.gov.br).
- I could not read the official MMA/gov.br pages directly, so totals rely on press reports citing federal data.
- National castration totals under ProPatinhas and its funding amounts were not found.
- State-level registries (e.g., SP state, RJ) and their relationship to SinPatinhas were not covered.

---

## 4. Brazil numbers with provenance

### Takeaway
The widely cited "30 million abandoned animals (WHO)" figure **has no traceable WHO primary source**. It circulates through blogs and student papers, citing Jusbrasil (2013) or "OMS 2014" second-hand, and should not be used. The best available figure is Instituto Pet Brasil's estimate of about 4.8M dogs and cats "in vulnerability" (2024), but its definition and changing species split need care. Device and connectivity context is mobile-only, Android-heavy, prepaid and data-constrained, and WhatsApp-dominant.

### Cited Findings

**The "30 million" figure**
- A 2024 IFAP academic paper notes that the source and the blogs replicating it never cite a date or WHO document — [Queiroz & Silva 2024, IFAP](https://repositorio.ifap.edu.br/jspui/bitstream/prefix/920/1/QUEIROZ%2c%20SILVA%20%282024%29%20-%20Diagn%c3%b3stico%20em%20prol.pdf)
- A Guarulhos paper traces it to a 2013 Jusbrasil page — [Semana do Conhecimento Guarulhos](https://semanadoconhecimento.guarulhos.sp.gov.br/index.php/SDC/article/download/332/295/930); a Unijuí paper cites "OMS, 2014" only via MAPAA 2015 — [Unijuí](https://publicacoeseventos.unijui.edu.br/index.php/moeducitec/article/view/7447/6198)
- Even the CRMV-SP Dezembro Verde campaign coverage concedes "não há estatísticas oficiais" before repeating the WHO attribution (20M dogs + 10M cats) — [Portal do Trânsito](https://www.portaldotransito.com.br/noticias/conscientizacao/comportamento/dezembro-verde-alerta-sobre-maus-tratos-e-abandono-de-animais/)

**Instituto Pet Brasil (IPB) estimates**
- 2018 census: about 370 NGOs caring for about 172k animals (165,200 dogs, 96%; 6,883 cats, 4%). About 3.9M animals (5% of dogs and cats) in vulnerability. — [Câmara dos Deputados enquete](https://www.camara.leg.br/enquetes/2265648); [Câmara Municipal SP parecer](https://www.saopaulo.sp.leg.br/iah/fulltext/parecer/SAUDE1151-2023.pdf)
- Earlier series (2020 base): 8.8M vulnerable, made up of 6.1M dogs (69.4%) and 2.7M cats (30.6%) — [Correio Braziliense](https://blogs.correiobraziliense.com.br/maisbichos/pandemia-aumentou-vulnerabilidade-de-animais/) (via search summary)
- **2024 survey (closed Nov 2024, with Abinpet):** about **4.8M** dogs and cats in vulnerability, about **201k** under the care of NGOs or independent protectors, reported as 92% cats and 8% dogs — [CNN Brasil](https://www.cnnbrasil.com.br/nacional/quase-5-milhoes-de-pets-estao-em-situacao-de-vulnerabilidade-no-brasil/); about 400 formal NGOs — [Band, Jan 2026](https://www.band.com.br/pets/noticias/brasil-tem-recorde-de-denuncias-de-violencia-contra-animais-202601311457)
- IPB definition of "vulnerable": animals owned by families below the poverty line, or living on the street but receiving some community care. NGO-held animals are counted separately. — [CNN Brasil](https://www.cnnbrasil.com.br/nacional/quase-5-milhoes-de-pets-estao-em-situacao-de-vulnerabilidade-no-brasil/)

**Pet population**
- Abinpet/IPB (2024 release): **160.9M pets** (155.7M in 2022), made up of **62.2M dogs**, **30.8M cats**, 42.8M ornamental birds and 22.3M fish — [CartaCapital](https://www.cartacapital.com.br/?p=442972); [Panorama PetVet](https://panoramapetvet.com.br/?p=14658); [Abinpet deck 2024](https://abinpet.org.br/wp-content/uploads/2024/10/abinpet_apresentacao_dados_mercado_2024_completo_draft5.pdf). A conflicting figure attributed to "IPB 2024" gives about 170M, with 58.1M dogs and 31.8M cats — [Paraíba Business](https://paraibabusiness.com.br/potencia-pet-mercado-brasileiro-de-animais-de-estimacao-mostra-resiliencia-e-sofisticacao-movimentando-r-60-bi/)
- Pet-sector revenue R$75.4bn in 2024 (+9.6%) — [Central do Varejo (Abinpet)](https://centraldovarejo.com.br/mercado-pet-crescimento-e-tendencias-e-do-setor/?amp=1)
- **IBGE PNS 2019:** 46.1% of households had at least one dog and 19.3% at least one cat. 39.4M households had a dog or cat. 72.0% had all of them vaccinated against rabies in the past 12 months (75.4% in 2013). — [IBGE PNS 2019 indicator sheet](https://anda.ibge.gov.br/media/com_mediaibge/arquivos/a09d971b8c3d3aebfe7e686cc221bc3d.pdf)

**Connectivity and devices (TIC Domicílios 2025, published 2026)**
- 157M internet users in 2025 (163M, 88%, under the expanded concept). **99%** of users access via mobile phone, and **65% exclusively via phone** (87% in classes DE, 83% rural). — [Cetic.br TIC Domicílios 2025 executive summary](https://www.cetic.br/media/docs/publicacoes/2/pt-br/20260511173151/tic_domicilios_2025_resumoexecutivo%20pt.pdf); [principais resultados](https://cetic.br/media/analises/tic_domicilios_2025_principais_resultados.pdf)
- **52%** of phone owners are on prepaid plans. **39%** (about 64M people) ran out of their data allowance before the end of the period at least once in the past 3 months. 47% of non-users cite lack of skill. — [Cetic.br executive summary](https://www.cetic.br/media/docs/publicacoes/2/pt-br/20260511173151/tic_domicilios_2025_resumoexecutivo%20pt.pdf)
- **Instant messaging (e.g., WhatsApp): 92% of internet users** (class A 99%, B 97%, C 93%, DE 84%; urban 92%, rural 85%). Social networks 81%, voice/video calls 80%, email 59%. — [Cetic.br C5 table 2025](https://cetic.br/en/tics/domicilios/2025/individuos/C5/)
- **OS share (StatCounter, mobile, Brazil):** Android about 77.9% and iOS about 22.1% (May 2026); Android 78.96% and iOS 21.03% (June 2026); Android 77.59% and iOS 22.41% (July 2026) — [StatCounter](https://gs.statcounter.com/os-market-share/mobile/brazil)
- **Zero-rating:** Claro, TIM and Vivo still offer unlimited WhatsApp on prepaid plans as a revocable promotional benefit. Plans have been reworked since 2024 (Claro in Feb, TIM in Oct), with capped social-media allowances. Executives openly discuss ending zero-rating, citing 5G costs. 53% of users say they would switch carrier if it ended (Mobile Time/Opinion Box, n=2,099). — [Estado de Minas](https://www.em.com.br/emfoco/?p=17985); [Banda B](https://www.bandab.com.br/nacional/vivo-tim-claro-discutem-fim-whatsapp-ilimitado/amp/); [Tecnoblog](https://tecnoblog.net/noticias/53-dos-brasileiros-mudariam-de-operadora-por-whatsapp-ilimitado/)

### Inferences
- Use "about 4.8M dogs and cats in vulnerability (IPB, 2024)" as the headline figure, with its definition stated. Never use "30M (WHO)". The IPB series moves a lot between editions (3.9M → 8.8M → 4.8M), and the species split flipped (96% dogs at NGOs in 2018 → 92% cats in 2024). That points to methodology changes or a reporting error. Treat it as order-of-magnitude only.
- No one measures street-animal populations directly. A platform that collects geotagged sightings could become a *source* of population and distribution data (a public-good byproduct), provided duplicate sightings are handled through chains and re-ID.
- Design constraints from connectivity: PWA or very light web pages on Android; image compression on the device before upload; resumable uploads; offline queueing; WhatsApp as the main way to bring in reports and send alerts (zero-rated for many prepaid users, though that benefit is not guaranteed). With 39% running out of data within 3 months, page weight and image size are product-critical.

### Gaps
- **Low-end device prevalence** (RAM and storage tiers, Android version distribution in Brazil) was not found. Check Anatel, IDC Brasil or Google Play Console benchmarks.
- No official count of WhatsApp users in Brazil (Meta does not publish one). TIC's 92% instant-messaging figure is the best proxy.
- The original IPB reports (methodology PDFs) were not accessed. The figures come via press.
- No primary source for the number of independent protetores in Brazil.

---

## 5. Legal: LGPD, Marco Civil (arts. 15 and 19 plus the STF ruling), animal-cruelty law, community-animal laws, defamation, ECA Digital

### Takeaway
Animal photos are not personal data in themselves. But exact locations (often a home or workplace), reporter identities, chat messages, and bystanders or license plates in photos are personal data under the LGPD and need a legal basis, minimization and rights handling. The STF (June 2025) made notice-and-takedown the general liability rule for third-party content, but kept the court-order requirement of art. 19 for crimes against honor. That matters a lot for posts accusing people of abuse, which Brazilian courts regularly treat as defamation (R$2k–20k awards). Art. 32 of Lei 9.605 (with Lei 14.064/2020) makes cruelty to a dog or cat punishable by 2–5 years of reclusão. The ECA Digital has been in force since Mar 17, 2026 and likely applies to an open civic app with chat.

### Cited Findings

**LGPD (Lei 13.709/2018)**
- Personal data = information relating to an identified or identifiable natural person (art. 5, I). Legal bases are in art. 7 (consent, legitimate interest, etc.). Sensitive data, including biometrics, is governed by art. 11. Children's and teens' data must be processed in their best interest (art. 14). Data-subject rights include access, correction, deletion and portability (art. 18). — [LGPD, Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- ANPD Legitimate Interest Guide (published Feb 2, 2024): explains the balancing test (LIA recommended, not mandatory). Legitimate interest **cannot** be used for sensitive data. It may apply to children's and teens' data with extra safeguards. — [Mattos Filho](https://www.mattosfilho.com.br/unico/anpd-legitimo-interesse-lgpd/); [Guide PDF (TCE-PB mirror)](https://tce.pb.gov.br/wp-content/uploads/2025/03/guia_legitimo_interesse.pdf)
- **Enunciado CD/ANPD nº 1/2023:** children's and teens' data may be processed under any basis in art. 7 or art. 11, provided their best interest is observed and prevails, so parental consent is not the only route — [Felsberg](https://www.felsberg.com.br/importante-anpd-publica-enunciado-sobre-o-tratamento-de-dados-pessoais-de-criancas-e-adolescentes/)
- The ANPD was turned into a regulatory agency by Lei 15.352/2026 (secondary source) — [Confidata](https://confidata.com.br/blog/eca-digital-o-que-muda-empresas)

**Marco Civil da Internet (Lei 12.965/2014)**
- **Art. 15:** an application provider "constituído na forma de pessoa jurídica e que exerça essa atividade de forma organizada, profissionalmente e com fins econômicos" must keep application access logs, confidential and secure, **for 6 months**. A court order can extend the duty to providers not covered (§1). Police, administrative authorities or the Public Prosecutor can request precautionary retention for longer (§2). Disclosure always requires a court order (§3). — [Planalto, Lei 12.965 (via Letra da Lei)](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm)
- **STF, Temas 987 and 533 (judged 26/06/2025):** art. 19 declared partially unconstitutional. Platforms can be liable for third-party content without a court order. — [Teletime](https://teletime.com.br/26/06/2025/art-19-stf-concilia-votos-e-plataformas-terao-responsabilizacao-parcial/); [Chambers](https://chambers.com/articles/stf-muda-regras-para-responsabilização-das-plataformas-digitais-o-que-precisa-saber-2)
  - Serious crimes (attempted coup, terrorism, inducement to self-harm or suicide, racism, homophobia, crimes against women and children): liability if the platform does not act "imediatamente". Crimes in general and other illicit acts: until Congress legislates, the platform "será responsabilizada pelos danos causados por conteúdos de terceiros" if it fails to remove content after receiving a takedown request. — [STF Notícias, 09/06/2026](https://noticias.stf.jus.br/postsnoticias/stf-vai-analisar-recursos-contra-tese-fixada-no-julgamento-do-marco-civil-da-internet/)
  - Art. 19 (court-order rule) remains for **crimes against honor** (calúnia, difamação, injúria). Email, closed videoconference and **instant-messaging** services remain under art. 19. Marketplaces answer under the CDC (consumer protection code). Effects apply prospectively. — [search summary of Teletime / Chambers / BMA](https://www.bmalaw.com.br/conteudo/institucional/informativos-e-newsletters/constitucionalidade-do-artigo-19-do-marco-civil-da-internet/pdf)
  - Acórdão published Nov 2025 — [Conjur](https://www.conjur.com.br/?p=871139). 12 embargos de declaração (Facebook, Google, amici) were scheduled for June 10, 2026. Requests included a 6-month implementation period, minimum requirements for extrajudicial notices, and a definition of which providers are covered. — [STF Notícias](https://noticias.stf.jus.br/postsnoticias/stf-vai-analisar-recursos-contra-tese-fixada-no-julgamento-do-marco-civil-da-internet/). Justice Toffoli reportedly proposed a 60-day implementation period (June 2026) — [search summary](https://noticias.stf.jus.br/postsnoticias/stf-vai-analisar-recursos-contra-tese-fixada-no-julgamento-do-marco-civil-da-internet/)

**Animal cruelty law**
- **Lei 9.605/98, art. 32:** abuse, mistreatment, wounding or mutilating wild, domestic or domesticated animals: detenção of 3 months to 1 year plus a fine. **§1-A (added by Lei 14.064/2020, "Lei Sansão"): for dogs or cats, reclusão of 2–5 years, a fine and a ban on keeping animals.** §1-B: tattoos or piercings on dogs or cats for aesthetic purposes. §1-C: causing an environmental disaster that harms animals. §2: penalty increased by 1/6 to 1/3 if the animal dies. The consolidated text in the Letra da Lei index is attributed to a redaction by Lei 15.355/2026, in force 12/03/2026. — [Planalto, Lei 9.605](https://www.planalto.gov.br/ccivil_03/leis/l9605.htm)

**Community-animal (cão/gato comunitário) laws**
- **RS state Lei 13.193/2009** creates the "cão comunitário", bans euthanasia of street dogs, and provides for identification, adoption and sterilization. Porto Alegre created a municipal Cadastro de Animal Comunitário (Feb 2026). A municipal bill is still pending. — [Prefeitura de Porto Alegre](https://prefeitura.poa.br/smgg/noticias/prefeitura-fortalece-politica-de-protecao-caes-comunitarios-por-meio-de-cadastro)
- **SP state:** bills, not enacted laws. PL 1/2026 (state policy for community animals: a dog or cat with ties of dependence on a community and no single owner) and PL 25/2026 (state policy for protecting and recognizing community dogs and cats). — [ALESP PL 25/2026](https://www.al.sp.gov.br/spl/2026/02/Propositura/1000676290_1000845826_Propositura.pdf); [ALESP accessory doc](https://www.al.sp.gov.br/spl/2026/03/Acessorio/1000680588_1000850414_Acessorio.doc)
- **RJ:** one secondary source says a new state animal-law code recognizes community dogs, which should preferably stay at their place of origin after sterilization and vaccination. Not verified against the official text. — [TVT News](https://tvtnews.com.br/?p=777186)

**Defamation risk from posting alleged abuse**
- TJMG (2017): a woman who posted a Facebook video alleging a dog was being mistreated was ordered to pay R$5,000. The court found the right to report legitimate, but the owner's image had been harmed, and vet statements showing no abuse were decisive. — [TJMG](https://bd.tjmg.jus.br/bitstreams/f05e811d-7c53-4a30-95ca-8fd451a1b93d/download) (via search summary)
- TJMG (recent appeal): R$4,000 upheld for posts accusing a person of a crime and **publishing their personal data** during a dispute over a rescued dog. The court held this exceeded freedom of expression. — [AdmDireito](https://www.admdireito.com.br/jurisprudencia/eme/118.5596.3209.5773) (via search summary)
- TJSC: damages for social-media attacks on an animal protector or an animal-protection association (one 2023 case R$2,000, plus a removal order) — [TJSC](https://www.tjsc.jus.br/web/imprensa/noticias/-/asset_publisher/GP1QtxFaSsX0/content/id/15681776); [Lex](https://www.lex.com.br/mulher-e-condenada-por-diatribes-lancadas-em-redes-sociais-contra-protetora-de-animais/)
- TJSP: an activist ordered to pay R$20,000 at first instance after confronting a dog owner and posting online. The appeal was partially granted and the final amount is unknown. (Search summary only; specific URL not confirmed.)

**ECA Digital (Lei 15.211/2025)**
- In force since **Mar 17, 2026** (date set by Lei 15.352/2026) — [Jornal de Brasília](https://jornaldebrasilia.com.br/noticias/brasil/eca-digital-entra-em-vigor-nesta-terca-17-veja-o-que-muda-para-plataformas-e-usuarios/); [Confidata](https://confidata.com.br/blog/eca-digital-o-que-muda-empresas)
- Applies to IT products and services **directed at minors or likely to be accessed by them** ("acesso provável"), including foreign providers: social networks, apps, games, operating systems and app stores. Obligations include **age verification**, **protection by default**, and faster response to harmful content. — [Jornal de Brasília](https://jornaldebrasilia.com.br/noticias/brasil/eca-digital-entra-em-vigor-nesta-terca-17-veja-o-que-muda-para-plataformas-e-usuarios/); [Machado Meyer factsheet](https://www.machadomeyer.com.br/images/ebooks/Factsheet_ECA_Digital.pdf); [Demarest](https://demarest.com.br/wp-content/uploads/2025/10/ECA-Digital-traz-novas-perspectivas-e-desafios.pdf)

### Inferences
- **LGPD mapping for the product:** (a) the exact coordinates of a sighting near a residence, the reporter's identity, phone number and chat content, and people or license plates in photos are personal data. (b) Legitimate interest (with a documented LIA) is the natural basis for the civic map and chains. Consent is natural for optional features such as precise-location sharing and WhatsApp notifications. (c) Animal re-ID embeddings are **not** human biometrics, but any face-detection or blurring pipeline that processes human faces should avoid creating templates. Blurring faces and plates by default on upload lowers risk. (d) The "exact vs. approximate" location model fits the LGPD minimization principle well: show the public a coarsened location and keep the precise point for verified responders.
- **Marco Civil art. 15 nuance:** the duty covers legal entities operating "com fins econômicos". A nonprofit or association running the platform might argue it falls outside the article, but a court order (§1) or a precautionary request (§2) can still require retention. A 6-month log retention policy is the safe default either way. This needs legal confirmation.
- **Post-STF liability:** a civic UGC platform now faces notice-and-takedown liability for illicit content in general. It needs a reporting channel, triage SLAs and records of decisions. Abuse accusations that name or identify people fall under crimes against honor, where art. 19 still requires a court order. However, the case law shows *users* get sued, and "exposing personal data" aggravates damages. Product rules worth considering: forbid naming or identifying alleged abusers in public posts; send abuse reports privately to authorities (police, MP, municipal animal-welfare departments, Ibama/Disque Denúncia); strip addresses; moderate "denúncia" posts before they go public.
- **ECA Digital:** an open, free civic app with photos, maps and stranger-to-stranger chat is plausibly "likely accessed" by teens, who are often involved in feeding or rescuing strays. That implies age assurance, privacy-protective defaults for minors (no precise location sharing, restricted DMs from adults) and fast handling of harmful content. Confirm against the regulatory decrees and ANPD guidance.
- **Community-animal recognition** (RS law and pending SP/RJ initiatives) supports a first-class "community animal" entity: a known territory, caregivers (cuidadores), castration status and no single owner. That entity is different from "lost" or "stray", and a sighting of it should not trigger a "found pet" flow.

### Gaps
- I did not read the full text of the STF thesis (the self-regulation duties, notification requirements, transparency reports, and any requirement for a legal representative in Brazil are reported but not verified here), and I don't know the outcome of the June 2026 embargos.
- No ANPD guidance specific to geolocation or user-uploaded images was found.
- ECA Digital regulatory decrees and ANPD guides (age-assurance standards) were not retrieved.
- Official texts of SP municipal and RJ state community-animal laws were not verified. Other capitals (BH, Curitiba, Recife, Salvador, Florianópolis) were not covered.
- No case law was found on *platform* (as opposed to user) liability for animal-abuse accusation posts after the 2025 STF ruling.

---

## 6. Current behavior: how Brazilians handle lost, stray and injured animals today

### Takeaway
Brazilians handle lost, stray and injured animals through Facebook groups (hundreds of posts a day), Instagram accounts of protectors, NGOs and newspapers, WhatsApp groups and communities, word of mouth, posters, and protectors who do the amplification. The channels reach people but are fragmented, hard to search, have no notion of geography or time, go stale without anyone closing cases, and invite fraud. Crisis events (the RS floods of 2024) push the volume past what these channels can handle and lead to ad hoc tools.

### Cited Findings
- Many Facebook groups exist for lost animals, with "hundreds of new posts per day". People are advised to post on their own profile, ask friends to share, and post in local search groups. Dogs are often found "a few kilometers" from where they went missing, so the search radius should widen after the first days. — [Catraca Livre](https://catracalivre.com.br/carrefour-causa-animal/como-encontrar-um-animal-perdido-veja-dicas-e-servicos-de-buscas/)
- Protectors act as amplifiers. In one example, a protector partnered with a school to spread a case, and the "found" post got more than 1.3k reactions. — [BNews](https://www.bnews.com.br/noticias/bnews-pet/criancas-fazem-retrato-falado-de-cachorro-perdido-e-mobiliza-comunidade-veja-fotos.html)
- Newsrooms run lost-pet sections through Instagram and WhatsApp communities ("Cadê meu pet?", Folha Vitória) — [Folha Vitória](https://www.folhavitoria.com.br/geral/cade-meu-pet-voce-viu-o-tutor-cao-foi-encontrado-perdido-na-serra/)
- During the RS floods, social networks were the main reunion channel, alongside NGO sites with search by neighborhood — [Canaltech](https://canaltech.com.br/redes-sociais/chuvas-no-rs-redes-sociais-ajudam-a-encontrar-animais-perdidos-288373/)
- Builders of the 2023 ILY platform describe the problem they addressed as owners relying on posters, social networks and WhatsApp groups, and they adopted WhatsApp for alerts and validation — [Estado de Minas](https://www.em.com.br/app/noticia/gerais/2023/01/24/interna_gerais,1448600/plataforma-mineira-ajuda-a-encontrar-pets-perdidos.shtml)
- Record numbers of animal-violence complaints were reported in Jan 2026 (Band). The article could not be fetched (HTTP 403), so the specific figures were not verified. — [Band](https://www.band.com.br/pets/noticias/brasil-tem-recorde-de-denuncias-de-violencia-contra-animais-202601311457)
- Lost-pet owners posting publicly on social media are targets for scams (international pattern, §1) — [CBS New York](https://www.cbsnews.com/amp/newyork/news/scammers-target-long-island-families-asking-for-help-finding-lost-pets-on-social-media)

### Inferences
- Pain points: no geographic search; no linking of the same animal across posts and platforms (the "chain" concept fills this directly); posts never marked resolved; contact via public phone numbers (scam exposure); emergency requests for injured animals that depend on whoever happens to be online; no handoff to CCZs or NGOs; burnout among the few protectors doing most of the amplification.
- The value is not in replacing WhatsApp and Facebook but in giving them a structured backbone: a canonical case URL that people share *into* those groups, WhatsApp intake that creates the structured record, and photo re-ID that links duplicates.

### Gaps
- **No quantitative data on the size of Brazilian lost-pet Facebook groups, Instagram accounts or WhatsApp groups** (member counts, post volumes) was found. Manual sampling of the largest groups per capital is needed.
- No Brazilian data on lost-pet scam incidence (e.g., golpe do pet perdido or Pix ransom).
- No survey data on what share of lost pets are recovered in Brazil, or by which channel.
- No data on CCZ capacity or response to citizen calls for injured animals (e.g., SP 156, RJ 1746).

---

## 7. Gaps and opportunities synthesized

### Takeaway
Nobody owns the space: Brazil has no dominant lost or stray platform, SinPatinhas covers only about 2% of owned animals and offers no visible API, and current behavior is fragmented across Meta platforms. The opportunities are (1) a structured, geo-temporal, scam-resistant case layer that works *with* WhatsApp, Instagram and Facebook; (2) first-class handling of strays and community animals (which SinPatinhas mostly does not register); (3) institutional anchoring (CCZs, NGOs, SinPatinhas linkage) of the kind that made Petco Love Lost the default in US cities; and (4) privacy-by-design, which the Ring backlash shows is make-or-break.

### Cited Findings
- Aggregation and integration won in the US (Nextdoor posts flow into Petco Love Lost, and cities adopted it as their official map) — [Nextdoor blog](https://blog.nextdoor.com/2024/05/30/reunite-lost-pets-beyond-your-neighborhood-with-petco-love); [Edhat](https://www.edhat.com/news/county-healths-animal-services-debuts-new-lost-found-pet-map/)
- Reunions are undercounted by about 3× unless people are prompted to confirm them — [Techstrong.ai](https://techstrong.ai/?p=44893)
- Camera-based AI search drew a large privacy backlash, with opt-out defaults criticized — [ABC7](https://abc7news.com/post/ring-flock-partnership-amazon-scraps-surveillance-company-safety-super-bowl-commercial-backlash/18596207/); [Techdirt](https://www.techdirt.com/company/ring/)
- SinPatinhas: about 1.8M registered (Sep 2026) out of about 93M owned dogs and cats; QR/RG Animal and microchip lookup exist — [Portal de Prefeitura](https://portaldeprefeitura.com.br/pernambuco/pernambuco-animais-cadastrados-sinpatinhas-castracao-microchipagem/634008/); [Tribuna de Minas](https://tribunademinas.com.br/colunas/bichoseacidade/03-05-2026/sinpatinhas-reune-informacoes-da-populacao-de-caes-e-gatos-no-brasil.html?amp=1); [CartaCapital](https://www.cartacapital.com.br/?p=442972)
- Mobile-only, prepaid and data-capped users are the norm in classes C and DE, and 92% of internet users use messaging — [Cetic.br](https://www.cetic.br/media/docs/publicacoes/2/pt-br/20260511173151/tic_domicilios_2025_resumoexecutivo%20pt.pdf); [Cetic.br C5](https://cetic.br/en/tics/domicilios/2025/individuos/C5/)
- Crisis demand is real and recurring (RS 2024, about 10k–20k animals sheltered), and the tools were improvised — [TecMundo](https://www.tecmundo.com.br/software/282908-rs-casal-lanca-sistema-ia-match-entre-pets-perdidos-tutores-veja.htm); [Diário de Pernambuco](https://www.diariodepernambuco.com.br/noticia/brasil/2024/05/rs-tem-20-mil-animais-em-abrigos-e-anuncia-castracao-e-microchipagem.html)

### Inferences (opportunity list, ranked by how much downstream pain each removes)
1. **WhatsApp-first intake plus a shareable canonical case link.** This meets users where they already are (92% use messaging, zero-rating) and gives the fragmented Facebook and WhatsApp ecosystem one place for each case to live. It directly addresses the cold-start failure of earlier Brazilian apps.
2. **Chains (dedup + time + place) plus prompts to confirm closure.** This addresses posts that go stale and the undercount of reunions, and produces an aggregate distribution signal for strays that nobody in Brazil currently measures.
3. **Separate entity types:** lost (owned), found, stray, community (with territory and caregivers), emergency (injured). Community animals are legally recognized in RS and pending in SP/RJ, and SinPatinhas mostly does not cover them.
4. **Scam resistance:** contact relay and masking, hidden verification traits, warnings about "codes" and Pix, and verified badges for NGOs, protectors and CCZs (ILY's WhatsApp-number validation is a local precedent).
5. **Privacy and legal design:** location precision tiers (approximate public, exact for verified responders), face and plate blurring, no naming of alleged abusers in public, a private route for abuse reports to authorities, notice-and-takedown workflow (post-STF), 6-month access-log retention, ECA Digital defaults for minors.
6. **Institutional anchoring:** pilot with one or two municipalities (CCZ / Bem-Estar Animal) and NGOs; pursue a SinPatinhas linkage (QR/RG lookup, nudges to register) through MMA; offer a "crisis mode" for floods and disasters.
7. **Photo re-ID as an amplifier, not the core.** Vendor claims (Pupz >94%, Finding Rover, Petco's 512 points) are unverified, and US evidence suggests matching helps most in long-tail cases. Ship the human workflow first.

### Gaps
- No Brazilian user research (surveys or interviews) on lost/stray handling was found. Primary research is needed.
- Sustainability and funding models for Brazilian civic animal platforms (municipal contracts, ProPatinhas-linked funds, pet-industry CSR, Abinpet/Petz/Cobasi/Petlove) were not researched.
- App-store status of Brazilian competitors has not been verified (it needs a manual check).
