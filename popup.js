document.addEventListener('DOMContentLoaded', () => {
    const sortButton = document.getElementById('sort');

    sortButton.addEventListener('click', () => {
        chrome.runtime.sendMessage({ action: 'sortBookmarks' }, (response) => {
            console.log(response.status);
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
