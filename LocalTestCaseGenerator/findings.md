# Findings & Research

## Project Goals
- Build a Local LLM Testcase Generator.
- Use Ollama for LLM inference.

## Constraints
- Local execution required.
- Must follow B.L.A.S.T. protocol.

## Research Notes
- **Best Practices**: Focus on semantic unit tests (correctness of meaning vs exact string match).
- **Diversity**: Ensure test cases cover edge cases, diverse topics, and varying complexity.
- **Automation**: Use scripts to generate questions (JSON) and exact responses from Ollama.
- **Tools**: Consider using `llm-benchmark` concepts for throughput testing if relevant.
