# SHIPSmart

## Inspiration 

With sharply rising insurance premiums, students at UC Davis frequently underutilize their UC SHIP benefits, missing critical preventative care and cost-saving opportunities. There's a clear need to bridge the gap between available coverage and student awareness.

Our solution provides UC SHIP enrollees with a personalized, AI-driven insurance companion that simplifies coverage details, promotes timely preventive care, and prevents unexpected medical bills.

## Key Objectives

1. Boost awareness and use of preventative care

2. Support underutilizers with targeted analytics

3. Simplify policy navigation and referrals

4. Reduce unexpected costs with AI-driven negotiation

5. Streamline appointment booking and network usage

## How we built it

Designed the app on figma. Implemented frontend using swiftui. Cerebas for AI. Regression model. Letta framework to build complex agent + API call.

## Challenges we ran into

Data scrapping Anthem's site for providers were incredibly difficult. Meaning our in-network provider table is most definitely incomplete. The solution is applying for the Anthem which we have done and waiting access.

## Accomplishments that we're proud of

## What we learned

## What's next for SHIPSmart

## Demo Video




## Modeling log:

Benefit Extraction

Parsed the UC‑Davis Anthem Benefit Book PDF into structured text (ExtractText.py → UCD‑Anthem‑Benefit‑Book.txt).

Extracted key policy parameters (deductibles, copays, coinsurance, OOP limits) into a Python script (ExtractBenefit.py) and loaded them into Postgres (policy_parameters table).

Database & Sample Data

Defined the schema in create_shipsmart_db.sql (tables: policy_parameters, visits, claims).

Populated policy_parameters via InsertPolicy.sql.

Created a small sample dataset under data/ (visits.csv, claims.csv) and loaded it with \copy.

Feature Engineering in SQL

visit_policy view: joins each visit to its plan’s parameters.

visit_features view: running sums of student payments → deductible remaining.

training_data view: computes

service_copay based on CPT code ranges (ER, primary care, imaging)

coinsurance_share = (allowed_amount – deductible_remaining – copay) × coinsurance%, floored at zero

actual student_pay (target).

MVP Regression Pipeline

Exported training_data → data/training_data.csv.

Wrote model.py to load the CSV, train a baseline LinearRegression on two features (service_copay, coinsurance_share), and report MAE.



