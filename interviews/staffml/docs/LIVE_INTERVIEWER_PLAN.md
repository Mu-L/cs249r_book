# Live Interviewer: Detailed Plan

## What This Is

An AI-driven mock interview mode for StaffML where a conversational
interviewer draws from the 10,711-question vault to conduct a realistic
staff-level ML systems interview. The interviewer adapts dynamically:
zooming into weak areas, accelerating through strengths, requesting
napkin math, and asking for system diagrams.

This is a separate mode from Practice (flashcard self-assessment) and
Gauntlet (timed quiz). It lives at `/interview`.

---

## Why It Matters

Peter's feedback crystallized the gap: his team's real interviews are
conversational and unstructured. They flow based on the candidate. They
zoom into blocks, zoom out to system level, and do napkin math together.
No existing mode replicates that.

The question vault has everything needed: 10,711 questions with
scenarios, solutions, napkin math, and rich metadata (zone, bloom level,
competency area, topic). What's missing is an orchestrator that weaves
these into a coherent interview arc.

---

## Goals

### G1. Feel like a real interview, not a quiz

A real staff-level interview is a conversation. The interviewer presents
a scenario, listens, follows up, probes, and transitions. The candidate
should forget they're talking to software.

Concrete requirements:

- The AI paraphrases scenarios naturally (never reads vault text
  verbatim)
- Follow-up questions reference what the candidate just said
- The AI explains acronyms inline when the candidate seems unfamiliar
  (Peter: "we don't expect them to know all acronyms")
- The AI does napkin math *with* the candidate, not just checks their
  number
- Transitions between topics feel motivated ("That memory budget is
  interesting. Let's see what happens when we scale this to a
  multi-node setup...")

### G2. Cover breadth and depth in a single session

Staff interviews assess both. The interviewer should:

- Touch 4-6 competency areas in a 45-minute session
- Go deep on 2-3 (3+ follow-ups in one area)
- Know when to move on (candidate clearly strong or clearly stuck)
- Track coverage and bias toward uncovered areas

Coverage targets per session length:

| Duration | Areas touched | Deep dives | Total scenarios |
|----------|---------------|------------|-----------------|
| 30 min   | 3-4           | 1-2        | 4-6             |
| 45 min   | 4-6           | 2-3        | 6-9             |
| 60 min   | 5-7           | 3-4        | 8-12            |

### G3. Calibrate difficulty dynamically

The interviewer starts at the target level (e.g., L4) and adjusts:

- Strong answer at L4: follow up at L5, then L6+
- Weak answer at L4: zoom in, simplify, try L3 angle
- No answer: give a hint, ask a more focused sub-question

This matches Peter's description: "We focus on system-level impacts,
chain of thought, but of course also napkin math."

### G4. Exercise the full question taxonomy

The vault has 11 zones (diagnosis, fluency, evaluation, recall, analyze,
design, mastery, specification, optimization, implement, realization)
and 6 Bloom levels (remember through create). A good interview mixes
these:

- Open with a scenario that requires diagnosis or design
- Follow up with analysis ("What's the bottleneck?")
- Request napkin math ("Can you estimate the memory footprint?")
- Push to evaluation ("What breaks first at 10x scale?")
- Ask for synthesis ("How would you design a monitoring system for
  this?")

### G5. Produce actionable feedback

The end-of-interview report should tell the candidate:

- Which competency areas are strong vs weak
- Where their napkin math was off and by how much
- Which concepts they should study (linked to specific practice
  questions)
- How their chain-of-thought was (clear reasoning vs jumping to
  answers)

---

## What the Interviewer Needs to Do Well

### 1. Question selection (the conductor function)

The AI does not see all 10,711 questions. The client pre-selects a pool
of ~30 hydrated questions matching the session config (track, level
range, diversity across areas). The AI picks from this pool.

Pool selection strategy (client-side):

1. Filter by track and level range (target level +/- 1)
2. Sample 2-3 questions per competency area for breadth
3. Prefer questions with napkin_math (all have it) and visuals (144 do)
4. Prefer higher Bloom levels (analyze, evaluate, create) for staff
5. Exclude questions the candidate has already practiced (from
   localStorage attempt history)
6. Refresh pool when < 10 unused questions remain

### 2. Conversational flow (the dialogue function)

Each AI turn has an intent. The intents form a grammar:

```
Session = Greeting, Body, Closing
Body    = Topic+
Topic   = Present, Response+, (Transition | End)
Response = FollowUp | Probe | NapkinMath | Diagram | ZoomIn | ZoomOut
```

Intent definitions:

- **greeting**: Ask about background, set the stage
- **present_scenario**: Introduce a new scenario (paraphrased from vault
  question)
- **follow_up**: Build on candidate's answer ("And if we doubled the
  batch size?")
- **probe_weakness**: Target something the candidate was vague about
  ("You mentioned memory-bound. Can you quantify that?")
- **napkin_math**: Request an estimation ("What's the memory footprint
  of the KV cache at 128K context?")
- **diagram_request**: Ask for a system description ("Walk me through
  the data flow from ingestion to serving")
- **zoom_in**: Focus on a component ("Let's focus on just the prefill
  stage")
- **zoom_out**: Expand scope ("Now how does this change across a
  1024-GPU cluster?")
- **transition**: Move to a new competency area with motivation
- **hint**: When candidate is stuck, offer a specific constraint or
  starting point
- **closing**: Summarize, invite questions, end

### 3. Performance evaluation (the assessor function)

The AI silently evaluates against the vault's canonical solution and
napkin math. It never reveals the answer during the interview.

What it tracks per question:

- **approach_quality**: Did they identify the right bottleneck/
  constraint/trade-off?
- **napkin_accuracy**: Was their estimate within an order of magnitude?
  Within 2x?
- **depth**: Did they reason about *why*, not just *what*?
- **breadth**: Did they consider failure modes, operational concerns,
  cost?
- **communication**: Was their reasoning clear and structured?

Rating scale per question: strong / adequate / weak / not assessed

### 4. Acronym awareness

When a candidate says "I'm not sure what that means" or gives a
response that suggests they don't know a term, the interviewer:

- Briefly explains the acronym (sourced from glossary.json)
- Moves on without penalizing
- Notes it as a knowledge gap, not a failure

This directly addresses Peter's feedback about candidates from
different backgrounds.

### 5. Diagram prompts

When the AI asks "Can you describe the architecture?", the candidate
types a text description. The AI evaluates:

- Did they identify the key components?
- Is the data flow correct?
- Did they account for failure/redundancy?

Future: integrate a simple block-diagram canvas (Phase 3+).

---

## Data Model

### InterviewConfig

```typescript
interface InterviewConfig {
  track: string;
  targetLevel: string;        // L4, L5, L6+
  durationMinutes: number;    // 30, 45, 60
  focusAreas?: string[];      // optional competency area filter
  roleDescription?: string;   // optional: "Staff ML Engineer, Edge AI"
}
```

### InterviewSession

```typescript
interface InterviewSession {
  id: string;
  config: InterviewConfig;
  phase: "setup" | "active" | "feedback";
  startedAt: number | null;
  endedAt: number | null;
  transcript: TranscriptEntry[];
  questionsUsed: QuestionUsage[];
  coverageMap: Record<string, AreaCoverage>;
  feedback: InterviewFeedback | null;
}

interface TranscriptEntry {
  id: string;
  role: "interviewer" | "candidate";
  content: string;
  timestamp: number;
  questionRef?: string;       // vault question ID
  intent?: InterviewerIntent;
}

interface QuestionUsage {
  questionId: string;
  area: string;
  topic: string;
  zone: string;
  level: string;
  performance: "strong" | "adequate" | "weak" | "not_assessed";
  napkinAccuracy?: "exact" | "close" | "off" | "way_off";
  notes: string;              // AI's brief assessment
}

interface AreaCoverage {
  area: string;
  questionsAsked: number;
  deepestLevel: string;
  overallRating: "strong" | "adequate" | "weak" | "not_covered";
}
```

### InterviewFeedback

```typescript
interface InterviewFeedback {
  overallAssessment: string;  // 2-3 sentence summary
  rating: "strong" | "hire" | "borderline" | "below";
  areas: AreaScore[];
  strengths: string[];
  improvements: string[];
  recommendations: Recommendation[];
  sessionStats: {
    durationMinutes: number;
    questionsPresented: number;
    areasExplored: number;
    napkinMathAttempts: number;
  };
}

interface AreaScore {
  area: string;
  rating: "strong" | "adequate" | "weak" | "not_covered";
  evidence: string;           // specific example from the session
}

interface Recommendation {
  area: string;
  suggestion: string;
  practiceQuestionIds: string[];
}
```

---

## Architecture

### Client-worker interaction

```
Client (Next.js)                    Worker (Cloudflare)
  |                                   |
  |  1. Hydrate question pool         |
  |     (30 questions via vault API)  |
  |                                   |
  |  2. POST /interview               |
  |     { action: "start",            |
  |       config, questionPool }      |
  |                                   |
  |  <-- { message, intent }          |
  |                                   |
  |  3. POST /interview               |
  |     { action: "respond",          |
  |       candidateMessage,           |
  |       transcript,                 |
  |       questionPool,               |
  |       coverageMap }               |
  |                                   |
  |  <-- { message, intent,           |
  |        questionRef?,              |
  |        performanceNote? }         |
  |                                   |
  |  ... repeat ...                   |
  |                                   |
  |  4. POST /interview               |
  |     { action: "end",              |
  |       transcript,                 |
  |       questionsUsed }             |
  |                                   |
  |  <-- { feedback }                 |
```

The worker is stateless. Every request carries the full context.

### Question pool (client-side selection)

The client manages the pool. Algorithm:

```
1. Filter corpus by track + level range
2. Group by competency_area
3. From each area, pick 2-3 questions:
   - Prefer zones: design, diagnosis, evaluation (over recall, fluency)
   - Prefer higher Bloom: analyze, evaluate, create
   - Prefer questions with visuals
   - Exclude already-practiced question IDs
4. Hydrate selected questions via vault worker (get full scenario,
   solution, napkin_math)
5. Send hydrated pool to interview worker
6. When pool runs low (< 10 unused), fetch replacement batch biased
   toward uncovered areas
```

### Token budget management

A 45-minute interview might produce 40 turns. The transcript grows.

Strategy:
- Send full transcript for first 20 turns
- After 20 turns, summarize turns 1-10 into a 200-word recap, send
  recap + turns 11-current
- Question pool: send title + first 200 chars of scenario + metadata
  (not full details)
- Full question details sent only for the question the AI selected
- Max response tokens: 400 (interviewer turn), 1500 (feedback)

### Model requirements

The conductor prompt is complex (role + structure + evaluation +
conversation style). Minimum model quality:

- **Preferred**: Claude Sonnet, GPT-4o, Gemini Pro, Llama 3.3 70B
- **Acceptable**: GPT-4o-mini, Gemini Flash, Llama 3.1 70B
- **Too small**: Llama 3.1 8B (current Ask Interviewer model)

The existing worker supports multiple providers with fallback. Add a
model tier preference for the interview endpoint.

---

## UI Design

### Setup Phase

```
┌─────────────────────────────────────────────┐
│  Live Interview                             │
│                                             │
│  Track:    [Cloud] [Edge] [Mobile] [TinyML] │
│  Level:    [L4 Staff] [L5 Senior] [L6+ Pr]  │
│  Duration: [30 min] [45 min] [60 min]       │
│                                             │
│  Focus areas (optional):                    │
│  [x] memory  [x] compute  [ ] networking    │
│  [ ] latency [x] deployment [ ] power       │
│                                             │
│  Role description (optional):               │
│  [ Staff ML Engineer, Edge AI for KWS    ]  │
│                                             │
│  [Start Interview]                          │
└─────────────────────────────────────────────┘
```

### Active Phase

```
┌─────────────────────────────────────────────┐
│  Interview in Progress    ██████░░░ 24 min   │
│  Areas: memory ✓  compute ✓  latency ·       │
├─────────────────────────────────────────────┤
│                                             │
│  Interviewer:                               │
│  "Tell me about a system you've worked on   │
│  where memory was the binding constraint."   │
│                                             │
│  You:                                       │
│  "I worked on a serving system for a 70B    │
│  model where the KV cache dominated..."     │
│                                             │
│  Interviewer:                               │
│  "Interesting. Let's dig into that. If       │
│  your context window is 128K tokens, can     │
│  you estimate the KV cache size for that     │
│  70B model on an H100?"                      │
│                                             │
│  You:                                       │
│  [                                        ] │
│  [                    ] [Send] [End Early]   │
│                                             │
│  ┌─ Tools ───────────────────────────────┐  │
│  │ [NapkinCalc] [HardwareRef] [Glossary] │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Feedback Phase

```
┌─────────────────────────────────────────────┐
│  Interview Complete                         │
│                                             │
│  Rating: STRONG                             │
│  "Demonstrated deep systems thinking with    │
│  accurate napkin math and clear trade-off    │
│  analysis across memory and compute."        │
│                                             │
│  ┌─ Competency Coverage ───────────────────┐│
│  │ memory       ████████░░  Strong         ││
│  │ compute      ██████░░░░  Adequate       ││
│  │ latency      █████████░  Strong         ││
│  │ deployment   ░░░░░░░░░░  Not covered    ││
│  │ networking   ███░░░░░░░  Weak           ││
│  └─────────────────────────────────────────┘│
│                                             │
│  Strengths:                                 │
│  • KV cache sizing was exact (within 5%)    │
│  • Strong roofline reasoning                │
│                                             │
│  To improve:                                │
│  • Network topology: confused ring with     │
│    tree AllReduce [Practice: cloud-1234]     │
│  • Power budgeting not covered              │
│    [Practice: cloud-3336, cloud-3337]        │
│                                             │
│  [View Transcript] [New Interview] [Share]   │
└─────────────────────────────────────────────┘
```

---

## System Prompt (Conductor)

The system prompt has five sections. It is parameterized by the session
config and the question pool.

### Section 1: Role

You are a senior staff-level ML systems engineer conducting a technical
interview. You evaluate candidates for {TARGET_LEVEL} {TRACK} ML
engineer roles. Your style is conversational: you flow based on the
candidate's responses, zooming into weak areas and accelerating through
strengths.

{If roleDescription provided}: The candidate is interviewing for:
{roleDescription}.

### Section 2: Interview arc

Opening (2-3 min): Ask about their background. Use their answer to
pick a starting area.

Core (bulk of time): Present scenarios from the question pool. For
each:
- Paraphrase the scenario. Never read vault text verbatim.
- Let them ask clarifying questions. Answer with specific numbers.
- Follow up: "What if we doubled the traffic?" or "Walk me through
  the napkin math."
- Strong answer: zoom out or increase difficulty.
- Weak answer: zoom in, simplify, or offer a hint.

Cross-cutting probes: Weave in estimation, system impact, and
trade-off questions.

Closing (3-5 min): Summarize coverage, ask if they have questions,
end naturally.

### Section 3: Question pool instructions

You have a pool of curated questions with scenarios, solutions, and
napkin math. When presenting a scenario:
- Paraphrase naturally
- Use metadata (zone, area, topic) to track coverage
- After the candidate responds, evaluate silently against the canonical
  solution and napkin math
- Never reveal the canonical answer
- Bias toward uncovered competency areas
- Note: {COVERED_AREAS} have been explored. Prioritize {UNCOVERED}.

### Section 4: Evaluation criteria

Silently track:
- Chain of thought: can they articulate reasoning?
- Napkin math: right order of magnitude?
- System thinking: do they consider failure modes, scale, cost?
- Trade-off analysis: do they weigh alternatives?
- Depth vs breadth: where is expertise deep vs surface?

Signal weak areas by probing deeper. Signal strong areas by moving on.

### Section 5: Conversation style

- Be conversational. Real interviewers adapt.
- When candidates don't know an acronym, explain it briefly and move
  on. Do not penalize.
- Use "we" language: "So if we were deploying this to production..."
- Ask for system descriptions: "Walk me through the architecture."
- Do napkin math together: "Let's estimate that."
- Keep turns concise (under 150 words) except for new scenarios.
- Never reveal the canonical solution.

---

## Implementation Phases

### Phase 1: MVP (target: working end-to-end)

Files to create:
- `src/app/interview/page.tsx` (setup + active + feedback phases)
- `src/lib/interview.ts` (session state, pool selection, transcript
  management)
- `src/lib/interview-prompt.ts` (system prompt builder)

Files to modify:
- `worker/src/index.ts` (add POST /interview endpoint)

What the MVP delivers:
- Setup page with track/level/duration selectors
- Chat interface with scrolling transcript
- AI interviewer that presents scenarios, follows up, and transitions
- Basic feedback page with area ratings and recommendations
- Session persistence in localStorage

What the MVP skips:
- Streaming responses
- Diagram canvas
- Competency radar chart
- Transcript export
- Session comparison

### Phase 2: Polish

- Session timer with visual progress bar
- Inline NapkinCalc and HardwareRef panels (collapsed)
- Transcript context windowing (summarize early turns)
- Pool refresh as questions are used
- Keyboard shortcuts (Enter to send, Esc to end)

### Phase 3: Rich feedback

- Competency coverage visualization (bar chart or radar)
- Performance timeline (how quality evolved over session)
- "Practice these" deep links to practice mode with pre-set filters
- Transcript review with AI annotations per turn
- Transcript export (markdown)

### Phase 4: Future

- Streaming responses (SSE from worker)
- Voice input (Web Speech API)
- Simple diagram canvas (block + arrow drawing)
- Job-description-driven customization (paste a JD, AI tailors
  questions)
- Multi-candidate comparison (interviewer dashboard)
- Collaborative mode (human interviewer + AI observer/coach)

---

## Open Questions

1. **Model cost**: A 45-minute interview with 40 LLM calls at GPT-4o
   rates costs roughly $0.50-1.00. Is that acceptable per session?
   Alternatives: use a smaller model for follow-ups and a larger one
   for scenario selection and feedback.

2. **Rate limiting**: How many free sessions per day? The current Ask
   Interviewer allows 10 clarifications/hour. Interviews are heavier
   (30-40 calls/session). Proposal: 2 sessions/day free, or require
   API key for unlimited.

3. **Diagram interaction**: Text-based diagram description works for
   MVP. When should we add a visual canvas? What's the minimum viable
   diagram tool?

4. **Candidate answer persistence**: Should we store interview
   transcripts for later review? Currently all state is localStorage.
   For cross-device access, would need server-side storage.

5. **Multiplayer**: Peter described interviews where the interviewer
   uses draw.io together with the candidate. Could two users share a
   session (one as interviewer, one as candidate)? This is Phase 4+.
