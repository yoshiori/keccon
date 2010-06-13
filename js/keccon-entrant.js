(function(){
    $(document).ready(function(){
        $.getJSON("/script/api/entrant", function(json){
            var ent = $("#entrant");
            $.each(json.result,function(i,data){
                ent.append('<a>')
                    .find('a:last')
                    .attr({'href' : 'http://twitter.com/' + data.username})
                    .append('<img>')
                    .find('img:last')
                    .attr({'src' : data.picture, 'alt' : data.name});
            });
        });
    });
})();