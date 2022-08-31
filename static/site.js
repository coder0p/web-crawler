function build_lyrics(song) {
    ret = $(`<div>
    <center><h1> ${song.name}
    <i class="fa-solid fa-circle-play"></i>
     </h1></center>

    <center>
    <em>
    ${song.lyrics.replaceAll("\n","<br/>")}
    </em>
    </center>
    </div>`)

    return ret;
}



function renderLyrics(e) {
    console.log("page loaded!");
        e.preventDefault();
        $("div.lyrics").text("Loading ... ");   
        $.ajax({url : e.target.href,
                dataType: 'json',
                success: function(data) {
                    $("div.lyrics").html(build_lyrics(data.song));
                    var text = e.target.innerText;
                    var currentChoice = e.target.parentNode;
                    $(currentChoice).html(text);
                    $("li.songlist").html(
                        `<a class = "songLink" href="/song/${$(".songlist")
                .attr("id")}">${$(".songlist").text()}<a/>`
                    )
                    $(".songlist a").click(renderLyrics);
            $(".songlist").attr("class", "songsLink  ps-2 py-3 m-1");
            $(currentChoice).attr("class", "songlist  ps-2 py-3 m-1 ");
                    
                }
            });
        
        
}

function main() {
    
    $("a.songLink").click(renderLyrics)
};


$(main);