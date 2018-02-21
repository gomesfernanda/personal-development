package main

import "fmt"

func main() {
	x := make(map[string]int) // a map needs to be initialized!!
	x["boat"] = 10
	fmt.Println(x["boat"])
}
