from pathlib import Path
import re, json, html

p = Path('index.html')
old = p.read_text()
s = old
css = '''
    :root { color-scheme: dark; --bg: #151719; --text: #ECEAE4; --muted: #A4AAA8; --accent: #9BB7A5; --line: #343a37; }
    * { box-sizing: border-box; }
    html { scroll-padding-top: 100px; }
    body { margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; font-size: 16px; line-height: 1.7; }
    a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 4px; transition: color .15s, background-color .15s, border-color .15s; }
    a:hover { color: var(--text); }
    button { font: inherit; cursor: pointer; }
    a:focus-visible, button:focus-visible { outline: 2px solid var(--accent); outline-offset: 5px; }
    .container { width: min(1120px, calc(100% - 80px)); margin-inline: auto; }
    .nav { position: sticky; top: 0; z-index: 10; background: var(--bg); border-bottom: 1px solid var(--line); }
    .nav-inner, .nav-group, .nav-links { display: flex; align-items: center; }
    .nav-inner { min-height: 78px; justify-content: space-between; gap: 24px; }
    .brand { font-weight: 600; white-space: nowrap; }
    .nav-group { gap: 28px; }
    .nav-links { gap: 28px; }
    .nav-links a { color: var(--muted); text-decoration: none; font-size: 14px; padding-block: 10px; }
    .nav-links a:hover, .nav-links a.active { color: var(--text); }
    .nav-links a.active { text-decoration: underline; text-decoration-color: var(--accent); text-underline-offset: 8px; }
    .lang-toggle { color: var(--text); background: transparent; border: 1px solid var(--line); border-radius: 4px; padding: 6px 12px; min-height: 40px; }
    .lang-toggle:hover { border-color: var(--accent); }
    .hero { padding: 76px 0 0; }
    .eyebrow { color: var(--accent); font-size: 15px; margin-bottom: 14px; }
    h1, h2, h3, p { margin-top: 0; }
    h1 { font-size: clamp(42px, 5.5vw, 72px); font-weight: 600; line-height: 1.12; letter-spacing: -.045em; margin-bottom: 26px; }
    h2 { font-size: 32px; line-height: 1.25; font-weight: 600; letter-spacing: -.025em; margin-bottom: 12px; }
    h3 { font-size: 22px; line-height: 1.4; font-weight: 600; letter-spacing: -.015em; margin-bottom: 16px; }
    .subtitle { max-width: 850px; font-size: 20px; line-height: 1.75; color: var(--muted); margin-bottom: 28px; }
    .actions { display: flex; align-items: center; flex-wrap: wrap; gap: 14px 24px; }
    .btn { display: inline-flex; justify-content: center; align-items: center; min-height: 46px; padding: 9px 20px; border: 1px solid var(--line); border-radius: 4px; text-decoration: none; color: var(--text); font-size: 15px; }
    .btn:hover { border-color: var(--accent); background: #202522; }
    .btn.primary { color: var(--bg); background: var(--accent); border-color: var(--accent); }
    .btn.primary:hover { background: #b4cbbb; }
    .text-link { font-size: 15px; }
    .hero-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0 32px; margin-top: 52px; }
    .stat-card { border-top: 1px solid var(--line); padding: 22px 0 26px; min-width: 0; }
    .stat-value { font-size: 19px; font-weight: 600; margin-bottom: 5px; }
    .stat-label { color: var(--muted); font-size: 14px; }
    .skills { border-top: 1px solid var(--line); margin-top: 12px; padding-top: 28px; }
    .quick-section { display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 32px; }
    .quick-label { display: block; color: var(--text); font-size: 15px; font-weight: 600; margin-bottom: 10px; }
    .quick-value { color: var(--muted); font-size: 15px; }
    .section { padding-top: 88px; }
    .section-desc { color: var(--muted); max-width: 760px; margin-bottom: 30px; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
    .card { border: 1px solid var(--line); border-radius: 5px; padding: 28px; min-width: 0; }
    .project { display: flex; flex-direction: column; }
    .meta { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; color: var(--muted); line-height: 1.8; margin-bottom: 14px; }
    .muted { color: var(--muted); font-size: 15px; }
    ul { padding-left: 20px; margin-top: 0; }
    li + li { margin-top: 8px; }
    .tags { display: flex; flex-wrap: wrap; gap: 8px 16px; margin-top: auto; padding-top: 12px; }
    .tag { color: var(--accent); font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; }
    .project-links { display: flex; flex-wrap: wrap; gap: 12px 24px; border-top: 1px solid var(--line); margin-top: 22px; padding-top: 18px; font-size: 14px; }
    .group-label { grid-column: 1 / -1; padding-top: 28px; }
    .group-label h3 { margin-bottom: 8px; }
    .group-label p { color: var(--muted); margin-bottom: 0; }
    #experience .grid { grid-template-columns: 1fr; gap: 0; }
    .timeline { border: 0; border-top: 1px solid var(--line); border-radius: 0; padding: 28px 0; }
    .timeline p { max-width: 940px; margin-bottom: 0; }
    #contact .card { padding: 24px 0; border: 0; border-top: 1px solid var(--line); border-radius: 0; }
    #contact .card p { margin-bottom: 10px; }
    .footer { margin-top: 56px; padding-block: 24px; border-top: 1px solid var(--line); color: var(--muted); font-size: 13px; }
    .footer p { margin-bottom: 0; }
    .stat-label, .quick-value, .card, .subtitle { overflow-wrap: anywhere; }
    @media (max-width: 899px) {
      .hero-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .quick-section { grid-template-columns: 1fr; gap: 22px; }
      .nav-group, .nav-links { gap: 18px; }
      .grid { grid-template-columns: 1fr; }
      .hero { padding-top: 56px; }
    }
    @media (max-width: 599px) {
      .container { width: calc(100% - 40px); }
      .nav-inner { flex-wrap: wrap; gap: 0; padding-top: 12px; }
      .brand { width: 100%; }
      .nav-group { width: 100%; justify-content: space-between; gap: 10px; padding-block: 6px 12px; }
      .nav-links { gap: 16px; }
      .nav-links a { font-size: 12px; }
      .lang-toggle { padding: 4px 8px; font-size: 12px; min-height: 34px; }
      html { scroll-padding-top: 125px; }
      .hero { padding-top: 40px; }
      .eyebrow { font-size: 13px; }
      .subtitle { font-size: 17px; }
      .actions { gap: 14px 20px; }
      .btn { padding-inline: 14px; }
      .hero-stats { grid-template-columns: 1fr; margin-top: 36px; }
      .stat-card { padding-block: 18px; }
      .section { padding-top: 60px; }
      h2 { font-size: 28px; }
      h3 { font-size: 21px; }
      .card { padding: 22px; }
      .timeline { padding: 24px 0; }
    }
    @media (max-width: 359px) {
      .nav-links { gap: 10px; }
      .nav-group { gap: 6px; }
      .actions { column-gap: 16px; }
      .btn { font-size: 14px; padding-inline: 12px; }
    }
'''
s = re.sub(r'  <style>.*?</style>', '  <style>'+css+'  </style>', s, flags=re.S)
s = re.sub(r'        <button class="scan-toggle".*?</button>\n', '', s, flags=re.S)
s = re.sub(r'          <a class="btn primary" href="#projects".*?</a>\n', '', s)
s = s.replace('class="btn" href="mailto:', 'class="btn primary" href="mailto:')
s = s.replace('class="btn" href="https://', 'class="text-link" href="https://')
s = s.replace('container hero-grid', 'container')
s = re.sub(r'      <div class="card hero-card">.*?<div class="quick-section">\s*<div class="quick-section-title".*?</div>', '      <div class="skills">\n        <div class="quick-section">', s, flags=re.S)
s = re.sub(r'\s*<span class="project-badge".*?</span>', '', s)
s = re.sub(r'<span class="project-icon".*?</span>', '', s)
s = re.sub(r'    const scanToggle.*?\n', '', s)
s = re.sub(r'    const savedScan.*?\n|    let scanEnabled.*?\n', '', s)
s = re.sub(r'    function updateScanToggle\(\) \{.*?\n    }\n', '', s, flags=re.S)
s = s.replace('      updateScanToggle();\n', '')
s = re.sub(r'    scanToggle.addEventListener.*?\n    }\);\n', '', s, flags=re.S)
updates = {
 'heroSubtitle': ["I’m an M.S. student in Electrical Engineering at Columbia University, working on RISC-V CPU/VPU architecture and ASIC design. I’m open to opportunities in hardware design, digital ICs, and computer architecture.", '我目前在哥伦比亚大学攻读电子工程硕士，专注于 RISC-V CPU/VPU 架构与 ASIC 设计。目前开放硬件设计、数字 IC 和计算机体系结构相关机会。'],
 'stat1Value': ['Columbia EE M.S.', 'Columbia EE M.S.'],
 'stat1Label': ['Expected December 2026', '预计 2026 年 12 月毕业'],
 'stat2Value': ['GPA 4.0/4.0', 'GPA 4.0/4.0'],
 'stat2Label': ['Columbia University', '哥伦比亚大学'],
 'stat3Value': ['CPU IP internship', 'CPU IP 实习'],
 'stat3Label': ['WingSemi · Jun–Sep 2026', '隼瞻科技 · 2026 年 6–9 月'],
 'stat4Value': ['VFCVT', 'VFCVT'],
 'stat4Label': ['FP64, FP32, FP16, BF16 & integer conversion', 'FP64、FP32、FP16、BF16 与整数转换'],
 'stat5Value': ['CNN ASIC', 'CNN ASIC'],
 'stat5Label': ['Apple sponsored · Taped out July 2026', 'Apple 赞助 · 2026 年 7 月投片'],
 'stat6Value': ['P6 RISC-V OoO', 'P6 RISC-V OoO'],
 'stat6Label': ['2-wide Fetch / Dispatch / Retire', '2-wide Fetch / Dispatch / Retire'],
 'skill1Label': ['EDA', 'EDA'], 'skill3Label': ['Focus', '研究与设计方向'],
 'ctaEmail': ['Email me', '邮件联系'], 'ctaResume': ['Download résumé', '下载简历'],
 'footer': ['© 2026 Linxiao Wu', '© 2026 吴林晓'],
 'contactDesc': ['For opportunities, project questions, or a conversation about hardware.', '欢迎联系我，交流工作机会、项目与硬件设计。'],
}
for key, values in updates.items():
    it = iter(values)
    s = re.sub(r'('+key+r': )"[^"\n]*"', lambda m: m[1]+json.dumps(next(it), ensure_ascii=False), s)
s = re.sub(r'^        (?:scanLabel|scanOn|scanOff|quickInfoTitle|skillsTitle|heroChip|ctaProjects|badge\w+): .*\n', '', s, flags=re.M)
# Keep the English HTML fallback identical to its translation strings.
en = s.split('      en: {', 1)[1].split('      zh: {', 1)[0]
copy = {k: json.loads(v) for k,v in re.findall(r'^        (\w+): (".*?")', en, re.M)}
s = re.sub(r'(<([\w]+)\b[^>]*data-i18n="([^"]+)"[^>]*>).*?(</\2>)', lambda m: m[1]+html.escape(copy[m[3]])+m[4], s, flags=re.S)
s = s.replace('target="_blank">', 'target="_blank" rel="noopener noreferrer">')
print('*** Begin Patch\n*** Update File: index.html\n@@')
print('\n'.join('-'+line for line in old.splitlines()))
print('\n'.join('+'+line for line in s.splitlines()))
print('*** End Patch')
