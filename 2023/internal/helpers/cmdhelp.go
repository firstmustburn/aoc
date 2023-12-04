package helpers

import "fmt"

type PartRunner interface {
	Setup(filename string)
	Part1()
	Part2()
}

func Dispatch(args []string, runner PartRunner) error {
	if len(args) != 3 {
		return fmt.Errorf("expected 3 arguments, not %v", args)
	}
	fmt.Printf("Executing setup on %s\n", args[2])
	runner.Setup(args[2])

	if args[1] == "1" {
		fmt.Println("Executing part 1")
		runner.Part1()
	} else if args[1] == "2" {
		fmt.Println("Executing part 2")
		runner.Part2()
	} else {
		return fmt.Errorf("unknown part '%s', expected 1 or 2", args[1])
	}
	return nil
}
