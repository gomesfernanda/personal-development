package main

import "fmt"

func main() {
	fmt.Println("What's your name? ")
	var yourname string
	fmt.Scanf("%s", &yourname)

	fmt.Println("Hello,", yourname)
}
