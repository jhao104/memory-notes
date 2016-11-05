/**
 * Created by Administrator on 2016/11/5.
 */

function GenerateContentList() {
    $(".post-content").find("h2,h3,h4,h5,h6").each(function (i, item) {
        var tag = $(item).get(0).localName;
        $(item).attr("id", "wow" + i);
        $("#AnchorContent").append('<li><a class="new' + tag + ' anchor-link"  href="#wow' + i + '">' + (i + 1) + " · " + $(this).text() + '</a></li>');
        $(".newh2").css("margin-left", 0);
        $(".newh3").css("margin-left", 20);
        $(".newh4").css("margin-left", 40);
        $(".newh5").css("margin-left", 60);
        $(".newh6").css("margin-left", 80);
    });
    $("#AnchorContentToggle").click(function () {
        var text = $(this).html();
        if (text == "目录[-]") {
            $(this).html("目录[+]");
            $(this).attr({"title": "展开"});
        } else {
            $(this).html("目录[-]");
            $(this).attr({"title": "收起"});
        }
        $("#AnchorContent").toggle();
    });
}


