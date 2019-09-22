function thumb(id, like) {
    var type = 0;
    if(like) {
        type = 1;
    }
    $.ajax({
        url: `/video.json?id=${id}`,
        type: "POST",
        data: {'type': type/*, 'removing': removing*/},
        success: function(result) {
            if(like){
                $('#like').text(result.video.likes + " 👍🏼");
            } else {
                $('#dislike').text(result.video.dislikes + " 👎🏼");
            }
        }
    })
}
