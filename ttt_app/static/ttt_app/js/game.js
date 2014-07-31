var player = "X";

if (player_first == "false")
{
    player = "O"
}

function drawBoard(board_string) {
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

$(document).ready( function () {
    $(".btn").html(player);
}

);