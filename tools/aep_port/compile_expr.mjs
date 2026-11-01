// Rewrite After Effects expressions so they run in a plain browser JS engine.
// AE allows vector math with operators (value + [x,y], arr * 2, -arr); JS does not,
// so + - * / and unary - become __add/__sub/__mul/__div/__neg calls, and
// compound assignments (a += b) become a = __add(a, b).
// usage: node compile_expr.mjs spec.json  (adds "js" next to every "expr", in place)
import fs from "fs";
import * as acorn from "acorn";
import { generate } from "astring";

const OPS = { "+": "__add", "-": "__sub", "*": "__mul", "/": "__div" };
const call = (name, args) => ({ type: "CallExpression", callee: { type: "Identifier", name }, arguments: args, optional: false });

function rewrite(node) {
  if (!node || typeof node.type !== "string") return node;
  for (const k of Object.keys(node)) {
    const v = node[k];
    if (Array.isArray(v)) node[k] = v.map((x) => (x && typeof x.type === "string" ? rewrite(x) : x));
    else if (v && typeof v.type === "string") node[k] = rewrite(v);
  }
  if (node.type === "BinaryExpression" && OPS[node.operator]) return call(OPS[node.operator], [node.left, node.right]);
  if (node.type === "UnaryExpression" && node.operator === "-") return call("__neg", [node.argument]);
  if (node.type === "AssignmentExpression" && OPS[node.operator[0]] && node.operator.length === 2) {
    const target = node.left;
    return { type: "AssignmentExpression", operator: "=", left: target,
             right: call(OPS[node.operator[0]], [JSON.parse(JSON.stringify(target)), node.right]) };
  }
  return node;
}

export function compile(src) {
  const ast = acorn.parse(src, { ecmaVersion: 2020, sourceType: "script", allowReturnOutsideFunction: true });
  return generate(rewrite(ast));
}

if (process.argv[2]) {
  const file = process.argv[2];
  const spec = JSON.parse(fs.readFileSync(file, "utf8"));
  let n = 0, bad = 0;
  const walk = (o) => {
    if (Array.isArray(o)) return o.forEach(walk);
    if (o && typeof o === "object") {
      if (typeof o.expr === "string") {
        try { o.js = compile(o.expr); n++; } catch (e) { o.js_error = String(e); bad++; }
      }
      Object.values(o).forEach(walk);
    }
  };
  walk(spec);
  fs.writeFileSync(file, JSON.stringify(spec));
  console.log(`${file}: compiled ${n} expressions, ${bad} failed`);
}
