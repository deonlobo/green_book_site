document.addEventListener('DOMContentLoaded', function() {
    const tagInput = document.getElementById('tag-input');
    const tagList = document.getElementById('tag-list');
    const searchInput = document.getElementById('tag-search');
    const searchResults = document.getElementById('search-results');

    let tags = new Set();

    function updateTagList() {
        tagList.innerHTML = '';
        tags.forEach(tag => {
            const tagElem = document.createElement('div');
            tagElem.className = 'tag-item';
            tagElem.textContent = tag;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'x';
            removeButton.className = 'remove-tag';
            removeButton.onclick = () => {
                tags.delete(tag);
                updateTagList();
            };
            tagElem.appendChild(removeButton);
            tagList.appendChild(tagElem);
        });

        tagInput.value = Array.from(tags).join(',');
    }

    function updateSearchResults(fetchedTags) {
        if(fetchedTags.length > 0){
            searchResults.innerHTML = '';
            searchResults.classList.add('with-border');
            fetchedTags.forEach(tag => {
                const tagElem = document.createElement('div');
                tagElem.className = 'search-result-item';
                tagElem.textContent = tag.name;
                tagElem.onclick = () => {
                    tags.add(tag.name);
                    updateTagList();
                    searchInput.value = '';
                    searchResults.innerHTML = '';
                };
                searchResults.appendChild(tagElem);
            });
        }else{
            searchResults.classList.remove('with-border');
        }

    }

    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        if (query) {
            fetch(`${searchTagsUrl}?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    updateSearchResults(data.tags);
                });
        } else {
            searchResults.innerHTML = '';
            searchResults.classList.remove('with-border');
        }
    });

    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            searchResults.innerHTML = '';
            searchResults.classList.remove('with-border');
        }
    });

    searchInput.addEventListener('keydown', function(e) {
        if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            const tag = searchInput.value.trim();
            if (tag && !tags.has(tag)) {
                tags.add(tag);
                updateTagList();
                searchInput.value = '';
                searchResults.innerHTML = '';
                searchResults.classList.remove('with-border');
            }
        }
    });
});
