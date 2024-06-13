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
                    displaySortedContent();
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
    function displaySortedContent() {
        // 카테고리별로 콘텐츠를 정렬하여 표시
        const categories = {};
        const contents = contentBox.querySelectorAll('.content');
        
        contents.forEach(content => {
            const category = content.getAttribute('data-category');
            if (!categories[category]) {
                categories[category] = [];
            }
            categories[category].push(content);
        });

        // 기존 콘텐츠 삭제
        contentBox.innerHTML = '';

        // 카테고리별로 정렬된 콘텐츠를 추가
        for (const category in categories) {
            categories[category].forEach(content => {
                contentBox.appendChild(content);
            });
        }
    }

    const chatbotButton = document.getElementById('chatbot-button');
    
    if (chatbotButton) {
        chatbotButton.addEventListener('click', function() {
            window.location.href = chatbotButton.getAttribute('data-link');
        });
    }
});






