from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import sqlite3 

_data = ['นายเจษฎา ตอนศรี' 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายชนะไชย์ เลิศสงคราม'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายบวรภัค ศรีพล'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายปฐม กล่อมปัญญา'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายปริญญา เรืองคำ'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายปรีชา ไชยนะรา'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายปวฤทธิ์ จิตหาญ'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายวัณณุวรรธน์ ศรีวงศ์แผน'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายสายฟ้า ธานี'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายอนุชา กัญญา'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายอภิสิทธิ์ สายทอง'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'สาวณัฐธยาน์ พันพิพัฒน์'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'สาวนวรรณธร แพงอก'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'สาวพิยดา ยิ้มจูงนาง'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'สาวแพรวพรรณ สุขเกษม'	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายนรวิชญ์ ไก่แก้ว' 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 
,'นายรัชชานนท์ เกษแก้ว']


# try :
#         con = sqlite3.connect('member.sqlite3')
#         cur = con.cursor()
        
#         for i in range(len(_data)):
#             sql = "insert into Students values (?,?)"
#             id = f'6512732{101+i}'
#             param = [id, _data[i]]
#             cur.execute(sql, param)
#             con.commit()
# except EOFError as err:
#     print(err)

 
# cur.close()
# con.close()


def member_system(request):
    data = {
        'title':'Register'
    }
    return render(request, 'system/member/register.html', data)

def login(request):
    data = {'title':'Login'}
    return render(request, 'system/member/login.html', data)
    

