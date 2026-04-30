#!/usr/bin/env python3
"""HTE Tracking Bot v2 — human-readable output"""

import os, json, re, sys, urllib.request
from datetime import datetime


MASTER_CSS     = """.logo-img{width:44px;height:44px;object-fit:contain}*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--yellow:#FFC72C;--page-bg:#f2f0ea}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--page-bg);color:#0d0d0d;min-height:100vh;font-size:13px}
header{padding:0 48px;display:flex;align-items:center;justify-content:space-between;height:68px;position:sticky;top:0;z-index:200;background:rgba(5,20,40,0.6);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,0.08)}
.logo{display:flex;align-items:center;gap:14px;text-decoration:none}
.logo-mark{width:38px;height:38px;background:var(--yellow);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#0d2040}
.logo-text{font-weight:700;font-size:15px;color:#fff}.logo-sub{font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:.1em;text-transform:uppercase}
.live-badge{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(8px);border-radius:24px;padding:6px 16px;font-size:11px;color:rgba(255,255,255,0.6)}
.live-dot{width:7px;height:7px;border-radius:50%;background:#4caf50;box-shadow:0 0 0 3px rgba(76,175,80,0.3);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 3px rgba(76,175,80,0.3)}50%{box-shadow:0 0 0 7px rgba(76,175,80,0.1)}}
.hero-section{position:relative;overflow:hidden}
.hero-bg{position:absolute;inset:0;background-image:url('https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=1600&q=80&auto=format&fit=crop');background-size:cover;background-position:center 40%;filter:brightness(0.45) saturate(0.8)}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(5,20,40,0.6) 0%,rgba(5,20,40,0.3) 50%,rgba(5,20,40,0.85) 100%)}
.hero{position:relative;z-index:2;padding:48px 48px 52px}
.hero-label{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--yellow);margin-bottom:14px;font-weight:500}
.hero-title{font-size:clamp(32px,5vw,58px);font-weight:800;color:#fff;line-height:1.05;letter-spacing:-.02em;margin-bottom:8px}
.hero-title .y{color:var(--yellow)}
.hero-desc{font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:40px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;max-width:720px;border-radius:14px;overflow:hidden;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(16px)}
.stat-card{background:rgba(5,20,40,0.55);padding:20px 24px}
.stat-val{font-size:40px;font-weight:800;line-height:1;margin-bottom:5px;color:#fff}
.stat-val.yl{color:var(--yellow)}
.stat-lbl{font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:.1em;text-transform:uppercase;font-weight:500}
.timeline-wrap{display:grid;grid-template-columns:200px 1fr;max-width:1100px;margin:0 auto;padding:60px 48px 80px}
.month-nav{position:sticky;top:88px;align-self:start;padding-right:28px;padding-top:4px}
.month-nav-title{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#999;margin-bottom:16px;font-weight:600}
.month-item{display:flex;align-items:center;gap:10px;padding:7px 0;text-decoration:none;transition:opacity .15s}
.month-item:hover{opacity:.6}
.month-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.month-name{font-size:13px;font-weight:600;color:#0d0d0d}
.month-count{font-size:10px;color:#aaa;margin-left:auto;font-weight:500}
.nav-line{width:1px;height:18px;background:#ddd;margin:1px 0 1px 4px}
.month-section{margin-bottom:52px;scroll-margin-top:100px}
.month-header{display:flex;align-items:center;padding:20px 24px;border-radius:14px 14px 0 0;position:relative;overflow:hidden}
.month-header::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(-45deg,transparent,transparent 12px,rgba(255,255,255,0.06) 12px,rgba(255,255,255,0.06) 13px)}
.mh-icon{font-size:26px;margin-right:14px;position:relative;z-index:1}
.mh-info{position:relative;z-index:1;flex:1}
.mh-big{font-size:20px;font-weight:800;line-height:1;margin-bottom:3px}
.mh-small{font-size:11px;opacity:.65}
.mh-pill{position:relative;z-index:1;font-size:10px;font-weight:600;padding:5px 12px;border-radius:20px;background:rgba(255,255,255,0.22);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.cards{display:flex;flex-direction:column;gap:10px;padding-top:10px}
.card{background:#fff;border-radius:14px;padding:18px 22px;border:1.5px solid transparent;transition:transform .15s,box-shadow .15s,border-color .15s;animation:rise .45s ease both}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,0.07)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.card-header{display:flex;align-items:flex-start;gap:14px;margin-bottom:12px}
.num-c{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;margin-top:2px}
.card-headline{flex:1}
.card-status-row{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.card-date-big{font-size:16px;font-weight:800;line-height:1}
.pill{display:inline-block;font-size:10px;font-weight:600;padding:4px 11px;border-radius:20px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}
.card-dest{font-size:11px;color:#888;margin-top:3px}
.eq-list{display:flex;flex-direction:column;gap:6px;border-top:1px solid #f0ede6;padding-top:12px}
.eq-item{display:flex;align-items:center;gap:8px;padding:6px 10px;background:#faf9f6;border-radius:8px}
.eq-icon{font-size:18px;flex-shrink:0}


.eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{margin-left:auto;font-size:12px;font-weight:700;padding:2px 10px;border-radius:12px;background:#eee;color:#444}
.card-note{font-size:11px;color:#e07000;margin-top:8px;font-weight:500;padding:6px 10px;background:#fff8ee;border-radius:8px;border-left:3px solid #e07000}
.card-tech{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tech-pill{font-size:10px;color:#aaa;background:#f5f3ee;padding:2px 8px;border-radius:10px}

/* COLOR THEMES */
.t-1 .month-header{background:linear-gradient(130deg,#1a4d2e,#2d8a4a);color:#fff}
.t-1 .card{border-color:#c5eed5}.t-1 .card:hover{border-color:#4daa6d}
.t-1 .num-c{background:#d4f0df;color:#1a4d2e}.t-1 .card-date-big{color:#1a4d2e}.t-1 .pill{background:#d4f0df;color:#1a4d2e}.t-1 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#d4f0df;color:#1a4d2e}
.t-2 .month-header{background:linear-gradient(130deg,#0d4848,#1a8080);color:#fff}
.t-2 .card{border-color:#bde8e8}.t-2 .card:hover{border-color:#30aaaa}
.t-2 .num-c{background:#c8ecec;color:#0d4848}.t-2 .card-date-big{color:#0d4848}.t-2 .pill{background:#c8ecec;color:#0d4848}.t-2 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#c8ecec;color:#0d4848}
.t-3 .month-header{background:linear-gradient(130deg,#0d2468,#1a4fa8);color:#fff}
.t-3 .card{border-color:#c4d8f8}.t-3 .card:hover{border-color:#4080e0}
.t-3 .num-c{background:#d2e4fa;color:#0d2468}.t-3 .card-date-big{color:#0d2468}.t-3 .pill{background:#d2e4fa;color:#0d2468}.t-3 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#d2e4fa;color:#0d2468}
.t-4 .month-header{background:linear-gradient(130deg,#221468,#4c38c8);color:#fff}
.t-4 .card{border-color:#d8d2f8}.t-4 .card:hover{border-color:#7060e0}
.t-4 .num-c{background:#e2dcfa;color:#221468}.t-4 .card-date-big{color:#221468}.t-4 .pill{background:#e2dcfa;color:#221468}.t-4 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#e2dcfa;color:#221468}
.t-5 .month-header{background:linear-gradient(130deg,#441468,#8a38b8);color:#fff}
.t-5 .card{border-color:#e8d2f8}.t-5 .card:hover{border-color:#aa60d4}
.t-5 .num-c{background:#eedcfa;color:#441468}.t-5 .card-date-big{color:#441468}.t-5 .pill{background:#eedcfa;color:#441468}.t-5 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#eedcfa;color:#441468}
.t-6 .month-header{background:linear-gradient(130deg,#641438,#c43868);color:#fff}
.t-6 .card{border-color:#f8c4d8}.t-6 .card:hover{border-color:#e06090}
.t-6 .num-c{background:#fad2e4;color:#641438}.t-6 .card-date-big{color:#641438}.t-6 .pill{background:#fad2e4;color:#641438}.t-6 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#fad2e4;color:#641438}
.t-7 .month-header{background:linear-gradient(130deg,#522800,#b05800);color:#fff}
.t-7 .card{border-color:#f8debb}.t-7 .card:hover{border-color:#e08838}
.t-7 .num-c{background:#fae8ca;color:#522800}.t-7 .card-date-big{color:#522800}.t-7 .pill{background:#fae8ca;color:#522800}.t-7 .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#fae8ca;color:#522800}
.t-sail .month-header{background:linear-gradient(130deg,#603800,#c47000);color:#fff}
.t-sail .card{border-color:#ffe4b8}.t-sail .card:hover{border-color:#f0a030}
.t-sail .num-c{background:#feeece;color:#603800}.t-sail .card-date-big{color:#603800}.t-sail .pill{background:#feeece;color:#603800}.t-sail .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#feeece;color:#603800}
.t-pend .month-header{background:linear-gradient(130deg,#282828,#545454);color:#fff}
.t-pend .card{border-color:#dedad2}.t-pend .card:hover{border-color:#aaa}
.t-pend .num-c{background:#eae6de;color:#444}.t-pend .card-date-big{color:#555}.t-pend .pill{background:#eae6de;color:#555}.t-pend .eq-label{flex:1;display:flex;flex-direction:column;gap:1px}.eq-label .eq-type{font-size:10px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.08em}.eq-label .eq-model{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.1}.eq-qty{background:#eae6de;color:#555}
footer{background:#0d2040;padding:28px 48px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
.ft-brand{font-size:13px;font-weight:600;color:rgba(255,255,255,0.35)}
.ft-brand span{color:var(--yellow)}
.ft-links{display:flex;gap:24px}
.ft-links a{font-size:11px;color:rgba(255,255,255,0.35);text-decoration:none;transition:color .15s;font-weight:500}
.ft-links a:hover{color:var(--yellow)}
@media(max-width:800px){header,.hero,footer{padding-left:20px;padding-right:20px}.timeline-wrap{grid-template-columns:1fr;padding:28px 20px 60px}.month-nav{display:none}.stats{grid-template-columns:repeat(2,1fr)}.card-status-row{flex-direction:column;align-items:flex-start}}"""
LOGO_SRC       = "data:image/png;base64,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"
CONTAINER_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><rect x="2" y="7" width="20" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="7" y1="7" x2="7" y2="18" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="7" x2="12" y2="18" stroke="currentColor" stroke-width="1.5"/><line x1="17" y1="7" x2="17" y2="18" stroke="currentColor" stroke-width="1.5"/><rect x="6" y="5" width="12" height="2.5" rx="0.5" fill="currentColor"/><rect x="4" y="18" width="3" height="2.5" rx="0.5" fill="currentColor"/><rect x="17" y="18" width="3" height="2.5" rx="0.5" fill="currentColor"/></svg>'

BOT_TOKEN   = "8327743942:AAGlZjo1bVwt3FvwF00zLYGiwIvLubY3S5s"
ADMIN_ID    = 1715716748
UPDATER_URL = "https://tracking.sdlg.online/updater.php"
UPDATER_KEY = "hte_tracking_2026_Xk9mP3qR"
API         = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ── Equipment dictionary ─────────────────────────────────────────────────────
MODELS = {
    'G9190H':  ('Автогрейдер',        'SDLG G9190H',  '🟡'),
    'G9165F':  ('Автогрейдер',        'SDLG G9165F',  '🟡'),
    'G9220H':  ('Автогрейдер',        'SDLG G9220H',  '🟡'),
    'E6255F':  ('Экскаватор',         'SDLG E6255F',  '⛏️'),
    'E6350H':  ('Экскаватор',         'SDLG E6350H',  '⛏️'),
    'E690F':   ('Экскаватор',         'SDLG E690F',   '⛏️'),
    'E7210H':  ('Экскаватор',         'SDLG E7210H',  '⛏️'),
    'L958F':   ('Фронтальный погрузчик','SDLG L958F', '🚜'),
    'L956FH':  ('Фронтальный погрузчик','SDLG L956FH','🚜'),
    'L956H':   ('Фронтальный погрузчик','SDLG L956H', '🚜'),
    'L933F':   ('Фронтальный погрузчик','SDLG L933F', '🚜'),
    'B877F':   ('Каток дорожный',     'SDLG B877F',   '🔵'),
    'SR900H':  ('Каток вибрационный', 'SDLG SR900H',  '🔵'),
    'SD26':    ('Бульдозер',          'SDLG SD26',    '🔨'),
    'D18H':    ('Бульдозер',          'SDLG D18H',    '🔨'),
}

SKIP_TOKENS = {'SKD','TDC','UST','ETD','ETA','BUS','SDLG','SRL','DOCS',
               'SHIPPING','SPARE','PARTS','FRET','CHINA','UST'}

def parse_equipment(raw):
    """
    Parse raw title string into list of dicts:
    [{'icon','type','model','qty','label'}, ...]
    """
    text = raw.upper()
    results = []
    found   = set()

    # Pattern: NxMODEL or MODEL+NxMODEL
    for m in re.finditer(r'(\d+)\s*[Xx]\s*([A-Z]\d+[A-Z0-9]*)', text):
        qty, model = m.group(1), m.group(2)
        if model in found: continue
        found.add(model)
        info = MODELS.get(model)
        if info:
            tp, mdl, icon = info
            results.append({'icon':icon,'type':tp,'model':mdl,'qty':int(qty)})
        else:
            results.append({'icon':'📦','type':'Техника','model':f'SDLG {model}','qty':int(qty)})

    # Standalone models (qty=1)
    for m in re.finditer(r'\b([A-Z]\d+[A-Z0-9]+)\b', text):
        model = m.group(1)
        if model in found or model in SKIP_TOKENS: continue
        info = MODELS.get(model)
        if not info: continue
        found.add(model)
        tp, mdl, icon = info
        results.append({'icon':icon,'type':tp,'model':mdl,'qty':1})

    # Buckets
    bm = re.search(r'(\d*)\s*[Xx]?\s*BUCKET', text)
    if bm or 'КОВШ' in text:
        qty = int(bm.group(1)) if bm and bm.group(1) else 1
        results.append({'icon':'🪣','type':'Ковш','model':'Навесное оборудование','qty':qty})

    # Forks
    fm = re.search(r'(\d*)\s*[Xx]?\s*FORK', text)
    if fm or 'ВИЛЫ' in text or 'ВИЛА' in text:
        qty = int(fm.group(1)) if fm and fm.group(1) else 1
        results.append({'icon':'🍴','type':'Вилы','model':'Навесное оборудование','qty':qty})

    # Yutong bus
    if 'YUTONG' in text and 'SPARE' not in text and 'PARTS' not in text:
        results.append({'icon':'🚌','type':'Автобус','model':'Yutong','qty':1})

    # Spare parts
    if 'SPARE' in text or 'ЗАП' in text:
        brand = 'SDLG' if 'SDLG' in text else ('Yutong' if 'YUTONG' in text else '')
        results.append({'icon':'🔧','type':'Запасные части','model':brand,'qty':0})

    # Robots AllyNav
    if 'ALLYNAV' in text or 'ALLYN' in text:
        results.append({'icon':'🤖','type':'Роботы','model':'AllyNav','qty':0})

    # Lonking forklift
    if 'LONKING' in text:
        results.append({'icon':'🏗️','type':'Погрузчик','model':'Lonking','qty':0})

    # Shandong Disam
    if 'DISAM' in text or 'SHANDONG' in text:
        results.append({'icon':'📦','type':'Техника','model':'Shandong Disam','qty':0})

    # Buldozer SD26 (text match)
    if 'BULDOZER' in text or 'БУЛЬДОЗЕР' in text:
        if not any(r['type']=='Бульдозер' for r in results):
            mdl_m = re.search(r'SD\d+', text)
            mdl = mdl_m.group(0) if mdl_m else 'SDLG'
            results.append({'icon':'🔨','type':'Бульдозер','model':f'SDLG {mdl}','qty':1})

    return results if results else [{'icon':'📦','type':'Груз','model':raw[:60],'qty':0}]


def build_card_items_html(equipment):
    """Build the equipment items list inside a card."""
    html = '<div class="eq-list">'
    for eq in equipment:
        qty_str = f'<span class="eq-qty">{eq["qty"]} ед.</span>' if eq['qty'] > 0 else ''
        model_str = f'<span class="eq-model">{eq["model"]}</span>' if eq['model'] else ''
        html += f'''<div class="eq-item">
  <span class="eq-icon">{eq["icon"]}</span>
  <span class="eq-type">{eq["type"]}</span>
  {model_str}
  {qty_str}
</div>'''
    html += '</div>'
    return html


# ── Parser ───────────────────────────────────────────────────────────────────

def parse_update_date(text):
    m = re.search(r'Обновление\s+(\d{1,2}/\d{1,2}/\d{4})', text)
    return m.group(1) if m else datetime.now().strftime("%d/%m/%Y")

def parse_shipments(text):
    shipments = []
    blocks = re.split(r'\n(?=\d+\))', text)
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r'^\d+\)', block): continue
        s = {}
        num_m = re.match(r'^(\d+)\)', block)
        s['num'] = num_m.group(1) if num_m else '?'
        frets = re.findall(r'FRET\d+', block)
        s['fret'] = ' · '.join(frets) if frets else ''
        bls = re.findall(r'\b\d{9,}\b', block)
        bls += re.findall(r'[A-Z]{2,}\d{6,}-\d{6,}', block)
        s['bl'] = bls[0] if bls else ''
        ems = re.findall(r'EM\d{4}-\d+', block)
        s['em'] = ' + '.join(ems) if ems else ''
        containers = re.findall(r'SZYH\w+', block)
        rys = re.findall(r'RYS\w+', block)
        s['containers'] = ' · '.join(containers + rys)
        eta_m = re.search(r'ETA\s+Constanta\s+(\d{1,2}/\d{1,2}/\d{4})', block)
        etd_m = re.search(r'(\d{1,2}[-–]\d{1,2}/\d{2}/\d{4})', block)
        if eta_m:
            s['eta'] = eta_m.group(1)
            try:
                days = (datetime.strptime(s['eta'],"%d/%m/%Y") - datetime.now()).days
                s['status'] = 'arriving' if days <= 7 else 'transit'
            except:
                s['status'] = 'transit'
        elif 'Выплываем' in block or 'ETD' in block:
            s['status'] = 'sailing'
            s['eta'] = etd_m.group(1) if etd_m else 'уточняется'
        else:
            s['status'] = 'pending'
            s['eta'] = ''
        notes = []
        if re.search(r'Ждем|Ждём', block) and 'документ' in block.lower():
            notes.append('Ожидаем коммерческие документы от SDLG')
        if 'будет обновление' in block.lower():
            notes.append('Дата погрузки уточняется')
        s['note'] = ' · '.join(notes)
        # Extract raw title for equipment parsing
        raw = block
        raw = re.sub(r'^\d+\)\s*', '', raw)
        raw = re.sub(r'SHIPPING\s+DOCS[-–\s]*', '', raw)
        raw = re.sub(r'SPARE\s+PARTS\s+', 'SPARE PARTS ', raw)
        raw = re.sub(r'EM\d{4}-\d+\s*[+]?\s*', '', raw)
        raw = re.sub(r'[/\s]*FRET\d+[,\s]*', ' ', raw)
        raw = re.sub(r'\b\d{9,}\b', '', raw)
        raw = re.sub(r'[A-Z]{2,}\d{6,}-\d{6,}', '', raw)
        raw = re.sub(r'SZYH\w+[,\s]*', '', raw)
        raw = re.sub(r'RYS\w+[,\s]*', '', raw)
        raw = re.sub(r'ETA\s+Constanta\s+\S+', '', raw)
        raw = re.sub(r'ETD\s+China\s+\S+', '', raw)
        raw = re.sub(r'Прибытие|Выплываем|Ждем.*|Ждём.*|будет обновление.*', '', raw, flags=re.I)
        raw = re.sub(r'\s{2,}', ' ', raw).strip(' \n\t-–/')
        s['raw_title'] = raw
        s['equipment'] = parse_equipment(raw)
        shipments.append(s)
    return shipments


# ── HTML Generator ───────────────────────────────────────────────────────────

THEMES = [
    ('t-1','#2d8a4a','linear-gradient(130deg,#1a4d2e,#2d8a4a)'),
    ('t-2','#1a8080','linear-gradient(130deg,#0d4848,#1a8080)'),
    ('t-3','#1a4fa8','linear-gradient(130deg,#0d2468,#1a4fa8)'),
    ('t-4','#4c38c8','linear-gradient(130deg,#221468,#4c38c8)'),
    ('t-5','#8a38b8','linear-gradient(130deg,#441468,#8a38b8)'),
    ('t-6','#c43868','linear-gradient(130deg,#641438,#c43868)'),
    ('t-7','#b05800','linear-gradient(130deg,#522800,#b05800)'),
]

# CSS defined as MASTER_CSS above
_UNUSED = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--yellow:#FFC72C;--page-bg:#f2f0ea}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--page-bg);color:#0d0d0d;min-height:100vh;font-size:13px}
header{padding:0 48px;display:flex;align-items:center;justify-content:space-between;height:68px;position:sticky;top:0;z-index:200;background:rgba(5,20,40,0.6);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,0.08)}
.logo{display:flex;align-items:center;gap:14px;text-decoration:none}
.logo-mark{width:38px;height:38px;background:var(--yellow);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#0d2040}
.logo-text{font-weight:700;font-size:15px;color:#fff}.logo-sub{font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:.1em;text-transform:uppercase}
.live-badge{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(8px);border-radius:24px;padding:6px 16px;font-size:11px;color:rgba(255,255,255,0.6)}
.live-dot{width:7px;height:7px;border-radius:50%;background:#4caf50;box-shadow:0 0 0 3px rgba(76,175,80,0.3);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 3px rgba(76,175,80,0.3)}50%{box-shadow:0 0 0 7px rgba(76,175,80,0.1)}}
.hero-section{position:relative;overflow:hidden}
.hero-bg{position:absolute;inset:0;background-image:url('https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=1600&q=80&auto=format&fit=crop');background-size:cover;background-position:center 40%;filter:brightness(0.45) saturate(0.8)}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(5,20,40,0.6) 0%,rgba(5,20,40,0.3) 50%,rgba(5,20,40,0.85) 100%)}
.hero{position:relative;z-index:2;padding:48px 48px 52px}
.hero-label{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--yellow);margin-bottom:14px;font-weight:500}
.hero-title{font-size:clamp(32px,5vw,58px);font-weight:800;color:#fff;line-height:1.05;letter-spacing:-.02em;margin-bottom:8px}
.hero-title .y{color:var(--yellow)}
.hero-desc{font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:40px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;max-width:720px;border-radius:14px;overflow:hidden;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(16px)}
.stat-card{background:rgba(5,20,40,0.55);padding:20px 24px}
.stat-val{font-size:40px;font-weight:800;line-height:1;margin-bottom:5px;color:#fff}
.stat-val.yl{color:var(--yellow)}
.stat-lbl{font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:.1em;text-transform:uppercase;font-weight:500}
.timeline-wrap{display:grid;grid-template-columns:200px 1fr;max-width:1100px;margin:0 auto;padding:60px 48px 80px}
.month-nav{position:sticky;top:88px;align-self:start;padding-right:28px;padding-top:4px}
.month-nav-title{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#999;margin-bottom:16px;font-weight:600}
.month-item{display:flex;align-items:center;gap:10px;padding:7px 0;text-decoration:none;transition:opacity .15s}
.month-item:hover{opacity:.6}
.month-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.month-name{font-size:13px;font-weight:600;color:#0d0d0d}
.month-count{font-size:10px;color:#aaa;margin-left:auto;font-weight:500}
.nav-line{width:1px;height:18px;background:#ddd;margin:1px 0 1px 4px}
.month-section{margin-bottom:52px;scroll-margin-top:100px}
.month-header{display:flex;align-items:center;padding:20px 24px;border-radius:14px 14px 0 0;position:relative;overflow:hidden}
.month-header::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(-45deg,transparent,transparent 12px,rgba(255,255,255,0.06) 12px,rgba(255,255,255,0.06) 13px)}
.mh-icon{font-size:26px;margin-right:14px;position:relative;z-index:1}
.mh-info{position:relative;z-index:1;flex:1}
.mh-big{font-size:20px;font-weight:800;line-height:1;margin-bottom:3px}
.mh-small{font-size:11px;opacity:.65}
.mh-pill{position:relative;z-index:1;font-size:10px;font-weight:600;padding:5px 12px;border-radius:20px;background:rgba(255,255,255,0.22);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.cards{display:flex;flex-direction:column;gap:10px;padding-top:10px}
.card{background:#fff;border-radius:14px;padding:18px 22px;border:1.5px solid transparent;transition:transform .15s,box-shadow .15s,border-color .15s;animation:rise .45s ease both}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,0.07)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.card-header{display:flex;align-items:flex-start;gap:14px;margin-bottom:12px}
.num-c{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;margin-top:2px}
.card-headline{flex:1}
.card-status-row{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.card-date-big{font-size:16px;font-weight:800;line-height:1}
.pill{display:inline-block;font-size:10px;font-weight:600;padding:4px 11px;border-radius:20px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}
.card-dest{font-size:11px;color:#888;margin-top:3px}
.eq-list{display:flex;flex-direction:column;gap:6px;border-top:1px solid #f0ede6;padding-top:12px}
.eq-item{display:flex;align-items:center;gap:8px;padding:6px 10px;background:#faf9f6;border-radius:8px}
.eq-icon{font-size:18px;flex-shrink:0}
.eq-type{font-size:13px;font-weight:600;color:#0d0d0d}
.eq-model{font-size:12px;color:#888;margin-left:2px}
.eq-qty{margin-left:auto;font-size:12px;font-weight:700;padding:2px 10px;border-radius:12px;background:#eee;color:#444}
.card-note{font-size:11px;color:#e07000;margin-top:8px;font-weight:500;padding:6px 10px;background:#fff8ee;border-radius:8px;border-left:3px solid #e07000}
.card-tech{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tech-pill{font-size:10px;color:#aaa;background:#f5f3ee;padding:2px 8px;border-radius:10px}

/* COLOR THEMES */
.t-1 .month-header{background:linear-gradient(130deg,#1a4d2e,#2d8a4a);color:#fff}
.t-1 .card{border-color:#c5eed5}.t-1 .card:hover{border-color:#4daa6d}
.t-1 .num-c{background:#d4f0df;color:#1a4d2e}.t-1 .card-date-big{color:#1a4d2e}.t-1 .pill{background:#d4f0df;color:#1a4d2e}.t-1 .eq-qty{background:#d4f0df;color:#1a4d2e}
.t-2 .month-header{background:linear-gradient(130deg,#0d4848,#1a8080);color:#fff}
.t-2 .card{border-color:#bde8e8}.t-2 .card:hover{border-color:#30aaaa}
.t-2 .num-c{background:#c8ecec;color:#0d4848}.t-2 .card-date-big{color:#0d4848}.t-2 .pill{background:#c8ecec;color:#0d4848}.t-2 .eq-qty{background:#c8ecec;color:#0d4848}
.t-3 .month-header{background:linear-gradient(130deg,#0d2468,#1a4fa8);color:#fff}
.t-3 .card{border-color:#c4d8f8}.t-3 .card:hover{border-color:#4080e0}
.t-3 .num-c{background:#d2e4fa;color:#0d2468}.t-3 .card-date-big{color:#0d2468}.t-3 .pill{background:#d2e4fa;color:#0d2468}.t-3 .eq-qty{background:#d2e4fa;color:#0d2468}
.t-4 .month-header{background:linear-gradient(130deg,#221468,#4c38c8);color:#fff}
.t-4 .card{border-color:#d8d2f8}.t-4 .card:hover{border-color:#7060e0}
.t-4 .num-c{background:#e2dcfa;color:#221468}.t-4 .card-date-big{color:#221468}.t-4 .pill{background:#e2dcfa;color:#221468}.t-4 .eq-qty{background:#e2dcfa;color:#221468}
.t-5 .month-header{background:linear-gradient(130deg,#441468,#8a38b8);color:#fff}
.t-5 .card{border-color:#e8d2f8}.t-5 .card:hover{border-color:#aa60d4}
.t-5 .num-c{background:#eedcfa;color:#441468}.t-5 .card-date-big{color:#441468}.t-5 .pill{background:#eedcfa;color:#441468}.t-5 .eq-qty{background:#eedcfa;color:#441468}
.t-6 .month-header{background:linear-gradient(130deg,#641438,#c43868);color:#fff}
.t-6 .card{border-color:#f8c4d8}.t-6 .card:hover{border-color:#e06090}
.t-6 .num-c{background:#fad2e4;color:#641438}.t-6 .card-date-big{color:#641438}.t-6 .pill{background:#fad2e4;color:#641438}.t-6 .eq-qty{background:#fad2e4;color:#641438}
.t-7 .month-header{background:linear-gradient(130deg,#522800,#b05800);color:#fff}
.t-7 .card{border-color:#f8debb}.t-7 .card:hover{border-color:#e08838}
.t-7 .num-c{background:#fae8ca;color:#522800}.t-7 .card-date-big{color:#522800}.t-7 .pill{background:#fae8ca;color:#522800}.t-7 .eq-qty{background:#fae8ca;color:#522800}
.t-sail .month-header{background:linear-gradient(130deg,#603800,#c47000);color:#fff}
.t-sail .card{border-color:#ffe4b8}.t-sail .card:hover{border-color:#f0a030}
.t-sail .num-c{background:#feeece;color:#603800}.t-sail .card-date-big{color:#603800}.t-sail .pill{background:#feeece;color:#603800}.t-sail .eq-qty{background:#feeece;color:#603800}
.t-pend .month-header{background:linear-gradient(130deg,#282828,#545454);color:#fff}
.t-pend .card{border-color:#dedad2}.t-pend .card:hover{border-color:#aaa}
.t-pend .num-c{background:#eae6de;color:#444}.t-pend .card-date-big{color:#555}.t-pend .pill{background:#eae6de;color:#555}.t-pend .eq-qty{background:#eae6de;color:#555}
footer{background:#0d2040;padding:28px 48px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
.ft-brand{font-size:13px;font-weight:600;color:rgba(255,255,255,0.35)}
.ft-brand span{color:var(--yellow)}
.ft-links{display:flex;gap:24px}
.ft-links a{font-size:11px;color:rgba(255,255,255,0.35);text-decoration:none;transition:color .15s;font-weight:500}
.ft-links a:hover{color:var(--yellow)}
@media(max-width:800px){header,.hero,footer{padding-left:20px;padding-right:20px}.timeline-wrap{grid-template-columns:1fr;padding:28px 20px 60px}.month-nav{display:none}.stats{grid-template-columns:repeat(2,1fr)}.card-status-row{flex-direction:column;align-items:flex-start}}"""

MONTHS_RU = ['','января','февраля','марта','апреля','мая','июня',
             'июля','августа','сентября','октября','ноября','декабря']
MONTHS_LONG = ['','Январь','Февраль','Март','Апрель','Май','Июнь',
               'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']

def date_nice(d):
    try:
        dt = datetime.strptime(d, "%d/%m/%Y")
        return f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}"
    except:
        return d

def parse_date_dt(d):
    try: return datetime.strptime(d, "%d/%m/%Y")
    except: return datetime.max

def generate_html(shipments, update_date):
    # Group
    groups, sail, pend = {}, [], []
    for s in shipments:
        if s['status'] in ('arriving','transit'):
            groups.setdefault(s['eta'], []).append(s)
        elif s['status'] == 'sailing':
            sail.append(s)
        else:
            pend.append(s)

    sorted_dates = sorted(groups.keys(), key=parse_date_dt)

    total    = len(shipments)
    arriving = sum(1 for s in shipments if s['status']=='arriving')
    transit  = sum(1 for s in shipments if s['status'] in ('transit','sailing'))
    pending  = sum(1 for s in shipments if s['status']=='pending')

    all_dts = [parse_date_dt(d) for d in sorted_dates if parse_date_dt(d)!=datetime.max]
    if all_dts:
        period = f"{MONTHS_LONG[all_dts[0].month]} — {MONTHS_LONG[all_dts[-1].month]} {all_dts[-1].year}"
    else:
        period = str(datetime.now().year)

    nav_html = ''
    sections_html = ''
    ti = 0

    STATUS_ICON = {'arriving':'🟢','transit':'🚢','sailing':'⚓','pending':'⏳'}
    STATUS_PILL = {'arriving':'Прибывает','transit':'В пути','sailing':'Отплывает','pending':'Нет даты'}

    def make_card(s, delay):
        eq_html = ''
        for eq in s['equipment']:
            qty_str = f'<span class="eq-qty">{eq["qty"]} ед.</span>' if eq.get('qty',0)>0 else ''
            model_str = f'<span class="eq-model">{eq["model"]}</span>' if eq.get('model') else ''
            eq_html += f'<div class="eq-item"><span class="eq-icon">{eq["icon"]}</span><span class="eq-type">{eq["type"]}</span>{model_str}{qty_str}</div>'

        note_html = f'<div class="card-note">⚠️ {s["note"]}</div>' if s['note'] else ''

        # Tech pills (FRET, EM) — small, unobtrusive
        tech = []
        if s['fret']: tech.append(s['fret'])
        if s['em']:   tech.append(s['em'])
        tech_html = ''
        if tech:
            pills = ''.join(f'<span class="tech-pill">{t}</span>' for t in tech)
            tech_html = f'<div class="card-tech">{pills}</div>'

        date_display = date_nice(s['eta']) if s['eta'] else '—'
        pill_text    = STATUS_PILL.get(s['status'],'В пути')
        dest = 'Порт Констанца, Румыния' if s['status'] in ('arriving','transit') else ''
        dest_html = f'<div class="card-dest">📍 {dest}</div>' if dest else ''

        return f'''<div class="card" style="animation-delay:{delay:.2f}s">
  <div class="card-header">
    <div class="num-c">{s['num']}</div>
    <div class="card-headline">
      <div class="card-status-row">
        <div class="card-date-big">{date_display}</div>
        <span class="pill">{pill_text}</span>
      </div>
      {dest_html}
    </div>
  </div>
  <div class="eq-list">{eq_html}</div>
  {note_html}
  {tech_html}
</div>'''

    for date_key in sorted_dates:
        grp = groups[date_key]
        tc, dot_c, _ = THEMES[ti % len(THEMES)]
        ti += 1
        gid   = f'g{ti}'
        icon  = STATUS_ICON.get(grp[0]['status'],'🚢')
        pill  = STATUS_PILL.get(grp[0]['status'],'В пути')
        dn    = date_nice(date_key)
        cnt   = len(grp)

        nav_html += f'<a class="month-item" href="#{gid}"><div class="month-dot" style="background:{dot_c}"></div><div class="month-name">{dn}</div><div class="month-count">{cnt}</div></a><div class="nav-line"></div>\n'

        cards = ''.join(make_card(s, 0.05*(i+1)) for i,s in enumerate(grp))
        sections_html += f'''<div class="month-section {tc}" id="{gid}">
  <div class="month-header">
    <div class="mh-icon">{icon}</div>
    <div class="mh-info"><div class="mh-big">{dn}</div><div class="mh-small">Прибытие в Констанцу &nbsp;·&nbsp; {cnt} отправлений</div></div>
    <div class="mh-pill">{pill}</div>
  </div>
  <div class="cards">{cards}</div>
</div>\n'''

    if sail:
        nav_html += f'<a class="month-item" href="#g-sail"><div class="month-dot" style="background:#c47000"></div><div class="month-name">Отплывают</div><div class="month-count">{len(sail)}</div></a><div class="nav-line"></div>\n'
        cards = ''.join(make_card(s, 0.05*(i+1)) for i,s in enumerate(sail))
        sections_html += f'''<div class="month-section t-sail" id="g-sail">
  <div class="month-header"><div class="mh-icon">⚓</div><div class="mh-info"><div class="mh-big">Отплывают из Китая</div><div class="mh-small">{len(sail)} отправлений</div></div><div class="mh-pill">Отплывает</div></div>
  <div class="cards">{cards}</div>
</div>\n'''

    if pend:
        nav_html += f'<a class="month-item" href="#g-pend"><div class="month-dot" style="background:#888"></div><div class="month-name">Ожидают</div><div class="month-count">{len(pend)}</div></a>\n'
        cards = ''.join(make_card(s, 0.05*(i+1)) for i,s in enumerate(pend))
        sections_html += f'''<div class="month-section t-pend" id="g-pend">
  <div class="month-header"><div class="mh-icon">⏳</div><div class="mh-info"><div class="mh-big">Ожидают обновления</div><div class="mh-small">Дата уточняется &nbsp;·&nbsp; {len(pend)} отправлений</div></div><div class="mh-pill">Нет даты</div></div>
  <div class="cards">{cards}</div>
</div>\n'''

    css = MASTER_CSS
    logo = LOGO_SRC
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Tracking — Hydro Tech Express</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header>
  <a class="logo" href="https://sdlg.online" target="_blank">
    <div class="logo-mark">HTE</div>
    <div><div class="logo-text">Hydro Tech Express</div><div class="logo-sub">Официальный дилер SDLG</div></div>
  </a>
  <div class="live-badge"><div class="live-dot"></div>Обновлено {update_date}</div>
</header>
<div class="hero-section">
  <div class="hero-bg"></div><div class="hero-overlay"></div>
  <div class="hero">
    <div class="hero-label">Container Tracking · Hydro Tech Express SRL</div>
    <div class="hero-title">Мониторинг<br><span class="y">контейнеров</span></div>
    <div class="hero-desc">Китай → Констанца → Молдова &nbsp;·&nbsp; {period}</div>
    <div class="stats">
      <div class="stat-card"><div class="stat-val">{total}</div><div class="stat-lbl">Отправлений</div></div>
      <div class="stat-card"><div class="stat-val yl">{arriving}</div><div class="stat-lbl">Прибывают скоро</div></div>
      <div class="stat-card"><div class="stat-val">{transit}</div><div class="stat-lbl">В пути</div></div>
      <div class="stat-card"><div class="stat-val">{pending}</div><div class="stat-lbl">Ожидают данных</div></div>
    </div>
  </div>
</div>
<div class="timeline-wrap">
  <nav class="month-nav">
    <div class="month-nav-title">По датам прибытия</div>
    {nav_html}
  </nav>
  <div class="sections">{sections_html}</div>
</div>
<footer>
  <div class="ft-brand"><span>Hydro Tech Express SRL</span> — Официальный дилер SDLG в Молдове</div>
  <div class="ft-links">
    <a href="https://sdlg.online" target="_blank">sdlg.online</a>
    <a href="tel:+37360726262">+373 60 72 62 62</a>
  </div>
</footer>
</body></html>"""

# ── Upload ────────────────────────────────────────────────────────────────────

def upload_html(html):
    body = json.dumps({"html": html}).encode()
    req  = urllib.request.Request(UPDATER_URL, data=body,
           headers={"X-Secret":UPDATER_KEY,"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

# ── Telegram ──────────────────────────────────────────────────────────────────

def tg(method, **kwargs):
    body = json.dumps(kwargs).encode()
    req  = urllib.request.Request(f"{API}/{method}", data=body,
           headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def send(chat_id, text):
    tg("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML")

def typing(chat_id):
    tg("sendChatAction", chat_id=chat_id, action="typing")

def handle(msg):
    chat_id = msg['chat']['id']
    text    = msg.get('text','') or ''
    if chat_id != ADMIN_ID:
        send(chat_id,"⛔ Доступ запрещён."); return
    if text.startswith('/start') or text.startswith('/help'):
        send(chat_id,
            "👋 <b>HTE Tracking Bot</b>\n\n"
            "Перешли сюда сообщение от логиста — я обновлю "
            "<a href='https://tracking.sdlg.online'>tracking.sdlg.online</a> автоматически.\n\n"
            "Просто скопируй и вставь текст целиком.")
        return
    if len(text) < 50:
        send(chat_id,"⚠️ Текст слишком короткий. Отправь полное обновление от логиста."); return
    typing(chat_id)
    try:
        update_date = parse_update_date(text)
        shipments   = parse_shipments(text)
        if not shipments:
            send(chat_id,"❌ Не удалось распарсить данные."); return
        typing(chat_id)
        html   = generate_html(shipments, update_date)
        result = upload_html(html)
        arriving = sum(1 for s in shipments if s['status']=='arriving')
        transit  = sum(1 for s in shipments if s['status'] in ('transit','sailing'))
        pending  = sum(1 for s in shipments if s['status']=='pending')
        send(chat_id,
            f"✅ <b>tracking.sdlg.online обновлён!</b>\n\n"
            f"📦 Всего: <b>{len(shipments)}</b> отправлений\n"
            f"🟢 Прибывают скоро: <b>{arriving}</b>\n"
            f"🚢 В пути: <b>{transit}</b>\n"
            f"⏳ Ожидают данных: <b>{pending}</b>\n\n"
            f"🕐 {result.get('time','')}\n"
            f"🔗 <a href='https://tracking.sdlg.online'>tracking.sdlg.online</a>")
    except Exception as e:
        send(chat_id, f"❌ Ошибка: {e}")

if __name__ == '__main__':
    print("🤖 HTE Tracking Bot v2 — polling mode")
    offset = 0
    while True:
        try:
            resp = tg("getUpdates", offset=offset, timeout=30)
            for upd in resp.get('result',[]):
                offset = upd['update_id'] + 1
                if 'message' in upd:
                    handle(upd['message'])
        except Exception as e:
            print(f"Error: {e}")
            import time; time.sleep(3)
