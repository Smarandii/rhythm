import argparse
import subprocess
import datetime
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description='Track time spent by each collaborator in a Git repository.')
    parser.add_argument('--repo_path', type=str, default='.', help='Path to the git repository. Default is the current directory.')
    parser.add_argument('--time_threshold', type=float, default=1.5, help='Threshold in hours to consider commits part of the same session. Default is 1.5 hours.')
    parser.add_argument('--extra_hours', type=float, default=0.5, help='Extra hours to add for the first commit in each session. Default is 0.5 hours.')
    return parser.parse_args()

def run_git_command(command, repo_path):
    result = subprocess.run(['git', '-C', repo_path] + command, capture_output=True, text=True, encoding='utf-8')
    return result.stdout.strip().split('\n')

def get_commit_log(repo_path):
    log = run_git_command(['log', '--pretty=format:%at %aN'], repo_path)
    commits = []
    for entry in log:
        parts = entry.split(' ', 1)
        if len(parts) == 2:
            timestamp, author = parts
            commits.append((int(timestamp), author))
    return commits

def calculate_coding_hours(commits, time_threshold):
    author_sessions = defaultdict(list)
    for i, (timestamp, author) in enumerate(commits):
        if i == 0 or (commits[i - 1][1] != author) or (
                datetime.datetime.fromtimestamp(commits[i - 1][0]) + datetime.timedelta(hours=time_threshold) < datetime.datetime.fromtimestamp(timestamp)):
            author_sessions[author].append([timestamp])
        else:
            author_sessions[author][-1].append(timestamp)
    return author_sessions

def sum_hours(author_sessions, extra_hours_per_session):
    author_hours = {}
    for author, sessions in author_sessions.items():
        total_seconds = 0
        for session in sessions:
            if len(session) > 1:
                session_start = datetime.datetime.fromtimestamp(session[0])
                session_end = datetime.datetime.fromtimestamp(session[-1])
                session_duration = (session_end - session_start).total_seconds()
                total_seconds += session_duration
            total_seconds += extra_hours_per_session * 3600
        author_hours[author] = max(total_seconds / 3600, 0)
    return author_hours

def main():
    args = parse_args()
    commits = sorted(get_commit_log(args.repo_path), key=lambda x: (x[1], x[0]))
    author_sessions = calculate_coding_hours(commits, args.time_threshold)
    author_hours = sum_hours(author_sessions, args.extra_hours)
    
    for author, hours in author_hours.items():
        print(f"{author}: {hours:.2f} hours")

if __name__ == "__main__":
    main()
