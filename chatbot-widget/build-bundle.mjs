/**
 * Post-build script: concatenates polyfills.js + main.js from the Angular build
 * into a single agentrix-chat.js and copies it to frontend/src/assets/.
 *
 * Run automatically via: npm run build (in chatbot-widget/)
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
// browser builder (webpack) outputs into dist root; application builder into dist/browser
const distRoot = join(__dirname, 'dist', 'agentrix-chat');
const distBrowser = existsSync(join(distRoot, 'browser'))
  ? join(distRoot, 'browser')
  : distRoot;
const outDir = join(__dirname, '..', 'frontend', 'src', 'assets');

// webpack browser builder emits runtime.js first, then polyfills.js, then main.js
const candidates = ['runtime.js', 'polyfills.js', 'main.js'];
const parts = [];

for (const name of candidates) {
  const filePath = join(distBrowser, name);
  if (existsSync(filePath)) {
    parts.push(readFileSync(filePath, 'utf-8'));
  }
}

if (parts.length === 0) {
  throw new Error(`No JS output found in ${distBrowser}. Run 'ng build' first.`);
}

const outFile = join(outDir, 'agentrix-chat.js');
writeFileSync(outFile, parts.join('\n'));
console.log(`✅  agentrix-chat.js → frontend/src/assets/agentrix-chat.js`);
