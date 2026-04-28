import streamlit as st
import random as _r

def render_ui():
    st.set_page_config(
        page_title="🎰 Lucky Draw Casino",
        page_icon="🎰",
        layout="centered",
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Rajdhani:wght@400;600;700&display=swap');

        :root {
            --bg:           #0d0521;
            --felt:         #140a2e;
            --felt2:        #1a0e38;
            --neon-red:     #ff2d78;
            --neon-gold:    #3dffc0;
            --neon-green:   #3dffc0;
            --chip-red:     #7b2fbe;
            --chip-blue:    #2ecfaa;
            --chip-white:   #e0e8f0;
            --card-cream:   #f0e8f5;
            --gold:         #3dffc0;
            --gold-bright:  #3dffc0;
            --gold-dim:     #1a7a5c;
            --white:        #e8e0f5;
            --muted:        #6a5a8a;
            --muted2:       #9a8aba;
            --danger:       #ff2d78;
            --border:       rgba(61,255,192,0.18);
            --border-bright:rgba(61,255,192,0.55);
            --serif:        'Playfair Display', Georgia, serif;
            --sans:         'Rajdhani', sans-serif;
        }

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .main .block-container {
            background: var(--bg) !important;
            color: var(--white);
            font-family: var(--sans);
        }
        .main .block-container {
            max-width: 700px !important;
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
        }
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Keyframes ── */
        @keyframes neon-flicker {
            0%,19%,21%,23%,25%,54%,56%,100% { opacity:1; }
            20%,24%,55% { opacity:.4; }
        }
        @keyframes marquee-lights {
            0%,100% { opacity:1; } 50% { opacity:.3; }
        }
        @keyframes fadeUp   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @keyframes spin-in  { from{transform:rotate(-8deg) scale(.9);opacity:0} to{transform:rotate(0deg) scale(1);opacity:1} }
        @keyframes chip-bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
        @keyframes suit-drift {
            0%   { transform:translateY(0) rotate(0deg);   opacity:.07 }
            50%  { transform:translateY(-20px) rotate(10deg); opacity:.13 }
            100% { transform:translateY(0) rotate(0deg);   opacity:.07 }
        }
        @keyframes border-chase {
            0%   { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }
        @keyframes winner-glow {
            0%,100% { box-shadow: 0 0 20px rgba(61,255,192,.2), inset 0 0 30px rgba(61,255,192,.03); }
            50%      { box-shadow: 0 0 60px rgba(61,255,192,.5), inset 0 0 50px rgba(61,255,192,.07); }
        }

        /* ── Felt texture background ── */
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse at 50% 0%, rgba(61,255,192,.06) 0%, transparent 55%),
                radial-gradient(ellipse at 0% 100%, rgba(123,47,190,.08) 0%, transparent 45%),
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 2px,
                    rgba(255,255,255,.008) 2px,
                    rgba(255,255,255,.008) 4px
                ),
                var(--bg) !important;
        }

        /* ── Floating card suits ── */
        .casino-suits {
            position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
        }
        .suit {
            position: absolute;
            font-size: 3rem;
            animation: suit-drift linear infinite;
        }

        /* ── Marquee light border at very top ── */
        .marquee-bar {
            position: fixed; top: 0; left: 0; right: 0; height: 4px; z-index: 100;
            background: linear-gradient(90deg,
                #7b2fbe, var(--neon-gold), #3dffc0,
                #7b2fbe, var(--neon-gold), #3dffc0);
            background-size: 200% 100%;
            animation: border-chase 2s linear infinite;
        }

        /* ── Header ── */
        .casino-header {
            text-align: center;
            margin-bottom: 0.5rem;
            animation: fadeUp .5s ease;
            position: relative; z-index: 1;
            padding: 1.5rem 0 0.5rem;
        }
        .casino-sign {
            display: inline-block;
            font-family: var(--serif);
            font-size: clamp(2.8rem, 9vw, 5rem);
            font-weight: 900;
            color: var(--neon-gold);
            text-shadow:
                0 0 10px rgba(61,255,192,.9),
                0 0 30px rgba(61,255,192,.5),
                0 0 70px rgba(61,255,192,.25);
            letter-spacing: .06em;
            text-transform: uppercase;
            animation: neon-flicker 6s ease-in-out infinite;
            line-height: 1;
        }
        .casino-subtitle {
            font-family: var(--sans);
            font-size: .78rem;
            letter-spacing: .5em;
            text-transform: uppercase;
            color: var(--muted2);
            margin-top: .5rem;
        }
        .casino-suits-row {
            font-size: 1.2rem;
            margin: .5rem 0;
            letter-spacing: .5rem;
            opacity: .6;
        }

        /* ── Divider ── */
        .casino-divider {
            display: flex; align-items: center; gap: .8rem;
            margin: 0.8rem 0 1.6rem;
            color: var(--gold-dim); font-size: .7rem;
        }
        .casino-divider::before,
        .casino-divider::after {
            content:'';
            flex: 1; height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
        }

        /* ── Chip stats bar ── */
        .stats-bar {
            display: grid; grid-template-columns: repeat(3,1fr);
            gap: .8rem; margin: 0 0 1.5rem;
            animation: fadeUp .4s ease .1s both;
        }
        .stat-chip {
            background: var(--felt2);
            border: 2px solid var(--border-bright);
            border-radius: 50px;
            padding: .8rem .5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .stat-chip::before {
            content: '';
            position: absolute; inset: 0;
            border-radius: 50px;
            background: repeating-linear-gradient(
                0deg, transparent, transparent 6px,
                rgba(255,255,255,.025) 6px, rgba(255,255,255,.025) 7px
            );
        }
        .stat-chip::after {
            content: '';
            position: absolute; top: 4px; left: 4px; right: 4px; bottom: 4px;
            border-radius: 50px;
            border: 1.5px dashed rgba(212,160,23,.25);
            pointer-events: none;
        }
        .stat-chip .val {
            font-family: var(--serif);
            font-size: 2.1rem; font-weight: 700;
            color: var(--neon-gold);
            line-height: 1;
            text-shadow: 0 0 14px rgba(255,215,0,.4);
            position: relative; z-index:1;
        }
        .stat-chip .lbl {
            font-family: var(--sans);
            font-size: .62rem; letter-spacing: .22em;
            text-transform: uppercase; color: var(--muted);
            margin-top: .2rem; position: relative; z-index:1;
        }

        /* ── Stage (table felt) ── */
        .casino-stage {
            background:
                radial-gradient(ellipse at 50% 50%, #261452 0%, #140a2e 65%);
            border: 2px solid var(--gold);
            border-radius: 28px;
            padding: 2.5rem 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
            min-height: 180px;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            position: relative; overflow: hidden;
            box-shadow:
                0 0 0 6px rgba(212,160,23,.08),
                0 0 0 8px rgba(212,160,23,.15),
                inset 0 2px 40px rgba(0,0,0,.4);
            animation: fadeUp .5s ease .2s both;
        }
        .casino-stage::before {
            content: '';
            position: absolute; inset: 6px;
            border-radius: 22px;
            border: 1px solid rgba(212,160,23,.2);
            pointer-events: none;
        }
        .casino-stage::after {
            content: '';
            position: absolute; inset: 0;
            background: repeating-linear-gradient(
                45deg, transparent, transparent 3px,
                rgba(255,255,255,.012) 3px, rgba(255,255,255,.012) 6px
            );
            border-radius: 28px;
            pointer-events: none;
        }
        .stage-tab {
            position: absolute; top: -1px; left: 50%; transform: translateX(-50%);
            background: var(--gold);
            color: #0d0521;
            font-family: var(--sans); font-size: .6rem;
            font-weight: 700; letter-spacing: .3em;
            text-transform: uppercase;
            padding: .22rem 1.2rem;
            border-radius: 0 0 8px 8px;
        }
        .stage-idle {
            font-family: var(--serif);
            font-size: 1.3rem; font-style: italic;
            color: var(--muted); position: relative; z-index: 1;
        }

        /* ── Upload ── */
        [data-testid="stFileUploader"] {
            background: var(--felt2) !important;
            border: 1.5px dashed var(--gold-dim) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            transition: border-color .3s, box-shadow .3s;
            animation: fadeUp .45s ease .15s both;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 0 20px rgba(212,160,23,.12) !important;
        }
        [data-testid="stFileUploader"] label {
            font-family: var(--sans) !important;
            font-size: .8rem !important;
            color: var(--muted2) !important;
            letter-spacing: .1em !important;
        }
        [data-testid="stFileUploader"] section { border: none !important; background: transparent !important; }

        /* ── Buttons ── */
        .stButton > button {
            width: 100%;
            font-family: var(--sans) !important;
            font-weight: 700 !important;
            letter-spacing: .18em !important;
            text-transform: uppercase !important;
            border-radius: 12px !important;
            transition: all .22s ease !important;
            animation: fadeUp .5s ease .3s both;
        }
        div[data-testid="column"]:first-child .stButton > button {
            background: linear-gradient(135deg, #1a0a3e 0%, #4a1a8a 30%, #7b2fbe 55%, #4a1a8a 80%, #1a0a3e 100%) !important;
            color: #3dffc0 !important;
            border: none !important;
            font-size: 1rem !important;
            padding: 1rem 1.5rem !important;
            box-shadow: 0 4px 24px rgba(123,47,190,.4), inset 0 1px 0 rgba(255,255,255,.15) !important;
            text-shadow: 0 1px 3px rgba(0,0,0,.5) !important;
        }
        div[data-testid="column"]:first-child .stButton > button:hover:not(:disabled) {
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: 0 8px 36px rgba(123,47,190,.55) !important;
        }
        div[data-testid="column"]:first-child .stButton > button:active:not(:disabled) {
            transform: translateY(1px) scale(.99) !important;
        }
        div[data-testid="column"]:first-child .stButton > button:disabled {
            opacity: .3 !important; cursor: not-allowed !important;
        }
        div[data-testid="column"]:last-child .stButton > button {
            background: transparent !important;
            color: var(--muted) !important;
            border: 1.5px solid rgba(255,255,255,.1) !important;
            font-size: .78rem !important; padding: 1rem .9rem !important;
        }
        div[data-testid="column"]:last-child .stButton > button:hover {
            color: var(--neon-gold) !important;
            border-color: rgba(255,215,0,.3) !important;
            background: rgba(255,215,0,.04) !important;
        }

        /* ── Section labels ── */
        .section-label {
            font-family: var(--sans);
            font-size: .65rem; letter-spacing: .3em;
            text-transform: uppercase; color: var(--muted);
            margin-bottom: .6rem; margin-top: 1.4rem;
            display: flex; align-items: center; gap: .6rem;
        }
        .section-label::after {
            content:''; flex:1; height:1px;
            background: linear-gradient(90deg, var(--gold-dim), transparent);
        }

        /* ── Alerts ── */
        .stAlert {
            border-radius: 10px !important;
            font-family: var(--sans) !important;
            font-size: .85rem !important;
            animation: fadeUp .3s ease;
        }

        /* ── Winners Hall ── */
        .winners-section {
            background:
                radial-gradient(ellipse at 50% 0%, rgba(61,255,192,.06) 0%, transparent 60%),
                var(--felt2);
            border: 1.5px solid var(--border-bright);
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: .5rem;
            animation: fadeUp .4s ease;
            box-shadow: inset 0 2px 20px rgba(0,0,0,.3);
        }
        .winners-header {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 1.25rem;
            padding-bottom: .75rem;
            border-bottom: 1px solid rgba(212,160,23,.15);
        }
        .winners-title {
            font-family: var(--serif);
            font-size: .95rem; font-weight: 700;
            letter-spacing: .08em; color: var(--gold-bright);
            text-shadow: 0 0 10px rgba(255,215,0,.3);
        }
        .winners-count-badge {
            font-family: var(--sans);
            font-size: .72rem; font-weight: 700;
            background: rgba(123,47,190,.2);
            color: #b88aff;
            padding: .2rem .7rem;
            border-radius: 20px;
            border: 1px solid rgba(123,47,190,.4);
            letter-spacing: .1em;
        }
        .winner-row {
            display: flex; align-items: center; gap: 1rem;
            padding: .65rem 0;
            border-bottom: 1px solid rgba(255,255,255,.04);
            animation: fadeUp .3s ease;
        }
        .winner-row:last-child { border-bottom: none; }
        .chip-num {
            width: 36px; height: 36px; flex-shrink: 0;
            border-radius: 50%;
            background: var(--chip-red);
            border: 2px solid rgba(255,255,255,.25);
            box-shadow: 0 2px 8px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.2);
            display: flex; align-items: center; justify-content: center;
            font-family: var(--sans); font-size: .75rem;
            font-weight: 700; color: #fff;
            position: relative;
            animation: chip-bob 2s ease-in-out infinite;
        }
        .chip-num::after {
            content: '';
            position: absolute; inset: 4px;
            border-radius: 50%;
            border: 1px dashed rgba(255,255,255,.35);
        }
        .winner-name-text {
            font-family: var(--serif);
            font-size: 1.1rem; color: var(--white);
            letter-spacing: .02em;
        }
        .winner-suit {
            margin-left: auto;
            opacity: .3; font-size: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    suits_data = [
        ("♠", "#0d0d1a", 8, 12, 5.5, 7),
        ("♥", "#1a0d0d", 22, 35, 4.5, 9),
        ("♦", "#1a1a0d", 68, 60, 6, 8),
        ("♣", "#0d1a0d", 85, 20, 5, 10),
        ("♠", "#0d0d1a", 45, 75, 7, 6),
        ("♥", "#1a0d0d", 5, 55, 4, 11),
        ("♦", "#1a1a0d", 92, 45, 5.5, 7),
        ("♣", "#0d1a0d", 55, 8, 6.5, 9),
    ]
    suits_html = '<div class="casino-suits">'
    for s, _col, left, top, dur, delay in suits_data:
        suits_html += (
            f'<div class="suit" style="left:{left}%;top:{top}%;'
            f'animation-duration:{dur}s;animation-delay:-{delay}s;">{s}</div>'
        )
    suits_html += '</div>'

    st.markdown(
        f"""
        <div class="marquee-bar"></div>
        {suits_html}
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="casino-header">
            <div class="casino-sign">Lucky Draw</div>
            <div class="casino-suits-row">♠ &nbsp; ♥ &nbsp; ♦ &nbsp; ♣</div>
            <div class="casino-subtitle">High Stakes Participant Selector</div>
        </div>
        <div class="casino-divider">✦ &nbsp; CASINO ROYALE &nbsp; ✦</div>
        """,
        unsafe_allow_html=True,
    )

    total     = len(st.session_state.get("names", [])) + len(st.session_state.get("winners", []))
    remaining = len(st.session_state.get("names", []))
    picked    = len(st.session_state.get("winners", []))

    st.markdown(
        f"""
        <div class="stats-bar">
            <div class="stat-chip">
                <div class="val">{remaining}</div>
                <div class="lbl">In the Pool</div>
            </div>
            <div class="stat-chip">
                <div class="val">{picked}</div>
                <div class="lbl">Winners</div>
            </div>
            <div class="stat-chip">
                <div class="val">{total}</div>
                <div class="lbl">Total Players</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    idle_msg = "Place your bets…" if st.session_state.get("names") else "Awaiting players…"
    st.markdown(
        f"""
        <div class="casino-stage">
            <div class="stage-tab">♠ Draw Stage ♠</div>
            <div class="stage-idle">{idle_msg}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">♦ Upload Participants</div>', unsafe_allow_html=True)
    file = st.file_uploader(
        'Excel file — column must be named **Name**',
        type=["xlsx"],
        label_visibility="visible",
    )

    st.markdown('<div class="section-label">♣ Actions</div>', unsafe_allow_html=True)
    col_pick, col_reset = st.columns([4, 1])
    with col_pick:
        pick_btn = st.button("🎰  Spin the Wheel", use_container_width=True)
    with col_reset:
        reset_btn = st.button("↺ Reset", use_container_width=True)

    winners = st.session_state.get("winners", [])
    suit_cycle = ["♠", "♥", "♦", "♣"]
    if winners:
        rows = ""
        for i, w in enumerate(reversed(winners)):
            num  = len(winners) - i
            suit = suit_cycle[(num - 1) % 4]
            rows += (
                f'<div class="winner-row">'
                f'<div class="chip-num">{num}</div>'
                f'<div class="winner-name-text">{w}</div>'
                f'<div class="winner-suit">{suit}</div>'
                f'</div>'
            )
        st.markdown(
            f"""
            <div class="winners-section">
                <div class="winners-header">
                    <span class="winners-title">♥ Hall of Winners ♥</span>
                    <span class="winners-count-badge">{len(winners)} drawn</span>
                </div>
                {rows}
            </div>
            """,
            unsafe_allow_html=True,
        )

    return file, pick_btn, reset_btn
