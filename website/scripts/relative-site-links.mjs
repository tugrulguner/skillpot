// Native Sätteri plugin: portable Markdown, serving-origin HTML navigation.
export const relativeSiteLinks = {
  name: 'skillpot-relative-site-links',
  element: {
    filter: ['a'],
    visit(node, context) {
      let href = node.properties?.href;
      if (typeof href !== 'string') return;
      if (href.startsWith('https://skillpot.modepot.io/')) {
        const url = new URL(href);
        href = url.pathname + url.search + url.hash;
        context.setProperty(node, 'href', href);
      }
      if (/^\/downloads\/[^/?#]+\.md$/.test(href)) {
        context.setProperty(node, 'download', href.split('/').at(-1));
      }
    },
  },
};
