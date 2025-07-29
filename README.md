# AI Research Paper Companion

This project is an interactive assistant for analyzing academic research papers using autonomous agents powered by large language models. It breaks down complex topics, retrieves relevant literature, and suggests future research directions through a Gradio-based user interface.

---

## Features

* **Topic Explanation**: Breaks down the research paper’s core ideas and key terminology.
* **Literature Review**: Retrieves and summarizes 5–7 relevant academic papers using live web search.
* **Gap Analysis**: Identifies research gaps and proposes actionable future research directions.

---

## Technologies Used

* [CrewAI](https://github.com/joaomdmoura/crewAI): Agent orchestration framework
* [OpenRouter](https://openrouter.ai): LLM provider (Qwen 235B model)
* [Serper.dev](https://serper.dev): Google Search API integration
* [Gradio](https://gradio.app): Web UI interface

---

## Setup Instructions

1. **Install dependencies**:

   ```bash
   pip install crewai crewai-tools gradio python-dotenv
   ```

2. **Set environment variables** in a `.env` file:

   ```
   OPENROUTER_API_KEY=your_openrouter_key
   SERPER_API_KEY=your_serper_dev_key
   ```

3. **Run the app**:

   ```bash
   python your_script.py
   ```

4. The Gradio interface will launch locally or via public link (if `share=True` is enabled).

![reuslt](/assets/t1.png)

![reuslt](/assets/t2.png)

---

## Example Queries

* "Attention Is All You Need" (NLP)
* "BERT: Pre-training of Deep Bidirectional Transformers" (Machine Learning)
* "Deep Residual Learning for Image Recognition" (Computer Vision)

---

## Output Includes

![reuslt](/assets/result.png)

* Clear explanation of the research focus
* Summarized key papers with relevance
* Identified limitations and new research suggestions

---

## License

MIT License
