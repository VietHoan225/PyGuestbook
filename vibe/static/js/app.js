// Tăng cường giao diện; trang vẫn hoạt động đầy đủ khi tắt JavaScript.

document.addEventListener("DOMContentLoaded", () => {
    setupToasts();
    setupDeleteConfirm();
    setupCharCount();
    setupSubmitLoading();
});

function dismissToast(toast) {
    if (toast.classList.contains("hiding")) return;
    toast.classList.add("hiding");
    toast.addEventListener("animationend", () => toast.remove(), { once: true });
    // Dự phòng khi tắt animation
    setTimeout(() => toast.remove(), 400);
}

function setupToasts() {
    document.querySelectorAll(".toast").forEach((toast) => {
        toast.querySelector(".toast-close")?.addEventListener("click", () => dismissToast(toast));
        setTimeout(() => dismissToast(toast), 4000);
    });
}

function setupDeleteConfirm() {
    const dialog = document.getElementById("confirm-dialog");
    if (!dialog || typeof dialog.showModal !== "function") return;

    const text = dialog.querySelector(".confirm-text");
    let pendingForm = null;

    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (form.dataset.confirmed) return;
            event.preventDefault();
            pendingForm = form;
            text.textContent = form.dataset.confirm;
            dialog.returnValue = "";
            dialog.showModal();
        });
    });

    dialog.addEventListener("close", () => {
        if (dialog.returnValue === "confirm" && pendingForm) {
            pendingForm.dataset.confirmed = "1";
            pendingForm.requestSubmit();
        }
        pendingForm = null;
    });

    // Bấm ra ngoài hộp thoại để đóng
    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) dialog.close("cancel");
    });
}

function setupCharCount() {
    document.querySelectorAll(".char-count[data-for]").forEach((counter) => {
        const field = document.getElementById(counter.dataset.for);
        if (!field) return;
        const max = Number(field.getAttribute("maxlength"));

        const update = () => {
            const length = field.value.length;
            counter.textContent = `${length}/${max}`;
            counter.classList.toggle("near-limit", length >= max * 0.9);
        };
        field.addEventListener("input", update);
        update();
    });
}

function setupSubmitLoading() {
    document.querySelectorAll("form.entry-form").forEach((form) => {
        form.addEventListener("submit", () => {
            const button = form.querySelector("[data-loading-text]");
            if (!button) return;
            button.disabled = true;
            button.textContent = button.dataset.loadingText;
        });
    });
}
