fun main() {
    val rowList = object {}.javaClass.getResourceAsStream("input.txt")?.bufferedReader()?.readLines()
        ?: throw Error("row list was null")
//    Part1.solve(rowList)
    Part2.solve(rowList)
}