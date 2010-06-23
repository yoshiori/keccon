(function(){
    var COOKIE_NAME = 'since_id';
    var growl = function(){
        var _since = $.cookie(COOKIE_NAME)
        $.ajax({
            url : "http://search.twitter.com/search.json",
            dataType : "jsonp",
            data : {
                q : "#keccon",
                since_id : _since
            },
            success : function(json){
                $.each(json['results'],function(i,obj){
                    if( _since != null){
                        $.pnotify({
                            pnotify_title: obj['from_user'],
                            pnotify_text: obj['text'],
                            pnotify_notice_icon: 'ui-icon ui-icon-contact',
                        });
                    }
                    var id = obj['id'];
                    if( id > $.cookie(COOKIE_NAME) ){
                        $.cookie(COOKIE_NAME, id, { path: '/', expires: 60 });
                    }
                });
            },
            error : function(){
                $.pnotify({
                    pnotify_title: 'error',
                    pnotify_text: '取得出来ませんでした',
                    pnotify_type: 'error',
                });
            }
        });
        setTimeout(growl,30000);
    };
    $(document).ready(function(){
            //        growl();
    });
})();