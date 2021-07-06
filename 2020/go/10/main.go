// Solution to: https://adventofcode.com/2020/day/10 (Part 1)
package main

import (
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	file := getFilePath()
	input := loadInput(file)
	adapters := getAdapaters(input)
	difs := calcDifferences(adapters)

	ans1 := solvePart1(difs)
	ans1Status := testAnswerPart1(file, ans1)
	fmt.Println("Part 1 answer:", ans1, ans1Status)

	ans2 := solvePart2(difs)
	ans2Status := testAnswerPart2(file, ans2)
	fmt.Println("Part 2 answer:", ans2, ans2Status)
}

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

func getAdapaters(s []string) []int {
	adapters := stringSliceToIntSlice(s)
	// Sort adapters in such a way they all should be connected
	sort.Ints(adapters)
	return adapters
}

func calcDifferences(a []int) []int {
	difs := make([]int, len(a))
	difs[0] = a[0] // charging outlet has joltage rating of 0
	for i := 1; i < len(a); i++ {
		difs[i] = a[i] - a[i-1]
	}
	return difs
}

func countDifferences(difs []int) map[int]int {
	counts := make(map[int]int)
	for _, num := range difs {
		counts[num] += 1
	}
	// Device's built-in adapter is always 3 higher than the highest adapter
	// so also count it
	counts[3] += 1
	return counts
}

func solvePart1(difs []int) int {
	counts := countDifferences(difs)
	// Answer is number of 1-jolt differences multiplied by
	// the number of 3-jolt differences
	return counts[1] * counts[3]
}

func countCombinations(difs []int) int {
	// There are only 1-jolt and 3-jolt difference adapters in our case
	// We can not skip adapters with difference == 3 in a way the total jolts
	// satisfies our device
	// So possible connection combinations occure only when 1-jolt difference
	// adapters follow each other
	// init number of combination when all adapters are connected is 1
	totalComb := 1
	onesSeq := 0 // length of ones sequence
	// Iterate from the last element because we must know how many combinations
	// are presented in .. to count total number correctly
	for i := len(difs) - 1; i >= -1; i-- {
		if (i == -1) || (difs[i] == 3) {
			totalComb *= localCombinations(onesSeq)
			onesSeq = 0
			continue
		}
		onesSeq += 1
	}
	return totalComb
}

func localCombinations(onesSeq int) int {
	// -1 because we cant drop last number,
	// because next jolt difference will be 4 then
	onesSeq -= 1
	// Formula calculated according to experiments with ones sequences from 0 to 4
	if onesSeq < 1 {
		return 1
	} else if onesSeq == 1 {
		return 2
	}
	return int(math.Pow(2, float64(onesSeq)) - (math.Pow(2, float64(onesSeq)-2) - 1))
}

func solvePart2(difs []int) int {
	return countCombinations(difs)
}

func testAnswerPart1(file string, ans int) string {
	correct := map[string]int{
		"input":       1848,
		"input_test":  220,
		"input_test2": 35,
	}
	if correct[file] != ans {
		return "NOT CORRECT"
	}
	return "CORRECT"
}

func testAnswerPart2(file string, ans int) string {
	correct := map[string]int{
		"input":       8099130339328,
		"input_test":  19208,
		"input_test2": 8,
	}
	if correct[file] != ans {
		return "NOT CORRECT"
	}
	return "CORRECT"
}
