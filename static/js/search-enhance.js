/* 搜索增强 - 即时下拉建议 */
(function () {
    // 等待原始搜索初始化完成后增强
    const originalFetch = window.fetch;
    let searchIndex = null;
    let fuse = null;

    // 拦截 index.json 加载
    window.fetch = function (...args) {
        return originalFetch.apply(this, args).then(response => {
            if (args[0] && args[0].toString().includes('index.json')) {
                return response.clone().json().then(data => {
                    searchIndex = data;
                    initEnhancedSearch(data);
                    return response;
                });
            }
            return response;
        });
    };

    function initEnhancedSearch(index) {
        // 使用更宽松的搜索选项
        const options = {
            ignoreLocation: true,
            findAllMatches: true,
            includeScore: true,
            shouldSort: true,
            keys: ['title', 'body', 'tags'],
            threshold: 0.4  // 放宽阈值，0.0=精确匹配, 1.0=匹配所有
        };

        if (typeof Fuse !== 'undefined') {
            fuse = new Fuse(index, options);
        }

        const searchField = document.querySelector('.search_field');
        const searchResults = document.querySelector('.search_results');

        if (searchField && searchResults) {
            // 移除原有事件，添加增强版搜索
            const newSearchField = searchField.cloneNode(true);
            searchField.parentNode.replaceChild(newSearchField, searchField);

            newSearchField.addEventListener('input', function (e) {
                const query = e.target.value.trim();

                if (query.length < 1) {
                    searchResults.innerHTML = '';
                    return;
                }

                if (fuse) {
                    const results = fuse.search(query).slice(0, 8);
                    displayResults(results, query, searchResults);
                }
            });

            // 聚焦时如果有内容就显示结果
            newSearchField.addEventListener('focus', function (e) {
                const query = e.target.value.trim();
                if (query.length >= 1 && fuse) {
                    const results = fuse.search(query).slice(0, 8);
                    displayResults(results, query, searchResults);
                }
            });
        }
    }

    function displayResults(results, query, container) {
        if (!results.length) {
            container.innerHTML = '<span class="search_result">未找到匹配结果</span>';
            return;
        }

        let html = '<h3 class="search_title">快速链接</h3>';
        results.forEach(r => {
            const item = r.item;
            html += `<a href="${item.link}?query=${encodeURIComponent(query)}" class="search_result">${item.title}</a>`;
        });
        container.innerHTML = html;
    }
})();
