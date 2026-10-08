from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
import sqlite3, json, secrets, string
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
DB = BASE / 'findyourfriend.db'
FRONTEND = BASE / 'frontend'

app = FastAPI(title='Find Your Real Friend API', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = db()
    con.executescript('''
    CREATE TABLE IF NOT EXISTS creators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        gender TEXT NOT NULL CHECK(gender IN ('Male','Female')),
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_code TEXT UNIQUE NOT NULL,
        creator_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        gender TEXT NOT NULL,
        questions_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(creator_id) REFERENCES creators(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        friend_name TEXT NOT NULL,
        relationship TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'In Progress',
        started_at TEXT NOT NULL,
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        friend_name TEXT NOT NULL,
        relationship TEXT NOT NULL,
        answers_json TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        result TEXT NOT NULL,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    );
    ''')
    con.commit(); con.close()

init_db()

class Question(BaseModel):
    question: str
    options: list[str] = Field(min_length=3)
    correctAnswer: str

class CreateQuiz(BaseModel):
    creator_token: str
    creator_name: str
    gender: str
    title: str = 'My Friendship Quiz'
    questions: list[Question] = Field(min_length=10, max_length=15)

class Submission(BaseModel):
    friend_name: str = Field(min_length=1, max_length=80)
    relationship: str = Field(min_length=1, max_length=60)
    answers: list[str]

RELATIONSHIPS = {
    'Girlfriend','Boyfriend','Best Friend','Friend','Brother','Sister','Cousin','Cousin Brother','Cousin Sister','Nephew','Niece','Classmate','School Friend','College Friend','Online Friend','Online Best Friend','Gaming Friend','Childhood Friend','Neighbor','Teammate','Colleague','Roommate','Fiancé/Fiancée','Brother-in-law','Sister-in-law'
}

def code(n=8):
    alphabet = string.ascii_uppercase + string.digits
    con = db()
    while True:
        value = ''.join(secrets.choice(alphabet) for _ in range(n))
        if not con.execute('SELECT 1 FROM quizzes WHERE quiz_code=?', (value,)).fetchone():
            con.close(); return value

def result_label(score,total):
    pct = (score/total*100) if total else 0
    if pct == 100: return 'Very Good Friend'
    if pct >= 70: return 'Good Friend'
    if pct >= 50: return 'Average Friend'
    return 'Fake Friend'

def creator_for_token(token):
    con=db(); row=con.execute('SELECT * FROM creators WHERE token=?',(token,)).fetchone(); con.close(); return row

@app.get('/api/health')
def health(): return {'status':'ok','service':'find-your-real-friend','database':'sqlite'}

@app.post('/api/quizzes')
def create_quiz(payload: CreateQuiz):
    if payload.gender not in {'Male','Female'}: raise HTTPException(400,'Gender must be Male or Female.')
    if any(q.correctAnswer not in q.options for q in payload.questions): raise HTTPException(400,'Every correct answer must exist in its question options.')
    creator = creator_for_token(payload.creator_token)
    con=db()
    if not creator:
        con.execute('INSERT INTO creators(token,name,gender,created_at) VALUES(?,?,?,?)',(payload.creator_token,payload.creator_name.strip(),payload.gender,datetime.now(timezone.utc).isoformat()))
        con.commit(); creator=con.execute('SELECT * FROM creators WHERE token=?',(payload.creator_token,)).fetchone()
    quiz_code=code()
    con.execute('INSERT INTO quizzes(quiz_code,creator_id,title,gender,questions_json,created_at) VALUES(?,?,?,?,?,?)',(quiz_code,creator['id'],payload.title.strip() or 'My Friendship Quiz',payload.gender,json.dumps([q.model_dump() for q in payload.questions]),datetime.now(timezone.utc).isoformat()))
    con.commit(); con.close()
    return {'quiz_code':quiz_code,'creator_token':payload.creator_token,'title':payload.title}

@app.get('/api/quizzes/{quiz_code}')
def get_quiz(quiz_code: str):
    con=db(); row=con.execute('SELECT quiz_code,title,gender,questions_json FROM quizzes WHERE quiz_code=?',(quiz_code,)).fetchone(); con.close()
    if not row: raise HTTPException(404,'Quiz not found.')
    questions=json.loads(row['questions_json'])
    # The creator's selected correct answer MUST always be present.
    # Friends get exactly 3 choices: 1 correct + 2 wrong choices.
    # We never send correctAnswer itself to the browser.
    rng = secrets.SystemRandom()
    public=[]
    for q in questions:
        correct=q['correctAnswer']
        wrong=[option for option in q['options'] if option != correct]
        if len(wrong) < 2:
            raise HTTPException(500, 'Each question must have at least 3 answer options.')
        selected_wrong=rng.sample(wrong, 2)
        options=[correct, *selected_wrong]
        rng.shuffle(options)
        public.append({'question':q['question'],'options':options})
    return {'quiz_code':row['quiz_code'],'title':row['title'],'gender':row['gender'],'questions':public}

@app.post('/api/quizzes/{quiz_code}/attempts')
def start_attempt(quiz_code: str, payload: Submission):
    if payload.relationship not in RELATIONSHIPS: raise HTTPException(400,'Invalid relationship.')
    con=db(); row=con.execute('SELECT id FROM quizzes WHERE quiz_code=?',(quiz_code,)).fetchone()
    if not row: con.close(); raise HTTPException(404,'Quiz not found.')
    cur=con.execute('INSERT INTO attempts(quiz_id,friend_name,relationship,status,started_at) VALUES(?,?,?,?,?)',(row['id'],payload.friend_name.strip(),payload.relationship,'In Progress',datetime.now(timezone.utc).isoformat()))
    con.commit(); aid=cur.lastrowid; con.close(); return {'attempt_id':aid,'status':'In Progress'}

@app.post('/api/quizzes/{quiz_code}/submissions')
def submit(quiz_code: str, payload: Submission):
    if payload.relationship not in RELATIONSHIPS: raise HTTPException(400,'Invalid relationship.')
    con=db(); row=con.execute('SELECT * FROM quizzes WHERE quiz_code=?',(quiz_code,)).fetchone()
    if not row: con.close(); raise HTTPException(404,'Quiz not found.')
    questions=json.loads(row['questions_json'])
    if len(payload.answers)!=len(questions): con.close(); raise HTTPException(400,'Please answer every question.')
    score=sum(1 for i,q in enumerate(questions) if payload.answers[i]==q['correctAnswer'])
    total=len(questions); label=result_label(score,total)
    cur=con.execute('INSERT INTO submissions(quiz_id,friend_name,relationship,answers_json,score,total,result,submitted_at) VALUES(?,?,?,?,?,?,?,?)',(row['id'],payload.friend_name.strip(),payload.relationship,json.dumps(payload.answers),score,total,label,datetime.now(timezone.utc).isoformat()))
    con.commit(); sid=cur.lastrowid
    con.execute("UPDATE attempts SET status='Completed' WHERE quiz_id=? AND friend_name=? AND relationship=? AND status='In Progress'",(row['id'],payload.friend_name.strip(),payload.relationship))
    con.commit(); con.close()
    return {'submission_id':sid,'score':score,'total':total,'result':label}

@app.get('/api/submissions/{submission_id}')
def get_submission(submission_id:int):
    con=db(); row=con.execute('''SELECT s.*,q.quiz_code,q.title,q.questions_json FROM submissions s JOIN quizzes q ON q.id=s.quiz_id WHERE s.id=?''',(submission_id,)).fetchone(); con.close()
    if not row: raise HTTPException(404,'Submission not found.')
    questions=json.loads(row['questions_json']); answers=json.loads(row['answers_json'])
    details=[]
    for i,q in enumerate(questions):
        chosen=answers[i] if i<len(answers) else ''
        details.append({'question':q['question'],'selected':chosen,'correct':q['correctAnswer'],'is_correct':chosen==q['correctAnswer']})
    return {'submission_id':submission_id,'quiz_code':row['quiz_code'],'title':row['title'],'friend_name':row['friend_name'],'relationship':row['relationship'],'score':row['score'],'total':row['total'],'result':row['result'],'submitted_at':row['submitted_at'],'details':details}

@app.get('/api/dashboard')
def dashboard(token: str = Query(...)):
    creator=creator_for_token(token)
    if not creator: raise HTTPException(404,'Creator dashboard not found on this device.')
    con=db(); quizzes=con.execute('SELECT id,quiz_code,title,gender,created_at FROM quizzes WHERE creator_id=? ORDER BY id DESC',(creator['id'],)).fetchall()
    out=[]
    for q in quizzes:
        subs=con.execute('SELECT id,friend_name,relationship,score,total,result,submitted_at FROM submissions WHERE quiz_id=? ORDER BY id DESC',(q['id'],)).fetchall()
        attempts=con.execute("SELECT id,friend_name,relationship,status,started_at FROM attempts WHERE quiz_id=? ORDER BY id DESC",(q['id'],)).fetchall()
        out.append({'quiz_code':q['quiz_code'],'title':q['title'],'gender':q['gender'],'created_at':q['created_at'],'submissions':[dict(s) for s in subs],'attempts':[dict(a) for a in attempts]})
    con.close(); return {'creator':{'name':creator['name'],'gender':creator['gender']},'quizzes':out}

@app.delete('/api/submissions/{submission_id}')
def remove_submission(submission_id:int, token:str=Query(...)):
    creator=creator_for_token(token)
    if not creator: raise HTTPException(404,'Creator not found.')
    con=db(); row=con.execute('''SELECT s.id FROM submissions s JOIN quizzes q ON q.id=s.quiz_id WHERE s.id=? AND q.creator_id=?''',(submission_id,creator['id'])).fetchone()
    if not row: con.close(); raise HTTPException(404,'Submission not found for this creator.')
    con.execute('DELETE FROM submissions WHERE id=?',(submission_id,)); con.commit(); con.close(); return {'deleted':True}

@app.get('/q/{quiz_code}')
def public_quiz_page(quiz_code: str):
    con=db(); exists=con.execute('SELECT 1 FROM quizzes WHERE quiz_code=?',(quiz_code.upper(),)).fetchone(); con.close()
    if not exists: raise HTTPException(404,'Quiz not found.')
    return FileResponse(FRONTEND / 'take-quiz.html')

# Serve the complete frontend from the same server. This makes localhost and production use the same-origin /api path.
app.mount('/', StaticFiles(directory=FRONTEND, html=True), name='frontend')
