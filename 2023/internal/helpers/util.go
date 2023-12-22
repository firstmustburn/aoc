package helpers

import (
	"fmt"
	"strconv"

	"golang.org/x/exp/constraints"
)

func Assert(condition bool, reason string) {
	if !condition {
		panic(reason)
	}
}

func IsDigit(c byte) bool {
	return c >= '0' && c <= '9'
}

func SumSlice[V constraints.Integer | constraints.Float](input []V) V {
	var theSum V

	for _, i := range input {
		theSum += i
	}
	return theSum
}

func AbsInt(val int) int {
	if val < 0 {
		return -val
	}
	return val
}

func StrToInt(val string) int {
	output, err := strconv.Atoi(val)
	Assert(err == nil, fmt.Sprintf("could not convert '%s' to int", val))
	return output
}

func All(values []bool) bool {
	for _, value := range values {
		if !value {
			return false
		}
	}
	return true
}

// mod returns the modulus and works for negative numbers
func Mod(d, m int) int {
	var res int = d % m
	if res < 0 && m > 0 {
		return res + m
	}
	return res
}
