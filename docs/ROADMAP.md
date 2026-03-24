# A3: AI Assembly Assistant - 14-Week Roadmap

## Phase 0: Foundation Setup (Week 1) - COMPLETED
- [x] Python environment & core dependencies (OpenCV, LiteLLM, Torch)
- [x] GPU Validation (NVIDIA RTX 4050)
- [x] Local Inference Server (LM Studio)
- [x] Camera input pipeline verification

## Phase 1: Local Vision & Frame Logic (Weeks 2-3) - COMPLETED
- [x] Steady-Frame Detection (SFD)
- [x] Frame preprocessing (resizing, normalization)
- [ ] Final-Frame Validation (Motion check before speaking)
- [ ] Privacy Blurring for Cloud transmission (ROI/Face)

## Phase 2: Local Inference & Resilience (Weeks 4-5) - IN PROGRESS
- [x] Qwen3-VL-4B (4-bit quantized) integration via LiteLLM/LM Studio
- [x] Predictive Memory Monitoring (RTX 4050 protection)
- [x] Hybrid Failover Router (Local ⟷ Gemini 3 Flash)
- [x] Interactive Voice Control (v0.1 - "Next", "Repeat")
- [x] "Thinking" Pulse (UX feedback during inference)
- [ ] Session Replay Dashboard (Visual debug UI)
- [ ] Interruptible TTS (Ducking during user speech)

## Phase 3: Multimodal RAG & Knowledge Base (Weeks 6-7)
- [ ] Structured assembly manual parsing (PDF/Image)
- [ ] Vector database setup for RAG
- [ ] Context-aware prompt engineering for guidance

## Phase 4: Production (Gemini) Integration (Weeks 8-9)
- [ ] Gemini 3 Flash Multimodal Live API integration
- [ ] Cloud-side streaming and inference pipeline
- [ ] Hybrid architecture switching (Local vs. Cloud)

## Phase 5: Voice Interaction & UI (Weeks 10-11)
- [ ] Real-time Text-to-Speech (TTS) and Speech-to-Text (STT)
- [ ] Frontend interface for visual feedback and guidance
- [ ] Hands-free control commands

## Phase 6: Optimization & Polish (Weeks 12-14)
- [ ] System-wide latency reduction
- [ ] Edge case handling (lighting, camera angles, assembly errors)
- [ ] Final production-ready deployment and testing
