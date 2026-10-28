import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { satteri } from '@astrojs/markdown-satteri';
import { relativeSiteLinks } from './scripts/relative-site-links.mjs';

export default defineConfig({
  site: 'https://skillpot.modepot.io',
  markdown: { processor: satteri({ hastPlugins: [relativeSiteLinks] }) },
  vite: { preview: { strictPort: true } },
  integrations: [starlight({
    title: 'SkillPot',
    description: 'Practical, installable agent skills for building, researching, and presenting real work.',
    favicon: '/assets/skillpot-mark.svg',
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/tugrulguner/skillpot' }],
    customCss: ['./src/styles/custom.css', './src/styles/product.css'],
    components: { Header: './src/components/FamilyHeader.astro', Hero: './src/components/ProductHero.astro', Head: './src/components/DocumentationHead.astro' },
    sidebar: [
      { label: 'Start here', items: [{ slug: 'index', label: 'Overview' }, { slug: 'quickstart' }, { slug: 'catalogue' }] },
      { label: 'Guides', items: [{ slug: 'host-setup' }, { slug: 'authoring' }, { slug: 'provenance-refresh' }] },
      { label: 'Reference', items: [{ slug: 'limits' }] },
    ],
  })],
});
