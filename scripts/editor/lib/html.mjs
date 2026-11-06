// Tiny HTML source scanner (no dependencies). It finds elements in index.html
// by the editor's selector keys ("#id" or "#id > :nth-child(n) > ...") so a
// text edit can be written back into the file without reformatting anything else.

const VOID = new Set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"]);
const RAW = new Set(["script", "style", "textarea", "title"]);

// Returns the root node; each element node = { tag, attrs, start, openEnd, closeStart, end, children, parent }.
export function parse(src) {
  const root = { tag: "#root", children: [], start: 0, openEnd: 0, closeStart: src.length, end: src.length, attrs: "" };
  const stack = [root];
  let i = 0;
  while (i < src.length) {
    const lt = src.indexOf("<", i);
    if (lt === -1) break;
    if (src.startsWith("<!--", lt)) {
      const e = src.indexOf("-->", lt + 4);
      i = e === -1 ? src.length : e + 3;
      continue;
    }
    if (src[lt + 1] === "!" || src[lt + 1] === "?") {
      const e = src.indexOf(">", lt);
      i = e === -1 ? src.length : e + 1;
      continue;
    }
    const tagEnd = findTagEnd(src, lt);
    if (tagEnd === -1) break;
    const raw = src.slice(lt, tagEnd + 1);
    const close = raw.match(/^<\/\s*([A-Za-z][\w:-]*)/);
    if (close) {
      const name = close[1].toLowerCase();
      for (let k = stack.length - 1; k > 0; k--) {
        if (stack[k].tag === name) {
          for (let j = stack.length - 1; j >= k; j--) {
            const n = stack[j];
            if (j === k) {
              n.closeStart = lt;
              n.end = tagEnd + 1;
            } else {
              n.closeStart = n.end = lt;
            }
          }
          stack.length = k;
          break;
        }
      }
      i = tagEnd + 1;
      continue;
    }
    const open = raw.match(/^<([A-Za-z][\w:-]*)([\s\S]*?)(\/?)>$/);
    if (!open) {
      i = lt + 1;
      continue;
    }
    const tag = open[1].toLowerCase();
    const parent = stack[stack.length - 1];
    const node = { tag, attrs: open[2], start: lt, openEnd: tagEnd + 1, closeStart: tagEnd + 1, end: tagEnd + 1, children: [], parent };
    parent.children.push(node);
    if (VOID.has(tag) || open[3] === "/") {
      i = tagEnd + 1;
      continue;
    }
    if (RAW.has(tag)) {
      const closeIdx = src.toLowerCase().indexOf(`</${tag}`, tagEnd + 1);
      const ce = closeIdx === -1 ? src.length : src.indexOf(">", closeIdx) + 1;
      node.closeStart = closeIdx === -1 ? src.length : closeIdx;
      node.end = ce;
      i = ce;
      continue;
    }
    stack.push(node);
    i = tagEnd + 1;
  }
  return root;
}

function findTagEnd(src, lt) {
  let q = null;
  for (let i = lt + 1; i < src.length; i++) {
    const c = src[i];
    if (q) {
      if (c === q) q = null;
    } else if (c === '"' || c === "'") q = c;
    else if (c === ">") return i;
  }
  return -1;
}

export function attr(node, name) {
  const m = node.attrs.match(new RegExp(`(?:^|\\s)${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, "i"));
  return m ? (m[2] ?? m[3] ?? m[4]) : null;
}

function* walk(node) {
  for (const c of node.children) {
    yield c;
    yield* walk(c);
  }
}

export function findById(root, id) {
  for (const n of walk(root)) if (attr(n, "id") === id) return n;
  return null;
}

// Resolve "#id > :nth-child(2) > :nth-child(1)".
export function findBySelector(root, sel) {
  const parts = sel.split(" > ");
  let node = findById(root, parts[0].slice(1));
  for (const p of parts.slice(1)) {
    if (!node) return null;
    const n = Number(p.match(/\d+/)[0]);
    node = node.children[n - 1] || null;
  }
  return node;
}

export const innerHtml = (src, node) => src.slice(node.openEnd, node.closeStart);

export function replaceInner(src, node, html) {
  return src.slice(0, node.openEnd) + html + src.slice(node.closeStart);
}
