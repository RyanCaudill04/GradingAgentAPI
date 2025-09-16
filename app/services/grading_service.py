from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.schemas.grading import GradingRequest
from app.db import models
from app.schemas.grading_result import GradingResult as GradingResultSchema
import tempfile
import subprocess
import os

async def save_criteria(assignment_name: str, criteria_file: UploadFile, db: Session):
    assignment = db.query(models.Assignment).filter(models.Assignment.name == assignment_name).first()
    if not assignment:
        assignment = models.Assignment(name=assignment_name)
        db.add(assignment)
        db.commit()
        db.refresh(assignment)

    criteria_text = await criteria_file.read()
    criteria = db.query(models.Criteria).filter(models.Criteria.assignment_id == assignment.id).first()
    if criteria:
        criteria.text = criteria_text.decode("utf-8")
    else:
        criteria = models.Criteria(assignment_id=assignment.id, text=criteria_text.decode("utf-8"))
        db.add(criteria)
    
    db.commit()
    return {"message": f"Criteria for {assignment_name} saved."}

async def grade_assignment(request: GradingRequest, db: Session) -> dict:
    repo_url = str(request.repo_link)
    authenticated_url = repo_url.replace("https://", f"https://oauth2:{request.token}@")

    assignment = db.query(models.Assignment).filter(models.Assignment.name == request.assignment_name).first()
    if not assignment or not assignment.criteria:
        raise HTTPException(status_code=404, detail=f"Grading criteria for '{request.assignment_name}' not found.")

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            subprocess.run(
                ["git", "clone", authenticated_url, temp_dir],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=400, detail=f"Failed to clone repository: {e.stderr}")

        assignment_path = os.path.join(temp_dir, request.assignment_name)

        if not os.path.isdir(assignment_path):
            raise HTTPException(status_code=404, detail=f"Assignment folder '{request.assignment_name}' not found in the repository.")

        source_files = []
        for root, _, files in os.walk(assignment_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    source_files.append({"path": file_path, "content": content})
        
        if not source_files:
            raise HTTPException(status_code=404, detail=f"No Java files found in '{request.assignment_name}'.")

        grading_result = await _grade_with_gemini(source_files, assignment.criteria.text)

        # Save the grading result
        student_id = "student_placeholder" # You would get this from the request or auth
        new_grading_result = models.GradingResult(
            assignment_id=assignment.id,
            student_id=student_id,
            grade=grading_result["grade"],
            feedback=grading_result["feedback"]
        )
        db.add(new_grading_result)
        db.commit()

        return {
            "message": "Assignment analysis complete.",
            "assignment_name": request.assignment_name,
            "grading_result": grading_result
        }

async def _grade_with_gemini(source_files: list, criteria: str) -> dict:
    prompt = """
    Please grade the following Java code based on the provided criteria.
    The criteria specifies deductions for certain issues.
    Start with a grade of 100 and apply deductions as listed.
    For each deduction, please specify the file, the issue, and the line number where the issue was found.

    Criteria:
    ---
    {criteria}
    ---

    Source Code:
    ---
    """
    for file in source_files:
        prompt += f"File: {file['path']}\n"
        prompt += f"{file['content']}\n---\n"

    # Mocking a response from Gemini
    print(prompt)
    return {
        "grade": 90,
        "feedback": "-10 points: Use of raw types in Factory.java line 25.",
        "prompt": prompt # for debugging
    }

async def get_all_grades(db: Session):
    results = db.query(models.GradingResult).options(joinedload(models.GradingResult.assignment)).all()
    # We need to manually construct the response to include the assignment name
    response = []
    for result in results:
        response.append(
            GradingResultSchema(
                assignment_name=result.assignment.name,
                student_id=result.student_id,
                grade=result.grade,
                feedback=result.feedback,
            )
        )
    return response
