package helpers

import (
	"fmt"
	"strconv"
	"strings"
)

// ParselabeledValue expects a string like "7 sheep" and returns 7 as an int and the string "sheep"
// if numberFirst is true, it processes the string like "7 sheep"
// if numberFirst is false, it processes the string liek "Game 12"
// if the string does not conform to the pattern, then it panics
func ParseLabeledValue(s string, numberFirst bool) (int, string) {
	tokens := strings.Split(s, " ")
	Assert(len(tokens) == 2, "token len != 2")

	numIndex := 0
	labelIndex := 1
	if !numberFirst {
		numIndex = 1
		labelIndex = 0
	}

	numVal, err := strconv.Atoi(tokens[numIndex])
	if err != nil {
		panic(fmt.Sprintf("number token '%s' is not an int: %s", tokens[numIndex], err))
	}

	return numVal, tokens[labelIndex]
}
