package main

import "fmt"
/*
func main() {
	for i := 1; i <= 100; i++ {
		if i%3 == 0 && i%5 == 0 {
			fmt.Println(i, "Fizz Buzz")
		} else if i%3 == 0 {
			fmt.Println(i, "Fizz")
		} else if i%5 == 0 {
			fmt.Println(i, "Buzz")
		}
	}
}

*/
func main() {
	for i := 1; i <= 100; i++ {



		switch i {
		case i % 15:
			fmt.Println(i, "FizzBuzz")
		case i % 3:
			fmt.Println(i, "Fizz")
		case i % 5:
			fmt.Println(i, "Buzz")
		default:
			fmt.Println(i)
		}
	}
}

