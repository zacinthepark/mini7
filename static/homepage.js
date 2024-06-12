document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".Button");
    const contents = document.querySelectorAll(".content");

    // 각 버튼에 클릭 이벤트를 추가합니다.
    buttons.forEach(button => {
        button.addEventListener("click", function() {
            const category = this.getAttribute("data-content");
            
            // 버튼이 '전체'일 경우 모든 컨텐츠를 표시합니다.
            if (category === 'all') {
                contents.forEach(content => {
                    content.style.display = "block";
                });
            } else {
                // 그 외 버튼일 경우 해당 카테고리의 컨텐츠만 표시합니다.
                contents.forEach(content => {
                    const contentCategory = content.getAttribute("data-category");
                    if (contentCategory === category) {
                        content.style.display = "block";
                    } else {
                        content.style.display = "none";
                    }
                });
            }
        });
    });

    const chatbotButton = document.getElementById('chatbot-button');
    if (chatbotButton) {
        chatbotButton.addEventListener('click', function() {
            const chatbotURL = this.getAttribute('data-link');
            window.open(chatbotURL, '_blank');
        });
    }
});





