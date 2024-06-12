document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".Button");
    const contentBox = document.getElementById("contentBox");
    const contentSections = document.querySelectorAll("#contentBox .content");

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            const contentId = this.getAttribute("data-content");
            const link = this.getAttribute("data-link");

            // 링크가 있는 경우 새 창을 열기
            if (link) {
                window.open(link, '_blank');
            } else if (contentId) {
                // 모든 content 숨기기
                contentSections.forEach(section => {
                    section.classList.add("hidden");
                });
                // 선택된 content 보이기
                const contentToShow = document.getElementById(contentId);
                if (contentToShow) {
                    contentBox.classList.remove("hidden");
                    contentToShow.classList.remove("hidden");
                }
            }
        });
    });
});