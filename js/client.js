const MAX_START_CELL = 1;
const MAX_GOAL_CELL = 1;

let start_cell_count = 0;
let goal_cell_count = 0;


let rows = 4;
let columns = 4;
let matrix = undefined;

$(()=>{

    //Default Board
    drawBoard(4,4)

    //Create new Board
    $('#create-new-board').on("click", ()=> {
        createBoard()
    });

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
        $('#clear_cell_button').addClass("marked");
    })


    /* SELECT ONE BUTTON TO DRAW IN BOARD*/
    $("table").mousedown(() => {
        IsClickDown = true;
        //logica para pintar celda
        if($('#place_start_button').hasClass('marked') && start_cell_count < MAX_START_CELL){
            //If the cell was goal update count
            if($(event.target).hasClass('goal_cell')){
                goal_cell_count  -=1;
            }
            $(event.target).addClass("start_cell");
            start_cell_count +=1;
            
        }
        else if($('#place_goal_button').hasClass('marked') && goal_cell_count < MAX_GOAL_CELL){
            //If the cell was start update count
            if($(event.target).hasClass('start_cell')){
                start_cell_count  -=1;
            }
            $(event.target).addClass("goal_cell");
            goal_cell_count  +=1;
        }
        else if($('#place_barrier_button').hasClass('marked')){
            //if the cell was start or goal update count
            if($(event.target).hasClass('goal_cell')){
                goal_cell_count  -=1;
            }
            else if($(event.target).hasClass('start_cell')){
                start_cell_count  -=1;
            }
            $(event.target).addClass("barrier_cell");
        }
        else if($('#clear_cell_button').hasClass('marked')){
            //if the cell was start or goal update count
            if($(event.target).hasClass('goal_cell')){
                goal_cell_count  -=1;
            }
            else if($(event.target).hasClass('start_cell')){
                start_cell_count  -=1;
            }
            $(event.target).removeClass();
        }

        IsClickDown = false;
    })

    /* START BUTTON*/
    $("#start").on("click",()=>{
        if(!start_cell_count || !goal_cell_count){
            alert("Falta celda de inicio o final");
        }
        else {
            console.log("Pintando matriz");
            boardtoMatrix()
        }
    })

})



/**
 * Draw new board given rows and columns
 * @param {*} rows 
 * @param {*} columns 
 */
function drawBoard(rows, columns){
    $("table").empty();
    //create cells
    for (let i = 0; i < rows; i++){
        let newRow = $("<tr></tr>")
        for (let j = 0; j < columns; j++){
            let newCol = $("<td></td>");
            newCol.attr("id","i"+ i + "_" + "j"+ j);
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
function createBoard(){
    if($("#rows-quantity").val() > 10 || $("#rows-quantity").val() < 2 || $("#columns-quantity").val() < 2 || $("#columns-quantity").val() > 10 ){
        alert("Las filas columnas deben estar comprendidas entre 2 y 10");
    }
    else{
        drawBoard($("#rows-quantity").val(), $("#columns-quantity").val());
        start_cell_count = 0;
        goal_cell_count = 0;
        rows = $("rows-quantity").val();
        columns = $("columns-quantity").val()        
    }
}

//TODO: Funcion para guardar tablero en una matriz
/**
 * Save the current board into the matrix
 */
function boardtoMatrix(){
    matrix = []; 
    for(let i = 0; i < rows; i++){
        matrix[i] = [];
        for(let j = 0; j < columns; j++){
            //Start
            if( $(`#i${i}_j${j}`).attr('class') === "start_cell") matrix[i][j] = "*";
            //Goal
            else if ($(`#i${i}_j${j}`).attr('class') === "goal_cell") matrix[i][j] = "#";
            //Barrier
            else if ($(`#i${i}_j${j}`).attr('class') === "barrier_cell") matrix[i][j] = "X";
            //Empty
            else matrix[i][j] = " ";
        }
    }
}

//TODO: Funcion para resolver A *
/********************************************************* */
/****************ALGORITHIM A STAR *********************** */
/********************************************************* */
