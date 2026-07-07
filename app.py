import streamlit as st
import pandas as pd
import numpy as np
import random
import io

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Cricket Match Simulator",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS - Mobile Friendly
# ============================================================
st.markdown("""
<style>
    .main { padding: 1rem; }
    .stButton>button {
        width: 100%;
        background-color: #1a472a;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        border: none;
        margin-top: 10px;
    }
    .stButton>button:hover { background-color: #2d6a4f; }
    .result-box {
        background-color: #1e1e1e;
        color: #00ff88;
        border-left: 4px solid #00ff88;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: monospace;
        white-space: pre-wrap;
        font-size: 13px;
    }
    .score-box {
        background-color: #1a472a;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    .voiceover-box {
        background-color: #2a2a00;
        color: #ffc107;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-style: italic;
        font-size: 15px;
    }
    h1 { font-size: 24px !important; }
    h2 { font-size: 20px !important; }
    h3 { font-size: 16px !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PLAYER DATABASE
# ============================================================
@st.cache_data
def load_players():
    data = {
        "name": [
            "Sachin Tendulkar","Virat Kohli","Rohit Sharma","MS Dhoni","Sunil Gavaskar",
            "Rahul Dravid","Kapil Dev","Anil Kumble","Virender Sehwag","Yuvraj Singh",
            "Jasprit Bumrah","Ravindra Jadeja","Ravichandran Ashwin","Hardik Pandya",
            "KL Rahul","Shubman Gill","Suresh Raina","Harbhajan Singh","Zaheer Khan",
            "Vinoo Mankad","Bishan Bedi","Gundappa Viswanath",
            "Don Bradman","Ricky Ponting","Adam Gilchrist","Shane Warne","Glenn McGrath",
            "Steve Waugh","Matthew Hayden","David Warner","Pat Cummins","Mitchell Starc",
            "Dennis Lillee","Brett Lee","Josh Hazlewood","Neil Harvey","Arthur Morris","Bill O\'Reilly",
            "Viv Richards","Brian Lara","Garfield Sobers","Clive Lloyd","Malcolm Marshall",
            "Joel Garner","Michael Holding","Chris Gayle","Kieron Pollard","Dwayne Bravo",
            "Rohan Kanhai","Lance Gibbs","Everton Weekes","Frank Worrell","Clyde Walcott",
            "Wasim Akram","Waqar Younis","Imran Khan","Javed Miandad","Shahid Afridi",
            "Babar Azam","Shoaib Akhtar","Younis Khan","Mohammad Yousuf","Inzamam-ul-Haq",
            "Saeed Anwar","Mohammad Amir","Abdul Qadir","Mushtaq Ahmed",
            "Ian Botham","James Anderson","Andrew Flintoff","Kevin Pietersen","Alastair Cook",
            "Joe Root","Ben Stokes","Stuart Broad","Eoin Morgan","Jos Buttler",
            "Jonny Bairstow","Len Hutton","Denis Compton","Wally Hammond","Freddie Trueman",
            "Wilfred Rhodes","Peter May",
            "Jacques Kallis","AB de Villiers","Graeme Pollock","Shaun Pollock","Dale Steyn",
            "Hashim Amla","Kagiso Rabada","Graeme Smith","Faf du Plessis","Quinton de Kock",
            "Imran Tahir",
            "Muttiah Muralitharan","Kumar Sangakkara","Mahela Jayawardene","Sanath Jayasuriya",
            "Lasith Malinga","Angelo Mathews","Arjuna Ranatunga","Chaminda Vaas","Wanindu Hasaranga",
            "Richard Hadlee","Martin Crowe","Kane Williamson","Ross Taylor","Daniel Vettori",
            "Trent Boult","Tim Southee",
            "Shakib Al Hasan","Tamim Iqbal","Mushfiqur Rahim",
            "Rashid Khan","Mohammad Nabi",
            "Andy Flower","Heath Streak",
        ],
        "type": [
            "BAT","BAT","BAT","WK","BAT","BAT","ALL","BOWL","BAT","ALL",
            "BOWL","ALL","ALL","ALL","WK","BAT","BAT","BOWL","BOWL",
            "ALL","BOWL","BAT",
            "BAT","BAT","WK","BOWL","BOWL","BAT","BAT","BAT","BOWL","BOWL",
            "BOWL","BOWL","BOWL","BAT","BAT","BOWL",
            "BAT","BAT","ALL","BAT","BOWL","BOWL","BOWL","BAT","ALL","ALL",
            "BAT","BOWL","BAT","ALL","WK",
            "BOWL","BOWL","ALL","BAT","ALL","BAT","BOWL","BAT","BAT","BAT",
            "BAT","BOWL","BOWL","BOWL",
            "ALL","BOWL","ALL","BAT","BAT","BAT","ALL","BOWL","BAT","WK",
            "WK","BAT","BAT","ALL","BOWL","ALL","BAT",
            "ALL","WK","BAT","ALL","BOWL","BAT","BOWL","BAT","BAT","WK","BOWL",
            "BOWL","WK","BAT","ALL","BOWL","ALL","BAT","BOWL","ALL",
            "ALL","BAT","BAT","BAT","ALL","BOWL","BOWL",
            "ALL","BAT","WK","BOWL","ALL","WK","ALL",
        ],
        "nation": [
            "India","India","India","India","India","India","India","India","India","India",
            "India","India","India","India","India","India","India","India","India",
            "India","India","India",
            "Australia","Australia","Australia","Australia","Australia","Australia","Australia",
            "Australia","Australia","Australia","Australia","Australia","Australia","Australia",
            "Australia","Australia",
            "West Indies","West Indies","West Indies","West Indies","West Indies","West Indies",
            "West Indies","West Indies","West Indies","West Indies","West Indies","West Indies",
            "West Indies","West Indies","West Indies",
            "Pakistan","Pakistan","Pakistan","Pakistan","Pakistan","Pakistan","Pakistan",
            "Pakistan","Pakistan","Pakistan","Pakistan","Pakistan","Pakistan","Pakistan",
            "England","England","England","England","England","England","England","England",
            "England","England","England","England","England","England","England","England","England",
            "South Africa","South Africa","South Africa","South Africa","South Africa",
            "South Africa","South Africa","South Africa","South Africa","South Africa","South Africa",
            "Sri Lanka","Sri Lanka","Sri Lanka","Sri Lanka","Sri Lanka","Sri Lanka",
            "Sri Lanka","Sri Lanka","Sri Lanka",
            "New Zealand","New Zealand","New Zealand","New Zealand","New Zealand",
            "New Zealand","New Zealand",
            "Bangladesh","Bangladesh","Bangladesh",
            "Afghanistan","Afghanistan",
            "Zimbabwe","Zimbabwe",
        ],
        "bat_avg_odi": [
            44.83,58.18,49.34,50.57,35.13,39.16,23.79,10.97,35.05,36.55,
            3.67,32.06,14.67,30.52,46.45,55.79,35.31,11.64,9.82,
            0,6.0,29.95,
            0,42.03,35.89,13.05,3.83,32.9,43.49,45.3,9.79,10.94,
            5.81,18.38,6.5,0,0,0,
            47.0,40.48,0,31.64,15.49,9.8,6.84,37.83,36.56,25.36,
            0,0,0,0,0,
            16.52,7.02,33.41,41.7,23.57,57.18,5.19,34.52,41.71,39.52,
            39.21,7.39,9.23,6.83,
            23.21,7.0,26.82,40.73,36.4,45.59,40.61,10.23,39.7,40.41,
            46.24,0,0,0,0,0,0,
            44.36,53.5,0,26.45,6.73,49.46,8.96,37.98,47.48,48.3,7.24,
            7.63,41.98,33.37,32.36,4.47,38.84,35.84,17.5,22.41,
            21.61,38.55,47.78,48.36,18.56,8.73,13.71,
            37.57,36.63,36.45,19.43,29.31,35.34,22.28,
        ],
        "bat_sr_odi": [
            86.23,93.25,90.59,87.56,60.05,71.24,95.07,67.97,104.33,87.67,
            58.93,87.88,71.88,113.86,87.76,104.12,92.32,77.31,84.0,
            0,66.67,62.28,
            0,80.39,96.95,70.57,48.53,76.25,85.96,96.19,95.65,117.03,
            65.24,110.36,76.47,0,0,0,
            90.2,79.47,0,65.0,81.56,72.94,76.63,85.57,107.2,92.48,
            0,0,0,0,0,
            86.02,86.06,72.61,67.48,117.0,88.29,86.79,72.97,76.94,74.24,
            80.27,79.64,75.51,78.07,
            78.74,70.0,86.57,86.49,77.64,86.78,95.12,78.16,87.69,119.23,
            105.92,0,0,0,0,0,0,
            72.89,101.18,0,73.38,89.46,88.39,126.23,84.38,88.83,100.48,103.43,
            71.96,78.86,78.96,91.2,102.45,79.51,76.02,65.18,88.59,
            65.32,72.45,81.5,82.73,68.42,104.35,115.82,
            83.16,80.28,76.92,103.35,84.52,72.32,70.27,
        ],
        "bat_sr_t20": [
            125.0,137.96,140.89,126.13,0,86.11,0,0,145.02,136.38,
            88.0,127.47,122.38,147.46,141.85,158.28,134.88,93.33,115.56,
            0,0,0,
            0,129.13,152.51,0,0,0,143.68,142.49,126.98,125.0,
            0,134.29,100.0,0,0,0,
            0,0,0,0,0,0,0,142.65,149.22,128.25,
            0,0,0,0,0,
            0,0,0,0,130.05,129.67,81.82,112.42,108.42,0,
            0,94.29,0,0,
            0,0,119.72,143.43,84.85,125.56,132.76,117.73,136.44,143.9,
            140.98,0,0,0,0,0,0,
            111.93,150.13,0,109.62,132.0,126.21,134.38,128.57,134.77,136.65,100.0,
            91.67,120.84,127.61,128.13,119.05,116.4,0,100.0,131.76,
            0,0,125.85,127.05,107.33,100.0,137.56,
            124.48,116.46,117.98,135.24,133.06,0,0,
        ],
        "bowl_economy_odi": [
            5.1,6.13,5.43,10.57,3.67,5.41,3.71,4.3,5.04,5.11,
            4.63,4.98,4.99,5.79,0,0,5.37,4.44,4.57,
            0,3.9,0,
            0,5.08,0,4.25,3.88,4.03,0,0,5.26,5.22,
            3.75,4.76,5.19,0,0,0,
            3.79,4.63,0,3.45,3.53,3.09,3.32,4.93,5.18,5.38,
            0,0,0,0,0,
            3.89,4.68,3.89,3.42,4.62,0,4.58,4.25,4.15,3.91,
            4.46,5.26,3.47,4.06,
            3.84,4.61,4.49,4.59,0,5.01,5.67,4.88,6.0,0,
            0,0,0,0,0,0,0,
            4.05,0,0,3.67,4.83,0,5.13,0,5.48,0,4.33,
            3.93,0,5.55,4.76,5.26,4.83,3.98,4.18,5.38,
            3.3,4.07,4.38,4.99,4.2,4.98,5.5,
            4.66,0,0,4.14,4.82,0,4.06,
        ],
        "bowl_economy_t20": [
            0,0,0,0,0,0,0,0,0,7.08,
            6.26,7.68,6.97,8.58,0,0,7.32,6.92,7.44,
            0,0,0,
            0,0,0,0,0,0,0,0,8.28,7.73,
            0,7.39,7.29,0,0,0,
            0,0,0,0,0,0,0,7.1,7.42,7.82,
            0,0,0,0,0,
            0,0,0,0,6.76,0,7.04,0,0,0,
            0,6.97,0,0,
            0,0,7.52,6.2,0,8.43,8.86,7.23,0,0,
            0,0,0,0,0,0,0,
            7.31,0,0,6.38,7.83,0,7.55,0,0,0,6.67,
            6.0,0,0,8.27,7.47,8.14,0,7.38,6.41,
            0,0,7.57,6.75,6.75,7.93,8.02,
            7.16,0,0,6.27,6.93,0,0,
        ],
        "bowl_wickets_odi": [
            154,4,8,1,1,4,253,337,96,111,
            149,220,156,136,0,0,36,269,282,
            0,7,0,
            0,3,0,293,381,195,0,0,196,235,
            103,380,142,0,0,0,
            118,4,0,38,157,146,142,167,58,199,
            0,0,0,0,0,
            502,416,182,7,395,0,247,12,2,29,
            8,81,132,161,
            145,269,168,7,0,20,74,178,1,0,
            0,0,0,0,0,0,0,
            273,0,0,393,196,0,164,0,8,0,173,
            534,0,4,323,338,118,86,400,107,
            158,47,37,25,305,169,230,
            323,0,0,172,160,0,239,
        ],
    }
    return pd.DataFrame(data)

@st.cache_data
def load_venues():
    venues = [
        "Neutral / Generic","Wankhede (Mumbai)","Eden Gardens (Kolkata)",
        "Chinnaswamy (Bangalore)","Chepauk (Chennai)","Feroz Shah Kotla (Delhi)",
        "Narendra Modi Stadium (Ahmedabad)","MCG (Melbourne)","SCG (Sydney)",
        "Gabba (Brisbane)","WACA (Perth)","Adelaide Oval","Lord's (London)",
        "Headingley (Leeds)","Edgbaston (Birmingham)","The Oval (London)",
        "National Stadium (Karachi)","Gaddafi Stadium (Lahore)",
        "Rawalpindi Cricket Stadium","Kingsmead (Durban)","Newlands (Cape Town)",
        "Wanderers (Johannesburg)","SuperSport Park (Centurion)",
        "R Premadasa Stadium (Colombo)","Galle International Stadium",
        "Sinhalese Sports Club (Colombo)","Pallekele International (Kandy)",
        "Shere Bangla (Dhaka)","Basin Reserve (Wellington)",
        "Eden Park (Auckland)","Hagley Oval (Christchurch)",
        "Kensington Oval (Barbados)","Sabina Park (Kingston)",
        "Queen's Park Oval (Trinidad)","Sharjah Cricket Stadium",
        "Dubai International Cricket Stadium",
    ]
    conditions = {
        "Neutral / Generic": {"pace_mod":1.0,"spin_mod":1.0,"bat_mod":1.0},
        "Wankhede (Mumbai)": {"pace_mod":0.9,"spin_mod":1.2,"bat_mod":1.15},
        "Eden Gardens (Kolkata)": {"pace_mod":0.85,"spin_mod":1.3,"bat_mod":1.1},
        "Chinnaswamy (Bangalore)": {"pace_mod":0.8,"spin_mod":1.25,"bat_mod":1.2},
        "Chepauk (Chennai)": {"pace_mod":0.75,"spin_mod":1.4,"bat_mod":1.0},
        "Feroz Shah Kotla (Delhi)": {"pace_mod":0.8,"spin_mod":1.35,"bat_mod":1.05},
        "Narendra Modi Stadium (Ahmedabad)": {"pace_mod":0.85,"spin_mod":1.25,"bat_mod":1.1},
        "MCG (Melbourne)": {"pace_mod":1.2,"spin_mod":0.85,"bat_mod":0.95},
        "SCG (Sydney)": {"pace_mod":1.1,"spin_mod":1.05,"bat_mod":1.0},
        "Gabba (Brisbane)": {"pace_mod":1.3,"spin_mod":0.8,"bat_mod":0.9},
        "WACA (Perth)": {"pace_mod":1.35,"spin_mod":0.75,"bat_mod":0.9},
        "Adelaide Oval": {"pace_mod":1.1,"spin_mod":0.95,"bat_mod":1.05},
        "Lord's (London)": {"pace_mod":1.25,"spin_mod":0.85,"bat_mod":0.95},
        "Headingley (Leeds)": {"pace_mod":1.3,"spin_mod":0.8,"bat_mod":0.9},
        "Edgbaston (Birmingham)": {"pace_mod":1.2,"spin_mod":0.9,"bat_mod":0.95},
        "The Oval (London)": {"pace_mod":1.15,"spin_mod":0.9,"bat_mod":1.0},
        "National Stadium (Karachi)": {"pace_mod":0.95,"spin_mod":1.1,"bat_mod":1.05},
        "Gaddafi Stadium (Lahore)": {"pace_mod":0.9,"spin_mod":1.2,"bat_mod":1.05},
        "Rawalpindi Cricket Stadium": {"pace_mod":0.95,"spin_mod":1.0,"bat_mod":1.15},
        "Kingsmead (Durban)": {"pace_mod":1.2,"spin_mod":0.85,"bat_mod":0.95},
        "Newlands (Cape Town)": {"pace_mod":1.25,"spin_mod":0.8,"bat_mod":0.9},
        "Wanderers (Johannesburg)": {"pace_mod":1.1,"spin_mod":0.9,"bat_mod":1.1},
        "SuperSport Park (Centurion)": {"pace_mod":1.15,"spin_mod":0.9,"bat_mod":1.0},
        "R Premadasa Stadium (Colombo)": {"pace_mod":0.8,"spin_mod":1.3,"bat_mod":1.05},
        "Galle International Stadium": {"pace_mod":0.7,"spin_mod":1.45,"bat_mod":0.95},
        "Sinhalese Sports Club (Colombo)": {"pace_mod":0.75,"spin_mod":1.4,"bat_mod":0.95},
        "Pallekele International (Kandy)": {"pace_mod":0.85,"spin_mod":1.25,"bat_mod":1.0},
        "Shere Bangla (Dhaka)": {"pace_mod":0.75,"spin_mod":1.4,"bat_mod":0.95},
        "Basin Reserve (Wellington)": {"pace_mod":1.3,"spin_mod":0.8,"bat_mod":0.88},
        "Eden Park (Auckland)": {"pace_mod":1.1,"spin_mod":0.9,"bat_mod":1.05},
        "Hagley Oval (Christchurch)": {"pace_mod":1.2,"spin_mod":0.85,"bat_mod":0.95},
        "Kensington Oval (Barbados)": {"pace_mod":1.1,"spin_mod":0.95,"bat_mod":1.0},
        "Sabina Park (Kingston)": {"pace_mod":1.2,"spin_mod":0.85,"bat_mod":0.9},
        "Queen's Park Oval (Trinidad)": {"pace_mod":1.0,"spin_mod":1.05,"bat_mod":1.0},
        "Sharjah Cricket Stadium": {"pace_mod":0.85,"spin_mod":1.25,"bat_mod":1.0},
        "Dubai International Cricket Stadium": {"pace_mod":0.85,"spin_mod":1.2,"bat_mod":1.0},
    }
    return venues, conditions

# ============================================================
# SIMULATION ENGINE
# ============================================================
OUTCOMES = ["dot","1","2","3","4","6","wicket"]
RUNS_MAP = {"dot":0,"1":1,"2":2,"3":3,"4":4,"6":6,"wicket":0}

def get_player_row(name, df):
    rows = df[df["name"] == name]
    return rows.iloc[0] if not rows.empty else None

def build_batter_profile(row, fmt, venue_cond):
    # T20 minimum strike rates by batting position type
    T20_MIN_SR = {
        "BAT": 125.0, "WK": 120.0, "ALL": 118.0,
        "BOWL": 90.0,
    }
    ODI_MIN_SR = {
        "BAT": 72.0, "WK": 70.0, "ALL": 68.0, "BOWL": 55.0,
    }
    ptype = str(row["type"])

    if fmt == "T20":
        sr_raw = float(row["bat_sr_t20"])
        # If no T20I SR recorded, estimate from ODI SR * 1.25
        if sr_raw <= 0:
            sr_raw = float(row["bat_sr_odi"]) * 1.25
        # Enforce minimums — nobody scores at <100 SR in T20
        sr = max(sr_raw, T20_MIN_SR.get(ptype, 100.0))
        avg = max(float(row["bat_avg_odi"]) * 0.6, 8.0)
    else:
        sr_raw = float(row["bat_sr_odi"])
        sr = max(sr_raw, ODI_MIN_SR.get(ptype, 60.0))
        avg = max(float(row["bat_avg_odi"]), 8.0)

    # Apply venue batting modifier
    sr = sr * venue_cond["bat_mod"]

    # Boundary rates — scale with SR
    # At SR=150, expect ~15% fours, ~8% sixes
    # At SR=80, expect ~8% fours, ~2% sixes
    sr_factor = sr / 130.0  # normalise around T20 average
    four_rate = min(0.18, max(0.06, 0.12 * sr_factor))
    six_rate  = min(0.12, max(0.02, 0.06 * sr_factor))

    # Wicket probability from average
    # Lower average = higher risk per ball
    wicket_prob = min(0.10, max(0.02, 1.0 / max(avg * (sr / 100.0), 8.0)))

    remaining = max(1.0 - four_rate - six_rate - wicket_prob, 0.25)
    return {
        "dot":    max(remaining * 0.38, 0.01),
        "1":      max(remaining * 0.42, 0.01),
        "2":      max(remaining * 0.12, 0.01),
        "3":      max(remaining * 0.08, 0.001),
        "4":      four_rate,
        "6":      six_rate,
        "wicket": wicket_prob,
        "name": row["name"], "avg": avg, "sr": sr,
    }

def build_bowler_profile(row, fmt, venue_cond):
    if fmt == "T20":
        econ = float(row["bowl_economy_t20"]) if row["bowl_economy_t20"] > 0 else float(row["bowl_economy_odi"]) * 1.2
    else:
        econ = float(row["bowl_economy_odi"])

    econ = max(econ, 3.5)
    wickets = float(row["bowl_wickets_odi"])

    # Apply venue modifier based on bowl type
    is_spinner = "spin" in row["name"].lower() or row["type"] == "BOWL"
    # Simple heuristic for spin vs pace
    spin_names = ["Warne","Muralitharan","Kumble","Ashwin","Jadeja","Harbhajan",
                  "Afridi","Qadir","Mushtaq","Bedi","Vettori","Nabi","Rashid",
                  "Tahir","Rhodes","Gibbs","O'Reilly","Mankad","Hasaranga"]
    is_spinner = any(s in row["name"] for s in spin_names)

    if is_spinner:
        econ_modifier = min((7.0 / econ) * venue_cond["spin_mod"], 2.5)
    else:
        econ_modifier = min((7.0 / econ) * venue_cond["pace_mod"], 2.5)

    wicket_modifier = min(35.0 / max(econ * 4, 10), 2.5)

    ptype = str(row["type"])
    is_genuine_bowler = ptype in {"BOWL", "ALL"}
    return {
        "name": row["name"],
        "econ_modifier": econ_modifier,
        "wicket_modifier": wicket_modifier if is_genuine_bowler else 0.1,
        "is_spinner": is_spinner,
        "is_bowler": is_genuine_bowler,
    }

# Hard list of known bowler types — belt and braces approach
BOWL_TYPES = {"BOWL", "ALL"}

def get_bowlers(xi, df):
    """Only return genuine bowlers. Never pick BAT or WK types."""
    bowlers = []
    for p in xi:
        rows = df[df["name"] == p]
        if not rows.empty:
            ptype = rows.iloc[0]["type"]
            if ptype in BOWL_TYPES:
                bowlers.append(p)
    # Safety: if somehow < 4 bowlers, warn but don't add batters
    return bowlers

def simulate_ball(bat_p, bowl_p, pressure=1.0):
    weights = {o: bat_p[o] for o in OUTCOMES}
    weights["dot"]    *= bowl_p["econ_modifier"]
    weights["wicket"] *= bowl_p["wicket_modifier"]
    weights["4"]      /= bowl_p["econ_modifier"]
    weights["6"]      /= bowl_p["econ_modifier"]
    weights["1"]      /= (bowl_p["econ_modifier"] ** 0.5)
    weights["4"] *= pressure
    weights["6"] *= pressure
    weights["wicket"] *= (pressure ** 1.5)
    total = sum(weights.values())
    probs = [weights[o] / total for o in OUTCOMES]
    return random.choices(OUTCOMES, weights=probs, k=1)[0]

def simulate_innings(batting_xi, bowling_xi, profiles, fmt, target=None):
    max_overs = 20 if fmt == "T20" else 50
    max_bowl_ovs = 4 if fmt == "T20" else 10
    # Only use genuine BOWL/ALL types — never BAT or WK
    bowlers = [p for p in bowling_xi
               if profiles.get(p, {}).get("bowl", {}).get("wicket_modifier", 0) > 0.5
               and profiles.get(p, {}).get("bowl", {}).get("is_bowler", False)]
    if len(bowlers) < 3:
        # Fallback: use anyone with bowling stats but still prefer proper bowlers
        bowlers = [p for p in bowling_xi
                   if profiles.get(p, {}).get("bowl", {}).get("wicket_modifier", 0) > 0.3][:6]
    if not bowlers:
        bowlers = bowling_xi[6:]  # last resort — use lower order only

    runs=0; wickets=0; balls=0
    striker=batting_xi[0]; non_striker=batting_xi[1]; bat_idx=2
    scorecard={p:{"runs":0,"balls":0,"fours":0,"sixes":0,"out":False} for p in batting_xi}
    bowl_card={p:{"overs":0,"runs":0,"wickets":0,"balls":0} for p in bowlers}
    bowl_idx=0; over_balls=0; key_moments=[]

    for ball_num in range(max_overs * 6):
        if wickets >= 10: break
        attempts=0
        while True:
            bowler = bowlers[bowl_idx % len(bowlers)]
            if bowl_card[bowler]["overs"] < max_bowl_ovs: break
            bowl_idx += 1; attempts += 1
            if attempts > len(bowlers): bowler = bowlers[0]; break

        pressure = 1.0
        if target:
            balls_left = (max_overs*6) - ball_num
            runs_needed = target - runs
            if balls_left > 0 and runs_needed > 0:
                rr_needed = (runs_needed/balls_left)*6
                rr_current = (runs/max(ball_num,1))*6
                pressure = min(max(rr_needed/max(rr_current,4),0.8),2.5)

        bat_p = profiles.get(striker,{}).get("bat",{})
        bowl_p = profiles.get(bowler,{}).get("bowl",{})

        if not bat_p or not bowl_p:
            outcome = random.choices(OUTCOMES,[0.35,0.30,0.10,0.02,0.12,0.05,0.06])[0]
        else:
            outcome = simulate_ball(bat_p, bowl_p, pressure)

        run_val = RUNS_MAP[outcome]
        runs+=run_val; balls+=1; over_balls+=1
        scorecard[striker]["balls"]+=1
        if bowler in bowl_card:
            bowl_card[bowler]["balls"]+=1
            bowl_card[bowler]["runs"]+=run_val

        if outcome=="4":
            scorecard[striker]["fours"]+=1; scorecard[striker]["runs"]+=4
        elif outcome=="6":
            scorecard[striker]["sixes"]+=1; scorecard[striker]["runs"]+=6
        elif outcome!="wicket":
            scorecard[striker]["runs"]+=run_val

        if outcome=="wicket":
            wickets+=1; scorecard[striker]["out"]=True
            if bowler in bowl_card: bowl_card[bowler]["wickets"]+=1
            if wickets in [3,5,7] or scorecard[striker]["runs"]>30:
                key_moments.append(f"{bowler} dismisses {striker} for {scorecard[striker]['runs']}")
            if bat_idx < len(batting_xi):
                striker=batting_xi[bat_idx]; bat_idx+=1
            else: break

        if run_val%2==1: striker,non_striker=non_striker,striker
        if over_balls==6:
            if bowler in bowl_card: bowl_card[bowler]["overs"]+=1
            over_balls=0; bowl_idx+=1
            striker,non_striker=non_striker,striker

        if target and runs>=target:
            key_moments.append("Target chased down!")
            break

    return {"runs":runs,"wickets":wickets,"overs":f"{balls//6}.{balls%6}",
            "scorecard":scorecard,"bowl_card":bowl_card,"key_moments":key_moments}

def simulate_match(t1_xi, t2_xi, profiles, fmt, sims=1000):
    results=[]
    for _ in range(sims):
        inn1=simulate_innings(t1_xi,t2_xi,profiles,fmt)
        inn2=simulate_innings(t2_xi,t1_xi,profiles,fmt,target=inn1["runs"]+1)
        t1w=inn2["runs"]<inn1["runs"] or inn2["wickets"]>=10
        results.append({
            "t1_score":inn1["runs"],"t1_wkts":inn1["wickets"],
            "t2_score":inn2["runs"],"t2_wkts":inn2["wickets"],
            "t1_wins":t1w,
            "margin_runs":inn1["runs"]-inn2["runs"] if t1w else 0,
            "margin_wkts":10-inn2["wickets"] if not t1w else 0,
            "inn1_moments":inn1["key_moments"],"inn2_moments":inn2["key_moments"],
            "inn1_card":inn1["scorecard"],"inn2_card":inn2["scorecard"],
            "inn1_bowl":inn1["bowl_card"],"inn2_bowl":inn2["bowl_card"],
        })

    t1wins=sum(1 for r in results if r["t1_wins"])
    t1pct=round(t1wins/sims*100,1)
    avg_t1=round(sum(r["t1_score"] for r in results)/sims)
    avg_t2=round(sum(r["t2_score"] for r in results)/sims)
    med=sorted(results,key=lambda r:r["t1_score"])[sims//2]

    return {"t1_win_pct":t1pct,"t2_win_pct":100-t1pct,
            "avg_t1":avg_t1,"avg_t2":avg_t2,"median":med,"sims":sims}

def generate_narrative(sim, t1_name, t2_name, fmt, venue):
    med=sim["median"]
    winner=t1_name if med["t1_wins"] else t2_name
    loser=t2_name if med["t1_wins"] else t1_name
    margin=f"{med['margin_runs']} runs" if med["t1_wins"] else f"{med['margin_wkts']} wickets"

    inn1_top=sorted(med["inn1_card"].items(),key=lambda x:x[1]["runs"],reverse=True)[:3]
    inn2_top=sorted(med["inn2_card"].items(),key=lambda x:x[1]["runs"],reverse=True)[:3]
    inn1_bowl=sorted(med["inn1_bowl"].items(),key=lambda x:x[1]["wickets"],reverse=True)[:2]
    inn2_bowl=sorted(med["inn2_bowl"].items(),key=lambda x:x[1]["wickets"],reverse=True)[:2]
    moments=(med["inn1_moments"]+med["inn2_moments"])[:4]

    scorecard=f"""
{fmt} SIMULATION — {venue}
{t1_name} vs {t2_name}
{'='*45}

INNINGS 1 — {t1_name}: {med['t1_score']}/{med['t1_wkts']}
Top Scorers:
{chr(10).join(f"  • {n}: {s['runs']} ({s['balls']}b) {s['fours']}x4 {s['sixes']}x6" for n,s in inn1_top)}
Key Bowlers:
{chr(10).join(f"  • {n}: {s['wickets']}wkts {s['runs']}runs" for n,s in inn1_bowl if s['wickets']>0) or "  • No wickets recorded"}

INNINGS 2 — {t2_name}: {med['t2_score']}/{med['t2_wkts']}
Target: {med['t1_score']+1}
Top Scorers:
{chr(10).join(f"  • {n}: {s['runs']} ({s['balls']}b) {s['fours']}x4 {s['sixes']}x6" for n,s in inn2_top)}
Key Bowlers:
{chr(10).join(f"  • {n}: {s['wickets']}wkts {s['runs']}runs" for n,s in inn2_bowl if s['wickets']>0) or "  • No wickets recorded"}

RESULT: {winner} won by {margin}

KEY MOMENTS:
{chr(10).join(f"  {i+1}. {m}" for i,m in enumerate(moments)) if moments else "  A close contest throughout."}

SIMULATION ({sim['sims']} matches):
  {t1_name}: {sim['t1_win_pct']}% wins
  {t2_name}: {sim['t2_win_pct']}% wins
  Avg scores — {t1_name}: {sim['avg_t1']} | {t2_name}: {sim['avg_t2']}
"""

    voiceover=f"""{t1_name} posted {med['t1_score']} for {med['t1_wkts']}.
{inn1_top[0][0] if inn1_top else "The openers"} top-scored with {inn1_top[0][1]['runs'] if inn1_top else 0}.
{t2_name} needed {med['t1_score']+1} to win.
{inn2_bowl[0][0] if inn2_bowl else "The bowlers"} struck at the crucial moment.
They fell short at {med['t2_score']} for {med['t2_wkts']}.
{winner} wins by {margin}.
{sim['sims']} simulations. One result. The numbers don't lie."""

    return scorecard, voiceover

# ============================================================
# MAIN APP UI
# ============================================================
st.title("🏏 Cricket Match Simulator")
st.caption("Pick your XIs. Run 1,000 simulations. Get the result.")

df = load_players()
venues, venue_conditions = load_venues()

all_players = sorted(df["name"].tolist())
nations = sorted(df["nation"].unique().tolist())

# ---- FORMAT & VENUE ----
col1, col2 = st.columns(2)
with col1:
    fmt = st.selectbox("Format", ["T20", "ODI"])
with col2:
    venue = st.selectbox("Venue", venues)

sims = st.select_slider("Simulations", options=[100, 500, 1000, 5000], value=1000)

st.divider()

# ---- TEAM SELECTION ----
st.subheader("🏏 Team 1")
t1_name = st.text_input("Team 1 Name", value="World Legends XI", key="t1_name")

# Filter by nation option
t1_nation = st.selectbox("Filter by nation (optional)", ["All Nations"] + nations, key="t1_nat")
t1_pool = all_players if t1_nation == "All Nations" else df[df["nation"]==t1_nation]["name"].tolist()
t1_pool = sorted(t1_pool)

t1_xi = st.multiselect(
    "Select 11 players for Team 1",
    options=t1_pool,
    max_selections=11,
    key="t1_players",
    help="Select exactly 11 players. Include at least 4 bowlers (BOWL or ALL type)."
)
if t1_xi:
    t1_bowlers = [p for p in t1_xi if df[df["name"]==p]["type"].values[0] in ["BOWL","ALL"]]
    st.caption(f"✅ {len(t1_xi)}/11 selected | Bowlers: {len(t1_bowlers)} ({', '.join(t1_bowlers[:3])}{'...' if len(t1_bowlers)>3 else ''})")
    if len(t1_bowlers) < 4:
        st.warning("⚠️ Add more bowlers (BOWL/ALL types)")

st.divider()

st.subheader("🏏 Team 2")
t2_name = st.text_input("Team 2 Name", value="Asian Legends XI", key="t2_name")

t2_nation = st.selectbox("Filter by nation (optional)", ["All Nations"] + nations, key="t2_nat")
t2_pool = all_players if t2_nation == "All Nations" else df[df["nation"]==t2_nation]["name"].tolist()
t2_pool = sorted(t2_pool)

t2_xi = st.multiselect(
    "Select 11 players for Team 2",
    options=t2_pool,
    max_selections=11,
    key="t2_players",
    help="Select exactly 11 players. Include at least 4 bowlers (BOWL or ALL type)."
)
if t2_xi:
    t2_bowlers = [p for p in t2_xi if df[df["name"]==p]["type"].values[0] in ["BOWL","ALL"]]
    st.caption(f"✅ {len(t2_xi)}/11 selected | Bowlers: {len(t2_bowlers)} ({', '.join(t2_bowlers[:3])}{'...' if len(t2_bowlers)>3 else ''})")
    if len(t2_bowlers) < 4:
        st.warning("⚠️ Add more bowlers (BOWL/ALL types)")

st.divider()

# ---- SIMULATE BUTTON ----
ready = len(t1_xi)==11 and len(t2_xi)==11
if not ready:
    st.info(f"Select 11 players for each team to simulate. T1: {len(t1_xi)}/11 | T2: {len(t2_xi)}/11")

if st.button("🏏 SIMULATE MATCH", disabled=not ready):
    with st.spinner(f"Running {sims} simulations..."):
        vc = venue_conditions.get(venue, venue_conditions["Neutral / Generic"])
        all_xi = list(set(t1_xi + t2_xi))
        profiles = {}
        for name in all_xi:
            row = df[df["name"]==name]
            if not row.empty:
                row = row.iloc[0]
                profiles[name] = {
                    "bat": build_batter_profile(row, fmt, vc),
                    "bowl": build_bowler_profile(row, fmt, vc),
                }

        sim = simulate_match(t1_xi, t2_xi, profiles, fmt, sims)
        scorecard, voiceover = generate_narrative(sim, t1_name, t2_name, fmt, venue)

    # ---- RESULTS ----
    st.success("✅ Simulation Complete!")

    med = sim["median"]
    winner = t1_name if med["t1_wins"] else t2_name
    margin = f"{med['margin_runs']} runs" if med["t1_wins"] else f"{med['margin_wkts']} wickets"

    st.markdown(f"""
    <div class="score-box">
        <h2 style="color:white;margin:0">{winner} WIN</h2>
        <p style="color:#90EE90;font-size:20px;margin:5px 0">by {margin}</p>
        <p style="color:#ccc;margin:0">{t1_name} {med['t1_score']}/{med['t1_wkts']} vs {t2_name} {med['t2_score']}/{med['t2_wkts']}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{t1_name} win %", f"{sim['t1_win_pct']}%")
        st.metric(f"Avg score", f"{sim['avg_t1']}")
    with col2:
        st.metric(f"{t2_name} win %", f"{sim['t2_win_pct']}%")
        st.metric(f"Avg score", f"{sim['avg_t2']}")

    st.subheader("📋 Full Scorecard")
    st.markdown(f'''<div class="result-box">{scorecard}</div>''', unsafe_allow_html=True)

    st.subheader("🎬 Voiceover Script")
    st.markdown(f'''<div class="voiceover-box">{voiceover}</div>''', unsafe_allow_html=True)

    # Download buttons
    st.download_button(
        "⬇️ Download Full Report",
        data=scorecard + "\n\nVOICEOVER SCRIPT:\n" + voiceover,
        file_name=f"{t1_name}_vs_{t2_name}_{fmt}.txt",
        mime="text/plain"
    )

st.divider()
st.caption("Cricket Match Simulator | Powered by Monte Carlo Simulation | 1,000 iterations")
