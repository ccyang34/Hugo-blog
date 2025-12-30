(function () {
    const trigger = document.getElementById('infinite-scroll-trigger');
    const container = document.querySelector('.taxonomy-grid') || document.querySelector('.article-list');

    if (!trigger || !container) return;

    let isLoading = false;
    let nextUrl = trigger.getAttribute('data-next-url');

    // 初始状态下隐藏传统分页器以防闪烁
    const pagination = document.querySelector('.pagination');
    if (pagination) pagination.style.display = 'none';

    if (!nextUrl) {
        trigger.style.display = 'none';
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !isLoading && nextUrl) {
                loadMore();
            }
        });
    }, {
        rootMargin: '200px' // 提前200px开始加载
    });

    observer.observe(trigger);

    async function loadMore() {
        isLoading = true;
        console.log('Loading next page:', nextUrl);

        try {
            const response = await fetch(nextUrl);
            const html = await response.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // 提取新内容 (支持分类方块和文章列表两种模式)
            const newItems = doc.querySelectorAll('.taxonomy-item, .article-list article');

            if (newItems.length > 0) {
                newItems.forEach(item => {
                    container.appendChild(item);
                });

                // 更新下一页链接
                const nextTrigger = doc.getElementById('infinite-scroll-trigger');
                nextUrl = nextTrigger ? nextTrigger.getAttribute('data-next-url') : null;

                if (!nextUrl) {
                    observer.unobserve(trigger);
                    trigger.style.display = 'none';
                }
            } else {
                nextUrl = null;
                observer.unobserve(trigger);
                trigger.style.display = 'none';
            }
        } catch (error) {
            console.error('Failed to load more items:', error);
        } finally {
            isLoading = false;
        }
    }
})();
