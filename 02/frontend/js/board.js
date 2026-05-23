const API_BASE_URL = "http://127.0.0.1:8000";

const username = localStorage.getItem("username");

if (!username) {
    window.location.href = "./login.html";
}

document.getElementById("currentUser").textContent = username;

const postForm = document.getElementById("postForm");
const submitButton = document.getElementById("submitButton");
const formMessage = document.getElementById("formMessage");
const listMessage = document.getElementById("listMessage");
const postList = document.getElementById("postList");
const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", () => {
    localStorage.removeItem("username");
    window.location.href = "./login.html";
});

postForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    clearMessage(formMessage);

    if (!title || !content) {
        showMessage(formMessage, "제목과 내용을 입력하세요.", "error");
        return;
    }

    try {
        submitButton.disabled = true;
        submitButton.textContent = "등록 중...";

        const response = await fetch(`${API_BASE_URL}/posts`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title,
                content,
                author: username,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage(formMessage, data.detail || "글 등록에 실패했습니다.", "error");
            return;
        }

        postForm.reset();
        showMessage(formMessage, "글이 등록되었습니다.", "success");
        await loadPosts();
    } catch (error) {
        showMessage(formMessage, "서버와 연결할 수 없습니다.", "error");
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "등록";
    }
});

async function loadPosts() {
    clearMessage(listMessage);
    postList.replaceChildren();

    try {
        const response = await fetch(`${API_BASE_URL}/posts`);
        const posts = await response.json();

        if (!response.ok) {
            showMessage(listMessage, "게시글을 불러오지 못했습니다.", "error");
            return;
        }

        if (!posts.length) {
            showMessage(listMessage, "등록된 게시글이 없습니다.", "info");
            return;
        }

        posts
            .slice()
            .reverse()
            .forEach((post) => {
                postList.appendChild(createPostItem(post));
            });
    } catch (error) {
        showMessage(listMessage, "서버와 연결할 수 없습니다.", "error");
    }
}

function createPostItem(post) {
    const item = document.createElement("li");
    item.className = "post-item";

    const title = document.createElement("h3");
    title.textContent = post.title;

    const meta = document.createElement("p");
    meta.className = "post-meta";
    meta.textContent = `작성자: ${post.author} · #${post.id}`;

    const body = document.createElement("p");
    body.className = "post-content";
    body.textContent = post.content;

    item.append(title, meta, body);
    return item;
}

function showMessage(element, text, type) {
    element.textContent = text;
    element.className = `message ${type}`;
}

function clearMessage(element) {
    element.textContent = "";
    element.className = "message";
}

loadPosts();
