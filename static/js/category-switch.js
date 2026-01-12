/**
 * 分类切换功能 - 类似新闻App的分类栏切换效果
 * 点击分类时：1. 下划线平滑切换 2. 文章列表动态刷新
 */
(function () {
    const categoryNav = document.querySelector('.main-category-nav');
    const articleList = document.getElementById('article-list');

    if (!categoryNav || !articleList) return;

    const categoryItems = categoryNav.querySelectorAll('.category-item');
    let isLoading = false;

    // 为每个分类项添加点击事件
    categoryItems.forEach(item => {
        item.addEventListener('click', async function (e) {
            e.preventDefault();

            // 避免重复点击
            if (isLoading || this.classList.contains('active')) return;

            // 切换激活状态
            categoryItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            const categoryUrl = this.getAttribute('data-category');

            if (categoryUrl === 'all') {
                // 返回主页获取全部文章
                await loadArticles('/');
            } else {
                // 加载对应分类的文章
                await loadArticles(categoryUrl);
            }
        });
    });

    /**
     * 加载指定URL的文章列表
     */
    async function loadArticles(url) {
        isLoading = true;

        // 添加加载中的淡出效果
        articleList.style.opacity = '0.5';
        articleList.style.pointerEvents = 'none';

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('加载失败');

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // 根据页面类型提取文章列表
            let newArticles;
            const newArticleList = doc.getElementById('article-list') || doc.querySelector('.article-list');

            if (newArticleList) {
                newArticles = newArticleList.innerHTML;
            } else {
                // 分类页面可能有不同的结构
                const articles = doc.querySelectorAll('.article-list article');
                if (articles.length > 0) {
                    newArticles = Array.from(articles).map(a => a.outerHTML).join('');
                }
            }

            if (newArticles) {
                // 淡入新内容
                articleList.innerHTML = newArticles;
                articleList.style.opacity = '1';
            } else {
                // 如果没有找到文章，显示提示
                articleList.innerHTML = '<div class="no-articles" style="text-align:center;padding:40px;color:#888;">该分类暂无文章</div>';
                articleList.style.opacity = '1';
            }

            // 更新无限滚动的触发器（如果存在）
            const newTrigger = doc.getElementById('infinite-scroll-trigger');
            const currentTrigger = document.getElementById('infinite-scroll-trigger');
            if (newTrigger && currentTrigger) {
                currentTrigger.setAttribute('data-next-url', newTrigger.getAttribute('data-next-url') || '');
            }

        } catch (error) {
            console.error('加载分类文章失败:', error);
            articleList.style.opacity = '1';
        } finally {
            articleList.style.pointerEvents = '';
            isLoading = false;
        }
    }
})();
