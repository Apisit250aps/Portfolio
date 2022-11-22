var work_list = [['Home', ''], ['Library', 'library'], ['Member', 'member']]

function work_render() {

    for (i = 0; i < work_list.length; i++) {
        document.write(`<a class="home-link" href="${work_list[i][1]}">${work_list[i][0]}</a>`);
    }

}

