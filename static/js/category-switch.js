/**
 * 分类切换功能 - 类似新闻App的分类栏切换效果
 * 点击分类时：1. 下划线平滑切换 2. 文章列表动态刷新
 * 支持分类内的无限滚动加载
 */
(function () {
    const categoryNav = document.querySelector('.main-category-nav');
    const articleList = document.getElementById('article-list');

    if (!categoryNav || !articleList) return;

    const categoryItems = categoryNav.querySelectorAll('.category-item');
    let isLoading = false;
    let currentCategoryUrl = '/'; // 当前分类 URL
    let nextPageUrl = null; // 下一页 URL

    // 隐藏传统分页器
    const pagination = document.querySelector('.pagination');
    if (pagination) pagination.style.display = 'none';

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
                currentCategoryUrl = '/';
            } else {
                currentCategoryUrl = categoryUrl;
            }

            // 加载第一页
            await loadArticles(currentCategoryUrl, true);
        });
    });

    // 初始化无限滚动
    initInfiniteScroll();

    /**
     * 加载指定URL的文章列表
     * @param {string} url - 要加载的 URL
     * @param {boolean} isFirstPage - 是否是第一页（切换分类时）
     */
    async function loadArticles(url, isFirstPage = false) {
        isLoading = true;

        if (isFirstPage) {
            // 切换分类时淡出效果
            articleList.style.opacity = '0.5';
            articleList.style.pointerEvents = 'none';
        }

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('加载失败');

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // 提取文章列表
            const newArticleList = doc.getElementById('article-list') || doc.querySelector('.article-list');
            const articles = newArticleList ? newArticleList.querySelectorAll('article') : doc.querySelectorAll('.article-list article');

            if (articles.length > 0) {
                const articlesHtml = Array.from(articles).map(a => a.outerHTML).join('');

                if (isFirstPage) {
                    // 第一页：替换内容
                    articleList.innerHTML = articlesHtml;
                    // 滚动到顶部
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    // 后续页：追加内容
                    articleList.insertAdjacentHTML('beforeend', articlesHtml);
                }
                articleList.style.opacity = '1';
            } else if (isFirstPage) {
                articleList.innerHTML = '<div class="no-articles" style="text-align:center;padding:40px;color:#888;">该分类暂无文章</div>';
                articleList.style.opacity = '1';
            }

            // 获取下一页 URL
            // 1. 优先从 infinite-scroll-trigger 获取（这是我们专门为 AJAX 模式准备的标识）
            const trigger = doc.getElementById('infinite-scroll-trigger');
            nextPageUrl = trigger ? trigger.getAttribute('data-next-url') : null;

            // 2. 如果没找到，再尝试从传统分页器提取
            if (!nextPageUrl) {
                const pagination = doc.querySelector('.pagination');
                if (pagination) {
                    const nextLink = pagination.querySelector('a[aria-label="next page"]') ||
                        pagination.querySelector('.page-link:last-child[href]');
                    nextPageUrl = nextLink ? nextLink.getAttribute('href') : null;
                }
            }

            // 重新应用头条标签和相对时间（调用 custom.html 中的函数）
            if (typeof applyHeadlineAndTime === 'function') {
                applyHeadlineAndTime();
            }

        } catch (error) {
            console.error('加载分类文章失败:', error);
            articleList.style.opacity = '1';
        } finally {
            articleList.style.pointerEvents = '';
            isLoading = false;
        }
    }

    /**
     * 初始化无限滚动
     */
    function initInfiniteScroll() {
        // 获取初始的下一页 URL
        const trigger = document.getElementById('infinite-scroll-trigger');
        nextPageUrl = trigger ? trigger.getAttribute('data-next-url') : null;

        // 如果没有 trigger，尝试从分页器获取一次初始 URL
        if (!nextPageUrl) {
            const pagination = document.querySelector('.pagination');
            if (pagination) {
                const nextLink = pagination.querySelector('a[aria-label="next page"]') ||
                    pagination.querySelector('.page-link:last-child[href]');
                nextPageUrl = nextLink ? nextLink.getAttribute('href') : null;
            }
        }

        // 监听滚动事件
        window.addEventListener('scroll', async function () {
            if (isLoading || !nextPageUrl) return;

            const scrollPosition = window.innerHeight + window.scrollY;
            const threshold = document.body.offsetHeight - 500;

            if (scrollPosition >= threshold) {
                await loadArticles(nextPageUrl, false);
            }
        });
    }
})();
