from collector.log_collector import collect_logs

logs = collect_logs("logs/sample_auth.log")

print("Collected logs:", len(logs))

for log in logs:
    print(log)
