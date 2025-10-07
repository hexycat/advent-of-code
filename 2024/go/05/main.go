package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func loadInput(filePath string) ([]string, []string) {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}

	rules := []string{}
	updates := []string{}
	isUpdatesPart := false
	for line := range strings.SplitSeq(string(input), "\n") {
		if len(line) == 0 {
			isUpdatesPart = true
			continue
		}
		if isUpdatesPart {
			updates = append(updates, line)
		} else {
			rules = append(rules, line)
		}
	}
	return rules, updates
}

func parseRules(rawRules []string) map[int]map[int]bool {
	parsedRules := map[int]map[int]bool{}
	for _, rule := range rawRules {
		parts := strings.Split(rule, "|")
		if len(parts) != 2 {
			log.Fatalln("Invalid rule:", rule)
		}

		before_page, err := strconv.Atoi(parts[0])
		if err != nil {
			log.Fatalln("Error converting before page to int:", parts[0])
		}

		after_page, err := strconv.Atoi(parts[1])
		if err != nil {
			log.Fatalln("Error converting after page to int:", parts[1])
		}

		if parsedRules[before_page] == nil {
			parsedRules[before_page] = map[int]bool{}
		}
		parsedRules[before_page][after_page] = true
	}
	return parsedRules
}

func parseUpdates(rawUpdates []string) [][]int {
	parsedUpdates := [][]int{}
	for _, rawUpdate := range rawUpdates {
		update := []int{}
		for page := range strings.SplitSeq(rawUpdate, ",") {
			pageNum, err := strconv.Atoi(page)
			if err != nil {
				log.Fatalln("Error converting page to int:", page)
			}
			update = append(update, pageNum)
		}
		parsedUpdates = append(parsedUpdates, update)
	}
	return parsedUpdates
}

func isValidUpdate(update []int, rules map[int]map[int]bool) bool {
	mustBeAfterPages := map[int]bool{}
	for i := len(update) - 1; i > -1; i-- {
		page := update[i]
		if mustBeAfterPages[page] {
			return false
		}
		for afterPage := range rules[page] {
			mustBeAfterPages[afterPage] = true
		}
	}
	return true
}

func groupUpdatesByValidity(updates [][]int, rules map[int]map[int]bool) (validUpdates [][]int, invalidUpdates [][]int) {
	for _, update := range updates {
		if isValidUpdate(update, rules) {
			validUpdates = append(validUpdates, update)
		} else {
			invalidUpdates = append(invalidUpdates, update)
		}
	}
	return validUpdates, invalidUpdates
}

func getMiddlePagesSum(updates [][]int) int {
	sum := 0
	for _, update := range updates {
		sum += update[len(update)/2]
	}
	return sum
}

func correctUpdate(update []int, rules map[int]map[int]bool) []int {
	correctedUpdate := make([]int, 0, len(update))
	for insertIdx, page := range update {
		for prevIdx, prevPage := range correctedUpdate {
			if rules[page][prevPage] {
				insertIdx = prevIdx
				break
			}
		}

		correctedUpdate = append(correctedUpdate[:insertIdx+1], correctedUpdate[insertIdx:]...)
		correctedUpdate[insertIdx] = page
	}
	return correctedUpdate
}

func correctUpdates(updates [][]int, rules map[int]map[int]bool) [][]int {
	correctedUpdates := [][]int{}
	for _, update := range updates {
		correctedUpdates = append(correctedUpdates, correctUpdate(update, rules))
	}
	return correctedUpdates
}

func main() {
	rawRules, rawUpdates := loadInput("input")

	rules := parseRules(rawRules)
	updates := parseUpdates(rawUpdates)
	validUpdates, invalidUpdates := groupUpdatesByValidity(updates, rules)

	validUpdatesSum := getMiddlePagesSum(validUpdates)
	fmt.Println("Middle pages sum (valid updates):", validUpdatesSum)

	correctedUpdatesSum := getMiddlePagesSum(correctUpdates(invalidUpdates, rules))
	fmt.Println("Middle pages sum (corrected updates):", correctedUpdatesSum)
}
