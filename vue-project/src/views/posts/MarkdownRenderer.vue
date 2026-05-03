<script setup>
import { computed } from "vue";

import { marked } from "marked";

import hljs from "highlight.js";

import "highlight.js/styles/github-dark.css";

const props = defineProps({
  content: {
    type: String,
    default: "",
  },
});

/* =========================
   HIGHLIGHT CONFIG
========================= */

marked.setOptions({
  breaks: true,
});

/* =========================
   CUSTOM RENDERER
========================= */

const renderer = new marked.Renderer();

renderer.code = ({ text, lang }) => {
  const language = hljs.getLanguage(lang)
    ? lang
    : "plaintext";

  const highlighted = hljs.highlight(
    text,
    { language }
  ).value;

  return `
    <pre class="code-block">
      <code class="hljs ${language}">
        ${highlighted}
      </code>
    </pre>
  `;
};

/* =========================
   COMPILED HTML
========================= */

const compiledMarkdown = computed(() => {
  return marked(props.content || "", {
    renderer,
  });
});
</script>

<template>
  <div
    class="markdown-body"
    v-html="compiledMarkdown"
  />
</template>