$(document).ready(function(){
    $(".editImage").click(function(){
    //    alert( $(".in img ").length);
        $('.in img').selectAreas({
            minSize: [10, 10],
            onChanged: displayAreas,
            width: 500,
            areas: [
                {
                    x: 10,
                    y: 20,
                    width: 60,
                    height: 100,
                }
            ]
        });
    });

    $(".blurArea").click(function(){
        var areas =  $('.in img').selectAreas('areas');
        // alert($('.in img').width());
        var text=displayAreas(areas);
        alert($('.in img').width());
        // alert(text);
         window.location=window.location.href+"tag/reject/"+ $(this).attr("postid")+"/" +$('.in img').width()+"!"+text;
    });
});




    var selectionExists;

    function areaToString (area) {
        return parseInt( area.x) + ':' + parseInt(area.y)  + ':' + parseInt(area.width) + ':' + area.height+" "
    }

    function output (text) {
        $('#output').html(text);
    }

    // Log the quantity of selections
    function debugQtyAreas (event, id, areas) {
        console.log(areas.length + " areas", arguments);
    };

    // Display areas coordinates in a div
    function displayAreas (areas) {
        var text = "";
        $.each(areas, function (id, area) {
            text += areaToString(area);
        });
       return text;
    };