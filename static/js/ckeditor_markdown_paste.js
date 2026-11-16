/*
 * CKEditor 5 plugin: when plain-text Markdown is pasted (e.g. text copied with a
 * "Copy" button from a chat), convert it to formatted content instead of
 * inserting the raw ** and ## characters.
 *
 * Rich pastes (copied from a web page, Word, Google Docs) are left untouched.
 * Registered through CKEDITOR_5_CONFIGS: "extraPlugins": ["callback:MarkdownPastePlugin"].
 */
(function () {
  var MARKDOWN_HINTS = [
    /^#{1,6}\s+\S/m,           // # heading
    /^\s*[-*+]\s+\S/m,         // - list item
    /^\s*\d+[.)]\s+\S/m,       // 1. list item
    /^\s*>\s?\S/m,             // > quote
    /^\s*```/m,                // ``` code block
    /\*\*[^*\n]+\*\*/,         // **bold**
    /`[^`\n]+`/,               // `inline code`
    /\[[^\]\n]+\]\([^)\s]+\)/, // [link](url)
    /^\s*\|.*\|\s*$/m,         // | table |
  ];

  function looksLikeMarkdown(text) {
    return MARKDOWN_HINTS.some(function (re) { return re.test(text); });
  }

  window.MarkdownPastePlugin = function (editor) {
    editor.editing.view.document.on("clipboardInput", function (evt, data) {
      if (data.content || !data.dataTransfer) return;           // already handled
      if (data.dataTransfer.getData("text/html")) return;       // rich paste
      var text = data.dataTransfer.getData("text/plain");
      if (!text || !looksLikeMarkdown(text)) return;

      // Inside a code block, paste text as-is.
      var position = editor.model.document.selection.getFirstPosition();
      if (position && position.parent.is("element", "codeBlock")) return;

      // With the Markdown plugin the editor's data processor understands GFM.
      var processor = editor.data.processor;
      if (!processor || typeof processor.toView !== "function") return;

      data.content = processor.toView(text.replace(/\r\n?/g, "\n"));
    }, { priority: "high" });
  };
})();
