package helpers

import (
	"fmt"
	"strconv"
	"strings"
)

func StripEmptyStrings(input []string) []string {
	temp := []string{}
	for _, token := range input {
		if len(token) > 0 {
			temp = append(temp, token)
		}
	}
	return temp
}

// ParselabeledValue expects a string like "7 sheep" and returns 7 as an int and the string "sheep"
// if numberFirst is true, it processes the string like "7 sheep"
// if numberFirst is false, it processes the string liek "Game 12"
// if the string does not conform to the pattern, then it panics
func ParseLabeledValue(s string, numberFirst bool) (int, string) {
	tokens := StripEmptyStrings(strings.Split(s, " "))
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

func ParseIntList(s string, sep string) []int {
	tokens := StripEmptyStrings(strings.Split(s, sep))

	// for _, token := range tokens {
	// 	fmt.Printf("'%s', ", token)
	// }
	// fmt.Println("")

	numbers := make([]int, len(tokens))

	var err error
	for index, token := range tokens {
		numbers[index], err = strconv.Atoi(token)
		if err != nil {
			panic(fmt.Errorf("could not convert '%s' to an int: %w", token, err))
		}
	}
	return numbers
}

func ParseInt64List(s string, sep string) []int64 {
	tokens := StripEmptyStrings(strings.Split(s, sep))

	// for _, token := range tokens {
	// 	fmt.Printf("'%s', ", token)
	// }
	// fmt.Println("")

	numbers := make([]int64, len(tokens))

	var err error
	for index, token := range tokens {
		numbers[index], err = strconv.ParseInt(token, 10, 64)
		if err != nil {
			panic(fmt.Errorf("could not convert '%s' to an int: %w", token, err))
		}
	}
	return numbers
}
