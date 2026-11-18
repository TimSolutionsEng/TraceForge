# TraceForge — Day 5 Development Progress

**Date:** 18 November 2026

## Overview

Today, I focused on connecting the different components of TraceForge into one working pipeline. I also improved the project's automated testing so that I can verify individual components as well as how they work together.

My main goal was to move TraceForge from having separate modules that perform individual tasks to having an application that can collect, process, analyse and store authentication log events.

## 1. Implementing the Application Pipeline

I implemented the main application logic in `backend/app.py`.

Previously, the collector, parser, detection engine and database modules existed separately. I needed a central component to coordinate their operations.

I created the `process_logs()` function to manage the processing sequence:

1. **Log collection:** Uses `collect_logs()` to read raw authentication logs from a specified file.
2. **Log parsing:** Passes each collected line to `parse_log()` to extract structured information.
3. **Threat detection:** Passes the parsed events to `detect_failed_logins()` to identify repeated failed login attempts.
4. **Database storage:** Initializes the database and uses `save_events()` to store the parsed events.
5. **Results reporting:** Returns a summary containing the number of collected logs, parsed events, newly inserted events and detected alerts.

I also implemented a `main()` function to run TraceForge using the default sample log file and display a processing report in the terminal.

This helped me understand the importance of application orchestration: individual modules can perform their own tasks, but the application needs to coordinate them in the correct order.

## 2. Testing the Complete Pipeline

I created `test_app.py` to test the application as a whole.

The integration test uses a temporary log file containing three failed SSH login attempts from the same IP address.

I verified that:

- All three log lines are collected.
- All three lines are successfully parsed.
- The detection engine generates a brute-force alert when the threshold of three failed attempts is reached.
- All three events are inserted into the database.
- Processing the same logs again does not insert duplicate events.
- The detection engine can still identify the suspicious activity when the same logs are processed again.

This was important because testing individual functions does not necessarily prove that the complete application works correctly.

## 3. Improving Automated Tests

While running the complete test suite, I discovered that some of my existing test files were actually manual demonstration scripts. They executed functions and printed their results, but they did not contain proper pytest test functions.

I converted these files into automated tests:

### `test_collector.py`

I added four tests to verify:

- Normal log collection.
- The collector returns a list.
- Empty lines are ignored.
- Missing log files are handled without crashing.

### `test_parser.py`

I added six tests to verify:

- Failed login parsing.
- Successful login parsing.
- Parsing attempts involving invalid usernames.
- Ignoring unrecognized authentication messages.
- Rejecting incorrectly formatted logs.
- Ensuring parsed events contain the expected fields.

### `test_database.py`

I added five tests to verify:

- Database initialization creates the events table.
- Events can be inserted.
- Duplicate events are prevented.
- Multiple events can be inserted.
- Stored events can be retrieved.

I used pytest's `tmp_path` fixture and `monkeypatch` to create temporary databases for testing. This prevents my automated tests from interfering with the actual TraceForge database.

The detection tests were also retained, covering failed login thresholds, different source IP addresses, successful logins and integration with the parser.

## 4. Full Test Suite Results

After updating the test files, I ran the complete test suite using:

`python3 -m pytest -v`

The results were:

| Test file | Tests passed |
|---|---:|
| `test_app.py` | 1 |
| `test_collector.py` | 4 |
| `test_database.py` | 5 |
| `test_detection.py` | 8 |
| `test_parser.py` | 6 |
| **Total** | **24** |

**Result: 24 passed, 0 failed.**

Pytest also displayed one deprecation warning originating from the installed AnyIO plugin. It did not affect the test results.

This was a significant milestone because all five test files were now being discovered and executed automatically by pytest.

## 5. Lessons Learned

Today's development helped me understand several important software engineering concepts:

**Application orchestration:** I learned how a central application module coordinates different components and passes information between them.

**Integration testing:** I learned that testing individual functions is not enough. I also need to verify that different modules work correctly when connected.

**Unit testing and assertions:** I learned to use assertions to verify expected behaviour instead of relying only on printed output.

**Test isolation:** I learned how temporary directories and database paths help prevent tests from modifying real application data.

**Database deduplication:** I reinforced my understanding of how unique event hashes and SQLite's `INSERT OR IGNORE` help prevent duplicate records.

**Separation of responsibilities:** I understood why collection, parsing, detection, storage and application orchestration should remain separate responsibilities.

**Security detection:** I also learned the difference between a security event and a detection alert. An event records something that happened, while an alert represents a finding produced by analysing events.

## 6. Current Project Status and Next Steps

At the end of today's work, TraceForge can:

- Collect authentication logs from a file.
- Parse SSH authentication events into structured data.
- Identify repeated failed login attempts from individual IP addresses.
- Store parsed events in an SQLite database.
- Prevent duplicate event insertion.
- Coordinate the processing pipeline through the application module.
- Produce a terminal report of processing results.
- Verify its main functionality using 24 automated tests.

There are still features I want to implement before considering the project complete.

My next planned improvement is **persistent security alerts**. Currently, the detection engine generates alerts, but they are not stored in the database. I plan to create a separate `alerts` table and implement a function for saving alerts while preventing duplicate alert records.

I also intend to improve the detection engine further, add more detection rules and eventually develop a dashboard for viewing security events and alerts.

## Conclusion

Today, I successfully connected the core TraceForge components into one working application and established a proper automated testing foundation.

I am gradually learning how individual programming concepts come together to form a larger software system. Rather than only writing functions, I am now thinking about how components communicate, how data moves through an application, how errors are handled and how the system can be tested reliably.

**My next focus is to implement persistent security alerts and continue developing TraceForge into a more complete security monitoring tool.**