function get_link_state(data, i = 0) { 
    if(document.getElementsByClassName(data + 'link_finder')[i]) {
        var link_data = document.getElementsByClassName(data + 'link_finder')[i];
        
        get_link_state(data, i + 1);

        var xhr = new XMLHttpRequest();
        xhr.open("GET", link_data.href.replace('/w/', '/api/w/').replace(/#([^#]*)/, '') + "?exist=1", true);
        xhr.send(null);

        xhr.onreadystatechange = function() {
            if(this.readyState === 4 && this.status === 200) {
                if(JSON.parse(this.responseText)['exist'] !== '1') {
                    document.getElementsByClassName(data + 'link_finder')[i].id = "not_thing";
                } else {
                    document.getElementsByClassName(data + 'link_finder')[i].id = "";
                }
            }
        }
    }
}

function get_file_state(data, i = 0) {       
    if(document.getElementsByClassName(data + 'file_finder_1')[i]) {
        var file_data = document.getElementsByClassName(data + 'file_finder_1')[i];
        
        get_file_state(data, i + 1);

        var xhr = new XMLHttpRequest();
        xhr.open("GET", file_data.src.replace('/image/', '/api/image/'), true);
        xhr.send(null);
        
        xhr.onreadystatechange = function() {
            if(this.readyState === 4 && this.status === 200) {
                if(JSON.parse(this.responseText)['exist'] !== '1') {
                    document.getElementsByClassName(data + 'file_finder_1')[i].style = "display: none;";
                } else {
                    document.getElementsByClassName(data + 'file_finder_2')[i].innerHTML = "";
                }
            }
        }
    }
}

function load_include(title, name, p_data) {
    var o_data = document.getElementById(name);

    var change = '';
    for(key in p_data) {
        change += '@' + p_data[key][0].replace('&', '<amp>') + '@,' + p_data[key][1].replace(',', '<comma>').replace('&', '<amp>') + ','
    }
    
    var url = "/api/w/" + encodeURI(title) + "?include=" + name + "&change=" + change;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send(null);

    xhr.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
            if(this.responseText === "{}\n") {
                o_data.innerHTML = "";

                document.getElementsByClassName(name)[0].id = "not_thing";
            } else {
                var o_p_data = JSON.parse(this.responseText);
                
                var g_data = o_p_data['data'];
                o_data.innerHTML = g_data;

                eval(o_p_data['js_data']);
            }
        }
    }
}

function page_count() {
    var n_ver = document.getElementsByClassName('all_page_count');

    var url = "/api/title_index";

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send(null);

    xhr.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
            var i = 0;
            while(1) {
                if(n_ver[i]) {
                    n_ver[i].innerHTML = JSON.parse(this.responseText)['count'];
                    i += 1;
                } else {
                    break;
                }
            }
        }
    }
}