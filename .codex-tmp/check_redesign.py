from pathlib import Path
import json
from urllib.parse import unquote, urlparse
from playwright.sync_api import sync_playwright, expect

root = Path.cwd()
out = root / '.codex-tmp/redesign-qa'
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless=True)
    page = browser.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto((root/'index.html').as_uri())
    results = []
    for lang in ['en', 'zh']:
        page.evaluate('(lang) => applyLanguage(lang)', lang)
        for width in [1440,1024,768,390,320]:
            page.set_viewport_size({'width':width,'height':1000})
            page.evaluate('window.scrollTo(0,0)')
            data = page.evaluate('''() => ({
              width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
              cols: getComputedStyle(document.querySelector('.hero-stats')).gridTemplateColumns,
              overflow: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1).map(e => e.className),
              missing: [...document.querySelectorAll('[data-i18n]')].filter(e => !translations[currentLang][e.dataset.i18n]).map(e => e.dataset.i18n),
              resume: document.getElementById('resume-link').getAttribute('href')
            })''')
            assert data['scrollWidth'] == width and not data['overflow'], data
            assert not data['missing'], data
            results.append({'lang':lang,**data})
            if width in [1440,390,320]:
                page.screenshot(path=str(out/f'{lang}-{width}.png'), full_page=True)
        page.locator('#lang-toggle').click()
        expected = 'zh-CN' if lang == 'en' else 'en'
        page.reload()
        assert page.locator('html').get_attribute('lang') == expected
    for href in page.locator('a').evaluate_all('(nodes) => nodes.map(n=>n.getAttribute("href"))'):
        if href.startswith('#'):
            assert page.locator(href).count() == 1, href
        elif not urlparse(href).scheme:
            assert (root/unquote(href)).is_file(), href
    page.set_viewport_size({'width':390,'height':850})
    for anchor in ['projects','experience','contact','about']:
        page.locator(f'.nav-links a[href="#{anchor}"]').click()
        expect(page.locator(f'.nav-links a[href="#{anchor}"]')).to_have_attribute('aria-current', 'page')
    assert page.locator('.project').count() == 8
    assert not errors, errors
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print('PASS: 10 layouts, language persistence, local assets, anchors, 8 projects, no JavaScript errors')
    browser.close()
