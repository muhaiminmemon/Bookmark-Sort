document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('sort').addEventListener('click', function () {
        chrome.runtime.sendMessage({ action: 'sortBookmarks' }, function (response) {
            if (response.status === 'Sorting initiated') {
                // Show a message in the popup
                const messageElement = document.createElement('p');
                messageElement.textContent = 'Bookmarks have been sorted.';
                document.getElementById('content').appendChild(messageElement);
            }
        });
    });
});




function refreshBookmarks() {
    chrome.bookmarks.getTree(function(bookmarkTreeNodes) {
        displayBookmarks(bookmarkTreeNodes);
    });
}

function displayBookmarks(bookmarkNodes) {
    const bookmarkList = document.getElementById('bookmarkList');
    bookmarkList.innerHTML = '';
    bookmarkNodes.forEach(node => {
        displayBookmarkNode(node, bookmarkList);
    });
}

function displayBookmarkNode(node, parentElement) {
    if (node.children) {
        const folder = document.createElement('li');
        folder.textContent = node.title;
        parentElement.appendChild(folder);

        const subList = document.createElement('ul');
        parentElement.appendChild(subList);

        node.children.forEach(childNode => {
            displayBookmarkNode(childNode, subList);
        });
    } else {
        const bookmark = document.createElement('li');
        bookmark.textContent = node.title;
        parentElement.appendChild(bookmark);
    }
}

function sortBookmarks() {
    chrome.runtime.sendMessage({ action: 'sortBookmarks' }, function(response) {
        console.log(response);
        refreshBookmarks();
    });
}
