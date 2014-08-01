var player = "X";
var result = "";
var board_string = "---------";


if (! playerFirst)
{
    player = "O"
}


function drawBoard() {
    for(var i in board_string)
    {
        if ( board_string[i] !== "-")
        {
            var $board_cell = $("#position"+i);
            $board_cell.html(board_string[i].toUpperCase());
            $board_cell.removeClass("button-container");
            $board_cell.addClass("xo");
        }
    }
    $(".btn").html(player);
}


function advance() {
    $.ajax({
                url: advanceURL+ '/' + playerFirst.toString()+'/'+board_string,
                type: "GET",
                success: function(json) {
                    board_string = json.board;
                    result = json.wins;
                    drawBoard();
                    if (result !== "")
                    {
                        showResult();
                    }
                }
           });
}


// called when a player clicks a button
function playerClick() {
    $parent = $(this).parent();
    var newBoard = "";
    var cellNumber = $parent[0].id[8];
    for(var i in board_string)
    {
        if (i === cellNumber)
        {
         newBoard += player.toLowerCase();
        }
        else
        {
            newBoard += board_string[i];
        }
    }
    board_string = newBoard;
    drawBoard(board_string);
    advance();
}


function showResult() {

    switch (result)
    {
        case ("x"):
            if (playerFirst)
            {
                var heading = "Player (X) Wins!";
            }
            else
            {
                var heading = "Perfect (X) Wins!";
            }
            break;
        case ("o"):
            if (playerFirst)
            {
                var heading = "Perfect (O) Wins!";
            }
            else
            {
                var heading = "Player (O) Wins!";
            }
            break;
        default:
            var heading = "It's a tie.";
            break;
    }
    $("h1").html(heading);
    $("h1").after('<a href="/">Play again</a>');
}


$(document).ready( function () {
    $(".btn").click(playerClick);
    drawBoard(board_string);
    if (! playerFirst)
    {
        advance();
    }
}

);