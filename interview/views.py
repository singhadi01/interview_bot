from django.shortcuts import render, redirect
import tempfile
from backend import workflow, stop_requested, load_pdf_text


def interview_page(request):
    return render(request, "interview.html")


def start_interview(request):
    return redirect("/interview/?instruction=1")  


def process_interview(request):
    if request.method == "POST":
        jd = request.POST.get("job_description")
        resume_file = request.FILES.get("resume")

        if not resume_file or not jd:
            return render(request, "interview.html", {"error": "Missing resume or JD!"})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in resume_file.chunks():
                tmp.write(chunk)
            resume_text = load_pdf_text(tmp.name)

        state = {"job_description": jd, "resume": resume_text}
        result = workflow.invoke(state)
        feedback = result.get("feedback", [])
        return render(request, "interview.html", {"feedback": feedback})

    return redirect("interview_home")


def stop_interview(request):
    stop_requested()
    return redirect("interview_home")
