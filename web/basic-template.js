
function ||name||(callback, id){
    return function(|args|) {
        var params;
        params = {|args|};
        hackkit_jsonp_handler(||method||, params, id, callback);
    };
}
