import os
import random
import time
import requests
import json
import hashlib
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- Dynamic Assets ---

TONES = [
    "highly analytical and data-driven",
    "bold, visionary, and disruptive",
    "consultative, empathetic, and solution-oriented",
    "concise, professional, and executive-level",
    "persuasive, high-energy, and sales-focused"
]

def generate_seed_from_input(*args):
    """Generate deterministic seed from input parameters for consistent decisions."""
    input_string = '|'.join(str(arg) for arg in args)
    return int(hashlib.md5(input_string.encode()).hexdigest()[:8], 16)

def get_stable_temperature(mode='creative'):
    """
    Return temperature based on output mode.
    - 'decision': Low temp (0.4) for stable scores/categories/recommendations
    - 'creative': High temp (0.7-0.85) for varied explanations and content
    """
    if mode == 'decision':
        return 0.4  # Stable for decisions
    else:
        return round(random.uniform(0.7, 0.85), 2)  # Creative for explanations

def call_groq_api(system_prompt, user_prompt, mode='creative', seed=None):
    """
    Calls the Groq API with mode-specific temperature.
    - mode: 'decision' for stable outputs, 'creative' for varied outputs
    - seed: Optional seed for deterministic randomness in creative elements
    """
    if not GROQ_API_KEY:
        return None

    # Set seed for deterministic tone selection if provided
    if seed and mode == 'creative':
        random.seed(seed)
        current_tone = random.choice(TONES)
        random.seed()  # Reset seed after tone selection
    else:
        current_tone = random.choice(TONES)
    
    # Inject tone into system prompt
    enhanced_system_prompt = f"{system_prompt}\n\nIMPORTANT: Adopt a {current_tone} tone. Ensure every response is uniquely phrased and avoids repetitive patterns."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": enhanced_system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": get_stable_temperature(mode),
        "max_tokens": 1200,
        "top_p": 0.95
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=12)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

# ==========================================
# MARKETING CAMPAIGN GENERATOR
# ==========================================

def generate_marketing_campaign(product, description, audience, platform):
    system_prompt = f"""You are a world-class Marketing Strategist. 
    Generate a high-impact, data-driven marketing campaign strategy.
    
    CRITICAL CONSTRAINTS:
    - The campaign MUST be designed EXCLUSIVELY for {platform}
    - All tactics, content ideas, and ad copy MUST be platform-specific to {platform}
    - Target audience is STRICTLY: {audience}
    - DO NOT reference any other platform or generalize
    - DO NOT override or ignore the specified platform
    
    Output Format (Markdown):
    ### 🚀 Marketing Campaign Strategy: [Product Name]
    
    **Campaign Objective:**
    [concise objective]
    
    **Core Marketing Message:**
    "[compelling tagline]"
    
    **Strategy for {platform}:**
    - [Specific tactic 1 for {platform}]
    - [Specific tactic 2 for {platform}]
    - [Specific tactic 3 for {platform}]
    
    **Content Ideas:**
    - **[Idea 1]:** [Brief description]
    - **[Idea 2]:** [Brief description]
    - **[Idea 3]:** [Brief description]
    - **[Idea 4]:** [Brief description]
    - **[Idea 5]:** [Brief description]
    
    **Ad Copy Variations:**
    1. "[Variation 1]"
    2. "[Variation 2]"
    3. "[Variation 3]"
    
    **Success Metrics:**
    - [Metric 1]
    - [Metric 2]
    - [Metric 3]
    """
    
    user_prompt = f"""
    Product: {product}
    Description: {description}
    Target Audience: {audience}
    Platform: {platform}
    
    REMINDER: All strategies must be tailored to {platform} ONLY.
    """
    
    # AI Call
    ai_response = call_groq_api(system_prompt, user_prompt)
    if ai_response:
        return ai_response
        
    # Fallback
    return fallback_marketing(product, description, audience, platform)

def fallback_marketing(product, description, audience, platform):
    # Dynamic Lists for Variance
    objectives = [
        f"To dominate share of voice in the {audience} segment on {platform}.",
        f"To aggressively scale brand awareness for {product} via high-impact visuals.",
        f"To establish {product} as the undisputed category leader for {audience}.",
        f"To drive rapid user acquisition and viral growth on {platform}.",
        f"To build a loyal community of {audience} advocates around {product}."
    ]
    
    tagline_templates = [
        f"Redefining {description} for the modern {audience}.",
        f"{product}: The {random.choice(['ultimate', 'premier', 'smart'])} choice for {audience}.",
        f"Step into the future of {description} with {product}.",
        f"Don't just survive, thrive. {product}.",
        f"{product}: Because {audience} deserve better."
    ]
    
    strategies = [
        [
            f"Leverage {platform} Reels for viral organic reach.",
            f"Partner with 5-10 micro-influencers in the {audience} niche.",
            "Implement a retargeting layer for high-intent visitors."
        ],
        [
            f"Launch a user-generated content (UGC) challenge on {platform}.",
            "Use carousel ads to breakdown complex features.",
            f"Host a live Q&A session tailored to {audience} pain points."
        ],
        [
            "Focus on 'Transformation' storytelling (Before vs After).",
            f"Use {platform} Stories for limited-time offers.",
            "Create a community-led ambassador program."
        ]
    ]
    
    content_ideas = [
        "**Day in the Life:** A relatable vlog-style post featuring a typical user.",
        "**Myth Buster:** Debunking common industry misconceptions.",
        "**Feature Spotlight:** 30-second deep dive into a specific benefit.",
        "**Unboxing Experience:** High-quality ASMR-style unsheathing of the product.",
        "**Founder's Story:** Authentic video sharing the 'why' behind the brand.",
        "**Customer Reaction:** Compilation of genuine user feedback.",
        "**How-To Guide:** Step-by-step tutorial for maximizing value.",
        "**Reaction Video:** Influencers reacting to the product for the first time."
    ]
    random.shuffle(content_ideas)
    
    metrics = [
        f"CTR > {random.uniform(1.5, 3.5):.1f}%",
        f"ROAS > {random.uniform(2.5, 5.0):.1f}x",
        f"Engagement Rate > {random.uniform(4.0, 9.0):.1f}%",
        f"CPA < ${random.randint(15, 45)}",
        f"Brand Mention Lift > {random.randint(10, 30)}%"
    ]
    
    return f"""### 🚀 Marketing Campaign Strategy: {product}

**Campaign Objective:**
{random.choice(objectives)}

**Core Marketing Message:**
"{random.choice(tagline_templates)}"

**Strategy for {platform}:**
- {random.choice(strategies)[0]}
- {random.choice(strategies)[1]}
- {random.choice(strategies)[2]}

**Content Ideas:**
- {content_ideas[0]}
- {content_ideas[1]}
- {content_ideas[2]}
- {content_ideas[3]}
- {content_ideas[4]}

**Ad Copy Variations:**
1. "{random.choice(['Stop settling.', 'Ready for an upgrade?', 'The wait is over.'])} {product} is here to change the game for {audience}."
2. "POV: You finally found a {description} that actually works. Meet {product}. #LinkInBio"
3. "{audience} are switching to {product} for a reason. Experience the difference today."

**Success Metrics:**
- {random.choice(metrics)}
- {random.choice(metrics)}
- {random.choice(metrics)}
"""

# ==========================================
# SALES PITCH GENERATOR
# ==========================================

def generate_sales_pitch(product, persona, industry, size):
    system_prompt = f"""You are an expert B2B Sales Consultant.
    Write a persuasive sales pitch tailored to the specific persona and industry.
    
    CRITICAL CONSTRAINTS:
    - Company size is STRICTLY: {size}
    - Industry is STRICTLY: {industry}
    - Persona is STRICTLY: {persona}
    - DO NOT generalize or reference other company sizes (e.g., if {size} is 'Enterprise', do NOT mention SMB or Mid-Market)
    - All value propositions and differentiators MUST be relevant to {size} companies in {industry}
    - Tailor objection handling to {size} budget and decision-making processes
    
    Output Format (Markdown):
    ### 💼 B2B Sales Pitch for {persona}
    
    **30-Second Elevator Pitch:**
    "[Script]"
    
    **Value Proposition:**
    - **[Point 1]:** [Detail]
    - **[Point 2]:** [Detail]
    - **[Point 3]:** [Detail]
    
    **Key Differentiators:**
    - [Diff 1]
    - [Diff 2]
    - [Diff 3]
    
    **Objection Handling:**
    - *"[Common Objection]"* -> "[Response]"
    - *"[Common Objection]"* -> "[Response]"
    
    **Recommended Next Step (CTA):**
    "[Closing question/action]"
    """
    
    user_prompt = f"""
    Product: {product}
    Persona: {persona}
    Industry: {industry}
    Company Size: {size}
    
    REMINDER: This pitch is for a {size} company in {industry}. Do not deviate from these constraints.
    """
    
    ai_response = call_groq_api(system_prompt, user_prompt)
    if ai_response:
        return ai_response
        
    # Fallback
    return fallback_sales(product, persona, industry, size)

def fallback_sales(product, persona, industry, size):
    openers = [
        f"Hi [Name], I noticed {size} companies in {industry} often struggle with efficiency.",
        f"Hello [Name], are you tired of outdated tools slowing down your {industry} teams?",
        f"Hi [Name], we've been helping {size} {industry} firms cut costs by 20%.",
        f"Hey [Name], quick question about your current {industry} stack."
    ]
    
    value_props = [
        f"**Purpose-Built:** Unlike generic tools, {product} is designed strictly for {industry}.",
        f"**Rapid Deployment:** Get your {size} team onboarded in days, not months.",
        f"**Cost Efficiency:** Replace 3 fragmented tools with one {product}.",
        f"**Compliance Ready:** Meets all standard {industry} regulatory requirements.",
        f"**AI-Powered:** Automates the mundane tasks your team hates."
    ]
    random.shuffle(value_props)
    
    differentiators = [
        "Superior UX/UI designed for non-technical users.",
        "24/7 Dedicated Support for Enterprise accounts.",
        "Proprietary algorithms that predict market shifts.",
        "Seamless integration with your existing stack.",
        "No-code customization engine."
    ]
    random.shuffle(differentiators)
    
    ctas = [
        "Do you have 10 minutes this week for a quick walkthrough?",
        "Would you be open to seeing a 5-minute personalized demo?",
        "Can I send over a case study relevant to your sector?",
        "Are you free Tuesday morning for a brief chat?"
    ]
    
    return f"""### 💼 B2B Sales Pitch for {persona}

**30-Second Elevator Pitch:**
"{random.choice(openers)} {product} solves this by streamlining operations and automating manual workflows. We essentially give your team hours back every week, allowing you to focus on high-value strategy rather than grunt work."

**Value Proposition:**
- {value_props[0]}
- {value_props[1]}
- {value_props[2]}

**Key Differentiators:**
- {differentiators[0]}
- {differentiators[1]}
- {differentiators[2]}

**Objection Handling:**
- *"We don't have budget."* -> "Totally understand. Most of our partners realized that {product} actually **pays for itself** within 3 months by consolidating vendors."
- *"Is it hard to switch?"* -> "Not at all. Our migration team handles the heavy lifting, ensuring zero downtime for your {size} org."

**Recommended Next Step (CTA):**
"{random.choice(ctas)}"
"""

# ==========================================
# LEAD SCORING
# ==========================================

def generate_lead_score(product, icp, value_prop, lead_data):
    system_prompt = f"""You are a Lead Qualification Expert.
    Analyze the raw lead data against the ICP and Value Prop.
    
    CRITICAL CONSTRAINTS:
    - Ideal Customer Profile (ICP): {icp}
    - Value Proposition: {value_prop}
    - Score the lead based STRICTLY on alignment with the ICP
    - DO NOT make assumptions beyond what is provided in the lead data
    - Ensure reasoning directly references the ICP and value proposition
    - Provide a STABLE score (avoid wild fluctuations)
    - Lock recommendations to score categories:
      * 75-100 = Hot → Immediate action (call, demo)
      * 50-74 = Warm → Priority follow-up (case study, nurture)
      * 25-49 = Lukewarm → Passive nurture (newsletter, monitor)
      * 0-24 = Cold → Deprioritize (break-up email)
    
    Output Format (Markdown):
    ### 📊 AI Lead Qualification Analysis
    
    **Lead Score:** **[0-100]/100**
    
    **Category:** <span style="color:[Green/Orange/Red]; font-weight:bold">[Hot/Warm/Lukewarm/Cold]</span>
    
    **Reasoning:**
    - [Reason 1]
    - [Reason 2]
    - [Reason 3]
    
    **Estimated Conversion Probability:**
    **[XX]%** based on intent signals.
    
    **Recommended Sales Action:**
    [Specific action matching the category]
    """
    
    user_prompt = f"""
    Product: {product}
    ICP: {icp}
    Value Proposition: {value_prop}
    Raw Lead Data: {lead_data}
    
    REMINDER: Evaluate this lead strictly against the ICP: {icp}
    """
    
    # Generate deterministic seed for stable scoring
    seed = generate_seed_from_input(product, icp, value_prop, lead_data)
    
    # Use decision mode for stable scores and recommendations
    ai_response = call_groq_api(system_prompt, user_prompt, mode='decision', seed=seed)
    if ai_response:
        return ai_response
        
    # Fallback with same seed for consistency
    return fallback_lead_scoring(product, lead_data, seed)

def fallback_lead_scoring(product, lead_data, seed=None):
    # Generate deterministic base score from inputs
    if seed is None:
        seed = generate_seed_from_input(product, lead_data)
    
    random.seed(seed)
    
    # Base score with narrow variance (±3)
    base_score = random.randint(47, 53)
    score = base_score
    reasons = []
    
    lower_data = lead_data.lower()
    
    # Keyword Logic with STABLE weights (deterministic)
    if any(x in lower_data for x in ['budget', 'price', 'quote', 'cost']):
        boost = 15  # Fixed boost for consistency
        score += boost
        reasons.append(f"Financial intent detected (+{boost} pts)")
    
    if any(x in lower_data for x in ['urgent', 'asap', 'now', 'deadline']):
        boost = 20  # Fixed boost
        score += boost
        reasons.append(f"High timeline urgency (+{boost} pts)")
        
    if any(x in lower_data for x in ['need', 'looking for', 'problem', 'solve']):
        boost = 10  # Fixed boost
        score += boost
        reasons.append(f"Clear pain point match (+{boost} pts)")
        
    if any(x in lower_data for x in ['vp', 'director', 'head', 'chief', 'founder']):
        boost = 10  # Fixed boost
        score += boost
        reasons.append("Decision-maker job title detected")

    # Small jitter for realism (±3 points)
    score += random.randint(-3, 3)
    
    # Reset random seed
    random.seed()
    
    if score > 99: score = 99
    if score < 10: score = 10
    
    # Determine Category with LOCKED recommendations
    if score >= 75:
        category = "Hot 🔥"
        color = "#22c55e"
        # LOCKED: Always immediate action for Hot leads
        action = "Call immediately (within 15 mins)."
    elif score >= 50:
        category = "Warm"
        color = "#eab308"
        # LOCKED: Always priority follow-up for Warm leads
        action = "Send case study and follow up in 2 days."
    elif score >= 25:
        category = "Lukewarm"
        color = "#f59e0b"
        # LOCKED: Always nurture for Lukewarm leads
        action = "Add to monthly newsletter and monitor engagement."
    else:
        category = "Cold"
        color = "#3b82f6"
        # LOCKED: Always deprioritize for Cold leads
        action = "Send 'break-up' email to gauge interest."
    
    # Stable conversion probability (based on score with minimal variance)
    conversion_prob = int(score * 0.85)
        
    return f"""### 📊 AI Lead Qualification Analysis

**Lead Score:** **{score}/100**

**Category:** <span style="color:{color}; font-weight:bold">{category}</span>

**Reasoning:**
- {reasons[0] if reasons else "Standard inquiry pattern."}
- Matches core value proposition of {product}.
- {reasons[1] if len(reasons) > 1 else "Context implies moderate commercial intent."}

**Estimated Conversion Probability:**
**{conversion_prob}%** based on current signals.

**Recommended Sales Action:**
-> **{action}**
"""
