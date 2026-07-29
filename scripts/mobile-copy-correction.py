from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")


RESPONSIVE_CSS = r'''
/* Screen-first document reflow. Print geometry remains governed separately. */
html, body { max-width: 100%; }
.sheet, .sheet * { min-width: 0; }
.resume-header > div, .letter-body, .job, .review-row, .decision-form,
.plan-phase, .plan-readout, .plan-deliverables { overflow-wrap: anywhere; }

/* Denser, deliberately composed 120-day plan. */
.plan-page { display: flex; flex-direction: column; }
.plan-kicker { margin: 0 0 8px; color: var(--bt-lime-dark); font-size: 11px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
.plan-page-title { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(220px, .75fr); gap: 28px; align-items: end; margin: 22px 0 24px; padding-bottom: 18px; border-bottom: 1px solid var(--bt-line); }
.plan-page-title h2 { margin: 0; font-size: 34px; line-height: 1.02; letter-spacing: -.04em; }
.plan-page-title p { margin: 0; color: var(--bt-slate); font-size: 14px; }
.plan-phase-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.plan-phase { padding: 18px 18px 16px; background: #f6f7f2; border-top: 4px solid var(--bt-lime); break-inside: avoid; }
.plan-phase header { display: flex; justify-content: space-between; gap: 14px; align-items: baseline; margin-bottom: 10px; }
.plan-phase header span { color: var(--bt-lime-dark); font-size: 10px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
.plan-phase h3 { margin: 0; font-size: 21px; line-height: 1.08; letter-spacing: -.02em; }
.plan-phase > p { margin: 0 0 11px; font-size: 13px; font-weight: 700; }
.plan-phase-body { display: grid; grid-template-columns: 1.15fr .85fr; gap: 14px; }
.plan-phase h4, .plan-readout h3, .plan-deliverables h3 { margin: 0 0 7px; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; }
.plan-phase ul, .plan-readout ul, .plan-deliverables ul { margin: 0; padding-left: 17px; }
.plan-phase li { margin: 0 0 5px; font-size: 11.4px; line-height: 1.35; }
.plan-output-list { border-left: 1px solid #c9ccc3; padding-left: 13px; }
.plan-readout, .plan-deliverables { margin-top: 16px; padding: 16px 18px; background: var(--bt-charcoal); color: white; break-inside: avoid; }
.plan-readout-grid, .plan-deliverables-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.plan-readout strong, .plan-deliverables strong { display: block; color: var(--bt-lime); font-size: 11px; margin-bottom: 4px; }
.plan-readout span, .plan-deliverables span { display: block; font-size: 10.7px; line-height: 1.35; color: #e6e8e1; }
.plan-outcomes { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px; }
.plan-outcomes article { padding: 15px 17px; border: 1px solid var(--bt-line); break-inside: avoid; }
.plan-outcomes h3 { margin: 0 0 8px; font-size: 15px; }
.plan-outcomes ul { margin: 0; padding-left: 17px; columns: 2; column-gap: 22px; }
.plan-outcomes li { margin: 0 0 5px; font-size: 10.8px; line-height: 1.35; break-inside: avoid; }

@media screen and (max-width: 900px) {
  html, body { overflow-x: hidden; }
  body { background: #eef0eb; }
  .document-nav {
    position: sticky !important;
    top: 0;
    z-index: 50;
    width: 100%;
    max-width: 100%;
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
    overflow-x: auto;
    overscroll-behavior-inline: contain;
    padding: 10px 12px !important;
    white-space: nowrap;
    background: rgba(43,42,41,.97) !important;
    -webkit-overflow-scrolling: touch;
  }
  .document-nav a {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    min-height: 44px;
    padding: 9px 13px !important;
    font-size: 13px !important;
  }
  .document-shell {
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 14px !important;
    overflow: visible !important;
  }
  .document-toolbar {
    position: static !important;
    inset: auto !important;
    width: 100% !important;
    max-width: none !important;
    margin: 0 0 12px !important;
    padding: 0 !important;
  }
  .document-toolbar .download {
    display: flex !important;
    width: 100%;
    min-height: 48px;
    align-items: center;
    justify-content: center;
  }
  .sheet {
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 0 16px !important;
    padding: clamp(22px, 5vw, 38px) !important;
    overflow: visible !important;
    box-shadow: 0 8px 24px rgba(20, 22, 18, .08) !important;
  }
  .doc-brand { display: flex !important; flex-wrap: wrap; gap: 10px 16px; align-items: center; }
  .doc-brand img { width: min(132px, 42vw) !important; height: auto !important; }
  .resume-header { margin-top: 20px !important; }
  .resume-header h1 { font-size: clamp(34px, 9vw, 48px) !important; line-height: 1 !important; }
  .resume-header p { font-size: 13px !important; line-height: 1.35 !important; }
  .resume-header > div { font-size: 12px !important; line-height: 1.55 !important; word-break: break-word; }
  .resume-summary, .letter-meta, .letter-body, .job, .applied-work, .resume-mechanisms,
  .review-title, .review-callout, .decision-form { max-width: 100% !important; }
  .resume-columns, .resume-columns.page-two, .plan-layout, .plan-phase-grid,
  .plan-page-title, .plan-phase-body, .plan-outcomes, .review-row,
  .form-grid, .form-grid.bottom, .applied-work-grid, .resume-mechanisms-grid {
    display: grid !important;
    grid-template-columns: minmax(0, 1fr) !important;
  }
  .resume-columns, .resume-columns.page-two { gap: 24px !important; }
  .resume-side {
    width: auto !important;
    border-left: 0 !important;
    border-top: 1px solid var(--bt-line);
    padding: 22px 0 0 !important;
  }
  .job > div { display: block !important; }
  .job span { display: block; margin-top: 3px; }
  .review-row { gap: 8px !important; padding: 16px 0 !important; }
  .review-row.header { display: none !important; }
  .review-row p { margin: 0 !important; }
  .decision-form .disposition { display: flex !important; flex-wrap: wrap !important; gap: 9px 14px !important; }
  .plan-readout-grid, .plan-deliverables-grid { grid-template-columns: 1fr 1fr !important; }
  .plan-outcomes ul { columns: 1; }
  .page-footer {
    position: static !important;
    inset: auto !important;
    display: flex !important;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 8px 16px;
    margin-top: 24px !important;
    padding-top: 12px !important;
  }
}

@media screen and (max-width: 420px) {
  .document-shell { padding: 8px !important; }
  .sheet { padding: 20px 16px !important; margin-bottom: 10px !important; }
  .document-nav { padding: 8px !important; }
  .document-nav a { font-size: 12px !important; padding: 8px 11px !important; }
  .resume-header h1 { font-size: 35px !important; }
  .sheet h2 { font-size: clamp(23px, 7vw, 30px) !important; }
  .sheet h3 { overflow-wrap: anywhere; }
  .sheet p, .sheet li { font-size: 14px; }
  .plan-phase { padding: 15px 14px; }
  .plan-phase header { display: block; }
  .plan-phase header span { display: block; margin-bottom: 4px; }
  .plan-phase li { font-size: 13px !important; }
  .plan-readout-grid, .plan-deliverables-grid { grid-template-columns: 1fr !important; }
}

@media print {
  .plan-page { padding: .42in .5in .38in !important; }
  .plan-page-title { margin: .12in 0 .16in; padding-bottom: .11in; gap: .2in; }
  .plan-page-title h2 { font-size: 25px; }
  .plan-phase-grid { gap: .12in; }
  .plan-phase { padding: .13in .14in .11in; }
  .plan-phase h3 { font-size: 16px; }
  .plan-phase li { font-size: 8.6px; line-height: 1.28; margin-bottom: 3px; }
  .plan-readout, .plan-deliverables { margin-top: .12in; padding: .12in .14in; }
  .plan-readout-grid, .plan-deliverables-grid { gap: .1in; }
  .plan-readout span, .plan-deliverables span { font-size: 8.3px; }
  .plan-outcomes { gap: .12in; margin-top: .12in; }
  .plan-outcomes article { padding: .11in .13in; }
  .plan-outcomes li { font-size: 8.2px; }
}
'''

PLAN_HTML = r'''
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Russell Dudek | 120-Day Entry Plan</title><meta name="description" content="Independent candidate vision by Russell Dudek for Baker Tilly Consulting AI Director."><link rel="stylesheet" href="brand-tokens.css"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="document-responsive.css"></head><body><div class="document-nav"><a href="resume.html">View Resume</a><a href="cover-letter.html">View Cover Letter</a><a href="value-conversion-review.html">Value Conversion Review</a><a href="index.html">Candidate Vision</a></div><main class="document-shell plan-doc"><div class="document-toolbar"><a class="download" href="docs/Russell-Dudek-Baker-Tilly-120-Day-Plan.pdf" download>Download PDF</a></div>
<section class="sheet plan-page"><div class="doc-brand"><img src="assets/brand/baker-tilly-logo.svg" alt="Baker Tilly"><span>Independent candidate material</span></div><header class="resume-header"><h1>Russell Dudek</h1><p>120-DAY ENTRY PLAN | CONSULTING AI DIRECTOR</p><div>Pittsburgh, PA | 412.287.8640 | russelldudek@gmail.com | https://www.linkedin.com/in/russelldudek | https://russelldudek.github.io/BakerTillyUS/</div></header>
<div class="plan-page-title"><div><p class="plan-kicker">Days 0-60</p><h2>Establish the business system.</h2></div><p>Build shared visibility into the work, the portfolio, the economics, and the decisions that will focus Baker Tilly Consulting’s AI activation agenda.</p></div>
<div class="plan-phase-grid">
<article class="plan-phase"><header><span>Phase 1 · Days 0-30</span><h3>Understand the work in practice</h3></header><p>Learn how Consulting teams create value today and where AI can strengthen delivery.</p><div class="plan-phase-body"><div><h4>Actions</h4><ul><li>Meet Consulting executives, practice leaders, delivery leaders, platform owners, data, security, legal, risk, learning, talent, and representative practitioners.</li><li>Observe priority workflows, reviews, handoffs, knowledge searches, exceptions, and client-delivery moments.</li><li>Reconcile the use-case inventory, active pilots, platform capabilities, dependencies, ownership, and adoption signals.</li><li>Define baseline measures for cycle time, quality, review burden, capacity, leverage, pricing, and reuse.</li></ul></div><div class="plan-output-list"><h4>Outputs</h4><ul><li>Consulting AI system map</li><li>Portfolio fact base</li><li>Stakeholder and decision-rights map</li><li>Baseline scorecard</li><li>Priority workflow observations</li></ul></div></div></article>
<article class="plan-phase"><header><span>Phase 2 · Days 31-60</span><h3>Focus the activation portfolio</h3></header><p>Convert broad opportunity into a small set of business-owned priorities.</p><div class="plan-phase-body"><div><h4>Actions</h4><ul><li>Rank opportunities by client value, delivery impact, economic mechanism, feasibility, reuse, readiness, and adoption effort.</li><li>Write capability requests that define the outcome, workflow, users, data, integrations, human authority, evaluation, and operating owner.</li><li>Choose a balanced pilot set across knowledge work, client deliverables, onboarding, and bounded automation.</li><li>Align investment, sequencing, dependencies, and executive decision cadence.</li></ul></div><div class="plan-output-list"><h4>Outputs</h4><ul><li>Prioritized activation portfolio</li><li>Value-conversion cases</li><li>Capability-request standard</li><li>Pilot charters</li><li>Executive decision calendar</li></ul></div></div></article>
</div>
<div class="plan-readout"><h3>First 60-day executive readout</h3><div class="plan-readout-grid"><div><strong>Portfolio</strong><span>What is active, why it matters, who owns it, and what decision comes next.</span></div><div><strong>Economics</strong><span>The value mechanism and baseline for each priority workflow.</span></div><div><strong>Capability</strong><span>Clear business-to-technology requests with bounded authority and evaluation.</span></div><div><strong>Adoption</strong><span>Named practice owners, role expectations, and enablement built into the work.</span></div></div></div>
<footer class="page-footer"><span>120-Day Entry Plan</span><span>1 / 2</span></footer></section>
<section class="sheet plan-page"><div class="doc-brand"><img src="assets/brand/baker-tilly-logo.svg" alt="Baker Tilly"><span>Independent candidate material</span></div><header class="resume-header"><h1>Russell Dudek</h1><p>120-DAY ENTRY PLAN | CONSULTING AI DIRECTOR</p><div>Pittsburgh, PA | 412.287.8640 | russelldudek@gmail.com | https://www.linkedin.com/in/russelldudek | https://russelldudek.github.io/BakerTillyUS/</div></header>
<div class="plan-page-title"><div><p class="plan-kicker">Days 61-120</p><h2>Turn learning into reusable advantage.</h2></div><p>Run measured pilots, strengthen practice capability, and package the operating mechanisms that compound across Consulting.</p></div>
<div class="plan-phase-grid">
<article class="plan-phase"><header><span>Phase 3 · Days 61-90</span><h3>Run measured, practice-owned pilots</h3></header><p>Prove changed work and adoption, not tool activity.</p><div class="plan-phase-body"><div><h4>Actions</h4><ul><li>Launch pilots with named practice sponsors, workflow owners, technical counterparts, and clear review authority.</li><li>Pair each pilot with role-based learning, office hours, practice champions, manager coaching, and reusable context.</li><li>Measure output quality, cycle time, review burden, exceptions, repeat use, confidence, and support effort.</li><li>Capture technical dependencies, operating friction, reusable patterns, and client-value implications.</li></ul></div><div class="plan-output-list"><h4>Outputs</h4><ul><li>Pilot evidence packs</li><li>Adoption scorecards</li><li>Champion network cadence</li><li>Reusable workflow patterns</li><li>Monthly value review</li></ul></div></div></article>
<article class="plan-phase"><header><span>Phase 4 · Days 91-120</span><h3>Scale the mechanisms that work</h3></header><p>Convert successful pilots into repeatable Consulting capability.</p><div class="plan-phase-body"><div><h4>Actions</h4><ul><li>Make scale, standardize, redesign, productize, or pause decisions using delivery, economics, trust, adoption, and reuse evidence.</li><li>Package proven methods into accelerators, playbooks, prompt/context assets, technical requirements, and training modules.</li><li>Establish portfolio intake, quarterly priorities, monthly value reviews, pilot checkpoints, and executive reporting.</li><li>Set the 12-month agenda for priority practices, platform dependencies, capability growth, and investment.</li></ul></div><div class="plan-output-list"><h4>Outputs</h4><ul><li>Portfolio decisions</li><li>Reusable Consulting AI methods</li><li>Operating cadence</li><li>Investment roadmap</li><li>12-month activation agenda</li></ul></div></div></article>
</div>
<div class="plan-outcomes"><article><h3>Day 120 leadership package</h3><ul><li>Consulting AI portfolio and roadmap</li><li>Value Conversion Review standard</li><li>Practice-owned pilot evidence</li><li>Capability-request library</li><li>Adoption and learning model</li><li>Executive scorecard and cadence</li></ul></article><article><h3>What good looks like</h3><ul><li>Priority workflows have named owners and baselines.</li><li>Practice leaders can see the economic claim and evidence.</li><li>Technical teams receive precise, decision-ready requests.</li><li>Practitioners gain useful capability inside real work.</li><li>Successful patterns are packaged for reuse.</li><li>Leadership has a credible 12-month scale agenda.</li></ul></article></div>
<div class="plan-deliverables"><h3>The operating result</h3><div class="plan-deliverables-grid"><div><strong>Sharper choices</strong><span>A focused portfolio tied to consulting priorities.</span></div><div><strong>Stronger delivery</strong><span>Workflow improvement with professional judgment visible.</span></div><div><strong>Faster learning</strong><span>Measured pilots that create reusable methods.</span></div><div><strong>Durable adoption</strong><span>Practice ownership, role capability, and executive cadence.</span></div></div></div>
<footer class="page-footer"><span>120-Day Entry Plan</span><span>2 / 2</span></footer></section></main></body></html>
'''

GENERATOR = r'''
import { chromium } from 'playwright';
import { readFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const css = `${await readFile(path.join(root, 'brand-tokens.css'), 'utf8')}\n${await readFile(path.join(root, 'styles.css'), 'utf8')}\n${await readFile(path.join(root, 'document-responsive.css'), 'utf8')}`;
const svg = await readFile(path.join(root, 'assets/brand/baker-tilly-logo.svg'));
const svgUri = `data:image/svg+xml;base64,${svg.toString('base64')}`;

const documents = [
  ['resume.html', 'Russell-Dudek-Baker-Tilly-Resume.pdf'],
  ['cover-letter.html', 'Russell-Dudek-Baker-Tilly-Cover-Letter.pdf'],
  ['120-day-plan.html', 'Russell-Dudek-Baker-Tilly-120-Day-Plan.pdf'],
  ['value-conversion-review.html', 'Russell-Dudek-Baker-Tilly-Value-Conversion-Review.pdf'],
];

await mkdir(path.join(root, 'docs'), { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

for (const [source, output] of documents) {
  let html = await readFile(path.join(root, source), 'utf8');
  html = html.replace(
    '<link rel="stylesheet" href="brand-tokens.css"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="document-responsive.css">',
    `<style>${css}</style>`,
  );
  html = html.replaceAll('src="assets/brand/baker-tilly-logo.svg"', `src="${svgUri}"`);
  await page.setContent(html, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: path.join(root, 'docs', output),
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: false,
  });
  console.log(`Generated docs/${output}`);
}

await browser.close();
'''

WORKFLOW = r'''
name: Generate candidate PDFs

on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - '*.html'
      - '*.css'
      - 'assets/brand/**'
      - 'scripts/generate-pdfs.mjs'
      - '.github/workflows/generate-pdfs.yml'

permissions:
  contents: write

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install PDF tooling
        run: |
          npm install --no-save playwright
          npx playwright install --with-deps chromium
          sudo apt-get update
          sudo apt-get install -y poppler-utils
      - name: Generate PDFs
        run: node scripts/generate-pdfs.mjs
      - name: Verify page contracts and campaign URL
        run: |
          test "$(pdfinfo docs/Russell-Dudek-Baker-Tilly-Resume.pdf | awk '/^Pages:/{print $2}')" = "2"
          test "$(pdfinfo docs/Russell-Dudek-Baker-Tilly-Cover-Letter.pdf | awk '/^Pages:/{print $2}')" = "1"
          test "$(pdfinfo docs/Russell-Dudek-Baker-Tilly-120-Day-Plan.pdf | awk '/^Pages:/{print $2}')" = "2"
          test "$(pdfinfo docs/Russell-Dudek-Baker-Tilly-Value-Conversion-Review.pdf | awk '/^Pages:/{print $2}')" = "2"
          for pdf in docs/*.pdf; do pdftotext "$pdf" - | grep -q 'BakerTillyUS'; done
      - name: Commit generated PDFs to main
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add docs/*.pdf
          if git diff --cached --quiet; then
            echo "PDFs already current"
          else
            git commit -m "Regenerate corrected candidate PDFs"
            git push origin main
          fi
'''

write("document-responsive.css", RESPONSIVE_CSS)
write("120-day-plan.html", PLAN_HTML)
write("scripts/generate-pdfs.mjs", GENERATOR)
write(".github/workflows/generate-pdfs.yml", WORKFLOW)

# Apply confident, positive-fit copy and remove the public interview-thesis artifact.
index = read("index.html")
index = index.replace(
    '<a class="button text-button" href="interview-brief.html">Read the interview thesis</a>',
    '<a class="button text-button" href="120-day-plan.html">Review the 120-day plan</a>',
)
index = index.replace(
    'This is not platform ownership. It is value-realization ownership:',
    'The role owns value realization:',
)
index = index.replace(
    'The fit is not a claim of prior Baker Tilly experience. It is a demonstrated pattern of building mechanisms that connect emerging technology, operating priorities, human judgment, and measurable execution.',
    'Russell brings a repeatable pattern of turning emerging technology into operating advantage—connecting strategy, workflow design, technical translation, human judgment, adoption, and measurable execution.',
)
write("index.html", index)

cover = read("cover-letter.html")
cover = cover.replace(
    '<p>I have prepared an independent candidate vision, a Value Conversion Review, and a 120-day entry plan in this application package to make that operating approach concrete. They are not claims about Baker Tilly’s undisclosed internal processes; they are a working hypothesis for discussion, grounded in the role description and Baker Tilly’s public direction.</p>',
    '<p>I have prepared an independent candidate vision, a Value Conversion Review, and a 120-day entry plan to make that operating approach concrete. Together, they show how I would connect practice priorities, technical capability, adoption, and measurable value from the first 120 days forward.</p>',
)
write("cover-letter.html", cover)

# Add the responsive stylesheet and remove every public link to the deleted artifact.
for name in ["index.html", "resume.html", "cover-letter.html", "value-conversion-review.html"]:
    text = read(name)
    if 'document-responsive.css' not in text:
        text = text.replace(
            '<link rel="stylesheet" href="styles.css">',
            '<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="document-responsive.css">',
        )
    text = re.sub(r'<a\s+href="interview-brief\.html"[^>]*>.*?</a>', '', text, flags=re.I | re.S)
    write(name, text)

readme_path = ROOT / "README.md"
if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
    readme = re.sub(r'^.*interview-brief.*\n?', '', readme, flags=re.I | re.M)
    readme = re.sub(r'^.*Interview Thesis.*\n?', '', readme, flags=re.I | re.M)
    readme_path.write_text(readme.rstrip() + "\n", encoding="utf-8")

for obsolete in [
    ROOT / "interview-brief.html",
    ROOT / "docs/Russell-Dudek-Baker-Tilly-Interview-Thesis-Brief.pdf",
]:
    if obsolete.exists():
        obsolete.unlink()

# Regression checks: no defensive candidate framing, odd phrase, or public interview-thesis artifact.
banned = [
    "prior Baker Tilly experience",
    "not a claim",
    "Interview thesis",
    "Interview Brief",
    "Listen at the work",
]
for path in list(ROOT.glob("*.html")) + list(ROOT.glob("*.md")):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in banned:
        if phrase.lower() in text.lower():
            raise SystemExit(f"Banned phrase remains in {path}: {phrase}")

print("Applied responsive document, positive-fit copy, and 120-day plan corrections.")
