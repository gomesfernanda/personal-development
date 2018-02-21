package main

import "fmt"

func second() {
	fmt.Println("seconnnd")
}

func first() {
	defer second()
	fmt.Println("firssst")
}

func a() {
	for i := 0; i < 4; i++ {
		defer fmt.Print(i, ", ")
	}
}

func c() (i int) {
	defer func() { i++ }()
	return 1
}

func main() {
	first()
	a()
	fmt.Println("")
	fmt.Println(c())
}
