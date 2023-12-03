val symbols = "=*+/#-$&%@".toCharArray().toList()

enum class FoundSymbol {
    GEAR,
    OTHER,
    NONE
}

data class FoundSymbolWithLocation (
    val symbol: FoundSymbol,
    val location: Coordinate
)

data class Coordinate (
    val row: Int,
    val col: Int
)

fun main() {
    val rowList = object {}.javaClass.getResourceAsStream("input.txt")?.bufferedReader()?.readLines()
        ?: throw Error("row list was null")

    val rowCount = rowList.size
    val columnCount = rowList[0].count()

    var currentlyParsingNumber = ""
    var currentNumberIsAPartNumber = false

    val partNumberList = mutableListOf<Int>()

    // a map of gear location to part numbers adjacent to that gear
    val gearAdjacencyMap = mutableMapOf<String,MutableList<Int>>()

    // hold the location of a gear adjacent to the number we're currently parsing
    var currentAdjacentGear = FoundSymbolWithLocation(FoundSymbol.NONE,Coordinate(0,0))

    for (row in 0..<rowCount) {
        for ( col in 0..<columnCount) {
            val currentChar = rowList[row][col]
            if (currentChar.isDigit()) {
                currentlyParsingNumber += currentChar
                val anySymbolsAdjacent = symbolInAnyDirectionFrom(row,col,rowCount,columnCount, rowList)
                if(anySymbolsAdjacent.symbol == FoundSymbol.GEAR){
                    currentNumberIsAPartNumber = true
                    currentAdjacentGear = anySymbolsAdjacent
                }
                else if(anySymbolsAdjacent.symbol == FoundSymbol.OTHER){
                    currentNumberIsAPartNumber = true
                }
            } else {
                if(currentlyParsingNumber != ""){
                    // We were previously parsing a number
                    // but have hit a non-number
                    // store that number in the part list if we ever saw a symbol
                    if(currentNumberIsAPartNumber){
                        partNumberList.add(currentlyParsingNumber.toInt())

                        // if we found a gear while parsing this number, store the part number in the
                        // gear adjacency map as well as the part number list
                        if(currentAdjacentGear.symbol == FoundSymbol.GEAR){
                            val key = "${currentAdjacentGear.location.row},${currentAdjacentGear.location.col}"

                            if(!gearAdjacencyMap.containsKey(key)){
                                gearAdjacencyMap[key] = mutableListOf(currentlyParsingNumber.toInt())
                            }
                            else{
                                gearAdjacencyMap[key]?.add(currentlyParsingNumber.toInt())
                            }
                        }
                    }
                }

                // it's safe to reset state any time we land on a non-number
                currentlyParsingNumber = ""
                currentAdjacentGear = FoundSymbolWithLocation(FoundSymbol.NONE,Coordinate(0,0))
                currentNumberIsAPartNumber = false
            }
        }

        // this is an edge-case where a number finishes on the right-edge of the grid
        // do all the processing as if we just landed on a non-number after parsing a number
        if(currentlyParsingNumber != ""){
            if(currentNumberIsAPartNumber){
                partNumberList.add(currentlyParsingNumber.toInt())
                if(currentAdjacentGear.symbol == FoundSymbol.GEAR){
                    val key = "${currentAdjacentGear.location.row},${currentAdjacentGear.location.col}"

                    if(!gearAdjacencyMap.containsKey(key)){
                        gearAdjacencyMap[key] = mutableListOf(currentlyParsingNumber.toInt())
                    }
                    else{
                        gearAdjacencyMap[key]?.add(currentlyParsingNumber.toInt())
                    }
                }
            }
        }
        //numbers do not span rows so reset
        currentlyParsingNumber = ""
        currentAdjacentGear = FoundSymbolWithLocation(FoundSymbol.NONE,Coordinate(0,0))
        currentNumberIsAPartNumber = false
    }

    val total = partNumberList.reduce { sum, element -> sum + element }
    println("part 1 total -> $total")

    var adjacencySum = 0
    for ( gear in gearAdjacencyMap ){
        if(gear.value.count() == 2){
            adjacencySum += (gear.value[0] * gear.value[1])
        }
    }

    println("part 2 total -> $adjacencySum")
}

// Check if there are symbols in any direction from current coordinate
fun symbolInAnyDirectionFrom(row: Int, col: Int, rowCount: Int, columnCount: Int, rowList: List<String>) : FoundSymbolWithLocation {
    val locationsToCheck = buildAdjacencyList(row, col, rowCount, columnCount)
    var foundSymbol = FoundSymbolWithLocation(FoundSymbol.NONE, Coordinate(0,0))

    for (location in locationsToCheck){
        val isSymbol = rowList[location.row][location.col] in symbols

        // we found a symbol at that location
        if(isSymbol){
            // if its a gear
            if(rowList[location.row][location.col] == '*'){
                // return gear object
                foundSymbol = FoundSymbolWithLocation(FoundSymbol.GEAR, Coordinate(location.row, location.col))
            }
            else{
                //otherwise, we found a symbol but it wasnt a gear
                // and there is no already found gear, store the "OTHER" symbol, otherwise keep "GEAR"
                if(foundSymbol.symbol == FoundSymbol.NONE){
                    foundSymbol = FoundSymbolWithLocation(FoundSymbol.OTHER, Coordinate(location.row, location.col))
                }
            }
        }
    }

    return foundSymbol
}

// Build a list of all coordinates we need to check for symbols,
// stripping out coordinates that are not valid as they'd be outside the grid
fun buildAdjacencyList(row: Int, col: Int, rowCount: Int, columnCount: Int): List<Coordinate> {
    return listOf(
        Coordinate(row-1, col-1),
        Coordinate(row-1, col),
        Coordinate(row-1, col+1),
        Coordinate(row, col - 1),
        Coordinate(row, col + 1),
        Coordinate(row+1, col - 1),
        Coordinate(row+1, col),
        Coordinate(row+1, col + 1))
            .filter { isValidToCheckLocation(Coordinate(it.row, it.col), rowCount, columnCount) }
}

// check a given coordinate falls inside the grid boundaries
fun isValidToCheckLocation(location: Coordinate, rowCount: Int, columnCount: Int): Boolean =
    location.row in 0..<rowCount && location.col in 0..<columnCount