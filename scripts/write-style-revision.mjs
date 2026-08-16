import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';

const cssPath = new URL('../output/_shared/tailwind.css', import.meta.url);
const revisionPath = new URL('../demos/shared-style.js', import.meta.url);
const css = await readFile(cssPath);
const revision = createHash('sha256').update(css).digest('hex').slice(0, 16);

await writeFile(
  revisionPath,
  `// Generado por npm run build:styles. Cambia con cada contenido de Tailwind.\nexport const SHARED_STYLE_REV = '${revision}';\n`,
);
