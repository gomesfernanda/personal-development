package main

import "fmt"

func main() {
	var feets float64
	fmt.Print("How many feets you want to convert? ")
	fmt.Scanf("%f", &feets)
	meters := feets * 0.3048
	fmt.Println(feets, "feets equals", meters, "meters")
}
