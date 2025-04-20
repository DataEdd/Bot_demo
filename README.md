# SHIPSmart

## Inspiration 

Have you ever walked out of a doctor's appointment, already exhausted from the wait, only to be hit with a surprise bill that leaves your jaw on the floor? We've all been there. The expectation? Spend the next few weeks battling with insurance companies, dealing with endless paperwork, and making phone calls just to get a vague idea of what you owe.

But what if it didn't have to be that way? What if you could get an estimate of your medical costs before even setting foot in the clinic? Welcome to SHIPSmart, your personal insurance companion designed to help UC students enrolled in SHIP (UC Student Health Insurance Plan) take control of their healthcare costs.

SHIPSmart is here to guarantee the lowest possible price for any medical, dental, or vision treatment you need, all while ensuring you get the most out of your insurance benefits. And the best part? If our estimate turns out to be lower than what you were charged, we'll fight for rebates and manage all follow-up claims.

No more surprise bills, no more endless phone calls, just peace of mind knowing that your health coverage is working for you, not the other way around.

## Key Objectives

1. Boost awareness and use of preventative care

2. Support underutilizers with targeted analytics

3. Simplify policy navigation and referrals

4. Reduce unexpected costs with AI-driven negotiation

5. Streamline appointment booking and network usage

## How we built it

Designed the app on figma. Implemented frontend using swiftui. . Regression model. OpenAi/Gemini framework to build complex agent for user-facing side and Cerebas AI to contact insurers and providers and auto-fill online intake forms when possible.

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



