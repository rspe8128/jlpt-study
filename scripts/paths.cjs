const path = require("path");

const ROOT = path.join(__dirname, "..");
const DATA = path.join(ROOT, "data");

module.exports = {
  ROOT,
  DATA,
  studyHtml: path.join(ROOT, "study.html"),
  vocab: (name) => path.join(DATA, "vocab", name),
  kanjiRaw: path.join(DATA, "kanji", "kanji_raw.tsv"),
  sources: (name) => path.join(DATA, "sources", name),
};
