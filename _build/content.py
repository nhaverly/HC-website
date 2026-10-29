# -*- coding: utf-8 -*-
"""Page content for the Haverly Consulting website.

Edit the text here, then run:  python3 _build/build.py
Blog post bodies live in _build/posts/<slug>.html; their titles and dates are in POSTS below.
"""

SITE = {
    "name": "Haverly Consulting",
    "url": "https://www.haverlyconsulting.co.uk",
    "email": "info@haverlyconsulting.co.uk",
    "phone": "020 8064 1937",
    "phone_intl": "+442080641937",
    "address": ["167-169 Great Portland Street", "5th Floor", "London", "W1W 5PF"],
    "linkedin": "https://www.linkedin.com/in/nick-haverly",
    # Formspree form ID for the contact form (looks like "xyzabcde"). Leave as is until you have one.
    "formspree_id": "mljjevkn",
    "company_number": "12109253",
    # Web address of the HRA Assistant back end (the Cloudflare Worker), e.g.
    # "https://haverly-hra-assistant.yourname.workers.dev". While empty, the Tools page
    # does not link to the assistant and the page shows a "being set up" message.
    "cf_analytics_token": "e538d1b7121b4a5dac1aa87ba5045514",
    "hra_endpoint": "https://haverly-hra-assistant.nick-haverly.workers.dev/",
}

SERVICES = [
    {"slug": "advisory-partnership", "name": "Advisory Partnership",
     "blurb": "Unlimited, on-demand access to housing finance specialists through one annual subscription. No per-query charges.",
     "tags": "HRA · Homelessness and TA · Housing companies"},
    {"slug": "finance-business-partnering", "name": "Finance Business Partnering",
     "blurb": "Experienced partners embedded in your service teams to challenge assumptions and drive better decisions. Interim or long term.",
     "tags": "Budget cycles · Business cases · Transformation"},
    {"slug": "financial-appraisals", "name": "Financial Appraisals",
     "blurb": "Independent investment appraisals that stand up to scrutiny committees, auditors and government funders.",
     "tags": "Green Book · Viability · S106 challenge"},
    {"slug": "financial-reviews", "name": "Financial Reviews",
     "blurb": "A fresh technical look at policies and treatments to find recurring savings. MRP reviews alone have delivered six-figure annual savings for some clients.",
     "tags": "MRP · Debt · Treasury · Capital receipts"},
    {"slug": "project-management", "name": "Project Management",
     "blurb": "Structure and discipline for funded capital programmes, from Outline Business Case through to grant drawdown.",
     "tags": "Homes England · MHCLG · PMO"},
    {"slug": "training", "name": "Training and Development",
     "blurb": "Practitioner-led seminars, in-house sessions and webinars, designed around your team's needs.",
     "tags": "HRA · MRP · Capital financing"},
]

PRACTICE = [
    ("Housing Revenue Account", "Business plans, rent setting and 30-year models", "advisory-partnership"),
    ("Temporary accommodation", "Acquisition, funding and cost strategies", "advisory-partnership"),
    ("Housing companies", "Governance, modelling and dividend strategy", "advisory-partnership"),
    ("MRP and debt", "Policy reviews and borrowing strategy", "financial-reviews"),
    ("Investment appraisal", "Green Book business cases", "financial-appraisals"),
    ("Developer viability", "S106 and affordable housing challenge", "financial-appraisals"),
]

CLIENTS = ["Cabinet Office", "City of Westminster", "Ealing Council", "Guildford Borough Council",
           "Waverley Borough Council", "Isle of Wight Council", "Gosport Borough Council", "Reading Borough Council",
           "Portsmouth City Council", "South Kesteven District Council"]

# The "Our focus" panel in the homepage hero: (label, page it links to)
HOME_FOCUS = [
    ("Housing Revenue Account", "advisory-partnership"),
    ("Temporary accommodation", "financial-appraisals"),
    ("Housing & regeneration", "finance-business-partnering"),
]

# Procurement routes shown on the homepage and contact page
FRAMEWORKS = [
    {"name": "YPO 1141", "via": "Consultancy+", "url": "https://servicesprocurement.consultancyplus.com/about",
     "detail": "Certified to supply through Consultancy+, sole provider of YPO framework 1141 for Managing Consultancy and Professional Services. Supports direct award, typically within five to seven days, or a mini-competition."},
    {"name": "NEPRO³", "via": "Bloom", "url": "https://bloom.services/framework/nepro-3",
     "detail": "Accredited supplier on NEPRO³, Bloom's compliant route to market for public sector professional services, with fast mini-competitions."},
    {"name": "NHS LPP DPS", "via": "NHS London Procurement Partnership",
     "url": "https://www.lpp.nhs.uk/categories-and-services/estates-fm-corporate-services/estates-facilities-consultancy-services-dynamic-purchasing-system/",
     "detail": "Estates and Facilities Consultancy Services Dynamic Purchasing System (ref LPP/2020/015), open to all public sector bodies until June 2028 through further competition. Approved for Lot 5 (Construction Project Management Services), Lot 9 (Estates Strategy and Business Case Development Services) and Lot 11 (Property Acquisition, Disposal and Management Advisory Services)."},
]

TESTIMONIALS = [
    {"org": "Guildford Borough Council", "role": "Assistant Director of Regeneration and Economic Development",
     "quote": "Haverly Consulting has provided ongoing financial support to Guildford Borough Council including financial modelling and analysis, ongoing cashflow management, submission of Housing Infrastructure Fund (HIF) grant claims, and preparation of viability appraisals. This work has been fundamental to the development of the scheme."},
    {"org": "Waverley Borough Council", "role": "Housing Development Manager",
     "quote": "The team at Haverly Consulting Limited has consistently delivered high-quality services. Their independent reports have strengthened our business cases for investment, enabling us to advance the delivery of new homes on Waverley-owned sites and confidently appraise acquisition opportunities."},
    {"org": "South Kesteven District Council", "role": "Finance Lead, Housing Delivery",
     "quote": "The report met all our requirements, gave clear advice, was provided quickly and in my opinion was very good value for money."},
    {"org": "Portsmouth City Council", "role": "Corporate Strategy Manager",
     "quote": "Nick has good experience of housing and regeneration issues and good technical financial skills to identify issues around viability and how to overcome them. This is an incredibly useful skill set when dealing with issues that were being looked at as part of the local OPE programme. Through this OPE commission Nick was able to identify potential ways forward that helped overcome the challenges faced."},
    {"org": "Ealing Council", "role": "Assistant Director of Housing Regeneration",
     "quote": "Nick Haverly provided an excellent service with high level professional consultancy advice."},
    {"org": "Stedman Denny", "role": "Managing Director",
     "quote": "I have worked with Haverly Consulting for many years and their service has always been excellent. Always an excellent addition to the team."},
]

TEAM = [
    {"id": "nick", "name": "Nick Haverly FCPFA", "role": "Director", "initials": "NH",
     "bio": [
        "Nick is an experienced and entrepreneurial CCAB qualified finance professional, with a proven track record of shaping public sector practice on a local and national level, influencing and improving the delivery of services, and leading large and complex organisations through periods of change and economic uncertainty, focusing on growth and innovation.",
        "He has significant experience advising chief executives, executive directors, elected members, governing bodies and central and local government on strategic financial matters, driving efficiencies and maximising best value and best returns.",
        "Nick has been the financial lead on a number of award-winning, multi-million pound property investments, energy efficiency schemes and housing and regeneration developments across the UK, including two major temporary accommodation funding structures for Westminster City Council.",
        "He was a member of the Cabinet Office's One Public Estate Pool of Experts, and has been both adviser and lead on a number of business transformation projects.",
        "Nick is also a former Housing Adviser to the Local Government Association (LGA)."]},
    {"id": "richard", "name": "Richard Burden FCCA", "role": "Housing Finance and Development Consultant", "initials": "RB",
     "bio": [
        "Richard is a qualified finance professional with significant experience across the local authority, social housing and charity sectors. He has a proven ability to challenge and improve existing processes and systems, and communicates clearly with clients and colleagues on detailed financial issues.",
        "His knowledge spans financial and business planning, management accounting, treasury management, VAT and Corporation Tax, contract negotiation and property development. A natural strategic thinker, he builds strong teams, leads large projects, manages significant budgets and improves business operations."]},
    {"id": "pepa", "name": "Pepa Gomez", "role": "Strategic Operations Partner", "initials": "PG",
     "bio": [
        "Pepa brings a wealth of experience from an international banking background. She has a proven record of challenging and improving processes and systems and, speaking four languages, communicates professionally with clients and colleagues at all levels.",
        "With an eye for detail and a positive outlook in often complex legal landscapes, Pepa draws on her experience of compliance and regulation in international banking to create value for the organisation and improve business operations."]},
    {"id": "owen", "name": "Owen Buckwell", "role": "Associate Consultant", "initials": "OB",
     "bio": [
        "Owen has over 30 years of housing experience, from operational management up to strategic Housing Director level. With his Vanguard accreditation, he has transformed a range of services for local authorities across the UK.",
        "His Systems Thinking reviews have covered housing repairs, community wardens, adult social care, procure to pay and housing benefits. Owen also has extensive experience of value for money and Best Value reviews, delivering solutions that get the most from services with limited resources."]},
]

# Newest first. "tag" shows as the eyebrow on the article.
POSTS = [
    {"slug": "budget-2026-small-print-190000-fewer-homes-councils",
     "title": "Budget 2026 Small Print: The OBR Now Expects 190,000 Fewer Homes",
     "short": "Budget 2026 small print: 190,000 fewer homes",
     "date": "2026-10-29", "tag": "Budget 2026",
     "desc": "The OBR's housing downgrade, a lower Green Book discount rate, new council duties and TA parked until 2027: the Budget small print for councils."},
    {"slug": "budget-2026-council-housing-temporary-accommodation",
     "title": "Budget 2026: More Council Homes, No Relief for Temporary Accommodation",
     "short": "Budget 2026: more council homes, no relief for TA",
     "date": "2026-10-28", "tag": "Temporary accommodation",
     "desc": "An extra £1.5bn for social rent and cheaper PWLB borrowing, but LHA stays frozen and TA subsidy is untouched. What the Budget means for councils."},
    {"slug": "rough-sleeping-funding-temporary-accommodation-subsidy-gap-budget-2026",
     "title": "£874m for Rough Sleeping Is Welcome. Temporary Accommodation Is the Bigger Bill.",
     "short": "Rough sleeping gets £874m. TA is the bigger bill",
     "date": "2026-10-27", "tag": "Temporary accommodation",
     "desc": "Rough sleeping funding has almost doubled. But councils spent £2.93bn on temporary accommodation last year, with subsidy still frozen at 2011 rents."},
    {"slug": "westminster-city-council-pension-fund-50m-sale-and-leaseback-frees-up-capital-for-new-temporary-accommodation",
     "title": "Westminster City Council Pension Fund: £50m Sale-and-Leaseback Frees Up Capital for New Temporary Accommodation",
     "short": "Westminster Pension Fund: £50m sale-and-leaseback frees up capital for new TA",
     "date": "2026-07-29", "tag": "Transactions",
     "desc": "How a £50m, 40-year index-linked sale-and-leaseback with the City of Westminster Pension Fund released capital from 124 temporary accommodation properties to fund new supply."},
    {"slug": "london-social-housing-waiting-list-crisis-2026",
     "title": "London's Social Housing Waiting List Grows 30% in a Decade",
     "date": "2026-05-22", "tag": "Social housing",
     "desc": "London's social housing waiting list has grown 30% in a decade to 341,421 households. The data is in. This is a crisis made by policy choices."},
    {"slug": "uk-homelessness-crisis-breaking-point",
     "title": "Britain's Homelessness Crisis Has Reached a Breaking Point",
     "date": "2026-05-12", "tag": "Homelessness",
     "desc": "Record numbers of families are living in temporary accommodation. What is driving the crisis, why B&B placements are a national shame, and what must change."},
    {"slug": "renters-rights-act-2025-temporary-accommodation-homelessness",
     "title": "Renters' Rights Act 2025: What Councils Need to Know",
     "date": "2026-05-01", "tag": "Legislation",
     "desc": "The Renters' Rights Act has come into force. The ten key provisions and their impact on temporary accommodation and homelessness duties for local authorities."},
    {"slug": "frozen-out-what-a-rent-freeze-would-mean-for-social-housing-budgets",
     "title": "Frozen Out: What a Rent Freeze Would Mean for Social Housing Budgets",
     "date": "2026-04-28", "tag": "HRA and rents",
     "desc": "If a rent freeze were extended to social housing, interest cover, development programmes and repairs budgets would all take the hit. Why certainty matters more than headlines."},
    {"slug": "temporary-accommodation-mtfp-hclg-report-2026",
     "title": "Temporary Accommodation: When Does an Emergency Become the New Normal?",
     "date": "2026-04-24", "tag": "Temporary accommodation",
     "desc": "The HCLG Committee's latest report highlights the worsening temporary accommodation crisis. What it means for local authority finances, MTFPs and housing finance strategy."},
    {"slug": "section-151-officers-is-your-temporary-accommodation-strategy-financially-sustainable",
     "title": "Section 151 Officers: Is Your Temporary Accommodation Strategy Financially Sustainable?",
     "date": "2026-02-27", "tag": "Temporary accommodation",
     "desc": "Temporary accommodation is now one of the biggest structural pressures in the MTFP. How a 42-year institutional funding solution turned TA cost into owned supply for Westminster."},
    {"slug": "types-of-local-authority-company",
     "update": 'This article was written in 2020. The company structures described remain available, but the financing context has changed. Revised PWLB lending terms from 26 November 2020 mean councils that plan to buy investment assets primarily for yield cannot borrow from the PWLB, and later changes to the capital finance regulations have tightened the rules on Minimum Revenue Provision. Councils considering a company should take advice on how it will be financed, not just on its legal form.',
     "title": "Types of Local Authority Company",
     "date": "2020-09-15", "tag": "Housing companies",
     "desc": "Companies limited by shares or guarantee, CICs, community benefit societies and LLPs: the corporate structures available to councils and when each is appropriate."},
    {"slug": "what-is-a-local-authority-housing-company-and-why-set-one-up",
     "update": 'This article was written in 2020. Its central point still stands: check whether you need a company before setting one up. Since then, revised PWLB lending terms from 26 November 2020 have restricted borrowing by councils that plan to buy investment assets primarily for yield, and Right to Buy has changed significantly, with discounts cut in November 2024 and further reform in the Social Housing Bill [HL]. Both affect the case for a housing company.',
     "title": "What is a Local Authority Housing Company and Why Set One Up?",
     "date": "2020-07-23", "tag": "Housing companies",
     "desc": "What a council-owned private rented housing company is, why councils set them up, and why you should first check whether you need one at all."},
    {"slug": "can-right-to-buy-receipts-be-used-to-buy-s106-properties",
     "update": 'Some figures in this 2020 article are now out of date. Maximum Right to Buy discounts were cut on 21 November 2024 to between £16,000 and £38,000, depending on region. Since 2024/25 councils can keep 100% of their Right to Buy receipts, and changes in July 2024 removed the caps on acquisitions and allowed receipts to be combined with section 106 contributions, which is directly relevant to the question discussed here. The Social Housing Bill [HL] would make further changes, including a 10-year qualifying period.',
     "title": "Can Right to Buy Receipts Be Used to Buy S106 Properties?",
     "date": "2020-05-25", "tag": "Right to Buy",
     "desc": "Whether councils can use retained Right to Buy receipts to buy developer-led S106 affordable homes, with precedents from Epping Forest, Brighton and Hove, Cambridge and Tower Hamlets."},
]

# ---------------------------------------------------------------- service pages
SERVICE_PAGES = {}

SERVICE_PAGES["advisory-partnership"] = {
    "title": "Housing Finance Advisory Partnership for Local Authorities",
    "desc": "Unlimited access to specialist housing finance advice through a simple annual subscription. Supporting UK councils on HRA, homelessness, temporary accommodation and housing companies.",
    "h1": "Advisory Partnership",
    "lede": "Flexible, on-demand housing finance expertise for local authorities, through one annual subscription.",
    "body": """
<p class="intro-line">Expert housing finance advice, when you need it.</p>
<p>Managing housing finance in a local authority has never been more complex. From the pressures of the Housing Revenue Account to the growing cost of temporary accommodation and the governance demands of housing companies, finance teams are being asked to do more with less.</p>
<p>The Advisory Partnership gives your council direct, on-demand access to specialist housing finance expertise, without the cost and commitment of a full-time hire. Through a simple annual subscription, you get unlimited access to our consultants across the areas that matter most.</p>
<h2>What the partnership covers</h2>
<ul class="scope">
<li><b>Housing Revenue Account</b><span>Business planning, rent setting, self-financing, capital financing strategies, headroom analysis and 30-year plan modelling.</span></li>
<li><b>Homelessness and temporary accommodation</b><span>General Fund cost pressures, acquisition and funding strategies, and budget management.</span></li>
<li><b>Local authority housing companies</b><span>Governance, financial modelling, dividend strategies, and compliance with IFRS 16 and other accounting standards.</span></li>
</ul>
<p>Members can call, email or meet our team as often as needed. There are no per-query charges, no retainer limits and no surprise invoices: just consistent, expert support throughout the year.</p>
<h2>Why councils choose a subscription</h2>
<ul>
<li><strong>Cost-effective.</strong> A fraction of the cost of recruiting or retaining a specialist in-house.</li>
<li><strong>Immediate access.</strong> No procurement delays, no scoping exercises, no waiting for a project to be approved.</li>
<li><strong>Broad expertise.</strong> Our team has worked across district, borough, county and unitary authorities.</li>
<li><strong>Continuity.</strong> Your account is supported by the same consultants, who build deep knowledge of your organisation over time.</li>
<li><strong>Flexible.</strong> Scale up to a higher tier or commission additional project work at any time.</li>
</ul>
""",
    "faq": [
        ("How is the Advisory Partnership different from commissioning a project?",
         "A project engagement is scoped and time-limited. The Advisory Partnership is an ongoing relationship: your team can ask questions, sense-check decisions or request analysis at any point during the year, without raising a purchase order for each interaction."),
        ("Is there a minimum contract period?",
         "Subscriptions are typically annual. We can discuss shorter arrangements depending on your circumstances. Contact us to find out what works best for your authority."),
        ("Can we add project support during the subscription?",
         "Yes. Many members also commission us for larger pieces of work such as HRA business plan reviews, housing company establishment or financial appraisals. These are charged separately, but members benefit from priority scheduling and preferential rates."),
        ("Which tier of local authority is this suitable for?",
         "We work with district and borough councils, unitary authorities and London boroughs. If your authority holds a Housing Revenue Account, manages temporary accommodation or is exploring or operating a housing company, the Advisory Partnership will add value."),
    ],
}

SERVICE_PAGES["finance-business-partnering"] = {
    "title": "Finance Business Partnering for Local Authorities",
    "desc": "Specialist finance business partners embedded in your service teams. Supporting local authorities to improve performance, enable transformation and drive informed decision-making.",
    "h1": "Finance Business Partnering",
    "lede": "Embedding financial expertise at the heart of your public services.",
    "body": """
<p class="intro-line">The most effective local authority finance teams don't just report on numbers. They shape strategy, challenge assumptions and enable better decisions.</p>
<p>That is exactly what a skilled Finance Business Partner does. We provide experienced partners who work alongside your service teams, bringing financial rigour to operational decisions, helping managers understand the financial implications of their choices, and supporting your organisation to achieve its strategic objectives.</p>
<h2>What our business partners do</h2>
<ul>
<li>Act as a trusted financial adviser to service directors and senior managers</li>
<li>Analyse and interpret financial data in a clear, accessible way</li>
<li>Challenge assumptions and present options to support better decision-making</li>
<li>Support budget setting, forecasting and monitoring cycles</li>
<li>Help service teams understand their financial position and build financial literacy</li>
<li>Identify efficiency opportunities and contribute to transformation programmes</li>
<li>Produce business cases, options appraisals and investment proposals</li>
<li>Maintain financial stewardship and governance standards</li>
</ul>
<h2>Where we add most value</h2>
<p>Our partners are particularly effective in services going through significant change: a restructure, a new delivery model, a capital programme or a response to budget pressure. We bring the external perspective and specialist experience that internal teams often can't easily access.</p>
<p>We have supported housing, homelessness, regeneration, adult social care and commercial services within local authorities, as well as corporate finance functions undertaking transformation.</p>
""",
    "faq": [
        ("How is a Finance Business Partner different from a management accountant?",
         "A management accountant typically focuses on reporting, reconciliation and compliance. A Finance Business Partner goes further, actively engaging with service managers to influence decisions, challenge thinking and drive better outcomes. The role is more strategic and forward-looking."),
        ("Can you provide interim cover as well as long-term partnerships?",
         "Yes. We regularly provide interim Finance Business Partners to cover vacancies, maternity leave or periods of high demand. We can also support on a project basis where a specific transformation or programme needs dedicated financial input."),
        ("How quickly can you mobilise?",
         "We aim to start new engagements within two to four weeks. For urgent requirements, contact us directly to discuss availability."),
    ],
}

SERVICE_PAGES["financial-appraisals"] = {
    "buy_via": [
        ("NHS LPP DPS, Lot 9", "Estates Strategy and Business Case Development Services"),
        ("NHS LPP DPS, Lot 11", "Property Acquisition, Disposal and Management Advisory Services"),
        ("YPO 1141", "via Consultancy+, with direct award available"),
        ("NEPRO³", "via Bloom"),
    ],
    "title": "Financial Appraisals for Local Authorities",
    "desc": "Expert investment appraisals for UK local authorities. We assess project viability, risk and value for money across housing development, regeneration, commercial property and more.",
    "h1": "Financial Appraisals",
    "lede": "Rigorous, independent investment appraisals to support defensible public sector decisions.",
    "body": """
<p class="intro-line">Every significant decision a local authority makes carries financial risk.</p>
<p>Whether you are acquiring investment property, commissioning a new housing development, establishing a trading company or allocating capital across a regeneration programme, a robust appraisal makes sure costs are justified, risks are understood and the decision is defensible.</p>
<p>We combine deep knowledge of public sector finance with practical expertise in housing, regeneration and commercial activity to give you a thorough, independent assessment you can rely on.</p>
<h2>What we appraise</h2>
<ul class="scope">
<li><b>Investment property</b><span>Commercial, residential and mixed-use acquisitions.</span></li>
<li><b>Housing development</b><span>New build, regeneration and estate renewal programmes.</span></li>
<li><b>Housing companies</b><span>Viability of wholly-owned council housing company business models.</span></li>
<li><b>Private finance and partnerships</b><span>Risk transfer and value for money.</span></li>
<li><b>Temporary accommodation</b><span>Cost comparison of options and long-term financial modelling.</span></li>
<li><b>Developer viability</b><span>Review of Section 106 and affordable housing contributions.</span></li>
<li><b>Business cases</b><span>Outline and Full Business Cases for capital programmes.</span></li>
</ul>
<h2>Our approach</h2>
<p>We work closely with your finance, housing and legal teams to understand the objectives and constraints of each appraisal. Our outputs are clear, well-structured and designed to support internal decision-making and external scrutiny, including by overview and scrutiny committees, external auditors and government funders.</p>
<p>When we review viability assessments submitted by private developers, our goal is to make sure the affordable housing element of a scheme is maximised and that the council is not accepting less than it is entitled to.</p>
""",
    "faq": [
        ("At what stage should we commission a financial appraisal?",
         "As early as possible, before significant resources are committed. An early appraisal can show whether a project is viable in principle and what the key risk factors are. We also provide appraisals at later stages, for example to review assumptions before a final decision or to give independent challenge to an existing business case."),
        ("Can you challenge a developer viability assessment?",
         "Yes. We regularly review viability assessments submitted with planning applications, scrutinising the assumptions, identifying where inputs may be optimistic or conservative, and giving the council an independent view of what affordable housing contribution is achievable."),
        ("Do your appraisals meet Green Book requirements?",
         "Yes. Our investment appraisals for capital projects follow HM Treasury Green Book guidance, including options appraisal, benefit valuation and sensitivity analysis where required."),
    ],
}

SERVICE_PAGES["financial-reviews"] = {
    "title": "Financial Reviews for Local Authorities",
    "desc": "Independent financial reviews helping UK councils unlock ongoing revenue savings. We review MRP, HRA, debt management, fees and charges, and capital receipts strategies.",
    "h1": "Financial Reviews",
    "lede": "Independent technical reviews that find recurring savings hidden in plain sight.",
    "body": """
<p class="intro-line">Under sustained budget pressure, most councils have already made the obvious cuts.</p>
<p>Our experience across dozens of councils shows that significant ongoing savings often remain untapped. Not through waste or inefficiency, but simply because nobody has had the time or the external perspective to look.</p>
<p>We examine your existing policies, accounting treatments and financial strategies, compare them with current best practice, and identify where changes could generate meaningful, recurring savings.</p>
<h2>What we review</h2>
<ul class="scope">
<li><b>Minimum Revenue Provision</b><span>Your MRP policy, for compliance and optimisation opportunities.</span></li>
<li><b>Housing Revenue Account</b><span>Income, expenditure, reserves and 30-year business plan assumptions.</span></li>
<li><b>Debt management</b><span>Borrowing strategy, interest rate exposure and debt scheduling.</span></li>
<li><b>Capital receipts</b><span>How receipts are applied and whether more advantageous options exist.</span></li>
<li><b>Fees and charges</b><span>Benchmarking against comparable authorities and statutory guidance.</span></li>
<li><b>Treasury management</b><span>Investment strategy, counterparty limits and Prudential Code compliance.</span></li>
</ul>
<h2>What to expect</h2>
<p>A review typically takes four to eight weeks, depending on scope. You receive a clear, prioritised report of findings and recommendations, with an estimate of the financial benefit of each. We are transparent about the effort needed to implement changes and realistic about timescales.</p>
<p>Many clients tell us the savings identified in a single review more than cover the cost of the engagement, often many times over.</p>
""",
    "faq": [
        ("How much could a financial review save us?",
         "It varies with the size of your authority and the areas reviewed. MRP reviews alone have generated six-figure annual savings for some of our clients. We offer a free initial assessment to show where the opportunities are likely to be before you commit to a full engagement."),
        ("Is an MRP and debt review only relevant for authorities with large debt portfolios?",
         "No. The absolute savings are larger where there is more borrowing, but the principles of MRP optimisation apply to any authority with capital financing charges. Smaller district councils have also achieved meaningful savings."),
        ("Will your recommendations be acceptable to our external auditor?",
         "Yes. All our recommendations are grounded in legislation, statutory guidance and professional accounting standards. We can brief your external auditors if required and will help make sure any policy changes are properly documented and defensible."),
    ],
}

SERVICE_PAGES["project-management"] = {
    "buy_via": [
        ("NHS LPP DPS, Lot 5", "Construction Project Management Services"),
        ("YPO 1141", "via Consultancy+, with direct award available"),
        ("NEPRO³", "via Bloom"),
    ],
    "title": "Project Management for Local Authorities",
    "desc": "Specialist project management support for UK local authorities. From business case development to programme delivery, we help councils achieve their corporate objectives.",
    "h1": "Project Management",
    "lede": "Delivering complex public sector programmes on time and on budget.",
    "body": """
<p class="intro-line">Public sector projects face a unique set of challenges.</p>
<p>They are highly scrutinised, must navigate complex governance, often depend on government funding with strict compliance requirements, and are delivered by teams that are already stretched.</p>
<p>We bring the structure, discipline and experience needed to keep programmes on track, whether you need a business case drafted, a funded capital programme managed or a transformation project overseen from start to finish.</p>
<h2>What we deliver</h2>
<ul class="scope">
<li><b>Business cases</b><span>Outline and Full Business Cases to HM Treasury Green Book and funding body requirements.</span></li>
<li><b>Funded capital projects</b><span>Compliance reporting, grant drawdown management and funder liaison.</span></li>
<li><b>Peer review and challenge</b><span>Independent review of project plans, risk registers and governance arrangements.</span></li>
<li><b>Budget and year-end</b><span>Financial planning and close-down support for complex programmes.</span></li>
<li><b>Programme governance</b><span>PMO functions, reporting frameworks and escalation procedures.</span></li>
<li><b>Stakeholder management</b><span>Engagement with elected members, government departments, partners and communities.</span></li>
</ul>
<h2>Our track record</h2>
<p>Our team has delivered project management across housing development, regeneration, service transformation and commercial activity within local government. We understand the political and organisational dynamics of public sector delivery and how to navigate them.</p>
""",
    "faq": [
        ("Can you provide project management on an interim basis?",
         "Yes. We regularly provide project managers and programme directors on an interim basis to cover capacity gaps, provide specialist expertise or support a specific phase of delivery. Engagements range from a few weeks to over a year."),
        ("Do you work with Homes England or MHCLG-funded programmes?",
         "Yes. We have managed projects funded through Homes England, MHCLG and other government bodies, and understand the monitoring, reporting and compliance requirements involved."),
        ("Can you help us write a business case for a housing scheme?",
         "Yes. We regularly produce Outline and Full Business Cases for housing development and regeneration projects, including those needing Green Book compliance, working closely with your housing, finance and legal teams."),
    ],
}

SERVICE_PAGES["training"] = {
    "title": "Housing Finance Training for Local Authorities",
    "desc": "Specialist housing finance training for UK councils. Seminars, in-house sessions and webinars covering HRA, MRP, housing companies, temporary accommodation and more.",
    "h1": "Training and Development",
    "lede": "Expert-led housing finance training for local authority teams.",
    "body": """
<p class="intro-line">The legislative, regulatory and financial landscape for council housing never stands still.</p>
<p>New legislation, revised accounting standards, changing government policy and cost-of-living pressures all place new demands on housing finance professionals.</p>
<p>Our trainers are active practitioners who bring real-world experience from working across dozens of councils, not just theory. Every session is practical, accessible and directly applicable to participants' day-to-day roles.</p>
<h2>Formats</h2>
<ul class="scope">
<li><b>Regional seminars</b><span>Full and half-day events bringing together finance professionals from several authorities.</span></li>
<li><b>In-house training</b><span>Bespoke sessions on-site or online, tailored to your authority and team.</span></li>
<li><b>Webinars</b><span>Shorter, focused sessions, live or on demand.</span></li>
</ul>
<h2>Topics</h2>
<ul>
<li><strong>Housing Revenue Account:</strong> fundamentals, business planning, rent setting and self-financing</li>
<li><strong>Minimum Revenue Provision:</strong> policy options, accounting treatment and recent case law</li>
<li><strong>Temporary accommodation:</strong> financial management, cost pressures and funding options</li>
<li><strong>Housing companies:</strong> establishing, governing and accounting for wholly-owned companies</li>
<li><strong>Capital financing:</strong> borrowing, the Prudential Code and treasury management basics</li>
<li><strong>Housing development finance:</strong> development appraisals, viability and grant funding</li>
<li><strong>Financial resilience:</strong> budget management under pressure, reserves strategy and medium-term planning</li>
</ul>
<p>If you have a topic or team need that isn't listed, get in touch. We regularly develop bespoke training in response to client requests.</p>
""",
    "faq": [
        ("How do we arrange in-house training?",
         "Tell us your team's size, current knowledge level and the topics you are most interested in. We will design a session for you and provide a quote. Most in-house sessions can be arranged within four to six weeks."),
        ("Are webinars available after the live event?",
         "Yes. Recordings are made available to registered participants afterwards. Ask us about on-demand access when you enquire."),
        ("Do you offer discounts for multiple bookings or consortia?",
         "Yes. We work with regional finance networks and consortia to deliver cost-effective shared training, and are happy to coordinate sessions with neighbouring authorities."),
    ],
}


# ---------------------------------------------------------------- case studies
# Shown on /case-studies; those with "home": True also appear on the homepage.
CASE_STUDIES = [
    {"id": "weyside", "home": True,
     "client": "Guildford Borough Council",
     "title": "Weyside Urban Village",
     "headline": "Finance lead on a £467m regeneration programme",
     "figure": "£467m", "figure_label": "regeneration programme delivering around 1,500 new homes",
     "facts": [("Scheme", "1,500 new homes, community facilities and a new council depot on a Thames Water site"),
               ("Our role", "Finance lead, replacing a Big Four firm"),
               ("Funding", "Housing Infrastructure Fund, Enterprise M3 LEP and discounted PWLB borrowing")],
     "summary": "Guildford Borough Council brought us in to replace a Big Four firm as finance lead for its Weyside Urban Village regeneration programme.",
     "body": [
        "The programme sought to deliver around 1,500 new homes, new community facilities and a new council depot on a Thames Water site, with a total cost of £467m.",
        "We produced the development appraisal, assessed the project's viability, and identified the funding and disposal solutions needed to make it deliverable.",
     ],
     "did": ["Development appraisal and viability assessment for the whole programme",
             "Funding and disposal strategy",
             "Housing Infrastructure Fund (HIF) application, grant claims and ongoing monitoring",
             "Enterprise M3 LEP funding application and monitoring",
             "Access to discounted PWLB borrowing",
             "Ongoing financial modelling and cashflow management"],
     "testimonial": 0},
    {"id": "waverley", "home": True,
     "client": "Waverley Borough Council",
     "title": "Appraisals for new council homes",
     "headline": "Independent appraisals that move housing schemes forward",
     "figure": "", "figure_label": "",
     "facts": [("Work", "Development appraisals and acquisition appraisals"),
               ("Focus", "Hurdle rates, default values and best-practice benchmarking"),
               ("Outcome", "Stronger investment business cases")],
     "summary": "We provide Waverley with detailed, independent development appraisals that strengthen the business case for delivering new homes on council-owned sites.",
     "body": [
        "Each appraisal tests the scheme's hurdle rates and default values and benchmarks them against best practice, so decisions rest on assumptions that stand up to scrutiny.",
        "Our independent reports have strengthened the Council's business cases for investment, helping it advance the delivery of new homes and appraise acquisition opportunities with confidence.",
     ],
     "did": ["Detailed development appraisals for council-owned sites",
             "Assessment of hurdle rates and default values",
             "Benchmarking against best practice",
             "Independent appraisal of acquisition opportunities"],
     "testimonial": 1},
    {"id": "gosport", "home": True,
     "client": "Portsmouth City Council · One Public Estate",
     "title": "From housing depot to new homes",
     "headline": "Making a challenging site viable",
     "figure": "", "figure_label": "",
     "facts": [("Commissioned by", "Portsmouth City Council, through One Public Estate"),
               ("Site", "Gosport Borough Council's former housing depot"),
               ("Challenge", "Difficult local development viability")],
     "summary": "Gosport faces particular challenges around development viability. In a One Public Estate commission from Portsmouth City Council, we helped Gosport Borough Council find new ways to turn its old housing depot into new homes.",
     "body": [
        "At the time, Portsmouth City Council's management team also ran Gosport Borough Council, so the commission came through Portsmouth.",
        "Conventional approaches would not make the scheme stack up, so the Council needed to consider innovative ways to achieve development.",
        "Working through the One Public Estate programme, we identified options that made the redevelopment of the old housing depot into new homes a viable reality.",
     ],
     "did": ["Viability analysis of the depot site",
             "Identification of innovative delivery and funding options",
             "Options to overcome viability barriers"],
     "testimonial": 3},
    {"id": "westminster-institutional", "home": False,
     "client": "Westminster City Council",
     "title": "Institutional funding for temporary accommodation",
     "headline": "368 homes brought into council control",
     "figure": "368", "figure_label": "homes acquired that were previously leased as temporary accommodation",
     "facts": [("Term", "42 years, index-linked"), ("Retrofit", "£33.5m embedded in the structure"),
               ("Outcome", "Assets unencumbered at lease expiry")],
     "summary": "A 42-year institutional funding solution that enabled Westminster to acquire 368 homes it previously leased for temporary accommodation.",
     "body": [
        "Volatile nightly accommodation costs were replaced with structured, index-linked payments, giving the Council long-term control of supply and unencumbered ownership of the homes when the lease ends.",
        "The structure also embedded £33.5m of retrofit funding to improve the homes.",
     ],
     "did": ["Led the funding structure", "Financial modelling and appraisal", "Retrofit funding built into the deal"],
     "article": "section-151-officers-is-your-temporary-accommodation-strategy-financially-sustainable",
     "testimonial": None},
    {"id": "westminster-pension", "home": False,
     "client": "City of Westminster Pension Fund",
     "title": "Pension fund sale and leaseback",
     "headline": "£50m released from existing stock",
     "figure": "£50m", "figure_label": "capital released from existing temporary accommodation stock",
     "facts": [("Term", "40 years, index-linked"), ("Portfolio", "124 properties via a council-owned LLP"),
               ("Outcome", "Receipt reinvested in new TA supply")],
     "summary": "A £50m sale and leaseback between Westminster City Council and its own pension fund, releasing capital from 124 temporary accommodation properties.",
     "body": [
        "The Council sold and leased back 124 existing TA properties to a council-owned LLP, funded by a 40-year, index-linked loan from the Pension Fund that matches the fund's own long-term liabilities.",
        "The capital receipt can be reinvested in additional TA supply, while the Council keeps full use of the properties under the leaseback.",
     ],
     "did": ["Designed and led the funding structure", "Council-owned LLP arrangement", "Matched the fund's liability profile"],
     "article": "westminster-city-council-pension-fund-50m-sale-and-leaseback-frees-up-capital-for-new-temporary-accommodation",
     "testimonial": None},
]

ABOUT_NICK = {
    "lede": "Led by Nick Haverly FCPFA, our team combines technical expertise with first-hand experience of council finance. We work alongside you to turn complex challenges into clear, practical next steps.",
    "points": [
        "Fellow of CIPFA (FCPFA)",
        "Former Housing Adviser to the Local Government Association",
        "Former member of the Cabinet Office's One Public Estate Pool of Experts",
        "Led two major temporary accommodation funding structures for Westminster City Council",
        "Financial lead on award-winning property, energy and regeneration schemes across the UK",
    ],
}


# ------------------------------------------------------------ Section 151 hub
# Every date and link below was checked against the official source on
# 27 October 2026. Re-check each autumn (S151_CHECKED) before the budget cycle.
S151_CHECKED = "2026-10-27"

# The annual cycle in England: (when, what, source label, source url)
S151_CALENDAR = [
    ("1 April", "New financial year begins. New social rents take effect, within the limit set by the Rent Standard.",
     "Rent Standard and guidance", "https://www.gov.uk/government/collections/rent-standard-and-guidance"),
    ("Quarterly", "Report treasury management activity and prudential indicators. Quarters 2 and 4 normally go to full council or the executive.",
     "CIPFA Prudential Code", "https://cipfa.org/policy-and-guidance/publications/t/the-prudential-code-for-capital-finance-in-local-authorities-2021-edition"),
    ("By 30 June", "Publish the draft (unaudited) statement of accounts and annual governance statement.",
     "Accounts and Audit Regulations 2015", "https://www.legislation.gov.uk/uksi/2015/234/contents"),
    ("Summer to autumn", "Report the annual treasury management review of the previous year to members.",
     "CIPFA Treasury Management Code", "https://cipfa.org/policy-and-guidance/publications/t/treasury-management-in-the-public-services-code-of-practice-and-crosssectoral-guidance-notes-2021-edition"),
    ("Autumn", "UK Budget. Refresh the medium-term financial strategy and test the assumptions behind next year's budget.",
     None, None),
    ("December", "Provisional local government finance settlement, usually published in mid to late December.",
     "Local government finance settlement", "https://www.gov.uk/government/collections/final-local-government-finance-settlement-england-2026-2027-to-2028-2029"),
    ("1 December to 31 January", "Billing authorities calculate the council tax base and notify precepting authorities.",
     "Council tax base regulations", "https://www.legislation.gov.uk/uksi/2012/2914/contents"),
    ("January to February", "Set rents and the HRA budget for April, update the HRA 30-year business plan and give tenants notice of rent changes.",
     "Policy statement on rents", "https://www.gov.uk/government/publications/direction-on-the-rent-standard-2026/policy-statement-on-rents-for-social-housing"),
    ("February", "Final settlement. Full council approves the budget, capital strategy, treasury management strategy and MRP statement, with the chief finance officer's section 25 report on the robustness of estimates and adequacy of reserves.",
     "Local Government Act 2003, s25", "https://www.legislation.gov.uk/ukpga/2003/26/section/25"),
    ("Before 1 March", "Major precepting authorities issue their precepts.",
     "Local Government Finance Act 1992, s40", "https://www.legislation.gov.uk/ukpga/1992/14/section/40"),
    ("Before 11 March", "Billing authorities set council tax for the coming year.",
     "Local Government Finance Act 1992, s30", "https://www.legislation.gov.uk/ukpga/1992/14/section/30"),
    ("1 to 31 March", "Submit capital spending and borrowing plans for the current year and next two years to the PWLB, with the section 151 officer's assurance on investment assets bought primarily for yield.",
     "PWLB guidance for applicants", "https://www.dmo.gov.uk/media/qa2npqvv/pwlb-guidance-for-applicants-for-publishing-november.pdf"),
]

# Audit backstop dates (England), from the written ministerial statement of 4 March 2025
S151_BACKSTOPS = [
    ("2025/26", "31 January 2027"),
    ("2026/27", "30 November 2027"),
    ("2027/28", "30 November 2028"),
]
S151_BACKSTOP_SOURCE = "https://questions-statements.parliament.uk/written-statements/1780736"

# Guidance library: (group, [(title, url, note)])
S151_LIBRARY = [
    ("The role", [
        ("Local Government Act 1972, section 151", "https://www.legislation.gov.uk/ukpga/1972/70/section/151",
         "The duty to make arrangements for the proper administration of financial affairs, and to appoint an officer responsible for them."),
        ("Local Government Finance Act 1988, section 114", "https://www.legislation.gov.uk/ukpga/1988/41/section/114",
         "When the chief finance officer must report unlawful expenditure or an unbalanced budget."),
        ("Local Government Act 2003, section 25", "https://www.legislation.gov.uk/ukpga/2003/26/section/25",
         "The report on the robustness of budget estimates and the adequacy of reserves."),
        ("CIPFA: The role of the chief financial officer in local government", "https://www.cipfa.org/policy-and-guidance/reports/the-role-of-the-chief-financial-officer-in-local-government",
         "CIPFA's statement of the principles and responsibilities of the role."),
        ("CIPFA Financial Management Code", "https://www.cipfa.org/fmcode",
         "Standards of financial management for local authorities."),
        ("Best value standards and intervention: statutory guide", "https://www.gov.uk/government/publications/best-value-standards-and-intervention-a-statutory-guide-for-best-value-authorities/best-value-standards-and-intervention-a-statutory-guide-for-best-value-authorities",
         "The characteristics of a well-functioning authority, including on finance, and how government intervenes."),
    ]),
    ("Capital and treasury", [
        ("CIPFA Prudential Code (2021 edition)", "https://cipfa.org/policy-and-guidance/publications/t/the-prudential-code-for-capital-finance-in-local-authorities-2021-edition",
         "The framework for affordable, prudent and sustainable capital investment and borrowing."),
        ("CIPFA Treasury Management Code (2021 edition)", "https://cipfa.org/policy-and-guidance/publications/t/treasury-management-in-the-public-services-code-of-practice-and-crosssectoral-guidance-notes-2021-edition",
         "The code of practice for treasury management in the public services."),
        ("Minimum revenue provision: statutory guidance (5th edition)", "https://www.gov.uk/government/publications/capital-finance-guidance-on-minimum-revenue-provision-third-edition/capital-finance-guidance-on-minimum-revenue-provision-5th-edition",
         "Applies to accounting periods starting on or after 1 April 2025."),
        ("Local government investments: statutory guidance (3rd edition)", "https://www.gov.uk/government/publications/capital-finance-guidance-on-local-government-investments-second-edition",
         "Guidance on treasury and non-treasury investments, applying from 1 April 2018."),
        ("Capital Finance and Accounting Regulations 2003", "https://www.legislation.gov.uk/uksi/2003/3146/contents",
         "The regulations behind MRP, capital receipts and the use of capital resources in England."),
        ("PWLB lending arrangements", "https://dmo.gov.uk/responsibilities/local-authority-lending/lending-arrangements",
         "The Debt Management Office's lending facility, rates and terms."),
        ("PWLB guidance for applicants", "https://www.dmo.gov.uk/media/qa2npqvv/pwlb-guidance-for-applicants-for-publishing-november.pdf",
         "Eligibility, the annual capital plan return and the section 151 officer's assurance."),
    ]),
    ("Funding and financial resilience", [
        ("Final local government finance settlement 2026-27 to 2028-29", "https://www.gov.uk/government/collections/final-local-government-finance-settlement-england-2026-2027-to-2028-2029",
         "The multi-year settlement for English councils."),
        ("Exceptional financial support for local authorities", "https://www.gov.uk/government/collections/exceptional-financial-support-for-local-authorities",
         "How the government supports councils that cannot set a balanced budget, and the support agreed to date."),
        ("CIPFA Financial Resilience Index", "https://www.cipfa.org/services/financial-resilience-index",
         "Comparative indicators of financial resilience for English councils."),
    ]),
    ("Accounts and audit", [
        ("Accounts and Audit Regulations 2015", "https://www.legislation.gov.uk/uksi/2015/234/contents",
         "Requirements for internal control, the annual governance statement and publishing accounts."),
        ("Audit backstop dates: written ministerial statement", "https://questions-statements.parliament.uk/written-statements/1780736",
         "The statutory backstop dates for accounts and audit, set out on 4 March 2025."),
        ("CIPFA/LASAAC Code of Practice on Local Authority Accounting", "https://cms.cipfa.org/policy-and-guidance/cipfa-lasaac-local-authority-code-board/code-of-practice",
         "The accounting code that statements of accounts must follow."),
    ]),
    ("Housing and the HRA", [
        ("Rent Standard and guidance", "https://www.gov.uk/government/collections/rent-standard-and-guidance",
         "The Regulator of Social Housing's Rent Standard, which applies to council landlords."),
        ("Policy statement on rents for social housing", "https://www.gov.uk/government/publications/direction-on-the-rent-standard-2026/policy-statement-on-rents-for-social-housing",
         "The government's rent policy from 1 April 2026."),
    ]),
]

# Insight tags shown on the hub
S151_TAGS = {"Temporary accommodation", "HRA and rents", "Borrowing and treasury", "Housing companies",
             "Transactions", "Budget 2026", "Homelessness", "Social housing"}

# Key figures panel: (label, figure, detail, source label, source url, as at)
# Refreshed monthly by scheduled task, with Nick's approval. Checked 27 October 2026.
S151_FIGURES = [
    ("2024/25 audit opinions", "248 of 433",
     "issued were disclaimed or qualified, 240 of them because of the backstop. 185 were unmodified and 24 were still outstanding.",
     "PSAA", "https://www.psaa.co.uk/2026/05/may-2026-update/", "31 March 2026"),
    ("Non-ringfenced reserves", "£31.1bn",
     "held by English councils at 31 March 2026, up £0.9bn in the year. Councils added £660m to reserves in 2025-26, after drawing £766m in 2024-25.",
     "MHCLG revenue outturn", "https://www.gov.uk/government/statistics/local-authority-revenue-expenditure-and-financing-england-2025-to-2026-first-release/local-authority-revenue-expenditure-and-financing-england-2025-to-2026-first-release", "17 September 2026"),
    ("Exceptional Financial Support", "36 councils",
     "have in-principle support for 2026-27, worth around £1.5bn in total.",
     "GOV.UK", "https://www.gov.uk/guidance/exceptional-financial-support-for-local-authorities-for-2026-27", "updated 18 August 2026"),
    ("Homelessness spending", "£2.3bn",
     "net in 2025-26, two thirds of councils' net housing spending outside the HRA. Gross spending was £4.0bn.",
     "MHCLG revenue outturn", "https://www.gov.uk/government/statistics/local-authority-revenue-expenditure-and-financing-england-2025-to-2026-first-release/local-authority-revenue-expenditure-and-financing-england-2025-to-2026-first-release", "17 September 2026"),
    ("Default council tax referendum limits", "3% + 2%",
     "core principle plus adult social care precept, 2026-27 to 2028-29. These are the defaults: a number of councils have different limits or exemptions under the settlement, so check your own council's position.",
     "Core spending power note", "https://www.gov.uk/government/publications/explanatory-note-on-core-spending-power-final-local-government-finance-settlement-2026-27-to-2028-29/explanatory-note-on-core-spending-power-final-local-government-finance-settlement-2026-27-to-2028-29", "February 2026"),
    ("Social rent cap, 2027/28", "4.5%",
     "the expected limit: September 2026 CPI of 3.5% plus 1%, under the Rent Standard. The Regulator confirms the limit each year.",
     "ONS", "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/september2026", "21 October 2026"),
    ("Bank Rate", "3.75%",
     "held by the Bank of England's Monetary Policy Committee on 17 September 2026. CPI inflation was 3.5% in September.",
     "Bank of England", "https://www.bankofengland.co.uk/monetary-policy/the-interest-rate-bank-rate", "17 September 2026"),
]

# Compare-your-council data: regenerate with _build/data_reserves.py and _build/data_audit.py
S151_RESERVES_YEAR = "2025-26"
S151_RESERVES_PUBLISHED = "17 September 2026"

# Data insights: England total non-ringfenced reserves (other earmarked, adjusted where MHCLG provides it,
# plus unallocated) at 31 March, and net revenue expenditure for the year, £bn. From each year's
# revenue outturn summary (RS), all English local authorities. Add one point each autumn.
S151_RESERVES_TREND = [
    ("31 March 2022", 33.93, 60.77),
    ("31 March 2023", 31.53, 64.99),
    ("31 March 2024", 30.47, 70.09),
    ("31 March 2025", 30.38, 74.35),
    ("31 March 2026", 31.14, 76.74),
]
