from html import escape

from glossary import CATEGORIES, GLOSSARY

_GA = """  <script>
    if (location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-HC5MG3MW4T';
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-HC5MG3MW4T');
    }
  </script>"""

_STYLE = """    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Hiragino Sans', 'Noto Sans JP', sans-serif;
      background: #fff; color: #374151; min-height: 100dvh;
      display: flex; flex-direction: column;
    }
    a { color: #2563eb; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .site-header { background: #fff; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 100; }
    .site-header-inner { max-width: 896px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; gap: 16px; }
    .back-link { font-size: 13px; color: #6b7280; }
    .back-link:hover { color: #111827; text-decoration: none; }
    .header-brand { font-size: 14px; font-weight: 700; color: #111827; }
    main { flex: 1; max-width: 896px; margin: 0 auto; padding: 40px 16px 64px; width: 100%; }
    h1 { font-size: 24px; font-weight: 700; color: #111827; margin-bottom: 8px; }
    .lead { font-size: 14px; line-height: 1.8; color: #4b5563; margin-bottom: 20px; }
    .search {
      width: 100%; padding: 10px 14px; font-size: 16px; color: #111827;
      border: 1px solid #d1d5db; border-radius: 10px; margin-bottom: 14px;
    }
    .cat-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 32px; }
    .cat-nav a {
      font-size: 12px; color: #1a4580; background: #eef4fb;
      padding: 5px 12px; border-radius: 999px;
    }
    .cat-nav a:hover { text-decoration: none; background: #dbeafe; }
    .cat { margin-bottom: 36px; scroll-margin-top: 64px; }
    .cat h2 { font-size: 17px; font-weight: 700; color: #111827; padding-bottom: 8px; border-bottom: 2px solid #dbeafe; margin-bottom: 4px; }
    dl.terms > div { padding: 14px 0; border-bottom: 1px solid #f0f2f5; scroll-margin-top: 64px; }
    dl.terms > div:target { background: #fffbe6; margin: 0 -8px; padding: 14px 8px; border-radius: 8px; }
    dt { font-size: 15px; font-weight: 700; color: #111827; }
    dt .reading { font-size: 12px; font-weight: 400; color: #9ca3af; margin-left: 8px; }
    dd { font-size: 14px; line-height: 1.8; color: #4b5563; margin-top: 4px; }
    dd .also { display: block; font-size: 12px; color: #9ca3af; margin-top: 2px; }
    .empty { display: none; font-size: 14px; color: #6b7280; padding: 24px 0; text-align: center; }
    .cta { display: block; text-align: center; background: #1a4580; color: #fff; font-weight: 700; padding: 14px; border-radius: 12px; margin-top: 8px; }
    .cta:hover { text-decoration: none; opacity: .9; }
    .note { font-size: 11px; color: #9ca3af; line-height: 1.7; margin-top: 20px; }
    .site-footer { background: #111827; color: #fff; padding: 36px 16px 24px; }
    .site-footer-inner { max-width: 896px; margin: 0 auto; }
    .site-footer-brand { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
    .site-footer-tagline { font-size: 13px; color: #9ca3af; margin-bottom: 20px; }
    .site-footer-links { display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
    .site-footer-links a { font-size: 13px; color: #9ca3af; }
    .site-footer-links a:hover { color: #fff; text-decoration: none; }
    .site-footer-copy { font-size: 12px; color: #6b7280; border-top: 1px solid #1f2937; padding-top: 20px; }"""

_SCRIPT = """  <script>
    (function () {
      var input = document.getElementById('q');
      var cats = document.querySelectorAll('.cat');
      var empty = document.getElementById('empty');
      input.addEventListener('input', function () {
        var kw = input.value.trim().toLowerCase();
        var total = 0;
        cats.forEach(function (cat) {
          var shown = 0;
          cat.querySelectorAll('dl.terms > div').forEach(function (row) {
            var hit = !kw || row.getAttribute('data-search').indexOf(kw) !== -1;
            row.hidden = !hit;
            if (hit) shown++;
          });
          cat.hidden = shown === 0;
          total += shown;
        });
        empty.style.display = total === 0 ? 'block' : 'none';
      });
    })();
  </script>"""


def _entry(g: dict) -> str:
    term = escape(g["term"])
    search = escape(" ".join([g["term"], g["reading"], *g["aliases"], g["desc"]]).lower())
    also = ""
    if g["aliases"]:
        also = f'<span class="also">同じ意味：{escape("、".join(g["aliases"]))}</span>'
    return (
        f'<div id="{term}" data-search="{search}">'
        f'<dt>{term}<span class="reading">{escape(g["reading"])}</span></dt>'
        f'<dd>{escape(g["desc"])}{also}</dd></div>'
    )


def render_glossary_html() -> str:
    nav = []
    sections = []
    for i, cat in enumerate(CATEGORIES):
        items = sorted((g for g in GLOSSARY if g["category"] == cat), key=lambda g: g["reading"])
        if not items:
            continue
        nav.append(f'<a href="#cat-{i}">{escape(cat)}</a>')
        rows = "\n".join(_entry(g) for g in items)
        sections.append(
            f'<section class="cat" id="cat-{i}">\n<h2>{escape(cat)}（{len(items)}語）</h2>\n'
            f'<dl class="terms">\n{rows}\n</dl>\n</section>'
        )
    desc = "釣りクイズに出てくる釣り用語を、やさしく解説。ライン、アタリ、マズメ、ショアジギングなど、初心者がつまずく言葉をカテゴリ別にまとめました。"
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>釣り用語集 | つれた日。</title>
  <meta name="description" content="{escape(desc)}">
{_GA}
  <style>
{_STYLE}
  </style>
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a href="/" class="back-link">← クイズへ戻る</a>
    <span class="header-brand">つれた日。/ 釣りクイズ</span>
  </div>
</header>

<main>
  <h1>釣り用語集</h1>
  <p class="lead">釣りクイズの解説に出てくる用語を、カテゴリ別にまとめました（{len(GLOSSARY)}語）。クイズの解説では、点線の付いた用語をタップ（PCではマウスを乗せる）すると意味が表示されます。</p>
  <input id="q" class="search" type="search" placeholder="用語を検索（例：アタリ、潮、ルアー）" aria-label="用語を検索">
  <nav class="cat-nav">{"".join(nav)}</nav>
{chr(10).join(sections)}
  <p id="empty" class="empty">見つかりませんでした。</p>
  <a class="cta" href="/">釣りクイズに挑戦する</a>
  <p class="note">用語の説明は、AIを活用して作成した一般的な内容です。地域や釣り場、釣り人によって呼び方や使い方が異なる場合があります。</p>
</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    <div class="site-footer-brand">つれた日。</div>
    <div class="site-footer-tagline">たのしいをつろう。</div>
    <div class="site-footer-links">
      <a href="/">釣りクイズ</a>
      <a href="/privacy.html">プライバシーポリシー</a>
      <a href="mailto:tsuretahi@gmail.com">お問い合わせ</a>
    </div>
    <div class="site-footer-copy">© 2026 tsuretahi. All rights reserved.</div>
  </div>
</footer>

{_SCRIPT}
</body>
</html>
"""
