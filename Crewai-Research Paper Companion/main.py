import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import gradio as gr
from typing import Optional
from dotenv import load_dotenv


search_tool = SerperDevTool()

class ResearchPaperCompanion:
    def __init__(self):
        
        self.llm = LLM(
            model="openrouter/qwen/qwen3-235b-a22b-2507:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get('OPENROUTER_API_KEY')
        )
        self.setup_agents()
        self.setup_crew()
    
    def setup_agents(self):
        
        self.topic_explainer = Agent(
            role='Topic Explainer',
            goal='Break down complex research topics into clear, understandable explanations',
            backstory="""You are an expert academic communicator who specializes in making 
            complex research topics accessible. You have a gift for identifying key concepts 
            and explaining them in clear, structured ways.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )
        
      
        self.literature_finder = Agent(
            role='Literature Finder',
            goal='Find and summarize relevant research papers and literature',
            backstory="""You are a skilled research librarian and academic researcher 
            with extensive experience in finding, evaluating, and summarizing academic 
            literature across various fields.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )
        
       
        self.gap_analyzer = Agent(
            role='Gap Analyzer',
            goal='Identify research gaps and suggest future research directions',
            backstory="""You are a strategic research analyst who excels at identifying 
            gaps in current research and suggesting innovative directions for future studies. 
            You have a keen eye for spotting opportunities in academic literature.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )
    
    def setup_crew(self):
        
        pass
    
    def analyze_paper(self, paper_title: str, paper_abstract: str = "", research_area: str = ""):
        
        explain_task = Task(
            description=f"""
            Analyze and explain the research topic: "{paper_title}"
            
            Paper abstract (if provided): {paper_abstract}
            Research area: {research_area}
            
            Provide:
            1. A clear explanation of the main research topic
            2. Key concepts and terminology
            3. The broader context and significance
            4. Why this research matters
            
            Keep explanations accessible but comprehensive.
            """,
            expected_output="A structured explanation of the research topic with key concepts clearly defined",
            agent=self.topic_explainer
        )
       
        literature_task = Task(
            description=f"""
            Find and summarize relevant literature related to: "{paper_title}"
            
            Research area: {research_area}
            
            Provide:
            1. 5-7 key papers in this area
            2. Brief summary of each paper's contribution
            3. How they relate to the main topic
            4. Current trends in this research area
            
            Focus on recent and influential work.
            """,
            expected_output="A comprehensive literature review with summaries of key related papers",
            agent=self.literature_finder
        )
      
       
        gap_task = Task(
            description=f"""
            Based on the topic explanation and literature review, identify research gaps 
            and suggest future directions for: "{paper_title}"
            
            Provide:
            1. Current limitations in the field
            2. Unexplored areas or questions
            3. Methodological gaps
            4. 3-5 specific research directions with rationale
            5. Potential impact of suggested research
            
            Be specific and actionable in your suggestions.
            """,
            expected_output="A detailed analysis of research gaps with specific, actionable research suggestions",
            agent=self.gap_analyzer
        )
        
        
        crew = Crew(
            agents=[self.topic_explainer, self.literature_finder, self.gap_analyzer],
            tasks=[explain_task, literature_task, gap_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result

def create_gradio_interface():
   
    companion = ResearchPaperCompanion()
    
    def process_paper(title, abstract, area):
        if not title.strip():
            return "Please provide a paper title."
        
        try:
            result = companion.analyze_paper(title, abstract, area)
            return str(result)
        except Exception as e:
            return f"Error analyzing paper: {str(e)}"
    
    
    with gr.Blocks(title="AI Research Paper Companion") as demo:
        gr.Markdown("# 🔬 AI Research Paper Companion")
        gr.Markdown("Get comprehensive analysis of research papers with topic explanations, literature reviews, and gap analysis.")
        
        with gr.Row():
            with gr.Column():
                title_input = gr.Textbox(
                    label="Paper Title",
                    placeholder="Enter the research paper title...",
                    lines=2
                )
                abstract_input = gr.Textbox(
                    label="Paper Abstract (Optional)",
                    placeholder="Paste the paper abstract here...",
                    lines=5
                )
                area_input = gr.Textbox(
                    label="Research Area (Optional)",
                    placeholder="e.g., Machine Learning, Natural Language Processing...",
                    lines=1
                )
                analyze_btn = gr.Button("🔍 Analyze Paper", variant="primary")
            
            with gr.Column():
                output = gr.Textbox(
                    label="Analysis Results",
                    lines=20,
                    max_lines=30
                )
        
        analyze_btn.click(
            fn=process_paper,
            inputs=[title_input, abstract_input, area_input],
            outputs=output
        )
        
        
        gr.Examples(
            examples=[
                ["Attention Is All You Need", "", "Natural Language Processing"],
                ["BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "", "Machine Learning"],
                ["Deep Residual Learning for Image Recognition", "", "Computer Vision"]
            ],
            inputs=[title_input, abstract_input, area_input]
        )
    
    return demo

if __name__ == "__main__":
    load_dotenv()
    
    os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')
    os.environ["OPENROUTER_API_KEY"] = os.getenv('OPENROUTER_API_KEY')
    
    print(f'Keys: {os.environ["SERPER_API_KEY"]}, {os.environ["OPENROUTER_API_KEY"]}') #js chekin 
   
    demo = create_gradio_interface()
    demo.launch(share=True)