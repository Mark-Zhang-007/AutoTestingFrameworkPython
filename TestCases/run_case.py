import pytest
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PyTest Cases")
    parser.add_argument("--casename", type=str, required=True, help="test case full name")
    parser.add_argument("--marker", type=str, default="", required=False, help="test case marker name")
    parser.add_argument("--rerun", type=int, default=1, required=False, help="test case rerun times, default as 1")
    
    args = vars(parser.parse_args())

    case_full_name = args["casename"]
    case_marker = args["marker"]
    case_reruns = args["rerun"]

    pytest_args = []
    pytest_args.append(case_full_name)    
    pytest_args.append("-s")
    pytest_args.append("-v")
    pytest_args.append("--reportportal")
    
    if case_marker != "":
        pytest_args.append("-m")
        pytest_args.append(case_marker)

    if case_reruns > 0:
        pytest_args.append("--reruns")
        pytest_args.append(str(case_reruns))
        pytest_args.append("--reruns-delay")
        pytest_args.append("5")

    pytest.main(pytest_args)

