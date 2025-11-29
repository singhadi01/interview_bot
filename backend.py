# %%
from langchain_community.document_loaders import PyPDFLoader
def load_pdf_text(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()      
    text = "\n".join(p.page_content for p in pages if p.page_content)
    return text

# %%
from langgraph.graph import StateGraph,START,END
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)
model=ChatHuggingFace(llm=llm)

# %%
schema = {
    "name": "InterviewQuestions",
    "description": "Schema that returns 10 interview questions as a list",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "description": "List of 10 interview questions",
                "items": {"type": "string"}
            }
        },
        "required": ["questions"]
    }
}

question_model = model.with_structured_output(schema)

# %%
schema2 = {
    "name": "InterviewFeedback",
    "description": "Schema that returns interview feedback points as a list",
    "parameters": {
        "type": "object",
        "properties": {
            "feedback": {
                "type": "array",
                "description": "List of feedback comments",
                "items": {"type": "string"}
            }
        },
        "required": ["feedback"]
    }
}

feedback_model = model.with_structured_output(schema2)


# %%

class chatstate(TypedDict):
    job_description: str
    resume: str 
    questions: list[str]
    answers: list[str]
    feedback: str
    

# %%
def generate_questions(state: chatstate):
    
    prompt=f"""Given the following job description and resume, generate a list of 10 relevant interview questions.
    Job Description: {state["job_description"]}
    Resume: {state["resume"]}
    Questions:[] """
    response=question_model.invoke(prompt)
    print("Questions_model:",response)
    state["questions"]=response["questions"]
    return state

# %%
stop=False
def stop_requested():
    global stop
    stop=True
def ask_questions(state: chatstate):
    from tts import tts_play
    import speech_recognition as sr
    import time

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 3
    recognizer.energy_threshold = 300
    answers = []
    for question in state["questions"]:
        global stop
        if stop:
            print("I am stopping now")
            stop=False
            state["answers"] = answers 
            return state
        tts_play(question)

        with sr.Microphone() as source:
            tts_play("Answer now") 
            print("Listening... (stay silent 5s to skip)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5) 
            start = time.time()
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=90)
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                answers.append(text)
            except sr.WaitTimeoutError:
                if time.time() - start >= 5:
                    print("No speech for 5s, skipping...")
                    answers.append(None)
                else:
                    answers.append(None)
            except Exception:
                print("Didn't catch, skipping...")
                answers.append(None)

    state["answers"] = answers 
    return state


# %%
def generate_feedback(state: chatstate):
    prompt = f"""
    You are an expert interview evaluator.
    Given interview Questions and Answers from a candidate, generate constructive, specific, and actionable feedback.
    Instructions:
    - Analyze each question and its corresponding answer
    - Point out what is missing, unclear, incorrect, or could be stronger
    - Suggest improvements in communication, structure, and technical depth
    - Keep feedback professional, encouraging, and practical
    - If any answer is None or empty, include a feedback comment saying "No answer provided for question"
    Return the feedback strictly as a JSON object that matches this format:
    {{"feedback": ["comment 1", "comment 2", "comment 3", ...]}}
    Now evaluate:
    Questions: {state['questions']}
    Answers: {state["answers"]}
    """
    response=feedback_model.invoke(prompt)
    print("feedback_model",response)
    state["feedback"]=response
    return state

# %%
graph=StateGraph(chatstate)
graph.add_node('generate_questions',generate_questions)
graph.add_node('ask_questions',ask_questions)
graph.add_node('generate_feedback',generate_feedback)

graph.add_edge(START,'generate_questions')
graph.add_edge('generate_questions','ask_questions')
graph.add_edge('ask_questions','generate_feedback')
graph.add_edge('generate_feedback',END)

workflow=graph.compile()
