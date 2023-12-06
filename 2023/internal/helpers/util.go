package helpers

import "golang.org/x/exp/constraints"

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
