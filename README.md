# Rhythm

Rhythm is a sophisticated utility designed to analyze Git commit logs to estimate the amount of time collaborators have spent on a project. By examining the timestamps and patterns of commits, Rhythm offers insights into the work rhythm of your team, providing a clearer picture of the project's development flow.

## Features

- **Time Tracking:** Calculates time spent by each collaborator on the Git repository.
- **Session Detection:** Identifies coding sessions based on commit patterns, with configurable thresholds.
- **Productivity Insights:** Helps gauge the productivity of project contributors over time.

## Getting Started

### Prerequisites

- Git installed on your system
- Python 3.6 or higher

### Installation

1. Clone the repository to your local machine:
```
git clone https://github.com/yourusername/Rhythm.git
```
2. Navigate to the cloned repository:
```
cd rhythm
```

### Usage

1. Set the `repo_path` variable in `rhythm.py` to the path of your Git repository.
2. Configure `time_threshold` and `extra_hours_per_session` in `rhythm.py` as needed.
3. Run the script:

```
python rhythm.py
```


## Configuration

- `repo_path`: Path to your git repository. Defaults to the current directory ('.').
- `time_threshold`: Threshold to consider commits part of the same session. Default is 1.5 hours.
- `extra_hours_per_session`: Extra hours to add for the first commit in each session. Default is 0.5 hours.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- The open-source community for continuous inspiration and support.
