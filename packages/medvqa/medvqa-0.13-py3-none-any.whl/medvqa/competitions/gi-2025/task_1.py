import sys
import argparse


def main(repo, verbose=False):
    print("🌟 ImageCLEFmed-MEDVQA-GI-2025 🌟",
          "https://github.com/simula/ImageCLEFmed-MEDVQA-GI-2025")
    print("🔍 Subtask 1: Algorithm Development for Question Interpretation and Response")
    print(f"Analyzing submission repository: {repo}")
    if verbose:
        print("Verbose mode is enabled")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run GI-1015 Task 1 (VQA)')
    parser.add_argument('--submission_repo', type=str, required=True,
                        help='Path to the HF submission repository')
    args, _ = parser.parse_known_args()
    main(args.submission_repo)
