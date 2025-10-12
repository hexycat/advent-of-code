package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Operation func(a, b int) int

func Add(a, b int) int {
	return a + b
}

func Multiply(a, b int) int {
	return max(a, 1) * b
}

func Concatenate(a, b int) int {
	concatenatedTerm, err := strconv.Atoi(fmt.Sprintf("%d%d", a, b))
	if err != nil {
		log.Fatalln("Error concatenating numbers:", a, b)
	}
	return concatenatedTerm
}

type Equation struct {
	value             int
	terms             []int
	allowedOperations []Operation
}

func (equation *Equation) setAllowedOperations(operations []Operation) {
	equation.allowedOperations = operations
}

func (equation *Equation) isValid() bool {
	return equation.isValidPart(0, 0)
}

func (equation *Equation) isValidPart(currentValue int, termPosition int) bool {
	if currentValue > equation.value {
		return false
	}
	if termPosition == len(equation.terms) {
		return equation.value == currentValue
	}

	for _, operation := range equation.allowedOperations {
		if equation.isValidPart(operation(currentValue, equation.terms[termPosition]), termPosition+1) {
			return true
		}
	}
	return false
}

func loadInput(filePath string) []Equation {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading input file")
	}

	equations := []Equation{}
	for rows := range strings.SplitSeq(string(input), "\n") {
		if rows == "" {
			continue
		}

		parts := strings.Split(rows, ":")
		if len(parts) != 2 {
			log.Fatalln("Invalid input line:", rows)
		}

		equationValue, err := strconv.Atoi(parts[0])
		if err != nil {
			log.Fatalln("Invalid equation value:", parts[0])
		}

		terms := []int{}
		for termStr := range strings.SplitSeq(parts[1], " ") {
			if termStr == "" {
				continue
			}
			term, err := strconv.Atoi(termStr)
			if err != nil {
				log.Fatalln("Invalid term number:", termStr)
			}
			terms = append(terms, term)
		}

		equations = append(equations, Equation{value: equationValue, terms: terms})
	}
	return equations
}

func getSumOfValidEquationValues(equations []Equation, operations []Operation) int {
	sum := 0
	for _, equation := range equations {
		equation.setAllowedOperations(operations)
		if equation.isValid() {
			sum += equation.value
		}
	}
	return sum
}

func main() {
	equations := loadInput("input")

	operations := []Operation{Add, Multiply}
	fmt.Println("Sum of valid equation values (Part 1):", getSumOfValidEquationValues(equations, operations))

	operations = []Operation{Add, Multiply, Concatenate}
	fmt.Println("Sum of valid equation values (Part 2):", getSumOfValidEquationValues(equations, operations))
}
