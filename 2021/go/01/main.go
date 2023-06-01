package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func getFilePath() string {
	if len(os.Args) < 2 {
		return "input"
	} else {
		return os.Args[1]
	}
}

func loadInput(file string) []string {
	input, err := os.ReadFile(file)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}
	return strings.Split(string(input), "\n")
}

// Part 1 solution
func countDepthIncrease(depths []string) int {
	prevDepth := 0
	increases := 0
	for i, s := range depths {
		depth, err := strconv.Atoi(s)
		if err != nil {
			log.Fatalln("Error occured on converting", s, "to int")
		}
		if i == 0 {
			prevDepth = depth
			continue
		}
		if depth > prevDepth {
			increases += 1
		}
		prevDepth = depth
	}
	return increases
}

// Part 2 solution
func stringSliceToIntSlice(ss []string) []int {
	is := make([]int, len(ss))
	for i, s := range ss {
		n, err := strconv.Atoi(s)
		if err != nil {
			log.Fatalln("Error occured on converting", s, "to int")
		}
		is[i] = n
	}
	return is
}

func countSlidingDepthIncrease(depths []int) int {
	var increases int
	n := len(depths)
	for i := 1; i < n-2; i++ {
		prevSum := depths[i-1] + depths[i] + depths[i+1]
		sum := depths[i] + depths[i+1] + depths[i+2]
		if sum > prevSum {
			increases += 1
		}
	}
	return increases
}

func main() {
	input := loadInput(getFilePath())

	increases := countDepthIncrease(input)
	fmt.Println("Part 1: Number of increases", increases)

	depths := stringSliceToIntSlice(input)
	increases = countSlidingDepthIncrease(depths)
	fmt.Println("Part 2: Number of increases", increases)
}
