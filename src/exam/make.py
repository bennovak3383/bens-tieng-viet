# Builds data/exam.json: test practice in the same task types as the first parts of the Vietnamese proficiency test for foreigners
# (speaking: social questions by topic; listening: hear a question and pick the reply; reading: short text with questions).
# All wording here is our own. Nothing is copied from any test paper. "gate" = how many core units should be done before it is "at level".
# Usage: python3 src/exam/make.py REPO
import sys, json, unicodedata
N = lambda s: unicodedata.normalize('NFC', s)
SPEAK = [
 ('Về tôi', 'About me', 4, [
  ('Anh tên gì?', 'What is your name?', 'Tôi tên là Ben.', 'My name is Ben.'),
  ('Anh là người nước nào?', 'Which country are you from?', 'Tôi là người Mỹ.', 'I am American.'),
  ('Anh sống ở đâu?', 'Where do you live?', 'Tôi sống ở Sài Gòn.', 'I live in Saigon.'),
  ('Anh có khỏe không?', 'How are you?', 'Dạ, tôi khỏe. Cảm ơn anh.', 'I am well. Thank you.'),
  ('Anh có thích Sài Gòn không?', 'Do you like Saigon?', 'Có, tôi rất thích Sài Gòn.', 'Yes, I like Saigon very much.')]),
 ('Công việc', 'Your work now', 10, [
  ('Bây giờ anh làm công việc gì?', 'What work do you do now?', 'Tôi làm chủ một phòng tập ở Mỹ.', 'I own a gym in the US.'),
  ('Anh làm việc ở đâu?', 'Where do you work?', 'Tôi làm việc ở nhà và ở quán cà phê.', 'I work at home and in cafés.'),
  ('Anh làm việc từ mấy giờ đến mấy giờ?', 'From what time to what time do you work?', 'Tôi làm việc từ tám giờ sáng đến năm giờ chiều.', 'I work from eight in the morning to five in the afternoon.'),
  ('Anh có thích công việc của anh không? Vì sao?', 'Do you like your work? Why?', 'Có, tôi rất thích, vì tôi được gặp nhiều người.', 'Yes, I like it a lot, because I get to meet many people.'),
  ('Anh có thường đi công tác không?', 'Do you often travel for work?', 'Đôi khi. Mỗi năm tôi về Mỹ vài lần.', 'Sometimes. I go back to the US a few times a year.')]),
 ('Đến Việt Nam', 'Coming to Vietnam', 11, [
  ('Anh đến Việt Nam khi nào?', 'When did you come to Vietnam?', 'Tôi đến Việt Nam hai năm trước.', 'I came to Vietnam two years ago.'),
  ('Anh sống ở Việt Nam bao lâu rồi?', 'How long have you lived in Vietnam?', 'Tôi sống ở đây khoảng hai năm rồi.', 'I have lived here about two years.'),
  ('Ở Việt Nam, anh sống với ai?', 'Who do you live with in Vietnam?', 'Tôi sống một mình.', 'I live alone.'),
  ('Anh đến Việt Nam để làm gì?', 'What did you come to Vietnam for?', 'Tôi đến đây để sống và làm việc.', 'I came here to live and work.'),
  ('Anh sẽ ở Việt Nam bao lâu nữa?', 'How much longer will you stay in Vietnam?', 'Tôi chưa biết. Có lẽ vài năm nữa.', 'I do not know yet. Maybe a few more years.')]),
 ('Tiếng Việt', 'How you feel about Vietnamese', 20, [
  ('Anh có thích học tiếng Việt không? Vì sao?', 'Do you like learning Vietnamese? Why?', 'Có. Tôi thích vì tôi muốn nói chuyện với mọi người ở đây.', 'Yes. I like it because I want to talk with everyone here.'),
  ('Anh học tiếng Việt bao lâu rồi?', 'How long have you been learning Vietnamese?', 'Tôi học khoảng một năm rồi.', 'I have been learning for about a year.'),
  ('Anh học tiếng Việt ở đâu?', 'Where do you study Vietnamese?', 'Tôi học với thầy và tự học ở nhà.', 'I study with a teacher and by myself at home.'),
  ('Anh thấy tiếng Việt thế nào so với tiếng Anh?', 'How do you find Vietnamese compared with English?', 'Tôi thấy tiếng Việt khó hơn tiếng Anh, đặc biệt là phần nghe.', 'I find Vietnamese harder than English, especially the listening.'),
  ('Theo anh, tiếng Việt khó nhất ở điểm nào?', 'In your view, what is the hardest point of Vietnamese?', 'Theo tôi, khó nhất là sáu thanh.', 'In my view, the hardest is the six tones.')]),
 ('Một ngày của tôi', 'Your daily routine', 25, [
  ('Buổi sáng anh thường dậy lúc mấy giờ?', 'What time do you usually get up in the morning?', 'Tôi thường dậy lúc sáu giờ.', 'I usually get up at six.'),
  ('Sau khi dậy, anh thường làm gì?', 'What do you usually do after getting up?', 'Tôi uống cà phê rồi đi tập.', 'I drink coffee and then go and work out.'),
  ('Buổi chiều anh thường làm gì?', 'What do you usually do in the afternoon?', 'Buổi chiều tôi học tiếng Việt.', 'In the afternoon I study Vietnamese.'),
  ('Buổi tối anh thường đi ngủ lúc mấy giờ?', 'What time do you usually go to bed?', 'Tôi thường đi ngủ lúc mười giờ rưỡi.', 'I usually go to bed at half past ten.'),
  ('Trước khi đi ngủ, anh thường làm gì?', 'What do you usually do before going to bed?', 'Tôi đọc sách một chút.', 'I read a little.')]),
 ('Gia đình', 'Your family', 30, [
  ('Gia đình anh có mấy người?', 'How many people are in your family?', 'Gia đình tôi có bốn người: cha, mẹ, anh tôi và tôi.', 'There are four people in my family: father, mother, my older brother and me.'),
  ('Cha mẹ anh là người nước nào?', 'Which country are your parents from?', 'Cha mẹ tôi đều là người Mỹ.', 'My parents are both American.'),
  ('Bây giờ cha mẹ anh sống ở đâu?', 'Where do your parents live now?', 'Cha mẹ tôi sống ở Mỹ.', 'My parents live in the US.'),
  ('Năm nay mẹ anh bao nhiêu tuổi?', 'How old is your mother this year?', 'Năm nay mẹ tôi bảy mươi tuổi.', 'My mother is seventy this year.'),
  ('Trong gia đình, anh thường nói chuyện với ai? Vì sao?', 'Who do you usually talk to in your family? Why?', 'Tôi thường nói chuyện với mẹ, vì mẹ rất hiểu tôi.', 'I usually talk to my mother, because she understands me very well.')]),
 ('Đất nước của tôi', 'Your country', 35, [
  ('Nước anh ở khu vực nào?', 'Which part of the world is your country in?', 'Nước tôi ở Bắc Mỹ.', 'My country is in North America.'),
  ('Thời tiết ở nước anh thế nào?', 'What is the weather like in your country?', 'Ở chỗ tôi, mùa hè rất nóng, còn mùa đông thì mát.', 'Where I am from, summer is very hot, while winter is cool.'),
  ('Người ở nước anh thế nào?', 'What are the people in your country like?', 'Theo tôi, họ vui vẻ và thích nói chuyện.', 'In my view, they are cheerful and like to talk.'),
  ('Từ nước anh đến Việt Nam bằng máy bay mất bao lâu?', 'How long does it take to fly from your country to Vietnam?', 'Mất khoảng hai mươi giờ.', 'It takes about twenty hours.'),
  ('Ở nước anh, thành phố nào nổi tiếng nhất?', 'Which city is the most famous in your country?', 'Theo tôi, New York là thành phố nổi tiếng nhất.', 'In my view, New York is the most famous city.')]),
 ('Một nước tôi thích', 'A country you like', 40, [
  ('Anh đã từng sống ở những nước nào?', 'Which countries have you lived in?', 'Tôi từng sống ở Mỹ và Việt Nam.', 'I have lived in the US and Vietnam.'),
  ('Anh thích nước nào nhất? Vì sao?', 'Which country do you like most? Why?', 'Tôi thích Việt Nam nhất, vì đồ ăn ngon và con người dễ thương.', 'I like Vietnam most, because the food is good and the people are lovely.'),
  ('Anh muốn đi nước nào nữa?', 'Which other country do you want to go to?', 'Tôi muốn đi Nhật, vì tôi chưa bao giờ tới đó.', 'I want to go to Japan, because I have never been there.')]),
 ('Tả một người thân', 'Describe someone in your family', 42, [
  ('Mẹ anh trông thế nào?', 'What does your mother look like?', 'Mẹ tôi không cao lắm, tóc ngắn, trông trẻ hơn tuổi.', 'My mother is not very tall, has short hair and looks younger than her age.'),
  ('Tính mẹ anh thế nào?', 'What is your mother like as a person?', 'Mẹ tôi vui tính và rất thương mọi người.', 'My mother is good-humoured and cares about everyone.'),
  ('Anh giống ai trong gia đình?', 'Who do you take after in your family?', 'Tôi giống cha: cao và ít nói.', 'I take after my father: tall and quiet.')]),
]
READ = [
 ('Nhà tôi', 'My home', 8, ['Tôi tên là Minh.', 'Tôi sống ở Quận Bốn, Sài Gòn.', 'Nhà tôi nhỏ nhưng rất đẹp.', 'Nhà tôi ở gần một quán cà phê.', 'Tôi sống với một người bạn.', 'Bạn tôi là người Mỹ.', 'Anh ấy đang học tiếng Việt.'], [
  ('Minh sống ở đâu?', ['Ở Quận Bốn', 'Ở Mỹ', 'Ở Huế'], 0), ('Nhà Minh thế nào?', ['Lớn và đẹp', 'Nhỏ nhưng đẹp', 'Nhỏ và xa'], 1),
  ('Minh sống với ai?', ['Một mình', 'Với gia đình', 'Với một người bạn'], 2), ('Bạn của Minh đang làm gì?', ['Học tiếng Việt', 'Học tiếng Anh', 'Làm việc ở quán cà phê'], 0)]),
 ('Một ngày của chị Lan', "Lan's day", 12, ['Hôm nay chị Lan rất bận.', 'Chị ấy dậy sớm vì phải đi làm.', 'Chị ấy chưa ăn sáng, chỉ uống một ly cà phê.', 'Chị ấy định về nhà sớm, nhưng công việc chưa xong.', 'Mai chị ấy được nghỉ, nên chị ấy sẽ đi chơi với bạn.'], [
  ('Tại sao chị Lan dậy sớm?', ['Vì phải đi làm', 'Vì đói', 'Vì muốn đi chơi'], 0), ('Chị Lan ăn sáng chưa?', ['Rồi', 'Chưa, chỉ uống cà phê', 'Chưa, và cũng không uống gì'], 1),
  ('Tại sao chị Lan chưa về nhà?', ['Vì trời mưa', 'Vì đợi bạn', 'Vì công việc chưa xong'], 2), ('Mai chị Lan làm gì?', ['Đi làm', 'Đi chơi với bạn', 'Ở nhà ngủ'], 1)]),
 ('Tại sao tôi học tiếng Việt', 'Why I am learning Vietnamese', 16, ['Tôi là người nước ngoài và tôi sống ở Sài Gòn hơn một năm rồi.', 'Lúc mới tới, tôi không nói được tiếng Việt, nên đi đâu cũng khó.', 'Vì vậy tôi quyết định học.', 'Mỗi tuần tôi gặp thầy hai lần.', 'Tiếng Việt khó, nhưng tôi rất thích.', 'Bây giờ tôi có thể nói chuyện một chút với mọi người ở gần nhà.', 'Nếu cố gắng, tôi nghĩ năm sau tôi sẽ nói giỏi hơn.'], [
  ('Người viết sống ở Sài Gòn bao lâu rồi?', ['Hơn một năm', 'Hai năm', 'Một tháng'], 0), ('Tại sao người viết quyết định học tiếng Việt?', ['Vì thích thầy', 'Vì không nói được nên đi đâu cũng khó', 'Vì bạn bè đều học'], 1),
  ('Mỗi tuần người viết gặp thầy mấy lần?', ['Một lần', 'Hai lần', 'Ba lần'], 1), ('Bây giờ người viết có thể làm gì?', ['Nói chuyện một chút với mọi người gần nhà', 'Đọc sách tiếng Việt', 'Dạy tiếng Việt'], 0)]),
 ('Cuối tuần', 'The weekend', 26, ['Cuối tuần tôi thường dậy trễ hơn.', 'Buổi sáng tôi đi uống cà phê với bạn ở một quán gần nhà.', 'Sau đó tôi đi tập khoảng một giờ.', 'Buổi chiều, nếu trời không mưa, tôi chạy xe ra ngoài thành phố.', 'Mặc dù hay bị kẹt xe nhưng tôi vẫn thích đi.', 'Buổi tối tôi ăn cơm ở nhà rồi coi phim.', 'Tối Chủ nhật tôi thường gọi điện thoại cho gia đình ở Mỹ.'], [
  ('Sáng cuối tuần, người viết làm gì trước?', ['Đi tập', 'Đi uống cà phê với bạn', 'Coi phim'], 1), ('Người viết tập bao lâu?', ['Nửa giờ', 'Khoảng một giờ', 'Hai giờ'], 1),
  ('Khi nào người viết chạy xe ra ngoài thành phố?', ['Buổi chiều, nếu trời không mưa', 'Buổi sáng', 'Buổi tối'], 0), ('Tối Chủ nhật người viết thường làm gì?', ['Đi làm', 'Đi Mỹ', 'Gọi điện thoại cho gia đình'], 2)]),
 ('Gia đình tôi', 'My family', 31, ['Gia đình tôi có bốn người: cha, mẹ, chị tôi và tôi.', 'Cha mẹ tôi sống ở quê, còn chị tôi thì sống ở nước ngoài.', 'Cha tôi ít nói nhưng rất thương con.', 'Mẹ tôi thì vui tính, ai cũng thích nói chuyện với mẹ.', 'Tụi tôi ít khi gặp nhau, vì vậy mỗi tuần tôi đều gọi về nhà.', 'Năm sau cả gia đình sẽ gặp nhau ở Sài Gòn.'], [
  ('Gia đình người viết có mấy người?', ['Ba người', 'Bốn người', 'Năm người'], 1), ('Chị của người viết sống ở đâu?', ['Ở quê', 'Ở Sài Gòn', 'Ở nước ngoài'], 2),
  ('Mẹ của người viết là người thế nào?', ['Vui tính', 'Ít nói', 'Hay giận'], 0), ('Tại sao mỗi tuần người viết đều gọi về nhà?', ['Vì mẹ yêu cầu', 'Vì họ ít khi gặp nhau', 'Vì cha bị bệnh'], 1)]),
 ('Quán cà phê gần nhà', 'The café near my place', 43, ['Gần nhà tôi có một quán cà phê nhỏ.', 'Quán trông không hiện đại, nhưng lúc nào cũng có khách.', 'Trên tường có nhiều tranh, trước cửa có một cây lớn.', 'Chủ quán là một chú khoảng sáu mươi tuổi, rất vui tính.', 'Sáng nào tôi cũng ghé uống một ly cà phê đen rồi mới đi làm.', 'Nhờ chú ấy mà tôi biết thêm nhiều câu tiếng Việt.', 'Tôi vừa uống cà phê vừa tập nói chuyện với mọi người.'], [
  ('Quán cà phê trông thế nào?', ['Rất hiện đại', 'Không hiện đại nhưng luôn có khách', 'Lớn và ít khách'], 1), ('Trước cửa quán có gì?', ['Nhiều tranh', 'Một cây lớn', 'Một chiếc xe'], 1),
  ('Chủ quán là ai?', ['Một chú khoảng sáu mươi tuổi', 'Một chị còn trẻ', 'Bạn của người viết'], 0), ('Người viết ghé quán khi nào?', ['Buổi tối, sau khi làm việc', 'Cuối tuần', 'Mỗi sáng, trước khi đi làm'], 2)]),
]
out = {'v': 1, 'speak': [{'vi': N(a), 'en': b, 'gate': g, 'q': [[N(x[0]), x[1], N(x[2]), x[3]] for x in q]} for a, b, g, q in SPEAK],
       'read': [{'vi': N(a), 'en': b, 'gate': g, 'text': [N(x) for x in t], 'q': [[N(x[0]), [N(o) for o in x[1]], x[2]] for x in q]} for a, b, g, t, q in READ]}
json.dump(out, open(sys.argv[1] + '/data/exam.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('speaking topics', len(SPEAK), 'questions', sum(len(x[3]) for x in SPEAK), '| reading texts', len(READ), 'questions', sum(len(x[4]) for x in READ))
