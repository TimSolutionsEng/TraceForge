# TraceForge — Day 4 Development Progress

## Overview

Day 4 focused on implementing the initial data-processing foundations of TraceForge, an educational SIEM-inspired project.

The goal was to understand how security logs are collected, parsed into structured events and stored in a database.

## 1. Database Implementation

**File:** `database/database.py`

Implemented:

- SQLite database connection.
- Automatic creation of the data directory.
- Initialization of the `events` table.
- Storage of structured security events.
- SHA-256 event fingerprints using Python's `hashlib`.
- Duplicate-event prevention using SQLite's `INSERT OR IGNORE`.

**What I learned:**

- How SQLite databases work.
- How to create and initialize database tables.
- How SQL INSERT statements store records.
- How hashing can be used to identify duplicate log entries.
- The difference between creating a table and modifying an existing table.

## 2. Log Collection

**File:** `collector/log_collector.py`

Implemented a `collect_logs()` function.

The function:

- Checks whether a specified log file exists.
- Opens the file.
- Reads its contents using `readlines()`.
- Removes unnecessary whitespace.
- Returns non-empty log entries.

**Test:** `test_collector.py`

Successfully collected four sample authentication log entries from `logs/sample_auth.log`.

**What I learned:**

- Python file handling.
- The `pathlib` module.
- Reading files using `open()` and `readlines()`.
- The difference between functions and built-in methods.
- Basic error handling.

## 3. Log Parsing

**File:** `parser/log_parser.py`

Implemented a `parse_log()` function using Python's regular expression module (`re`).

The parser extracts:

- Timestamp.
- Hostname.
- Process name.
- Process ID.
- Event type.
- Username.
- Source IP address.
- Port.
- Original raw log entry.

It currently recognizes successful and failed SSH password authentication events.

**Test:** `test_parser.py`

Successfully parsed all four sample authentication events:

- Three failed login attempts.
- One successful login attempt.

**What I learned:**

- Regular expressions and pattern matching.
- Extracting information from unstructured text.
- Python dictionaries.
- Converting extracted values into appropriate data types.
- How raw logs become structured security events.

## 4. Security Analysis Observations

During testing, two failed login attempts were observed from the same IP address:

`192.168.1.20`

The attempts targeted two different accounts:

- `admin`
- `root`

This could indicate suspicious authentication activity, potentially account enumeration or brute-force behaviour.

However, two failed attempts alone are insufficient to confirm an attack. More evidence and repeated observations would be required.

## 5. Current Development Status

| Component | Status |
|---|---|
| Database | Implemented and tested |
| Log collector | Implemented and tested |
| Log parser | Implemented and tested |
| Detection engine | Not yet implemented |
| Backend | Not yet implemented |
| Dashboard | Not yet implemented |

## 6. Next Development Goals

The next stage will focus on:

1. Implementing the detection engine.
2. Creating rules to identify repeated failed login attempts.
3. Testing detection rules using sample authentication logs.
4. Connecting the collector, parser, detection engine and database.
5. Gradually developing the backend and dashboard.

## 7. Key Learning Outcome

This development session demonstrated the initial stages of a SIEM processing pipeline:

**Log collection → Log parsing → Event storage**

The work provided practical experience in Python programming, file handling, regular expressions, SQLite, hashing, testing and modular software development.

TraceForge remains an educational project. Its purpose is to understand how SIEM systems work by building simplified components incrementally.