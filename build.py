#!/usr/bin/env python3
"""StackPick static site generator. Usage: DOMAIN=https://yourdomain.com python3 build.py"""
import os, json, shutil, html
DOMAIN = os.environ.get("DOMAIN", "https://yourdomain.com").rstrip("/")
OUT = "public"; TODAY = "2026-10-10"; SITE = "StackPick"
# Put your affiliate links here, e.g. AFF = {"canva": "https://partner-link..."}
AFF = {}
e = html.escape

TOOLS = [
 dict(s="chatgpt", n="ChatGPT", g="Writing and research", u="https://chat.openai.com", c="Easy",
  d="A general AI assistant for emails, ideas, and quick answers.",
  l="ChatGPT is a chat-based AI assistant. You type a request in plain English and it writes a draft, summarizes text, or explains a topic. Small business owners use it for customer emails, product descriptions, social posts, and brainstorming.",
  p=["Fast first drafts for almost any writing task","Easy to learn: you just type what you want","Free plan available to try it"],
  w=["Answers can contain mistakes, so check facts and numbers","Drafts can sound generic until you edit them"], a=["notion","grammarly"]),
 dict(s="grammarly", n="Grammarly", g="Clean, professional writing", u="https://www.grammarly.com", c="Easy",
  d="Checks spelling, grammar, and tone as you write in any app.",
  l="Grammarly works inside your browser and apps. It underlines mistakes and suggests clearer wording while you type emails, proposals, and posts. It is useful if English is your second language or if you write many customer messages.",
  p=["Catches typos before customers see them","Works in email, docs, and social sites","Free plan covers basic checks"],
  w=["Advanced suggestions need a paid plan","Suggestions can flatten your personal style"], a=["chatgpt","notion"]),
 dict(s="notion", n="Notion", g="Notes, tasks, and projects", u="https://www.notion.so", c="Medium",
  d="One workspace for notes, to-do lists, and simple databases.",
  l="Notion combines notes, documents, task lists, and small databases in one app. Freelancers use it to track clients and projects, and teams use it as a shared handbook. It also has built-in AI features for summarizing and drafting.",
  p=["Replaces several separate apps","Flexible templates for clients, content, and tasks","Free plan for personal use"],
  w=["Takes time to set up well","Can feel crowded if you add too much"], a=["chatgpt","zapier"]),
 dict(s="canva", n="Canva", g="Social posts, flyers, and logos", u="https://www.canva.com", c="Easy",
  d="Drag-and-drop design tool with thousands of templates.",
  l="Canva lets you design social posts, menus, flyers, presentations, and simple logos from templates. You do not need design training. It is a common first choice for small businesses that want consistent branding.",
  p=["Large template library","Simple drag-and-drop editing","Free plan with many templates"],
  w=["Some templates and assets require a paid plan","Popular templates can look familiar, so customize them"], a=["descript","mailchimp"]),
 dict(s="otter-ai", n="Otter.ai", g="Meeting notes", u="https://otter.ai", c="Easy",
  d="Records meetings and turns them into searchable notes.",
  l="Otter.ai joins or records your calls and creates a written transcript with a short summary. This helps if you spend a lot of time on client calls and need accurate notes without typing during the conversation.",
  p=["Saves time writing up calls","Searchable transcripts","Free plan to test it"],
  w=["Accuracy drops with background noise or heavy accents","Tell people when you record, and follow local recording laws"], a=["descript","notion"]),
 dict(s="zapier", n="Zapier", g="Connecting your apps", u="https://zapier.com", c="Medium",
  d="Moves information between apps automatically.",
  l="Zapier connects the apps you already use. For example, when someone fills in your contact form, Zapier can add them to a spreadsheet and send you a message. You build these automations without writing code.",
  p=["Removes repetitive copy and paste","Works with thousands of apps","Free plan for simple automations"],
  w=["Complex workflows take practice","Costs rise as you run more automations"], a=["notion","mailchimp"]),
 dict(s="descript", n="Descript", g="Video and podcast editing", u="https://www.descript.com", c="Medium",
  d="Edit video and audio by editing the text transcript.",
  l="Descript turns your recording into text. You delete words from the transcript and the matching audio or video is cut for you. It suits creators and small businesses who make short videos, podcasts, or tutorials.",
  p=["Easier than traditional editing software","Automatic transcripts and captions","Free plan available"],
  w=["Large projects can feel slow","Some export options need a paid plan"], a=["canva","otter-ai"]),
 dict(s="shopify", n="Shopify", g="Online stores", u="https://www.shopify.com", c="Medium",
  d="Build and run an online store with payments and shipping.",
  l="Shopify is a store builder. It handles product pages, checkout, payments, and shipping tools, so you can sell physical or digital products online. It is aimed at people who want a real store rather than a simple payment link.",
  p=["Everything for selling in one place","Many themes and apps","Trial available to test the setup"],
  w=["Monthly plan plus transaction costs","Extra apps can add up"], a=["mailchimp","canva"]),
 dict(s="mailchimp", n="Mailchimp", g="Email marketing", u="https://mailchimp.com", c="Easy",
  d="Send newsletters and offers to your customer list.",
  l="Mailchimp helps you collect email addresses and send newsletters, offers, and automated welcome emails. Email is one of the most reliable ways for a small business to get repeat customers.",
  p=["Beginner-friendly email builder","Signup forms for your website","Free plan for small lists"],
  w=["Pricing changes as your list grows","Follow US anti-spam rules and include an unsubscribe link"], a=["canva","zapier"]),
]
BY = {t["s"]: t for t in TOOLS}

GUIDES = [
 dict(s="ai-tools-for-one-person-business", t="AI Tools for a One-Person Business: A Simple Starter Stack",
  d="Four types of tools cover most of what a solo owner needs. Here is a simple, low-cost stack to start with.", tools=["chatgpt","canva","notion","mailchimp"],
  b=[("p","You do not need ten subscriptions. Most solo owners do well with one tool for each job: writing, design, notes, and email."),
  ("h","1. An assistant for writing and questions"),("p","Use an AI assistant such as ChatGPT to draft emails, product descriptions, and replies to customers. Always read the result and edit it so it sounds like you."),
  ("h","2. A design tool"),("p","Canva has templates for social posts, menus, and flyers. Pick one template style and reuse it so your brand looks consistent."),
  ("h","3. A place for notes and tasks"),("p","Notion or a similar app keeps your to-do list, customer notes, and ideas in one place instead of scattered across messages."),
  ("h","4. Email to your customers"),("p","A tool like Mailchimp lets you reach people who already like your work. Email usually beats social media for repeat sales."),
  ("h","How much should you spend?"),("p","Start on free plans. Upgrade only when a limit blocks real work, and write down the date each paid plan renews.")]),
 dict(s="save-5-hours-a-week-with-software", t="How to Save 5 Hours a Week With Software",
  d="Three repeating chores you can hand to software this month, with simple steps to set each one up.", tools=["otter-ai","zapier","notion"],
  b=[("p","Time is the thing small businesses run out of first. These three chores are the easiest to hand off."),
  ("h","Meeting notes"),("p","A note-taking tool such as Otter.ai can write up calls for you. That can save 20 to 30 minutes after each meeting."),
  ("h","Repeating messages"),("p","Save common replies such as pricing, hours, and how to book. Paste and adjust instead of typing from scratch."),
  ("h","Moving data between apps"),("p","If you copy form answers into a spreadsheet by hand, a tool like Zapier can do it automatically each time someone fills in the form."),
  ("h","How to start"),("p","Pick one chore, set it up this week, and measure the time saved before adding another.")]),
 dict(s="free-vs-paid-plans", t="Free Plan or Paid Plan? How to Decide",
  d="Almost every tool has a free plan. Learn when free is enough and when upgrading pays for itself.", tools=["canva","grammarly","zapier"],
  b=[("p","Almost every tool on this site has a free plan. Use it first."),
  ("h","Stay on free when"),("p","You use the tool a few times a week, you work alone, and you have not hit a limit yet."),
  ("h","Upgrade when"),("p","The limit blocks paying work, or the paid features save more time than the plan costs. A simple test: if the tool saves you two hours a month and your time is worth more than the monthly price, upgrade."),
  ("h","Watch out for"),("p","Annual plans that renew automatically and extra seats you do not need. Set a calendar reminder before renewal.")]),
 dict(s="write-better-business-emails-with-ai", t="Write Clearer Business Emails With AI",
  d="A short routine for using AI to draft business emails that still sound like you.", tools=["chatgpt","grammarly"],
  b=[("p","AI can write a first draft in seconds, but customers can tell when an email is generic. Use this routine."),
  ("h","Give it the facts"),("p","Tell the assistant who the reader is, what you want them to do, and any dates or prices. The more detail, the better the draft."),
  ("h","Edit for your voice"),("p","Cut filler, add a personal line, and check every fact and number yourself."),
  ("h","Run a final check"),("p","A tool like Grammarly catches typos and tone problems before you press send.")]),
]

CSS = """:root{--bg:#F2F5F9;--card:#fff;--ink:#14213D;--mute:#4d5a72;--line:#d9e0ea;--accent:#0b6b63;--hi:#FFB400}
@media (prefers-color-scheme:dark){:root{--bg:#0e1626;--card:#16213a;--ink:#eef2f8;--mute:#a9b8d0;--line:#2a3857;--accent:#4fd1c5}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 Georgia,"Times New Roman",serif}
h1,h2,h3,.btn,nav,th,.crumb{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
a{color:var(--accent)}.wrap{max-width:980px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px}.skip:focus{left:10px;top:10px;background:var(--hi);color:#14213D;padding:8px;z-index:9}
header.top{border-bottom:1px solid var(--line)}
nav{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:16px 0}
.logo{font-size:22px;font-weight:800;color:var(--ink);text-decoration:none}
nav a.l{color:var(--ink);text-decoration:none;margin-left:16px;font-size:15px}nav a.l:hover{text-decoration:underline}
h1{font-size:clamp(30px,5.5vw,52px);line-height:1.1;margin:0 0 16px;font-weight:800}
h2{font-size:27px;margin:0 0 14px}h3{font-size:20px;margin:24px 0 8px}
.hero{padding:44px 0 24px}.hero p{max-width:34em;color:var(--mute);font-size:19px}
.btn{display:inline-block;background:var(--hi);color:#14213D;padding:12px 20px;border-radius:10px;font-weight:700;text-decoration:none}
a:focus-visible,.btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px}
.box h3{margin:0 0 6px}.box p{margin:0 0 8px;font-size:15.5px;line-height:1.55}.box a{font-family:system-ui,Arial,sans-serif;font-weight:700}
.for{font-size:14px;color:var(--accent);font-family:system-ui,Arial,sans-serif;font-weight:700;display:block;margin-bottom:6px}
.mute{color:var(--mute)}section{margin:0 0 40px}.art{max-width:680px}
.crumb{font-size:14px;color:var(--mute);padding:18px 0 0}.crumb a{color:var(--mute)}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:560px;background:var(--card)}
th,td{text-align:left;padding:12px;border-bottom:1px solid var(--line);font-size:15px}
.note{background:var(--card);border-left:4px solid var(--hi);padding:12px 16px;font-size:15px;border-radius:6px}
.two{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
footer{padding:26px 0 48px;color:var(--mute);font-size:14px;border-top:1px solid var(--line);margin-top:40px}footer a{margin-right:14px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14213D"/><path d="M32 12l8 18-8 22-8-22z" fill="#FFB400"/></svg>'

def aff(slug): return AFF.get(slug, BY[slug]["u"])
def url(path): return DOMAIN + path
pages = []  # (path, priority)

def layout(path, title, desc, body, schema=None, crumbs=None, og="website", prio="0.7"):
    full = url(path); schema = list(schema or [])
    if crumbs:
        items = [{"@type":"ListItem","position":i+1,"name":n,"item":url(p)} for i,(n,p) in enumerate(crumbs)]
        schema.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumb wrap" aria-label="Breadcrumb">' + " &rsaquo; ".join(
            f'<a href="{p}">{e(n)}</a>' if i < len(crumbs)-1 else e(n) for i,(n,p) in enumerate(crumbs)) + '</nav>'
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schema)
    t = title if title.endswith(SITE) else f"{title} | {SITE}"
    page = f"""<!DOCTYPE html>
<html lang="en-US"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{full}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#14213D">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="{SITE}"><meta property="og:type" content="{og}">
<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{full}"><meta property="og:image" content="{url('/og.svg')}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(t)}"><meta name="twitter:description" content="{e(desc)}">
<link rel="stylesheet" href="/style.css">{ld}</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><nav aria-label="Main"><a class="logo" href="/">{SITE}</a><span>
<a class="l" href="/tools/">Tools</a><a class="l" href="/guides/">Guides</a><a class="l" href="/compare/">Compare</a><a class="l" href="/about/">About</a></span></nav></div></header>
{crumb_html}<main id="main" class="wrap">{body}</main>
<footer><div class="wrap"><p><a href="/about/">About</a><a href="/legal/">Disclosure &amp; privacy</a><a href="/sitemap.xml">Sitemap</a></p>
<p>Some links on this site are affiliate links. We may earn a commission if you buy through them, at no extra cost to you. {SITE} is independent and not affiliated with the tools listed. Prices and features change, so check each company's site. &copy; 2026 {SITE}.</p></div></footer>
</body></html>"""
    d = OUT + path
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
    pages.append((path, prio))

def tcard(t): return f'<div class="box"><h3><a href="/tools/{t["s"]}/">{e(t["n"])}</a></h3><span class="for">{e(t["g"])}</span><p>{e(t["d"])}</p><a href="/tools/{t["s"]}/">Read overview</a></div>'
def gcard(g): return f'<div class="box"><h3><a href="/guides/{g["s"]}/">{e(g["t"])}</a></h3><p class="mute">{e(g["d"])}</p><a href="/guides/{g["s"]}/">Read guide</a></div>'

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
open(OUT+"/style.css","w").write(CSS); open(OUT+"/favicon.svg","w").write(FAVICON)
open(OUT+"/og.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#14213D"/><text x="80" y="300" font-family="Arial" font-size="96" font-weight="800" fill="#fff">StackPick</text><text x="80" y="390" font-family="Arial" font-size="40" fill="#FFB400">AI tools and guides for US small businesses</text></svg>')

# Home
home_schema = [
 {"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":url("/"),"inLanguage":"en-US"},
 {"@context":"https://schema.org","@type":"Organization","name":SITE,"url":url("/"),"logo":url("/favicon.svg")}]
layout("/", f"{SITE}: AI Tools and Guides for US Small Businesses",
 "Plain-English guides and tool overviews for US freelancers and small business owners. Find the right AI tool without the jargon.",
 f"""<div class="hero"><h1>Stop guessing which AI tool your business needs.</h1>
<p>Plain-English guides and tool overviews for US freelancers and small business owners. No jargon, no hype.</p>
<a class="btn" href="/tools/">Browse all tools</a></div>
<section><h2>Popular tools</h2><div class="grid">{"".join(tcard(t) for t in TOOLS[:6])}</div></section>
<section><h2>Start with these guides</h2><div class="grid">{"".join(gcard(g) for g in GUIDES[:3])}</div></section>
<section class="art"><h2>How we pick tools</h2><p>We list tools that have a free plan or trial, are easy to start with, and are widely used by small businesses. We explain what each one does, who it suits, and what to watch out for. See our <a href="/about/">about page</a> and <a href="/legal/">affiliate disclosure</a>.</p></section>""",
 schema=home_schema, prio="1.0")

# Tools index
layout("/tools/", "AI Tools for Small Business: Overviews and Picks",
 "Browse AI and software tools for small businesses: writing, design, meetings, automation, video, email, and online stores.",
 f'<section><h1>AI and software tools for small business</h1><p class="mute">Each tool has its own overview with pros, things to watch out for, and alternatives. Not sure how they differ? See the <a href="/compare/">comparison table</a>.</p><div class="grid">{"".join(tcard(t) for t in TOOLS)}</div></section>',
 crumbs=[("Home","/"),("Tools","/tools/")], prio="0.9")

# Tool pages
for t in TOOLS:
    rel_g = [g for g in GUIDES if t["s"] in g["tools"]]
    body = f"""<article class="art"><h1>{e(t["n"])} Overview: What It Does and Who It Is For</h1>
<p>{e(t["l"])}</p>
<p><a class="btn" href="{aff(t['s'])}" target="_blank" rel="sponsored nofollow noopener">Visit {e(t["n"])}</a></p>
<p class="note">Affiliate link: we may earn a commission at no extra cost to you. Check the official site for current prices and limits. Last reviewed {TODAY}.</p>
<h2>Quick facts</h2><ul><li><strong>Best for:</strong> {e(t["g"])}</li><li><strong>Learning curve:</strong> {t["c"]}</li><li><strong>Free option:</strong> Check the official site for the current free plan or trial</li></ul>
<div class="two"><div><h3>What we like</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in t["p"])}</ul></div>
<div><h3>Watch out for</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in t["w"])}</ul></div></div>
<h2>Alternatives</h2><ul>{"".join(f'<li><a href="/tools/{a}/">{e(BY[a]["n"])}</a>: {e(BY[a]["d"])}</li>' for a in t["a"])}</ul>
{"<h2>Related guides</h2><ul>"+"".join(f'<li><a href="/guides/{g["s"]}/">{e(g["t"])}</a></li>' for g in rel_g)+"</ul>" if rel_g else ""}
</article>"""
    layout(f"/tools/{t['s']}/", f"{t['n']} Overview for Small Business",
     f"{t['n']} overview: {t['d']} See who it is for, what we like, what to watch out for, and alternatives.", body,
     crumbs=[("Home","/"),("Tools","/tools/"),(t["n"],f"/tools/{t['s']}/")], prio="0.8")

# Guides index + pages
layout("/guides/", "Small Business AI and Software Guides",
 "Practical, plain-English guides on choosing and using AI and software tools in a small business.",
 f'<section><h1>Guides</h1><div class="grid">{"".join(gcard(g) for g in GUIDES)}</div></section>',
 crumbs=[("Home","/"),("Guides","/guides/")], prio="0.9")
for g in GUIDES:
    art = "".join(f"<h2>{e(x)}</h2>" if k=="h" else f"<p>{e(x)}</p>" for k,x in g["b"])
    sch = [{"@context":"https://schema.org","@type":"Article","headline":g["t"],"description":g["d"],"datePublished":TODAY,"dateModified":TODAY,
            "mainEntityOfPage":url(f"/guides/{g['s']}/"),"author":{"@type":"Organization","name":SITE},"publisher":{"@type":"Organization","name":SITE}}]
    body = f"""<article class="art"><h1>{e(g["t"])}</h1><p class="mute">Updated {TODAY}</p>{art}
<h2>Tools mentioned</h2><ul>{"".join(f'<li><a href="/tools/{s}/">{e(BY[s]["n"])}</a>: {e(BY[s]["d"])}</li>' for s in g["tools"])}</ul>
<p class="note">Some tool links on this site are affiliate links. See our <a href="/legal/">disclosure</a>.</p></article>"""
    layout(f"/guides/{g['s']}/", g["t"], g["d"], body, schema=sch, og="article",
     crumbs=[("Home","/"),("Guides","/guides/"),(g["t"],f"/guides/{g['s']}/")], prio="0.8")

# Compare
rows = "".join(f'<tr><td><a href="/tools/{t["s"]}/">{e(t["n"])}</a></td><td>{e(t["g"])}</td><td>{t["c"]}</td></tr>' for t in TOOLS)
layout("/compare/", "Compare Small Business AI Tools Side by Side",
 "Compare popular AI and software tools for small business by what they are best for and how easy they are to learn.",
 f'<section><h1>Compare tools</h1><h2>Head-to-head comparisons</h2><p><a href="/compare/canva-vs-adobe-express/">Canva vs Adobe Express</a></p><h2>All tools</h2><p class="mute">Check each official site for current free plans and prices, since they change often.</p><div class="tw"><table><thead><tr><th>Tool</th><th>Best for</th><th>Learning curve</th></tr></thead><tbody>{rows}</tbody></table></div></section>',
 crumbs=[("Home","/"),("Compare","/compare/")], prio="0.8")

# About + Legal
layout("/about/", "About StackPick", "StackPick helps US small business owners and freelancers choose software without wading through marketing pages.",
 f'<section class="art"><h1>About {SITE}</h1><p>{SITE} helps small business owners and freelancers in the US choose software without wading through marketing pages. We explain what each tool does, who it suits, and when a free plan is enough.</p><p>We earn money through affiliate links. When you sign up through one, the company may pay us a commission. It does not change your price.</p><p>Contact: add your email address here before launch.</p></section>',
 crumbs=[("Home","/"),("About","/about/")], prio="0.5")
layout("/legal/", "Affiliate Disclosure and Privacy Policy", "How StackPick earns money through affiliate links and how we handle your information.",
 f'<section class="art"><h1>Disclosure and privacy</h1><h2>Affiliate disclosure</h2><p>Some links on this site are affiliate links. We may earn a commission if you buy through them, at no extra cost to you. We only list tools we would recommend either way.</p><h2>Privacy</h2><p>This site does not use cookies or collect personal information itself. If you add analytics or a newsletter later, update this section to say what you collect and why.</p><h2>No professional advice</h2><p>Content here is general information, not legal, tax, or financial advice.</p></section>',
 crumbs=[("Home","/"),("Disclosure & privacy","/legal/")], prio="0.3")


# Comparison page: Canva vs Adobe Express
FAQ=[("Is Canva or Adobe Express better for beginners?","Both are built for beginners. Canva has a larger template library and a very simple editor. Adobe Express is a good fit if you already use Adobe apps or want quick edits like removing a background."),
("Can I use Canva or Adobe Express for free?","Both offer a free plan. Free plans have limits on templates, assets, and features, so check each official site for what is included today."),
("Which one is better for social media posts?","Either works well. Choose by testing a few templates in your niche. The better tool is the one where you can make a good-looking post fastest."),
("Can I switch later?","Yes. You can download your designs as images or PDFs from either tool, but you may need to rebuild layouts if you change tools.")]
cmp_rows=[("Best for","Social posts, flyers, presentations, simple logos","Quick social graphics, edits, and people already using Adobe apps"),
("Templates","Very large library across many styles","Large library with a focus on social and marketing formats"),
("Learning curve","Easy","Easy"),
("Free plan","Yes, with limits","Yes, with limits"),
("Brand kit (fonts, colors, logos)","Available on paid plans","Available on paid plans"),
("Works well with","Many apps and social schedulers","Other Adobe apps and Creative Cloud files"),
("AI features","Built-in AI design and writing helpers","Built-in AI image and text effects")]
tbl="".join(f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a,b,c in cmp_rows)
faq_html="".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in FAQ)
faq_schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
art_schema={"@context":"https://schema.org","@type":"Article","headline":"Canva vs Adobe Express: Which Is Better for Small Business?","datePublished":TODAY,"dateModified":TODAY,"mainEntityOfPage":url("/compare/canva-vs-adobe-express/"),"author":{"@type":"Organization","name":SITE},"publisher":{"@type":"Organization","name":SITE}}
layout("/compare/canva-vs-adobe-express/","Canva vs Adobe Express: Which Is Better for Small Business?",
 "Canva vs Adobe Express compared for small business: templates, ease of use, free plans, AI features, and who should pick which.",
 f"""<article class="art"><h1>Canva vs Adobe Express: Which Is Better for Small Business?</h1>
<p class="mute">Updated {TODAY}</p>
<p><strong>Short answer:</strong> pick Canva if you want the biggest range of templates and the simplest editor. Pick Adobe Express if you already use Adobe apps or mostly need fast social graphics and quick edits. Both have free plans, so you can test both in an afternoon.</p>
<p class="note">Affiliate disclosure: some links here may earn us a commission at no extra cost to you. Features and plans change, so confirm details on the official sites.</p>
<h2>Side-by-side comparison</h2>
<div class="tw"><table><thead><tr><th>Feature</th><th>Canva</th><th>Adobe Express</th></tr></thead><tbody>{tbl}</tbody></table></div>
<h2>Canva: what it does well</h2>
<p>Canva is a design tool built around templates. You pick a layout for a social post, menu, flyer, or presentation and change the text and images. It is easy to stay consistent, which matters for small business branding. Read our <a href="/tools/canva/">Canva overview</a> for more.</p>
<p><a class="btn" href="{aff('canva')}" target="_blank" rel="sponsored nofollow noopener">Try Canva</a></p>
<h2>Adobe Express: what it does well</h2>
<p>Adobe Express is Adobe's simple design app. It covers social graphics, short videos, and quick image edits, and it connects with other Adobe tools. If your files already live in Adobe apps, that connection can save time.</p>
<p><a class="btn" href="https://www.adobe.com/express/" target="_blank" rel="sponsored nofollow noopener">Try Adobe Express</a></p>
<h2>Which should you choose?</h2>
<ul><li><strong>Choose Canva</strong> if you are new to design, want many template styles, or make flyers and presentations as well as social posts.</li>
<li><strong>Choose Adobe Express</strong> if you already pay for Adobe apps, or want quick edits and social content in one place.</li>
<li><strong>Not sure?</strong> Make the same post in both free plans and keep the one that felt faster.</li></ul>
<h2>Frequently asked questions</h2>{faq_html}
<p>Related: <a href="/guides/ai-tools-for-one-person-business/">AI tools for a one-person business</a> and <a href="/guides/free-vs-paid-plans/">Free plan or paid plan?</a></p></article>""",
 schema=[art_schema,faq_schema], og="article",
 crumbs=[("Home","/"),("Compare","/compare/"),("Canva vs Adobe Express","/compare/canva-vs-adobe-express/")], prio="0.8")

# 404, robots, sitemap
open(OUT+"/404.html","w").write(f'<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | {SITE}</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/style.css"></head><body><main class="wrap hero"><h1>Page not found</h1><p>That page does not exist. Try the <a href="/">home page</a>, <a href="/tools/">tools</a>, or <a href="/guides/">guides</a>.</p></main></body></html>')
open(OUT+"/robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
sm = "".join(f"<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p,pr in pages)
open(OUT+"/sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
open(OUT+"/.nojekyll","w").write("")
host=DOMAIN.split("://",1)[-1]
if host != "yourdomain.com": open(OUT+"/CNAME","w").write(host+"\n")
print(f"Built {len(pages)} pages for {DOMAIN} into ./{OUT}")
