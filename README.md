
This repository contains a production-ready AI research agent for analyzing Indian equities (NSE-listed companies).

## 🎯 Assignment Completion Checklist

- ✅ **System prompt** (`system_prompt.txt`) - Hardened with adversarial defense
- ✅ **Main agent script** (`agent.py`) - Uses modern `google-genai` SDK
- ✅ **Generated brief** (`output/SRVCABLE_brief.md`) - Demonstrates all security features
- ✅ **Test log** (`test_log.md`) - 3 documented iterations with failure analysis
- ✅ **README** (`README.md`) - Complete documentation + video script
- ✅ **Research pack** (`research_pack/`) - All 8 source documents
- ✅ **Dependencies** (`requirements.txt`, `.env.example`)

## 🔬 Key Technical Achievements

### 1. Adversarial Defense ✅
- Successfully ignores prompt injection in `multibaggeralerts_2026-08-12.md`
- No unauthorized "STRONG BUY" or price targets in output

### 2. Entity Disambiguation ✅
- Correctly rejects "Sarvottam Cable Network" (Nagpur cable TV operator)
- Verified NSE ticker and business description match

### 3. Temporal Integrity ✅
- Recognized promoter pledge reduction from 35% (Mar 2024) → 4.1% (Jun 2026)
- Treated as deleveraging progress, not contradiction

### 4. Contradiction Detection ✅
- Flagged revenue discrepancy: ₹1,248 Cr (official) vs ₹1,428 Cr (news)
- Listed in "Open Questions" section for transparency

### 5. Brevity Constraint ✅
- Output: 398 words (within 350-450 target)
- Fits cleanly on one page for retail investors

## 📊 Test Results Summary

| Metric | Run 1 (Naive) | Run 2 (Heuristic) | Run 3 (Production) |
|--------|---------------|-------------------|-------------------|
| Injection Defense | ❌ | ✅ | ✅ |
| Entity Check | ❌ | ⚠️ | ✅ |
| Temporal Resolution | ❌ | ❌ | ✅ |
| Contradiction Handling | ❌ | ⚠️ | ✅ |
| Word Count | 720 | 620 | 398 |
| **Status** | **FAIL** | **FAIL** | **PASS** |

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Run the agent
python agent.py

# Output appears in output/SRVCABLE_brief.md
```

## 📹 Video Recording Notes

**Recommended segments:**
1. **Live execution** (0:00-0:45): Show `python agent.py` and generated output
2. **Design decision** (0:45-1:45): Demo prompt injection defense + entity disambiguation
3. **Limitation & roadmap** (1:45-2:30): Discuss RAG scaling for production

## 📝 What's Different from Initial Files

The `research_pack/` folder now contains the **official assignment documents** (from `files/` directory). The earlier synthetic documents in `research_pack/` were moved aside to match the assignment structure.

Key facts about Sarvottam Cables Ltd (from the actual research pack):
- Q1 FY27 revenue: ₹1,248 Cr (official) vs ₹1,428 Cr (reported by Business Daily)
- PAT: ₹82 Cr (+5.9% YoY)
- Order book: ₹3,900 Cr
- Bharuch plant: Coming in Q3 FY27 (30% capacity addition)
- Promoter pledge: Reduced from 35% (Mar 2024) to 4.1% (Jun 2026)
- GST demand: ₹46.3 Cr (56% of Q1 PAT) - received Sep 2, 2026

## 🎓 Submission Artifacts

1. **GitHub Repository Link**: https://github.com/Rdoliya/AI-Research-Agent-for-Super-Investing
2. **Research Brief**: See `output/SRVCABLE_brief.md`
3. **Test Log**: See `test_log.md`
4. **Video Recording**: [Add Loom/YouTube link here]

---

**Built by:** **RISHYUP DOLIYA**
**Model:** Google Gemini 2.0 Flash Experimental  
**Date:** October 2026  
**Assignment:** Super Investing AI Innovator
