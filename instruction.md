An Apache-style access log is at `/app/access.log`. Parse it and write a JSON summary to `/app/report.json` with these fields:

- `total_requests` (integer): number of non-empty log lines
- `unique_ips` (integer): count of distinct client IP addresses (first field on each line)
- `top_path` (string): the request path that appears most often (from the quoted HTTP request); break ties by choosing any one path with the highest count

Success criteria:

1. `/app/report.json` exists.
2. `total_requests` equals the number of non-empty lines in `/app/access.log`.
3. `unique_ips` equals the number of distinct client IPs in the log.
4. `top_path` equals the most frequently requested path in the log.

You have 120 seconds to complete this task.
