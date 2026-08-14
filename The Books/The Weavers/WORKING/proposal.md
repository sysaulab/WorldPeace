
# PROPOSAL: THE LIVING ARCHIVE PROJECT  
*A Community‑Owned Narrative Engine for Ethical Storytelling, Economic Equity, and Sustainable AI*

---

## 1. EXECUTIVE SUMMARY

**The Living Archive Project** is a novel, a community economic experiment, and a scalable ethical AI architecture—all in one. We are creating a science fiction novel built from the real, lived experiences of community members, especially those whose voices are rarely centred.

**Our operational core:**

- **Winter Pilot:** 16-week storytelling session at the **Evelyne Saller Centre** (Vancouver), conducting **10 interviews per week** (160 total).
- **The Product:** A novel that dynamically regenerates for each reader, adapting to their chosen **tone, setting, and language**—powered by a massive cached AI master prompt.
- **The Economics:** Revenue split **1/3 Editor (The Living Archive Press)**, **1/3 Authors (contributors)**, **1/3 Community Fund**—creating a self-sustaining long-term cultural institution.
- **The Distribution:** We bypass hostile traditional editors by founding **The Living Archive Press**. We **print, bind, trim, and fulfill every single book in-house** from our Hastings storefront—using eco-friendly desktop equipment and a **volunteer-friendly three-station guillotine workflow**.
- **The Ask:** **$58,012** in seed funding plus **provision of a free storefront on Hastings Street** to serve as our community hub and micro-factory.

---

## 2. PROJECT VISION & OVERVIEW

### The Cultural Gap We Fill

Cities are rich with untold stories—of migration, resilience, love, loss, and everyday survival. Yet these stories rarely enter the cultural mainstream except through extractive journalism or voyeuristic documentaries. Our project reverses that flow. We place the storyteller at the centre, with:

- **Dignity** – no exploitation, no sensationalism.
- **Ownership** – the contributor keeps their original booklet.
- **Partnership** – they share directly in the project's financial success.

### The Narrative Product

The final output is a novel that regenerates itself for each reader. A buyer chooses their preferred:
- **Genre:** noir, pastoral, thriller, lyrical, epistolary, etc.
- **Setting:** megacity, frontier colony, undersea habitat, arctic outpost, etc.
- **Language:** English, French, Mandarin, Spanish, Punjabi, Tagalog, etc. (serving Vancouver's diverse linguistic communities).

The engine delivers a coherent, emotionally resonant novel that honours the source stories while weaving them into a cohesive fictional world.

> *One reader gets a rain-soaked cyberpunk detective story in English. Another gets a quiet, epistolary meditation on loss in French. A third receives a pastoral family saga in Mandarin. The underlying human truths remain identical.*

---

## 3. THE COMMUNITY ECONOMIC MODEL

### The 1/3 – 1/3 – 1/3 Split – Long-Term Sustainability

| Revenue Stream | Allocation | Purpose |
| :--- | :--- | :--- |
| **1/3 – Editor (The Living Archive Press)** | Reinvested into the press | Covers operational costs, equipment maintenance, future automation, and staff. Ensures the project is **self-sustaining** beyond the pilot. |
| **1/3 – Authors (Contributors)** | Split equally among all contributors | Direct economic partnership. Every contributor receives an equal share—presence is the only measure. |
| **1/3 – Community Fund** | Democratic governance by contributors | Funded initiatives chosen by the contributor pool (youth programmes, mental health, digital literacy, public art). |

**Why This Model Works:**
- The **Editor share** ensures The Living Archive Press becomes a **permanent, self-funding cultural institution**—not a one-off grant-dependent project.
- The **Author share** honours the storytellers with real economic partnership.
- The **Community Fund** keeps the project rooted in collective decision-making and local impact.

---

## 4. METHODOLOGY – THE THREE PILLARS

### Pillar 1: The AI Witness Interview (Personal Booklet)
- A contributor sits with a **peer worker** for an unhurried conversation.
- A **prompter** observes quietly, noting thematic shape and emotional texture.
- An LLM (via a secure, paid API) structures the narrative into a **personal booklet**—written in the contributor's own voice, with no editorialising.
- The booklet is returned to the contributor for review.

### Pillar 2: The Generative Novel Engine (For Readers)
- We construct a **master narrative prompt** of approximately **500,000 tokens** containing plot, character arcs, world lore, and style guides.
- When a reader purchases the novel, they select their preferred **tone, setting, and language** (≈200 tokens).
- The engine combines the cached master prompt with that dynamic input and generates a full, cohesive novel. **Generation time is approximately 2 minutes for a 250,000-token output**—a realistic, acceptable wait for a personalised book.

---

## 5. TECHNICAL INFRASTRUCTURE & AI STRATEGY

### A. Privacy – Paid API vs. Free Chatbots

| Feature | Free Public Chatbot | Our Paid API (DeepSeek) |
| :--- | :--- | :--- |
| Data retention | Stored for training / auditing | **Zero‑retention** – by contract |
| Training opt‑out | Often superficial | **Guaranteed** – no training use |
| Encryption | Variable | TLS 1.2+ end‑to‑end |
| Local orchestration | None | **AnythingLLM** – fully local |

All contributor transcripts are deleted immediately after the booklet is generated.

### B. Cost Efficiency – The 500k‑Token Caching Breakthrough

**The Problem:** Naively generating a personalised novel from scratch for every reader would cost ~$1.50–$2.00 per copy and take ~20+ seconds just to process the prompt.

**Our Solution – Prefix Caching:**
- **First request (cache write):** The API processes the full 500k‑token master prompt (~$1.50, ~20 seconds). The cache is stored.
- **All subsequent requests (cache hits):** The API skips computation for the 500k prefix, processing only the 200‑token buyer instruction (tone + setting + language).
- **Result:** Marginal cost per copy drops to **~$0.10–$0.25**—a reduction of over 90%. Total generation time, including output streaming, is approximately **2 minutes**—fully acceptable for a bespoke book.

### C. Language Expansion – Serving Vancouver's Diversity

By adding **language** as a dynamic parameter, we unlock:
- **Mandarin** for the city's significant Chinese-speaking community.
- **French** for our bilingual heritage.
- **Spanish, Punjabi, Tagalog**—languages spoken in Vancouver's diverse neighbourhoods.
- **Future expansion:** Any language supported by the underlying LLM.

This transforms the novel from a monolingual product into a **truly inclusive cultural artifact**, while the caching strategy ensures adding languages does not increase marginal cost.

### D. Environmental Impact

Our caching strategy reduces GPU compute and energy consumption by **90%+** per sale, turning a carbon-heavy digital product into a remarkably sustainable one. Combined with print-on-demand (no unsold remaindered books), the project has a minimal environmental footprint.

### E. Fostering Neutral & Multicultural Societies

Beyond technical efficiency and cost savings, the AI architecture serves a deeper civic purpose: **building bridges across Vancouver's richly diverse communities.**

- **Linguistic Equity:** By offering the novel in multiple languages, we provide equitable cultural access without demanding linguistic assimilation. A Mandarin-speaking elder and an English-speaking teenager can both experience the same story in their mother tongue, fostering intergenerational and intercultural dialogue.
- **Neutral Framing:** Our master prompt is carefully constructed to emphasize **universal human themes**—resilience, love, loss, hope, and the search for meaning—over divisive political, religious, or ethnic hierarchies. The AI is guided to translate and transform these stories using culturally neutral bridging language where appropriate.
- **Shared Narrative Cosmos:** Diverse communities see themselves reflected in a *shared* fictional universe, reducing "us vs. them" narratives. This is particularly vital in a city like Vancouver, where immigration, displacement, and cultural coexistence are daily realities.
- **A Civic Asset:** When AI is ethically architected—with multilingual support, human-centric prompts, and a governance model that puts storytellers in charge—it becomes a **tool for social cohesion**, not division. The Living Archive Project proves that technology can help de-escalate cultural friction and celebrate our common humanity.

> *"We are not asking different communities to read the same book. We are inviting them to read their own book—and discover that it tells the same story."*

---

## 6. PRIVACY & ETHICAL SAFEGUARDS

- **No Data for Training:** API agreement explicitly forbids training use.
- **No Persistent Storage:** Transcripts deleted immediately after generation.
- **Local Orchestration:** AnythingLLM on secured local machines.
- **Informed Consent:** Plain-language agreements with a clear withdrawal window (up until public release).
- **Trauma‑Informed Design:** Peer workers trained to recognise distress and offer grounding.

---

## 7. BUDGET & FINANCIAL PROJECTIONS (16‑Week Winter Pilot)

### A. Estimated Fixed Setup & Operational Costs

| Category | Cost | Rationale & Notes |
| :--- | :--- | :--- |
| **Software Development (E‑commerce Bridge & Automation)** | **$15,000** | Custom platform to: take prepaid orders + preferred genre/setting/language, trigger the AI API call, generate the print-ready PDF, and auto-create shipping labels. One‑time build. |
| **In‑House Fulfillment Hardware** | **$2,350** | Epson EcoTank monochrome printer (ultra-low ink cost), thermal label printer, manual binding machine, and **3 manual guillotine trimmers**—each pre-set to a fixed trim depth (trim 1, trim 2, trim 3) for volunteer-friendly station-based workflow. Includes extra blades and binding supplies. |
| **AI Credits (Interview Transcriptions)** | **$320** | 160 interviews × $2 per interview. (We **do not** need advance credits for novel generation—those costs are covered by prepaid orders.) |
| **Peer Worker Stipends** | **$12,800** | 160 interviews × $80 per session (split with prompters). Includes prep, interview, and light admin. |
| **Prompter Stipends** | **$3,200** | 160 interviews × $20 per session (observing, noting themes, guiding the AI booklet assembly). |
| **Community Outreach & Grassroots** | **$5,000** | Flyers, translations, partnerships with the Evelyne Saller Centre and other local organizations. |
| **Book Launch Marketing & Press Campaign** | **$7,100** | Press conference, media kit, targeted social ads, and a launch event. |
| **Legal & Compliance** | **$3,000** | Privacy policy, contributor agreements, imprint registration (ISBNs). |
| **Subtotal** | **$48,770** | |
| **Contingency (10%)** | **$4,877** | Unforeseen costs (hardware replacement, extra sessions). |
| **Total Fixed Pilot Cost** | **$53,647** | |

*(Note: This figure excludes the value of the requested free storefront on Hastings Street.)*

---

### B. Variable Cost per Copy (Novel Generation + In‑House Printing)

| Component | Cost | Notes |
| :--- | :--- | :--- |
| **AI Generation per Novel** | ~$0.25 | Fully covered by the prepaid purchase price—no upfront float required. |
| **In‑House Printing Materials** | ~$2.50 – $3.50 | Paper, ink, binding wire/spine, trimmer blades (amortized). |
| **Total Variable Cost per Book** | **~$2.75 – $3.75** | |

---

### C. Estimated Revenue Scenarios (Prepaid Model)

All books are **prepaid** by buyers, meaning our AI generation costs are instantly covered by the customer's payment.

| Sales Scenario | Copies Sold | Price per Copy | Gross Revenue | Gross Margin (After Print & AI) |
| :--- | :--- | :--- | :--- | :--- |
| Conservative (Seed) | 300 | $14.99 | $4,497 | ~$3,400 |
| Moderate (Growth) | 800 | $14.99 | $11,992 | ~$9,000 |
| Optimistic (Scale) | 2,000 | $14.99 | $29,980 | ~$22,000 |

*Note: Because printing and AI are covered by prepaid orders, the **$53,647** seed grant is purely for infrastructure, people, and outreach. The revenue from sales flows directly into the 1/3 – 1/3 – 1/3 split.*

---

### D. Long-Term Revenue Stream (Post-Pilot)

| Revenue Source | 1/3 Editor (Press) | 1/3 Authors | 1/3 Community Fund |
| :--- | :--- | :--- | :--- |
| **2,000 copies sold** | ~$7,333 | ~$7,333 | ~$7,333 |
| **5,000 copies sold** | ~$18,333 | ~$18,333 | ~$18,333 |
| **10,000 copies sold** | ~$36,667 | ~$36,667 | ~$36,667 |

- **Editor share** funds automation, staff, and future volumes—making the project **permanent**.
- **Author share** provides meaningful compensation to storytellers.
- **Community Fund** grows with success, creating a lasting legacy.

---

## 8. PUBLICATION & DISTRIBUTION STRATEGY  
*Radical Vertical Integration – We Own the Entire Supply Chain*

### The Problem with Traditional Publishing
Major editorial houses have drawn a hard line against AI-assisted content. Submitting *The Living Archive* to traditional editors would guarantee rejection.

**Our Solution:** We found **The Living Archive Press**—our own independent imprint. We handle ISBNs, quality assurance, branding, and **every single step of physical production**.

### The Core Proposition: In‑House Micro‑Factory with Volunteer-Friendly Workflow

We do not outsource. We do not share margins. We bring the entire manufacturing process into our Hastings storefront.

**The Workflow:**

1. **Order Placement:** Customer prepays online, selects genre + setting + language.
2. **AI Generation:** The engine produces the personalized PDF (cost: $0.25; time: ~2 minutes).
3. **In‑House Printing:** The PDF is sent to our Epson EcoTank monochrome printer (ultra-low ink cost, eco-friendly).
4. **Manual Binding:** The printed pages are bound using our manual binding machine.
5. **Three‑Station Trimming (Volunteer-Friendly):**
   - **Station 1 (Trimmer 1):** Pre-set to trim depth #1.
   - **Station 2 (Trimmer 2):** Pre-set to trim depth #2.
   - **Station 3 (Trimmer 3):** Pre-set to trim depth #3.
   - **Process:** A volunteer places the book block in Station 1, secures it, pulls the guillotine lever, moves the pile to Station 2, repeats, moves to Station 3, repeats.
   - **Why three trimmers:** Eliminates time-consuming manual re-setting of the guillotine depth. Each volunteer needs only 30 seconds of training: *"Place, secure, pull."* This makes trimming accessible to anyone, turning the storefront into a **community-powered micro-factory**.
6. **Labeling & Shipping:** The thermal printer produces the shipping label. The book is dispatched from our storefront.

**Unit Cost:** ~$2.50 – $3.50 per book (paper, ink, binding materials, blade amortization).  
**Quality:** Professional, bookstore‑ready finish.  
**Waste:** Zero. We print only what is ordered.

---

### The Scaling Roadmap – Self‑Funded Automation

We start manual. We stay capital‑light. But we have a clear, self‑sustaining growth path:

| Phase | Trigger | Reinvestment Strategy |
| :--- | :--- | :--- |
| **Phase 1 – Manual (0 – 500 copies)** | Initial prepaid orders. | Fulfill using the Epson + binder + 3 guillotines. Throughput: ~20–30 books per day with volunteer labour. |
| **Phase 2 – Semi‑Automated (500 – 2,000 copies)** | Revenue from Phase 1 accumulates (Editor share). | Reinvest 1/3 Editor share into an **automated digital press** and **electric perfect binder**. Throughput scales to ~100+ books per day. |
| **Phase 3 – Fully Automated (2,000+ copies)** | Revenue snowballs. | Acquire an **inline print‑and‑bind system**—a single machine that prints, collates, binds, and trims in one pass. The Hastings storefront becomes a fully autonomous micro‑publishing factory. |

> **Why this impresses funders:** We have **zero external dependency**. No supply chain shocks. No outsourced margin leakage. Every dollar of revenue stays in the community, building our own capital base. The city is not funding perpetual subsidies—it is seeding a **self‑scaling, autonomous cultural manufacturer** that creates volunteer opportunities and local jobs.

---

## 9. TIMELINE (16‑Week Winter Session)

| Phase | Duration | Key Activities |
| :--- | :--- | :--- |
| **Phase 0 – Setup** | Weeks 1–2 | Recruit peer workers and prompters; install e‑commerce bridge; set up printer/binder/3 guillotines in Hastings storefront; finalize master prompt scaffold with language support. |
| **Phase 1 – Story Collection** | Weeks 3–16 | Conduct **10 interviews/week** (160 total) at Evelyne Saller Centre; generate booklets. |
| **Phase 2 – Master Prompt Finalization** | Week 16 | Integrate booklets into the final 500k‑token master prompt. |
| **Phase 3 – Pre‑Sales / Soft Launch** | Week 17 | Open prepaid orders to the public; test the full e‑commerce → AI → print → bind → trim → ship workflow. |
| **Phase 4 – Public Launch & Press** | Week 18 | City‑wide launch event; press conference; initiate $7,100 marketing campaign. |
| **Phase 5 – Fulfillment & Reinvestment** | Weeks 19–24 | Fulfill orders with volunteer trimming stations; use 1/3 Editor revenue to fund Phase 2 automation. First contributor assembly for community fund vote. |

---

## 10. WHY THIS MATTERS TO THE CITY

- **Economic:** Direct cash transfers to marginalized residents; a self‑sustaining cultural asset; every dollar spent on printing stays in Vancouver's local economy.
- **Labour:** Creates meaningful local work (fulfillment coordinator, peer workers, prompters) and volunteer opportunities that cannot be offshored.
- **Social:** Amplifies excluded voices; builds trust through non‑extractive engagement.
- **Cultural:** Positions Vancouver as a leader in ethical AI, multilingual publishing, and **radically independent community‑owned media**.
- **Environmental:** Caching strategy + print‑on‑demand + eco‑friendly ink = minimal waste and 90% lower AI energy use. No unsold remaindered books end up in landfills.
- **Civic Cohesion:** The multilingual, humanistically framed AI engine actively fosters intercultural understanding, making the project a tangible tool for de‑escalating division and celebrating shared humanity in one of the world's most diverse cities.
- **Replicable:** The model—community interviews + cached AI + in‑house micro‑factory—can be adopted by other cities, making Vancouver a pioneer.

---

## 11. REQUEST FOR SUPPORT

We are seeking:

1. **Seed Funding:** **$53,647** to cover personnel, software development, hardware, outreach, and the launch campaign.
2. **In‑Kind Space:** A **free storefront on Hastings Street** in Vancouver to serve as our community hub, micro‑factory, and public‑facing bookshop. This physical presence is non‑negotiable for our vertical integration model.
3. **Municipal Endorsement:** A letter of support to unlock private foundation grants.
4. **Outreach Partnership:** Access to centres like the **Evelyne Saller Centre** to recruit storytellers.

**In return, we offer:** Regular public reporting, co‑branding, a dedicated city showcase, and a lasting cultural institution that continues to generate community wealth and local manufacturing opportunities long after the pilot ends.

---

## 12. CONCLUSION

The Living Archive Project is not a tech demo. It is not an art project. It is a **complete, economically self‑sustaining ecosystem** for turning lived experience into shared cultural wealth—without exploitation, without surveillance, and without begging legacy publishers or third‑party printers for permission.

We have the technical architecture (prefix caching, multilingual support, ~2-minute generation).
We have the community infrastructure (Evelyne Saller Centre, peer workers, prompters).
We have the publishing strategy (The Living Archive Press).
We have the manufacturing roadmap (in‑house, volunteer‑friendly, self‑funded automation).
We have the unit economics (prepaid model, 90% AI cost reduction, zero external margins).
We have the long‑term revenue model (1/3 – 1/3 – 1/3).
We have the civic vision (AI as a tool for multicultural cohesion).

Now we ask for the city's partnership to bring it to life.

---

**Contact:** [Your Name / Organisation]  
**Next Steps:** We are ready to present to council, answer technical questions, or co‑design the outreach plan. We look forward to building this together.
