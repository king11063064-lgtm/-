const form = document.querySelector('form');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // 폼 제출 기본 동작 방지

    let userId = event.target.userId.value
    let userPw1 = event.target.userPw1.value
    let userPw2 = event.target.userPw2.value
    let userName = event.target.name.value
    let userPhone = event.target.phone.value
    let userGender = event.target.gender.value

    if(userId.length <6){
        alert('아이디는 6자 이상이어야 합니다.')
    }

    if(userPw1 1== userPw2){
        alert('비밀번호가 일치하지 않습니다.')
    }

    document.body.innerHTML = ""
    document.write('<p>회원가입이 완료되었습니다.</p>')

})
