import base64
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ----- Page setup -----
st.set_page_config(page_title="💘 A Question For You", page_icon="💘", layout="centered")

# ----- Custom names -----
HER_NAME = "Onigiri"
ME_NICKNAME = "Maki Pie"

# ----- Load songs as base64 (fixes "missing on deploy") -----
APP_DIR = Path(__file__).resolve().parent
SONG1_PATH = APP_DIR / "song1.mp3"
SONG2_PATH = APP_DIR / "song2.mp3"

SONG1_B64 = ""
SONG2_B64 = ""
AUDIO_ERROR = ""

try:
    SONG1_B64 = base64.b64encode(SONG1_PATH.read_bytes()).decode("utf-8")
except FileNotFoundError:
    AUDIO_ERROR += f"song1 file not found at: {SONG1_PATH}\n"
except Exception as e:
    AUDIO_ERROR += f"Could not load song1 file: {e}\n"

try:
    SONG2_B64 = base64.b64encode(SONG2_PATH.read_bytes()).decode("utf-8")
except FileNotFoundError:
    AUDIO_ERROR += f"song2 file not found at: {SONG2_PATH}\n"
except Exception as e:
    AUDIO_ERROR += f"Could not load song2 file: {e}\n"

AUDIO_ERROR = AUDIO_ERROR.strip()

# ----- CSS (Theme: pink > blue > yellow) -----
CSS = """
<style>
:root{
  --pink:#ffc0c0;   /* dominant */
  --blue:#a8d8f0;   /* secondary */
  --yellow:#fbf9a3; /* least */
  --card:#ffffffcc;
  --ink:#2b2b2b;
  --shadow: rgba(0,0,0,0.12);
}

/* Background */
.stApp{
  background:
    radial-gradient(circle at 18% 18%, rgba(255, 192, 192, 0.95), rgba(255, 192, 192, 0.0) 55%),
    radial-gradient(circle at 85% 30%, rgba(168, 216, 240, 0.85), rgba(168, 216, 240, 0.0) 55%),
    radial-gradient(circle at 25% 88%, rgba(251, 249, 163, 0.55), rgba(251, 249, 163, 0.0) 60%),
    linear-gradient(160deg, var(--pink) 0%, var(--pink) 40%, var(--blue) 72%, var(--yellow) 100%);
  min-height: 100vh;
}

/* Card */
.card{
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.55);
  box-shadow: 0 12px 34px var(--shadow);
  border-radius: 22px;
  padding: 26px 22px;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 2;
}

/* Typography */
h1,h2,h3,p{ color: var(--ink) !important; }
.big{
  font-size: 1.25rem;
  line-height: 1.65;
}

/* Badge */
.badge{
  display:inline-block;
  padding: 7px 13px;
  border-radius: 999px;
  background: rgba(255,255,255,0.76);
  border: 1px solid rgba(255,255,255,0.55);
  font-weight: 800;
}

/* Header strip */
.title-strip{
  display:flex;
  align-items:center;
  justify-content:center;
  gap: 10px;
  margin-top: 6px;
  margin-bottom: 10px;
  font-size: 1.08rem;
  opacity: 0.95;
}

/* Pulse */
.pulse{
  display:inline-block;
  animation: pulse 1.25s ease-in-out infinite;
}
@keyframes pulse{
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}

/* Footer */
.footer{
  opacity: 0.85;
  font-size: 0.95rem;
}

/* Floating particles (in parent page DOM) */
.floaty{
  position: fixed;
  bottom: -60px;
  opacity: 0.92;
  pointer-events: none;
  z-index: 1;
  filter: drop-shadow(0 6px 10px rgba(0,0,0,0.12));
  animation-name: floatUp;
  animation-timing-function: linear;
  animation-iteration-count: 1;
  will-change: transform;
}
@keyframes floatUp{
  from { transform: translate3d(0,0,0) rotate(0deg); }
  to   { transform: translate3d(60px, -118vh, 0) rotate(22deg); }
}

/* Twinkles overlay */
.twinkle{
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events:none;
  background-image:
    radial-gradient(rgba(255,255,255,0.38) 1px, transparent 1px),
    radial-gradient(rgba(255,255,255,0.24) 1px, transparent 1px);
  background-size: 46px 46px, 72px 72px;
  background-position: 0 0, 18px 26px;
  animation: twinkleMove 9s linear infinite;
  opacity: 0.33;
}
@keyframes twinkleMove{
  from { transform: translateY(0); }
  to { transform: translateY(70px); }
}

/* Make Streamlit buttons feel more cute */
.stButton > button{
  border-radius: 14px !important;
  font-weight: 800 !important;
  box-shadow: 0 10px 22px rgba(0,0,0,0.10) !important;
}

/* =========================
   LOVE LETTER ENVELOPE STAGE
   ========================= */
.envelope-wrap{
  display:flex;
  justify-content:center;
  margin: 22px 0 10px;
}
.envelope{
  width:min(560px, 94vw);
  border-radius: 26px;
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(255,255,255,0.55);
  box-shadow: 0 14px 36px rgba(0,0,0,0.12);
  backdrop-filter: blur(10px);
  padding: 18px 18px 20px;
  cursor: pointer;
  position: relative;
  overflow:hidden;
  user-select:none;
  -webkit-tap-highlight-color: transparent;
  transform: translateZ(0);
}
.envelope:hover{
  box-shadow: 0 18px 44px rgba(0,0,0,0.14);
}
.envelope:active{
  transform: translateY(1px);
}

.env-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 10px;
  font-weight: 900;
}
.env-stamp{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: rgba(255,192,192,0.45);
  border: 1px solid rgba(255,255,255,0.65);
  box-shadow: 0 10px 22px rgba(0,0,0,0.10);
  font-size: 26px;
  transform: rotate(-6deg);
}
.env-title{
  font-size: 1.18rem;
  line-height: 1.2;
}
.env-sub{
  opacity: 0.82;
  font-weight: 700;
  margin-top: 5px;
  font-size: 0.98rem;
}

.env-body{
  margin-top: 14px;
  position: relative;
  border-radius: 22px;
  padding: 16px 14px 14px;
  background: rgba(255,255,255,0.60);
  border: 1px dashed rgba(43,43,43,0.18);
}

/* Fake “paper” inside envelope */
.env-paper{
  height: 126px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,255,255,0.72));
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 10px 26px rgba(0,0,0,0.08);
  transform: translateY(34px);
  position: relative;
  overflow:hidden;
}
.paper-line{
  height: 10px;
  border-radius: 999px;
  background: rgba(43,43,43,0.10);
  margin: 12px 16px;
}
.paper-line.short{ width: 62%; }
.paper-line.tiny{ width: 42%; }

/* Envelope flap (pseudo) */
.envelope::before{
  content:"";
  position:absolute;
  left: 0;
  right: 0;
  top: 118px; /* aligns with env-body top visually */
  height: 170px;
  background:
    linear-gradient(180deg, rgba(255,192,192,0.25), rgba(168,216,240,0.16)),
    radial-gradient(circle at 20% 20%, rgba(255,255,255,0.55), rgba(255,255,255,0.0) 60%);
  clip-path: polygon(0 0, 100% 0, 50% 70%);
  opacity: 0.85;
  transform-origin: 50% 0%;
  transform: rotateX(0deg);
  transition: transform 520ms ease;
  pointer-events:none;
}

/* Cute open CTA */
.env-cta{
  margin-top: 14px;
  display:flex;
  align-items:center;
  justify-content:center;
  gap: 10px;
  font-weight: 900;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(168,216,240,0.35);
  border: 1px solid rgba(255,255,255,0.65);
}

/* Opening animation state */
.envelope.opening{
  animation: envWiggle 520ms ease both;
}
@keyframes envWiggle{
  0%   { transform: translateY(0) rotate(0deg); }
  35%  { transform: translateY(-1px) rotate(-0.7deg); }
  70%  { transform: translateY(0) rotate(0.7deg); }
  100% { transform: translateY(0) rotate(0deg); }
}
.envelope.opening::before{
  transform: rotateX(70deg);
}

/* Paper slides up when opening */
.envelope.opening .env-paper{
  animation: paperUp 520ms ease both;
}
@keyframes paperUp{
  from { transform: translateY(34px); }
  to   { transform: translateY(4px); }
}

/* Little sparkle burst */
.envelope .sparkle{
  position:absolute;
  inset: 0;
  pointer-events:none;
  opacity: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(255,255,255,0.65) 1px, transparent 2px),
    radial-gradient(circle at 72% 38%, rgba(255,255,255,0.55) 1px, transparent 2px),
    radial-gradient(circle at 38% 70%, rgba(255,255,255,0.55) 1px, transparent 2px),
    radial-gradient(circle at 82% 78%, rgba(255,255,255,0.55) 1px, transparent 2px);
}
.envelope.opening .sparkle{
  animation: sparkle 520ms ease both;
}
@keyframes sparkle{
  0% { opacity: 0; transform: scale(0.98); }
  45%{ opacity: 0.55; }
  100%{ opacity: 0; transform: scale(1.02); }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----- State -----
if "stage" not in st.session_state:
    st.session_state.stage = "letter"  # start as a love letter
if "answered" not in st.session_state:
    st.session_state.answered = None

# ----- Handle query params from JS buttons -----
choice = st.query_params.get("choice")
if choice in ("yes", "maybe", "no"):
    st.session_state.answered = choice
    st.session_state.stage = "result"
    if choice == "yes":
        st.balloons()
    st.query_params.clear()
    st.rerun()

stage_q = st.query_params.get("stage")
if stage_q in ("letter", "intro", "question", "result"):
    st.session_state.stage = stage_q

# ----- Inject floaties + persistent audio into PARENT DOM -----
# NOTE: base64 audio means no missing-file URL issues on Streamlit Cloud.
# IMPORTANT: do NOT attempt autoplay on load; play on letter-open click for reliability.
EFFECTS_AND_AUDIO = f"""
<div></div>
<script>
(function(){{
  try {{
    const doc = window.parent.document;

    // Prevent duplicate install on reruns
    if (!doc.getElementById("floaty-layer-installed")) {{
      const marker = doc.createElement("div");
      marker.id = "floaty-layer-installed";
      marker.style.display = "none";
      doc.body.appendChild(marker);

      // Twinkles
      const tw = doc.createElement("div");
      tw.className = "twinkle";
      doc.body.appendChild(tw);

      // Persistent audio element (starts as song1, but played only by gesture)
      const audio = doc.createElement("audio");
      audio.id = "bgm_onigiri";
      audio.loop = true;
      audio.preload = "auto";
      audio.volume = 0.55;
      audio.style.display = "none";

      // store both tracks
      audio.dataset.song1 = "data:audio/mpeg;base64,{SONG1_B64}";
      audio.dataset.song2 = "data:audio/mpeg;base64,{SONG2_B64}";
      audio.dataset.current = "song1";

      audio.src = audio.dataset.song1;
      doc.body.appendChild(audio);

      // Helpers
      window.parent.__BGM_PLAY = async function(){{
        const a = doc.getElementById("bgm_onigiri");
        if (!a) return;
        try {{ await a.play(); }} catch(e) {{ /* blocked unless gesture */ }}
      }};

      window.parent.__BGM_TOGGLE = async function(){{
        const a = doc.getElementById("bgm_onigiri");
        if (!a) return;
        if (a.paused) {{
          try {{ await a.play(); }} catch(e) {{}}
        }} else {{
          a.pause();
        }}
      }};

      window.parent.__BGM_SET = async function(which){{
        const a = doc.getElementById("bgm_onigiri");
        if (!a) return;
        const wanted = (which === "song2") ? "song2" : "song1";
        if (a.dataset.current === wanted) return;

        a.pause();
        a.dataset.current = wanted;
        a.src = (wanted === "song2") ? a.dataset.song2 : a.dataset.song1;
        a.load();

        try {{ await a.play(); }} catch(e) {{}}
      }};

      // Floaties
      const FLOATIES = ["💖","💘","💝","💗","💓","💕","❤️","🎈","🎈","🍙","🍙","🍣","✨","✨"];

      function spawnFloaty(emoji=null){{
        // hard cap for performance
        if (doc.querySelectorAll(".floaty").length > 18) return;

        const el = doc.createElement("div");
        el.className = "floaty";
        el.textContent = emoji || FLOATIES[Math.floor(Math.random()*FLOATIES.length)];
        el.style.left = Math.floor(Math.random()*96) + "vw";

        const dur = 6 + Math.random()*4;      // 6–10s
        const size = 18 + Math.random()*24;   // lighter
        el.style.animationDuration = dur + "s";
        el.style.fontSize = size + "px";
        el.style.transform = `translate3d(0,0,0) rotate(${{
          Math.floor(Math.random()*22)-11
        }}deg)`;

        doc.body.appendChild(el);
        window.setTimeout(()=>el.remove(), (dur*1000)+900);
      }}

      function burst(){{
        const burstSet = ["✨","💖","💕","🍙","🍣"];
        for(let i=0;i<6;i++) {{
          window.setTimeout(()=>spawnFloaty(burstSet[Math.floor(Math.random()*burstSet.length)]), i*90);
        }}
      }}

      // Initial sprinkle
      for(let i=0;i<12;i++) {{
        window.setTimeout(()=>spawnFloaty(), i*120);
      }}
      window.setTimeout(burst, 900);

      // Continuous spawning
      const baseInterval = 900;
      const burstChance = 0.03;

      window.setInterval(()=>{{
        spawnFloaty();
        if (Math.random() < burstChance) burst();
      }}, baseInterval);
    }}
  }} catch(e) {{
    console.log("Effects/audio blocked:", e);
  }}
}})();
</script>
"""
components.html(EFFECTS_AND_AUDIO, height=0)

# ----- UI -----
st.write("")

if AUDIO_ERROR:
    st.error(AUDIO_ERROR)

with st.container():
    st.markdown(
        '<div class="badge">✨ A tiny website I made just for you, my love, my heart, my honey pie pie ✨</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="title-strip">
          <span>🍙</span>
          <span>MNO 5ever</span>
          <span>🍣</span>
        </div>
        <div class="title-strip">
          <span class="pulse">💘</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    who = HER_NAME.strip() if HER_NAME.strip() else "baby pie"

    # =========================
    # STAGE 0: LOVE LETTER
    # =========================
    if st.session_state.stage == "letter":
        st.markdown("## 💌 A love letter for you…")
        st.markdown(
            f"""
            <div class="envelope-wrap">
              <div class="envelope" id="open_letter" role="button" aria-label="Open love letter">
                <div class="sparkle"></div>

                <div class="env-top">
                  <div>
                    <div class="env-title">To: <b>{HER_NAME}</b> 🍙</div>
                    <div class="env-sub">From: <b>{ME_NICKNAME}</b> 🍣</div>
                  </div>
                  <div class="env-stamp">💘</div>
                </div>

                <div class="env-body">
                  <div class="env-paper">
                    <div class="paper-line"></div>
                    <div class="paper-line short"></div>
                    <div class="paper-line"></div>
                    <div class="paper-line tiny"></div>
                  </div>
                </div>

                <div class="env-cta">
                  <span class="pulse">✨</span>
                  <span>Tap to open</span>
                  <span class="pulse">✨</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # JS: animate envelope -> play song1 on this click gesture -> navigate to intro
        components.html(
            """
            <script>
            (function(){
              try{
                const doc = window.parent.document;
                const env = doc.getElementById("open_letter");
                if (!env) return;

                if (env.dataset.bound === "1") return;
                env.dataset.bound = "1";

                const goIntro = () => {
                  const url = new URL(window.parent.location.href);
                  url.searchParams.set("stage", "intro");
                  window.parent.location.href = url.toString();
                };

                env.addEventListener("click", async () => {
                  try{
                    // Start animation immediately
                    env.classList.add("opening");

                    // Ensure correct track (song1) and attempt to play (gesture-based)
                    if (window.parent.__BGM_SET) {
                      await window.parent.__BGM_SET("song1");
                    }
                    if (window.parent.__BGM_PLAY) {
                      await window.parent.__BGM_PLAY();
                    }
                  }catch(e){}

                  // Let the animation be seen before navigation
                  window.setTimeout(goIntro, 520);
                }, {capture:true});

                // Make Enter/Space also open (accessibility)
                env.setAttribute("tabindex", "0");
                env.addEventListener("keydown", (e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    env.click();
                  }
                });
              }catch(e){}
            })();
            </script>
            """,
            height=0,
        )

    # =========================
    # STAGE 1: INTRO
    # =========================
    elif st.session_state.stage == "intro":
        st.markdown("## 💌 Hey baby pie…")
        st.markdown(
            f"""
            <p class="big">
              I made this little page because I wanted to ask you something in a way that’s
              <b>very {ME_NICKNAME}</b>… and very <span class="pulse">💘</span>
              <br><br>
              First, make sure your music sounds are on! 🔊🎶
              <br><br>
              Also, I added 🍣 and 🍙 floating around because we’re literally Maki &amp; Onigiri.
              <br><br>
              So… here goes nothing!
            </p>
            """,
            unsafe_allow_html=True,
        )

        # Streamlit button (changes stage)
        if st.button("Open the question 💖"):
            st.session_state.stage = "question"
            st.rerun()

        # IMPORTANT: Bind to the same click gesture and switch to song2
        components.html(
            """
            <script>
            (function(){
              try {
                const doc = window.parent.document;

                // Find the Streamlit button by its visible text
                const buttons = Array.from(doc.querySelectorAll('button'));
                const target = buttons.find(b => (b.innerText || "").trim() === "Open the question 💖");
                if (!target) return;

                // Avoid binding multiple times on reruns
                if (target.dataset.bgmBound === "1") return;
                target.dataset.bgmBound = "1";

                target.addEventListener("click", async () => {
                  try {
                    if (window.parent.__BGM_SET) {
                      await window.parent.__BGM_SET("song2");
                    } else if (window.parent.__BGM_PLAY) {
                      await window.parent.__BGM_PLAY();
                    }
                  } catch (e) {
                    console.log("BGM switch blocked:", e);
                  }
                }, { capture: true });
              } catch (e) {
                console.log("Bind failed:", e);
              }
            })();
            </script>
            """,
            height=0,
        )

    # =========================
    # STAGE 2: QUESTION
    # =========================
    elif st.session_state.stage == "question":
        st.markdown(
            f"""
            <h1 style="margin-top: 0.2rem;">{who}, will you be my Valentine? 💝</h1>
            <p class="big">
              No pressure… but also… <b>I’m really hoping you say yes.</b> 🥺
              <br>
              (I even brought some snacks: 🍙 for you, 🍣 for me, while you think.)
            </p>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("YES 💖", use_container_width=True):
                st.session_state.answered = "yes"
                st.balloons()
                st.session_state.stage = "result"
                st.rerun()

        with col2:
            # Runaway "I'm thinking" button (navigate parent URL so Streamlit sees it)
            components.html(
                """
                <div style="position: relative; height: 68px; display:flex; align-items:center; justify-content:center;">
                  <button id="runaway"
                    style="
                      position:absolute;
                      padding: 12px 14px;
                      border-radius: 14px;
                      border: 0;
                      font-weight: 900;
                      cursor: pointer;
                      box-shadow: 0 12px 26px rgba(0,0,0,0.14);
                      background: rgba(255,255,255,0.90);
                      color: #2b2b2b;
                    ">
                    I’m thinking… 🤭
                  </button>
                </div>

                <script>
                  const btn = document.getElementById("runaway");

                  function moveButton() {
                    const x = (Math.random() * 210) - 105;
                    const y = (Math.random() * 40) - 20;
                    const r = (Math.random() * 14) - 7;
                    btn.style.transform = `translate(${x}px, ${y}px) rotate(${r}deg)`;
                  }

                  btn.addEventListener("mouseenter", moveButton);
                  btn.addEventListener("touchstart", () => moveButton(), {passive:true});

                  btn.addEventListener("click", () => {
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set("choice", "maybe");
                    window.parent.location.href = url.toString();
                  });

                  setTimeout(moveButton, 420);
                </script>
                """,
                height=82,
            )

        st.caption("psst… the ‘thinking’ button is shy 😳")

    # =========================
    # STAGE 3: RESULT
    # =========================
    else:
        if st.session_state.answered == "yes":
            st.markdown(
                f"""
                <h1 class="pulse">YAYYYYY 💘💘💘</h1>
                <p class="big">
                  Okay it’s official. {who}, you just made my whole day.
                  <br><br>
                  <b>Long-distance Valentine plan:</b> video call + dinner together + a silly screenshot 📸
                  <br>
                  Then we do a “food exchange”: my food for you, your food for me, and 💖 for both.
                </p>
                """,
                unsafe_allow_html=True,
            )
            st.success("Achievement unlocked: Official Valentine 💘🍙🍣")

        if st.button("Ask again (reset) 🔁"):
            st.session_state.stage = "letter"  # reset back to envelope
            st.session_state.answered = None
            st.rerun()

    st.markdown(
        '<hr style="border: none; height: 1px; background: rgba(0,0,0,0.08);">',
        unsafe_allow_html=True,
    )
