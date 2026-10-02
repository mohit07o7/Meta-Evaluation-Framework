#  Meta-Evaluation Framework for LLMs

A research-grade AI benchmarking and stress-testing system designed to evaluate Large Language Model (LLM) outputs using semantic understanding and data-driven "Meta-Evaluation" techniques.

---

##  Key Framework Upgrades 

###  Upgrade 1: Learning to Rank (AIML Core)
Replaced arbitrary heuristic weights with a **Ridge Regression model** trained on human preference datasets (Achieved **R²=0.89** in cross-validation). The aggregator now learns how highly a human would value Relevance vs. Quality vs. Bias.

###  Upgrade 2: RAG (Retrieval-Augmented Generation) Evaluation
Industry-relevant support for context-aware pipelines. Includes:
- **Faithfulness (Hallucination Detector)**: Uses NLI (DeBERTa-v3-small) to verify if model claims are grounded in provided context.
- **Answer Relevance**: Detects "context-echoing" vs genuine answering using prompt-response similarity vs context-response similarity.

###  Upgrade 3: Batch Processing & Analytics Pipeline
Scalable software engineering for large-scale benchmarks:
- **Async Execution**: Multi-threaded processing of thousands of prompts using `ThreadPoolExecutor`.
- **Statistical Dashboard**: Rich Streamlit visualisations including Radar Charts, Score Heatmaps, and Distribution Box Plots.

---

## Project Structure

```text
metaevalai/
├── modules/
│   ├── relevance.py     # SentenceTransformers (all-MiniLM-L6-v2)
│   ├── quality.py       # Rule-based + Structural analysis (JSON/Markdown)
│   ├── bias.py          # Toxicity detection (toxic-bert)
│   ├── consistency.py   # NLI Contradiction (DeBERTa-v3-small)
│   ├── faithfulness.py  # RAG Hallucination detection
│   ├── red_team.py      # Adversarial prompts & validation
│   └── llm_providers.py # Live model integration (Ollama/OpenAI/Gemini)
├── data/
│   ├── labeled_dataset.csv # Used for weight training
│   └── batch_sample.csv    # Sample benchmarking file
├── models/
│   └── learned_weights.json # Output of Ridge regression
├── tests/               # 54+ Unit tests (98% logic coverage)
├── app.py               # Streamlit Dashboard (Full UI)
├── main.py              # CLI Entry point
└── train_weights.py     # Training script for Upgrade 1
```

##  Getting Started

1. **Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run Interactive Dashboard**:
   ```bash
   streamlit run app.py
   ```
3. **Run Batch Benchmarking**:
   ```bash
   python batch_runner.py --file data/batch_sample.csv
   ```

---

##  Methodology Brief
- **"The Ground Truth"**: In RAG mode, the *Context* provided by the user is the truth. In standard mode, the framework uses **Cross-Model Consistency** (Consensus) to determine factual reliability between Model A, B, and C outputs.
- **Inference Models**:
  - `all-MiniLM-L6-v2` for embeddings.
  - `DeBERTa-v3-small` for NLI tasks.
  - `toxic-bert` for safety guardrails.
