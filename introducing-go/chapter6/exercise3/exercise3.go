package main

import "fmt"

func findGreater(lista []int) int {
	x := lista[1]
	for _, y := range lista {
		if y > x {
			x = y
		}
	}
	return x
}

func main() {
	mySlice := []int{2, 10, 7, 14, 12}
	fmt.Println(findGreater(mySlice))
}
