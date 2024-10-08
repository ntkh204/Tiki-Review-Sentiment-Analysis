def processing_text(df):
    #Import các thư viện cần thiết
    import pandas as pd
    import unicodedata
    from underthesea import text_normalize, word_tokenize
    import regex as re
    import emot
    
    #Đọc file
    #1. Đọc file teencode
    with open('files/teencode.txt', 'r', encoding='utf8') as file:
        teencode_list = file.read().split('\n')
        teencode_dict = {}
        for line in teencode_list:
            key, value = line.split('\t')
            teencode_dict[key] = str(value)
    file.close()
    
    #2. Đọc file cá từ bị sai
    with open('files/wrong-word.txt', 'r', encoding='utf8') as file:
        wrongword_list = file.read().split('\n')
    file.close()
    
    #3. Đọc file các từ stopword trong  tiếng việt
    with open('files/vietnamese-stopwords.txt', 'r', encoding='utf8') as file:
        stopword_list = file.read().split('\n')
    file.close()
    
    #Xóa emoji và emoticon
    emot_obj = emot.core.emot()
    def xoa_emoji_va_emoticon(text):
        emojis = emot_obj.emoji(text)
        emoticons = emot_obj.emoticons(text)
        for i in emojis['value'] + emoticons['value']:
            for punc in ['(', ')', '.', '+', '*']:
                i = i.replace(punc, '\\' + punc)
            pattern = r'\s' + i + r'\s'
            text = re.sub(pattern, ' ', text)
        return text
    df['clean_content'] = df['content'].apply(lambda x: xoa_emoji_va_emoticon(x))
    
    #Chuyển teencode thành từ đúng
    def chuyen_teencode(text):
        text = ' '.join(teencode_dict[word] if word in teencode_dict else word for word in text.split())
        return text
    df['clean_content'] = df['clean_content'].apply(lambda x: chuyen_teencode(x))
    
    #Xóa các từ bị sai
    def xoa_wrongword(text):
        text = ' '.join('' if word in wrongword_list else word for word in text.split())
        return text
    df['clean_content'] = df['clean_content'].apply(lambda x: xoa_wrongword(x))
    
    #Chuẩn hóa dấu câu và loại bỏ các thành phần không cần thiết
    def xoa_dau_cau_va_so(text):
            pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
            text = ' '.join(re.findall(pattern, text))
            text = text.lower()
            text = re.sub(r'\s+', ' ', text).strip()  
            return text
    df['clean_content'] = df['clean_content'].apply(lambda x: xoa_dau_cau_va_so(x))

    #Chuẩn hóa unicode tiếng việt (cre: nguyenvanhieuvn)
    def loaddicchar():
        # uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
        # unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"
        dic = {}
        char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split('|')
        charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split('|')
        for i in range(len(char1252)):
            dic[char1252[i]] = charutf8[i]
        return dic
         
    def chuyen_unicode(text):
        dicchar = loaddicchar()
        return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|\
        À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], text)
    df['clean_content'] = df['clean_content'].apply(lambda x: chuyen_unicode(x))
        
    #Chuẩn hóa dấu câu trong tiếng việt
    def chuan_hoa_dau_tieng_viet(text):
        text = text_normalize(text)
        return text
    df['clean_content'] = df['clean_content'].apply(lambda x: chuan_hoa_dau_tieng_viet(x))
    
    #Tách từ tiếng việt
    def tach_tu_tieng_viet(text):
        text = word_tokenize(text, format="text")
        return text
    
    #Xóa stopword
    def xoa_stopword(text):
        text = ' '.join('' if word in stopword_list else word for word in text.split())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    df['clean_content'] = df['clean_content'].apply(lambda x: xoa_stopword(x))
    
    return df