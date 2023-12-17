import java.util.*

data class CrucibleState(
    val cumulativeHeatLoss:Int,
    val row: Int,
    val col: Int,
    val rowDirection:Int,
    val colDirection:Int,
    val stepsInThisDirection:Int
    ): Comparable<CrucibleState> {
    override fun compareTo(other: CrucibleState) = compareValuesBy(
        this,
        other,
        {it.cumulativeHeatLoss},
        {it.row},
        {it.col},
        {it.rowDirection},
        {it.colDirection},
        {it.stepsInThisDirection}
        );
}

data class Direction(val rowChange:Int, val colChange:Int)

fun getDirectionsThatArentStraightAheadOrBehind(rowDirection: Int, colDirection:Int): List<Direction>{
    val allDirectionList = listOf(
        Direction(0,1),  // RIGHT
        Direction(1,0),  // DOWN
        Direction(0,-1), // LEFT
        Direction(-1, 0) // UP
    )

    return allDirectionList
        .filter { (it.rowChange != rowDirection) && (it.colChange != colDirection) }
        .filter { (it.rowChange != (rowDirection * -1)) && (it.colChange != (colDirection * -1)) }
}

fun main(args: Array<String>) {
    val rowList = object {}.javaClass.getResourceAsStream("input.txt")?.bufferedReader()?.readLines()
        ?: throw Error("row list was null")

    val grid = rowList.map { row -> row.map { char -> char.toString().toInt() } }

    val openQueue = PriorityQueue<CrucibleState>()
    val seen = hashSetOf<CrucibleState>();

    val rowCount = grid.count()
    val colCount = grid[0].count()

    val targetRow = rowCount - 1
    val targetCol = colCount - 1

    val allDirectionList = listOf(
        Direction(0,1),  // RIGHT
        Direction(1,0),  // DOWN
        Direction(0,-1), // LEFT
        Direction(-1, 0) // UP
    )

    // add initial state.
    // first square counts as 0 heat loss, is at (0,0), has no direction, and has taken no steps
    openQueue.add(CrucibleState(0,0,0,0,0,0))

    while(!openQueue.isEmpty()){
        val currentState = openQueue.remove()

        // we have hit the target node
        if(currentState.row == targetRow && currentState.col == targetCol){
            println(currentState.cumulativeHeatLoss)
            break;
        }

        // heat loss may be different each time we arrive here but want them all to hash the same in the seen set.
        val currentStateWithZeroHeatLoss = CrucibleState(0, currentState.row, currentState.col, currentState.rowDirection, currentState.colDirection, currentState.stepsInThisDirection)
        if (currentStateWithZeroHeatLoss in seen){
            continue
        }

        seen.add(currentStateWithZeroHeatLoss)

        // special case for (0,0) since we have no direction
        if(currentState.row == 0 && currentState.col == 0){
            // attempt to add all neighbours (left and up will be out of bounds)
            for (neighbourDirection in allDirectionList){
                val newRow = 0 + neighbourDirection.rowChange
                val newCol = 0 + neighbourDirection.colChange

                // bounds check this new point and add it to the priority queue if valid
                if(newRow in 0..<rowCount && newCol in 0..<colCount) {
                    openQueue.add(
                        CrucibleState(
                            currentState.cumulativeHeatLoss + grid[newRow][newCol],
                            newRow,
                            newCol,
                            neighbourDirection.rowChange,
                            neighbourDirection.colChange,
                            1 // change in direction means reset the step count
                        )
                    )
                }
            }
        }
        else{
            if(currentState.stepsInThisDirection < 3){
                val newRow = currentState.row + currentState.rowDirection
                val newCol = currentState.col + currentState.colDirection

                // bounds check this new point and add it to the priority queue if valid
                if(newRow in 0..<rowCount && newCol in 0..<colCount){
                    openQueue.add(CrucibleState(
                        currentState.cumulativeHeatLoss + grid[newRow][newCol],
                        newRow,
                        newCol,
                        currentState.rowDirection,
                        currentState.colDirection,
                        currentState.stepsInThisDirection + 1
                        )
                    )
                }
            }

            // now we can add all directions that arent straight ahead, and arent behind us
            for (neighbourDirection in getDirectionsThatArentStraightAheadOrBehind(currentState.rowDirection, currentState.colDirection)){
                val newRow = currentState.row + neighbourDirection.rowChange
                val newCol = currentState.col + neighbourDirection.colChange

                // bounds check this new point and add it to the priority queue if valid
                if(newRow in 0..<rowCount && newCol in 0..<colCount){
                    openQueue.add(CrucibleState(
                        currentState.cumulativeHeatLoss + grid[newRow][newCol],
                        newRow,
                        newCol,
                        neighbourDirection.rowChange,
                        neighbourDirection.colChange,
                        1 // change in direction means reset the step count
                    )
                    )
                }
            }
        }
    }
}