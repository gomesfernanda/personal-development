package main

import "fmt"

func main() {
	var fahr float64
	fmt.Print("What's your temperature in Fahrenheit? ")
	fmt.Scanf("%f", &fahr)
	cels := (fahr - 32) * 5 / 9
	fmt.Println("Your temperature in Celsius is", cels)
}
