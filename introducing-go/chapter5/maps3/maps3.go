package main

import "fmt"

func main() {
	elements := map[string]map[string]string{
		"H": map[string]string{
			"name":  "",
			"state": "gas",
		},
		"He": map[string]string{
			"name":  "Helium",
			"state": "gas",
		},
	}
	if el, ok := elements["He"]; ok {
		fmt.Println(el["name"], el["state"])
	}

}
