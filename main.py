from fastapi import FastAPI, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
import markdown
from database import SessionLocal, engine
import models, services
import shutil

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/check-grammar/")
def grammar_check(text: str = Form(...)):
    return {"corrections": services.check_grammar(text)}

@app.post("/upload-markdown/")
def upload_markdown(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")
    html_content = markdown.markdown(content)

    note = models.Note(title=file.filename, content=content, html_content=html_content)
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return {"message": "Markdown file uploaded successfully!", "note": note}

@app.get("/notes/")
def list_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@app.get("/render-note/{note_id}")
def render_markdown(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        return {"error": "Note not found"}
    return {"title": note.title, "html_content": note.html_content}
