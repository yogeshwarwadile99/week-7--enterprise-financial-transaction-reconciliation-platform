# Enterprise Financial Transaction & Reconciliation Platform

## Project Overview

A high-integrity transactional backend for a fintech company that processes thousands of customer financial transactions daily through multiple channels (UPI, Card, Bank Transfer, Wallet, Payment Gateway). The system ensures transactions are never lost, duplicated, or incorrectly modified.

---

## Business Scenario

A fintech company processes thousands of customer financial transactions every day through multiple channels. The backend must:
- Create and process transactions
- Maintain account balances
- Prevent duplicate transactions
- Detect suspicious transaction patterns
- Reconcile internal transactions against external payment reports
- Handle failed transactions
- Generate audit trails
- Provide management analytics

**Primary Requirement:** The system must never silently lose, duplicate, or incorrectly modify a financial transaction.

---

## Core Architecture
API Clients
|
v
FastAPI Backend
|
┌────────────────┼────────────────┐
| | |
v v v
Auth Service Transaction Account Service
Service
|
┌──────────┴──────────┐
v v
PostgreSQL Redis
|
v
Transaction Ledger
|
v
Celery Workers
|
┌──────┼──────┐
v v v
Reconciliation Alerts Reports

text

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Programming Language |
| FastAPI | Web Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Redis | Caching |
| Celery | Background Jobs |
| JWT | Authentication |
| bcrypt | Password Hashing |
| Swagger/OpenAPI | Documentation |

---

## Project Structure
enterprise-financial-transaction-platform/
│
├── app/
│ ├── main.py
│ ├── config.py
│ ├── database.py
│ ├── models/
│ ├── schemas/
│ ├── routes/
│ ├── services/
│ ├── middleware/
│ └── utils/
│
├── tests/
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── README.md

text

---

## 👥 User Roles (RBAC)

| Role | Access |
|------|--------|
| Customer | View account, balance, create transaction, view own transactions, download statement |
| Operations Analyst | View transactions, investigate failed transactions, review reconciliation mismatches |
| Finance Manager | Approve adjustments, view financial reports, review reconciliation |
| Admin | Manage users, accounts, access audit logs, configure system settings |

---

## Authentication System

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | Logout and revoke token |
| GET | `/api/v1/auth/me` | Get current user info |

---

## Account Management

### Account Statuses
- ACTIVE
- FROZEN
- SUSPENDED
- CLOSED

### APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/accounts` | Create account |
| GET | `/api/v1/accounts` | Get all accounts |
| GET | `/api/v1/accounts/{id}` | Get account by ID |
| PATCH | `/api/v1/accounts/{id}/status` | Update account status |

---

##  Transaction Processing

### Transaction Types
- CREDIT
- DEBIT
- TRANSFER
- REFUND
- REVERSAL

### APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/transactions` | Create transaction |
| GET | `/api/v1/transactions` | Get all transactions |
| GET | `/api/v1/transactions/{id}` | Get transaction by ID |
| POST | `/api/v1/transactions/{id}/cancel` | Cancel transaction |

---

## Transaction Lifecycle
INITIATED → PENDING → PROCESSING → SUCCESS

text

**Failure Path:**
PENDING → FAILED

text

**Reversal Path:**
SUCCESS → REVERSAL_REQUESTED → REVERSED

text

---

## Double-Entry Ledger

For an internal transfer of ₹5,000:

| Account | Entry Type | Amount |
|---------|------------|--------|
| Account A | DEBIT | ₹5,000 |
| Account B | CREDIT | ₹5,000 |

> The transaction is treated as a single atomic operation. If credit fails, debit is rolled back using PostgreSQL transactions.

---

## Balance Integrity

- Available Balance >= 0 (unless overdraft is enabled)
- If balance is ₹10,000 and transfer is ₹15,000 → **REJECTED**
- Response: `{"success": false, "error_code": "INSUFFICIENT_FUNDS"}`

---

## Idempotency

```http
POST /api/v1/transactions
Idempotency-Key: TXN-2026-001234
If the same request is sent twice, the system does not create another transaction.

Reconciliation Engine
Method	Endpoint	Description
POST	/api/v1/reconciliation/run	Run reconciliation
GET	/api/v1/reconciliation/runs	Get all runs
GET	/api/v1/reconciliation/mismatches	Get mismatches
GET	/api/v1/reconciliation/{id}	Get reconciliation by ID
Mismatch Types
AMOUNT_MISMATCH

STATUS_MISMATCH

MISSING_INTERNAL

MISSING_EXTERNAL

DUPLICATE

UNKNOWN

Suspicious Transaction Detection
Rule	Description
1	More than 5 transactions in 2 minutes
2	Transaction amount significantly higher than normal
3	Multiple failed transactions followed by successful high-value transaction
4	Large transaction from newly created account
5	Multiple accounts transferring money rapidly
Risk Levels
LOW

MEDIUM

HIGH

CRITICAL

APIs
Method	Endpoint	Description
GET	/api/v1/risk/alerts	Get all risk alerts
GET	/api/v1/risk/alerts/{id}	Get alert by ID
PATCH	/api/v1/risk/alerts/{id}/review	Review alert
Audit Logging
Track every sensitive action:

Field	Description
User	Who performed the action
Action	What was done
Resource	Which resource was affected
Previous Value	Old value
New Value	New value
IP Address	User's IP
Timestamp	When it happened
Request ID	Unique request identifier
Database Design
#	Table	Purpose
1	users	User accounts
2	roles	User roles
3	accounts	Financial accounts
4	account_balances	Balance history
5	transactions	Transaction records
6	transaction_entries	Ledger entries (DEBIT/CREDIT)
7	transaction_metadata	Additional transaction info
8	idempotency_keys	Prevent duplicate transactions
9	reconciliation_runs	Reconciliation execution records
10	reconciliation_records	Mismatch details
11	risk_alerts	Fraud detection alerts
12	audit_logs	Complete audit trail
13	notifications	User notifications
 Installation & Setup
Prerequisites
Python 3.11+

PostgreSQL

Redis

Steps
bash
# Clone repository
git clone https://github.com/yogeshwarwadile99/week-7.git
cd week-7

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Create database
createdb financial_db

# Run server
uvicorn app.main:app --reload --port 8009
Testing APIs
Register User
bash
curl -X POST http://localhost:8009/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Admin","email":"admin@fintech.com","password":"Admin123","role":"ADMIN"}'
Login
bash
curl -X POST http://localhost:8009/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@fintech.com","password":"Admin123"}'
Create Account
bash
curl -X POST http://localhost:8009/api/v1/accounts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"currency":"INR","initial_balance":100000}'
Create Transaction (Transfer)
bash
curl -X POST http://localhost:8009/api/v1/transactions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: TXN-2026-001234" \
  -d '{"sender_account_id":1,"receiver_account_id":2,"amount":5000,"currency":"INR","transaction_type":"TRANSFER","channel":"INTERNAL","description":"Test transfer"}'
Run Reconciliation
bash
curl -X POST http://localhost:8009/api/v1/reconciliation/run \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"reference_number":"TXN-20260928-1234","amount":5000,"status":"SUCCESS"}]'
Swagger Documentation
Access the interactive API documentation:

text
http://localhost:8009/api/docs
