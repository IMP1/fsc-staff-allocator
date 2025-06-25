import os
import argparse
from datetime import datetime

import allocation_data
import allocator


def main(args):
    if args.dry_run:
        allocator.log_to_file = False
        allocation_data.log_to_file = False
    if args.verbose:
        allocator.log_to_stdout = True
        allocation_data.log_to_stdout = True
    if args.quiet:
        allocator.log_to_stdout = False
        allocation_data.log_to_stdout = False

    applications = allocation_data.load_staff_data("data/All Applications for All Staff for Summer - First Fortnight.csv")
    camps = allocation_data.load_camp_data("data/Camp_Requirements First Fortnight.csv")
    if not args.quiet:
        print(f"Loaded data for {len(applications)} applications.")
        print(f"Loaded data for {len(camps)} camps.")

    if not os.path.exists("output"):
        os.mkdir("output")

    allocator.log_filepath = args.log_file or "output/log_" + datetime.now().strftime("%d%m%y_%H%M%S") + ".txt"

    applications_copy = [a for a in applications]
    camps = allocator.allocate(camps, applications_copy)
    results_filename = args.result_file or "output/results_" + datetime.now().strftime("%d%m%y_%H%M%S") + ".txt"
    if not args.quiet:
        print("Allocating staff to camps...")
    if not args.dry_run:
        allocation_data.save_allocation_data(camps, results_filename)
    if not args.quiet:
        print("Allocation Success.")
    if not args.dry_run and not args.quiet:
        print(f"See '{results_filename}' for the allocations.")
        print(f"See '{allocator.log_filepath}' for the decisions made.")

    if not args.quiet:
        allocator.analyse_allocations(camps, applications)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Staff Allocator',
                    description='Allocates FSC staff to camps based on camp needs and staff preferences',
                    epilog='version 0.0.1')
    parser.add_argument('--log-file')
    parser.add_argument('--result-file')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    main(parser.parse_args())


# TODO: Test case where staff have people they must camp with
#       Currently there don't seem to be any of this (or it's not read from the spreadsheet yet)
# TODO: Test case where staff have people they mustn't camp with
#       Currently there don't seem to be any of this (or it's not read from the spreadsheet yet)

