def valid_password(password='',level='ful'):
    v1='1234567890'
    v2='QWERTYUIOPASDFGHJKLZXCVBNM'
    v3='!@#$%^&*()_+= -{[}]|\?><.,;:\'\"'
    if len(password)<8:
        return "Пароль повинен мати не менше 8 символiв"
    if len(password)>100:
        return "Пароль занадто довгий"
    if level=='light':
        return None
    f1=True
    for i in v1:
        if i in password:
            f1=False
    if f1:
        return 'В пароле должна быть хоть одна цифра'
    if level=='numeric':
        return None
    f1=True
    for i in v2:
        if i in password:
            f1=False
    if f1:
        return 'В пароле должна быть хоть одна заглавная буква'
    if level=='hig_case':
        return None
    f1=True
    for i in v3:
        if i in password:
            f1=False
    if f1:
        return 'В пароле должна быть хоть один спец символ'
    return None #levl ful
def valid_mail(mail=''):
    if (('@' in mail)and('.' in mail)):
        return True
    return False        
def valid_phone(phone=''):
    #+380678326281
    if not((len(phone)==10) or (len(phone)==13)):
        return False
    elif ((len(phone)==13)and(phone[0]!='+')):
        return False
    return True
            
        
        
if __name__=='__main__': 
    print(valid_passwordsword('ieurytei',level='ligt'))
