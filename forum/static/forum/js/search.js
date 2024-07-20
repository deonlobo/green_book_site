document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('question-search');
    const searchResults = document.getElementById('search-results');
    let debounceTimeout;

    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();

        if (debounceTimeout) {
            clearTimeout(debounceTimeout);
        }

        debounceTimeout = setTimeout(() => {
            if (query.length > 0) {
                fetch(`${searchUrl}?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        displaySearchResults(data.questions);
                    });
            } else {
                clearSearchResults();
            }
        }, 300); // Adjust the delay as needed (300ms in this case)
    });

    function displaySearchResults(questions) {
        clearSearchResults();

        if (questions.length > 0) {
            searchResults.classList.add('with-border');
            questions.forEach(question => {
                const resultItem = document.createElement('div');
                resultItem.className = 'search-result-item';
                resultItem.innerHTML = `
                    <a href="/forum/questions/${question.id}/${question.question_id}">${question.title}</a>
                `;
                searchResults.appendChild(resultItem);
            });
        } else {
            searchResults.classList.add('with-border');
            const noResultsItem = document.createElement('div');
            noResultsItem.className = 'search-result-item';
            noResultsItem.textContent = 'No results found';
            searchResults.appendChild(noResultsItem);
        }
    }

    function clearSearchResults() {
        searchResults.innerHTML = '';
        searchResults.classList.remove('with-border');
    }

    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            searchResults.innerHTML = '';
            searchResults.classList.remove('with-border');
        }
    });

     searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            window.location.href = `/forum?search=${encodeURIComponent(searchInput.value.trim())}`;
        }
    });
});
