from pathlib import Path
import sys

from epjson_transition.exceptions import EpJSONTransitionError
from epjson_transition.logger import SimpleLogger
from epjson_transition.transition import EpJSONTransition


def main() -> int:
    """Entry point for command line packaging"""
    argc = len(sys.argv)
    if argc == 4:
        input_file_path = Path(sys.argv[1])
        output_file_path = Path(sys.argv[2])
        logger = SimpleLogger(console=True, log_file_path=sys.argv[3])
    else:
        print("Invalid command line execution: expecting 3 arguments")
        print("  Argument 1: the path to the EpJSON file to be transitioned.")
        print("  Argument 2: the path to the output file to be written.")
        print("  Argument 3: optional path to an error file to log progress")
        return 1
    try:
        EpJSONTransition(input_file_path, output_file_path).transform(logger)
    except EpJSONTransitionError:
        print("Caught EpJSON transition error during execution")
        return 1
    finally:
        logger.close()
    # except Exception as e:
    #    print("Caught unknown exception during execution, message: " + str(e))
    #    return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - Covering main() directly, not this script entry
    """Entry point for direct script usage"""
    sys.exit(main())
