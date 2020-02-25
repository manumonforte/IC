const MAX_START_CELL = 1;
const MAX_GOAL_CELL = 1;

let start_cell_count = 0;
let goal_cell_count = 0;


let rows = 4;
let columns = 4;
let matrix = undefined;

let startNode = undefined
let goalNode = undefined

let caminoEncontrado = false;

$(() => {

    //Default Board
    drawBoard(4, 4)

    //Create new Board
    $('#create-new-board').on("click", () => {
        createBoard()
    });


    //TODO: CREAR FUNCION CLEARBUTTONS Y AÑADIMOS MARKED AL QUE PULSAMOS
    /*GET SELECTED ONLY ONE BUTTON*/
    $('#place_barrier_button').on("click", () => {
        if ($('#place_start_button').hasClass('marked')) {
            $('#place_start_button').removeClass('marked')
        }
        if ($('#place_goal_button').hasClass('marked')) {
            $('#place_goal_button').removeClass('marked')
        }
        if ($('#clear_cell_button').hasClass('marked')) {
            $('#clear_cell_button').removeClass('marked')
        }
        if ($('#dangerous_cell_button').hasClass('marked')) {
            $('#dangerous_cell_button').removeClass('marked')
        }
        $('#place_barrier_button').addClass("marked");
    })

    $('#place_goal_button').on("click", () => {
        if ($('#place_start_button').hasClass('marked')) {
            $('#place_start_button').removeClass('marked')
        }
        if ($('#place_barrier_button').hasClass('marked')) {
            $('#place_barrier_button').removeClass('marked')
        }
        if ($('#clear_cell_button').hasClass('marked')) {
            $('#clear_cell_button').removeClass('marked')
        }
        if ($('#dangerous_cell_button').hasClass('marked')) {
            $('#dangerous_cell_button').removeClass('marked')
        }
        $('#place_goal_button').addClass("marked");
    })

    $('#place_start_button').on("click", () => {
        if ($('#place_barrier_button').hasClass('marked')) {
            $('#place_barrier_button').removeClass('marked')
        }
        if ($('#place_goal_button').hasClass('marked')) {
            $('#place_goal_button').removeClass('marked')
        }
        if ($('#clear_cell_button').hasClass('marked')) {
            $('#clear_cell_button').removeClass('marked')
        }
        if ($('#dangerous_cell_button').hasClass('marked')) {
            $('#dangerous_cell_button').removeClass('marked')
        }
        $('#place_start_button').addClass("marked");
    })

    $('#clear_cell_button').on("click", () => {
        if ($('#place_barrier_button').hasClass('marked')) {
            $('#place_barrier_button').removeClass('marked')
        }
        if ($('#place_goal_button').hasClass('marked')) {
            $('#place_goal_button').removeClass('marked')
        }
        if ($('#place_start_button').hasClass('marked')) {
            $('#place_start_button').removeClass('marked')
        }
        if ($('#dangerous_cell_button').hasClass('marked')) {
            $('#dangerous_cell_button').removeClass('marked')
        }
        $('#clear_cell_button').addClass("marked");
    })

    $('#dangerous_cell_button').on("click", () => {
        if ($('#place_barrier_button').hasClass('marked')) {
            $('#place_barrier_button').removeClass('marked')
        }
        if ($('#place_goal_button').hasClass('marked')) {
            $('#place_goal_button').removeClass('marked')
        }
        if ($('#place_start_button').hasClass('marked')) {
            $('#place_start_button').removeClass('marked')
        }
        if ($('#clear_cell_button').hasClass('marked')) {
            $('#clear_cell_button').removeClass('marked')
        }
        $('#dangerous_cell_button').addClass("marked");
    })


    /* SELECT ONE BUTTON TO DRAW IN BOARD*/
    $(document).on("click","td",() => {
        //logica para pintar celda
        console.log(start_cell_count);
        if ($('#place_start_button').hasClass('marked') && start_cell_count < MAX_START_CELL) {
            //If the cell was goal update count
            if ($(event.target).hasClass('goal_cell')) {
                goal_cell_count -= 1;
                $(event.target).removeClass();
            }
            else if ($(event.target).hasClass('path')) {
                $(event.target).removeClass()
            }
            $(event.target).addClass("start_cell");
            start_cell_count += 1;
        }
        else if ($('#place_goal_button').hasClass('marked') && goal_cell_count < MAX_GOAL_CELL) {
            //If the cell was start update count
            if ($(event.target).hasClass('start_cell')) {
                start_cell_count -= 1;
                $(event.target).removeClass('start_cell')
            }
            else if ($(event.target).hasClass('path')) {
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('barrier_cell')) {
                $(event.target).removeClass()
            }
            $(event.target).addClass("goal_cell");
            goal_cell_count += 1;
        }
        else if ($('#place_barrier_button').hasClass('marked')) {
            //if the cell was start or goal update count
            if ($(event.target).hasClass('goal_cell')) {
                goal_cell_count -= 1;
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('start_cell')) {
                start_cell_count -= 1;
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('path')) {
                $(event.target).removeClass()
            }
            $(event.target).addClass("barrier_cell");
        }
        else if ($('#clear_cell_button').hasClass('marked')) {
            //if the cell was start or goal update count
            if ($(event.target).hasClass('goal_cell')) {
                goal_cell_count -= 1;
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('start_cell')) {
                start_cell_count -= 1;
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('barrier_cell')) {
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('path')) {
                $(event.target).removeClass()
            }
        }
        else if ($('#dangerous_cell_button').hasClass('marked')) {
            //if the cell was start or goal update count
            if ($(event.target).hasClass('goal_cell')) {
                goal_cell_count -= 1;
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('start_cell')) {
                start_cell_count -= 1;
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('path')) {
                $(event.target).removeClass()
            }
            else if ($(event.target).hasClass('barrier_cell')) {
                $(event.target).removeClass()
            }
            $(event.target).addClass("dangerous_cell");
        }
        
        event.preventDefault();
    })

    /* START BUTTON*/
    $("#start").on("click", () => {
        if (!start_cell_count || !goal_cell_count) {
            alert("Falta celda de inicio o final");
        }
        else {
            clearPath();
            boardtoMatrix();
            let path = findTrip()
            if (!path.length) alert("No hay solución");
            else drawPath(path);
            console.log(path);
        }
    })

})



/**
 * Draw new board given rows and columns
 * @param {*} rows 
 * @param {*} columns 
 */
function drawBoard(rows, columns) {
    $("table").empty();
    //create cells
    for (let i = 0; i < rows; i++) {
        let newRow = $("<tr></tr>")
        for (let j = 0; j < columns; j++) {
            let newCol = $("<td></td>");
            newCol.attr("id", "i" + i + "_" + "j" + j);
            newRow.append(newCol);
        }
        $("table").append(newRow)
    }

    //style in cells
    $('td').css({ "padding": "25px" });
}

/**
 * Creates new board when user press the button
 */
function createBoard() {
    if ($("#rows-quantity").val() > 10 || $("#rows-quantity").val() < 2 || $("#columns-quantity").val() < 2 || $("#columns-quantity").val() > 10) {
        alert("Las filas columnas deben estar comprendidas entre 2 y 10");
    }
    else {
        drawBoard($("#rows-quantity").val(), $("#columns-quantity").val());
        start_cell_count = 0;
        goal_cell_count = 0;
        rows = $("#rows-quantity").val();
        columns = $("#columns-quantity").val()
    }
}

/**
 * Save the current board into the matrix
 */
function boardtoMatrix() {
    caminoEncontrado = false;
    matrix = [];
    for (let i = 0; i < rows; i++) {
        matrix[i] = [];
        for (let j = 0; j < columns; j++) {
            //Start
            if ($(`#i${i}_j${j}`).attr('class') == "start_cell") {
                startNode = { i, j, f: 0, g: 0, h: undefined, parent: undefined, dangerous: 0, representation: "*" };
                matrix[i][j] = startNode;
            }
            //Goal
            else if ($(`#i${i}_j${j}`).attr('class') == "goal_cell") {
                goalNode = { i, j, f: undefined, g: undefined, h: undefined, parent: undefined, dangerous: 0, representation: "#" };
                matrix[i][j] = goalNode;
            }
            //Barrier
            else if ($(`#i${i}_j${j}`).attr('class') == "barrier_cell") matrix[i][j] = { i, j, f: undefined, g: undefined, h: undefined, parent: undefined, dangerous: 0, representation: "X" };

            //Dangerous
            else if ($(`#i${i}_j${j}`).attr('class') == "dangerous_cell") matrix[i][j] = { i, j, f: undefined, g: undefined, h: undefined, parent: undefined, dangerous: 0.1, representation: "^" };

            //Empty
            else
                matrix[i][j] = { i, j, f: undefined, g: undefined, h: undefined, parent: undefined, dangerous: 0, representation: " " };
        }
    }

    startNode.h = h(startNode);
    startNode.f = startNode.h;

}


/********************************************************* */
/****************ALGORITHIM A STAR *********************** */
/********************************************************* */

function findTrip() {
    let openList = [];
    let closeList = [];
    let trip = [];

    openList.push(startNode);

    //while the open list isn't empty and we don't find the end
    while (openList.length > 0 && !caminoEncontrado) {
        let min = Infinity;
        let nodeSelected = undefined;

        //get node with less f
        openList.forEach(node => {
            if (node.f < min) {
                min = node.f;
                nodeSelected = node;
            }
        })
        //if the less node is goalNode
        if (compareNodes(nodeSelected, goalNode)) {
            goalNode.parent = nodeSelected.parent;
            caminoEncontrado = true;
            //create solution(path) and return it
            while (nodeSelected.parent != undefined) {
                trip.push(nodeSelected);
                nodeSelected = nodeSelected.parent;
            }
            trip.push(startNode);

        }
        else {//put the less node isn't the goal
            //put it in the close list
            closeList.push(nodeSelected);
            //remove it from the open list
            openList.splice(openList.indexOf(nodeSelected), 1);
            //expand node

            //search Neighbours
            neighboursList = getNeighbours(nodeSelected);
            neighboursList.forEach(neighbour => {
                //if the neighbour doesn't appear in close, open list and the node is not a barrier or the start
                if (closeList.indexOf(neighbour) == -1 && neighbour.representation != "X" && openList.indexOf(neighbour) == -1 && neighbour.representation != "*") {
                    neighbour.parent = nodeSelected;
                    neighbour.g = (nodeSelected.i != neighbour.i && nodeSelected.j != nodeSelected.j) ? (nodeSelected.g + Math.sqrt(2)) : (nodeSelected.g + 1);
                    neighbour.h = h(neighbour);
                    neighbour.f = neighbour.g + neighbour.h + neighbour.dangerous;
                    openList.push(neighbour);
                }
                //if the neighbour doesn't appear in close, and appears open list
                else if (closeList.indexOf(neighbour) == -1 && neighbour.representation != "X" && openList.indexOf(neighbour) != -1 && neighbour.representation != "*") {
                    //calculate new F
                    gAux = (nodeSelected.i != neighbour.i && nodeSelected.j != nodeSelected.j) ? (nodeSelected.g + Math.sqrt(2)) : (nodeSelected.g + 1);
                    hAux = h(neighbour);
                    fAux = gAux + hAux + neighbour.dangerous;
                    //update F
                    if (fAux < neighbour.f) {
                        neighbour.f = fAux;
                        neighbour.h = hAux;
                        neighbour.g = gAux;
                        neighbour.parent = nodeSelected;
                    }

                }
            })

        }
    }
    return trip;
}

/**
 * Returns the heuristic distance between node gicen and the goalNode
 * @param {*} actualNode 
 */
function h(actualNode) {
    return Math.sqrt(Math.pow((goalNode.i - actualNode.i), 2) + Math.pow((goalNode.j - actualNode.j), 2));
}

/**
 * Two nodes are equal if their corrdinates are the same
 * @param {*} a 
 * @param {*} b 
 */
function compareNodes(a, b) {
    return (a.i == b.i && a.j == b.j);
}

/**
 * Get Neighbours given a node
 * @param {*} node 
 */
function getNeighbours(node) {
    let x = node.i;
    let y = node.j;
    neighbours = [];
    if (x - 1 >= 0 && y - 1 >= 0) neighbours.push(matrix[x - 1][y - 1]);
    if (y - 1 >= 0) neighbours.push(matrix[x][y - 1]);
    if (x + 1 < matrix.length && y - 1 >= 0) neighbours.push(matrix[x + 1][y - 1]);
    if (x - 1 >= 0) neighbours.push(matrix[x - 1][y]);
    if (x + 1 < matrix.length) neighbours.push(matrix[x + 1][y]);
    if (x - 1 >= 0 && y + 1 < matrix[0].length) neighbours.push(matrix[x - 1][y + 1]);
    if (y + 1 < matrix[0].length) neighbours.push(matrix[x][y + 1]);
    if (x + 1 < matrix.length && y + 1 < matrix[0].length) neighbours.push(matrix[x + 1][y + 1]);

    return neighbours;

}

function drawPath(path) {
    path.forEach(elem => {         
           if (!$(`#i${elem.i}_j${elem.j}`).hasClass("start_cell") && !$(`#i${elem.i}_j${elem.j}`).hasClass("goal_cell")) $(`#i${elem.i}_j${elem.j}`).addClass("path");
            
    })
}

function clearPath(){
    if(matrix != undefined){
    for (let i = 0; i < rows; i++) {
            matrix[i] = [];
            for (let j = 0; j < columns; j++) {
                if ($(`#i${i}_j${j}`).attr('class') === "path") $(`#i${i}_j${j}`).removeClass("path");
            }
        }
    }
}
