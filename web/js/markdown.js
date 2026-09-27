/*
 * WIDS tiny markdown renderer (safe subset).
 * Block: # headings, > blockquote, - / * / 1. lists (nested by indent), - [ ] tasks,
 *        ``` fenced code, | pipe tables |, --- rules, paragraphs.
 * Inline: `code`, **bold**, *italic*, [text](url).
 * All text is HTML-escaped first; only http(s)/mailto links become <a>,
 * external links get target="_blank" rel="noopener noreferrer".
 * opts.resolveLink(href) → {href, internal?:slug} lets callers map relative links.
 * opts.codeLink(code)    → slug|null turns `foo.md` code spans into in-app links.
 * Works in browsers (window.WIDS_MD) and Node (module.exports).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_MD = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function safeUrl(href) {
    var h = String(href).trim();
    if (/^(https?:|mailto:)/i.test(h)) return h;
    return null;
  }

  function inline(text, opts) {
    // Protect code spans first (their content is escaped, not formatted).
    var slots = [];
    function slot(html) { slots.push(html); return '\u0000' + (slots.length - 1) + '\u0000'; }
    var s = String(text).replace(/`([^`]+)`/g, function (_, code) {
      var slug = opts.codeLink ? opts.codeLink(code) : null;
      if (slug) return slot('<a href="#pattern=' + esc(slug) + '" class="md-internal" data-pattern="' + esc(slug) + '"><code>' + esc(code) + '</code></a>');
      return slot('<code>' + esc(code) + '</code>');
    });
    // Links [text](url) — handled before escaping so we can validate raw URL.
    s = s.replace(/\[([^\]]+)\]\(((?:[^()\s]|\([^()\s]*\))+)(?:\s+"[^"]*")?\)/g, function (_, label, href) {
      var resolved = opts.resolveLink ? opts.resolveLink(href) : null;
      if (resolved && resolved.internal) {
        return slot('<a href="#pattern=' + esc(resolved.internal) + '" class="md-internal" data-pattern="' + esc(resolved.internal) + '">' + inlineFormat(esc(label)) + '</a>');
      }
      var url = safeUrl(resolved && resolved.href ? resolved.href : href);
      if (!url) return slot(inlineFormat(esc(label)));
      return slot('<a href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + inlineFormat(esc(label)) + '</a>');
    });
    s = inlineFormat(esc(s));
    return s.replace(/\u0000(\d+)\u0000/g, function (_, i) { return slots[+i]; });
  }

  function inlineFormat(escaped) {
    return escaped
      .replace(/\*\*([^*]+?)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?!\w)/g, '$1<em>$2</em>');
  }

  function isTableSep(line) { return /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(line); }
  function splitRow(line) {
    var t = line.trim();
    if (t.charAt(0) === '|') t = t.slice(1);
    if (t.charAt(t.length - 1) === '|') t = t.slice(0, -1);
    return t.split('|').map(function (c) { return c.trim(); });
  }

  function render(md, opts) {
    opts = opts || {};
    var lines = String(md == null ? '' : md).replace(/\r\n?/g, '\n').split('\n');
    var out = [];
    var i = 0;
    var para = [];
    function flushPara() {
      if (para.length) { out.push('<p>' + inline(para.join(' '), opts) + '</p>'); para = []; }
    }
    while (i < lines.length) {
      var line = lines[i];
      var m;
      if (/^\s*```/.test(line)) {
        flushPara();
        var lang = line.replace(/^\s*```/, '').trim();
        var buf = [];
        i++;
        while (i < lines.length && !/^\s*```/.test(lines[i])) { buf.push(lines[i]); i++; }
        i++;
        out.push('<pre><code' + (lang ? ' class="lang-' + esc(lang.replace(/[^\w-]/g, '')) + '"' : '') + '>' + esc(buf.join('\n')) + '</code></pre>');
        continue;
      }
      if (/^\s*$/.test(line)) { flushPara(); i++; continue; }
      if ((m = /^(#{1,6})\s+(.*?)\s*#*\s*$/.exec(line))) {
        flushPara();
        var lvl = m[1].length;
        out.push('<h' + lvl + '>' + inline(m[2], opts) + '</h' + lvl + '>');
        i++; continue;
      }
      if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) { flushPara(); out.push('<hr>'); i++; continue; }
      if (/^\s*>/.test(line)) {
        flushPara();
        var q = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) { q.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
        out.push('<blockquote>' + render(q.join('\n'), opts) + '</blockquote>');
        continue;
      }
      if (/^\s*\|/.test(line) && i + 1 < lines.length && isTableSep(lines[i + 1])) {
        flushPara();
        var head = splitRow(line);
        i += 2;
        var body = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) { body.push(splitRow(lines[i])); i++; }
        var t = '<div class="md-table"><table><thead><tr>' + head.map(function (c) { return '<th>' + inline(c, opts) + '</th>'; }).join('') + '</tr></thead><tbody>';
        body.forEach(function (r) { t += '<tr>' + r.map(function (c) { return '<td>' + inline(c, opts) + '</td>'; }).join('') + '</tr>'; });
        out.push(t + '</tbody></table></div>');
        continue;
      }
      if (/^\s*([-*+]|\d+[.)])\s+/.test(line)) {
        flushPara();
        var items = [];
        while (i < lines.length) {
          var l = lines[i];
          var lm = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/.exec(l);
          if (lm && items.length && lm[1].replace(/\t/g, '    ').length <= items[0].indent && /\d/.test(lm[2]) !== items[0].ordered) break;
          if (lm) { items.push({ indent: lm[1].replace(/\t/g, '    ').length, ordered: /\d/.test(lm[2]), text: lm[3] }); i++; continue; }
          if (/^\s+\S/.test(l) && items.length) { items[items.length - 1].text += ' ' + l.trim(); i++; continue; }
          break;
        }
        out.push(renderList(items, 0, items.length, opts));
        continue;
      }
      para.push(line.trim());
      i++;
    }
    flushPara();
    return out.join('\n');
  }

  function renderList(items, start, end, opts) {
    if (start >= end) return '';
    var base = items[start].indent;
    var tag = items[start].ordered ? 'ol' : 'ul';
    var html = '<' + tag + '>';
    var k = start;
    while (k < end) {
      var it = items[k];
      var j = k + 1;
      while (j < end && items[j].indent > base) j++;
      var text = it.text, cls = '';
      var tm = /^\[( |x|X)\]\s+(.*)$/.exec(text);
      if (tm) { cls = ' class="task"'; text = (tm[1] === ' ' ? '☐ ' : '☑ ') + tm[2]; }
      html += '<li' + cls + '>' + inline(text, opts) + renderList(items, k + 1, j, opts) + '</li>';
      k = j;
    }
    return html + '</' + tag + '>';
  }

  return { render: render, escapeHtml: esc, inline: inline };
});
