export class LiveLogConsole {
    constructor(container) {
        this.container = container;
    }
    append(text) {
        this.container.textContent += text;
        this.container.scrollTop =
            this.container.scrollHeight;
    }
    clear() {
        this.container.textContent = "";
    }
}