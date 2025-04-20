PRAGMA foreign_keys = ON;      -- enforce FK constraints in SQLite

-- ===== reference tables =====
CREATE TABLE plan_years (
  plan_year_id INTEGER PRIMARY KEY AUTOINCREMENT,
  year_label   TEXT UNIQUE NOT NULL
);

-- ===== students =====
CREATE TABLE students (
  uc_student_uid TEXT PRIMARY KEY,
  campus         TEXT NOT NULL,
  first_name     TEXT,
  last_name      TEXT,
  email          TEXT,
  date_of_birth  DATE,
  deductible_met REAL  DEFAULT 0.0,
  oop_met        REAL  DEFAULT 0.0,
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== providers =====
CREATE TABLE providers (
  provider_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT,
  npi             TEXT,
  specialty       TEXT,
  network_status  TEXT,
  accepts_uc_ship INTEGER,
  contact_info    TEXT,
  location        TEXT
);

-- ===== policy_parameters =====
CREATE TABLE policy_parameters (
  policy_param_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  plan_year_id           INTEGER REFERENCES plan_years(plan_year_id),
  campus_flag            TEXT,
  deductible_in_network  REAL,
  deductible_oon         REAL,
  er_copay               REAL,
  urgent_care_copay      REAL,
  specialist_copay       REAL,
  imaging_copay          REAL,
  coinsurance_in         REAL,
  coinsurance_oon        REAL,
  oop_max_in             REAL,
  oop_max_oon            REAL,
  pharmacy_tier_1        REAL,
  pharmacy_tier_2        REAL,
  pharmacy_tier_3        REAL,
  vision_exam_copay      REAL,
  dental_cleaning_pct    REAL,
  created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== visits =====
CREATE TABLE visits (
  visit_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  uc_student_uid  TEXT    REFERENCES students(uc_student_uid),
  visit_date      DATE    NOT NULL,
  provider_id     INTEGER REFERENCES providers(provider_id),
  cpt_code        TEXT,
  visit_type      TEXT,
  referral_obtained INTEGER,
  is_in_network     INTEGER,
  location        TEXT,
  status          TEXT DEFAULT 'pending'
);

-- ===== predictions =====
CREATE TABLE predictions (
  prediction_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  uc_student_uid      TEXT    REFERENCES students(uc_student_uid),
  visit_id            INTEGER REFERENCES visits(visit_id),
  model_version       TEXT,
  predicted_total     REAL,
  predicted_breakdown TEXT,
  predicted_range_min REAL,
  predicted_range_max REAL,
  confidence_score    REAL,
  created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== claims =====
CREATE TABLE claims (
  claim_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  uc_student_uid  TEXT    REFERENCES students(uc_student_uid),
  visit_id        INTEGER REFERENCES visits(visit_id),
  billed_amount   REAL,
  allowed_amount  REAL,
  student_paid    REAL,
  insurance_paid  REAL,
  claim_status    TEXT,
  processed_date  DATE
);

-- ===== prediction_results =====
CREATE TABLE prediction_results (
  result_id           INTEGER PRIMARY KEY AUTOINCREMENT,
  prediction_id       INTEGER REFERENCES predictions(prediction_id),
  actual_student_paid REAL,
  error_amount        REAL,
  error_pct           REAL,
  comparison_notes    TEXT,
  result_logged_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== superbill =====
CREATE TABLE superbill (
  superbill_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  claim_id             INTEGER REFERENCES claims(claim_id),
  billed_amount        REAL,
  insurance_paid       REAL,
  student_paid         REAL,
  services_provided    TEXT,  -- Service names or CPT codes
  additional_charges   REAL,  -- Any extra charges (e.g., for specific tests)
  adjustments          REAL,  -- Any adjustments made to the billed amount
  date_of_service      DATE,
  created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ===== helpful indexes =====
CREATE INDEX idx_visits_student      ON visits(uc_student_uid);
CREATE INDEX idx_predictions_student ON predictions(uc_student_uid);
CREATE INDEX idx_claims_student      ON claims(uc_student_uid);
