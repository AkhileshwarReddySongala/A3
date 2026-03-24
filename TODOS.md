# A3: Project TODOs

## P1: High Priority (Assembly Critical)
- [ ] **Background Noise Calibration:** Implement noise filtering for the voice interruption logic (to ignore printer fans, background tools).
- [ ] **Final-Frame Validation:** Add final motion check immediately before TTS starts to prevent stale advice.

## P2: System Resilience
- [ ] **Offline Safety Mode:** Static fallback instructions for when both Local and Cloud inference are unavailable.
- [ ] **Predictive Memory Monitor:** Pre-emptive routing based on RTX 4050 VRAM usage.

## P3: Polish & UX
- [ ] **Session Replay Dashboard:** Simple local UI to review VLM frames and AI reasoning history.
- [ ] **"Thinking" Pulse:** Breathing light/soft audio cue during inference latency.
