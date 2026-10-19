#!/usr/bin/env python3
"""Builds the static content pages (guides, about, contact, privacy, disclosure) and sitemap.xml.
Run: python3 build.py   (index.html is hand edited and left alone)."""
import json, os, re

BASE = "https://imthiyasyusuf1-dotcom.github.io/true-car-cost-uk/"
TODAY = "2026-10-18"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = "https://github.com/imthiyasyusuf1-dotcom/true-car-cost-uk"
FORM_ID = "a86053f34787b30fb53795886dc44aad"  # FormSubmit hashed endpoint (activated), forwards privately

CSS = """
:root{--bg:#0d0f12;--panel:#15181d;--panel2:#1b1f26;--line:#262b34;--text:#eef0f3;--muted:#9aa2af;--accent:#d8ff3e;--ink:#0d0f12}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--text);font:16px/1.65 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.wrap{max-width:760px;margin:0 auto;padding:22px 20px 60px}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:30px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:17px;color:var(--text);text-decoration:none}
.logo i{display:grid;place-items:center;width:32px;height:32px;border-radius:9px;background:var(--accent);color:var(--ink);font-style:normal;font-weight:900}
nav{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}
nav a{color:var(--muted);text-decoration:none}nav a:hover{color:var(--text)}
.crumbs{font-size:13px;color:var(--muted);margin-bottom:10px}.crumbs a{color:var(--muted)}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin-bottom:14px}
h2{font-size:22px;letter-spacing:-.02em;margin:32px 0 10px}
h3{font-size:17px;margin:22px 0 6px}
p,ul,ol,table{margin-bottom:14px}
ul,ol{padding-left:22px}li{margin-bottom:6px}
.lede{color:var(--muted);font-size:18px}
.meta{color:var(--muted);font-size:13px;margin-bottom:24px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:20px 0}
.cta{display:inline-block;background:var(--accent);color:var(--ink);font-weight:800;text-decoration:none;padding:12px 18px;border-radius:12px;margin-top:6px}
table{width:100%;border-collapse:collapse;font-size:15px}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.cards{display:grid;gap:14px}
.cards a{display:block;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px 18px;text-decoration:none;color:var(--text)}
.cards a strong{display:block;font-size:17px;margin-bottom:4px}
.cards a span{color:var(--muted);font-size:14.5px}
footer{margin-top:50px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
footer nav{margin-bottom:10px}
.cform label{display:block;font-size:14px;color:var(--muted);margin:14px 0 4px}
.cform input,.cform select,.cform textarea{display:block;width:100%;background:var(--panel2);border:1px solid #333a45;border-radius:10px;color:var(--text);font:inherit;padding:10px 12px;-webkit-appearance:none;appearance:none}
.cform input,.cform select{height:46px;line-height:24px}
.cform select{padding-right:36px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%239aa2af' stroke-width='2'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center}
.cform input:focus,.cform select:focus,.cform textarea:focus{outline:none;border-color:var(--accent)}
.cform textarea{resize:vertical}
.cform button{display:block;width:100%;height:48px;padding:0 18px;border:0;cursor:pointer;font:inherit;font-weight:800;margin-top:18px}
"""

NAV = [("Calculator", ""), ("Guides", "guides/"), ("About", "about/"), ("Contact", "contact/")]
FOOT = [("Calculator", ""), ("Guides", "guides/"), ("About", "about/"), ("Contact", "contact/"),
        ("Privacy", "privacy/"), ("Affiliate disclosure", "affiliate-disclosure/")]


def page(path, title, desc, body, crumbs=None, article=None, h1=None):
    depth = path.count("/")
    rel = "../" * depth
    url = BASE + path
    nav = "".join(f'<a href="{rel}{h}">{t}</a>' for t, h in NAV)
    foot = "".join(f'<a href="{rel}{h}">{t}</a>' for t, h in FOOT)
    ld = []
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
        for i, (n, h) in enumerate(crumbs, 2):
            items.append({"@type": "ListItem", "position": i, "name": n, "item": BASE + h})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if article:
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": h1 or title,
                   "description": desc, "inLanguage": "en-GB", "datePublished": TODAY, "dateModified": TODAY,
                   "mainEntityOfPage": url, "image": BASE + "og.png",
                   "author": {"@type": "Organization", "name": "True Car Cost UK", "url": BASE},
                   "publisher": {"@type": "Organization", "name": "True Car Cost UK", "url": BASE}})
    ldtags = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>\n' for x in ld)
    crumb_html = ""
    if crumbs:
        parts = [f'<a href="{rel}">Home</a>'] + [f'<a href="{rel}{h}">{n}</a>' for n, h in crumbs[:-1]] + [crumbs[-1][0]]
        crumb_html = '<div class="crumbs">' + " / ".join(parts) + "</div>"
    meta = f'<p class="meta">Updated 18 October 2026</p>' if article else ""
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="True Car Cost UK">
<meta property="og:locale" content="en_GB">
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{h1 or title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d0f12">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23d8ff3e'/%3E%3Ctext x='32' y='44' font-family='Arial' font-weight='900' font-size='34' text-anchor='middle' fill='%230d0f12'%3E%C2%A3%3C/text%3E%3C/svg%3E">
{ldtags}<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><a class="logo" href="{rel}"><i>£</i>True Car Cost</a><nav>{nav}</nav></header>
<main>
{crumb_html}
<h1>{h1 or title}</h1>
{meta}
{body.replace('{rel}', rel)}
</main>
<footer><nav>{foot}</nav>Rough guides, not financial advice. Check your own quotes and the official GOV.UK pages before you sign anything.</footer>
</div>
</body>
</html>
"""
    out = os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    return path


CALC_BOX = '<div class="box"><strong>Try it with your own numbers.</strong><br>The free calculator adds finance, fuel, insurance, tax and the rest into one monthly figure and shows what share of your take home pay it uses.<br><a class="cta" href="{rel}">Open the car cost calculator</a></div>'

GUIDES = []


def guide(slug, title, h1, desc, blurb, body):
    GUIDES.append((slug, h1, blurb))
    return page(f"guides/{slug}/", title, desc, body, crumbs=[("Guides", "guides/"), (h1, f"guides/{slug}/")], article=True, h1=h1)


# ---------------- Guides ----------------
guide("true-cost-of-running-a-car-uk",
      "How Much Does It Cost to Run a Car in the UK? Monthly Breakdown",
      "How much does it really cost to run a car in the UK?",
      "A line by line monthly breakdown of what a typical used car costs to run in the UK: finance, fuel, insurance, road tax, MOT, servicing, tyres, parking and breakdown cover.",
      "A line by line monthly breakdown for a typical used car, with the figures worked out.",
      """
<p class="lede">The monthly payment on the advert is usually less than half of what the car really costs you. Here is a worked example for an ordinary used hatchback, line by line.</p>

<h2>The example car</h2>
<p>A £16,000 used car bought on PCP with a £2,000 deposit, 9.9% APR over 48 months and a £6,500 balloon at the end. The driver does 8,000 miles a year, gets 45 mpg and pays 138p a litre for fuel.</p>

<table>
<tr><th>Cost</th><th class="n">Per month</th><th class="n">Per year</th></tr>
<tr><td>Finance payment</td><td class="n">£240</td><td class="n">£2,876</td></tr>
<tr><td>Deposit spread over the 4 years</td><td class="n">£42</td><td class="n">£500</td></tr>
<tr><td>Fuel (8,000 miles at 45 mpg)</td><td class="n">£93</td><td class="n">£1,115</td></tr>
<tr><td>Insurance</td><td class="n">£75</td><td class="n">£900</td></tr>
<tr><td>Road tax</td><td class="n">£16</td><td class="n">£195</td></tr>
<tr><td>Service and MOT</td><td class="n">£25</td><td class="n">£300</td></tr>
<tr><td>Tyres and repairs</td><td class="n">£21</td><td class="n">£250</td></tr>
<tr><td>Parking</td><td class="n">£20</td><td class="n">£240</td></tr>
<tr><td>Breakdown cover</td><td class="n">£5</td><td class="n">£60</td></tr>
<tr><td><strong>Total</strong></td><td class="n"><strong>£536</strong></td><td class="n"><strong>£6,436</strong></td></tr>
</table>

<p>So a car advertised at "£240 a month" really costs about £536 a month, or roughly 80p for every mile driven. On a £28,000 salary that is around 27% of take home pay, which is a lot.</p>

<h2>Where the money goes</h2>
<h3>Finance or depreciation</h3>
<p>This is normally the biggest single cost. If you pay cash there is no monthly payment, but the car still loses value every year. A car that drops 15% a year costs you about £200 a month in lost value at £16,000, so cash is not free. Our <a href="{rel}guides/pcp-vs-hp/">PCP vs HP guide</a> shows how the finance types compare.</p>
<h3>Fuel</h3>
<p>Fuel cost depends on three things: miles, mpg and the pump price. A UK gallon is 4.546 litres, so at 45 mpg and 138p a litre, each mile costs about 14p in fuel. Drop to 35 mpg and the same 10,000 miles a year goes from about £1,394 to £1,792.</p>
<h3>Insurance</h3>
<p>For younger drivers and anyone in a city, insurance can be bigger than the finance payment. It is also the cost you can change most easily. See <a href="{rel}guides/cut-car-insurance-cost/">how to cut your car insurance</a>.</p>
<h3>Road tax, MOT and servicing</h3>
<p>Most cars registered since April 2017 pay a flat standard rate of road tax after the first year, with an extra yearly charge in years 2 to 6 if the list price was over £40,000. Electric cars have paid road tax since April 2025. Check the current figures on <a href="https://www.gov.uk/vehicle-tax-rate-tables" rel="noopener">GOV.UK</a>. An MOT is needed once a car is three years old and the maximum fee for a car is £54.85. A basic service at an independent garage is usually a few hundred pounds a year.</p>
<h3>The small stuff</h3>
<p>Tyres, wiper blades, a cracked windscreen, parking permits, tolls and breakdown cover add up. Budgeting £20 to £40 a month for this is sensible for an older car.</p>

<h2>Rules of thumb</h2>
<ul>
<li>Keep the total cost of the car under about 15% of take home pay. Under 10% is comfortable.</li>
<li>Expect the real monthly cost to be roughly double the finance payment.</li>
<li>Work out the cost per mile. If it is well over 50p and you do few miles, a cheaper car, car club or train might make more sense. Our <a href="{rel}guides/car-cost-per-mile/">cost per mile guide</a> explains how.</li>
</ul>
""" + CALC_BOX)

guide("pcp-vs-hp",
      "PCP vs HP: Which Car Finance Is Cheaper? Worked UK Example",
      "PCP vs HP: which car finance works out cheaper?",
      "PCP vs HP explained with real numbers. Same £16,000 car, same deposit and APR: monthly payments, total interest and what you pay if you keep the car.",
      "Same car, same deposit and APR, two finance types. The real numbers side by side.",
      """
<p class="lede">PCP gives you a lower monthly payment. HP gives you the car. Which is cheaper depends on what you plan to do at the end, so here are the numbers.</p>

<h2>Same car, two deals</h2>
<p>A £16,000 car, £2,000 deposit, 9.9% APR, 48 months. The PCP deal has a £6,500 balloon payment (the guaranteed future value) at the end.</p>
<table>
<tr><th></th><th class="n">PCP</th><th class="n">HP</th></tr>
<tr><td>Monthly payment</td><td class="n">£240</td><td class="n">£352</td></tr>
<tr><td>Total interest</td><td class="n">£4,005</td><td class="n">£2,875</td></tr>
<tr><td>Paid over 4 years (deposit plus payments)</td><td class="n">£13,505</td><td class="n">£18,875</td></tr>
<tr><td>Total if you keep the car</td><td class="n">£20,005</td><td class="n">£18,875</td></tr>
<tr><td>Who owns it after the last payment?</td><td class="n">The lender, unless you pay the balloon</td><td class="n">You</td></tr>
</table>
<p>If you want to keep the car, HP is about £1,130 cheaper here. That is because on PCP you borrow the balloon amount for the whole four years and pay interest on it the whole time.</p>

<h2>When PCP makes sense</h2>
<ul>
<li>You want a newer car every three or four years and will hand it back or part exchange it.</li>
<li>You are confident you will stay under the mileage limit. Going over usually costs a set amount per mile, often somewhere between 5p and 15p.</li>
<li>You will look after the bodywork, because "fair wear and tear" is checked when you hand it back.</li>
</ul>

<h2>When HP makes sense</h2>
<ul>
<li>You plan to keep the car for years after the finance ends. The payment then disappears and the car is yours.</li>
<li>You do high mileage. HP has no mileage limit.</li>
<li>You want to be able to sell or modify the car once it is paid off without asking anyone.</li>
</ul>

<h2>Rights that apply to both</h2>
<p>Under the Consumer Credit Act you can usually hand the car back once you have paid half of the total amount payable (this is called voluntary termination). Once you have paid a third, the lender normally needs a court order to take the car back. Read your agreement and check the <a href="https://www.moneyhelper.org.uk/en/everyday-money/buying-and-running-a-car/car-finance-explained" rel="noopener">MoneyHelper car finance guide</a> if you are unsure.</p>

<h2>Do not forget the running costs</h2>
<p>Finance is only one line. On a typical used car, fuel, insurance, tax and upkeep add another £250 or more a month. See the <a href="{rel}guides/true-cost-of-running-a-car-uk/">full monthly breakdown</a>.</p>
""" + CALC_BOX)

guide("car-cost-per-mile",
      "Car Cost Per Mile UK: How to Work It Out (With Examples)",
      "How to work out your car's real cost per mile",
      "Work out what your car really costs per mile in the UK, including finance or depreciation, fuel, insurance and upkeep, plus a quick fuel only cost per mile formula.",
      "Fuel only cost per mile, full cost per mile, and why the difference matters.",
      """
<p class="lede">Most people only think about fuel when they think about cost per mile. The full figure is usually four or five times higher.</p>

<h2>Fuel only cost per mile</h2>
<p>Use this formula:</p>
<div class="box">Fuel cost per mile (pence) = price per litre (pence) x 4.546 / mpg</div>
<p>At 138p a litre and 45 mpg that is 138 x 4.546 / 45 = about 14p a mile. At 30 mpg it is about 21p a mile.</p>
<p>For an electric car: pence per kWh divided by miles per kWh. Charging at home at 25p per kWh with a car that does 3.5 miles per kWh is about 7p a mile. Public rapid charging can easily be three times that.</p>

<h2>Full cost per mile</h2>
<p>Add up everything the car costs in a year and divide by the miles you drive:</p>
<ul>
<li>Finance payments, or depreciation if you paid cash</li>
<li>Fuel or charging</li>
<li>Insurance</li>
<li>Road tax</li>
<li>Servicing and MOT</li>
<li>Tyres and repairs</li>
<li>Parking, tolls and breakdown cover</li>
</ul>
<p>For our <a href="{rel}guides/true-cost-of-running-a-car-uk/">example £16,000 car on PCP</a>, that is £6,436 a year over 8,000 miles, or about 80p a mile.</p>

<h2>Why it matters</h2>
<p>Most of a car's cost is fixed. You pay the finance, insurance and tax whether you drive 2,000 miles or 12,000. So the fewer miles you do, the more each one costs. At 4,000 miles a year the same car would cost well over £1.40 a mile, which is often more than a taxi or train for the trips you actually make.</p>

<h2>HMRC mileage rates are not your cost</h2>
<p>HMRC's approved rate of 45p a mile for the first 10,000 business miles is a tax free allowance, not a measure of what your car costs. If your full cost per mile is higher than what your employer pays, business driving is costing you money.</p>
""" + CALC_BOX)

guide("cut-car-insurance-cost",
      "How to Cut Your Car Insurance Cost in the UK: 9 Things That Work",
      "How to cut your car insurance cost",
      "Practical ways to pay less for car insurance in the UK: when to buy, comparing quotes, excess, mileage, job title, security and paying annually instead of monthly.",
      "When to buy, what to change on the form, and the extras worth dropping.",
      """
<p class="lede">Insurance is often the second biggest car cost, and the one you can change fastest. These are the things that tend to make a real difference.</p>

<ol>
<li><strong>Buy about three weeks before renewal.</strong> Quotes tend to be cheapest when you buy around 20 to 26 days ahead. Leaving it to the day before usually costs more.</li>
<li><strong>Compare more than one site.</strong> Comparison sites do not all list the same insurers, and some insurers are not on any comparison site at all, so check a couple of direct quotes too.</li>
<li><strong>Pay annually if you can.</strong> Paying monthly is usually a loan with interest added. The APR on monthly car insurance is often well into double figures.</li>
<li><strong>Be accurate about mileage.</strong> Do not guess high. Check your last two MOT certificates on <a href="https://www.gov.uk/check-mot-history" rel="noopener">GOV.UK</a> to see what you really drive.</li>
<li><strong>Check your job title.</strong> Some job titles are priced differently even when they mean the same thing. Only ever pick a title that honestly describes what you do.</li>
<li><strong>Think about the voluntary excess.</strong> A higher excess lowers the premium, but only set it at a level you could actually pay after an accident.</li>
<li><strong>Add an experienced named driver</strong> if they really do drive the car sometimes. Never put a parent down as the main driver of a car you mainly drive. That is fronting, and it is fraud.</li>
<li><strong>Look at a black box policy</strong> if you are under 25. Good driving can bring the price down at renewal.</li>
<li><strong>Drop extras you already have.</strong> Breakdown cover, legal cover and key cover are often duplicated through a bank account or a separate policy.</li>
</ol>

<h2>Renewal prices</h2>
<p>Since January 2022 insurers have not been allowed to charge a renewing customer more than they would charge a new customer for the same cover. That does not mean your renewal is the best price on the market, so it still pays to shop around every year.</p>

<h2>Before you buy the car</h2>
<p>Get an insurance quote for the exact car before you buy it. Two cars with the same price can sit in very different insurance groups. Put the quote into the calculator alongside the finance so you see the full monthly cost, not just the payment.</p>
""" + CALC_BOX)

guide("used-car-checks-before-buying",
      "Used Car Checks Before You Buy: Free and Paid Checks UK",
      "Used car checks to do before you buy",
      "The free GOV.UK checks and the paid history check to do before buying a used car in the UK, plus what to look for on the V5C logbook and at the viewing.",
      "Free GOV.UK checks, the one paid check worth doing, and what to look at on the day.",
      """
<p class="lede">Ten minutes of checks can save you from a car with hidden finance, a clocked mileage or an expensive fault. Most of them are free.</p>

<h2>Free checks on GOV.UK</h2>
<ul>
<li><strong><a href="https://www.gov.uk/check-mot-history" rel="noopener">MOT history</a>.</strong> Shows every MOT result, the mileage at each test and all advisories. Mileage that goes down, or the same advisory year after year, are warning signs.</li>
<li><strong><a href="https://www.gov.uk/get-vehicle-information-from-dvla" rel="noopener">Vehicle information from DVLA</a>.</strong> Confirms the make, colour, engine size, tax status and date of first registration match the advert.</li>
<li><strong><a href="https://www.gov.uk/check-vehicle-recall" rel="noopener">Vehicle recall check</a>.</strong> Shows any safety recalls that may not have been fixed.</li>
</ul>

<h2>The paid check worth doing</h2>
<p>A vehicle history check from a provider such as HPI or the AA usually costs between about £10 and £20. It tells you if the car has outstanding finance, has been written off, or is recorded as stolen. If there is finance still owed on it, it can be taken back from you even after you have paid. This is the one check not to skip.</p>

<h2>Paperwork</h2>
<ul>
<li>The V5C logbook should show the seller's name and the address you are viewing the car at.</li>
<li>Check the VIN on the V5C matches the one on the car (usually at the bottom of the windscreen and on a plate in the door frame).</li>
<li>Ask for service history and receipts. Stamps with no garage details mean very little.</li>
</ul>

<h2>At the viewing</h2>
<ul>
<li>See the car in daylight and start it from cold. Smoke, rattles or warning lights that stay on are reasons to walk away.</li>
<li>Check the tyres. The legal minimum tread is 1.6mm, and four new tyres can easily cost several hundred pounds.</li>
<li>Test every button: air con, windows, central locking, lights.</li>
<li>Take it on a road where you can get above 50 mph if possible.</li>
</ul>

<h2>Then work out the real cost</h2>
<p>Once the car passes, get an insurance quote for it and put the price, finance and running costs into the calculator. A cheap car with a high insurance group or poor mpg can cost more each month than a dearer one.</p>
""" + CALC_BOX)

# ---------------- Guides index ----------------
cards = "".join(f'<a href="{{rel}}guides/{s}/"><strong>{h}</strong><span>{b}</span></a>' for s, h, b in GUIDES)
page("guides/", "UK Car Cost Guides: Running Costs, PCP vs HP, Insurance | True Car Cost UK",
     "Plain English guides to what a car really costs in the UK: monthly running costs, PCP vs HP, cost per mile, cheaper insurance and used car checks.",
     f'<p class="lede">Plain English guides to what owning a car in the UK really costs. Each one uses worked numbers you can check in the calculator.</p><div class="cards">{cards}</div>' + CALC_BOX,
     crumbs=[("Guides", "guides/")], h1="UK car cost guides")

# ---------------- Trust pages ----------------
page("about/", "About True Car Cost UK", "Who makes True Car Cost UK, why it exists and how the calculator works out the real monthly cost of a car.",
     """
<p class="lede">True Car Cost UK is a free calculator that shows what a car really costs you each month, not just the finance payment on the advert.</p>
<h2>Why it exists</h2>
<p>Car adverts lead with one number: the monthly payment. But fuel, insurance, road tax, servicing, MOT, tyres, parking and the money the car loses in value often add up to more than the payment itself. People find this out after they have signed. This site puts all of it in one place so you can see the full monthly figure, the cost per mile and the share of your take home pay before you commit.</p>
<h2>Who runs it</h2>
<p>It is an independent site built and run by one independent developer in the UK. It is not owned by a lender, dealer, insurer or comparison site.</p>
<h2>How the numbers are worked out</h2>
<ul>
<li>Finance payments use the standard loan formula from the APR, term, deposit and (for PCP) the balloon payment.</li>
<li>Fuel is miles divided by mpg, converted to litres (4.546 litres to a UK gallon), times the price per litre.</li>
<li>Take home pay is a rough estimate using England income tax, National Insurance and student loan thresholds, with no pension.</li>
<li>For cash buyers the yearly loss in value is counted as a cost, because it is one.</li>
</ul>
<p>Everything runs in your browser. Nothing you type is sent anywhere. The figures are estimates to help you decide, not financial advice.</p>
<h2>How the site is paid for</h2>
<p>The calculator and guides are free and always will be. In the future some links may be affiliate links, which means the site could earn a small commission if you buy through them, at no extra cost to you. Any such links will be labelled. See the <a href="{rel}affiliate-disclosure/">affiliate disclosure</a>.</p>
<p>Spotted a mistake or have an idea? <a href="{rel}contact/">Get in touch</a>.</p>
""", crumbs=[("About", "about/")], h1="About True Car Cost UK")

page("contact/", "Contact | True Car Cost UK", "How to contact True Car Cost UK to report a mistake, suggest a feature or ask about the site.",
     f"""
<p class="lede">Found a figure that looks wrong, or want something added to the calculator? We would like to hear about it.</p>
<form class="box cform" action="https://formsubmit.co/{FORM_ID}" method="POST">
<strong>Send a message</strong>
<input type="hidden" name="_subject" value="True Car Cost UK: new contact message">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="{BASE}contact/thanks/">
<input type="text" name="_honey" tabindex="-1" autocomplete="off" style="display:none">
<label for="cf-name">Your name</label>
<input id="cf-name" type="text" name="name" required maxlength="100">
<label for="cf-email">Your email (so we can reply)</label>
<input id="cf-email" type="email" name="email" required maxlength="200">
<label for="cf-topic">What is it about?</label>
<select id="cf-topic" name="topic"><option>Mistake in a figure</option><option>Feature idea</option><option>Advertising or affiliate</option><option>Something else</option></select>
<label for="cf-msg">Message</label>
<textarea id="cf-msg" name="message" rows="6" required maxlength="5000"></textarea>
<button class="cta" type="submit">Send message</button>
</form>
<p>Your message goes privately to the person who runs this site. It is not published anywhere. Please do not include personal financial details such as bank or card numbers.</p>
<p>Advertisers and affiliate networks are welcome to use the same form and we will reply by email.</p>
""", crumbs=[("Contact", "contact/")], h1="Contact")

page("contact/thanks/", "Message sent | True Car Cost UK", "Thanks for contacting True Car Cost UK.",
     """
<p class="lede">Thanks, your message has been sent. We usually reply within a few days.</p>
<p><a class="cta" href="{rel}">Back to the calculator</a></p>
""", crumbs=[("Contact", "contact/"), ("Message sent", "contact/thanks/")], h1="Message sent")

page("privacy/", "Privacy Policy | True Car Cost UK", "How True Car Cost UK handles your data: no accounts, no cookies, calculations stay in your browser, and an anonymous visit count.",
     """
<p class="lede">Short version: no accounts, no cookies, no ads tracking you, and the numbers you type never leave your device.</p>
<h2>What you type into the calculator</h2>
<p>All calculations run in your browser. The figures you enter are not sent to us or anyone else. If you press "Copy link to this setup", your numbers are put into the web address so you can share them. Only people you send that link to will see them.</p>
<h2>Visit counting</h2>
<p>We count visits and clicks on outbound links using a simple counter service (abacus.jasoncameron.dev). It records a number going up by one. No cookies are set and no personal profile is built. To count each browser only once a day, the site saves today's date in your browser's local storage. You can clear this at any time through your browser settings.</p>
<h2>Hosting</h2>
<p>The site is hosted on GitHub Pages. Like any web host, GitHub may log technical data such as IP addresses for security. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub privacy statement</a>.</p>
<h2>Contact form</h2>
<p>If you use the contact form, your name, email address and message are passed through FormSubmit (formsubmit.co) and delivered to our private inbox. We only use them to reply to you and delete them when they are no longer needed. See the <a href="https://formsubmit.co/privacy.pdf" rel="noopener">FormSubmit privacy policy</a>.</p>
<h2>Links to other sites</h2>
<p>We link to GOV.UK and other useful sites. Some links may in future be affiliate links (see our <a href="{rel}affiliate-disclosure/">affiliate disclosure</a>). When you click through, that site's own privacy policy and cookies apply, and an affiliate network may set a cookie so the site knows you came from us.</p>
<h2>Your rights</h2>
<p>We do not hold personal data about you unless you send us a message, so there is normally nothing for us to access, correct or delete. If you have a question, <a href="{rel}contact/">contact us</a>. You can also contact the Information Commissioner's Office at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>
<p>Last updated 18 October 2026.</p>
""", crumbs=[("Privacy", "privacy/")], h1="Privacy policy")

page("affiliate-disclosure/", "Affiliate Disclosure | True Car Cost UK", "How True Car Cost UK may earn money from affiliate links, and how that does and does not affect the calculator and guides.",
     """
<p class="lede">True Car Cost UK is free to use. To help cover the cost of running it, some links on the site may be affiliate links.</p>
<h2>What that means</h2>
<p>If you click an affiliate link and then buy something or take out a policy, the company may pay us a small commission. You pay exactly the same price as you would going direct. Affiliate links may come through networks such as Awin.</p>
<h2>How we label them</h2>
<p>Any affiliate link will be marked near the link itself, for example with "(affiliate link)" or a short note at the top of the section. Links to GOV.UK, MoneyHelper and similar free public services are never affiliate links.</p>
<h2>What it does not change</h2>
<ul>
<li>The calculator's maths is the same whatever car, lender or insurer you are looking at.</li>
<li>No company can pay to change a guide's advice or a result.</li>
<li>We only link to products and services that we think are useful for keeping car costs down, such as comparing insurance quotes.</li>
</ul>
<p>The site is not a lender, credit broker or insurance broker and does not give regulated financial advice. Always read the terms of any finance or insurance product before you sign up.</p>
<p>Questions about this? <a href="{rel}contact/">Contact us</a>.</p>
<p>Last updated 18 October 2026.</p>
""", crumbs=[("Affiliate disclosure", "affiliate-disclosure/")], h1="Affiliate disclosure")

# ---------------- sitemap ----------------
urls = [("", "1.0"), ("guides/", "0.8")] + [(f"guides/{s}/", "0.8") for s, _, _ in GUIDES] + \
       [("about/", "0.4"), ("contact/", "0.3"), ("privacy/", "0.3"), ("affiliate-disclosure/", "0.3")]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, p in urls:
    sm.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>")
sm.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(ROOT, "urls.txt"), "w").write("\n".join(BASE + u for u, _ in urls) + "\n")

# ---------------- dash / wording lint ----------------
bad_words = re.compile(r"\b(delve|seamless|leverage|robust|comprehensive|crucial|navigate|landscape|unlock|elevate|empower|tapestry|realm|game.changer)\b", re.I)
problems = []
for dp, _, fs in os.walk(ROOT):
    if "/.git" in dp:
        continue
    for f in fs:
        if f.endswith((".html", ".xml", ".md", ".txt")):
            t = open(os.path.join(dp, f)).read()
            for ch in ("\u2014", "\u2013"):
                if ch in t:
                    problems.append(f"{f}: dash {ch!r}")
            text = re.sub(r"<[^>]+>", " ", t)
            for m in bad_words.finditer(text):
                problems.append(f"{os.path.join(dp, f)}: word {m.group(0)}")
print("built", len(urls), "urls")
print("problems:", problems or "none")
