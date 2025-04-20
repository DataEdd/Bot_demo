from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import aiosqlite
from typing import Optional
from datetime import datetime, date

DB = "ucship.db"
app = FastAPI(title="UC SHIP mini‑API")

# Plan term window for OOP calculations (UC SHIP 2025–26)
TERM_START = date(2025, 9, 15)
TERM_END = date(2026, 9, 13)

# ─────────── helpers ───────────
async def fetch_all(db, query, params=()):
    cur = await db.execute(query, params)
    rows = await cur.fetchall()
    return [dict(r) for r in rows]

async def fetch_one(db, query, params=()):
    cur = await db.execute(query, params)
    row = await cur.fetchone()
    return dict(row) if row else None

# ─────────── READ endpoints ───────────
@app.get("/students/{uid}")
async def get_student(uid: str):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        row = await fetch_one(db,
            "SELECT * FROM students WHERE uc_student_uid = ?", (uid,))
        if not row:
            raise HTTPException(404, "Student not found")
        return row

@app.get("/visits")
async def get_visits(
    uid: str,
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row

        query = "SELECT * FROM visits WHERE uc_student_uid = ?"
        params = [uid]

        if start_date:
            query += " AND visit_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND visit_date <= ?"
            params.append(end_date)

        cur = await db.execute(query, params)
        rows = await cur.fetchall()
        return [dict(row) for row in rows]

@app.get("/policy")
async def get_policy(campus: str, plan_year: str):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        row = await fetch_one(db, """
            SELECT p.*
              FROM policy_parameters p
              JOIN plan_years y ON p.plan_year_id = y.plan_year_id
             WHERE y.year_label = ? AND p.campus_flag = ?
        """, (plan_year, campus))
        if not row:
            raise HTTPException(404, "Policy not found")
        return row

@app.get("/oop_total")
async def get_oop_total(uid: str):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row

        row = await db.execute_fetchone(
            """
            SELECT SUM(student_paid) AS total_oop, oop_max_in
            FROM claims
            WHERE uc_student_uid = ?
              AND processed_date BETWEEN ? AND ?
            """,
            (uid, TERM_START.isoformat(), TERM_END.isoformat())
        )

        if row is None or row["total_oop"] is None:
            return {"uid": uid, "oop_total": 0.0, "status": "no claims found"}

        oop_total = row["total_oop"]
        oop_max_in = row["oop_max_in"]

        # If the OOP max has been reached, user pays $0
        if oop_total >= oop_max_in:
            return {"uid": uid, "oop_total": oop_total, "status": "OOP max reached", "you_pay": 0.0}

        return {"uid": uid, "oop_total": oop_total, "status": "within OOP max", "you_pay": oop_max_in - oop_total}

@app.get("/prediction_history")
async def prediction_history(uid: str):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row

        query = """
        SELECT p.prediction_id, v.visit_date, p.predicted_range_min, p.predicted_range_max,
               r.actual_student_paid, r.error_amount, r.error_pct
        FROM predictions p
        JOIN visits v ON p.visit_id = v.visit_id
        LEFT JOIN prediction_results r ON p.prediction_id = r.prediction_id
        WHERE p.uc_student_uid = ?
        ORDER BY v.visit_date DESC
        """

        rows = await db.execute_fetchall(query, (uid,))
        return [dict(row) for row in rows]

# ─────────── WRITE endpoints ───────────
class VisitIn(BaseModel):
    uc_student_uid: str
    provider_id: int
    cpt_code: str
    visit_date: str
    visit_type: Optional[str] = None
    is_in_network: Optional[bool] = None

@app.post("/visits", status_code=201)
async def add_visit(v: VisitIn):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("""
            INSERT INTO visits(
                uc_student_uid, provider_id, cpt_code,
                visit_date, visit_type, is_in_network
            ) VALUES (?,?,?,?,?,?)
        """, (v.uc_student_uid, v.provider_id, v.cpt_code,
              v.visit_date, v.visit_type, v.is_in_network))
        await db.commit()
        return {"visit_id": cur.lastrowid}

class PredIn(BaseModel):
    uc_student_uid: str
    visit_id: Optional[int] = None
    cpt_code: Optional[str] = None
    youpay_low: float
    youpay_high: float

@app.post("/predictions", status_code=201)
async def add_prediction(p: PredIn):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO predictions(
                uc_student_uid, visit_id, cpt_code,
                predicted_range_min, predicted_range_max
            ) VALUES (?,?,?,?,?)
        """, (p.uc_student_uid, p.visit_id, p.cpt_code,
              p.youpay_low, p.youpay_high))
        await db.commit()
    return {"status": "logged"}

@app.post("/prediction_results")
async def log_prediction_result(prediction_id: int):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row

        pred = await fetch_one(db, "SELECT * FROM predictions WHERE prediction_id = ?", (prediction_id,))
        if not pred or not pred["visit_id"]:
            raise HTTPException(404, "Prediction or visit not found")

        claim = await fetch_one(db, "SELECT * FROM claims WHERE visit_id = ?", (pred["visit_id"],))
        if not claim:
            raise HTTPException(404, "No claim for that visit")

        actual = claim["student_paid"]
        predicted = pred["predicted_total"] if "predicted_total" in pred and pred["predicted_total"] else (pred["predicted_range_min"] + pred["predicted_range_max"]) / 2
        error = abs(actual - predicted)
        error_pct = round(error / predicted * 100, 2) if predicted else 0.0

        await db.execute("""
            INSERT INTO prediction_results (
                prediction_id, actual_student_paid, error_amount, error_pct
            ) VALUES (?, ?, ?, ?)
        """, (prediction_id, actual, error, error_pct))
        await db.commit()

        return {
            "status": "logged",
            "prediction_id": prediction_id,
            "actual": actual,
            "predicted": predicted,
            "error": error,
            "error_pct": error_pct
        }

@app.post("/superbill", status_code=201)
async def log_superbill(claim_id: int, billed_amount: float, insurance_paid: float, student_paid: float, services_provided: str, additional_charges: float, adjustments: float, date_of_service: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO superbill(
                claim_id, billed_amount, insurance_paid, student_paid, 
                services_provided, additional_charges, adjustments, date_of_service
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (claim_id, billed_amount, insurance_paid, student_paid, services_provided, additional_charges, adjustments, date_of_service))
        await db.commit()
    return {"status": "superbill logged"}

@app.post("/update_prediction_results", status_code=200)
async def update_prediction_results(prediction_id: int, actual_student_paid: float):
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row

        # Fetch the prediction record
        prediction = await fetch_one(db, "SELECT * FROM predictions WHERE prediction_id = ?", (prediction_id,))
        if not prediction or not prediction["visit_id"]:
            raise HTTPException(404, "Prediction or visit not found")

        # Fetch the related claim
        claim = await fetch_one(db, "SELECT * FROM claims WHERE visit_id = ?", (prediction["visit_id"],))
        if not claim:
            raise HTTPException(404, "No claim for that visit")

        # Calculate the error and error percentage
        predicted = prediction["predicted_total"] if "predicted_total" in prediction else (prediction["predicted_range_min"] + prediction["predicted_range_max"]) / 2
        error = abs(actual_student_paid - predicted)
        error_pct = round(error / predicted * 100, 2) if predicted else 0.0

        # Update the prediction results
        await db.execute("""
            INSERT INTO prediction_results (
                prediction_id, actual_student_paid, error_amount, error_pct
            ) VALUES (?, ?, ?, ?)
        """, (prediction_id, actual_student_paid, error, error_pct))
        await db.commit()

    return {"status": "prediction result updated", "error_pct": error_pct}
