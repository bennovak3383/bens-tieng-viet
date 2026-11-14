import json
NOTE="Example from a made-up student, Leo. Answer about your own life — any answer that fits is fine."
A={
"c01":("Tôi tên là Leo.","My name is Leo.","Leo"),
"c02":("Tôi ba mươi bốn tuổi.","I'm thirty-four.","34"),
"c03":("Tôi là người Canada.","I'm Canadian.","Canada"),
"c04":("Tôi là đầu bếp.","I'm a cook.","đầu bếp"),
"c05":("Tôi đang làm việc ở Quận 1.","I work in District 1.","Quận 1"),
"c06":("Tôi làm ở một nhà hàng nhỏ, không phải công ty.","I work at a small restaurant, not a company.","nhà hàng nhỏ"),
"c07":("Dạ có. Tôi học được bốn tháng rồi.","Yes. I've been studying for four months.","Dạ có"),
"c08":("Tôi học ở một trung tâm nhỏ ở Quận 3.","I study at a small language centre in District 3.","trung tâm nhỏ"),
"c09":("Tôi học ba ngày một tuần.","I study three days a week.","ba ngày"),
"c10":("Tôi học thứ Hai, thứ Tư và thứ Sáu.","I study on Monday, Wednesday and Friday.","thứ Hai, thứ Tư và thứ Sáu"),
"c11":("Tôi học từ chín giờ đến mười một giờ sáng.","I study from nine to eleven in the morning.","chín giờ đến mười một giờ"),
"c12":("Lớp tôi có sáu học viên.","My class has six students.","sáu học viên"),
"c13":("Có người Hàn, người Đức và người Mỹ.","There are Koreans, Germans and Americans.","Hàn, Đức, Mỹ"),
"c14":("Lớp vui, nhưng hơi khó.","The class is fun, but a bit hard.","vui, hơi khó"),
"c15":("Cô giáo rất kiên nhẫn.","The teacher is very patient.","kiên nhẫn"),
"c16":("Các bạn trong lớp dễ thương lắm.","My classmates are really nice.","dễ thương"),
"c17":("Tôi học để nói chuyện với khách và hàng xóm.","I study so I can talk with customers and neighbours.","nói chuyện với khách"),
"c18":("Chắc là hai năm.","Probably two years.","hai năm"),
"c19":("Tôi đang sống ở Sài Gòn.","I live in Saigon.","Sài Gòn"),
"c20":("Tôi sống ở quận Bình Thạnh.","I live in Bình Thạnh district.","Bình Thạnh"),
"c21":("Tôi sống ở một căn nhà nhỏ trong hẻm.","I live in a small house down an alley.","nhà nhỏ trong hẻm"),
"c22":("Tôi đi xe đạp.","I ride a bicycle.","xe đạp"),
"c23":("Học xong, tôi đi chợ mua đồ để nấu ăn.","After class I go to the market to buy food to cook.","đi chợ"),
"c24":("Tôi thức dậy lúc bảy giờ rưỡi.","I get up at half past seven.","bảy giờ rưỡi"),
"c25":("Tôi tập thể dục một chút rồi đi tắm.","I exercise a bit, then shower.","tập thể dục"),
"c26":("Tôi ăn sáng lúc tám giờ.","I have breakfast at eight.","tám giờ"),
"c27":("Tôi hay ăn bánh mì ốp la.","I often eat bánh mì with fried eggs.","bánh mì ốp la"),
"c28":("Ăn sáng xong, tôi đạp xe tới lớp.","After breakfast I cycle to class.","đạp xe tới lớp"),
"d29":("Tôi ăn trưa lúc một giờ.","I eat lunch at one.","một giờ"),
"d30":("Tôi ăn ở quán cơm tấm đầu hẻm.","I eat at the broken-rice place at the top of the alley.","quán cơm tấm"),
"d31":("Tôi ăn cơm tấm sườn.","I eat broken rice with pork chop.","cơm tấm sườn"),
"d32":("Ngon lắm, mà no lâu nữa.","Very good, and it keeps me full for ages.","ngon lắm"),
"d33":("Rẻ lắm, khoảng bốn mươi ngàn.","Very cheap, about forty thousand.","rẻ"),
"d34":("Buổi chiều tôi đi làm ở nhà hàng.","In the afternoon I go to work at the restaurant.","đi làm"),
"d35":("Có. Ngày nào tôi cũng ghé quán cà phê.","Yes. I drop by a café every day.","Có"),
"d36":("Tôi thường đi một mình.","I usually go alone.","một mình"),
"d37":("Không thường. Nhưng tôi hay nói chuyện với chủ quán.","Not often. But I often chat with the café owner.","Không thường"),
"d38":("Tôi uống cà phê đen đá.","I drink iced black coffee.","cà phê đen đá"),
"d39":("Tôi ăn tối ở nhà hàng, sau giờ làm.","I eat dinner at the restaurant, after work.","ở nhà hàng"),
"d40":("Tôi ăn món của nhà hàng, thường là bún bò.","I eat food from the restaurant, usually bún bò.","bún bò"),
"d41":("Có. Chủ nhật tôi hay đi ăn lẩu với bạn bè.","Yes. On Sundays I often go for hot pot with friends.","Có"),
"d42":("Không. Ở nhà tôi ít nấu.","No. At home I rarely cook.","Không"),
"d43":("Vì tôi nấu cả ngày ở nhà hàng rồi.","Because I already cook all day at the restaurant.","nấu cả ngày"),
"d44":("Tôi đọc truyện tiếng Việt và gọi điện cho gia đình.","I read Vietnamese stories and call my family.","đọc truyện"),
"d45":("Tôi đi ngủ lúc mười hai giờ đêm.","I go to bed at midnight.","mười hai giờ đêm"),
}
READ=[("Xin chào! Mình tên là Leo, năm nay ba mươi bốn tuổi.","Hi! My name is Leo, and I'm thirty-four."),
("Mình là người Canada, nhưng mình sống ở Sài Gòn được một năm rồi.","I'm Canadian, but I've lived in Saigon for a year."),
("Mình là đầu bếp ở một nhà hàng nhỏ ở Quận 1.","I'm a cook at a small restaurant in District 1."),
("Mình sống ở một căn nhà nhỏ trong hẻm, ở quận Bình Thạnh.","I live in a small house down an alley in Bình Thạnh."),
("Một tuần mình học tiếng Việt ba buổi: thứ Hai, thứ Tư và thứ Sáu.","I study Vietnamese three mornings a week: Monday, Wednesday and Friday."),
("Lớp học bắt đầu lúc chín giờ và kết thúc lúc mười một giờ.","Class starts at nine and finishes at eleven."),
("Lớp mình chỉ có sáu người: hai bạn Hàn, một bạn Đức, hai bạn Mỹ và mình.","My class has only six people: two Koreans, a German, two Americans and me."),
("Cô giáo rất kiên nhẫn, còn các bạn thì rất dễ thương.","The teacher is very patient, and my classmates are lovely."),
("Mình học tiếng Việt để nói chuyện với khách và với hàng xóm.","I learn Vietnamese to talk with customers and neighbours."),
("Sáng nào mình cũng thức dậy lúc bảy giờ rưỡi, tập thể dục một chút rồi đi tắm.","Every morning I get up at half past seven, exercise a bit, then shower."),
("Mình hay ăn sáng bằng một ổ bánh mì ốp la, rồi đạp xe tới lớp.","I usually have a bánh mì with fried eggs for breakfast, then cycle to class."),
("Học xong, mình ghé chợ mua rau, thịt và cá cho nhà hàng.","After class I stop by the market for greens, meat and fish for the restaurant."),
("Buổi trưa mình ăn cơm tấm sườn ở quán đầu hẻm, khoảng bốn mươi ngàn một dĩa.","At noon I eat broken rice with pork chop at the place at the top of the alley, about forty thousand a plate."),
("Buổi chiều mình đi làm. Trước khi vô bếp, mình uống một ly cà phê đen đá.","In the afternoon I go to work. Before going into the kitchen I drink an iced black coffee."),
("Mình nói chuyện với chủ quán cà phê mỗi ngày. Chú ấy sửa tiếng Việt cho mình.","I chat with the café owner every day. He corrects my Vietnamese."),
("Ở nhà mình ít nấu ăn, vì cả ngày mình đã nấu ở nhà hàng rồi.","At home I rarely cook, because I've already cooked all day at the restaurant."),
("Chủ nhật mình hay đi ăn lẩu với bạn bè.","On Sundays I often go for hot pot with friends."),
("Buổi tối, mình đọc truyện tiếng Việt và gọi điện về cho gia đình.","In the evening I read Vietnamese stories and call my family back home."),
("Mình thường đi ngủ lúc mười hai giờ đêm.","I usually go to bed at midnight.")]
NAMES={"James Baker":"Tom Walker","James":"Tom","Baker":"Walker","Bình":"Huy","Keiko":"Yuki","Kenji":"Sơn","Lan":"Thảo","Việt và":"Nam và","anh Việt":"anh Nam","Việt\"":"Nam\""}
def fix(c,c6):
    n=0
    for p in c['qa']:
        if p['id'] in A:
            a,en,k=A[p['id']]; p['a']=a; p['aEn']=en; p['key']=k; p['note']=NOTE; n+=1
        if p['id']=='c31': p['a']='Tôi tên là Huy. Rất vui được gặp anh.'
        if p['id']=='c32': p['a']='Em tên là Yuki.'
        if p['id']=='c33': p['a']='Đây là bạn Sơn.'
        if p['id']=='hoc-o-dau':
            p['a']='Tôi học tiếng Việt với một thầy giáo ở Quận 3.'; p['aEn']='I study Vietnamese with a teacher in District 3.'
            p['note']='Say where you really study: a class, a teacher, an app.'
            for s in p.get('sit',[]): s['a']='Tôi học với thầy giáo, ở Quận 3.'
        for s in p.get('sit',[]):
            for kk in ('a','q'):
                if kk in s: s[kk]=s[kk].replace('trường Nhân văn','một lớp ở Quận 3')
    st=c['lr']['story'][0]; st['t']='Leo · bài đọc'; st['items']=[{"vi":v,"en":e} for v,e in READ]
    for t in c['lr']['talk']:
        if t['t'].startswith('1.1'): t['t']='1.1 Huy và anh Tom Walker'
        if t['t'].startswith('1.2'): t['t']='1.2 Nam và Thảo đã biết nhau'; t['en']='Nam and Thảo already know each other'
        for it in t['items']:
            for kk in ('vi','en','who'):
                if kk in it:
                    v=it[kk]
                    v=v.replace('James','Tom').replace('Baker','Walker').replace('Bình','Huy').replace('Keiko','Yuki').replace('Kenji','Sơn')
                    v=v.replace('cô Lan','cô Thảo').replace('Miss Lan','Thảo').replace('anh Việt','anh Nam').replace('Hello Việt','Hello Nam')
                    if kk=='who': v={'Lan':'Thảo','Việt':'Nam'}.get(v,v)
                    it[kk]=v
    # the frame-ladder line about where Thầy Tâm teaches
    s=json.dumps(c,ensure_ascii=False)
    s=s.replace('Thầy Tâm dạy tiếng Việt ở trường đại học.','Thầy Tâm dạy tiếng Việt cho người nước ngoài.').replace('Thầy Tâm teaches Vietnamese at the university.','Thầy Tâm teaches Vietnamese to foreigners.')
    s=s.replace('David','Leo').replace('My name is Bình.','My name is Huy.').replace('My name is Keiko.','My name is Yuki.').replace('my friend Kenji','my friend Sơn')
    return json.loads(s),n
