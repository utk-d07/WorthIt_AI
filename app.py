import streamlit as st
import pandas as pd
import pickle
import os
import textwrap

# ---------------- SETUP ----------------

st.set_page_config(
    page_title="WorthIt",
    page_icon="✷",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

with open(os.path.join(MODEL_DIR, "worthit_model.pkl"), "rb") as file:
    model = pickle.load(file)

with open(os.path.join(MODEL_DIR, "preprocessor.pkl"), "rb") as file:
    preprocessor = pickle.load(file)


def render_html(content):
    st.html(textwrap.dedent(content).strip())


# ---------------- DESIGN + CSS ----------------

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700;800;900&display=swap');

:root {
    --paper: #f4eadc;
    --ink: #171914;
    --green: #075c43;
    --orange: #ff4c27;
    --muted: #77766c;
    --line: #d9cbbb;
}

.stApp {
    background: var(--paper);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1160px;
    padding: 1rem 2rem 3rem;
}

html {
    scroll-behavior: smooth;
    scroll-padding-top: 90px;
}

/* NAVIGATION */

.worth-nav {
    position: relative;
    z-index: 999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    background: rgba(244,234,220,.94);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--line);
}

.worth-logo {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--green);
    font-size: 21px;
    font-weight: 700;
    letter-spacing: -1.5px;
    text-decoration: none;
}

.worth-logo span {
    color: var(--orange);
    font-size: 25px;
}

.worth-links {
    display: flex;
    align-items: center;
    gap: 25px;
}

.worth-links a {
    text-decoration: none;
    color: var(--ink);
    font-size: 12px;
    font-weight: 600;
    transition: color .2s ease;
}

.worth-links a:hover {
    color: var(--orange);
}

.worth-links .nav-cta {
    background: var(--green);
    color: var(--paper);
    padding: 11px 18px;
    border-radius: 30px;
}

.worth-links .nav-cta:hover {
    background: var(--orange);
    color: white;
}

/* FLOATING DECISION BUTTON */

.floating-decision {
    position: fixed;
    bottom: 25px;
    right: 25px;
    z-index: 1000;
    background: var(--orange);
    color: white !important;
    padding: 15px 22px;
    border-radius: 50px;
    text-decoration: none !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 800;
    font-size: 12px;
    box-shadow: 0 8px 28px rgba(23,25,20,.2);
    transition: transform .25s ease, background .25s ease;
}

.floating-decision:hover {
    transform: translateY(-5px) scale(1.04);
    background: var(--green);
}

/* HERO */

.hero {
    position: relative;
    overflow: hidden;
    padding: 85px 0 50px;
    border-bottom: 1px solid var(--line);
}

.hero-title {
    position: relative;
    z-index: 2;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(85px, 14vw, 165px);
    font-weight: 900;
    letter-spacing: -4px;
    line-height: .77;
    text-transform: uppercase;
    color: var(--orange);
    margin: 0;
    animation: hero-arrive 1s cubic-bezier(.2,.8,.2,1) both;
}

.hero-title span {
    color: var(--green);
}

@keyframes hero-arrive {
    from {
        opacity: 0;
        transform: translateY(55px);
        filter: blur(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
    }
}

.hero-lower {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 30px;
    margin-top: 45px;
}

.hero-description {
    max-width: 390px;
    font-size: 14px;
    line-height: 1.8;
    color: #626359;
}

.hero-scroll {
    color: var(--green);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* FLOATING ORBS */

.ambient-orb {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    animation: float-orb 8s ease-in-out infinite;
}

.orb-one {
    width: 115px;
    height: 115px;
    background: radial-gradient(circle at 35% 35%, #ffb18e, var(--orange));
    opacity: .8;
    top: 12%;
    right: 9%;
    box-shadow: 0 10px 40px rgba(255,76,39,.15);
}

.orb-two {
    width: 65px;
    height: 65px;
    background: radial-gradient(circle at 35% 35%, #a5d4bd, var(--green));
    opacity: .8;
    bottom: 12%;
    right: 32%;
    animation-delay: -3s;
}

@keyframes float-orb {
    0%, 100% {
        transform: translate3d(0,0,0) rotate(0deg);
    }
    50% {
        transform: translate3d(-15px,-28px,0) rotate(12deg);
    }
}

/* SCROLL REVEAL */

.scroll-reveal {
    animation: reveal-up linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 30%;
}

@keyframes reveal-up {
    from {
        opacity: 0;
        transform: translateY(55px) scale(.97);
        filter: blur(7px);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
        filter: blur(0);
    }
}

/* STATEMENT */

.statement {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    padding: 85px 0;
    align-items: center;
}

.statement-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(55px, 8vw, 100px);
    line-height: .86;
    text-transform: uppercase;
    font-weight: 900;
    color: var(--green);
    letter-spacing: -1px;
}

.statement-copy {
    font-size: 15px;
    line-height: 1.9;
    color: #65665c;
    max-width: 410px;
}

.statement-copy strong {
    color: var(--ink);
}

/* CHOICES */

.choices {
    background: var(--ink);
    color: var(--paper);
    margin: 0 -2rem;
    padding: 65px 2rem;
    transition: background .5s ease;
}

.choices-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(55px, 8vw, 90px);
    line-height: .87;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 30px;
}

.choices-title span {
    color: var(--orange);
}

.choice-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(130px, 1fr));
    gap: 9px;
    overflow-x: auto;
    padding: 10px 3px 18px;
    scrollbar-width: thin;
    scrollbar-color: var(--orange) #333;
}

.choice {
    position: relative;
    overflow: hidden;
    min-height: 135px;
    padding: 15px;
    border: 1px solid #4b4c44;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    cursor: default;
    transition:
        transform .35s cubic-bezier(.2,.8,.2,1),
        background .35s ease,
        border-radius .35s ease;
}

.choice::after {
    content: "";
    position: absolute;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,.13);
    top: 100%;
    left: 50%;
    transform: translate(-50%,-50%) scale(0);
    transition: transform .5s ease;
}

.choice:hover {
    transform: translateY(-12px) rotate(-1deg);
    background: var(--green);
    border-radius: 12px;
}

.choice:hover::after {
    transform: translate(-50%,-50%) scale(2.5);
}

.choice:nth-child(2),
.choice:nth-child(5) {
    background: var(--orange);
    border-color: var(--orange);
}

.choice:nth-child(even):hover {
    transform: translateY(-12px) rotate(1deg);
}

.choice-number {
    font-size: 11px;
    color: #c5c3b8;
}

.choice-name {
    position: relative;
    z-index: 2;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 29px;
    font-weight: 800;
    text-transform: uppercase;
    line-height: .9;
}

/* FORM INTRO */

.form-intro {
    padding: 85px 0 30px;
}

.form-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(65px, 9vw, 110px);
    line-height: .85;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--green);
}

.form-description {
    max-width: 400px;
    font-size: 13px;
    line-height: 1.8;
    color: var(--muted);
    margin-top: 20px;
}

/* FORM */

div[data-testid="stForm"] {
    background: linear-gradient(135deg, rgba(255,255,255,.58), rgba(255,249,241,.72));
    padding: 38px;
    border: 1px solid rgba(255,255,255,.82);
    border-radius: 18px;
    box-shadow: 0 18px 55px rgba(23,25,20,.08),
                inset 0 1px 0 rgba(255,255,255,.9);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

/* QUESTION LABELS */

div[data-testid="stForm"] label p {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: var(--green) !important;
    margin-bottom: 11px !important;
}

/* GLASS DROPDOWNS AND NUMBER FIELDS */

div[data-testid="stForm"] div[data-baseweb="select"] > div,
div[data-testid="stForm"] div[data-baseweb="input"] > div {
    background: rgba(255,255,255,.62) !important;
    border: 1px solid rgba(7,92,67,.18) !important;
    border-radius: 13px !important;
    min-height: 64px !important;
    box-shadow: 0 8px 22px rgba(23,25,20,.045),
                inset 0 1px 0 rgba(255,255,255,.95) !important;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    transition: border-color .25s ease, box-shadow .25s ease, transform .25s ease;
}

div[data-testid="stForm"] div[data-baseweb="select"] > div:hover,
div[data-testid="stForm"] div[data-baseweb="input"] > div:hover {
    border-color: rgba(7,92,67,.55) !important;
    box-shadow: 0 10px 26px rgba(7,92,67,.10),
                inset 0 1px 0 rgba(255,255,255,.95) !important;
    transform: translateY(-1px);
}

div[data-testid="stForm"] div[data-baseweb="select"] > div:focus-within,
div[data-testid="stForm"] div[data-baseweb="input"] > div:focus-within {
    border: 1.5px solid var(--green) !important;
    box-shadow: 0 0 0 4px rgba(7,92,67,.10),
                0 12px 28px rgba(7,92,67,.09) !important;
}

/* INPUT TEXT AND PLACEHOLDERS */

div[data-testid="stForm"] div[data-baseweb="select"] *,
div[data-testid="stForm"] div[data-baseweb="input"] input {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: var(--ink) !important;
}

div[data-testid="stForm"] div[data-baseweb="input"] input::placeholder {
    color: #99978d !important;
    opacity: 1 !important;
}

/* DROPDOWN ARROW */

div[data-testid="stForm"] div[data-baseweb="select"] svg {
    color: var(--green) !important;
    width: 22px !important;
    height: 22px !important;
    transition: transform .2s ease;
}

/* DROPDOWN OPTION MENU */

div[data-baseweb="popover"] {
    border: 1px solid rgba(255,255,255,.9) !important;
    border-radius: 14px !important;
    background: rgba(255,252,246,.94) !important;
    box-shadow: 0 18px 45px rgba(23,25,20,.16) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    overflow: hidden;
}

div[data-baseweb="popover"] li {
    min-height: 48px !important;
    padding-top: 9px !important;
    padding-bottom: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {
    gap: 24px;
}

/* FORM GROUPS */

.form-divider {
    border-top: 1px solid rgba(7,92,67,.16);
    margin: 32px 0 26px;
}

.form-group-title {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--green);
    font-weight: 700;
    font-size: 20px;
    margin-bottom: 6px;
    letter-spacing: -.4px;
}

.form-group-copy {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 23px;
}

/* SUBMIT BUTTON */

div[data-testid="stFormSubmitButton"] button {
    background: var(--orange);
    color: white;
    border: none;
    border-radius: 6px;
    min-height: 58px;
    font-size: 15px;
    font-weight: 800;
    transition: background .2s ease, transform .2s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: var(--green);
    color: white;
    transform: translateY(-3px);
}

/* RESULT */

.result {
    margin-top: 50px;
    background: var(--green);
    padding: 55px;
    color: var(--paper);
    animation: result-arrive .8s cubic-bezier(.2,.8,.2,1) both;
}

.result-heading {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(60px, 10vw, 110px);
    font-weight: 900;
    line-height: .85;
    text-transform: uppercase;
    color: var(--paper);
}

.result-description {
    max-width: 480px;
    font-size: 14px;
    line-height: 1.8;
    color: #dce9df;
    margin-top: 20px;
}

@keyframes result-arrive {
    from {
        opacity: 0;
        transform: translateY(35px) scale(.97);
        clip-path: inset(0 0 100% 0);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
        clip-path: inset(0);
    }
}

/* FOOTER */

.worth-footer {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    border-top: 1px solid var(--line);
    margin-top: 60px;
    padding: 18px 0;
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* ACCESSIBILITY */

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        scroll-behavior: auto !important;
        transition: none !important;
    }
}

/* MOBILE RESPONSIVENESS */

@media (max-width: 700px) {

    .block-container {
        padding: 0 14px 2rem;
    }

    /* NAVIGATION */

    .worth-nav {
        flex-wrap: wrap;
        gap: 12px;
        padding: 13px 0;
    }

    .worth-logo {
        font-size: 20px;
    }

    .worth-links {
        width: 100%;
        justify-content: space-between;
        gap: 8px;
    }

    .worth-links a {
        font-size: 10px;
        white-space: nowrap;
    }

    .worth-links .nav-cta {
        padding: 9px 12px;
    }

    /* HERO */

    .hero {
        padding: 65px 0 35px;
    }

    .hero-title {
        font-size: clamp(58px, 17vw, 105px);
        letter-spacing: -2px;
        line-height: .84;
    }

    .hero-lower {
        flex-direction: column;
        align-items: flex-start;
        gap: 18px;
        margin-top: 30px;
    }

    .hero-description {
        max-width: 100%;
        font-size: 13px;
    }

    .orb-one {
        width: 65px;
        height: 65px;
    }

    .orb-two {
        width: 42px;
        height: 42px;
    }

    /* STATEMENT */

    .statement {
        grid-template-columns: 1fr;
        gap: 24px;
        padding: 55px 0;
    }

    .statement-title {
        font-size: clamp(52px, 14vw, 80px);
    }

    .statement-copy {
        font-size: 14px;
    }

    /* CHOICES */

    .choices {
        margin: 0 -14px;
        padding: 42px 14px;
    }

    .choices-title {
        font-size: clamp(48px, 13vw, 75px);
    }

    .choice-grid {
        grid-template-columns: repeat(7, 125px);
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        gap: 8px;
    }

    .choice {
        min-height: 120px;
        padding: 13px;
    }

    .choice-name {
        font-size: 26px;
    }

    /* FORM INTRO */

    .form-intro {
        padding: 55px 0 25px;
    }

    .form-title {
        font-size: clamp(55px, 14vw, 85px);
    }

    .form-description {
        font-size: 13px;
    }

    /* FORM LAYOUT */

    div[data-testid="stForm"] {
        padding: 24px 16px;
        border-radius: 15px;
    }

    div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 16px !important;
    }

    div[data-testid="stForm"] [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    div[data-testid="stForm"] label p {
        font-size: 13px !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] > div,
    div[data-testid="stForm"] div[data-baseweb="input"] > div {
        min-height: 58px !important;
    }

    .form-group-title {
        font-size: 18px;
    }

    .form-group-copy {
        font-size: 11px;
    }

    .form-divider {
        margin: 25px 0 22px;
    }

    div[data-testid="stFormSubmitButton"] button {
        min-height: 56px;
        font-size: 14px;
    }

    /* RESULT */

    .result {
        margin-top: 30px;
        padding: 30px 20px;
    }

    .result-heading {
        font-size: clamp(48px, 13vw, 75px);
        overflow-wrap: anywhere;
    }

    .result-description {
        font-size: 13px;
    }

    /* FOOTER */

    .worth-footer {
        flex-direction: column;
        gap: 10px;
        margin-top: 40px;
        font-size: 9px;
    }

    /* FLOATING BUTTON */

    .floating-decision {
        display: none;
    }
}

/* SMALL PHONES */

@media (max-width: 380px) {

    .block-container {
        padding-left: 11px;
        padding-right: 11px;
    }

    .worth-links a {
        font-size: 9px;
    }

    .worth-links .nav-cta {
        padding: 8px 9px;
    }

    div[data-testid="stForm"] {
        padding: 20px 12px;
    }

    .hero-title {
        font-size: 58px;
    }
}
</style>
""")


# ---------------- NAVIGATION ----------------

render_html("""
<nav class="worth-nav">
    <a class="worth-logo" href="#top"><span>✷</span> worthit</a>

    <div class="worth-links">
        <a href="#idea">The idea</a>
        <a href="#options">Your options</a>
        <a class="nav-cta" href="#decision-form">Make a decision ↗</a>
    </div>
</nav>

<div id="top"></div>

<a href="#decision-form" class="floating-decision">
    Let's figure it out ↗
</a>
""")


# ---------------- HERO ----------------

render_html("""
<section class="hero">

    <div class="ambient-orb orb-one"></div>
    <div class="ambient-orb orb-two"></div>

    <h1 class="hero-title">
        WANT IT.<br>
        <span>NEED IT?</span>
    </h1>

    <div class="hero-lower">
        <div class="hero-description">
            Before you spend your money, take a second.
            There might be a better way to get what you need.
        </div>

        <div class="hero-scroll">
            SCROLL TO EXPLORE ↓
        </div>
    </div>
</section>
""")


# ---------------- IDEA ----------------

render_html("""
<div id="idea"></div>

<section class="statement scroll-reveal">

    <div class="statement-title">
        NOT EVERY<br>
        NEED NEEDS<br>
        A NEW THING.
    </div>

    <div class="statement-copy">
        <p>
            Sometimes you already own what you need.
            Sometimes it just needs fixing.
        </p>

        <p>
            Maybe someone can lend it to you.
            Maybe renting makes more sense.
        </p>

        <p>
            <strong>
                Buying is an option. It doesn't have to be the first one.
            </strong>
        </p>
    </div>
</section>
""")


# ---------------- OPTIONS ----------------

render_html("""
<div id="options"></div>

<section class="choices scroll-reveal">

    <div class="choices-title">
        SEVEN WAYS.<br>
        <span>ONE DECISION.</span>
    </div>

    <div class="choice-grid">

        <div class="choice">
            <div class="choice-number">01</div>
            <div class="choice-name">Reuse</div>
        </div>

        <div class="choice">
            <div class="choice-number">02</div>
            <div class="choice-name">Repair</div>
        </div>

        <div class="choice">
            <div class="choice-number">03</div>
            <div class="choice-name">Borrow</div>
        </div>

        <div class="choice">
            <div class="choice-number">04</div>
            <div class="choice-name">Rent</div>
        </div>

        <div class="choice">
            <div class="choice-number">05</div>
            <div class="choice-name">Second-hand</div>
        </div>

        <div class="choice">
            <div class="choice-number">06</div>
            <div class="choice-name">Buy new</div>
        </div>

        <div class="choice">
            <div class="choice-number">07</div>
            <div class="choice-name">Wait</div>
        </div>

    </div>
</section>
""")


# ---------------- FORM INTRO ----------------

render_html("""
<div id="decision-form"></div>

<section class="form-intro scroll-reveal">

    <div class="form-title">
        LET'S FIGURE<br>
        IT OUT.
    </div>

    <div class="form-description">
        Tell us what you need and a little about your situation.
        We'll help you think through the options.
    </div>

</section>
""")


# ---------------- INPUT FORM ----------------

with st.form("worthit_form"):

    render_html("""
    <div class="form-group-title">The item</div>
    <div class="form-group-copy">
        First, tell us what you're looking for.
    </div>
    """)

    c1, c2 = st.columns(2)

    with c1:
        item_category = st.selectbox(
            "Item category",
            ["Appliances", "Clothing", "Electronics", "Furniture",
             "Other", "Sports", "Stationery"],
            index=None,
            placeholder="Select an option..."
        )

        purpose = st.selectbox(
            "Purpose",
            ["Education", "Household", "Other", "Personal",
             "Recreation", "Work"],
            index=None,
            placeholder="Select an option..."
        )

        estimated_cost = st.number_input(
            "Estimated cost (₹)",
            min_value=0,
            value=None,
            step=100,
            placeholder="Enter estimated cost"
        )

    with c2:
        budget = st.number_input(
            "Your budget (₹)",
            min_value=0,
            value=None,
            step=100,
            placeholder="Enter your budget"
        )

        urgency = st.selectbox(
            "How urgently do you need it?",
            ["High", "Medium", "Low"],
            index=None,
            placeholder="Select an option..."
        )

        usage_frequency = st.selectbox(
            "How often will you use it?",
            ["Daily", "Weekly", "Occasionally", "Rarely"],
            index=None,
            placeholder="Select an option..."
        )

    render_html("""
    <div class="form-divider"></div>

    <div class="form-group-title">What you already have</div>
    <div class="form-group-copy">
        Could something you own do the job?
    </div>
    """)

    c1, c2 = st.columns(2)

    with c1:
        duration_of_need = st.selectbox(
            "How long will you need it?",
            ["Short-term", "Medium-term", "Long-term"],
            index=None,
            placeholder="Select an option..."
        )

        similar_item_owned = st.selectbox(
            "Do you own a similar item?",
            ["Yes", "No"],
            index=None,
            placeholder="Select an option..."
        )

        item_condition = st.selectbox(
            "Condition of your existing item",
            ["Good", "Repairable", "Beyond Repair", "Not Applicable"],
            index=None,
            placeholder="Select an option..."
        )

    with c2:
        repair_feasibility = st.selectbox(
            "Can your existing item be repaired?",
            ["Yes", "No", "Not Applicable"],
            index=None,
            placeholder="Select an option..."
        )

        convenience_priority = st.selectbox(
            "How important is convenience?",
            ["High", "Medium", "Low"],
            index=None,
            placeholder="Select an option..."
        )

    render_html("""
    <div class="form-divider"></div>

    <div class="form-group-title">Other possibilities</div>
    <div class="form-group-copy">
        What alternatives would you consider?
    </div>
    """)

    c1, c2 = st.columns(2)

    with c1:
        borrowing_willingness = st.selectbox(
            "Would you be willing to borrow?",
            ["Yes", "No"],
            index=None,
            placeholder="Select an option..."
        )

        borrowing_renting_availability = st.selectbox(
            "What is available to you?",
            ["Borrowing", "Renting", "Both", "Neither"],
            index=None,
            placeholder="Select an option..."
        )

    with c2:
        secondhand_acceptance = st.selectbox(
            "Would you consider second-hand?",
            ["Yes", "No"],
            index=None,
            placeholder="Select an option..."
        )

    submitted = st.form_submit_button(
        "LET'S FIND OUT  ↗",
        use_container_width=True
    )


# ---------------- PREDICTION ----------------

if submitted:
    required_answers = [
        item_category, purpose, estimated_cost, budget, urgency,
        usage_frequency, duration_of_need, similar_item_owned,
        item_condition, repair_feasibility, convenience_priority,
        borrowing_willingness, borrowing_renting_availability,
        secondhand_acceptance
    ]

    if any(answer is None for answer in required_answers):
        st.error("Please answer every question before getting your recommendation.")
    else:

        input_data = pd.DataFrame([{
            "item_category": item_category,
            "purpose": purpose,
            "estimated_cost": estimated_cost,
            "budget": budget,
            "urgency": urgency,
            "usage_frequency": usage_frequency,
            "duration_of_need": duration_of_need,
            "similar_item_owned": similar_item_owned,
            "item_condition": item_condition,
            "repair_feasibility": repair_feasibility,
            "borrowing_willingness": borrowing_willingness,
            "borrowing_renting_availability": borrowing_renting_availability,
            "secondhand_acceptance": secondhand_acceptance,
            "convenience_priority": convenience_priority
        }])

        processed_input = preprocessor.transform(input_data)
        prediction = model.predict(processed_input)[0]

        recommendations = {
            "reuse": (
                "USE WHAT YOU HAVE.",
                "You may already own something that works. Try using it before spending money on another one."
            ),

            "repair": (
                "FIX IT. DON'T REPLACE IT.",
                "Your existing item may still have some life left. Repairing it could be the better move."
            ),

            "borrow": (
                "BORROW IT FOR NOW.",
                "If someone nearby has what you need, borrowing could save you from buying something you may not use often."
            ),

            "rent": (
                "RENT IT FOR NOW.",
                "If you only need it temporarily, renting could make more sense than owning it."
            ),

            "second_hand": (
                "GIVE PRE-OWNED A CHANCE.",
                "A second-hand item could do the job without the cost of buying a new one."
            ),

            "buy_new": (
                "GO AHEAD. BUY NEW.",
                "Given the details you entered, buying new may be the most suitable option."
            ),

            "postpone": (
                "NOT JUST YET.",
                "You may not need to spend right now. Give it some time and reconsider when the need becomes more pressing."
            )
        }

        title, description = recommendations[prediction]

        render_html(f"""
        <section class="result" id="result">

            <div class="result-heading">
                {title}
            </div>

            <div class="result-description">
                {description}
            </div>

        </section>
        """)

        st.caption(
            "This suggestion is based on your answers and the project's "
            "synthetic training dataset. It is not a guarantee."
        )


# ---------------- FOOTER ----------------

render_html("""
<footer class="worth-footer">
    <span>✷ WORTHIT</span>
    <span>THINK TWICE. SPEND WISELY.</span>
</footer>
""")
