import sys
from datetime import datetime

def parse_line(line):
    parts = line.split()
    if len(parts) != 3:
        return None, None, None
    try:
        timestamp = datetime.strptime(parts[0], "%H:%M:%S").time()
        username = parts[1]
        action = parts[2]
        return timestamp, username, action
    except ValueError:
        return None, None, None

def calculate_duration(start, end):
    start_time = datetime.combine(datetime.min, start)
    end_time = datetime.combine(datetime.min, end)
    return (end_time - start_time).total_seconds()

def process_log_file(file_path):
    user_sessions = {}
    start_time = None
    end_time = None

    with open('sample.txt', 'r') as file:
        for line in file:
            timestamp, username, action = parse_line(line)
            if timestamp is None or username is None or action not in ['Start', 'End']:
                continue
            
            if action == 'Start':
                start_time = timestamp
                if username in user_sessions:
                    user_sessions[username]['active_sessions'] += 1
                else:
                    user_sessions[username] = {'active_sessions': 1, 'total_duration': 0}
            else:
                end_time = timestamp
                if username in user_sessions:
                    user_sessions[username]['active_sessions'] -= 1
                    user_sessions[username]['total_duration'] += calculate_duration(start_time, end_time)
    
    # Handling cases where sessions are still active at the end of the log file
    last_timestamp = max(end_time, start_time)
    for user in user_sessions:
        if user_sessions[user]['active_sessions'] > 0:
            user_sessions[user]['total_duration'] += calculate_duration(last_timestamp, last_timestamp)

    # Print the report
    for user, data in user_sessions.items():
        print(f"{user} {data['active_sessions']} {int(data['total_duration'])}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_log_file>")
        sys.exit(1)
    log_file_path = sys.argv[1]
    process_log_file(log_file_path)
