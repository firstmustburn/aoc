package helpers

func GCD(n1, n2 uint64) uint64 {
	//Euclid's algorithm
	//repeate the loop of gcd(n1,n2) = gcd(n2, n1 % n2) until n1 % n2 = 0 which means n2 is the GCD
	for n2 != 0 {
		temp := n2
		n2 = n1 % n2
		n1 = temp
	}
	return n1
}

func LCM(values ...uint64) uint64 {
	//LCM = n1 * n2 / GCD(n1, n2)
	//start with the first pair and repeat until we have the LCM of all of them
	Assert(len(values) >= 2, "need at least two integer values")

	lcm := (values[0] * values[1]) / GCD(values[0], values[1])

	for _, value := range values[2:] {
		lcm = (lcm * value) / GCD(lcm, value)
	}
	return lcm
}
