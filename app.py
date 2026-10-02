"""
Meta-Evaluation Framework — Streamlit Dashboard
=================================================
Interactive web UI for evaluating and comparing AI model outputs.

Pages:
  - Single Evaluation: Standard & RAG evaluation of individual prompts
  - Batch Analytics:   Upload CSV/JSON, process N prompts, statistical dashboard

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from modules.relevance import RelevanceAnalyzer
from modules.quality import QualityAnalyzer
from modules.bias import BiasDetector
from modules.consistency import ConsistencyAnalyzer
from modules.aggregator import ScoreAggregator
from modules.faithfulness import FaithfulnessChecker
from modules.answer_relevance import AnswerRelevanceChecker
from modules.llm_providers import PROVIDER_REGISTRY, create_provider


# ─────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Meta-Evaluation Framework",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.score-high { color: #00d4aa; font-weight: 600; }
.score-mid { color: #ffd93d; font-weight: 600; }
.score-low { color: #ff6b6b; font-weight: 600; }

.rag-badge {
    background: #667eea; color: white; border-radius: 4px;
    padding: 4px 12px; font-size: 0.8em; font-weight: 500;
}

.batch-badge {
    background: #f093fb; color: white; border-radius: 4px;
    padding: 4px 12px; font-size: 0.8em; font-weight: 500;
}

.stat-card {
    background: #1a1a2e; padding: 1.5rem; border-radius: 8px;
    border: 1px solid #2a2a4e; text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────
# Cached model loaders
# ─────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading evaluation models...")
def load_standard_models():
    relevance   = RelevanceAnalyzer()
    quality     = QualityAnalyzer()
    bias        = BiasDetector()
    consistency = ConsistencyAnalyzer()
    return relevance, quality, bias, consistency


@st.cache_resource(show_spinner="Loading RAG models...")
def load_rag_models():
    relevance, quality, bias, consistency = load_standard_models()
    faithfulness    = FaithfulnessChecker(
        shared_model=consistency.model,
        shared_tokenizer=consistency.tokenizer,
    )
    answer_relevance = AnswerRelevanceChecker(shared_model=relevance.model)
    return relevance, quality, bias, consistency, faithfulness, answer_relevance


# ─────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────

def score_emoji(score: float) -> str:
    return "●" if score >= 0.7 else "●" if score >= 0.4 else "●"


def explain_dimension(dim: str, score: float) -> str:
    explanations = {
        "relevance":        {True: "Highly relevant to the prompt",           False: "Partially or not relevant"},
        "quality":          {True: "Well-structured with diverse vocabulary",  False: "Too short, repetitive, or poor"},
        "bias":             {True: "Clean and free from toxic content",        False: "Contains harmful or biased content"},
        "consistency":      {True: "Logically consistent",                    False: "Contains logical contradictions"},
        "faithfulness":     {True: "Grounded in context (no hallucination)",  False: "Claims not supported by context"},
        "answer_relevance": {True: "Directly answers the prompt",             False: "Summarising context, not answering"},
    }
    return explanations.get(dim, {}).get(score >= 0.7, "")


def create_radar_chart(results: list[dict], rag_mode: bool = False) -> plt.Figure:
    if rag_mode:
        dimensions = ["relevance", "quality", "bias", "consistency", "faithfulness", "answer_relevance"]
        labels     = ["Relevance", "Quality", "Bias", "Consistency", "Faithfulness", "Answer\nRelevance"]
    else:
        dimensions = ["relevance", "quality", "bias", "consistency"]
        labels     = ["Relevance", "Quality", "Bias", "Consistency"]

    colors = ["#00d4aa", "#ff6b6b", "#ffd93d", "#6bcbff", "#c084fc"]
    n      = len(dimensions)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    for i, result in enumerate(results):
        values = [result.get(d, 0) or 0 for d in dimensions]
        values += values[:1]
        color = colors[i % len(colors)]
        ax.plot(angles, values, "o-", linewidth=2.5, label=result["model"], color=color)
        ax.fill(angles, values, alpha=0.08, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, fontweight="500", color="white")
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8, color="#aaa")
    ax.yaxis.grid(True, color="#2a2a4e", alpha=0.5, linewidth=0.8)
    ax.xaxis.grid(True, color="#2a2a4e", alpha=0.5, linewidth=0.8)
    ax.spines["polar"].set_color("#2a2a4e")
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=10,
              facecolor="#0e1117", edgecolor="#2a2a4e", labelcolor="white")
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────
# Page 1: Single Evaluation
# ─────────────────────────────────────────────────────────────────────────

def page_single_eval():
    st.subheader("Single Prompt Evaluation")

    # Sidebar config
    with st.sidebar:
        st.header("Configuration")

        rag_mode = st.toggle("RAG Evaluation Mode", value=False,
                             help="Enable to add Faithfulness and Answer Relevance dimensions.")
        if rag_mode:
            st.markdown('<span class="rag-badge">RAG MODE</span>', unsafe_allow_html=True)
            st.caption("6 dimensions active")
        else:
            st.caption("4 dimensions active")

        st.divider()
        weight_mode = st.radio(
            "Weight Mode",
            ["Static (Manual)", "Learned (Trained)"],
            disabled=rag_mode,
        )
        use_learned = (weight_mode == "Learned (Trained)") and not rag_mode
        if use_learned and not os.path.exists("models/learned_weights.json"):
            st.warning("No learned weights found.")
            use_learned = False

        st.subheader("Weights")
        try:
            agg = ScoreAggregator(use_learned=use_learned)
        except FileNotFoundError:
            agg = ScoreAggregator()
        weights = agg.get_weights(rag_mode=rag_mode)
        for dim, w in weights.items():
            st.progress(w, text=f"{dim.replace('_',' ').capitalize()}: {w:.1%}")

    # --- State init for auto-generation ---
    if "auto_a" not in st.session_state: st.session_state["auto_a"] = "Machine learning is a branch of artificial intelligence where computers learn patterns from data instead of being explicitly programmed. For example, a spam filter learns to identify junk emails by analyzing thousands of examples."
    if "auto_b" not in st.session_state: st.session_state["auto_b"] = "ML is computer learn data computer learn data computer. Machine learning data computer learning."
    if "auto_c" not in st.session_state: st.session_state["auto_c"] = "Machine learning is a fascinating technology. It allows systems to learn from experience. However, machine learning is completely useless and does not work."
    if "prompt_input" not in st.session_state: st.session_state["prompt_input"] = "Explain machine learning in simple terms."
    if "context_input" not in st.session_state: st.session_state["context_input"] = "Machine learning is a branch of artificial intelligence that focuses on the development of algorithms and statistical models that enable computers to learn from and make predictions based on data, without being explicitly programmed."

    # --- Offline Data Loader ---
    st.markdown("### Load Sample Dataset")
    with st.expander("Load pre-computed model outputs from CSV"):
        try:
            sample_df = pd.read_csv("data/batch_sample.csv")
            unique_prompts = sample_df["prompt"].unique().tolist()
            selected_prompt = st.selectbox("Select a prompt:", ["-- Select --"] + unique_prompts)
            
            if st.button("Load", type="primary", use_container_width=True):
                if selected_prompt != "-- Select --":
                    subset = sample_df[sample_df["prompt"] == selected_prompt]
                    st.session_state["prompt_input"] = selected_prompt
                    
                    if "context" in subset.columns and pd.notna(subset.iloc[0]["context"]):
                        st.session_state["context_input"] = str(subset.iloc[0]["context"])
                    else:
                        st.session_state["context_input"] = ""
                    
                    # Fetch models and responses
                    responses = subset.to_dict('records')
                    st.session_state["auto_a"] = responses[0]["response"] if len(responses) > 0 else ""
                    st.session_state["auto_b"] = responses[1]["response"] if len(responses) > 1 else ""
                    st.session_state["auto_c"] = responses[2]["response"] if len(responses) > 2 else ""
                    st.rerun()
        except Exception:
            st.info("No sample dataset available.", icon="ℹ️")

    # --- Inputs ---
    st.markdown("### Input")
    prompt = st.text_area("Prompt", key="prompt_input", height=80)

    context = None
    if rag_mode:
        st.info("Provide the context the model used.", icon="ℹ️")
        context = st.text_area(
            "Retrieved Context",
            key="context_input",
            height=100,
        )

    st.markdown("### Generate Responses")
    with st.expander("Connect to Live Models (OpenAI, Gemini, Ollama)", expanded=False):
        c1, c2, c3 = st.columns(3)
        
        provider_names = list(PROVIDER_REGISTRY.keys())
        
        # Define 10+ models for the dropdowns
        model_options = {
            "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "gemini": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-lite"],
            "ollama": ["llama3", "mistral", "gemma", "phi3", "qwen", "llama2"],
            "none": ["none"]
        }

        with c1:
            p_a = st.selectbox("API Provider A", ["none"] + provider_names, index=1)
            m_a = st.selectbox("Target Model A", model_options.get(p_a, ["none"]), key="ma")
            k_a = st.text_input("API Key A (if needed)", type="password", key="ka") if p_a not in ["none", "ollama"] else ""
        with c2:
            p_b = st.selectbox("API Provider B", ["none"] + provider_names, index=2)
            m_b = st.selectbox("Target Model B", model_options.get(p_b, ["none"]), key="mb")
            k_b = st.text_input("API Key B (if needed)", type="password", key="kb") if p_b not in ["none", "ollama"] else ""
        with c3:
            p_c = st.selectbox("API Provider C", ["none"] + provider_names, index=3)
            m_c = st.selectbox("Target Model C", model_options.get(p_c, ["none"]), key="mc")
            k_c = st.text_input("API Key C (if needed)", type="password", key="kc") if p_c not in ["none", "ollama"] else ""

        if st.button("Auto-Generate text for A, B, and C", type="primary"):
            full_prompt = f"Context: {context}\n\nPrompt: {prompt}" if (rag_mode and context) else prompt
            with st.spinner("Generating responses..."):
                try:
                    if p_a != "none":
                        prov_a = create_provider(p_a, m_a, k_a)
                        st.session_state["auto_a"] = prov_a.generate(full_prompt)["response"]
                    if p_b != "none":
                        prov_b = create_provider(p_b, m_b, k_b)
                        st.session_state["auto_b"] = prov_b.generate(full_prompt)["response"]
                    if p_c != "none":
                        prov_c = create_provider(p_c, m_c, k_c)
                        st.session_state["auto_c"] = prov_c.generate(full_prompt)["response"]
                    st.success("Successfully generated responses!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Generation failed: {e}")

    st.markdown("**Model Responses:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        model_a_name = st.text_input("Model A Name", value="OpenAI", label_visibility="collapsed")
        model_a_resp = st.text_area("Model A Response", key="auto_a", height=150, label_visibility="collapsed")
    with col2:
        model_b_name = st.text_input("Model B Name", value="Gemini", label_visibility="collapsed")
        model_b_resp = st.text_area("Model B Response", key="auto_b", height=150, label_visibility="collapsed")
    with col3:
        model_c_name = st.text_input("Model C Name", value="Ollama", label_visibility="collapsed")
        model_c_resp = st.text_area("Model C Response", key="auto_c", height=150, label_visibility="collapsed")

    btn_label = "Evaluate (RAG)" if rag_mode else "Evaluate"
    if st.button(btn_label, type="primary", use_container_width=True):
        responses = {}
        if model_a_resp.strip(): responses[model_a_name] = model_a_resp
        if model_b_resp.strip(): responses[model_b_name] = model_b_resp
        if model_c_resp.strip(): responses[model_c_name] = model_c_resp

        if len(responses) < 2:
            st.error("Please provide at least 2 model responses.")
            return

        if rag_mode:
            relevance, quality, bias, consistency, faithfulness_checker, answer_relevance_checker = load_rag_models()
        else:
            relevance, quality, bias, consistency = load_standard_models()

        aggregator = ScoreAggregator(use_learned=use_learned)
        results = []
        model_names = list(responses.keys())
        progress = st.progress(0, text="Evaluating models...")

        for idx, (model_name, response) in enumerate(responses.items()):
            progress.progress(idx / len(responses), text=f"Evaluating {model_name}...")
            r_score = relevance.compute_score(prompt, response)
            q_score = quality.compute_score(response)
            b_score = bias.compute_score(response)
            other_responses = [responses[m] for m in model_names if m != model_name]
            c_result = consistency.compute_score(response, other_responses)
            c_score = c_result["combined"]

            f_score = ar_score = None
            f_result = ar_result = None
            if rag_mode and context and context.strip():
                f_result  = faithfulness_checker.compute_score(context, response)
                f_score   = f_result["score"] if f_result["score"] is not None else 1.0
                ar_result = answer_relevance_checker.compute_score(prompt, response, context)
                ar_score  = ar_result["score"]

            final_score = aggregator.compute_final(r_score, q_score, b_score, c_score, faithfulness=f_score, answer_relevance=ar_score)

            result_dict = {
                "model": model_name, "relevance": round(r_score, 4), "quality": round(q_score, 4),
                "bias": round(b_score, 4), "consistency": round(c_score, 4), "final_score": round(final_score, 4),
            }
            if rag_mode and f_score is not None:
                result_dict.update({"faithfulness": round(f_score, 4), "answer_relevance": round(ar_score, 4),
                                    "_f_result": f_result, "_ar_result": ar_result})
            results.append(result_dict)

        results = sorted(results, key=lambda x: x["final_score"], reverse=True)
        progress.progress(1.0, text="Done!")
        time.sleep(0.3)
        progress.empty()

        # --- Results display ---
        st.markdown("### Results")
        medals = ["🥇", "🥈", "🥉"]
        cols = st.columns(len(results))
        standard_dims = ["relevance", "quality", "bias", "consistency"]
        rag_dims = ["faithfulness", "answer_relevance"]

        for i, (col, r) in enumerate(zip(cols, results)):
            with col:
                medal = medals[i] if i < len(medals) else f"#{i+1}"
                st.markdown(f"#### {medal} {r['model']}")
                st.metric("Score", f"{r['final_score']:.3f}")
                st.markdown("**Dimensions:**")
                for dim in standard_dims:
                    st.markdown(f"{score_emoji(r[dim])} {dim.capitalize()}: `{r[dim]:.3f}`")
                if rag_mode and "faithfulness" in r:
                    st.markdown("**RAG:**")
                    for dim in rag_dims:
                        s = r.get(dim, 0)
                        st.markdown(f"{score_emoji(s)} {dim.replace('_',' ').capitalize()}: `{s:.3f}`")

        st.markdown("### Comparison")
        chart_col, table_col = st.columns(2)
        with chart_col:
            fig = create_radar_chart(results, rag_mode=rag_mode)
            st.pyplot(fig)
            plt.close(fig)
        with table_col:
            display_cols = ["model"] + standard_dims + ([d for d in rag_dims if d in results[0]] if rag_mode else []) + ["final_score"]
            df = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in results])
            df.insert(0, "Rank", range(1, len(df) + 1))
            st.dataframe(df[[c for c in ["Rank"] + display_cols if c in df.columns]], use_container_width=True, hide_index=True)

        if rag_mode:
            st.markdown("### Hallucination Analysis")
            for r in results:
                f_res = r.get("_f_result")
                if not f_res or not f_res.get("claim_details"):
                    continue
                with st.expander(f"{r['model']} — Faithfulness: {r.get('faithfulness','N/A')}"):
                    for detail in f_res["claim_details"]:
                        label = detail["label"].upper()
                        st.markdown(f"**{label}** — \"{detail['claim']}\"")


# ─────────────────────────────────────────────────────────────────────────
# Page 2: Batch Analytics
# ─────────────────────────────────────────────────────────────────────────

def page_batch_analytics():
    st.subheader("Batch Analytics Pipeline")

    with st.sidebar:
        st.header("Batch Configuration")
        st.markdown('<span class="batch-badge">BATCH MODE</span>', unsafe_allow_html=True)
        st.caption("Upload a CSV/JSON dataset for evaluation")
        st.divider()
        st.markdown("""
**Required columns:**
- `prompt` — the question
- `model` — model name
- `response` — model output

**Optional:**
- `context` — enables RAG evaluation
        """)
        st.divider()

        # Load sample
        if st.button("Load Sample", use_container_width=True):
            sample_path = "data/batch_sample.csv"
            if os.path.exists(sample_path):
                st.session_state["batch_df"] = pd.read_csv(sample_path)
                st.success("✓ Loaded sample")
            else:
                st.error("Sample not found")

    # --- File upload ---
    uploaded = st.file_uploader(
        "Upload dataset (.csv or .json)",
        type=["csv", "json"],
        help="Required: prompt, model, response columns. Optional: context column.",
    )

    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            st.session_state["batch_df"] = pd.read_csv(uploaded)
        else:
            st.session_state["batch_df"] = pd.read_json(uploaded)

    if "batch_df" not in st.session_state:
        st.info("Upload a file or load sample to begin", icon="ℹ️")
        return

    df = st.session_state["batch_df"]
    required = ["prompt", "model", "response"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {', '.join(missing)}")
        return

    has_context = "context" in df.columns and df["context"].notna().any()

    # --- Dataset preview ---
    st.markdown("### Dataset")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", len(df))
    col2.metric("Models", df["model"].nunique())
    col3.metric("Prompts", df["prompt"].nunique())

    if has_context:
        st.success("✓ Context detected — RAG evaluation enabled")

    with st.expander("Preview data"):
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    # --- Run batch ---
    if st.button("Run Evaluation", type="primary", use_container_width=True):
        relevance, quality, bias, consistency = load_standard_models()
        faith_checker = ar_checker = None
        if has_context:
            _, _, _, _, faith_checker, ar_checker = load_rag_models()

        aggregator = ScoreAggregator()
        all_results = []
        total = len(df)
        progress = st.progress(0, text="Processing batch...")

        grouped = df.groupby("prompt")
        completed = 0

        for prompt_text, group_df in grouped:
            all_responses = group_df["response"].tolist()

            for _, row in group_df.iterrows():
                response = str(row["response"])
                r_score = relevance.compute_score(str(row["prompt"]), response)
                q_score = quality.compute_score(response)
                b_score = bias.compute_score(response)
                other = [r for r in all_responses if r != response]
                c_result = consistency.compute_score(response, other if other else None)
                c_score = c_result["combined"]

                f_score = ar_score = None
                ctx = str(row.get("context", "")) if row.get("context") and pd.notna(row.get("context")) else None
                if has_context and ctx and ctx.strip() and faith_checker and ar_checker:
                    f_res = faith_checker.compute_score(ctx, response)
                    f_score = f_res["score"] if f_res["score"] is not None else 1.0
                    ar_res = ar_checker.compute_score(str(row["prompt"]), response, ctx)
                    ar_score = ar_res["score"]

                final = aggregator.compute_final(r_score, q_score, b_score, c_score, faithfulness=f_score, answer_relevance=ar_score)

                result = {
                    "prompt": str(row["prompt"]), "model": str(row["model"]),
                    "relevance": round(r_score, 4), "quality": round(q_score, 4),
                    "bias": round(b_score, 4), "consistency": round(c_score, 4),
                    "final_score": round(final, 4),
                }
                if f_score is not None:
                    result["faithfulness"] = round(f_score, 4)
                if ar_score is not None:
                    result["answer_relevance"] = round(ar_score, 4)
                all_results.append(result)

                completed += 1
                progress.progress(completed / total, text=f"Processing {completed}/{total} rows...")

        progress.progress(1.0, text="Batch evaluation complete!")
        time.sleep(0.3)
        progress.empty()

        results_df = pd.DataFrame(all_results)
        st.session_state["batch_results"] = results_df

        # Save to disk
        os.makedirs("results", exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        results_df.to_csv(f"results/batch_{ts}.csv", index=False)
        st.success(f"✓ Saved to results/batch_{ts}.csv")

    # --- Analytics Dashboard ---
    if "batch_results" not in st.session_state:
        return

    results_df = st.session_state["batch_results"]
    score_cols = ["relevance", "quality", "bias", "consistency"]
    extra = [c for c in ["faithfulness", "answer_relevance"] if c in results_df.columns]
    all_score_cols = score_cols + extra

    st.markdown("## Analytics Dashboard")

    # --- KPI Cards ---
    st.markdown("### Metrics")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Rows", len(results_df))
    kpi2.metric("Models", results_df["model"].nunique())
    kpi3.metric("Avg Score", f"{results_df['final_score'].mean():.3f}")
    best_model = results_df.groupby("model")["final_score"].mean().idxmax()
    kpi4.metric("Best", best_model)

    # --- Per-model ranking table ---
    st.markdown("### Model Rankings")
    model_means = results_df.groupby("model")[["final_score"] + all_score_cols].mean()
    model_means = model_means.sort_values("final_score", ascending=False).reset_index()
    model_means.insert(0, "Rank", range(1, len(model_means) + 1))
    model_means.columns = [c.replace("_", " ").capitalize() for c in model_means.columns]
    st.dataframe(model_means, use_container_width=True, hide_index=True)

    # --- Charts row ---
    st.markdown("### Visualizations")
    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("**Radar Chart**")
        avg_results = []
        for model_name in results_df["model"].unique():
            model_data = results_df[results_df["model"] == model_name]
            avg = {"model": model_name}
            for col in all_score_cols:
                avg[col] = model_data[col].mean()
            avg_results.append(avg)
        fig = create_radar_chart(avg_results, rag_mode=bool(extra))
        st.pyplot(fig)
        plt.close(fig)

    with chart2:
        st.markdown("**Score Distribution**")
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        fig2.patch.set_facecolor("#0e1117")
        ax2.set_facecolor("#0e1117")
        colors = ["#00d4aa", "#ff6b6b", "#ffd93d", "#6bcbff", "#c084fc"]
        models = results_df["model"].unique()
        for i, model_name in enumerate(models):
            scores = results_df[results_df["model"] == model_name]["final_score"]
            ax2.hist(scores, bins=15, alpha=0.6, label=model_name, color=colors[i % len(colors)], edgecolor="#2a2a4e", linewidth=0.8)
        ax2.set_xlabel("Final Score", color="white", fontsize=11)
        ax2.set_ylabel("Frequency", color="white", fontsize=11)
        ax2.tick_params(colors="white")
        ax2.legend(facecolor="#0e1117", edgecolor="#2a2a4e", labelcolor="white")
        ax2.grid(True, alpha=0.15, color="#555")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # --- Heatmap ---
    st.markdown("### Score Heatmap")
    heatmap_data = results_df.groupby("model")[all_score_cols].mean()
    fig3, ax3 = plt.subplots(figsize=(10, max(3, len(heatmap_data) * 0.8)))
    fig3.patch.set_facecolor("#0e1117")
    ax3.set_facecolor("#0e1117")

    im = ax3.imshow(heatmap_data.values, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax3.set_xticks(range(len(all_score_cols)))
    ax3.set_xticklabels([c.replace("_", " ").capitalize() for c in all_score_cols], fontsize=10, color="white", rotation=30, ha="right")
    ax3.set_yticks(range(len(heatmap_data)))
    ax3.set_yticklabels(heatmap_data.index.tolist(), fontsize=11, color="white")

    for i in range(len(heatmap_data)):
        for j in range(len(all_score_cols)):
            v = heatmap_data.values[i, j]
            text_color = "black" if v > 0.5 else "white"
            ax3.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=10, fontweight="500", color=text_color)

    cbar = plt.colorbar(im, ax=ax3, shrink=0.8)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # --- Per-dimension box plots ---
    st.markdown("### Dimension Distribution")
    fig4, axes = plt.subplots(1, len(all_score_cols), figsize=(4 * len(all_score_cols), 5))
    fig4.patch.set_facecolor("#0e1117")
    if len(all_score_cols) == 1:
        axes = [axes]

    for idx, dim in enumerate(all_score_cols):
        ax = axes[idx]
        ax.set_facecolor("#0e1117")
        model_scores = [results_df[results_df["model"] == m][dim].values for m in models]
        bp = ax.boxplot(model_scores, patch_artist=True, labels=models, widths=0.6)
        for patch, color in zip(bp["boxes"], colors[:len(models)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        for element in ["whiskers", "caps", "medians"]:
            plt.setp(bp[element], color="white", linewidth=1.2)
        plt.setp(bp["fliers"], markeredgecolor="white")
        ax.set_title(dim.replace("_", " ").capitalize(), color="white", fontsize=12, fontweight="500")
        ax.tick_params(colors="white")
        ax.set_ylim(-0.05, 1.1)
        ax.grid(True, alpha=0.15, color="#555")
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

    # --- Most controversial prompts ---
    st.markdown("### Controversial Prompts")
    st.caption("Prompts where model scores varied the most")
    variance = results_df.groupby("prompt")["final_score"].agg(["std", "mean", "min", "max"])
    variance = variance.sort_values("std", ascending=False).head(10).reset_index()
    variance.columns = ["Prompt", "Variance", "Mean", "Min", "Max"]
    variance["Prompt"] = variance["Prompt"].str[:100]
    st.dataframe(variance, use_container_width=True, hide_index=True)

    # --- Download results ---
    st.markdown("### Export")
    csv_bytes = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Results (CSV)",
        data=csv_bytes,
        file_name="batch_evaluation_results.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ─────────────────────────────────────────────────────────────────────────
# Page 3: Validation Experiments
# ─────────────────────────────────────────────────────────────────────────

def page_validation():
    st.subheader("Validation Experiments")
    st.caption("Controlled test cases proving the evaluation system correctly distinguishes good vs bad AI outputs.")

    from validation_experiments import VALIDATION_CASES, run_validation

    # Show the test cases
    st.markdown("### Test Cases")
    case_df = pd.DataFrame([
        {
            "Case": c["id"],
            "Label": c["label"],
            "Metric": c["target_metric"],
            "Expected": c["expected"],
            "Prompt": c["prompt"][:60] + "...",
        }
        for c in VALIDATION_CASES
    ])
    st.dataframe(case_df, use_container_width=True, hide_index=True)

    if st.button("Run Validation Experiments", type="primary", use_container_width=True):
        with st.spinner("Running 10 controlled test cases across all metrics..."):
            results = run_validation(verbose=False)

        st.session_state["validation_results"] = results

    if "validation_results" not in st.session_state:
        st.info("Click the button above to run the validation suite.")
        return

    results = st.session_state["validation_results"]
    results_df = pd.DataFrame(results)

    # Summary KPIs
    total = len(results)
    passed = sum(1 for r in results if r["Pass/Fail"] == "PASS")
    failed = total - passed
    accuracy = (passed / total) * 100

    st.markdown("### Results Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Cases", total)
    k2.metric("Passed", passed)
    k3.metric("Failed", failed)
    k4.metric("Accuracy", f"{accuracy:.0f}%")

    # Full results table
    st.markdown("### Detailed Results")
    st.dataframe(results_df, use_container_width=True, hide_index=True)

    # Color-coded breakdown
    st.markdown("### Per-Metric Breakdown")
    metrics = results_df["Metric"].unique()
    cols = st.columns(min(len(metrics), 3))
    for i, metric in enumerate(metrics):
        with cols[i % 3]:
            subset = results_df[results_df["Metric"] == metric]
            metric_passed = sum(1 for _, r in subset.iterrows() if r["Pass/Fail"] == "PASS")
            metric_total = len(subset)
            st.markdown(f"**{metric.replace('_', ' ').capitalize()}**")
            st.progress(metric_passed / metric_total if metric_total > 0 else 0,
                        text=f"{metric_passed}/{metric_total} passed")

    # Observations
    st.markdown("### Observations")
    st.markdown("""
1. **Faithfulness Detection**: The system correctly assigns high scores to responses grounded in context
   and penalizes hallucinated claims (e.g., inventing medications not in the medical record).

2. **Answer Relevance vs Context Echoing**: Responses that directly answer the prompt score higher than
   responses that simply copy-paste the context verbatim, validating the dual-similarity penalty mechanism.

3. **Bias/Toxicity Detection**: Clean, professional responses receive high bias scores while toxic or
   discriminatory language is correctly flagged and penalized.

4. **Quality & Consistency**: Gibberish or repetitive text receives low quality scores. Self-contradictory
   responses (e.g., "exercise is beneficial" followed by "exercise is harmful") are penalized by the
   NLI-based consistency checker.
""")


# ─────────────────────────────────────────────────────────────────────────
# Main: Tab navigation
# ─────────────────────────────────────────────────────────────────────────

def main():
    st.title("Meta-Evaluation Framework")
    st.caption("AI Model Output Evaluation & Ranking")

    tab1, tab2, tab3 = st.tabs(["Single Evaluation", "Batch Analytics", "Validation Experiments"])

    with tab1:
        page_single_eval()

    with tab2:
        page_batch_analytics()

    with tab3:
        page_validation()


if __name__ == "__main__":
    main()
