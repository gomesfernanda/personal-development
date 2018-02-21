package main

import "fmt"

func fibonacci(x int) int {
	y := int(x)
	if x == 1 {
		return 1
	}

	if x == 0 {
		return 0
	}
	y = fibonacci(x-1) + fibonacci(x-2)
	return y
}

func main() {
	for i := 12; i > 0; i-- {
		fmt.Printf("for %d, fibonacci is %d \n", i, fibonacci(i))
	}
}
