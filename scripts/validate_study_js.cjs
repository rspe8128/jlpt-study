const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

const html = fs.readFileSync(studyHtml, "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
console.log("script blocks:", scripts.length);

for (let i = 0; i < scripts.length; i++) {
  const code = scripts[i][1];
  try {
    new Function(code);
    console.log(`block ${i + 1}: OK (${code.length} chars)`);
  } catch (e) {
    console.log(`block ${i + 1}: FAIL — ${e.message}`);
    const pos = Number((e.message.match(/position (\d+)/) || [])[1]);
    if (pos) {
      const snippet = code.slice(Math.max(0, pos - 80), pos + 80);
      console.log("near:", JSON.stringify(snippet));
    }
  }
}

// Check template literals
for (const name of ["RAW", "VOCAB_RAW", "HIRA_RAW", "N5_VOCAB_LEGACY_RAW"]) {
  const re = new RegExp(`const ${name} = \`([\\s\\S]*?)\`;`);
  const m = html.match(re);
  if (!m) console.log(name, "MISSING or unclosed");
  else console.log(name, "lines", m[1].split("\n").length);
}
