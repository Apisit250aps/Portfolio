var work_list = [['Home', ''], ['Library', 'library']]

function work_render() {

    for (i = 0; i < work_list.length; i++) {

        document.write(`<a class="nav-link" href="${work_list[i][1]}">${work_list[i][0]}</a>`)


    }

}

