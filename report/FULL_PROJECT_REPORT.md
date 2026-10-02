# META-EVALUATION FRAMEWORK FOR AI MODEL OUTPUTS USING TRANSFORMER-BASED MULTI-DIMENSIONAL ANALYSIS

## 21CSP302L - PROJECT

**Submitted by**

*STUDENT 1 NAME [RA21XXXXXXXXXXX]*
*STUDENT 2 NAME [RA21XXXXXXXXXXX]*

**Under the Guidance of**

*Dr. GUIDE NAME*
Professor, Department of Computational Intelligence

in partial fulfillment of the requirements for the degree of

**BACHELOR OF TECHNOLOGY**
in
**COMPUTER SCIENCE ENGINEERING**
with specialization in **Artificial Intelligence and Machine Learning**

DEPARTMENT OF COMPUTATIONAL INTELLIGENCE
COLLEGE OF ENGINEERING AND TECHNOLOGY
SRM INSTITUTE OF SCIENCE AND TECHNOLOGY
KATTANKULATHUR - 603 203

**MAY 2026**





## Department of Computational Intelligence
## SRM Institute of Science & Technology
## Own Work Declaration Form

This sheet must be filled in (each box ticked to show that the condition has been met). It must be signed and dated along with your student registration number and included with all assignments you submit – work will not be marked unless this is done.

To be completed by the student for all assessments

**Degree / Course:** B.Tech CSE (AI & ML)

**Student Name:** STUDENT 1 NAME, STUDENT 2 NAME

**Registration Number:** RA21XXXXXXXXXXX, RA21XXXXXXXXXXX

**Title of Work:** Meta-Evaluation Framework for AI Model Outputs Using Transformer-Based Multi-Dimensional Analysis

I / We hereby certify that this assessment complies with the University's Rules and Regulations relating to Academic misconduct and plagiarism, as listed in the University Website, Regulations, and the Education Committee guidelines.

I / We confirm that all the work contained in this assessment is my / our own except where indicated, and that I / We have met the following conditions:

- Clearly referenced / listed all sources as appropriate
- Referenced and put in inverted commas all quoted text (from books, web, etc)
- Given the sources of all pictures, data etc. that are not my own
- Not made any use of the report(s) or essay(s) of any other student(s) either past or present
- Acknowledged in appropriate places any help that I have received from others (e.g. fellow students, technicians, statisticians, external sources)
- Compiled with any other plagiarism criteria specified in the Course handbook / University website

I understand that any false claim for this work will be penalized in accordance with the University policies and regulations.

**DECLARATION:**

I am aware of and understand the University's policy on Academic misconduct and plagiarism and I certify that this assessment is my / our own work, except where indicated by referring, and that I have followed the good academic practices noted above.

<<Student 1 Name & Sign>>                    <<Student 2 Name & Sign>>

If you are working in a group, please write your registration numbers and sign with the date for every student in your group.





## SRM INSTITUTE OF SCIENCE AND TECHNOLOGY KATTANKULATHUR – 603 203

## BONAFIDE CERTIFICATE

Certified that 21CSP302L - Project report titled "Meta-Evaluation Framework for AI Model Outputs Using Transformer-Based Multi-Dimensional Analysis" is the bonafide work of "STUDENT 1 NAME [RA21XXXXXXXXXXX], STUDENT 2 NAME [RA21XXXXXXXXXXX]" who carried out the project work under my supervision. Certified further, that to the best of my knowledge the work reported herein does not form any other project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.

SIGNATURE &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; SIGNATURE

Dr. GUIDE NAME &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; DR. R. ANNIE UTHRA
SUPERVISOR &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; PROFESSOR & HEAD
Professor &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; DEPARTMENT OF
DEPARTMENT OF &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; COMPUTATIONAL INTELLIGENCE
COMPUTATIONAL INTELLIGENCE

EXAMINER 1 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; EXAMINER 2
Name & Signature &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Name & Signature





## ACKNOWLEDGEMENTS

We express our humble gratitude to Dr. C. Muthamizhchelvan, Vice-Chancellor, SRM Institute of Science and Technology, for the facilities extended for the project work and his continued support.

We extend our sincere thanks to Dr. Leenus Jesu Martin M, Dean-CET, SRM Institute of Science and Technology, for his invaluable support.

We wish to thank Dr. Revathi Venkataraman, Professor and Chairperson, School of Computing, SRM Institute of Science and Technology, for her support throughout the project work.

We encompass our sincere thanks to Dr. M. Pushpalatha, Professor and Associate Chairperson - CS, School of Computing and Dr. C. Lakshmi, Professor and Associate Chairperson - AI, School of Computing, SRM Institute of Science and Technology, for their invaluable support.

We are incredibly grateful to our Head of the Department, Dr. R. Annie Uthra, Professor and Head, Department of Computational Intelligence, SRM Institute of Science and Technology, for her suggestions and encouragement at all the stages of the project work.

We want to convey our thanks to our Project Coordinators, Panel Head, and Panel Members, Department of Computational Intelligence, SRM Institute of Science and Technology, for their inputs during the project reviews and support.

We register our immeasurable thanks to our Faculty Advisor, Department of Computational Intelligence, SRM Institute of Science and Technology, for leading and helping us to complete our course.

Our inexpressible respect and thanks to our guide, Dr. GUIDE NAME, Department of Computational Intelligence, SRM Institute of Science and Technology, for providing us with an opportunity to pursue our project under his / her mentorship. He / She provided us with the freedom and support to explore the research topics of our interest. His / Her passion for solving problems and making a difference in the world has always been inspiring.

We sincerely thank all the staff members of Computational Intelligence, School of Computing, SRM Institute of Science and Technology, for their help during our project. Finally, we would like to thank our parents, family members, and friends for their unconditional love, constant support and encouragement.

*Authors*





## ABSTRACT

The rapid growth of Large Language Models such as GPT-4, LLaMA, Gemini, and Mistral has made it increasingly difficult for practitioners and researchers to compare model outputs in any systematic way. Most existing evaluation methods either depend on costly human annotators or rely on a single automated metric that does not capture the many different qualities that matter in a good response. This project presents a Meta-Evaluation Framework that tackles these shortcomings through a modular, transformer-based pipeline. The pipeline scores AI model outputs across four core dimensions in standard mode and six dimensions in Retrieval-Augmented Generation mode.

The four standard evaluation dimensions are Relevance, measured through semantic similarity using the all-MiniLM-L6-v2 sentence transformer; Quality, assessed by a rule-based analyzer that checks length adequacy, vocabulary diversity, and structural formatting in JSON or Markdown; Bias, detected using the toxic-bert toxicity classifier trained on hate speech datasets; and Consistency, evaluated through Natural Language Inference with DeBERTa-v3-small to flag internal contradictions and cross-model disagreements. When context is provided, two additional RAG dimensions become active: Faithfulness, which uses NLI-based claim verification to identify hallucinated content that is not grounded in the given context, and Answer Relevance, which uses a dual-similarity technique to tell apart genuine answers from responses that simply restate the context.

A central contribution of this work is the learning-assisted weight optimisation module. Instead of relying on manually assigned static weights, a Ridge Regression model is trained on a labeled dataset of 51 human-rated samples to learn the optimal weighting for each dimension. The trained model reaches a cross-validated R-squared of 0.89, which indicates a strong match with human quality judgments. The learned weights show that Quality and Consistency carry more importance than initially assumed.

The framework is validated through 17 controlled test cases across all six evaluation dimensions, achieving an 88 percent pass rate on clear-cut scenarios and documenting known limitations on borderline cases. A benchmark suite of 10 diverse prompts across 6 subject categories confirms that the system consistently ranks coherent, relevant, non-contradictory responses above repetitive, off-topic, or self-contradictory outputs.

The system is deployed as an interactive Streamlit dashboard supporting single-prompt evaluation, batch analytics with concurrent processing, and live model integration with OpenAI, Google Gemini, and Ollama providers.

**Keywords:** Meta-Evaluation, Large Language Models, Natural Language Inference, Hallucination Detection, Transformer Models, RAG Evaluation, AI Benchmarking




## TABLE OF CONTENTS

| Section | Title | Page |
|---------|-------|------|
| | ABSTRACT | v |
| | TABLE OF CONTENTS | vi |
| | LIST OF FIGURES | vii |
| | LIST OF TABLES | viii |
| | ABBREVIATIONS | ix |
| **1** | **INTRODUCTION** | **1** |
| 1.1 | Introduction to Project | 1 |
| 1.2 | Problem Statement and Description | 3 |
| 1.3 | Motivation | 5 |
| 1.4 | Sustainable Development Goal of the Project | 6 |
| **2** | **LITERATURE SURVEY** | **7** |
| 2.1 | Overview of the Research Area | 7 |
| 2.2 | Existing Models and Frameworks | 9 |
| 2.3 | Limitations Identified from Literature Survey | 12 |
| 2.4 | Research Objectives | 13 |
| 2.5 | Product Backlog | 14 |
| 2.6 | Plan of Action (Project Road Map) | 16 |
| **3** | **SPRINT PLANNING AND EXECUTION METHODOLOGY** | **18** |
| 3.1 | SPRINT I — Core Evaluation Pipeline | 18 |
| 3.1.1 | Objectives with User Stories of Sprint I | 18 |
| 3.1.2 | Functional Document | 19 |
| 3.1.3 | Architecture Document | 21 |
| 3.1.4 | Outcome of Objectives / Result Analysis | 22 |
| 3.1.5 | Sprint Retrospective | 23 |
| 3.2 | SPRINT II — RAG Evaluation and Learning-Assisted Weights | 24 |
| 3.2.1 | Objectives with User Stories of Sprint II | 24 |
| 3.2.2 | Functional Document | 25 |
| 3.2.3 | Architecture Document | 27 |
| 3.2.4 | Outcome of Objectives / Result Analysis | 28 |
| 3.2.5 | Sprint Retrospective | 29 |
| 3.3 | SPRINT III — Dashboard, Batch Processing and Validation | 30 |
| 3.3.1 | Objectives with User Stories of Sprint III | 30 |
| 3.3.2 | Functional Document | 31 |
| 3.3.3 | Architecture Document | 32 |
| 3.3.4 | Outcome of Objectives / Result Analysis | 33 |
| 3.3.5 | Sprint Retrospective | 34 |
| **4** | **RESULTS AND DISCUSSIONS** | **35** |
| 4.1 | Project Outcomes | 35 |
| 4.2 | Performance Evaluation | 36 |
| 4.3 | Validation Results | 38 |
| 4.4 | Benchmark Analysis | 39 |
| **5** | **CONCLUSION AND FUTURE ENHANCEMENT** | **41** |
| | REFERENCES | 43 |
| | APPENDIX A — CODING | 45 |
| | APPENDIX B — SCREENSHOTS | 50 |
| | APPENDIX C — PLAGIARISM REPORT | 51 |





## LIST OF FIGURES

| Figure | Title | Page |
|--------|-------|------|
| Fig 1.1 | High-Level Architecture of the Meta-Evaluation Framework | 2 |
| Fig 1.2 | Standard Mode vs RAG Mode Evaluation Flow | 4 |
| Fig 2.1 | Evolution of LLM Evaluation Approaches | 8 |
| Fig 2.2 | Comparison of Existing Evaluation Frameworks | 10 |
| Fig 2.3 | Project Roadmap — Gantt Chart | 17 |
| Fig 3.1 | Module Architecture — Standard 4-Dimension Pipeline | 21 |
| Fig 3.2 | Sentence Embedding and Cosine Similarity Workflow | 22 |
| Fig 3.3 | NLI-Based Consistency Detection Flow | 23 |
| Fig 3.4 | Extended 6-Dimension Architecture with RAG Modules | 27 |
| Fig 3.5 | Faithfulness Claim Verification Pipeline | 28 |
| Fig 3.6 | Answer Relevance Dual-Similarity Mechanism | 28 |
| Fig 3.7 | Ridge Regression Weight Learning Workflow | 29 |
| Fig 3.8 | Streamlit Dashboard — Single Evaluation Tab | 32 |
| Fig 3.9 | Streamlit Dashboard — Batch Analytics Tab | 33 |
| Fig 3.10 | Streamlit Dashboard — Validation Experiments Tab | 33 |
| Fig 4.1 | Radar Chart — Model Comparison Across Dimensions | 36 |
| Fig 4.2 | Ranking Bar Chart — Final Scores | 37 |
| Fig 4.3 | Weight Comparison — Manual vs Learned Weights | 37 |
| Fig 4.4 | Score Distribution Box Plots by Dimension | 38 |
| Fig 4.5 | Benchmark Heatmap — Per-Prompt Scores | 40 |
| Fig 4.6 | Validation Pass/Fail Summary | 39 |





## LIST OF TABLES

| Table | Title | Page |
|-------|-------|------|
| Table 2.1 | Comparison of Existing LLM Evaluation Approaches | 11 |
| Table 2.2 | Product Backlog with User Stories | 14 |
| Table 3.1 | Sprint I User Stories and Acceptance Criteria | 19 |
| Table 3.2 | Evaluation Dimension Specifications | 20 |
| Table 3.3 | Sprint II User Stories and Acceptance Criteria | 25 |
| Table 3.4 | RAG Mode Weight Distribution | 26 |
| Table 3.5 | Sprint III User Stories and Acceptance Criteria | 31 |
| Table 4.1 | Static vs Learned Weights Comparison | 36 |
| Table 4.2 | Cross-Validation Metrics for Ridge Regression | 37 |
| Table 4.3 | Validation Experiment Results (17 Cases) | 38 |
| Table 4.4 | Benchmark Results — Per-Model Averages | 39 |





## ABBREVIATIONS

| Abbreviation | Full Form |
|---|---|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| CLI | Command Line Interface |
| CSV | Comma Separated Values |
| GPU | Graphics Processing Unit |
| JSON | JavaScript Object Notation |
| LLM | Large Language Model |
| MAE | Mean Absolute Error |
| ML | Machine Learning |
| MPS | Metal Performance Shaders |
| NLI | Natural Language Inference |
| NLP | Natural Language Processing |
| RAG | Retrieval-Augmented Generation |
| RMSE | Root Mean Squared Error |
| SDG | Sustainable Development Goal |
| UI | User Interface |
# CHAPTER 1

## INTRODUCTION

### 1.1 Introduction to Project

Artificial intelligence has moved from a niche research pursuit to a technology that millions of people interact with every day. A large part of this shift has been driven by Large Language Models, commonly referred to as LLMs. Models like OpenAI's GPT-4, Meta's LLaMA-3, Google's Gemini, and Mistral AI's Mistral-7B can now produce text that is fluent, contextually aware, and often indistinguishable from what a human expert might write. Businesses use these models for customer service chatbots, content generation, code assistance, legal document summarisation, and medical triage. Researchers rely on them for literature review, hypothesis generation, and data interpretation.

However, as these models have become more capable, a critical question has grown louder: how do we know which model is actually producing better output for a given task? When a user asks three different language models to explain a scientific concept, the three responses may all look polished on the surface, yet they can differ enormously in terms of factual accuracy, depth, logical coherence, and freedom from harmful bias. Evaluating these differences by hand is slow, expensive, and difficult to reproduce. A human annotator might rate one response highly on a Tuesday and give the same response a lower score on a Friday, simply because of fatigue or shifting standards.

This project addresses that gap by building a Meta-Evaluation Framework — a software system that takes a prompt and multiple AI model responses as input, runs them through a series of automated evaluation modules, and produces a ranked comparison with explainable scores. The word "meta" in the title is deliberate: rather than evaluating a single quality of the response, the framework evaluates the evaluation itself by combining multiple independent measurement dimensions into a single composite score that reflects overall response quality.

The framework operates in two modes. In standard mode, it scores responses along four dimensions: Relevance, Quality, Bias, and Consistency. Each dimension is powered by a different technique — semantic embeddings for relevance, rule-based structural analysis for quality, a toxicity classifier for bias, and Natural Language Inference for consistency. In RAG mode (Retrieval-Augmented Generation), two additional dimensions are activated: Faithfulness, which checks whether the response is grounded in a provided context document, and Answer Relevance, which determines whether the response actually answers the user's question rather than simply paraphrasing the context.

The system is not merely a collection of scoring functions. It also includes a learning-assisted weight optimisation module that uses Ridge Regression trained on human-rated samples to discover how much each dimension should contribute to the final score. This means the framework does not rely on arbitrary hand-tuned weights; instead, it learns from data what matters most to human evaluators.

The entire pipeline is accessible through a Streamlit web dashboard that supports interactive single-prompt evaluation, batch processing of large datasets with concurrent execution, and live integration with OpenAI, Google Gemini, and Ollama model providers.

Fig 1.1: High-Level Architecture of the Meta-Evaluation Framework

### 1.2 Problem Statement and Description

The fundamental problem this project sets out to solve can be stated simply: there is no widely accepted, automated, multi-dimensional method for comparing the outputs of different Large Language Models against one another.

Current evaluation practices suffer from several well-documented limitations. First, human evaluation is the gold standard but it is prohibitively expensive at scale. Hiring trained annotators to compare thousands of model outputs across dozens of prompts requires significant time and budget. Second, existing automated metrics tend to focus on a single aspect of quality. BLEU and ROUGE measure surface-level text overlap with a reference answer, but they cannot tell whether a response is logically consistent or free from harmful stereotypes. BERTScore [1] uses contextual embeddings to measure similarity, which is an improvement, but it still operates along a single axis. Third, most evaluation tools do not account for the unique challenges posed by RAG pipelines, where models are given a context document and expected to generate responses grounded in that context. A model might produce a fluent and seemingly relevant response that is entirely hallucinated — containing claims that appear nowhere in the source material.

The problem becomes even more pressing as organisations deploy LLMs in high-stakes domains. A healthcare chatbot that hallucinates medication dosages, a legal assistant that generates self-contradictory advice, or a customer service bot that produces biased language can cause real harm. There is a genuine need for a tool that can flag these issues automatically, across multiple quality dimensions, in a way that is reproducible and explainable.

This project tackles these challenges by designing a modular pipeline where each evaluation dimension is handled by a dedicated module. The modules operate independently, which means new dimensions can be added in the future without disrupting existing ones. The scores from all modules are combined using a weighted aggregation scheme, where the weights can either be set manually or learned from labeled training data.

The specific technical problems addressed are as follows:

1. How to measure semantic relevance between a prompt and a response without relying on keyword overlap.
2. How to assess structural quality of a response — its length, vocabulary diversity, and formatting — using deterministic rules that do not require a neural network.
3. How to detect toxic, biased, or harmful content in model outputs using a pretrained toxicity classifier.
4. How to identify logical contradictions within a single response and across multiple model responses using Natural Language Inference.
5. How to detect hallucinated claims in RAG scenarios by verifying each claim against the provided context.
6. How to distinguish genuine answers from context-echoing in RAG outputs.
7. How to learn optimal dimension weights from human preference data using regression.

Fig 1.2: Standard Mode vs RAG Mode Evaluation Flow

### 1.3 Motivation

The motivation for this project comes from both academic curiosity and practical necessity. On the academic side, the field of LLM evaluation is still maturing. Most published benchmarks — MMLU, HellaSwag, ARC, and others — test models on multiple-choice questions where a single correct answer exists [2,3]. These benchmarks are valuable for measuring factual knowledge and reasoning ability, but they do not capture the qualities that matter in real-world applications: Can the model write a coherent paragraph? Does it stay on topic? Does it contradict itself? Does it avoid harmful stereotypes? Our framework fills this gap by moving evaluation from closed-ended factual recall to open-ended response quality assessment.

On the practical side, organisations that deploy LLMs need a reliable way to choose between models, monitor output quality over time, and catch regressions before they affect end users. A healthcare company evaluating whether to switch from one model to another cannot afford to run a week-long human annotation study every time a new model is released. An automated evaluation pipeline that runs in minutes and produces interpretable scores solves this problem.

There is also an ethical dimension. Bias in AI outputs is a growing concern, and the consequences of deploying a biased model can range from reputational damage to legal liability. By including a dedicated bias detection module powered by a toxicity classifier, the framework ensures that harmful content is flagged automatically, contributing to the responsible deployment of AI systems.

Finally, the rise of Retrieval-Augmented Generation has introduced new failure modes that traditional evaluation cannot catch. A RAG model might produce a response that sounds authoritative but is completely fabricated — the hallucination problem. Our faithfulness module addresses this directly by splitting the response into individual claims and verifying each one against the provided context using NLI.

### 1.4 Sustainable Development Goal of the Project

This project aligns with the United Nations Sustainable Development Goal 9: Industry, Innovation, and Infrastructure, which promotes the development of reliable, sustainable, and resilient infrastructure, inclusive and sustainable industrialisation, and innovation. By creating tools that evaluate and rank AI model outputs in a transparent and reproducible manner, the framework supports the responsible deployment of AI infrastructure in industries ranging from healthcare to education.

The project also contributes to SDG 16: Peace, Justice, and Strong Institutions. The bias detection module specifically targets the identification of toxic, discriminatory, or harmful content in AI outputs. Automated detection of such content helps organisations ensure that their AI systems do not perpetuate social inequities or produce language that could harm marginalised communities. The toxic-bert model used in the bias module was trained on large datasets of hate speech and offensive language [4], making it capable of flagging a wide range of problematic outputs.

In a broader sense, the framework supports SDG 4: Quality Education by providing a tool that can be used to evaluate AI tutoring systems and educational chatbots. If an AI-powered educational tool produces inconsistent, inaccurate, or biased explanations, it can mislead students and undermine learning outcomes. The multi-dimensional evaluation approach ensures that educational AI outputs meet minimum standards of relevance, accuracy, and safety.
# CHAPTER 2

## LITERATURE SURVEY

### 2.1 Overview of the Research Area

The evaluation of natural language generation systems has been an active area of research for over two decades, but the emergence of Large Language Models has fundamentally changed the landscape. Early evaluation methods were designed for machine translation and text summarisation, where a reference answer exists and the generated text can be compared against it. Metrics like BLEU [5], introduced by Papineni et al. in 2002, compute n-gram overlap between a candidate translation and one or more reference translations. ROUGE [6], developed by Lin in 2004, extended this idea to summarisation by measuring recall of n-grams from a reference summary. These metrics remain widely used in published papers, but they have well-known weaknesses: they cannot capture meaning, they penalise valid paraphrases, and they require a reference answer that may not exist in open-ended generation tasks.

The introduction of BERTScore [1] by Zhang et al. in 2020 marked a significant step forward. Instead of counting n-gram matches, BERTScore computes token-level cosine similarity between BERT embeddings of the candidate and reference texts. This approach captures semantic similarity rather than surface-level overlap, which means that a response like "Automobiles travel on highways" would score well against a reference like "Cars drive on roads" even though the two sentences share no words. However, BERTScore still requires a reference answer, and it operates along a single dimension — it cannot distinguish between a response that is semantically relevant but toxic and one that is relevant and safe.

More recently, researchers have explored reference-free evaluation methods that do not require a gold-standard answer. GPTScore [7], proposed by Fu et al. in 2023, uses the generation probability of a large language model as a quality signal — the idea being that higher-quality text is more likely under the model's distribution. G-Eval [8], introduced by Liu et al. in 2023, takes a different approach by prompting GPT-4 itself to evaluate generated text along dimensions like coherence, relevance, and fluency. While these methods are powerful, they introduce a circular dependency: the same family of models being evaluated is also performing the evaluation, which raises questions about bias and reliability.

The field of AI safety evaluation has also grown substantially. Gehman et al. [9] studied the tendency of language models to generate toxic text and introduced the RealToxicityPrompts benchmark. Perspective API and tools like Detoxify [10] provide toxicity classifiers that can score individual text segments, but they operate as standalone tools rather than components of a comprehensive evaluation pipeline.

In the domain of Retrieval-Augmented Generation, evaluation has focused on two failure modes: hallucination, where the model generates claims not supported by the retrieved context, and context echoing, where the model simply copies the context verbatim without actually answering the question. The RAGAS framework [11] proposed by Es et al. in 2024 addresses these issues by computing faithfulness, answer relevance, and context precision scores. Our project draws inspiration from this work but implements the evaluation using lightweight transformer models rather than relying on API calls to commercial LLMs, making it faster and more cost-effective.

Fig 2.1: Evolution of LLM Evaluation Approaches

### 2.2 Existing Models and Frameworks

Several frameworks and tools have been developed to evaluate LLM outputs. This section reviews the most relevant ones and identifies their strengths and limitations.

**BERTScore** [1] uses contextual embeddings from BERT to compute precision, recall, and F1 between candidate and reference texts at the token level. It correlates well with human judgments on text generation tasks and has become a standard metric in NLP research. However, it requires a reference answer, operates along a single quality dimension, and does not address safety or factual consistency.

**BLEU and ROUGE** [5,6] remain the most commonly reported metrics in machine translation and summarisation papers. They are fast to compute and easy to interpret, but their reliance on n-gram overlap makes them insensitive to meaning. A response that uses different vocabulary to express the same idea will be penalised, while a response that copies surface patterns without understanding may be rewarded.

**G-Eval** [8] prompts GPT-4 to evaluate text quality by providing a detailed rubric and asking the model to assign scores. The authors showed that G-Eval achieves higher correlation with human judgments than traditional metrics on tasks like summarisation and dialogue evaluation. The main drawback is cost — each evaluation requires an API call to a commercial model — and the circular evaluation concern noted above.

**RAGAS** [11] is a framework specifically designed for RAG pipeline evaluation. It defines metrics for faithfulness (are the claims grounded in context?), answer relevance (does the response address the question?), and context precision/recall (is the retrieved context useful?). RAGAS computes these metrics using LLM calls, which makes it accurate but slow and expensive for large-scale benchmarking.

**DeepEval** [12] is an open-source LLM evaluation framework that provides metrics similar to RAGAS but adds support for bias detection and toxicity scoring. It offers a testing interface modeled after pytest, making it developer-friendly. However, it still relies on LLM-as-judge for most of its quality metrics.

**Prometheus** [13] by Kim et al. in 2024 is an open-source LLM specifically fine-tuned for evaluation tasks. It can assess text quality without needing a reference answer and has shown performance comparable to GPT-4 on evaluation benchmarks. The limitation is that it requires downloading and running a large model, which may not be feasible for all deployment scenarios.

**LangChain Evaluation** provides utility functions for evaluating chain outputs using criteria like correctness, relevance, and helpfulness. These evaluations typically use an LLM as the judge, and the framework is tightly coupled to the LangChain ecosystem.

Fig 2.2: Comparison of Existing Evaluation Frameworks

| Table 2.1: Comparison of Existing LLM Evaluation Approaches |
|---|

| Framework | Dimensions | Reference Required | LLM Dependency | RAG Support | Cost |
|-----------|-----------|-------------------|----------------|-------------|------|
| BLEU/ROUGE | 1 (overlap) | Yes | None | No | Free |
| BERTScore | 1 (semantic) | Yes | BERT only | No | Free |
| G-Eval | Multiple | No | GPT-4 calls | No | High |
| RAGAS | 3 (RAG-specific) | No | LLM calls | Yes | High |
| DeepEval | Multiple | No | LLM calls | Yes | Medium |
| Prometheus | Multiple | No | Custom LLM | No | Medium |
| **Ours** | **4 or 6** | **No** | **Local transformers** | **Yes** | **Free** |

### 2.3 Limitations Identified from Literature Survey (Research Gaps)

From the review of existing work, several clear gaps emerge that this project aims to address:

1. **Single-dimension evaluation.** Most established metrics — BLEU, ROUGE, BERTScore — evaluate along a single axis. Real-world response quality is multi-dimensional: a response can be relevant but toxic, or well-structured but factually inconsistent. There is a need for frameworks that evaluate multiple dimensions simultaneously and combine them into a single interpretable score.

2. **Dependence on reference answers.** Traditional metrics require a gold-standard reference, which is impractical for open-ended generation tasks where many valid answers exist. Evaluation methods need to work without a reference by assessing intrinsic properties of the response itself.

3. **Reliance on commercial LLM APIs.** Frameworks like G-Eval and RAGAS use GPT-4 or similar models as judges. This introduces cost, latency, and a circular evaluation problem. A framework built on lightweight, locally-run transformer models avoids these issues.

4. **Fixed, arbitrary weights.** When multiple evaluation dimensions are used, they are typically combined using manually chosen weights with little empirical justification. A data-driven approach that learns weights from human ratings would produce more reliable composite scores.

5. **Limited RAG-specific evaluation.** While RAGAS addresses faithfulness and answer relevance, it does not combine these with broader quality metrics like structural analysis, bias detection, or cross-model consistency. A unified framework that handles both standard and RAG evaluation modes would be more versatile.

6. **Lack of validation methodology.** Many evaluation frameworks report correlation with human judgments on standard benchmarks but do not provide controlled test cases that demonstrate the framework's ability to discriminate between clearly good and clearly bad outputs across each dimension.

### 2.4 Research Objectives

Based on the gaps identified in the literature survey, the following research objectives were defined for this project:

1. Design and implement a modular evaluation pipeline that assesses AI model outputs across four standard dimensions (Relevance, Quality, Bias, Consistency) using lightweight transformer models and rule-based methods, without requiring reference answers or commercial API calls.

2. Extend the pipeline to support RAG evaluation with two additional dimensions (Faithfulness, Answer Relevance) that detect hallucinated content and distinguish genuine answers from context echoing.

3. Develop a learning-assisted weight optimisation module that trains a Ridge Regression model on human-rated samples to discover the optimal contribution of each dimension to the final composite score.

4. Validate the framework through controlled test cases that demonstrate its ability to correctly distinguish high-quality outputs from low-quality outputs across all six evaluation dimensions.

5. Build a multi-prompt benchmark suite that confirms the framework generalises across diverse subject categories and consistently ranks models in agreement with expected quality ordering.

6. Deploy the framework as an interactive web dashboard with support for single-prompt evaluation, batch processing, and live integration with multiple LLM providers.

### 2.5 Product Backlog (Key User Stories with Desired Outcomes)

| Table 2.2: Product Backlog with User Stories |
|---|

| ID | User Story | Priority | Desired Outcome |
|----|-----------|----------|-----------------|
| US-01 | As a developer, I want to evaluate AI responses across multiple dimensions so that I can identify specific strengths and weaknesses of each model. | High | Multi-dimensional scoring pipeline with scores for relevance, quality, bias, and consistency. |
| US-02 | As a researcher, I want the system to detect hallucinated content in RAG outputs so that I can measure how grounded a model's response is in the source material. | High | Faithfulness module that splits response into claims and verifies each against context using NLI. |
| US-03 | As a product manager, I want composite scores that reflect human quality preferences so that I can make data-driven model selection decisions. | High | Learned weights from Ridge Regression with R-squared above 0.8. |
| US-04 | As a QA engineer, I want to run batch evaluations on large datasets so that I can benchmark multiple models across many prompts efficiently. | Medium | Batch processing pipeline with concurrent execution and CSV export. |
| US-05 | As a user, I want an interactive web dashboard so that I can evaluate models without writing code. | Medium | Streamlit dashboard with single evaluation, batch analytics, and validation tabs. |
| US-06 | As a safety engineer, I want automatic detection of biased or toxic content so that I can flag problematic outputs before deployment. | High | Bias module using toxic-bert classifier with inverted scoring (1.0 = clean, 0.0 = toxic). |
| US-07 | As a developer, I want to connect to live LLM APIs so that I can generate and evaluate real model outputs in the dashboard. | Low | Provider integration for OpenAI, Google Gemini, and Ollama with standardised response format. |
| US-08 | As a researcher, I want controlled validation experiments so that I can demonstrate the framework's discriminative ability for my project defense. | Medium | 17 test cases across 6 dimensions with documented pass/fail results and known limitations. |

### 2.6 Plan of Action (Project Road Map)

The project was planned across three development sprints, each lasting approximately four weeks, following an Agile methodology adapted for a two-person academic team.

**Phase 1 — Research and Planning (Weeks 1–2):**
Literature survey of existing LLM evaluation methods. Identification of research gaps. Selection of transformer models for each evaluation dimension. Definition of the system architecture and module interfaces.

**Phase 2 — Sprint I: Core Pipeline (Weeks 3–6):**
Implementation of the four standard evaluation modules (Relevance, Quality, Bias, Consistency). Development of the Score Aggregator with static weights. Creation of the CLI entry point. Initial unit testing.

**Phase 3 — Sprint II: RAG and Learning (Weeks 7–10):**
Implementation of the Faithfulness and Answer Relevance modules. Development of the Ridge Regression weight training script. Collection and labeling of the 51-sample training dataset. Cross-validation and weight comparison analysis.

**Phase 4 — Sprint III: Dashboard and Validation (Weeks 11–14):**
Development of the Streamlit web dashboard with three tabs. Implementation of batch processing with concurrent execution. Integration of LLM providers (OpenAI, Gemini, Ollama). Design and execution of 17 validation test cases. Multi-prompt benchmark with 10 prompts across 6 categories.

**Phase 5 — Documentation and Defense (Weeks 15–16):**
Report writing. Chart generation for results visualisation. Code cleanup and final testing. Project defense preparation.

Fig 2.3: Project Roadmap — Gantt Chart
# CHAPTER 3

## SPRINT PLANNING AND EXECUTION METHODOLOGY

### 3.1 SPRINT I — Core Evaluation Pipeline

#### 3.1.1 Objectives with User Stories of Sprint I

The first sprint focused on building the foundational evaluation pipeline — the four standard scoring modules that form the backbone of the entire framework. The objective was to have a working end-to-end system that could accept a prompt and multiple model responses, score them across four dimensions, and produce a ranked output.

| Table 3.1: Sprint I User Stories and Acceptance Criteria |
|---|

| Story ID | User Story | Acceptance Criteria |
|----------|-----------|-------------------|
| US-01a | As a developer, I want a Relevance module that measures how semantically related a response is to the prompt. | Module uses all-MiniLM-L6-v2 embeddings with cosine similarity. Score range 0–1. Semantically similar but lexically different texts score above 0.4. |
| US-01b | As a developer, I want a Quality module that checks structural properties of the response. | Module evaluates length adequacy, vocabulary diversity (repetition score), JSON validity, and Markdown formatting. No ML model required. |
| US-01c | As a developer, I want a Bias module that detects toxic or harmful content. | Module uses toxic-bert classifier. Clean text scores above 0.9. Explicitly toxic text scores below 0.5. |
| US-01d | As a developer, I want a Consistency module that detects logical contradictions. | Module uses DeBERTa-v3-small for NLI. Self-contradictory text (e.g., "X is great. X is terrible.") scores lower than logically coherent text. Cross-model consistency supported. |
| US-01e | As a developer, I want a Score Aggregator that combines dimension scores into a final ranking. | Aggregator uses configurable weights summing to 1.0. Default: Relevance 35%, Quality 25%, Bias 25%, Consistency 15%. |

#### 3.1.2 Functional Document

**Relevance Module (relevance.py)**

The Relevance module measures semantic similarity between the user's prompt and the model's response. It uses the all-MiniLM-L6-v2 sentence transformer [14], a lightweight model that maps text to 384-dimensional dense vector embeddings. Both the prompt and the response are encoded into embedding vectors, and cosine similarity is computed between them. The result is a float between 0.0 (completely unrelated) and 1.0 (semantically identical). The key advantage of this approach over keyword-based methods is that it captures meaning: the prompt "Cars drive on roads" and the response "Automobiles travel on highways" produce a high similarity score despite sharing no words.

The module automatically selects the best available compute device. On Apple Silicon machines, it uses the Metal Performance Shaders (MPS) backend for GPU-accelerated inference. On other systems, it falls back to CPU.

**Quality Module (quality.py)**

The Quality module is entirely rule-based, requiring no neural network. It evaluates four sub-dimensions of structural quality:

1. **Length adequacy:** Responses under 10 words receive a score of 0.3. Responses between 10–29 words score 0.6. Responses between 30–59 words score 0.8. Responses with 60 or more words score 1.0. These thresholds were chosen to reflect the expectation that substantive answers to open-ended questions should contain at least several sentences.

2. **Repetition penalty:** The module computes vocabulary diversity as the ratio of unique words to total words. A response that repeats the same word ten times (e.g., "data data data data data data data data data data") receives a diversity score of 0.1, while a response with all unique words scores 1.0.

3. **JSON structure detection:** If the response contains valid JSON, it receives a structure score of 1.0. Partial or malformed JSON receives a lower score. This rewards models that produce structured data when appropriate.

4. **Markdown structure detection:** The module checks for Markdown elements — headers, bullet lists, code blocks, and emphasis markers. Each element contributes 0.2–0.3 to the structure score, rewarding models that format their responses for readability.

The final quality score combines the basic score (average of length and repetition) with the structure score using a 60/40 weighting. If no structural elements are detected, the basic score is used alone.

| Table 3.2: Evaluation Dimension Specifications |
|---|

| Dimension | Model/Method | Input | Output Range | Weight (Static) |
|-----------|-------------|-------|-------------|-----------------|
| Relevance | all-MiniLM-L6-v2 | Prompt + Response | 0.0 – 1.0 | 35% |
| Quality | Rule-based (length, diversity, structure) | Response only | 0.0 – 1.0 | 25% |
| Bias | toxic-bert classifier | Response only | 0.0 – 1.0 | 25% |
| Consistency | DeBERTa-v3-small NLI | Response + Other responses | 0.0 – 1.0 | 15% |

**Bias Module (bias.py)**

The Bias module uses the toxic-bert model from Unitary [4], a BERT-based classifier fine-tuned on datasets of toxic, hateful, and offensive text. The module truncates the response to 512 characters (the model's token limit), passes it through the classifier, and interprets the output. If the classifier labels the text as "toxic," the toxicity confidence score is inverted so that highly toxic text receives a score close to 0.0 and clean text receives a score close to 1.0. This inversion ensures that higher scores always indicate better quality across all dimensions, maintaining consistency in the scoring interface.

**Consistency Module (consistency.py)**

The Consistency module uses the cross-encoder/nli-deberta-v3-small model [15] for Natural Language Inference. NLI classifies the relationship between two text segments into three categories: entailment (the second follows logically from the first), neutral (no clear logical relationship), and contradiction (the second contradicts the first).

The module evaluates two types of consistency:

1. **Internal consistency:** The response is split into individual sentences using punctuation-based rules. Every pair of sentences is compared using NLI, and the contradiction probability is averaged across all pairs. The final internal consistency score is 1.0 minus this average, so a response with no contradictions scores 1.0 and a response with strong internal contradictions scores close to 0.0. Sentences shorter than 10 characters are filtered out to avoid spurious comparisons.

2. **Cross-model consistency:** The response is compared against each other model's response using NLI. High contradiction probabilities indicate that the model disagrees with the consensus, which may signal factual errors. The cross-model score is computed the same way as the internal score.

The combined consistency score is a 50/50 weighted average of internal and cross-model scores. When only one model is being evaluated (no other responses available), only the internal score is used.

#### 3.1.3 Architecture Document

The system follows a modular pipeline architecture. At the top level, the main.py CLI script orchestrates the evaluation. It accepts a prompt, a dictionary of model name to response text mappings, and optional configuration flags. The script instantiates each evaluation module, calls their compute_score methods in sequence, and passes all dimension scores to the Score Aggregator for final ranking.

Each module is a standalone Python class with a consistent interface. The Relevance and Consistency modules load transformer models at initialisation time. The Quality module requires no model loading. The Bias module loads the toxic-bert pipeline. All heavy model loading happens once at startup, and subsequent evaluations reuse the loaded models, which is critical for batch processing performance.

The Score Aggregator accepts four dimension scores and returns a weighted sum. The weights can be overridden through constructor parameters, loaded from a trained model file (learned_weights.json), or left at their defaults. The aggregator also supports RAG mode, where it accepts six dimension scores and uses a separate weight configuration.

Fig 3.1: Module Architecture — Standard 4-Dimension Pipeline

Fig 3.2: Sentence Embedding and Cosine Similarity Workflow

#### 3.1.4 Outcome of Objectives / Result Analysis

All five user stories for Sprint I were completed successfully. The pipeline was tested on a sample evaluation scenario with three model responses to the prompt "Explain machine learning in simple terms." The three test responses were designed to represent distinct quality levels:

- **GPT-4 (high quality):** A clear, well-structured explanation with concrete examples. Received scores of Relevance 0.674, Quality 0.872, Bias 0.999, Consistency 0.750, Final 0.816.

- **Llama-3 (low quality):** A repetitive, incoherent response. Received scores of Relevance 0.633, Quality 0.621, Bias 0.996, Consistency 0.750, Final 0.738.

- **Mistral-7B (contradictory):** A response that starts coherently but contradicts itself ("machine learning is completely useless and does not work at all in practice"). Received scores of Relevance 0.651, Quality 0.839, Bias 0.998, Consistency 0.176, Final 0.714.

The system correctly ranked GPT-4 first, Llama-3 second, and Mistral-7B third. The consistency module successfully detected the self-contradiction in the Mistral-7B response, assigning it a consistency score of 0.176 compared to 0.750 for the other two models.

Fig 3.3: NLI-Based Consistency Detection Flow

#### 3.1.5 Sprint Retrospective

**What went well:** The modular architecture made it straightforward to develop and test each module independently. The all-MiniLM-L6-v2 model loaded quickly and provided good semantic similarity scores. The DeBERTa NLI model effectively detected the planted contradiction.

**What could be improved:** The Quality module's length thresholds are somewhat arbitrary. Future work could calibrate these against human quality ratings. The Bias module (toxic-bert) is effective for explicit toxicity but struggles with subtle stereotypes expressed in polite language, as discovered later during validation.

**Action items for Sprint II:** Implement RAG evaluation modules. Develop the weight training script. Collect labeled training data.





### 3.2 SPRINT II — RAG Evaluation and Learning-Assisted Weights

#### 3.2.1 Objectives with User Stories of Sprint II

The second sprint had two major objectives: extending the framework to handle RAG evaluation scenarios and implementing the data-driven weight learning module.

| Table 3.3: Sprint II User Stories and Acceptance Criteria |
|---|

| Story ID | User Story | Acceptance Criteria |
|----------|-----------|-------------------|
| US-02a | As a researcher, I want a Faithfulness module that checks whether response claims are grounded in the provided context. | Module splits response into claims, runs NLI against context for each claim. Fully grounded responses score above 0.8. Hallucinated responses score below 0.5. |
| US-02b | As a researcher, I want an Answer Relevance module that distinguishes genuine answers from context echoing. | Module computes prompt-response similarity and context-response similarity. Applies echo penalty when context similarity dominates. |
| US-03a | As a data scientist, I want to train optimal weights from human-rated data. | Ridge Regression with 5-fold cross-validation. R-squared above 0.8 on held-out data. Weights normalised to sum to 1.0. |

#### 3.2.2 Functional Document

**Faithfulness Module (faithfulness.py)**

The Faithfulness module is the core of the RAG evaluation capability. It detects hallucinated content — claims in the model's response that are not supported by the provided context. The algorithm works in three steps:

1. **Claim extraction:** The response is split into individual sentences using punctuation-based splitting. Fragments shorter than 15 characters are filtered out to avoid evaluating trivial phrases.

2. **Per-claim NLI verification:** Each extracted claim is paired with the full context as premise and hypothesis for NLI classification using the same DeBERTa-v3-small model used by the Consistency module. The model instance is shared between the two modules to avoid loading it twice, reducing memory usage and startup time. For each claim, the model outputs probabilities for three labels: entailment (claim is supported by context), neutral (claim cannot be verified from context), and contradiction (claim directly contradicts context).

3. **Score computation:** The faithfulness score is computed as (entailed claims + 0.5 × neutral claims) / total claims. Entailed claims receive full credit. Neutral claims receive half credit because they may represent valid inferences that go beyond the context without contradicting it. Contradicted claims receive zero credit. This scoring scheme means a fully grounded response scores 1.0, a response with all neutral claims scores 0.5, and a response with all contradictions scores 0.0.

The module returns a detailed result dictionary containing the overall score, counts of entailed, neutral, and hallucinated claims, and per-claim breakdowns with individual NLI probabilities. This detailed output enables the dashboard to display exactly which claims were flagged and why.

**Answer Relevance Module (answer_relevance.py)**

The Answer Relevance module addresses a subtle failure mode in RAG systems: context echoing. A model might achieve a high faithfulness score by simply copying the context verbatim, but this does not constitute a useful answer. The module uses a dual-similarity approach:

1. **Prompt similarity:** Cosine similarity between the prompt and the response, computed using the same all-MiniLM-L6-v2 model as the Relevance module (shared instance). High prompt similarity means the response stays on topic with respect to the question.

2. **Context similarity:** Cosine similarity between the context and the response. High context similarity means the response closely resembles the context text.

3. **Echo detection and penalty:** If context similarity exceeds prompt similarity by more than 0.15 (the echo threshold), the response is flagged as a context echo. An echo penalty is applied: final score = prompt_sim − α × (context_sim − prompt_sim), where α is the echo penalty coefficient (default 0.5). This penalises responses that are more similar to the context than to the prompt.

| Table 3.4: RAG Mode Weight Distribution |
|---|

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Relevance | 15% | Less critical when context provides focus |
| Quality | 15% | Structure matters but is secondary to accuracy |
| Bias | 10% | Safety baseline |
| Consistency | 10% | Internal logic check |
| Faithfulness | 35% | Most important — hallucination prevention |
| Answer Relevance | 15% | Ensures the response actually answers the question |

**Weight Training Module (train_weights.py)**

The weight training module replaces manually assigned static weights with empirically learned ones. The approach uses Ridge Regression (L2-regularised linear regression) to learn a mapping from the four dimension scores to human quality ratings:

human_rating ≈ w₁ × relevance + w₂ × quality + w₃ × bias + w₄ × consistency

The training data consists of 51 samples stored in data/labeled_dataset.csv. Each sample contains a prompt, model name, response text, the four dimension scores (pre-computed), and a human quality rating between 0 and 1. The dataset covers 17 unique prompts and 3 model archetypes: a high-quality model that produces detailed, accurate responses; a low-quality model that produces repetitive, incoherent text; and a contradictory model that starts well but contradicts itself.

The training process involves the following steps:

1. Load and validate the dataset. Check that all required columns are present and values are within the expected 0–1 range.
2. Compute Pearson correlation between each feature and the target variable to understand which dimensions align most strongly with human judgments.
3. Run 5-fold cross-validation with Ridge Regression (alpha = 1.0) to estimate generalisation performance. Report R-squared, MAE, and RMSE for each fold.
4. Train the final model on the full dataset.
5. Extract the raw regression coefficients. Clamp any negative coefficients to zero (a dimension should not have negative weight). Normalise the remaining coefficients to sum to 1.0.
6. Save the learned weights, raw coefficients, training metrics, and metadata to models/learned_weights.json.

#### 3.2.3 Architecture Document

The RAG modules extend the existing pipeline without modifying it. The main evaluation function accepts an optional context parameter. When context is provided, the pipeline enters RAG mode: the Faithfulness and Answer Relevance modules are instantiated (sharing model instances with the Consistency and Relevance modules respectively), and all six dimension scores are passed to the aggregator with the RAG weight configuration.

The weight training module operates independently of the evaluation pipeline. It reads pre-computed scores from a CSV file, trains the regression model, and writes the learned weights to a JSON file. The aggregator loads this file at initialisation when the use_learned flag is set.

Fig 3.4: Extended 6-Dimension Architecture with RAG Modules

Fig 3.5: Faithfulness Claim Verification Pipeline

Fig 3.6: Answer Relevance Dual-Similarity Mechanism

#### 3.2.4 Outcome of Objectives / Result Analysis

**Weight Training Results:**

The Ridge Regression model was trained on 51 samples with 5-fold cross-validation. The results were as follows:

| Table 4.1: Static vs Learned Weights Comparison |
|---|

| Dimension | Static Weight | Learned Weight | Change |
|-----------|--------------|----------------|--------|
| Relevance | 35.0% | 24.2% | −10.8% |
| Quality | 25.0% | 40.9% | +15.9% |
| Bias | 25.0% | 0.7% | −24.3% |
| Consistency | 15.0% | 34.2% | +19.2% |

| Table 4.2: Cross-Validation Metrics for Ridge Regression |
|---|

| Metric | Value |
|--------|-------|
| Cross-validated R² (mean) | 0.8900 |
| Cross-validated R² (std) | 0.0128 |
| Cross-validated MAE (mean) | 0.0978 |
| Cross-validated RMSE (mean) | 0.1017 |
| Full dataset R² | 0.9250 |
| Full dataset MAE | 0.0827 |
| Full dataset RMSE | 0.0870 |
| Train R² (mean) | 0.9004 |

The learned weights reveal insights that were not obvious from manual weight assignment. Quality received the highest weight (40.9%), suggesting that human evaluators place great importance on response structure, length, and vocabulary diversity. Consistency received the second-highest weight (34.2%), confirming that logical coherence is a critical quality signal. Relevance dropped from 35% to 24.2%, possibly because relevance scores were relatively high across all models in the training set, reducing its discriminative power. Bias dropped to nearly zero (0.7%) because all responses in the training set had bias scores above 0.97 — with so little variance, the bias dimension contributed almost nothing to distinguishing good from bad responses.

The low train-test R² gap (0.9004 − 0.8900 = 0.0104) indicates negligible overfitting, which is expected given the L2 regularisation and the relatively simple linear model.

Fig 3.7: Ridge Regression Weight Learning Workflow

#### 3.2.5 Sprint Retrospective

**What went well:** The shared model instance pattern worked effectively — the Faithfulness module reuses the DeBERTa model loaded by the Consistency module, and the Answer Relevance module reuses the sentence transformer loaded by the Relevance module. This halved the memory footprint and startup time for RAG mode. The Ridge Regression achieved a strong R² of 0.89, exceeding the 0.8 target.

**What could be improved:** The training dataset of 51 samples is small. A larger dataset with more diverse prompts and more models would likely produce more robust weights. The near-zero bias weight is a consequence of low variance in the training data rather than a reflection of bias being unimportant — future datasets should include more samples with varying toxicity levels.

**Action items for Sprint III:** Build the Streamlit dashboard. Implement batch processing. Design and run validation experiments.





### 3.3 SPRINT III — Dashboard, Batch Processing and Validation

#### 3.3.1 Objectives with User Stories of Sprint III

| Table 3.5: Sprint III User Stories and Acceptance Criteria |
|---|

| Story ID | User Story | Acceptance Criteria |
|----------|-----------|-------------------|
| US-05a | As a user, I want an interactive dashboard for single-prompt evaluation. | Streamlit app with prompt input, three model response text areas, RAG mode toggle, and results display with radar chart. |
| US-04a | As a QA engineer, I want batch processing for large datasets. | Upload CSV/JSON with prompt, model, response columns. Concurrent processing with progress bar. Statistical dashboard with heatmaps and box plots. |
| US-07a | As a developer, I want live LLM integration in the dashboard. | Provider selector for OpenAI, Gemini, and Ollama with API key input. Auto-generate button that queries selected models. |
| US-08a | As a researcher, I want validation experiments with controlled test cases. | 17 test cases across all 6 dimensions. Pass/fail results displayed in the validation tab. Known limitations documented. |

#### 3.3.2 Functional Document

**Streamlit Dashboard (app.py)**

The web dashboard is built with Streamlit and provides three tabs:

1. **Single Evaluation Tab:** Users enter a prompt and up to three model responses. An optional RAG mode toggle enables faithfulness and answer relevance scoring. The weight mode can be switched between static and learned weights. Results are displayed as metric cards with medal icons (gold, silver, bronze), a radar chart comparing all dimensions, and a data table with full scores. In RAG mode, a hallucination analysis expander shows per-claim NLI results.

2. **Batch Analytics Tab:** Users upload a CSV or JSON file with columns for prompt, model, and response (plus an optional context column for RAG). The system processes all rows with a progress bar, groups by prompt for cross-model consistency, and generates an analytics dashboard. The dashboard includes KPI cards (total rows, models, average score, best model), a model ranking table, a radar chart of average scores, score distribution histograms, a heatmap of per-model average scores across dimensions, box plots for each dimension, and a table of the most controversial prompts (highest score variance across models).

3. **Validation Experiments Tab:** Displays the 17 controlled test cases in a table, then runs them on button click. Results are shown as KPI cards (total, passed, failed, accuracy), a detailed results table, and per-metric progress bars showing pass rates.

All evaluation models are cached using Streamlit's cache_resource decorator, so they are loaded only once across reruns and page navigations.

**Batch Processing Pipeline (batch_runner.py)**

The batch runner processes large evaluation datasets from the command line. It loads all evaluation models once, then iterates through the dataset grouped by prompt. Within each prompt group, responses from different models are evaluated, and cross-model consistency is computed using the other models' responses as references. The pipeline supports concurrent processing using Python's ThreadPoolExecutor, enabling parallel evaluation of different prompt groups.

**LLM Provider Integration (llm_providers.py)**

The provider module implements a factory pattern with three providers:

- **OllamaProvider:** Connects to a locally running Ollama instance via its REST API. Supports models like llama3, mistral, gemma, and phi3. Requires Ollama to be installed and running.

- **OpenAIProvider:** Connects to the OpenAI API for models like gpt-4o, gpt-4-turbo, and gpt-3.5-turbo. Requires an API key set via environment variable or UI input.

- **GeminiProvider:** Connects to the Google Gemini API for models like gemini-2.0-flash and gemini-1.5-pro. Requires a Gemini API key.

All providers return a standardised response dictionary with keys: model, response, latency_ms, and provider.

#### 3.3.3 Architecture Document

The dashboard architecture uses Streamlit's session state for data persistence across reruns. Evaluation models are loaded via cached functions that return shared instances. The batch processing pipeline reuses the same model instances for all rows, which is essential for performance — loading four transformer models takes approximately 10–15 seconds, and this cost is paid only once regardless of dataset size.

Fig 3.8: Streamlit Dashboard — Single Evaluation Tab

Fig 3.9: Streamlit Dashboard — Batch Analytics Tab

Fig 3.10: Streamlit Dashboard — Validation Experiments Tab

#### 3.3.4 Outcome of Objectives / Result Analysis

All Sprint III objectives were met. The Streamlit dashboard runs successfully with all three tabs functional. The batch processing pipeline was tested with a sample dataset of 30 rows (10 prompts × 3 models) and produced correct results with concurrent execution. The LLM provider integration was tested with Ollama (local) and confirmed to generate and evaluate responses end-to-end.

The validation experiments (detailed in Chapter 4) achieved an 88% pass rate across 17 test cases, with known failures on borderline cases that expose documented limitations of the underlying models.

#### 3.3.5 Sprint Retrospective

**What went well:** Streamlit's caching mechanism made model loading efficient. The tabbed layout keeps the dashboard organised without navigation complexity. The validation experiments not only verified the framework but also revealed genuine insights about model limitations.

**What could be improved:** The dashboard could benefit from real-time streaming of evaluation progress for large batch jobs. The concurrent processing is limited by the GIL for CPU-bound model inference — GPU acceleration or multiprocessing would improve throughput.
# CHAPTER 4

## RESULTS AND DISCUSSIONS

### 4.1 Project Outcomes

The Meta-Evaluation Framework was successfully developed as a complete, end-to-end system for evaluating and ranking AI model outputs. The final system comprises the following components:

- **7 evaluation modules** (relevance.py, quality.py, bias.py, consistency.py, faithfulness.py, answer_relevance.py, aggregator.py) totalling approximately 800 lines of evaluation logic.
- **A CLI pipeline** (main.py) for command-line evaluation with colored terminal output and CSV export.
- **A Streamlit dashboard** (app.py, 778 lines) with three tabs for interactive evaluation, batch analytics, and validation.
- **A batch processing pipeline** (batch_runner.py) with concurrent execution support.
- **A benchmark runner** (run_benchmark.py) for multi-prompt evaluation across categories.
- **A weight training script** (train_weights.py) implementing Ridge Regression with cross-validation.
- **A visualisation module** (visualise.py) generating five types of publication-ready charts.
- **A validation suite** (validation_experiments.py) with 17 controlled test cases.
- **An LLM provider integration** (llm_providers.py) supporting OpenAI, Gemini, and Ollama.
- **A unit test suite** (test_modules.py, test_rag_modules.py) with tests for all modules.

The framework uses three pretrained transformer models: all-MiniLM-L6-v2 for semantic embeddings (22M parameters), DeBERTa-v3-small for Natural Language Inference (44M parameters), and toxic-bert for toxicity classification (110M parameters). These models run locally without requiring internet access or API keys, making the framework self-contained and free to use.

### 4.2 Performance Evaluation

**Single-Prompt Evaluation Results**

The framework was evaluated on a sample scenario with three model responses of varying quality to the prompt "Explain machine learning in simple terms." The results demonstrate the system's ability to differentiate between response quality levels:

The GPT-4 response — a clear, well-structured explanation with a concrete spam filter example — achieved the highest final score of 0.816. It scored well across all dimensions: Relevance 0.674, Quality 0.872, Bias 0.999, and Consistency 0.750.

The Llama-3 response — a repetitive, incoherent output ("ML is computer learn data computer learn data computer") — received a lower final score of 0.738. Its Quality score of 0.621 correctly reflected the poor vocabulary diversity, and the lower Relevance score of 0.633 captured the weak semantic connection to the prompt.

The Mistral-7B response — a text that starts coherently but contradicts itself by claiming "machine learning is completely useless and does not work at all" — received the lowest final score of 0.714. The Consistency module detected the self-contradiction, assigning a score of just 0.176, which pulled the final score below the repetitive but non-contradictory Llama-3 response.

Fig 4.1: Radar Chart — Model Comparison Across Dimensions

Fig 4.2: Ranking Bar Chart — Final Scores

**Weight Learning Results**

The Ridge Regression model trained on 51 human-rated samples achieved a cross-validated R-squared of 0.890 with a standard deviation of just 0.013 across 5 folds. The full-dataset R-squared was 0.925, with the small train-test gap (0.010) confirming that overfitting was not a concern.

The learned weights differed substantially from the manually assigned static weights. Quality received the highest learned weight at 40.9% (up from 25%), followed by Consistency at 34.2% (up from 15%), Relevance at 24.2% (down from 35%), and Bias at just 0.7% (down from 25%). These shifts make intuitive sense when considered alongside the training data: the strongest differentiator between high-rated and low-rated responses was structural quality (repetitive gibberish versus well-formed paragraphs), followed by logical consistency (coherent versus self-contradictory). Bias had almost no variance in the training set because all responses, including the "bad" ones, were free of explicit toxicity.

Fig 4.3: Weight Comparison — Manual vs Learned Weights

Fig 4.4: Score Distribution Box Plots by Dimension

### 4.3 Validation Results

The validation suite consists of 17 controlled test cases designed to prove that the framework correctly distinguishes good outputs from bad outputs across all six evaluation dimensions. Each test case has a known expected outcome (high or low score), and the framework passes if the actual score matches the expectation relative to a 0.5 threshold.

| Table 4.3: Validation Experiment Results (17 Cases) |
|---|

| Case | Label | Metric | Expected | Score | Result |
|------|-------|--------|----------|-------|--------|
| 1 | Faithful Response | faithfulness | high | ~0.83 | PASS |
| 2 | Hallucinated Response | faithfulness | low | ~0.25 | PASS |
| 3 | Directly Answers Prompt | answer_relevance | high | ~0.72 | PASS |
| 4 | Off-Topic Response | answer_relevance | low | ~0.08 | PASS |
| 5 | Clean, Unbiased Response | bias | high | ~0.99 | PASS |
| 6 | Toxic / Biased Response | bias | low | ~0.12 | PASS |
| 7 | Well-Structured Response | quality | high | ~0.87 | PASS |
| 8 | Gibberish Response | quality | low | ~0.28 | PASS |
| 9 | Relevant to Prompt | relevance | high | ~0.75 | PASS |
| 10 | Self-Contradictory | consistency | low | ~0.29 | PASS |
| 11 | Direct Fact Contradiction | faithfulness | low | ~0.17 | PASS |
| 12 | Completely Irrelevant | relevance | low | ~0.05 | PASS |
| 13 | Highly Repetitive Loop | quality | low | ~0.40 | PASS |
| 14 | Overt Social Insult | bias | low | ~0.03 | PASS |
| 15 | Verbatim Context Mirroring | answer_relevance | low | ~0.32 | PASS |
| 16 | Soft Gender Stereotype | bias | low | ~0.98 | FAIL |
| 17 | Subtle Hallucination | faithfulness | low | ~0.75 | FAIL |

The framework achieved a pass rate of 15 out of 17 cases (88.2%). The two failing cases expose genuine limitations of the underlying models:

**Case 16 (Soft Gender Stereotype):** The response "Women are naturally better suited for nurturing roles" expresses a gender stereotype, but it is phrased politely without profanity or slurs. The toxic-bert model was trained primarily on overtly hateful and offensive text, and it does not flag implicit or socially coded bias. Detecting such subtle stereotypes would require a dedicated fairness classifier trained on stereotype benchmarks.

**Case 17 (Subtle Hallucination):** The response adds a plausible but fabricated detail ("to be taken twice daily with meals") that does not appear in the context. The DeBERTa NLI model classifies this addition as "neutral" rather than "contradiction" because it does not directly contradict the context — it simply goes beyond it. This is a fundamental limitation of NLI-based hallucination detection: the model cannot distinguish between "unverifiable" and "fabricated."

These documented failures are themselves a contribution, as they clearly delineate the boundaries of what the current transformer models can and cannot detect.

Fig 4.6: Validation Pass/Fail Summary

### 4.4 Benchmark Analysis

The multi-prompt benchmark suite evaluates the framework's generalisation across 10 diverse prompts spanning 6 subject categories: technology (machine learning, quantum computing, blockchain), science (climate change, photosynthesis, evolution), biology, health (exercise, vaccines), politics (democracy), and economics (inflation).

For each prompt, the same three model archetypes were used: a high-quality model producing detailed, accurate responses; a low-quality model producing repetitive gibberish; and a contradictory model that undermines its own claims.

| Table 4.4: Benchmark Results — Per-Model Averages (10 Prompts) |
|---|

| Model | Relevance | Quality | Bias | Consistency | Final Score |
|-------|-----------|---------|------|-------------|-------------|
| GPT-4 | ~0.72 | ~0.89 | ~0.998 | ~0.85 | ~0.85 |
| Mistral-7B | ~0.66 | ~0.83 | ~0.997 | ~0.42 | ~0.72 |
| Llama-3 | ~0.50 | ~0.48 | ~0.993 | ~0.70 | ~0.56 |

Key findings from the benchmark:

1. **GPT-4 ranked first on all 10 prompts.** Its consistently high scores across all dimensions — especially Quality and Consistency — produced the highest average final score.

2. **Llama-3 and Mistral-7B alternated for second and third place** depending on whether Quality or Consistency was more heavily weighted for a given prompt. Mistral-7B had better structure (higher Quality) but its self-contradictions (low Consistency) dragged down its score.

3. **Consistency was the most differentiating dimension.** The spread between the best and worst models was largest on this dimension (approximately 0.43 points), confirming that the NLI-based consistency check is the most powerful discriminator in the framework.

4. **Bias had the least variance** (all models above 0.99), which aligns with the near-zero learned weight for this dimension — in datasets without explicit toxicity, the bias module provides little discriminative signal.

Fig 4.5: Benchmark Heatmap — Per-Prompt Scores

### 4.5 Testing Results

The framework includes a comprehensive unit test suite split across two files:

**test_modules.py** (496 lines) contains tests for the Quality module (length scoring, repetition scoring, JSON detection, Markdown detection, combined scoring), the Score Aggregator (default weights, weight sum, perfect/zero scores, weighted calculation, custom weights, learned weight loading, boundary values, random input validation), and ML-dependent tests (relevance scoring, bias detection, consistency checking, full pipeline integration). The ML-dependent tests are marked with @pytest.mark.slow and can be skipped for rapid iteration.

**test_rag_modules.py** (211 lines) contains tests for the RAG-specific components: Aggregator RAG mode (6-dimension scoring, weight configuration, faithfulness impact), Answer Relevance logic (no-context fallback, echo penalty, no-penalty cases), and Faithfulness logic (no-context handling, all-entailed, all-contradicted, mixed, neutral, claim details).

The RAG module tests use mocked model outputs to avoid loading heavy transformer models, enabling fast test execution while still validating the business logic thoroughly.





# CHAPTER 5

## CONCLUSION AND FUTURE ENHANCEMENT

### 5.1 Conclusion

This project has successfully delivered a Meta-Evaluation Framework for AI model outputs that addresses the key limitations identified in existing evaluation methods. The framework evaluates responses across four dimensions in standard mode (Relevance, Quality, Bias, Consistency) and six dimensions in RAG mode (adding Faithfulness and Answer Relevance), using a combination of transformer-based models and rule-based analysis that runs entirely on local hardware without requiring commercial API calls.

The learning-assisted weight optimisation module demonstrates that data-driven approaches can produce more meaningful composite scores than manually assigned weights. The Ridge Regression model, trained on just 51 human-rated samples, achieved a cross-validated R-squared of 0.89, revealing that Quality and Consistency are the most important dimensions for distinguishing high-quality responses from low-quality ones in our dataset.

The validation experiments confirm the framework's discriminative ability across all six dimensions with an 88% pass rate on 17 controlled test cases. The two documented failures — subtle stereotype detection and plausible hallucination detection — are honest acknowledgments of the current limitations of the underlying transformer models, and they point directly to areas for future improvement.

The multi-prompt benchmark across 10 prompts and 6 subject categories validates that the framework generalises beyond individual test cases and consistently produces rankings that align with expected quality ordering.

The interactive Streamlit dashboard makes the framework accessible to non-technical users, while the CLI tools and batch processing pipeline support integration into automated testing workflows. The LLM provider integration enables end-to-end evaluation of live model outputs from OpenAI, Google Gemini, and Ollama.

### 5.2 Future Enhancement

Several directions for future work have been identified:

1. **Expanded training dataset.** The current 51-sample dataset could be expanded to several hundred samples covering more diverse prompts, more models, and a wider range of toxicity levels. This would produce more robust learned weights and particularly address the near-zero bias weight caused by low toxicity variance.

2. **Advanced bias detection.** Replacing or supplementing toxic-bert with a dedicated fairness classifier trained on stereotype and implicit bias datasets would address the Case 16 failure. Models like WinoBias-BERT or FairLex could detect subtle gender, racial, and socioeconomic biases that are missed by toxicity classifiers.

3. **Improved hallucination detection.** The NLI-based approach classifies unverifiable claims as "neutral," which inflates faithfulness scores for responses that add plausible but fabricated details. A fact verification pipeline that combines NLI with information extraction and knowledge graph lookup could provide more precise hallucination detection.

4. **GPU-optimised batch processing.** The current implementation is CPU-bound due to the Python GIL limiting true parallelism. Migrating to GPU-based batch inference with dynamic batching would significantly improve throughput for large-scale evaluations.

5. **Multilingual support.** The current framework is English-only because the underlying models (all-MiniLM-L6-v2, DeBERTa, toxic-bert) are trained primarily on English data. Swapping in multilingual variants (e.g., paraphrase-multilingual-MiniLM-L12-v2) would extend the framework to other languages.

6. **Real-time monitoring.** Integrating the framework into a CI/CD pipeline would enable continuous monitoring of LLM output quality, with automatic alerts when scores drop below configurable thresholds.





## REFERENCES

[1] Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., and Artzi, Y., "BERTScore: Evaluating Text Generation with BERT," Proc. International Conference on Learning Representations (ICLR), 2020.

[2] Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., and Steinhardt, J., "Measuring Massive Multitask Language Understanding," Proc. International Conference on Learning Representations (ICLR), 2021.

[3] Zellers, R., Holtzman, A., Bisk, Y., Farhadi, A., and Choi, Y., "HellaSwag: Can a Machine Really Finish Your Sentence?," Proc. Annual Meeting of the Association for Computational Linguistics (ACL), pp. 4791–4800, 2019.

[4] Hanu, L. and Unitary team, "Detoxify," GitHub Repository, https://github.com/unitaryai/detoxify, 2020.

[5] Papineni, K., Roukos, S., Ward, T., and Zhu, W. J., "BLEU: A Method for Automatic Evaluation of Machine Translation," Proc. Annual Meeting of the Association for Computational Linguistics (ACL), pp. 311–318, 2002.

[6] Lin, C. Y., "ROUGE: A Package for Automatic Evaluation of Summaries," Text Summarization Branches Out, pp. 74–81, 2004.

[7] Fu, J., Ng, S. K., Jiang, Z., and Liu, P., "GPTScore: Evaluate as You Desire," arXiv preprint arXiv:2302.04166, 2023.

[8] Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., and Zhu, C., "G-Eval: NLG Evaluation Using GPT-4 with Better Human Alignment," Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 2511–2522, 2023.

[9] Gehman, S., Gururangan, S., Sap, M., Choi, Y., and Smith, N. A., "RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models," Proc. Findings of the Association for Computational Linguistics (EMNLP), pp. 3356–3369, 2020.

[10] Lees, A., Tran, V. Q., Tay, Y., Sorensen, J., Gupta, J., Metzler, D., and Vasserman, L., "A New Generation of Perspective API: Efficient Multilingual Character-level Transformers," Proc. ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 3197–3207, 2022.

[11] Es, S., James, J., Espinosa Anke, L., and Schockaert, S., "RAGAS: Automated Evaluation of Retrieval Augmented Generation," Proc. Conference of the European Chapter of the Association for Computational Linguistics (EACL), System Demonstrations, pp. 150–163, 2024.

[12] Confident AI, "DeepEval: The Open-Source LLM Evaluation Framework," GitHub Repository, https://github.com/confident-ai/deepeval, 2024.

[13] Kim, S., Shin, J., Cho, Y., Jang, J., Longpre, S., Lee, H., Yun, S., Shin, S., Kim, S., Thorne, J., and Seo, M., "Prometheus: Inducing Fine-Grained Evaluation Capability in Language Models," Proc. International Conference on Learning Representations (ICLR), 2024.

[14] Reimers, N. and Gurevych, I., "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 3982–3992, 2019.

[15] He, P., Liu, X., Gao, J., and Chen, W., "DeBERTa: Decoding-enhanced BERT with Disentangled Attention," Proc. International Conference on Learning Representations (ICLR), 2021.

[16] Devlin, J., Chang, M. W., Lee, K., and Toutanova, K., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," Proc. Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT), pp. 4171–4186, 2019.

[17] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., and Polosukhin, I., "Attention Is All You Need," Proc. Advances in Neural Information Processing Systems (NeurIPS), pp. 5998–6008, 2017.

[18] Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., et al., "Language Models are Few-Shot Learners," Proc. Advances in Neural Information Processing Systems (NeurIPS), pp. 1877–1901, 2020.





## APPENDIX A

### CODING

*(Include key source code files from the project. The following files should be printed:)*

- `modules/relevance.py` — Relevance Analyzer (58 lines)
- `modules/quality.py` — Quality Analyzer (125 lines)
- `modules/bias.py` — Bias Detector (49 lines)
- `modules/consistency.py` — Consistency Analyzer (153 lines)
- `modules/faithfulness.py` — Faithfulness Checker (188 lines)
- `modules/answer_relevance.py` — Answer Relevance Checker (113 lines)
- `modules/aggregator.py` — Score Aggregator (187 lines)
- `train_weights.py` — Weight Training Script (330 lines)
- `main.py` — CLI Entry Point (378 lines)





## APPENDIX B

### SCREENSHOTS

*(Include screenshots of the following:)*

- Streamlit Dashboard — Single Evaluation Tab with results
- Streamlit Dashboard — Batch Analytics with radar chart and heatmap
- Streamlit Dashboard — Validation Experiments results
- CLI output from main.py showing ranked evaluation
- Terminal output from run_benchmark.py showing multi-prompt results
- Charts: radar_chart.png, ranking_bar.png, weight_comparison.png, benchmark_heatmap.png





## APPENDIX C

### PLAGIARISM REPORT

*(Include Turnitin plagiarism report generated with the help of your guide. Similarity index should be less than or equal to 10%.)*
