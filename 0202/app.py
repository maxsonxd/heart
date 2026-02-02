import base64
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ----- Page setup -----
st.set_page_config(page_title="💘 A Question For You", page_icon="💘", layout="centered")

# ----- Custom names -----
HER_NAME = "Onigiri"
ME_NICKNAME = "Maki Pie"

# ----- Load song.mp3 as base64 (fixes "missing on deploy") -----
APP_DIR = Path(__file__).resolve().parent
SONG_PATH = APP_DIR / "song2.mp3"

AUDIO_B64 = ""
AUDIO_ERROR = ""

try:
    AUDIO_B64 = base64.b64encode(SONG_PATH.read_bytes()).decode("utf-8")
except FileNotFoundError:
    AUDIO_ERROR = f"song file not found at: {SONG_PATH}"
except Exception as e:
    AUDIO_ERROR = f"Could not load song file: {e}"

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

/* Mini music controls */
.musicbar{
  display:flex;
  justify-content:center;
  gap: 10px;
  margin: 8px 0 2px 0;
}
.musicbtn{
  padding: 9px 12px;
  border-radius: 12px;
  border: 0;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 10px 22px rgba(0,0,0,0.12);
  background: rgba(255,255,255,0.90);
  color: #2b2b2b;
}
.musichint{
  text-align:center;
  font-size: 0.92rem;
  opacity: 0.78;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----- State -----
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
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
if stage_q in ("intro", "question", "result"):
    st.session_state.stage = stage_q

# ----- Inject floaties + persistent audio into PARENT DOM -----
# NOTE: base64 audio means no missing-file URL issues on Streamlit Cloud.
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

      // Persistent audio element
      const audio = doc.createElement("audio");
      audio.id = "bgm_onigiri";
      audio.loop = true;
      audio.preload = "auto";
      audio.volume = 0.55;
      audio.style.display = "none";
      audio.src = "data:audio/mpeg;base64,{AUDIO_B64}";
      doc.body.appendChild(audio);

      // Helpers
      window.parent.__BGM_PLAY = async function(){{
        const a = doc.getElementById("bgm_onigiri");
        if (!a) return;
        try {{ await a.play(); }} catch(e) {{ console.log("BGM blocked:", e); }}
      }};
      window.parent.__BGM_TOGGLE = async function(){{
        const a = doc.getElementById("bgm_onigiri");
        if (!a) return;
        if (a.paused) {{
          try {{ await a.play(); }} catch(e) {{ console.log("BGM blocked:", e); }}
        }} else {{
          a.pause();
        }}
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
        el.style.transform = `translate3d(0,0,0) rotate(${{Math.floor(Math.random()*22)-11}}deg)`;

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

# # Music toggle (backup gesture if a phone blocks the first play)
# components.html(
#     """
#     <div class="musicbar">
#       <button class="musicbtn" id="musicToggle">🎵 Mute/Unmute</button>
#     </div>
#     <script>
#       const btn = document.getElementById("musicToggle");
#       btn.addEventListener("click", async () => {
#         if (window.parent.__BGM_TOGGLE) await window.parent.__BGM_TOGGLE();
#       });
#     </script>
#     """,
#     height=80,
# )

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

    if st.session_state.stage == "intro":
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

        # IMPORTANT: Custom HTML button so audio.play() runs in the SAME click gesture.
        # Also navigate the TOP-LEVEL window (window.parent.location), not the iframe.
        if st.button("Open the question 💖"):
          st.session_state.stage = "question"
          st.rerun()
          
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
                    if (window.parent.__BGM_PLAY) {
                      await window.parent.__BGM_PLAY();
                    }
                  } catch (e) {
                    console.log("BGM play blocked:", e);
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

    else:  # result
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
            st.session_state.stage = "intro"
            st.session_state.answered = None
            st.rerun()

    st.markdown(
        '<hr style="border: none; height: 1px; background: rgba(0,0,0,0.08);">',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
