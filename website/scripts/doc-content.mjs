import { fromMarkdown } from 'mdast-util-from-markdown';
import { toMarkdown } from 'mdast-util-to-markdown';
import { posix } from 'node:path';

const origin = 'https://skillpot.modepot.io';
const routes = new Map([
  ['README.md', '/'], ['README.md#quick-start', '/quickstart/'],
  ['README.md#boundaries', '/limits/'], ['catalog/README.md', '/catalogue/'],
  ['docs/quickstart.md', '/host-setup/'], ['docs/skill-contract.md', '/authoring/'],
  ['docs/release-policy.md', '/provenance-refresh/'],
]);
const textOf = node => typeof node.value === 'string' ? node.value : (node.children || []).map(textOf).join('');

export function canonicalBody(source, filename, start, end) {
  const tree = fromMarkdown(source);
  if (start) {
    const begin = tree.children.findIndex(node => node.type === 'heading' && node.depth === 2 && textOf(node) === start);
    const finish = tree.children.findIndex((node, index) => index > begin && node.type === 'heading' && node.depth === 2 && textOf(node) === end);
    if (begin < 0 || finish < 0) throw new Error(`Missing canonical section ${filename}: ${start}`);
    return source.slice(tree.children[begin].position.end.offset, tree.children[finish].position.start.offset).trim();
  }
  const heading = tree.children[0];
  return (heading?.type === 'heading' && heading.depth === 1 ? source.slice(heading.position.end.offset) : source).trim();
}

function canonicalUrl(destination, filename) {
  if (/^(?:[a-z][a-z\d+.-]*:|#|\/\/)/i.test(destination)) return destination;
  const hash = destination.indexOf('#');
  const path = hash < 0 ? destination : destination.slice(0, hash);
  const fragment = hash < 0 ? '' : destination.slice(hash);
  const decoded = decodeURIComponent(path);
  const target = posix.normalize(decoded.startsWith('/') ? decoded.slice(1) : posix.join(posix.dirname(filename), decoded));
  if (target === '..' || target.startsWith('../')) throw new Error(`Documentation link leaves repository: ${destination}`);
  if (routes.has(target + fragment)) return origin + routes.get(target + fragment);
  // The curated homepage does not contain every heading from the repository README.
  if (routes.has(target) && !(target === 'README.md' && fragment)) return origin + routes.get(target) + fragment;
  return 'https://github.com/tugrulguner/skillpot/blob/main/' + target.split('/').map(encodeURIComponent).join('/') + fragment;
}

export function rewriteLinks(source, filename) {
  const tree = fromMarkdown(source);
  const edits = [];
  function visit(node, insideLink = false) {
    const isLink = ['link', 'image', 'definition'].includes(node.type);
    let changed = false;
    if (isLink) {
      const replacement = canonicalUrl(node.url, filename);
      changed = replacement !== node.url;
      node.url = replacement;
    }
    for (const child of node.children || []) changed = visit(child, insideLink || isLink) || changed;
    if (isLink && !insideLink && changed) {
      const children = node.type === 'definition' ? [node] : [{type:'paragraph', children:[node]}];
      const replacement = toMarkdown({type:'root', children}).trimEnd();
      edits.push({start:node.position.start.offset, end:node.position.end.offset, replacement});
    }
    return changed;
  }
  visit(tree);
  for (const edit of edits.sort((a, b) => b.start - a.start)) source = source.slice(0, edit.start) + edit.replacement + source.slice(edit.end);
  return source;
}
