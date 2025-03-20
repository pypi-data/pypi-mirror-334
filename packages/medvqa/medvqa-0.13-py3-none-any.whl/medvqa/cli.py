import argparse
import subprocess
import os


report = '''\n⚠️⚠️⚠️\n
Try installing latest version of the library by running the following command:
    pip install git+https://github.com/SushantGautam/MedVQA.git
If you cannot solve the problem, don't hesitate to add an issue at https://github.com/SushantGautam/MedVQA/issues with the log above! We will try to solve the problem ASAP. Can also interact with us on Discord: https://discord.gg/22V9huwc3R.\n
⚠️⚠️⚠️'''


def main():
    parser = argparse.ArgumentParser(
        description='MedVQA CLI', allow_abbrev=False)
    parser.add_argument('--competition', type=str, required=True,
                        help='Name of the competition (e.g., gi-2025)')
    parser.add_argument('--task', type=str, required=True,
                        help='Task number (1 or 2)')
    args, unknown = parser.parse_known_args()

    # Dynamically find the base directory of the MedVQA library
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if competition directory exists
    competition_dir = os.path.join(base_dir, 'competitions', args.competition)
    if not os.path.isdir(competition_dir):
        raise FileNotFoundError(
            f"Competition '{args.competition}' does not exist! Need to update library?"+report)
    # Check if task file exists
    task_file = os.path.join(competition_dir, f'task_{args.task}.py')
    if not os.path.isfile(task_file):
        raise FileNotFoundError(
            f"Task '{args.task}' does not exist! Need to update library?"+report)
    subprocess.run(
        ['python', task_file] + unknown)


if __name__ == '__main__':
    main()
