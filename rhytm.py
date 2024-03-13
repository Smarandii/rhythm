import subprocess
import datetime
from collections import defaultdict

# Parameters
repo_path = '.'  # Path to your git repository, '.' means current directory
time_threshold = datetime.timedelta(hours=1.5)  # Threshold to consider commits part of the same session
extra_hours_per_session = 0.5  # Extra hours to add for the first commit in each session


# Function to run git command
def run_git_command(command):
    result = subprocess.run(['git', '-C', repo_path] + command, capture_output=True, text=True, encoding='utf-8')
    return result.stdout.strip().split('\n')


# Function to parse git log into a list of (timestamp, author) tuples
def get_commit_log():
    log = run_git_command(['log', '--pretty=format:%at %aN'])
    commits = []
    for entry in log:
        parts = entry.split(' ', 1)
        if len(parts) == 2:
            timestamp, author = parts
            commits.append((int(timestamp), author))
    return commits


# Function to calculate coding hours
def calculate_coding_hours(commits):
    author_sessions = defaultdict(list)
    for i, (timestamp, author) in enumerate(commits):
        if i == 0 or (commits[i - 1][1] != author) or (
                datetime.datetime.fromtimestamp(commits[i - 1][0]) + time_threshold < datetime.datetime.fromtimestamp(
                timestamp)):
            author_sessions[author].append([timestamp])
        else:
            author_sessions[author][-1].append(timestamp)
    return author_sessions


# Function to sum up hours per author
def sum_hours(author_sessions):
    author_hours = {}
    for author, sessions in author_sessions.items():
        total_seconds = 0
        for session in sessions:
            if len(session) > 1:
                session_start = datetime.datetime.fromtimestamp(session[0])
                session_end = datetime.datetime.fromtimestamp(session[-1])
                session_duration = (session_end - session_start).total_seconds()
                total_seconds += session_duration
            # Add extra hours for the session; ensure this doesn't result in negative hours
            total_seconds += extra_hours_per_session * 3600
        author_hours[author] = max(total_seconds / 3600, 0)  # Convert seconds to hours, ensure non-negative
    return author_hours


# Main logic
commits = sorted(get_commit_log(), key=lambda x: (x[1], x[0]))  # Ensure commits are sorted by author and timestamp
author_sessions = calculate_coding_hours(commits)
author_hours = sum_hours(author_sessions)

# Print results
for author, hours in author_hours.items():
    print(f"{author}: {hours:.2f} hours")
