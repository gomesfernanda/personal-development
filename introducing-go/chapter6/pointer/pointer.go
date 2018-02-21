package main

import "fmt"

func zero(xPr *int) {
	*xPr = 0
}

func one(xPr *int) {
	*xPr = 1
}
func main() {
	x := 5
	zero(&x)
	fmt.Println(x)

	y := new(int)
	one(y)
	fmt.Println(*y)

}
