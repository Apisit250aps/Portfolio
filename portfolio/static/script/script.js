var work_list = [['Home', ''], ['Library', 'statics/library'], ['Member', 'system/member/register']]
var skills = ['Python', 'Django', 'JavaScript', 'HTML, CSS, Bootstrap', 'JAVA']
var contact = [['Facebook', 'https://web.facebook.com/aps.apisit.250/'], ['GitHub', 'https://github.com/Apisit250aps']]

function work_render() {

    for (i = 0; i < work_list.length; i++) {
        document.write(`<li><a class="th-txt text-white" href="${work_list[i][1]}">${work_list[i][0]}</a></li>`);
    }

}

function skill_render() {
    for (i = 0; i < skills.length; i++) {
        document.write(`<li class="th-txt text-light">${skills[i]}</li>`)
    }

}

function contact_render() {
    for (i = 0; i < contact.length; i++) {
        document.write(`<li><a class="th-txt text-white" href="${contact[i][1]}">${contact[i][0]}</a></li>`)
    }
}

