package main

import (
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Order int

const (
	Ascending Order = iota
	Descending
	Flat
)

func loadInput(filePath string) []string {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}
	return strings.Split(string(input), "\n")
}

func parseInput(input []string) [][]int {
	reports := [][]int{}
	for _, row := range input {
		if row == "" {
			continue
		}

		report := []int{}
		for part := range strings.SplitSeq(row, " ") {
			level, err := strconv.Atoi(part)
			if err != nil {
				log.Fatalln("Error converting part to int:", part)
			}
			report = append(report, level)
		}

		reports = append(reports, report)
	}
	return reports
}

func getOrderDirection(difference int) Order {
	if difference > 0 {
		return Ascending
	} else if difference < 0 {
		return Descending
	}
	return Flat
}

func removeLevel(report []int, index int) []int {
	result := make([]int, 0, len(report)-1)
	result = append(result, report[:index]...)
	result = append(result, report[index+1:]...)
	return result
}

func calculateNSafeReports(reports [][]int, canRemoveLevelOnce bool) int {
	safeCount := 0
	for _, report := range reports {
		if isSafeReport(report, canRemoveLevelOnce) || (canRemoveLevelOnce && isSafeReport(report[1:], false)) {
			safeCount++
		}
	}
	return safeCount
}

func isSafeReport(report []int, canRemoveLevelOnce bool) bool {
	if len(report) < 2 {
		log.Fatalln("Report must have at least two levels")
	}

	expectedOrder := getOrderDirection(report[1] - report[0])
	if expectedOrder == Flat {
		return false
	}

	for i := 1; i < len(report); i++ {
		difference := report[i] - report[i-1]
		currentOrder := getOrderDirection(difference)
		difference = int(math.Abs(float64(difference)))
		if currentOrder == expectedOrder && difference > 0 && difference < 4 {
			continue
		}
		if !canRemoveLevelOnce {
			return false
		}

		return isSafeReport(removeLevel(report, i-1), false) || isSafeReport(removeLevel(report, i), false)
	}
	return true
}

func main() {
	filePath := "input"
	if len(os.Args) > 1 {
		filePath = os.Args[1]
	}

	input := loadInput(filePath)
	reports := parseInput(input)

	// Part One
	safeReportsCountPartOne := calculateNSafeReports(reports, false)
	fmt.Printf("Number of safe reports with Part One rules: %d\n", safeReportsCountPartOne)

	// Part Two
	safeReportsCountPartTwo := calculateNSafeReports(reports, true)
	fmt.Printf("Number of safe reports with Part Two rules: %d\n", safeReportsCountPartTwo)
}
