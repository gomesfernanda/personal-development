package main

import "fmt"

func half(x int) (int, bool) {
	y := (x / 2)
	if x%2 == 0 {
		return y, true
	}
	return y, false

}

func main() {
	x, y := half(2)
	fmt.Printf("(%d, %t)\n", x, y)
}
