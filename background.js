chrome.runtime.onInstalled.addListener(() => {
    const categories = [
        "Education / E-Learning",
        "Lifestyle",
        "Movies & TV Shows",
        "Career & Job Searching"
    ];

    // Create folders if they don't exist
    chrome.bookmarks.getTree((bookmarkTreeNodes) => {
        const bookmarkBar = bookmarkTreeNodes[0].children.find(child => child.title === 'Bookmarks Bar' || child.id === '1');
        if (!bookmarkBar) {
            console.error('Bookmark Bar not found.');
            return;
        }
        console.log('Bookmark Bar:', bookmarkBar);

        const existingFolders = new Set(bookmarkBar.children.map(folder => folder.title));

        categories.forEach(category => {
            if (!existingFolders.has(category)) {
                chrome.bookmarks.create({ parentId: bookmarkBar.id, title: category });
            }
        });
    });

    // Show a welcome notification
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: 'Welcome to AI Bookmark Manager',
        message: 'Your bookmarks will be categorized into the following folders: Education / E-Learning, Lifestyle, Movies & TV Shows, Career & Job Searching.'
    });

    console.log("AI Bookmark Manager installed.");

    // Add a button to the context menu for sorting bookmarks
    chrome.contextMenus.create({
        id: "sortBookmarks",
        title: "Sort Bookmarks",
        contexts: ["all"]
    });
});

// Listener for context menu item click
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "sortBookmarks") {
        sortAllBookmarks();
        // Show notification after sorting
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon128.png',
            title: 'AI Bookmark Manager',
            message: 'Bookmarks have been sorted.'
        });
    }
});

chrome.bookmarks.onCreated.addListener((id, bookmark) => {
    console.log("Bookmark created:", bookmark);
    categorizeBookmark(bookmark);
});

chrome.bookmarks.onChanged.addListener((id, changeInfo) => {
    chrome.bookmarks.get(id, (bookmarkArray) => {
        const bookmark = bookmarkArray[0];
        console.log("Bookmark changed:", bookmark);
        categorizeBookmark(bookmark);
    });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'sortBookmarks') {
        sortAllBookmarks();
        sendResponse({ status: 'Sorting initiated' });
    }
});

function categorizeBookmark(bookmark) {
    fetch('https://bookmarksort.azurewebsites.net/categorize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: bookmark.title, url: bookmark.url })
    })
    .then(response => response.json())
    .then(data => {
        const category = data.category;
        console.log(`Bookmark categorized as: ${category}`);
        moveBookmarkToCategoryFolder(bookmark, category);
    })
    .catch(error => console.error('Error:', error));
}

function moveBookmarkToCategoryFolder(bookmark, category) {
    chrome.bookmarks.search({}, (results) => {
        let folderFound = false;
        results.forEach((result) => {
            if (result.title === category && !result.url) {
                folderFound = true;
                chrome.bookmarks.move(bookmark.id, { parentId: result.id }, () => {
                    console.log(`Moved bookmark to existing folder: ${category}`);
                });
            }
        });
        if (!folderFound) {
            chrome.bookmarks.getTree((bookmarkTreeNodes) => {
                const bookmarkBar = bookmarkTreeNodes[0].children.find(child => child.title === 'Bookmarks Bar' || child.id === '1');
                if (!bookmarkBar) {
                    console.error('Bookmark Bar not found.');
                    return;
                }
                console.log('Bookmark Bar:', bookmarkBar);
                chrome.bookmarks.create({ parentId: bookmarkBar.id, title: category }, (newFolder) => {
                    chrome.bookmarks.move(bookmark.id, { parentId: newFolder.id }, () => {
                        console.log(`Created new folder and moved bookmark to: ${category}`);
                    });
                });
            });
        }
    });
}

function sortAllBookmarks() {
    chrome.bookmarks.getTree((bookmarkTreeNodes) => {
        const bookmarkBar = bookmarkTreeNodes[0].children.find(child => child.title === 'Bookmarks Bar' || child.id === '1');
        if (!bookmarkBar) {
            console.error('Bookmark Bar not found.');
            return;
        }
        traverseBookmarks(bookmarkBar);
    });
}

function traverseBookmarks(node) {
    if (node.children) {
        node.children.forEach((childNode) => {
            traverseBookmarks(childNode);
        });
    } else {
        categorizeBookmark(node);
    }
}
