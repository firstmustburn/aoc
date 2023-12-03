package helpers

func Assert(condition bool, reason string) {
	if !condition {
		panic(reason)
	}
}
