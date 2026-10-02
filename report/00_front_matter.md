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
