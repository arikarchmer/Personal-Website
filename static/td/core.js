/**
 * Created by arikarchmer on 6/8/16.
 */

var counter = 0;
function change_message(x, mes1, mes2) {
    if (counter % 2 == 0) {
        x.innerHTML = mes2.fontsize(4);
        counter = counter + 1;
    } else {
        x.innerHTML = mes1;
        counter = counter + 1;
    }
}
function rotate_img(x, title) {
    x.style.transform = "rotate(30deg)";
    document.getElementById(title).style.visibility = 'visible';
}
function reg_img(x, title) {
    x.style.transform = "rotate(360deg)";
    document.getElementById(title).style.visibility = 'hidden';
}
function parse_info() {
    // parse keyword, city, state
    var info_lst = document.getElementById('info').elements[0].value.split(', ');
    var keyword = info_lst[0];
    var city = info_lst[1];
    var state = info_lst[2];
    window.location = '/twitterdata/results/city_state?keyword=' + keyword +'&city=' + city + '&state=' + state;
}
function invalid_search() {
    var search = document.getElementById('/search');
    search.style.color = 'red';
}