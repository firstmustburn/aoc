package helpers

func Assert(condition bool, reason string) {
	if !condition {
		panic(reason)
	}
}

func IsDigit(c byte) bool {
	return c >= '0' && c <= '9'
}
