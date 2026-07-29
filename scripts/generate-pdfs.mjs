import { chromium } from 'playwright';
import { readFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const sharedCss = `${await readFile(path.join(root, 'brand-tokens.css'), 'utf8')}\n${await readFile(path.join(root, 'styles.css'), 'utf8')}\n${await readFile(path.join(root, 'document-responsive.css'), 'utf8')}`;
const planCss = await readFile(path.join(root, 'plan-density.css'), 'utf8');
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
  if (source === '120-day-plan.html') {
    html = html.replace(
      '<link rel="stylesheet" href="brand-tokens.css"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="document-responsive.css"><link rel="stylesheet" href="plan-density.css">',
      `<style>${sharedCss}\n${planCss}</style>`,
    );
  } else {
    html = html.replace(
      '<link rel="stylesheet" href="brand-tokens.css"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="document-responsive.css">',
      `<style>${sharedCss}</style>`,
    );
  }
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
