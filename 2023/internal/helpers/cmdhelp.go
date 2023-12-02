package helpers

import "fmt"

type PartRunner interface {
	Part1(filename string) error
	Part2(filename string) error
}

func Dispatch(args []string, runner PartRunner) error {
	if len(args) != 3 {
		return fmt.Errorf("expected 3 arguments, not %v", args)
	}
	if args[1] == "1" {
		fmt.Printf("Executing part 1 on %s\n", args[2])
		return runner.Part1(args[2])
	}
	if args[1] == "2" {
		fmt.Printf("Executing part 2 on %s\n", args[2])
		return runner.Part2(args[2])
	}
	return fmt.Errorf("unknown part '%s', expected 1 or 2", args[1])
}
