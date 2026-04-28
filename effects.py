import streamlit as st
import time
import json

def countdown():
    pool = st.session_state.get("names", [])
    import random as _rand
    import logic as _logic

    if pool:
        pre_winner = _rand.choice(pool)
        st.session_state["current_winner"] = pre_winner

        import sys
        _app = sys.modules.get("__main__")
        _orig = getattr(_app, "pick_winner", _logic.pick_winner)

        def _patched(names, winners):
            setattr(_app, "pick_winner", _orig)
            n = list(names)
            w = list(winners)
            if pre_winner in n:
                n.remove(pre_winner)
                w.append(pre_winner)
                return pre_winner, n, w
            return _orig(names, winners)

        if _app:
            setattr(_app, "pick_winner", _patched)
    else:
        pre_winner = None
        st.session_state["current_winner"] = None

    pre_winner_json = json.dumps(pre_winner if pre_winner else "")
    pool_json = json.dumps(pool[:40])

    overlay = st.empty()

    for num, label in [("5", "GET READY"), ("4", "GET READY"), ("3", "PLACE YOUR BETS"), ("2", "PLACE YOUR BETS"), ("1", "NO MORE BETS")]:
        overlay.markdown(
            f"""
            <div id="ld-overlay">
                <div class="ld-bg-felt"></div>
                <div class="ld-lights-top"></div>
                <div class="ld-lights-bot"></div>
                <div class="ld-stage">
                    <div class="ld-ring ld-ring1"></div>
                    <div class="ld-ring ld-ring2"></div>
                    <div class="ld-suits-ring" id="ld-suits"></div>
                    <div class="ld-label">{label}</div>
                    <div class="ld-num">{num}</div>
                    <div class="ld-suits-row">♠ &nbsp; ♥ &nbsp; ♦ &nbsp; ♣</div>
                </div>
            </div>

            <style>
            #ld-overlay {{
                position: fixed !important;
                inset: 0 !important;
                z-index: 2147483647 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                animation: ld-fadein .2s ease;
                overflow: hidden;
            }}
            .ld-bg-felt {{
                position: absolute; inset: 0;
                background:
                    radial-gradient(ellipse at 50% 50%, #261452 0%, #0d0521 70%);
            }}
            .ld-bg-felt::after {{
                content:'';
                position: absolute; inset: 0;
                background: repeating-linear-gradient(
                    45deg, transparent, transparent 4px,
                    rgba(255,255,255,.018) 4px, rgba(255,255,255,.018) 8px
                );
            }}
            .ld-lights-top, .ld-lights-bot {{
                position: absolute; left: 0; right: 0; height: 8px;
                display: flex; z-index: 2;
            }}
            .ld-lights-top {{ top: 0; }}
            .ld-lights-bot {{ bottom: 0; }}
            @keyframes ld-fadein     {{ from{{opacity:0}} to{{opacity:1}} }}
            @keyframes ld-ring-spin  {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}
            @keyframes ld-ring-rspin {{ from{{transform:rotate(0deg)}} to{{transform:rotate(-360deg)}} }}
            @keyframes ld-bounce {{
                0%{{transform:scale(2.8);opacity:0}}
                38%{{transform:scale(.82)}}
                62%{{transform:scale(1.2)}}
                80%{{transform:scale(.96)}}
                100%{{transform:scale(1);opacity:1}}
            }}
            @keyframes ld-neon-flicker {{
                0%,18%,20%,24%,54%,56%,100% {{ opacity:1; text-shadow:0 0 30px rgba(61,255,192,.9),0 0 80px rgba(61,255,192,.4); }}
                19%,23%,55% {{ opacity:.5; text-shadow:none; }}
            }}
            @keyframes ld-bulb-blink {{
                0%,49%{{background:#3dffc0;box-shadow:0 0 10px #3dffc0,0 0 20px rgba(61,255,192,.5);}}
                50%,100%{{background:#0a2a1e;box-shadow:none;}}
            }}
            @keyframes ld-suits-spin {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}

            .ld-stage {{
                position: relative; z-index: 3;
                width: 380px; height: 380px;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
            }}
            .ld-ring {{
                position: absolute;
                border-radius: 50%;
                border: 2px solid transparent;
            }}
            .ld-ring1 {{
                width: 300px; height: 300px;
                border-top-color: #3dffc0;
                border-right-color: rgba(61,255,192,.4);
                box-shadow: 0 0 16px rgba(61,255,192,.2);
                animation: ld-ring-spin 1.4s linear infinite;
            }}
            .ld-ring2 {{
                width: 350px; height: 350px;
                border-top-color: rgba(61,255,192,.35);
                border-left-color: rgba(61,255,192,.2);
                animation: ld-ring-rspin 2s linear infinite;
            }}
            .ld-suits-ring {{
                position: absolute;
                width: 260px; height: 260px;
                border-radius: 50%;
                animation: ld-suits-spin 8s linear infinite;
                z-index: 1;
            }}
            .ld-label {{
                font-family: 'Rajdhani', sans-serif;
                font-size: .7rem; font-weight: 700;
                letter-spacing: .5em;
                text-transform: uppercase;
                color: rgba(61,255,192,.6);
                margin-bottom: .3rem;
                position: relative; z-index: 4;
            }}
            .ld-num {{
                font-family: 'Playfair Display', Georgia, serif;
                font-size: 11rem; font-weight: 900;
                color: #3dffc0; line-height: 1;
                position: relative; z-index: 4;
                animation: ld-bounce .5s cubic-bezier(.175,.885,.32,1.275) both,
                           ld-neon-flicker 3s ease-in-out infinite .6s;
            }}
            .ld-suits-row {{
                font-size: 1.1rem; letter-spacing: .6rem;
                color: rgba(61,255,192,.4);
                margin-top: .3rem; position: relative; z-index: 4;
            }}
            </style>

            <script>
            (function() {{
                var lightContainers = document.querySelectorAll('.ld-lights-top, .ld-lights-bot');
                lightContainers.forEach(function(bar) {{
                    var w = window.innerWidth;
                    var count = Math.floor(w / 28);
                    for (var i = 0; i < count; i++) {{
                        var b = document.createElement('div');
                        b.style.cssText = 'width:20px;height:8px;border-radius:0 0 4px 4px;margin:0 4px;';
                        var del = (i % 3) * .3;
                        b.style.animation = 'ld-bulb-blink .6s ' + del + 's ease-in-out infinite';
                        b.style.background = '#3dffc0';
                        b.style.boxShadow = '0 0 10px #3dffc0,0 0 20px rgba(61,255,192,.5)';
                        bar.appendChild(b);
                    }}
                }});

                var suits = ['♠','♥','♦','♣'];
                var ring = document.getElementById('ld-suits');
                if (ring) {{
                    for (var i = 0; i < 8; i++) {{
                        var s = document.createElement('div');
                        var angle = (i / 8) * 360;
                        var rad = angle * Math.PI / 180;
                        var r = 130;
                        s.textContent = suits[i % 4];
                        s.style.cssText = 'position:absolute;font-size:1.1rem;opacity:.4;color:#3dffc0;';
                        s.style.left = (50 + r * Math.cos(rad) / 2.6 - 10) + '%';
                        s.style.top  = (50 + r * Math.sin(rad) / 2.6 - 12) + '%';
                        ring.appendChild(s);
                    }}
                }}
            }})();
            </script>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.8)

    import random as _rand
    start_spin = time.time()
    spin_duration = 3.5
    
    while time.time() - start_spin < spin_duration:
        display_name = _rand.choice(pool) if pool else "✦"
        
        # We use a slightly simplified version of the overlay for the spinning loop
        # to ensure it's responsive.
        overlay.markdown(
            f"""
            <div id="ld-overlay">
                <div class="ld-bg-felt"></div>
                <div class="ld-lights-top" id="lights-top"></div>
                <div class="ld-lights-bot" id="lights-bot"></div>
                <div class="ld-spin-stage">
                    <div class="ld-ring ld-ring1"></div>
                    <div class="ld-ring ld-ring2"></div>
                    <div class="ld-ring ld-ring3"></div>
                    <div class="ld-suits-ring" id="ld-suits-spin"></div>
                    <div class="ld-spin-label" id="ld-spin-label">SPINNING…</div>
                    <div class="ld-reel-window">
                        <div class="ld-reel-top-fade"></div>
                        <div class="ld-spin-name" id="ld-spin-name">{display_name}</div>
                        <div class="ld-reel-bot-fade"></div>
                    </div>
                    <div class="ld-badge" id="ld-badge">🏆 &nbsp; WINNER &nbsp; 🏆</div>
                    <div class="ld-winner-suits" id="ld-wsuits" style="opacity:0">♠ &nbsp; ♥ &nbsp; ♦ &nbsp; ♣</div>
                </div>
            </div>

            <style>
            #ld-overlay {{
                position: fixed !important;
                inset: 0 !important;
                z-index: 2147483646 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                overflow: hidden;
            }}
            .ld-bg-felt {{
                position: absolute; inset: 0;
                background: radial-gradient(ellipse at 50% 50%, #261452 0%, #0d0521 70%);
            }}
            .ld-lights-top, .ld-lights-bot {{
                position: absolute; left: 0; right: 0; height: 8px;
                display: flex; z-index: 2; justify-content: center;
                background: repeating-linear-gradient(90deg, #3dffc0 0px, #3dffc0 20px, transparent 20px, transparent 28px);
                animation: ld-bulb-blink .6s infinite;
            }}
            .ld-lights-top {{ top: 0; }}
            .ld-lights-bot {{ bottom: 0; }}

            @keyframes ld-ring-spin   {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}
            @keyframes ld-ring-rspin  {{ from{{transform:rotate(0deg)}} to{{transform:rotate(-360deg)}} }}
            @keyframes ld-suits-spin  {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}
            @keyframes ld-slot-scroll {{
                0%   {{transform:translateY(-10px);opacity:.8}}
                50%  {{transform:translateY(0);   opacity:1}}
                100% {{transform:translateY(10px);opacity:.8}}
            }}
            @keyframes ld-bulb-blink {{
                0%, 49% {{ opacity: 1; }}
                50%, 100% {{ opacity: 0.3; }}
            }}

            .ld-spin-stage {{
                position: relative; z-index: 3;
                width: 480px; height: 480px;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
            }}
            .ld-ring {{
                position: absolute; border-radius: 50%;
                border: 2px solid transparent;
            }}
            .ld-ring1 {{
                width: 390px; height: 390px;
                border-top-color: #3dffc0;
                border-right-color: rgba(61,255,192,.4);
                box-shadow: 0 0 20px rgba(61,255,192,.2);
                animation: ld-ring-spin 1.3s linear infinite;
            }}
            .ld-ring2 {{
                width: 440px; height: 440px;
                border-top-color: rgba(61,255,192,.35);
                border-left-color: rgba(61,255,192,.2);
                animation: ld-ring-rspin 1.9s linear infinite;
            }}
            .ld-ring3 {{
                width: 340px; height: 340px;
                border-right-color: rgba(123,47,190,.35);
                border-bottom-color: rgba(123,47,190,.2);
                animation: ld-ring-spin .85s linear infinite;
            }}
            .ld-suits-ring {{
                position: absolute;
                width: 300px; height: 300px;
                border-radius: 50%;
                animation: ld-suits-spin 10s linear infinite;
                z-index: 1;
                display: flex; align-items: center; justify-content: center;
            }}
            .ld-suits-ring::before {{
                content: '♠ ♥ ♦ ♣ ♠ ♥ ♦ ♣';
                color: #3dffc0; opacity: .3; letter-spacing: 1.5rem;
                font-size: 1.2rem;
            }}
            .ld-spin-label {{
                font-family: 'Rajdhani', sans-serif;
                font-size: .75rem; font-weight: 700;
                letter-spacing: .5em; text-transform: uppercase;
                color: rgba(61,255,192,.6);
                margin-bottom: .8rem;
                position: relative; z-index: 4;
            }}
            .ld-reel-window {{
                position: relative; z-index: 4;
                width: 100%; max-width: 420px;
                display: flex; flex-direction: column; align-items: center;
                overflow: hidden; padding: .5rem 0;
            }}
            .ld-spin-name {{
                font-family: 'Playfair Display', Georgia, serif;
                font-size: clamp(2.4rem, 6vw, 4rem);
                font-weight: 700; color: #3dffc0;
                line-height: 1.1; text-align: center;
                max-width: 400px; word-break: break-word;
                padding: 0 1.5rem;
                animation: ld-slot-scroll 0.08s linear infinite;
            }}
            .ld-badge {{
                font-family: 'Rajdhani', sans-serif;
                font-size: .85rem; font-weight: 700;
                letter-spacing: .4em; text-transform: uppercase;
                background: linear-gradient(135deg, #1a0a3e, #4a1a8a, #7b2fbe, #4a1a8a, #1a0a3e);
                color: #fff;
                padding: .4rem 1.8rem; border-radius: 4px;
                margin-top: 1.2rem;
                opacity: 0.3; position: relative; z-index: 4;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.08) # ~12 FPS for smooth spinning appearance


    winner = pre_winner or st.session_state.get("current_winner", None)

    if winner:
        overlay.markdown(
            f"""
            <div id="ld-winner-screen">
                <div class="ld-ws-bg"></div>
                <div class="ld-ws-lights-top"></div>
                <div class="ld-ws-lights-bot"></div>
                <div class="ld-ws-content">
                    <div class="ld-ws-suits-top">♠ &nbsp; ♥ &nbsp; ♦ &nbsp; ♣</div>
                    <div class="ld-ws-crown">👑</div>
                    <div class="ld-ws-label">WINNER</div>
                    <div class="ld-ws-divider"></div>
                    <div class="ld-ws-name" id="ld-ws-name">{winner}</div>
                    <div class="ld-ws-divider"></div>
                    <div class="ld-ws-suits-bot">♣ &nbsp; ♦ &nbsp; ♥ &nbsp; ♠</div>
                    <div class="ld-ws-tap">tap anywhere to continue</div>
                </div>
            </div>

            <canvas id="ld-ws-confetti" style="position:fixed;inset:0;pointer-events:none;z-index:2147483647;width:100vw;height:100vh;"></canvas>

            <style>
            #ld-winner-screen {{
                position: fixed !important;
                inset: 0 !important;
                z-index: 2147483646 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                cursor: pointer;
                animation: ldws-fadein .4s ease;
            }}
            @keyframes ldws-fadein  {{ from{{opacity:0}} to{{opacity:1}} }}
            @keyframes ldws-fadeout {{ from{{opacity:1}} to{{opacity:0}} }}
            @keyframes ldws-crown-drop {{
                0%  {{transform:translateY(-60px) scale(1.6);opacity:0}}
                55% {{transform:translateY(6px) scale(.92)}}
                75% {{transform:translateY(-4px) scale(1.04)}}
                100%{{transform:translateY(0) scale(1);opacity:1}}
            }}
            @keyframes ldws-name-slam {{
                0%  {{transform:scale(.3) rotate(-4deg);opacity:0;letter-spacing:-.1em}}
                55% {{transform:scale(1.12) rotate(1.5deg);letter-spacing:.06em}}
                75% {{transform:scale(.96) rotate(0deg)}}
                100%{{transform:scale(1) rotate(0deg);opacity:1;letter-spacing:.04em}}
            }}
            @keyframes ldws-label-rise {{
                0%  {{transform:translateY(30px);opacity:0}}
                100%{{transform:translateY(0);opacity:1}}
            }}
            @keyframes ldws-glow-pulse {{
                0%,100% {{text-shadow:0 0 30px rgba(61,255,192,.7),0 0 80px rgba(61,255,192,.3),0 0 160px rgba(61,255,192,.1)}}
                50%     {{text-shadow:0 0 80px rgba(61,255,192,1),0 0 160px rgba(61,255,192,.6),0 0 280px rgba(61,255,192,.25)}}
            }}
            @keyframes ldws-suits-fade {{
                0%  {{opacity:0;transform:translateY(10px)}}
                100%{{opacity:.55;transform:translateY(0)}}
            }}
            @keyframes ldws-tap-blink {{
                0%,100%{{opacity:.35}} 50%{{opacity:.8}}
            }}
            @keyframes ldws-bulb-blink {{
                0%,49%{{background:#3dffc0;box-shadow:0 0 10px #3dffc0,0 0 20px rgba(61,255,192,.5);}}
                50%,100%{{background:#0a2a1e;box-shadow:none;}}
            }}
            @keyframes ldws-divider-grow {{
                0%  {{width:0;opacity:0}}
                100%{{width:280px;opacity:1}}
            }}

            .ld-ws-bg {{
                position: absolute; inset: 0;
                background:
                    radial-gradient(ellipse at 50% 40%, rgba(61,255,192,.18) 0%, transparent 55%),
                    radial-gradient(ellipse at 50% 50%, #261452 0%, #08031a 70%);
            }}
            .ld-ws-bg::before {{
                content:'';
                position: absolute; inset: 0;
                background: repeating-linear-gradient(
                    45deg, transparent, transparent 4px,
                    rgba(255,255,255,.015) 4px, rgba(255,255,255,.015) 8px
                );
            }}
            .ld-ws-bg::after {{
                content:'';
                position: absolute; inset: 0;
                background: repeating-linear-gradient(
                    0deg, transparent, transparent 3px,
                    rgba(0,0,0,.06) 3px, rgba(0,0,0,0.06) 4px
                );
            }}
            .ld-ws-lights-top, .ld-ws-lights-bot {{
                position: absolute; left: 0; right: 0; height: 10px;
                display: flex; z-index: 2;
            }}
            .ld-ws-lights-top {{ top: 0; }}
            .ld-ws-lights-bot {{ bottom: 0; }}
            .ld-ws-content {{
                position: relative; z-index: 3;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                text-align: center; padding: 2rem;
                max-width: 700px; width: 100%;
            }}
            .ld-ws-crown {{
                font-size: 4.5rem; line-height: 1;
                margin-bottom: .5rem;
                filter: drop-shadow(0 0 20px rgba(61,255,192,.8));
                animation: ldws-crown-drop .7s cubic-bezier(.175,.885,.32,1.275) both;
            }}
            .ld-ws-label {{
                font-family: 'Rajdhani', sans-serif;
                font-size: clamp(.9rem,2.5vw,1.1rem);
                font-weight: 700;
                letter-spacing: .8em;
                text-transform: uppercase;
                color: rgba(61,255,192,.7);
                margin-bottom: .8rem;
                animation: ldws-label-rise .5s ease .3s both;
            }}
            .ld-ws-divider {{
                width: 280px; height: 1.5px;
                background: linear-gradient(90deg, transparent, #3dffc0, transparent);
                margin: .8rem auto;
                animation: ldws-divider-grow .6s ease .4s both;
            }}
            .ld-ws-name {{
                font-family: 'Playfair Display', Georgia, serif;
                font-size: clamp(3rem, 10vw, 7rem);
                font-weight: 900;
                color: #3dffc0;
                line-height: 1.05;
                word-break: break-word;
                padding: 0 1rem;
                animation: ldws-name-slam .75s cubic-bezier(.175,.885,.32,1.275) .15s both,
                           ldws-glow-pulse 2.5s ease-in-out 1s infinite;
            }}
            .ld-ws-suits-top, .ld-ws-suits-bot {{
                font-size: 1.4rem; letter-spacing: .9rem;
                color: #3dffc0;
                animation: ldws-suits-fade .5s ease .8s both;
            }}
            .ld-ws-suits-top {{ margin-bottom: .5rem; }}
            .ld-ws-suits-bot {{ margin-top: .5rem; }}
            .ld-ws-tap {{
                font-family: 'Rajdhani', sans-serif;
                font-size: .72rem; letter-spacing: .3em;
                text-transform: uppercase;
                color: rgba(61,255,192,.4);
                margin-top: 2rem;
                animation: ldws-tap-blink 1.6s ease-in-out 1.5s infinite;
            }}
            </style>

            <script>
            (function() {{
                var lightBars = document.querySelectorAll('.ld-ws-lights-top, .ld-ws-lights-bot');
                lightBars.forEach(function(bar) {{
                    var count = Math.floor(window.innerWidth / 30);
                    for (var i = 0; i < count; i++) {{
                        var b = document.createElement('div');
                        var del = (i % 4) * .22;
                        b.style.cssText = 'flex-shrink:0;width:22px;height:10px;border-radius:0 0 5px 5px;margin:0 3px;background:#3dffc0;box-shadow:0 0 10px #3dffc0,0 0 22px rgba(61,255,192,.5);';
                        b.style.animation = 'ldws-bulb-blink .55s ' + del + 's ease-in-out infinite';
                        bar.appendChild(b);
                    }}
                }});

                var screen = document.getElementById('ld-winner-screen');
                if (screen) {{
                    screen.addEventListener('click', function() {{
                        screen.style.animation = 'ldws-fadeout .35s ease forwards';
                        setTimeout(function() {{ screen.remove(); }}, 350);
                    }});
                }}

                var canvas = document.getElementById('ld-ws-confetti');
                if (!canvas) return;
                var ctx = canvas.getContext('2d');
                canvas.width  = window.innerWidth;
                canvas.height = window.innerHeight;
                var palette = ['#3dffc0','#2ecfaa','#7b2fbe','#FFFFFF','#e8e0f5','#3dffc0','#b88aff','#1a7a5c'];
                var parts = [];
                for (var i = 0; i < 300; i++) {{
                    var isCard = i < 50;
                    parts.push({{
                        x: Math.random() * canvas.width,
                        y: -30 - Math.random() * 700,
                        w: isCard ? 16 : 6 + Math.random() * 11,
                        h: isCard ? 22 : 4 + Math.random() * 8,
                        r: Math.random() * Math.PI * 2,
                        rv: -.15 + Math.random() * .3,
                        vx: -7 + Math.random() * 14,
                        vy: 1.5 + Math.random() * 6,
                        color: palette[Math.floor(Math.random() * palette.length)],
                        shape: isCard ? 'card' : (['rect','circle','ribbon'][Math.floor(Math.random()*3)]),
                        suit: ['♠','♥','♦','♣'][Math.floor(Math.random()*4)],
                        alpha: 1
                    }});
                }}
                var raf;
                function draw() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    var live = false;
                    for (var i = 0; i < parts.length; i++) {{
                        var p = parts[i];
                        if (p.y > canvas.height + 30) continue;
                        live = true;
                        p.x += p.vx; p.y += p.vy; p.vy += .08; p.r += p.rv;
                        if (p.y > canvas.height * .6) p.alpha = Math.max(0, p.alpha - .011);
                        ctx.save();
                        ctx.globalAlpha = p.alpha;
                        ctx.translate(p.x, p.y); ctx.rotate(p.r);
                        if (p.shape === 'card') {{
                            ctx.fillStyle = '#f5f0e8';
                            ctx.strokeStyle = 'rgba(0,0,0,.12)'; ctx.lineWidth = .5;
                            ctx.beginPath(); ctx.roundRect(-p.w/2,-p.h/2,p.w,p.h,2);
                            ctx.fill(); ctx.stroke();
                            ctx.fillStyle = (p.suit==='♥'||p.suit==='♦') ? '#7b2fbe' : '#1a0a2e';
                            ctx.font = 'bold ' + (p.w*.72) + 'px serif';
                            ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                            ctx.fillText(p.suit, 0, 0);
                        }} else if (p.shape === 'rect') {{
                            ctx.fillStyle = p.color;
                            ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);
                        }} else if (p.shape === 'circle') {{
                            ctx.fillStyle = p.color;
                            ctx.beginPath(); ctx.arc(0,0,p.w/2,0,Math.PI*2); ctx.fill();
                        }} else {{
                            ctx.fillStyle = p.color;
                            ctx.fillRect(-p.w/2,-p.h/4,p.w,p.h/4);
                            ctx.fillRect(-p.w/4,-p.h/2,p.w/4,p.h);
                        }}
                        ctx.restore();
                    }}
                    if (live) raf = requestAnimationFrame(draw);
                }}
                cancelAnimationFrame(raf);
                draw();
            }})();
            </script>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(5.5)

    overlay.empty()
