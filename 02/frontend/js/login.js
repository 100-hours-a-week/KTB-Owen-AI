const API_BASE_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");
const loginButton = document.getElementById("loginButton");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    message.textContent = "";
    message.className = "message";

    if (!username || !password) {
        showMessage("아이디와 비밀번호를 입력하세요.", "error");
        return;
    }

    try {
        loginButton.disabled = true;
        loginButton.textContent = "로그인 중...";

        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.detail || "로그인에 실패했습니다.", "error");
            return;
        }

        showMessage("로그인 성공", "success");

        localStorage.setItem("username", data.username);

        setTimeout(() => {
            window.location.href = "./board.html";
        }, 500);

    } catch (error) {
        showMessage("서버와 연결할 수 없습니다.", "error");
    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "로그인";
    }
});

function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;
}